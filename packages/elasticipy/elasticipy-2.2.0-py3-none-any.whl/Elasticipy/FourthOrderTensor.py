import numpy as np
import re
from Elasticipy.StressStrainTensors import SecondOrderTensor, StrainTensor, StressTensor
from Elasticipy.SphericalFunction import SphericalFunction, HyperSphericalFunction
from scipy.spatial.transform import Rotation


def _parse_tensor_components(prefix, **kwargs):
    pattern = r'^{}(\d{{2}})$'.format(prefix)
    value = dict()
    for k, v in kwargs.items():
        match = re.match(pattern, k)  # Extract 'C11' to '11' and so
        if match:
            value[match.group(1)] = v
    return value


def voigt_indices(i, j):
    """
    Translate the two-index notation to one-index notation

    Parameters
    ----------
    i : int or np.ndarray
        First index
    j : int or np.ndarray
        Second index

    Returns
    -------
    Index in the vector of length 6
    """
    voigt_mat = np.array([[0, 5, 4],
                          [5, 1, 3],
                          [4, 3, 2]])
    return voigt_mat[i, j]


def unvoigt_index(i):
    """
    Translate the one-index notation to two-index notation

    Parameters
    ----------
    i : int or np.ndarray
        Index to translate
    """
    inverse_voigt_mat = np.array([[0, 0],
                                  [1, 1],
                                  [2, 2],
                                  [1, 2],
                                  [0, 2],
                                  [0, 1]])
    return inverse_voigt_mat[i]


def _compute_unit_strain_along_direction(S, m, n, transverse=False):
    m_vec = np.atleast_2d(m)
    n_vec = np.atleast_2d(n)
    if not isinstance(S, ComplianceTensor):
        S = S.inv()
    if np.any(np.linalg.norm(m_vec) < 1e-9) or np.any(np.linalg.norm(n_vec) < 1e-9):
        raise ValueError('The input vector cannot be zeros')
    m_vec = (m_vec.T / np.linalg.norm(m_vec, axis=1)).T
    n_vec = (n_vec.T / np.linalg.norm(n_vec, axis=1)).T

    indices = np.indices((3, 3, 3, 3))
    i, j, k, ell = indices[0], indices[1], indices[2], indices[3]
    dot = np.abs(np.einsum('ij,ij->i', m_vec, n_vec))
    if np.any(np.logical_and(dot > 1e-9, dot < (1 - 1e-9))):
        raise ValueError('The two directions must be either equal or orthogonal.')
    if transverse:
        cosine = m_vec[:, i] * m_vec[:, j] * n_vec[:, k] * n_vec[:, ell]
    else:
        cosine = m_vec[:, i] * n_vec[:, j] * m_vec[:, k] * n_vec[:, ell]
    return np.einsum('pijkl,ijkl->p', cosine, S.full_tensor())


