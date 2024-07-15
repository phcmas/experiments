import time
import numpy as np


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # 함수 실행 전 시간
        result = func(*args, **kwargs)  # 실제 함수 호출
        end_time = time.perf_counter()  # 함수 실행 후 시간
        print(f"Function {func.__name__} took {end_time - start_time:.4f} seconds to complete.")
        return result

    return wrapper


def generate_one_logit(type_count: int):
    alpha = np.ones(type_count)
    excluding_last = np.round(np.random.dirichlet(alpha), 3).tolist()[:-1]
    last = max(round(1 - sum(excluding_last), 3), 0)

    return excluding_last + [last]


def generate_logits(type_count: int, stage_count: int):
    return [generate_one_logit(type_count) for _ in range(stage_count)]


@timeit
def convert_logits(logits: list[list[float]]):
    return [max(enumerate(logit), key=lambda x: x[1])[0] for logit in logits]


def main():
    # fmt: on
    logits0 = generate_logits(4, 1200)
    logits1 = generate_logits(4, 1200)
    logits2 = generate_logits(4, 1200)
    logits3 = generate_logits(4, 1200)

    convert_logits(logits0)
    convert_logits(logits1)
    convert_logits(logits2)
    convert_logits(logits3)


main()
