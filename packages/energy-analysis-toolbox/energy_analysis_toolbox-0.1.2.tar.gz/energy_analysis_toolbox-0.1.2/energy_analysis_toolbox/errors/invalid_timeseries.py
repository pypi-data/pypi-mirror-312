"""Defines custom errors for time-series."""
from .base import EATError


class EATInvalidTimeseriesError(EATError):
    """A timeseries is inconsistent.

    This exception is used to notify a problem regarding the consistency of
    a timeseries definition.

    Derived classes may be inherited in order to deal with more specific problems.
    """


class EATUndefinedTimestepError(EATInvalidTimeseriesError):
    """A timestep is undefined in an interval-sampled timeseries.

    A timestep duration is undefined, either explicitly or implicitly in a
    timeseries which contain values defined "over overconsumption" (VS at
    instantaneous timestamps).
    """


class EATInvalidTimestepDurationError(EATInvalidTimeseriesError):
    """An invalid timestep duration has been passed for a timeseries.

    This exception is used when a timestep duration is encountered which does
    not comply with implicit or explicit assumptions about the possible timestep
    durations in a timeseries. Such assumptions could be :

    - durations are >=0,
    - durations have a specific value,
    - etc.

    """
