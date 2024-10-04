import os
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

SUMSUB_SECRET_KEY = os.environ.get("SUMSUB_KEY")
SUMSUB_APP_TOKEN = os.environ.get("SUMSUB_TOKEN")
SUMSUB_TEST_BASE_URL = os.environ.get("SUMSUB_TEST_BASE_URL")
REQUEST_TIMEOUT = 60


def sign_request(request: requests.Request) -> requests.PreparedRequest:
    """Signs the request for Sumsub API"""
    prepared_request = request.prepare()
    now = int(time.time())
    method = request.method.upper()
    path_url = prepared_request.path_url
    body = b"" if prepared_request.body is None else prepared_request.body
    if isinstance(body, str):
        body = body.encode("utf-8")
    data_to_sign = (
        str(now).encode("utf-8")
        + method.encode("utf-8")
        + path_url.encode("utf-8")
        + body
    )
    signature = hmac.new(
        SUMSUB_SECRET_KEY.encode("utf-8"), data_to_sign, digestmod=hashlib.sha256
    )
    prepared_request.headers["X-App-Token"] = SUMSUB_APP_TOKEN
    prepared_request.headers["X-App-Access-Ts"] = str(now)
    prepared_request.headers["X-App-Access-Sig"] = signature.hexdigest()
    return prepared_request


def create_applicant(user_id, email, phone, state):
    url = f"{SUMSUB_TEST_BASE_URL}/resources/applicants?levelName=basic-kyc-level"
    headers = {"Content-Type": "application/json"} 
    data = {
        "externalUserId": user_id,
        "email": email,
        "phone": phone,
        "fixedInfo": {"country": "NGA", "placeOfBirth": state},
    }

    request = requests.Request(method="POST", url=url, headers=headers, json=data)
    prepared_request = sign_request(request)
    with requests.Session() as session:
        response = session.send(prepared_request, timeout=REQUEST_TIMEOUT)

    if response.status_code == 201:
        return {"response": response.json().get("id"), "message": "Applicant created successfully."}
    return {
            "response": response.json().get("id"),
            "message": "Applicant creation failed.",
            }


def upload_id(applicant_id, file_path):
    url = f"{SUMSUB_TEST_BASE_URL}/resources/applicants/{applicant_id}/info/idDoc"
    headers = {
        "Content-Type": "multipart/form-data",
    }
    with open(file_path, "rb") as file:
        files = {
            "file": file,
            "metadata": (
                "",
                '{"idDocType": "NIN", "country": "NGA"}',
                "application/json",
            ),
        }
        request = requests.Request(method="POST", url=url, headers=headers, files=files)
        prepared_request = sign_request(request)

        with requests.Session() as session:
            response = session.send(prepared_request, timeout=REQUEST_TIMEOUT)

        if response.status_code == 200:
            return {
                "message": "ID uploaded successfully for verification.",
                "body": response.json(),
                "status": response.status_code,
            }
        else:
            print("Failed to upload ID.")
            return {
                "message": "Failed to upload ID.",
                "body": response.json(),
                "status": response.status_code,
            }


