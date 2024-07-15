import string
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


def measure_the_size_for_logits(hour: int):
    logits_count = int(hour * 60 * 60 / 30)

    sleep_logits = generate_logits(4, logits_count)
    osa_logits = generate_logits(3, logits_count)
    snoring_logits = generate_logits(2, logits_count)

    sleep_logits_size = len(str(sleep_logits).encode("utf-8"))
    osa_logits_size = len(str(osa_logits).encode("utf-8"))
    snoring_logits_size = len(str(snoring_logits).encode("utf-8"))

    print(f"sleep logits for {hour} hours: {sleep_logits_size} bytes")
    print(f"osa logits for {hour} hours: {osa_logits_size} bytes")
    print(f"snoring logits for {hour} hours: {snoring_logits_size} bytes")
    print(f"total: {sleep_logits_size + osa_logits_size + snoring_logits_size} bytes")
    print()


def measure_the_time_of_conversion(hour: int):
    logits_count = int(hour * 60 * 60 / 30)

    # sleep logits
    logits0 = generate_logits(4, logits_count)
    logits1 = generate_logits(4, logits_count)
    logits2 = generate_logits(4, logits_count)
    logits3 = generate_logits(4, logits_count)

    # osa logits - 10 hours
    logits4 = generate_logits(3, logits_count)
    logits5 = generate_logits(3, logits_count)
    logits6 = generate_logits(3, logits_count)
    logits7 = generate_logits(3, logits_count)

    # snoring logits - 10 hours
    logits8 = generate_logits(2, logits_count)
    logits9 = generate_logits(2, logits_count)
    logits10 = generate_logits(2, logits_count)
    logits11 = generate_logits(2, logits_count)

    print(f"converting sleep logits for {hour} hours...")
    convert_logits(logits0)
    convert_logits(logits1)
    convert_logits(logits2)
    convert_logits(logits3)

    print(f"converting osa logits for {hour} hours...")
    convert_logits(logits4)
    convert_logits(logits5)
    convert_logits(logits6)
    convert_logits(logits7)

    print(f"converting snoring logits for {hour} hours...")
    convert_logits(logits8)
    convert_logits(logits9)
    convert_logits(logits10)
    convert_logits(logits11)

    print()


def main():
    measure_the_size_for_logits(10)
    measure_the_time_of_conversion(10)


main()