def _matrixFromCrystalSymmetry(C11_C12_factor=0.5, component_prefix='C', symmetry='Triclinic', point_group=None,
                               diad='x', **kwargs):
    values = _parse_tensor_components(component_prefix, **kwargs)
    C = np.zeros((6, 6))
    symmetry = symmetry.lower()
    if ((symmetry == 'tetragonal') or (symmetry == 'trigonal')) and (point_group is None):
        raise ValueError('For tetragonal and trigonal symmetries, the point group is mandatory.')
    tetra_1 = ['-42m', '422', '4mm', '4/mm']
    tetra_2 = ['4', '-4', '4m']
    trigo_1 = ['32', '3m', '-3m']
    trigo_2 = ['3', '-3']
    if point_group is not None:
        if (point_group in tetra_1) or (point_group in tetra_2):
            symmetry = 'tetragonal'
        elif (point_group in trigo_1) or (point_group in trigo_2):
            symmetry = 'trigonal'
    try:
        if symmetry == 'isotropic':
            C[0, 0] = C[1, 1] = C[2, 2] = values['11']
            C[0, 1] = C[0, 2] = C[1, 2] = values['12']
            C[3, 3] = C[4, 4] = C[5, 5] = (C[0, 0] - C[0, 1]) * C11_C12_factor
        elif symmetry == 'cubic':
            C[0, 0] = C[1, 1] = C[2, 2] = values['11']
            C[0, 1] = C[0, 2] = C[1, 2] = values['12']
            C[3, 3] = C[4, 4] = C[5, 5] = values['44']
        elif symmetry == 'hexagonal':
            C[0, 0] = C[1, 1] = values['11']
            C[0, 1] = values['12']
            C[0, 2] = C[1, 2] = values['13']
            C[2, 2] = values['33']
            C[3, 3] = C[4, 4] = values['44']
            C[5, 5] = (C[0, 0] - C[0, 1]) * C11_C12_factor
        elif symmetry == 'tetragonal':
            C[0, 0] = C[1, 1] = values['11']
            C[0, 1] = values['12']
            C[0, 2] = C[1, 2] = values['13']
            C[2, 2] = values['33']
            C[3, 3] = C[4, 4] = values['44']
            C[5, 5] = values['66']
            if point_group in tetra_2:
                C[0, 5] = values['16']
                C[1, 5] = -C[0, 5]
        elif symmetry == 'trigonal':
            C[0, 0] = C[1, 1] = values['11']
            C[0, 1] = values['12']
            C[0, 2] = C[1, 2] = values['13']
            C[0, 3] = C[4, 5] = values['14']
            C[1, 3] = -C[0, 3]
            C[2, 2] = values['33']
            C[3, 3] = C[4, 4] = values['44']
            C[5, 5] = (C[0, 0] - C[0, 1]) * C11_C12_factor
            if point_group in trigo_2:
                C[1, 4] = values['25']
                C[3, 5] = C[1, 4]
                C[0, 4] = -C[1, 4]
        else:  # Orthorombic, monoclinic or triclinic
            C[0, 0], C[0, 1], C[0, 2] = values['11'], values['12'], values['13']
            C[1, 1], C[1, 2] = values['22'], values['23']
            C[2, 2] = values['33']
            C[3, 3], C[4, 4], C[5, 5] = values['44'], values['55'], values['66']
            if (symmetry == 'monoclinic') or (symmetry == 'triclinic'):
                if (symmetry == 'monoclinic') and (diad == 'x'):
                    C[0, 5], C[1, 5], C[2, 5] = values['16'], values['26'], values['36']
                    C[3, 4] = values['45']
                else:
                    C[0, 4], C[1, 4], C[2, 4] = values['15'], values['25'], values['35']
                    C[3, 5] = values['46']
                if symmetry == 'triclinic':
                    C[0, 3], C[1, 3], C[2, 3] = values['14'], values['24'], values['34']
                    C[0, 4], C[1, 4], C[2, 4] = values['15'], values['25'], values['35']
                    C[3, 5], C[4, 5] = values['46'], values['56']
        return C + np.tril(C.T, -1)
    except KeyError as key:
        entry_error = component_prefix + key.args[0]
        if (symmetry == 'tetragonal') or (symmetry == 'trigonal'):
            err_msg = "For point group {}, keyword argument {} is required".format(point_group, entry_error)
        elif symmetry == 'monoclinic':
            err_msg = "For {} symmetry with diag='{}', keyword argument {} is required".format(symmetry, diad,
                                                                                               entry_error)
        else:
            err_msg = "For {} symmetry, keyword argument {} is required".format(symmetry, entry_error)
        raise ValueError(err_msg)


def _isotropic_matrix(C11, C12, C44):
    return np.array([[C11, C12, C12, 0, 0, 0],
                     [C12, C11, C12, 0, 0, 0],
                     [C12, C12, C11, 0, 0, 0],
                     [0, 0, 0, C44, 0, 0],
                     [0, 0, 0, 0, C44, 0],
                     [0, 0, 0, 0, 0, C44]])


