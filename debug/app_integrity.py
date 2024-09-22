import base64
import json
from hashlib import sha256
from pathlib import Path

import jwt
import requests
from pyattest.attestation import Attestation
from pyattest.configs.apple import AppleConfig
from pyattest.configs.google_play_integrity_api import GooglePlayIntegrityApiConfig
from pyattest.verifiers.apple_attestation import AppleAttestationVerifier


def ios_app_attestation():
    file_path = f"{str(Path(__file__).parents[1])}/app_attestation.json"

    with open(file_path, "r") as file:
        data = json.load(file)

    valid_app_ids = ["M49GZVCJ3B.ai.asleep.AsleepSDKSampleApp", "A39BZVZJVB.ai.asleep.AsleepSDKSampleApp"]
    app_id = "M49GZVCJ3B.ai.asleep.AsleepSDKSampleApp"
    attestation_decoded = base64.b64decode(data["attestation"])

    unpacked = AppleAttestationVerifier.unpack(attestation_decoded)
    hashed_valid_app_ids = [sha256(app_id.encode()).digest() for app_id in valid_app_ids]

    if unpacked["rp_id"] in hashed_valid_app_ids:
        config = AppleConfig(key_id=base64.b64decode(data["key_id"]), app_id=app_id, production=False)

        try:
            Attestation(attestation_decoded, data["challenge"].encode(), config).verify()
        except Exception as e:
            raise e


# Google 공개 키를 가져오는 함수
def get_google_public_keys():
    response = requests.get("https://www.googleapis.com/oauth2/v3/certs")
    if response.status_code == 200:
        return response.json()["keys"]
    else:
        raise Exception("Google 공개 키를 가져오는 데 실패했습니다.")


# JWT 토큰 서명 검증 함수
def verify_jwt_token(token):
    # JWT 헤더의 'kid' 값 확인
    headers = jwt.get_unverified_header(token)
    kid = headers["kid"]

    # Google의 공개 키 가져오기
    public_keys = get_google_public_keys()

    # 'kid'에 맞는 공개 키 찾기
    public_key = next((key for key in public_keys if key["kid"] == kid), None)
    if not public_key:
        raise Exception("일치하는 공개 키를 찾을 수 없습니다.")

    # JWT 토큰 서명 검증 및 디코딩
    public_key_data = jwt.algorithms.RSAAlgorithm.from_jwk(public_key)
    decoded_token = jwt.decode(token, public_key_data, algorithms=["RS256"], audience="your_package_name")

    return decoded_token


def android_play_integrity():
    # Google의 공개 키 URL
    GOOGLE_PUBLIC_KEY_URL = "https://www.googleapis.com/oauth2/v3/certs"
    integrity_token = "앱에서 받은 JWT 토큰"

    # 서명 검증 및 디코딩 시도
    try:
        decoded_payload = verify_jwt_token(integrity_token)
        print("JWT 토큰 검증 성공:", decoded_payload)
    except Exception as e:
        print("JWT 토큰 검증 실패:", str(e))

    response = requests.get(GOOGLE_PUBLIC_KEY_URL)

    print(response.json())

    attest = ""
    challenge = ""
    config = GooglePlayIntegrityApiConfig(decryption_key="", verification_key="", apk_package_name="", production=False)

    try:
        Attestation(attest, challenge, config).verify()
    except Exception as e:
        raise e


android_play_integrity()
