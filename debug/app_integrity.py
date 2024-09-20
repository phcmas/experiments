import base64
import json

from pyattest.verifiers.apple_attestation import AppleAttestationVerifier
from pyattest.configs.apple import AppleConfig
from pyattest.attestation import Attestation
from hashlib import sha256

from pathlib import Path

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
