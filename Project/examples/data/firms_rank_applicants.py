
from scipy.stats import norm

# generates an interview score for all the candidates by all the firms (candidates who made the resume cut-off)
# takes in the list of firms as well as a dictionary of top candidates and their resume scores
def generate_cumulative_scores(firms, top_scores):
    cumulative_scores = {} # a dictionary of interview scores for all the qualified applicants for all the firms
    for firm in firms:
        firm_cumulative_scores = {} # a dictionary of interview scores for just one firm
        for applicant, res_score in top_scores.items():
            interview_score = norm.rvs(loc=res_score, scale=5, size=1)[0] # sample from a gaussian dist where mean is original resume score
            firm_cumulative_scores[applicant] = interview_score + top_scores[applicant] # add up interview score and original resume score
        cumulative_scores[firm] = firm_cumulative_scores # how this specific firm scored the qualified applicants
    return cumulative_scores

# sorts the dictionary of interview scores
# converts the dictionary of dictionaries into a dictionary of lists
def convert_to_preferences(applicants, cumulative_scores):
    converted_score_preferences = {} # what we will return
    for firm, scores in cumulative_scores.items():
        sorted_interview_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True) # sort the list of interview scores by highest to lowest
        #print("sorted_interview_scores", sorted_interview_scores)
        applicant_preferences = []
        for applicant in sorted_interview_scores: # for each applicant in the sorted list
            index = applicants.index(applicant[0]) + 1 # find their place in the top_applicants list
            applicant_preferences.append(index)
        converted_score_preferences[firm] = applicant_preferences # preferences for this specific firm
    return converted_score_preferences