class SymmetricTensor:
    """
    Template class for manipulating symmetric fourth-order tensors.

    Attributes
    ----------
    matrix : np.ndarray
        (6,6) matrix gathering all the components of the tensor, using the Voigt notation.
    symmetry : str
        Symmetry of the tensor

    """
    tensor_name = 'Symmetric'
    voigt_map = np.ones((6, 6))
    C11_C12_factor = 0.5
    component_prefix = 'C'

    def __init__(self, M, phase_name='', symmetry='Triclinic', orientations=None):
        """
        Construct of stiffness tensor from a (6,6) matrix

        Parameters
        ----------
        M : np.ndarray
            (6,6) matrix corresponding to the stiffness tensor, written using the Voigt notation
        phase_name : str, default None
            Name to display
        symmetry : str, default Triclinic
        """
        self.matrix = np.array(M)
        self.phase_name = phase_name
        self.symmetry = symmetry
        self.orientations = orientations

    def __repr__(self):
        if self.phase_name == '':
            heading = '{} tensor (in Voigt notation):\n'.format(self.tensor_name)
        else:
            heading = '{} tensor (in Voigt notation) for {}:\n'.format(self.tensor_name, self.phase_name)
        print_symmetry = '\nSymmetry: {}'.format(self.symmetry)
        msg = heading + self.matrix.__str__() + print_symmetry
        if self.orientations is not None:
            msg = msg + '\n{} orientations'.format(len(self))
        return msg

    def __len__(self):
        if self.orientations is None:
            return ()
        elif self.orientations.single:
            return 1
        else:
            return len(self.orientations)

    def full_tensor(self):
        """
        Returns the full (unvoigted) tensor, as a [3, 3, 3, 3] array

        Returns
        -------
        np.ndarray
            Full tensor (4-index notation)
        """
        i, j, k, ell = np.indices((3, 3, 3, 3))
        ij = voigt_indices(i, j)
        kl = voigt_indices(k, ell)
        m = self.matrix[ij, kl] / self.voigt_map[ij, kl]
        if self.orientations is None:
            return m
        else:
            ori = self.orientations.as_matrix()
            rotated_tensors = np.einsum('qim,qjn,qko,qlp,mnop->qijkl', ori, ori, ori, ori, m)
            return rotated_tensors

    def rotate(self, rotation):
        """
        Apply a single rotation to a tensor, and return its component into the rotated frame.

        Parameters
        ----------
        rotation : Rotation
            Rotation to apply

        Returns
        -------
        SymmetricTensor
            Rotated tensor
        """
        rot_mat = rotation.as_matrix()
        rotated_tensor = np.einsum('im,jn,ko,lp,mnop->ijkl', rot_mat, rot_mat, rot_mat, rot_mat, self.full_tensor())
        ij, kl = np.indices((6, 6))
        i, j = unvoigt_index(ij).T
        k, ell = unvoigt_index(kl).T
        rotated_matrix = rotated_tensor[i, j, k, ell] * self.voigt_map[ij, kl]
        return self.__class__(rotated_matrix)

    def __add__(self, other):
        if isinstance(other, np.ndarray):
            if other.shape == (6, 6):
                mat = self.matrix + other
            elif other.shape == (3, 3, 3, 3):
                ten = self.full_tensor() + other
                ij, kl = np.indices((6, 6))
                i, j = unvoigt_index(ij).T
                k, ell = unvoigt_index(kl).T
                mat = ten[i, j, k, ell] * self.voigt_map[ij, kl]
            else:
                raise ValueError('The input argument must be either a 6x6 matrix or a (3,3,3,3) array.')
        elif isinstance(other, SymmetricTensor):
            if type(other) == type(self):
                mat = self.matrix + other.matrix
            else:
                raise ValueError('The two tensors to add must be of the same class.')
        else:
            raise ValueError('I don''t know how to add {} with {}.'.format(type(self), type(other)))
        return self.__class__(mat)

    def __sub__(self, other):
        if isinstance(other, SymmetricTensor):
            return self.__add__(-other.matrix)
        else:
            return self.__add__(-other)

    def __mul__(self, other):
        if isinstance(other, SecondOrderTensor):
            return SecondOrderTensor(self * other.matrix)
        elif isinstance(other, np.ndarray):
            if other.shape[-2:] == (3, 3):
                if self.orientations is None:
                    return np.einsum('ijkl,...kl->...ij', self.full_tensor(), other)
                else:
                    return np.einsum('qijkl,...kl->q...ij', self.full_tensor(), other)
        elif isinstance(other, Rotation):
            if other.single:
                return self.rotate(other)
            else:
                return self.__class__(self.matrix, symmetry=self.symmetry, orientations=other)
        else:
            return self.__class__(self.matrix * other, symmetry=self.symmetry)

    def __rmul__(self, other):
        if isinstance(other, (Rotation, float, int, np.number)):
            return self * other
        else:
            raise NotImplementedError('A fourth order tensor can be left-multiplied by rotations or scalar only.')

    def __truediv__(self, other):
        if isinstance(other, (float, int, np.number)):
            return self.__class__(self.matrix / other, symmetry=self.symmetry)
        else:
            raise NotImplementedError

    def _orientation_average(self, orientations):
        """
        Rotate the tensor by a series of rotations, then evaluate its mean value.

        Parameters
        ----------
        orientations : np.ndarray or Rotation
            If an array is provided, it must be of shape [m, 3, 3], where orientations[i,:,:] gives i-th the orientation
            matrix

        Returns
        -------
        SymmetricTensor
            Mean tensor

        """
        if isinstance(orientations, Rotation):
            orientations = orientations.as_matrix()
        if len(orientations.shape) == 2:
            raise ValueError('The orientation must be a 3x3 or a Nx3x3 matrix')
        elif len(orientations.shape) == 2:
            return self * orientations
        else:
            m = orientations
            mean_full_tensor = np.mean(self.full_tensor(), axis=0)
            ij, kl = np.indices((6, 6))
            i, j = unvoigt_index(ij).T
            k, ell = unvoigt_index(kl).T
            rotated_matrix = mean_full_tensor[i, j, k, ell] * self.voigt_map[ij, kl]
            return self.__class__(rotated_matrix)

    @classmethod
    def fromCrystalSymmetry(cls, symmetry='Triclinic', point_group=None, diad='x', phase_name=None, **kwargs):
        """
        Create a fourth-order tensor from limited number of components, taking advantage of crystallographic symmetries

        Parameters
        ----------
        symmetry : str, default Triclinic
            Name of the crystallographic symmetry
        point_group : str
            Point group of the considered crystal. Only used (and mandatory) for tetragonal and trigonal symmetries.
        diad : str {'x', 'y'}, default 'x'
            Alignment convention. Sets whether x||a or y||b. Only used for monoclinic symmetry.
        phase_name : str, default None
            Name to use when printing the tensor
        kwargs
            Keywords describing all the necessary components, depending on the crystal's symmetry and the type of tensor.
            For Stiffness, they should be named as 'Cij' (e.g. C11=..., C12=...).
            For Comliance, they should be named as 'Sij' (e.g. S11=..., S12=...).
            See examples below.

        Returns
        -------
        FourthOrderTensor

        See Also
        --------
        StiffnessTensor.isotropic : creates an isotropic stiffness tensor from two paremeters (e.g. E and v).

        Notes
        -----
        The relationships between the tensor's components depend on the crystallogrpahic symmetry [1]_.

        References
        ----------
        .. [1] Nye, J. F. Physical Properties of Crystals. London: Oxford University Press, 1959.

        Examples
        --------
        >>> from Elasticipy.FourthOrderTensor import StiffnessTensor\n
        >>> StiffnessTensor.fromCrystalSymmetry(symmetry='monoclinic', diad='y', phase_name='TiNi',
        ...                                     C11=231, C12=127, C13=104,
        ...                                     C22=240, C23=131, C33=175,
        ...                                     C44=81, C55=11, C66=85,
        ...                                     C15=-18, C25=1, C35=-3, C46=3)
        Stiffness tensor (in Voigt notation) for TiNi:
        [[231. 127. 104.   0. -18.   0.]
         [127. 240. 131.   0.   1.   0.]
         [104. 131. 175.   0.  -3.   0.]
         [  0.   0.   0.  81.   0.   3.]
         [-18.   1.  -3.   0.  11.   0.]
         [  0.   0.   0.   3.   0.  85.]]
        Symmetry: monoclinic

        >>> from Elasticipy.FourthOrderTensor import ComplianceTensor\n
        >>> ComplianceTensor.fromCrystalSymmetry(symmetry='monoclinic', diad='y', phase_name='TiNi',
        ...                                      S11=8, S12=-3, S13=-2,
        ...                                      S22=8, S23=-5, S33=10,
        ...                                      S44=12, S55=116, S66=12,
        ...                                      S15=14, S25=-8, S35=0, S46=0)
        Compliance tensor (in Voigt notation) for TiNi:
        [[  8.  -3.  -2.   0.  14.   0.]
         [ -3.   8.  -5.   0.  -8.   0.]
         [ -2.  -5.  10.   0.   0.   0.]
         [  0.   0.   0.  12.   0.   0.]
         [ 14.  -8.   0.   0. 116.   0.]
         [  0.   0.   0.   0.   0.  12.]]
        Symmetry: monoclinic
        """
        matrix = _matrixFromCrystalSymmetry(C11_C12_factor=cls.C11_C12_factor, component_prefix=cls.component_prefix,
                                            point_group=point_group, diad=diad, symmetry=symmetry, **kwargs)
        return cls(matrix, symmetry=symmetry, phase_name=phase_name)


