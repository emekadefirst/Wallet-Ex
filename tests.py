# import os
# import time
# import hmac
# import hashlib
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# SUMSUB_SECRET_KEY = os.environ.get("SUMSUB_KEY")
# SUMSUB_APP_TOKEN = os.environ.get("SUMSUB_TOKEN")
# SUMSUB_TEST_BASE_URL = os.environ.get("SUMSUB_TEST_BASE_URL")
# REQUEST_TIMEOUT = 60


# def sign_request(request: requests.Request) -> requests.PreparedRequest:
#     """Signs the request for Sumsub API"""
#     prepared_request = request.prepare()
#     now = int(time.time())
#     method = request.method.upper()
#     path_url = prepared_request.path_url
#     body = b"" if prepared_request.body is None else prepared_request.body
#     if isinstance(body, str):
#         body = body.encode("utf-8")
#     data_to_sign = (
#         str(now).encode("utf-8")
#         + method.encode("utf-8")
#         + path_url.encode("utf-8")
#         + body
#     )
#     signature = hmac.new(
#         SUMSUB_SECRET_KEY.encode("utf-8"), data_to_sign, digestmod=hashlib.sha256
#     )
#     prepared_request.headers["X-App-Token"] = SUMSUB_APP_TOKEN
#     prepared_request.headers["X-App-Access-Ts"] = str(now)
#     prepared_request.headers["X-App-Access-Sig"] = signature.hexdigest()
#     return prepared_request


# def create_applicant(user_id, email, phone, state):
#     url = f"{SUMSUB_TEST_BASE_URL}/resources/applicants?levelName=basic-kyc-level"
#     headers = {"Content-Type": "application/json", "Content-Encoding": "utf-8"}
#     data = {
#         "externalUserId": user_id,
#     }

#     request = requests.Request(
#         method="POST",
#         url=url,
#         headers=headers,
#         data=json.dumps(data),  # Use json.dumps() for the request body
#     )
#     prepared_request = sign_request(request)

#     with requests.Session() as session:
#         response = session.send(prepared_request, timeout=REQUEST_TIMEOUT)

#     if response.status_code == 201:
#         return {
#             "response": response.json().get("id"),
#             "message": "Applicant created successfully.",
#         }
#     else:
#         # Print the response body for debugging
#         print("Failed to create applicant.")
#         print("Response:", response.status_code, response.text)
#         return {
#             "response": None,
#             "message": "Applicant creation failed.",
#         }


# import os
# import requests
# import json
# def upload_id(applicant_id, file_path):
#     url = f"{SUMSUB_TEST_BASE_URL}/resources/applicants/{applicant_id}/info/idDoc"

#     # Open the file to upload
#     with open(file_path, "rb") as f:
#         files = {
#             "content": f,  # The key should be 'content', not 'file'
#         }
#         metadata = '{"idDocType":"NIN", "country":"NGA"}'  # Properly format the metadata as a string

#         # Prepare the request
#         request = requests.Request(
#             method="POST",
#             url=url,
#             files=files,
#             data={
#                 "metadata": metadata
#             },  # Send metadata as a form field, not in 'files'
#         )
#         prepared_request = sign_request(request)

#         try:
#             with requests.Session() as session:
#                 response = session.send(prepared_request, timeout=REQUEST_TIMEOUT)

#             if response.status_code == 200:
#                 return {
#                     "message": "ID uploaded successfully for verification.",
#                     "body": response.json(),
#                     "status": response.status_code,
#                 }
#             else:
#                 print("Failed to upload ID.")
#                 print("Response:", response.status_code, response.text)
#                 return {
#                     "message": "Failed to upload ID.",
#                     "body": response.json(),
#                     "status": response.status_code,
#                 }
#         except requests.exceptions.RequestException as e:
#             raise Exception(f"An error occurred during the request: {str(e)}")


# applicant = create_applicant(
#     "64f16be8f57150d070208ID",
#     "victorchibuogwu33@gmail.com",
#     "234148374084",
#     "Delta",
# )
# print("application")
# print(applicant)

# # Ensure the applicant was successfully created and has an ID before proceeding
# if applicant and applicant.get("response"):
#     print("upload id doc")
#     # Pass the applicant ID to the upload_id function
#     upload = upload_id(applicant["response"], "id.jpeg")
#     print(upload)
# else:
#     print("Failed to create applicant. Skipping ID upload.")


# from auth.session import get_current_user
# from auth.config import create_access_token

# print(
#     get_current_user(
#         "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNzI5OTc0MjQ5fQ.FoSiJfCl-geJMvfrbrjiVYNx2NV18016GXla49UvnIo"
#     )
# )
# # print(create_access_token({"id": 1}))

