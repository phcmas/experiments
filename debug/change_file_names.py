import os
from config import load_env, logger

env = load_env()


def change_file_names():
    file_path = env.MEL_FILE_DIR

    for filename in os.listdir(file_path):
        order = int(filename.split("_")[-1].split(".")[0])
        old_file = os.path.join(file_path, filename)

        if os.path.isfile(old_file):
            new_file = os.path.join(file_path, f"{order}_mel")

            os.rename(old_file, new_file)
            logger.info(f"Renamed: {old_file} to {new_file}")


change_file_names()
