import numbers
from typing import Union, final, Any, TypeVar, Tuple, List

import numpy as np
from numpy.typing import ArrayLike

__all__ = ["Numeric", "Scalar", "Real", "ArrayLike", "NOTSET", "NOTSETTYPE", "T"]

Numeric = Union[int, float]

Scalar = Numeric

Real = numbers.Real

ArrayContainer = Union[Tuple[ArrayLike, ...], List[ArrayLike], np.ndarray]

@final
class NOTSETTYPE:
    """A type used as a sentinel for unspecified values."""
    
    def __copy__(self):
        return self
        
    def __deepcopy__(self, memo: Any):
        return self

NOTSET = NOTSETTYPE()

T = TypeVar('T')