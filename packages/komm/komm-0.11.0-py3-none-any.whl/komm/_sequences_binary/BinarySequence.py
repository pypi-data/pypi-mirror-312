from typing import Optional

import numpy as np
import numpy.typing as npt

from .._types import ArrayIntLike
from .._util.correlation import acorr, cyclic_acorr


class BinarySequence:
    r"""
    General binary sequence. It may be represented either in *bit format*, denoted by $b[n]$, with elements in the set $\\{ 0, 1 \\}$, or in *polar format*, denoted by $x[n]$, with elements in the set $\\{ \pm 1 \\}$. The correspondences $0 \mapsto +1$ and $1 \mapsto -1$ from bit format to polar format is assumed.

    The constructor expects either the bit sequence or the polar sequence.

    Parameters:
        bit_sequence: The binary sequence in bit format, $b[n] \in \\{ 0, 1 \\}$.
        polar_sequence: The binary sequence in polar format, $x[n] \in \\{ \pm 1 \\}$.

    Examples:
        >>> seq = komm.BinarySequence(bit_sequence=[0, 1, 1, 0])
        >>> seq.bit_sequence
        array([0, 1, 1, 0])
        >>> seq.polar_sequence
        array([ 1, -1, -1,  1])

        >>> seq = komm.BinarySequence(polar_sequence=[1, -1, -1, 1])
        >>> seq.bit_sequence
        array([0, 1, 1, 0])
        >>> seq.polar_sequence
        array([ 1, -1, -1,  1])
    """

    def __init__(
        self,
        bit_sequence: Optional[ArrayIntLike] = None,
        polar_sequence: Optional[ArrayIntLike] = None,
    ) -> None:
        if bit_sequence is not None and polar_sequence is None:
            self.bit_sequence = np.asarray(bit_sequence, dtype=int)
            self.polar_sequence = (-1) ** self.bit_sequence
        elif polar_sequence is not None and bit_sequence is None:
            self.polar_sequence = np.asarray(polar_sequence, dtype=int)
            self.bit_sequence = 1 * (self.polar_sequence < 0)
        else:
            raise ValueError("either specify 'bit_sequence' or 'polar_sequence'")

    def __repr__(self) -> str:
        args = f"bit_sequence={self.bit_sequence.tolist()}"
        return f"{self.__class__.__name__}({args})"

    @property
    def length(self) -> int:
        r"""
        The length (or period) $L$ of the binary sequence.
        """
        return self.bit_sequence.size

    def autocorrelation(
        self, shifts: Optional[ArrayIntLike] = None, normalized: bool = False
    ) -> npt.NDArray[np.float64]:
        r"""
        Returns the autocorrelation $R[\ell]$ of the binary sequence in polar format. See [`komm.acorr`](/ref/acorr) for more details.

        Parameters:
            shifts: See the corresponding parameter in [`komm.acorr`](/ref/acorr).
            normalized: See the corresponding parameter in [`komm.acorr`](/ref/acorr).

        Returns:
            The autocorrelation $R[\ell]$ of the binary sequence.

        Examples:
            >>> seq = komm.BinarySequence(bit_sequence=[0, 1, 1, 0])
            >>> seq.autocorrelation()
            array([ 4, -1, -2,  1])
        """
        return acorr(self.polar_sequence, shifts=shifts, normalized=normalized)

    def cyclic_autocorrelation(
        self, shifts: Optional[ArrayIntLike] = None, normalized: bool = False
    ) -> npt.NDArray[np.float64]:
        r"""
        Returns the cyclic autocorrelation $\tilde{R}[\ell]$ of the binary sequence in polar format. See [`komm.cyclic_acorr`](/ref/cyclic_acorr) for more details.

        Parameters:
            shifts: See the corresponding parameter in [`komm.cyclic_acorr`](/ref/cyclic_acorr).
            normalized: See the corresponding parameter in [`komm.cyclic_acorr`](/ref/cyclic_acorr).

        Returns:
            The cyclic autocorrelation $\tilde{R}[\ell]$ of the binary sequence.

        Examples:
            >>> seq = komm.BinarySequence(bit_sequence=[0, 1, 1, 0])
            >>> seq.cyclic_autocorrelation()
            array([ 4,  0, -4,  0])
        """
        return cyclic_acorr(self.polar_sequence, shifts=shifts, normalized=normalized)
