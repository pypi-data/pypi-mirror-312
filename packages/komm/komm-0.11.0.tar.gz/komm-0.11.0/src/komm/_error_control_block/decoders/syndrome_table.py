import numpy as np
import numpy.typing as npt

from ..._util import binlist2int
from ..BlockCode import BlockCode
from ..registry import RegistryBlockDecoder


def decode_syndrome_table(
    code: BlockCode,
    r: npt.ArrayLike,
) -> npt.NDArray[np.int_]:
    coset_leaders = code.coset_leaders()
    s = np.dot(code.check_matrix, r) % 2
    e_hat = coset_leaders[binlist2int(s)]
    v_hat = np.bitwise_xor(r, e_hat)
    return v_hat


RegistryBlockDecoder.register(
    "syndrome-table",
    {
        "description": "Syndrome table decoder",
        "decoder": decode_syndrome_table,
        "type_in": "hard",
        "type_out": "hard",
        "target": "codeword",
    },
)
