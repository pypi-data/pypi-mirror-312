"""Defines custom errors about resampling."""
from .base import EATEmptyDataError, EATError


class EATResamplingError(EATError):
    """A resampling operation is impossible.

    This base class is used when an invalid resampling operation is attempted in |eat|.
    Derived classed may be used for more specific resampling errors.
    """


class EATEmptySourceError(EATResamplingError, EATEmptyDataError):
    """Resampling an empty timeseries to specific instants is impossible.

    This exception is used when :

    - a resampling operation is undefined/meaningless when the source data is empty,
    - empty data is passed as source.

    """


class EATEmptyTargetsError(EATResamplingError, EATEmptyDataError):
    """Resampling a timeseries to empty targets is meaningless in this situation.

    This exception is used when :

    - a resampling operation is undefined/meaningless when the target instants
      set is empty,
    - empty data is passed as targets.

    """
