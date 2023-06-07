import random

# F = number of firms
# N = number of applicants
# r = weight of the first firm in an applicant's priority list, used to determine how similar the applicants' firm rankings will be

# generates applicant priority lists over firms using weights
# returns a dictionary
def applicants_rank_firms(applicants, firms, r):
    F = len(firms)
    N = len(applicants)

    # a dictionary representing each applicant's ranking of every firm where firms are identified by name
    app_rankings_of_firms = {}

    # compute weights using the rho
    if r == 1:
        # applicants will have dissimilar rankings of firms
        weights = [1 / F] * F
        print("weights1", weights)
    else:
        weights = []
        rx = (r - 1) / (r ** F - 1)
        for i in range(F):
            weights.append(rx * (r ** i))
        print("weights", weights)

    # returns a list, xP, containing each applicant's rankings of the firms
    for i in range(N):
        app_name = applicants[i]
        rankings = list(range(1, F + 1))
        random.shuffle(rankings)
        app_rankings_of_firms[app_name] = rankings

    # returns a dictionary in the format compatible with deferred_acceptance.py
    return app_rankings_of_firms
