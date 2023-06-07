from scipy.stats import norm
import random
import math
import numpy as np

# randomly generates a resume score for each applicant from 1-100
def generate_resume_scores(applicants):
    # what we will return: a dictionary matching each applicant to their score
    scores = {}
    # for each applicant
    for applicant in applicants:
        # mean score is generated randomly
        scores[applicant] = random.randint(1, 100)
    return scores

# truncates the dictionary applicants to a top k% based on resume scores
def truncate(scores, keep):
    k = math.floor(keep * len(scores)) # how many applicants we will keep
    print("k", k)

    sorted_res_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True) # sort from highest to lowest
    sorted_res_scores = sorted_res_scores[:k] # only keep top k applicants based on their resume scores
    sorted_res_scores = dict(sorted_res_scores) # convert back to dictionary

    return sorted_res_scores # a truncated dictionary

