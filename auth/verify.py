import os
import uuid
from typing import Optional
from database import engine
from sqlmodel import Session
from datetime import datetime
from .models import Credentials
from decorators import verified_user
from .session import oauth2_scheme, get_current_user, get_user_by_id
from services.sumsub import create_applicant, upload_id
from fastapi import Depends, HTTPException, UploadFile, File, status, APIRouter, Form, Request


validate = APIRouter()

PROFILE_IMAGE_DIRECTORY = "./profil_image/"
if not os.path.exists(PROFILE_IMAGE_DIRECTORY):
    os.makedirs(PROFILE_IMAGE_DIRECTORY)


ID_DOC_DIRECTORY = "./IDs/"
if not os.path.exists(ID_DOC_DIRECTORY):
    os.makedirs(ID_DOC_DIRECTORY)


async def save_file(file: UploadFile, directory: str) -> str:
    if not file:
        return None

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(directory, unique_filename)

    try:
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        return unique_filename
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}",
        )


async def save_credentials(**kwargs):
    with Session(engine) as session:
        try:
            detail = Credentials(**kwargs)
            session.add(detail)
            session.commit()
            session.refresh(detail)
            return detail
        except Exception as e:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error saving credentials: {str(e)}",
            )


@validate.post("/verify_account")
async def verify(
    city: str = Form(...),
    zip_code: str = Form(...),
    state: str = Form(...),
    street: str = Form(...),
    country: str = Form(...),
    phone_number: str = Form(...),
    user_id: str = Form(...),
    id_document: Optional[UploadFile] = File(None),
):
    try:
        id_document_path = (
            await save_file(id_document, ID_DOC_DIRECTORY) if id_document else None
        )


        await save_credentials(
            street=street,
            city=city,
            zip_code=zip_code,
            state=state,
            id_document=id_document_path,
            country=country,
            phone_number=phone_number,
            user_id=user_id,
        )
        user = get_user_by_id(user_id)
        email = user.email
        applicant = create_applicant(user_id, email, phone_number, state)
        if applicant:
            upload_id(applicant, os.path.join(ID_DOC_DIRECTORY, id_document_path))
        return {
            "status": status.HTTP_200_OK,
            "message": "Credentials collected successfully",
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )

    # token = request.headers.get("Authorization")
    # if token and token.startswith("Bearer "):
    #     token = token[7:]
    # print(f"Processed token: {token}")
    # current_user = await get_current_user(token)
    # if not current_user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid authentication credentials",
    #     )
