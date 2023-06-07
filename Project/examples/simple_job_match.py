from deferred_acceptance.deferred_acceptance import deferred_acceptance
from deferred_acceptance.utils import create_dataframes
from data.applicants_rank_firms import applicants_rank_firms
from data.generate_resume import generate_resume_scores, truncate
from data.firms_rank_applicants import generate_cumulative_scores, convert_to_preferences


def simple_job_match() -> None:
    """
    Here is a minimalistic example of deferred acceptance for the consulting market
    """
    # Names
    applicants_list = ["emily", "shaurya", "melina", "ellie", "lea", "logan", "natalia", "riley", "maya", "lindsay"] 
    firms_list = ["Vain & Company", "VCG", "McKidney & Company"]

    # generate resume scores for each applicant (all firms score resumes identically)
    res_scores = generate_resume_scores(applicants_list)
    print("res_scores", res_scores)
    # based on resume scores, only keep top x percent of applicants
    top_scores = truncate(res_scores, .4)
    print("top scores", top_scores)
    top_applicants = list(top_scores.keys())
    print("top applicants", top_applicants)
    firms_preferences = convert_to_preferences(top_applicants, generate_cumulative_scores(firms_list, top_scores))
    print("firms preferences", firms_preferences)
    applicants_preferences = applicants_rank_firms(top_applicants, firms_list, .0001)
    print("applicants preferences", applicants_preferences)

    applicants_df, firms_df = create_dataframes(
        applicants_list=top_applicants,
        applicants_preferences=applicants_preferences,
        firms_list=firms_list,
        firms_preferences=firms_preferences,
    )

    # Run the algorithm
    firms_quota = {"Vain & Company": 2, "VCG": 9, "McKidney & Company": 1}
    matches = deferred_acceptance(
        applicants_df=applicants_df, firms_df=firms_df, firms_quota=firms_quota
    )

    print("matches", matches)


if __name__ == "__main__":
    simple_job_match()