class StiffnessTensor(SymmetricTensor):
    """
    Class for manipulating fourth-order stiffness tensors.
    """
    tensor_name = 'Stiffness'
    C11_C12_factor = 0.5

    def __init__(self, S, **kwargs):
        super().__init__(S, **kwargs)

    def __mul__(self, other):
        if isinstance(other, StrainTensor):
            new_tensor = super().__mul__(other)
            return StressTensor(new_tensor.matrix)
        elif isinstance(other, StressTensor):
            raise ValueError('You cannot multiply a stiffness tensor with a Stress tensor.')
        else:
            return super().__mul__(other)

    def inv(self):
        """
        Compute the reciprocal compliance tensor

        Returns
        -------
        ComplianceTensor
            Reciprocal tensor
        """
        C = np.linalg.inv(self.matrix)
        return ComplianceTensor(C, symmetry=self.symmetry, phase_name=self.phase_name, orientations=self.orientations)

    @property
    def Young_modulus(self):
        """
        Directional Young's modulus

        Returns
        -------
        SphericalFunction
            Young's modulus
        """

        def compute_young_modulus(n):
            eps = _compute_unit_strain_along_direction(self, n, n)
            return 1 / eps

        return SphericalFunction(compute_young_modulus)

    @property
    def shear_modulus(self):
        """
        Directional shear modulus

        Returns
        -------
        HyperSphericalFunction
            Shear modulus
        """

        def compute_shear_modulus(m, n):
            eps = _compute_unit_strain_along_direction(self, m, n)
            return 1 / (4 * eps)

        return HyperSphericalFunction(compute_shear_modulus)

    @property
    def Poisson_ratio(self):
        """
        Directional Poisson's ratio

        Returns
        -------
        HyperSphericalFunction
            Poisson's ratio
        """

        def compute_PoissonRatio(m, n):
            eps1 = _compute_unit_strain_along_direction(self, m, m)
            eps2 = _compute_unit_strain_along_direction(self, m, n, transverse=True)
            return -eps2 / eps1

        return HyperSphericalFunction(compute_PoissonRatio)

    def Voigt_average(self):
        """
        Compute the Voigt average of the stiffness tensor. If the tensor contains no orientation, we assume isotropic
        behaviour. Otherwise, the mean is computed over all orientations.

        Returns
        -------
        StiffnessTensor
            Voigt average of stiffness tensor

        See Also
        --------
        Reuss_average : compute the Reuss average
        Hill_average : compute the Voigt-Reuss-Hill average
        """
        if self.orientations is None:
            c = self.matrix
            C11 = (c[0, 0] + c[1, 1] + c[2, 2]) / 5 \
                  + (c[0, 1] + c[0, 2] + c[1, 2]) * 2 / 15 \
                  + (c[3, 3] + c[4, 4] + c[5, 5]) * 4 / 15
            C12 = (c[0, 0] + c[1, 1] + c[2, 2]) / 15 \
                  + (c[0, 1] + c[0, 2] + c[1, 2]) * 4 / 15 \
                  - (c[3, 3] + c[4, 4] + c[5, 5]) * 2 / 15
            C44 = (c[0, 0] + c[1, 1] + c[2, 2] - c[0, 1] - c[0, 2] - c[1, 2]) / 15 + (c[3, 3] + c[4, 4] + c[5, 5]) / 5
            mat = _isotropic_matrix(C11, C12, C44)
            return StiffnessTensor(mat, symmetry='isotropic', phase_name=self.phase_name)
        else:
            return self._orientation_average(self.orientations)

    def Reuss_average(self):
        """
        Compute the Reuss average of the stiffness tensor. If the tensor contains no orientation, we assume isotropic
        behaviour. Otherwise, the mean is computed over all orientations.

        Returns
        -------
        StiffnessTensor
            Reuss average of stiffness tensor

        See Also
        --------
        Voigt_average : compute the Voigt average
        Hill_average : compute the Voigt-Reuss-Hill average
        """
        return self.inv().Reuss_average().inv()

    def Hill_average(self):
        """
        Compute the (Voigt-Reuss-)Hill average ofthe stiffness tensor. If the tensor contains no orientation, we assume
        isotropic behaviour. Otherwise, the mean is computed over all orientations.

        Parameters
        ----------
        orientations : np.ndarray or None
            Set of m orientation matrices, defined as a [m, 3, 3] array.
            If None, uniform distribution is assumed, resulting in isotropic tensor

        Returns
        -------
        StiffnessTensor
            Voigt-Reuss-Hill average of tensor

        See Also
        --------
        Voigt_average : compute the Voigt average
        Reuss_average : compute the Reuss average
        """
        Reuss = self.Reuss_average()
        Voigt = self.Voigt_average()
        return (Reuss + Voigt) * 0.5

    @classmethod
    def isotropic(cls, E=None, nu=None, lame1=None, lame2=None, phase_name=None):
        """
        Create an isotropic stiffness tensor from two elasticity coefficients, namely: E, nu, lame1, or lame2. Exactly
        two of these coefficients must be provided.

        Parameters
        ----------
        E : float, None
            Young modulus
        nu : float, None
            Poisson ratio
        lame1 : float, None
            First Lamé coefficient
        lame2 : float, None
            Second Lamé coefficient
        phase_name : str, None
            Name to print

        Returns
        -------
            Corresponding isotropic stiffness tensor

        Examples
        --------
        On can check that the shear modulus for steel is around 82 GPa:

        >>> from Elasticipy.FourthOrderTensor import StiffnessTensor
        >>> C=StiffnessTensor.isotropic(E=210e3, nu=0.28)
        >>> C.shear_modulus
        Hyperspherical function
        Min=82031.24999999991, Max=82031.24999999997
        """
        argument_vector = np.array([E, nu, lame1, lame2])
        if np.count_nonzero(argument_vector) != 2:
            raise ValueError("Exactly two values are required among E, nu, lame1 and lame2.")
        if E is not None:
            if nu is not None:
                lame1 = E * nu / ((1 + nu) * (1 - 2 * nu))
                lame2 = E / (1 + nu) / 2
            elif lame1 is not None:
                R = np.sqrt(E ** 2 + 9 * lame1 ** 2 + 2 * E * lame1)
                lame2 = (E - 3 * lame1 + R) / 4
            elif lame2 is not None:
                lame1 = lame2 * (E - 2 * lame2) / (3 * lame2 - E)
            else:
                raise ValueError('Either nu, lame1 or lame2 must be provided.')
        elif nu is not None:
            if lame1 is not None:
                lame2 = lame1 * (1 - 2 * nu) / (2 * nu)
            elif lame2 is not None:
                lame1 = 2 * lame2 * nu / (1 - 2 * nu)
            else:
                raise ValueError('Either lame1 or lame2 must be provided.')
        C11 = lame1 + 2 * lame2
        C12 = lame1
        C44 = lame2
        matrix = _isotropic_matrix(C11, C12, C44)
        return StiffnessTensor(np.array(matrix), symmetry='isotropic', phase_name=phase_name)

    def Christoffel_tensor(self, u):
        """
        Create the Christoffel tensor along a given direction, or set or directions.

        Parameters
        ----------
        u : list or np.ndarray
            3D direction(s) to compute the Christoffel tensor along with

        Returns
        -------
        Gamma : np.ndarray
            Array of Christoffel tensor(s). if u is a list of directions, Gamma[i] is the Christoffel tensor for
            direction  u[i].

        See Also
        --------
        wave_velocity : computes the p- and s-wave velocities.

        Notes
        -----
        For a given stiffness tensor **C** and a given unit vector **u**, the Christoffel tensor is defined as [2]_ :

            .. math:: M_{ij} = C_{iklj}.u_k.u_l

        """
        u_vec = np.atleast_2d(u)
        u_vec = (u_vec.T/np.linalg.norm(u_vec, axis=1)).T
        return np.einsum('inmj,pn,pm->pij', self.full_tensor(), u_vec, u_vec)

    def wave_velocity(self, rho):
        """
        Compute the wave velocities, given the mass density.

        Parameters
        ----------
        rho : float
            mass density. Its unit must be consistent with that of the stiffness tensor. See notes for hints.

        See Also
        --------
        ChristoffelTensor : Computes the Christoffel tensor along a given direction

        Returns
        -------
        c_p : SphericalFunction
            Velocity of the primary (compressive) wave
        c_s1 : SphericalFunction
            Velocity of the fast secondary (shear) wave
        c_s2 : SphericalFunction
            Velocity of the slow secondary (shear) wave

        Notes
        -----
        The estimation of the wave velocities is made by finding the eigenvalues of the Christoffel tensor [2]_.

        One should double-check the units. The table below provides hints about the unit you get, depending on the units
        you use for stiffness and the mass density:

        +-----------------+--------------+------------+-----------------------+
        | Stiffness       | Mass density | Velocities | Notes                 |
        +=================+==============+============+=======================+
        | Pa (N/m²)       | kg/m³        | m/s        | SI units              |
        +-----------------+--------------+------------+-----------------------+
        | GPa (10⁹ Pa)    | kg/dm³       | km/s       | Conversion factor     |
        +-----------------+--------------+------------+-----------------------+
        | GPa (10³ N/mm²) | kg/mm³       | m/s        | Consistent units      |
        +-----------------+--------------+------------+-----------------------+
        | MPa (10⁶ Pa)    | kg/m³        | km/s       | Conversion factor     |
        +-----------------+--------------+------------+-----------------------+
        | MPa (10³ N/mm²) | g/mm³        | m/s        | Consistent units      |
        +-----------------+--------------+------------+-----------------------+

        References
        ----------
        .. [2] J. W. Jaeken, S. Cottenier, Solving the Christoffel equation: Phase and group velocities, Computer Physics
               Communications (207), 2016, https://doi.org/10.1016/j.cpc.2016.06.014.

        """
        def make_fun(index):
            def fun(n):
                Gamma = self.Christoffel_tensor(n)
                eig, _ = np.linalg.eig(Gamma)
                if index == 0:
                    eig_of_interest = np.max(eig, axis=-1)
                elif index == 1:
                    eig_of_interest = np.median(eig, axis=-1)
                else:
                    eig_of_interest = np.min(eig, axis=-1)
                return np.sqrt(eig_of_interest/rho)
            return fun
        return [SphericalFunction(make_fun(i)) for i in range(3)]


