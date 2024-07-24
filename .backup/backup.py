import numpy as np


def generate_one_logit(type_count: int, decimal_point: int):
    alpha = np.ones(type_count)
    # excluding_last = np.round(np.random.dirichlet(alpha), decimal_point).tolist()[:-1]
    excluding_last = np.random.dirichlet(alpha).tolist()[:-1]
    last = max(round(1 - sum(excluding_last), decimal_point), 0)

    return excluding_last + [last]
