from random import randint
from typing import Tuple

import numpy as np
import pandas as pd


def strict_preference_check(
    applicants_list: list,
    applicants_preferences: dict,
) -> None:
    """
    Check the strict order of applicant's preference over firms
    If a applicant's preference is not strict, it will raise an error

    Args:
        applicants_list: list of applicants
        applicants_preferences: applicants' preference dictionary
    """
    submitted_preference = []

    for applicant in applicants_list:
        for preference in applicants_preferences[applicant]:
            if preference not in submitted_preference:
                submitted_preference.append(preference)
            else:
                raise ValueError("The applicant's preference must be strictly ordered")

        submitted_preference = []


def create_dataframes(
    applicants_list: list,
    applicants_preferences: dict,
    firms_list: list,
    firms_preferences: dict,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Create applicants and firms dataframes

    Args:
        applicants_list: list of applicants
        applicants_preferences: applicants' preference dictionary
        firms_list: list of firms
        firms_preferences: firms' preference dictionary
    Return:
        tuple contains applicants_df and firms_df
    """
    strict_preference_check(applicants_list, applicants_preferences)

    applicants_df = pd.DataFrame(applicants_preferences)
    applicants_df.index = firms_list
    applicants_df = applicants_df.transpose()
    firms_df = pd.DataFrame(firms_preferences)
    firms_df.index = applicants_list

    return applicants_df, firms_df


def tie_break(firms_df: pd.DataFrame) -> pd.DataFrame:
    """
    This function randomly breaks the indifferent firms' preference over applicants
    and make their preference strict.

    Iterations:
    0. Iterate through each firm's preference
    1. Create a subset that contains the same ranked applicants
    2. Randomly order applicants in the same rank until all the applicants get the unique rank
    3. Merge all applicants with new order and assign new rank to them
    4. Merge all the firms' preferences

    Args:
        firms_df: firms' dataframe
    Return:
        new firms_df with strict preferences over applicants
    """
    new_firms_df = pd.DataFrame()
    # 0. Iterate through each firm's preference
    for firm in firms_df.columns:
        new_rank = pd.Series(dtype="int32")

        # 1. Create a subset that contains the same ranked applicants
        for rank in sorted(firms_df[firm].unique()):
            allocated_ranks = []
            sub_df = firms_df.loc[firms_df[firm] == rank, firm]

            # 2. Randomly order applicants in the same rank until all the applicants get the unique rank
            for applicant in sub_df.index:
                lottery = randint(1, len(sub_df))
                while lottery in allocated_ranks:
                    lottery = randint(1, len(sub_df))
                sub_df.loc[[applicant]] = lottery
                allocated_ranks.append(lottery)

            # 3. Merge all applicants with new order and assign new rank to them
            new_rank = pd.concat([new_rank, sub_df.sort_values()])

        # 4. Merge all the firms' preferences
        new_rank_df = pd.DataFrame(new_rank, columns=[firm])
        new_rank_df[firm] = np.arange(len(new_rank))
        new_firms_df[firm] = new_rank_df[firm]

    return new_firms_df
