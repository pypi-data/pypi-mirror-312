"""Compute hybrid profiles based on deviations from the mean profile.

This module provides tools to calculate threshold profiles driven by a combination
of standard deviation and relative thresholds derived from historical data.
The thresholds are designed to adapt to variability in the data, balancing stability
with tolerance for variability in consumption patterns.
"""

import pandas as pd

from energy_analysis_toolbox.timeseries.profiles.mean_profile import MeanProfile


class HybridThreshold(MeanProfile):
    """Returns the deviation from mean profile (hybrid std and relative thresholds)."""

    def __init__(
        self,
        offset_std: float = 3,
        offset_relative: float = 0.5,
        **kwargs,
    ) -> None:
        """Initialize HybridThreshold.

        Parameters
        ----------
        period : str, optional
            A pandas period string which specifies the kind of period on which
            the profile is realized.
        offset_std : float, optional
            Number of standard deviations VS the computed reference to obtain
            the threshold profile. Default is 3 (profile is 3 standard deviations
            from reference)
        offset_relative : float, optional
            Relative difference VS the computed reference to obtain
            the threshold profile. Default is 0.5 (profile is 150%
            of reference)

        """
        super().__init__(**kwargs)
        self.offset_std = offset_std
        self.offset_rel = offset_relative

    def compute(
        self,
        history: pd.Series,
        time: pd.Timestamp,
        **kwargs,
    ) -> pd.Series:
        """Return a threshold profile.

        The threshold profile is obtained using a user-defined relative variation
        from the mean profile built from history.

        Parameters
        ----------
        history : pd.Series
            Consumption history used to computed the reference
            profile.
        time : pd.Timestamp
            The time at which the profile is of interest. Only
            the information about the date is used in the passed
            timestamp.

        Returns
        -------
        profile : pd.Series
            Profile threshold with same resolution as the history data

        Notes
        -----
        The profile threshold is obtained as an hybrid between the std and
        arbitrary tshd profiles :

            - an average profile is computed from the rolling max of the history
              on a window centered on each slot with size ``window``.
            - a std profile is computed from the history (without rolling max)
            - the returned profile is obtained as the max between :

                * the profile based on ``tshd_std`` standard deviation over the
                  mean profile (the std is computed from the data without rolling
                  aggregation),
                * the profile based on ``(1 + tshd_rel)`` times the mean profile.

        The idea behind this profile is to base the threshold on the data variability,
        but to still have a certain tolerance when the consumption is very stable in
        the (short) history.

        The rolling max also artificially increases the mean value around slots where
        the consumption is high in order to account for the correlation between the
        consumption on consecutive slots : a certain "horizontal" dispersion of the
        consumption is relatively normal.


        .. note:

            In ``self.is_max == False``, replace "max" by "min" in the text above.

        """
        # rel and ref on smoothed data
        smooth_mean_profile = super().compute(history, time, **kwargs)
        rel_profile = smooth_mean_profile * self.offset_rel
        # std on unsmoothed data
        std_profile = self.group(history).std() * self.offset_std
        std_profile.index = rel_profile.index
        profile_deviations = pd.DataFrame.from_dict(
            {"std": std_profile, "tshd": rel_profile},
        )
        if self.is_max:
            var_profile = profile_deviations.max(axis=1)
        else:
            var_profile = profile_deviations.min(axis=1)
        return smooth_mean_profile + var_profile
