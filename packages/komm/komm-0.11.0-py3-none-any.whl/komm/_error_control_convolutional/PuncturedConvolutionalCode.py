import numpy as np
import numpy.typing as npt

from .._finite_state_machine.FiniteStateMachine import FiniteStateMachine
from .ConvolutionalCode import ConvolutionalCode


class PuncturedConvolutionalCode:
    r"""Punctured convolutional code. It is obtained by periodically deleting some of the bits from the output of a $(n, k)$ *mother [convolutional code](/ref/ConvolutionalCode)*. The *puncturing pattern* $\mathbf{\Pi}$ is an $n \times T$ binary matrix where each entry indicates whether a bit is kept ($1$) or deleted ($0$). The parameter $T$ is called the *puncturing period*. The resulting code has rate $R = (k T) / \wH({\mathbf{\Pi}})$, where $\wH({\mathbf{\Pi}})$ is the Hamming weight of the puncturing pattern. For more details, see <cite>LC04, Sec. 12.7</cite>.

    Parameters:
        mother_code: The mother convolutional code.
        puncture_matrix: The puncturing pattern $\mathbf{\Pi}$.

    Examples:
        Consider a mother convolutional code with parameters $(n, k) = (2, 1)$ and transfer function matrix $\mathbf{G}(D) = \begin{bmatrix}D^2 + 1 & D^2 + D + 1\end{bmatrix}$.

        If the puncturing pattern is given by
        $$
            \mathbf{\Pi} = \begin{bmatrix}
                1 & 0 \\\\
                1 & 1 \\\\
            \end{bmatrix},
        $$
        then the punctured convolutional code has rate $R = 2/3$.

        >>> mother_code = ConvolutionalCode(feedforward_polynomials=[[0b101, 0b111]])
        >>> puncture_matrix = np.array([[1, 0], [1, 1]])
        >>> punctured_code = PuncturedConvolutionalCode(mother_code, puncture_matrix)
        >>> punctured_code.puncturing_period
        2
        >>> punctured_code.rate
        0.6666666666666666

        If the puncturing pattern is given by
        $$
            \mathbf{\Pi} = \begin{bmatrix}
                1 & 0 & 1 \\\\
                1 & 1 & 0 \\\\
            \end{bmatrix},
        $$
        then the punctured convolutional code has rate $R = 3/4$.

        >>> mother_code = komm.ConvolutionalCode(feedforward_polynomials=[[0b101, 0b111]])
        >>> puncture_matrix = np.array([[1, 0, 1], [1, 1, 0]])
        >>> punctured_code = komm.PuncturedConvolutionalCode(mother_code, puncture_matrix)
        >>> punctured_code.puncturing_period
        3
        >>> punctured_code.rate
        0.75
    """

    def __init__(self, mother_code: ConvolutionalCode, puncture_matrix: npt.ArrayLike):
        self.mother_code = mother_code
        self.puncture_matrix = np.asarray(puncture_matrix)

    def __repr__(self) -> str:
        args = (
            f"(mother_code={self.mother_code}, "
            f"puncture_matrix={self.puncture_matrix.tolist()})"
        )
        return f"{self.__class__.__name__}{args}"

    @property
    def puncturing_period(self) -> int:
        r"""
        The puncturing period $T$.
        """
        return self.puncture_matrix.shape[1]

    @property
    def rate(self) -> float:
        r"""
        The rate $R$ of the punctured convolutional code.
        """
        k = self.mother_code.num_input_bits
        return k * self.puncturing_period / np.count_nonzero(self.puncture_matrix)

    @property
    def finite_state_machine(self) -> FiniteStateMachine:
        r"""
        The finite state machine of the punctured convolutional code.
        """
        return self.mother_code.finite_state_machine()
