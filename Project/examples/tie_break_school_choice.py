from deferred_acceptance.deferred_acceptance import deferred_acceptance
from deferred_acceptance.utils import create_dataframes, tie_break


def tie_break_firm_choice() -> None:
    """
    This example shows how the deferred acceptance algorithm works with the random tie-breaking mechanism.
    """
    # Prepare the dataframes
    applicants_list = ["a", "b", "c", "d"]
    firms_list = ["A", "B", "C"]
    applicants_preferences = {
        "a": [1, 2, 3],
        "b": [2, 3, 1],
        "c": [3, 2, 1],
        "d": [2, 1, 3],
    }
    firms_preferences = {"A": [1, 1, 1, 4], "B": [1, 3, 3, 1], "C": [2, 2, 2, 2]}

    applicants_df, firms_df = create_dataframes(
        applicants_list=applicants_list,
        applicants_preferences=applicants_preferences,
        firms_list=firms_list,
        firms_preferences=firms_preferences,
    )

    # Break the "tie" and make the firms' preference strict
    strict_firm_df = tie_break(firms_df)

    # Run the algorithm
    firms_quota = {"A": 1, "B": 2, "C": 1}
    matches = deferred_acceptance(
        applicants_df=applicants_df,
        firms_df=strict_firm_df,
        firms_quota=firms_quota,
    )

    print(matches)


if __name__ == "__main__":
    tie_break_firm_choice()
