from typing import AnyStr, Dict
import numpy as np


def add_to_dict_valuelist(dictionary: Dict, key: AnyStr, value) -> Dict:
    if key not in dictionary:
        dictionary[key] = [value]
    else:
        dictionary[key].append(value)

    return dictionary

def decodeMask(R):
    """
    Decode binary mask M encoded via run-length encoding.
    :param   R (object RLE)    : run-length encoding of binary mask
    :return: M (bool 2D array) : decoded binary mask
    """
    N = len(R['counts'])
    M = np.zeros( (R['size'][0]*R['size'][1], ), dtype=np.uint8)
    n = 0
    val = 1
    for pos in range(N):
        val = not val
        for c in range(R['counts'][pos]):
            M[n] = val
            n += 1
    return M.reshape((R['size']), order='F')