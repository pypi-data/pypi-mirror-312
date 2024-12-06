from collections.abc import Callable
from typing import Literal

import pandas as pd

from .conservative import (
    flow_rate_to_freq,
    volume_to_freq,
)
from .index_transformation import index_to_freq
from .interpolate import (
    piecewise_affine,
    piecewise_constant,
)

resampling_methods = (
    Literal[
        "piecewise_affine",
        "piecewise_constant",
        "volume_conservative",
        "flow_rate_conservative",
    ]
    | Callable[[pd.Series, pd.DatetimeIndex], pd.Series]
)


def to_freq(
    timeseries: "pd.Series[float]",
    freq: str,
    origin: Literal["floor", "ceil"] | pd.Timestamp | None = None,
    last_step_duration: float | None = None,
    method: resampling_methods = "piecewise_affine",
    **kwargs,
) -> "pd.Series[float]":
    """Return a timeseries resampled at a given frequency.

    Parameters
    ----------
    timeseries : pd.Series
        Series of values of a function of time, indexed using DateTimeIndex.
    freq : str
        Frequency of the resampled series. See :py:func:`pandas.Series.resample`
        for a list of possible values.
    origin : {None, 'floor', 'ceil', pd.Timestamp}, optional
        Origin of the resampling period. see :py:func:`.index_to_freq` for details.
    last_step_duration : {None, float}, optional
        Duration of the last time-step in `timeseries` in (s). See
        :py:func:`.index_to_freq` for details.
    method : str or callable, optional
        Method used to interpolate the values of the resampled series. The accepted
        values are:

        * 'piecewise_affine': uses :py:func:`.piecewise_affine`, assume the values a
          straight line between two points. The default method.
        * 'piecewise_constant': uses :py:func:`.piecewise_constant`, assume the values
          constant until the next point.
        * 'volume_conservative': uses :py:func:`.volume_to_freq`, conserve the quantity
          of the values. Best to use it for energy timeseries.
        * 'flow_rate_conservative': uses :py:func:`.flow_rate_to_freq`, conserve the
          values time the duration between two points. Best to use it for power
          timeseries.

        If a callable is passed, it must take a :py:class:`pandas.Series` as first
        argument and a :py:class:`pandas.DatetimeIndex` as second argument.
        See the interface of :py:func:`piecewise_affine` function.
        The default is 'piecewise_affine'.


    .. important::

        The various methods may manage extrapolation differently, so this situation
        should be avoided or managed with special care.

    Returns
    -------
    new_series : pd.Series
        Values of the series resampled at the given frequency.

    Examples
    --------
    This function can be used to resample timeseries of different physical nature
    with the right method depending on the physical quantity. For example, a
    timeseries of pointwise temperature can be resampled using piecewise affine
    interpolation:

    >>> new_temp = eat.timeseries.resample.to_freq(temperature, '1min',
    ... method='piecewise_affine')

    The same is true for an energy index :

    >>> new_index = eat.timeseries.resample.to_freq(temperature, '1min',
    ... method='piecewise_affine')

    Regarding a quantity that is conserved over time, such as a volume or a flow
    rate, the resampling should be done using a conservative method. For power and
    energy, dedicated functions exists, but this function can also be used:

    >>> new_volume = eat.timeseries.resample.to_freq(volume, '1min',
    ... method='volume_conservative')
    >>> new_flow_rate = eat.timeseries.resample.to_freq(flow_rate, '1min',
    ... method='flow_rate_conservative')

    See more examples of use in :doc:`/user_guide/Resampling_time_series`.


    """
    # Directly apply the method if it is a conservative method for which an
    # integrated method exists
    integrated_methods = {
        "volume_conservative": volume_to_freq,
        "flow_rate_conservative": flow_rate_to_freq,
    }
    try:
        method = integrated_methods[method]
    except KeyError:
        pass
    else:
        return method(
            timeseries,
            freq,
            origin=origin,
            last_step_duration=last_step_duration,
        )
    # Resample
    target_instants = index_to_freq(
        timeseries.index,
        freq,
        origin=origin,
        last_step_duration=last_step_duration,
    )
    # Ensure each method receives only its required parameters
    if method == "piecewise_constant":
        new_series = piecewise_constant(
            timeseries,
            target_instants,
            left_pad=kwargs.get("left_pad"),
        )
    elif method == "piecewise_affine":
        new_series = piecewise_affine(timeseries, target_instants)
    else:
        kwargs["freq"] = freq
        kwargs["origin"] = origin
        kwargs["last_step_duration"] = last_step_duration
        new_series = method(timeseries, target_instants, **kwargs)
    new_series.index.name = timeseries.index.name
    return new_series


def trim_out_of_bounds(
    data: pd.DataFrame | pd.Series,
    resampled_data: pd.DataFrame | pd.Series,
    fill_value: dict[str, any] | None = None,
) -> pd.DataFrame | pd.Series:
    """Fill resampled data with NA outside the boundaries of initial index.

    Parameters
    ----------
    data : pd.DataFrame or pd.Series
        The table of original data which has been resampled.
    resampled_data : pd.DataFrame or pd.Series
        The result of the resampling.
    fill_value : dict, optional
        A dictionary where keys are column names, and values are the placeholders
        used for samples outside the boundaries of the original index.
        If None, defaults to ``{'value': pd.NA}``.

    Returns
    -------
    resampled_data : pd.DataFrame or Series
        The passed resample data with placeholders set **inplace**.

    """
    if fill_value is None:
        fill_value = {"value": pd.NA}
    if resampled_data.index[0] < data.index[0]:
        for col, value in fill_value.items():
            resampled_data.loc[resampled_data.index < data.index[0], col] = value
    if resampled_data.index[-1] > data.index[-1]:
        for col, value in fill_value.items():
            resampled_data.loc[resampled_data.index > data.index[-1], col] = value
    return resampled_data