class ComplianceTensor(StiffnessTensor):
    """
    Class for manipulating compliance tensors
    """
    tensor_name = 'Compliance'
    voigt_map = np.vstack((
        np.hstack((np.ones((3, 3)), 2 * np.ones((3, 3)))),
        np.hstack((2 * np.ones((3, 3)), 4 * np.ones((3, 3))))
    ))
    C11_C12_factor = 2.0
    component_prefix = 'S'

    def __init__(self, C, **kwargs):
        super().__init__(C, **kwargs)

    def __mul__(self, other):
        if isinstance(other, StressTensor):
            return StrainTensor(self * other.matrix)
        elif isinstance(other, StrainTensor):
            raise ValueError('You cannot multiply a compliance tensor with Strain tensor.')
        else:
            return super().__mul__(other)

    def inv(self):
        """
        Compute the reciprocal stiffness tensor

        Returns
        -------
        StiffnessTensor
            Reciprocal tensor
        """
        S = np.linalg.inv(self.matrix)
        return StiffnessTensor(S, symmetry=self.symmetry, phase_name=self.phase_name, orientations=self.orientations)

    def Reuss_average(self):
        if self.orientations is None:
            s = self.matrix
            S11 = (s[0, 0] + s[1, 1] + s[2, 2]) / 5 \
                  + (s[0, 1] + s[0, 2] + s[1, 2]) * 2 / 15 \
                  + (s[3, 3] + s[4, 4] + s[5, 5]) * 1 / 15
            S12 = (s[0, 0] + s[1, 1] + s[2, 2]) / 15 \
                  + (s[0, 1] + s[0, 2] + s[1, 2]) * 4 / 15 \
                  - (s[3, 3] + s[4, 4] + s[5, 5]) * 1 / 30
            S44 = ((s[0, 0] + s[1, 1] + s[2, 2] - s[0, 1] - s[0, 2] - s[1, 2]) * 4 / 15 +
                   (s[3, 3] + s[4, 4] + s[5, 5]) / 5)
            mat = _isotropic_matrix(S11, S12, S44)
            return ComplianceTensor(mat, symmetry='isotropic', phase_name=self.phase_name)
        else:
            return self._orientation_average(self.orientations)

    def Voigt_average(self):
        return self.inv().Voigt_average().inv()

    def Hill_average(self):
        return self.inv().Hill_average()

    @classmethod
    def isotropic(cls, **kwargs):
        """
        Create an isotropic compliance tensor for either E, nu, lame1 or lame2. Exactly two of these parameters must be
        provided.

        Parameters
        ----------
        kwargs : keyword arguments
            E, nu, lame1 or lame2, passed to the StiffnessTensor.isotropic constructor

        See Also
        --------
        fromCrystalSymmetry : Define a stiffness tensor, taking advantage of crystal symmetry
        """
        return StiffnessTensor.isotropic(**kwargs).inv()

