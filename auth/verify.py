import os
import uuid
from typing import Optional
from database import engine
from sqlmodel import Session
from datetime import datetime
from pydantic import BaseModel
from .models import Credentials
from .session import oauth2_scheme, get_current_user
from fastapi import Depends, HTTPException, UploadFile, File, status, APIRouter


validate = APIRouter()

PROFILE_IMAGE_DIRECTORY = "./profil_image/"
if not os.path.exists(PROFILE_IMAGE_DIRECTORY):
    os.makedirs(PROFILE_IMAGE_DIRECTORY)


ID_DOC_DIRECTORY = "./IDs/"
if not os.path.exists(ID_DOC_DIRECTORY):
    os.makedirs(ID_DOC_DIRECTORY)


class CredentialsSchema(BaseModel):
    first_name: str
    last_name: str
    other_name: str
    dob: str
    city: str
    zip_code: str
    state: str
    id_document: Optional[UploadFile] = File(None)
    profile_image: Optional[UploadFile] = File(None)
    street: str
    country: str
    phone_number_1: str
    phone_number_2: str


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


@validate.post("/verify_account")
async def verify(form: CredentialsSchema, token: str = Depends(oauth2_scheme)):
    try:
        # Verify user
        current_user = await get_current_user(token)
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        profile_image_path = (
            await save_file(form.profile_image, PROFILE_IMAGE_DIRECTORY)
            if form.profile_image
            else None
        )
        id_document_path = (
            await save_file(form.id_document, ID_DOC_DIRECTORY)
            if form.id_document
            else None
        )
        try:
            dob_datetime = datetime.strptime(form.dob, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Use YYYY-MM-DD",
            )
        await save_credentials(
            first_name=form.first_name,
            last_name=form.last_name,
            other_name=form.other_name,
            dob=dob_datetime,
            street=form.street,
            city=form.city,
            zip_code=form.zip_code,
            state=form.state,
            id_document=id_document_path,
            profile_image=profile_image_path,
            country=form.country,
            phone_number_1=form.phone_number_1,
            phone_number_2=form.phone_number_2,
            user_id=current_user,
        )

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
