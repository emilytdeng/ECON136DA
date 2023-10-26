from collections import Counter
from copy import copy
from typing import Optional

import pandas as pd


def deferred_acceptance(
    applicants_df: pd.DataFrame,
    firms_df: pd.DataFrame,
    firms_quota: dict,
    verbose: Optional[int] = 0,
) -> dict:
    """
    The deferred acceptance algorithm implementation.
    The process would be following:
    1. Create the initial environments for matching
    2. Start matching
    3. Count applications in firm

    Args:
        applicants_df: applicants dataframe
        firms_df: firms dataframe
        firms_quota: applicants quota in each firms
        verbose: verbose=0 (silent), else shows the number of iterations
    Return:
        dictionary of applicant - firm matches
    """
    # Create the initial environments for matching
    available_firm = {
        applicant: list(applicants_df.columns.values)
        for applicant in list(applicants_df.index.values)
    }
    unassigned_applicants = []
    matches = {}
    itr_count = 0

    # Start matching
    while len(unassigned_applicants) < len(applicants_df):
        for applicant in applicants_df.index:
            if applicant not in unassigned_applicants:
                firm = available_firm[applicant]
                best_choice = applicants_df.loc[applicant][
                    applicants_df.loc[applicant].index.isin(firm)
                ].idxmin()
                matches[(applicant, best_choice)] = (
                    applicants_df.loc[applicant][best_choice],
                    firms_df.loc[applicant][best_choice],
                )

        # Count applications in firm
        firms_applications = Counter([key[1] for key in matches.keys()])

        for firm in firms_applications.keys():
            if firms_applications[firm] > firms_quota[firm]:
                pairs_to_drop = sorted(
                    {
                        pair: matches[pair] for pair in matches.keys() if firm in pair
                    }.items(),
                    key=lambda x: x[1][1],
                )[1:]

                for p_to_drop in pairs_to_drop:
                    del matches[p_to_drop[0]]
                    _firm = copy(available_firm[p_to_drop[0][0]])
                    _firm.remove(p_to_drop[0][1])
                    available_firm[p_to_drop[0][0]] = _firm

        unassigned_applicants = [applicant[0] for applicant in matches.keys()]
        itr_count += 1

    if verbose != 0:
        print(f"Number of iterations: {itr_count}")

    return matches
