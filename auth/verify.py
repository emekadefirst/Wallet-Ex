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
from fastapi import Depends, HTTPException, UploadFile, File, status, APIRouter, Form


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


@verified_user
@validate.post("/verify_account")
async def verify(
    first_name: str = Form(...),
    last_name: str = Form(...),
    other_name: str = Form(...),
    dob: str = Form(...),
    city: str = Form(...),
    zip_code: str = Form(...),
    state: str = Form(...),
    street: str = Form(...),
    country: str = Form(...),
    phone_number: str = Form(...),
    id_document: Optional[UploadFile] = File(None),
    profile_image: Optional[UploadFile] = File(None),
    token: str = Depends(oauth2_scheme),
):
    try:
        current_user = await get_current_user(token)
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        profile_image_path = (
            await save_file(profile_image, PROFILE_IMAGE_DIRECTORY)
            if profile_image
            else None
        )
        id_document_path = (
            await save_file(id_document, ID_DOC_DIRECTORY) if id_document else None
        )
        try:
            dob_datetime = datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Use YYYY-MM-DD",
            )

        await save_credentials(
            first_name=first_name,
            last_name=last_name,
            other_name=other_name,
            dob=dob_datetime,
            street=street,
            city=city,
            zip_code=zip_code,
            state=state,
            id_document=id_document_path,
            profile_image=profile_image_path,
            country=country,
            phone_number=phone_number,
            user_id=current_user,
        )
        user = get_user_by_id(current_user)
        email = user.email
        applicant = create_applicant(current_user, email, phone_number, state)
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
