import base64
import time
import numpy as np
import struct
from pydantic import BaseModel, ConfigDict


class InputPayload(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    session_id: str
    db_type: str = "MAIN"

    sleep_stage_logits: np.ndarray
    osa_logits: np.ndarray
    snoring_logits: np.ndarray

    callback_url: str = "http://test-api.asleep.ai/data"
    callback_version: str = "V2"


def timeit(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # 함수 실행 전 시간
        result = func(*args, **kwargs)  # 실제 함수 호출
        end_time = time.perf_counter()  # 함수 실행 후 시간
        print(f"Function {func.__name__} took {end_time - start_time:.4f} seconds to complete.")
        return result

    return wrapper


def generate_logits(type_count: int, stage_count: int, decimal_point: int = -1) -> np.ndarray:
    if decimal_point == -1:
        return np.random.rand(stage_count, type_count).astype(np.float32)
    else:
        return np.round(np.random.rand(stage_count, type_count).astype(np.float32), decimal_point)


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


def array_to_base64_2d(array):
    # Convert the 2D list of floats to a 1D byte array
    byte_array = b"".join(struct.pack("f", item) for row in array for item in row)

    # Encode the byte array to Base64
    base64_encoded = base64.b64encode(byte_array)

    # Convert the Base64 bytes to a string
    return base64_encoded.decode("utf-8")


def array_to_utf8_2d(array):
    as_str = "[" + ",".join(map(str, array)) + "]"
    return as_str.encode("utf-8")


def base64_to_array_2d(base64_string, num_rows, num_cols):
    # Decode the Base64 string to bytes
    byte_array = base64.b64decode(base64_string)

    num_floats = len(byte_array) // struct.calcsize("f")
    floats = [
        struct.unpack("f", byte_array[i * struct.calcsize("f") : (i + 1) * struct.calcsize("f")])[0]
        for i in range(num_floats)
    ]

    # Reconstruct the 2D list from the list of floats
    return [floats[i * num_cols : (i + 1) * num_cols] for i in range(num_rows)]


def encode_and_decode_logits_base64():
    sleep_logits = generate_logits(4, 1200)
    osa_logits = generate_logits(3, 1200)
    snoring_logits = generate_logits(2, 1200)

    # Encode the list of floats to Base64
    sleep_logits_base64 = array_to_base64_2d(sleep_logits)
    osa_logits_base64 = array_to_base64_2d(osa_logits)
    snoring_logits_base64 = array_to_base64_2d(snoring_logits)

    print(f"sleep logits base64: {len(sleep_logits_base64)}")
    print(f"osa logits base64: {len(osa_logits_base64)}")
    print(f"snoring logits base64: {len(snoring_logits_base64)}")
    print(f"total: {len(snoring_logits_base64) + len(osa_logits_base64) + len(snoring_logits_base64)}")

    # Decode the Base64 string back to the list of floats
    sleep_logits_decoded = base64_to_array_2d(sleep_logits_base64, num_rows=1200, num_cols=4)
    osa_logits_decoded = base64_to_array_2d(osa_logits_base64, num_rows=1200, num_cols=3)
    snoring_logits_decoded = base64_to_array_2d(snoring_logits_base64, num_rows=1200, num_cols=2)

    print(f"sleep logits decoded: {sleep_logits_decoded}")
    print(f"osa logits decoded: {osa_logits_decoded}")
    print(f"snoring logits decoded: {snoring_logits_decoded}")


def save_and_load_binary():
    sleep_stage_logits = generate_logits(4, 1200)
    osa_stage_logits = generate_logits(3, 1200)
    snoring_stage_logits = generate_logits(2, 1200)

    with open("sleep_stage_logits", "wb") as file:
        np.save(file, sleep_stage_logits)

    with open("osa_stage_logits", "wb") as file:
        np.save(file, osa_stage_logits)

    with open("snoring_stage_logits", "wb") as file:
        np.save(file, snoring_stage_logits)

    with open("sleep_stage_logits", "rb") as file:
        sleep_stage_logits_from_file = np.load(file)

    with open("osa_stage_logits", "rb") as file:
        osa_stage_logits_from_file = np.load(file)

    with open("snoring_stage_logits", "rb") as file:
        snoring_stage_logits_from_file = np.load(file)

    print(sleep_stage_logits_from_file)
    print(osa_stage_logits_from_file)
    print(snoring_stage_logits_from_file)


def main():
    # measure_the_size_for_logits(10)
    # measure_the_time_of_conversion(10)

    # measure_the_size_for_logits(24)
    # measure_the_time_of_conversion(24)

    # measure_the_size_for_logits(48)
    # measure_the_time_of_conversion(48)

    save_and_load_binary()


main()
