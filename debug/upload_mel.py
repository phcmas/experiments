from config import load_env, logger
import requests


settings = load_env()


def upload_mel_file_v2(start_seq: int, end_seq: int, session_id: str):
    base_file_dir = settings.MEL_FILE_DIR
    base_url = settings.UPLOAD_API_BASE_URL

    for seq in range(start_seq, end_seq + 1):
        file_dir = f"{base_file_dir}/{seq}_mel"
        url = f"{base_url}/v2/sessions/{session_id}/mel-data/{seq}"

        with open(file_dir, "rb") as file:
            files = {"melspectrogram": (f"{seq}_mel", file, "application/octet-stream")}
            upload_file_response = requests.request(
                method="POST",
                url=url,
                headers={
                    "x-api-key": "NOAaYLIxs5iNJr20VGu2LAVyjehcgCjB6C8G1Inn",
                    "x-api-key-uuid": "af1c90ed-4cd4-45d3-a74c-5b42ba41c697",
                    "x-api-key-type": "live",
                    "x-plan": '{"contract_id": 1, "id": 1, "version": 0, "name": "TRIAL", "sleep_stage_level": 4,  "stride": 300, "apnea_detection": 1, "snoring_detection": 1, "realtime_polling": 1, "realtime_callback": 1, "started_from": "2024-05-28 00:00:00", "ended_on": "2024-05-28 00:20:00"}',
                    "x-customer-uuid": "G-20240602170436-BZabfwGQCAbqsGwsywWl",
                },
                files=files,
                data={"melspectrogram": f"{seq}_mel"},
            )

            logger.info(upload_file_response)


def upload_mel_file_v1(start_seq: int, end_seq: int, session_id: str):
    base_file_dir = settings.MEL_FILE_DIR
    base_url = settings.UPLOAD_API_BASE_URL

    for seq in range(start_seq, end_seq + 1):
        file_dir = f"{base_file_dir}/{seq}_mel"
        url = f"{base_url}/v1/sessions/{session_id}/mel-data/{seq}"

        with open(file_dir, "rb") as file:
            files = {"melspectrogram": (f"{seq}_mel", file, "application/octet-stream")}
            upload_file_response = requests.request(
                method="POST",
                url=url,
                headers={
                    "x-api-key": "NOAaYLIxs5iNJr20VGu2LAVyjehcgCjB6C8G1Inn",
                    "x-api-key-uuid": "af1c90ed-4cd4-45d3-a74c-5b42ba41c697",
                    "x-api-key-type": "live",
                    "x-plan": '{"contract_id": 1, "id": 1, "version": 0, "name": "TRIAL", "sleep_stage_level": 4,  "stride": 300, "apnea_detection": 1, "snoring_detection": 1, "realtime_polling": 1, "realtime_callback": 1, "started_from": "2024-05-28 00:00:00", "ended_on": "2024-05-28 00:20:00"}',
                    "x-customer-uuid": "G-20240602170436-BZabfwGQCAbqsGwsywWl",
                },
                files=files,
                data={"melspectrogram": f"{seq}_mel"},
            )

            logger.info(upload_file_response)


def main():
    session_id = "20240605062959_esl7q"
    # upload_mel_file_v1(0, 38, session_id)
    upload_mel_file_v1(0, 38, session_id)

    print("end")


main()
