import os
import uuid
from typing import Optional
from database import engine
from sqlmodel import Session
from datetime import datetime
from .models import Credentials
from decorators import verified_user
from .session import oauth2_scheme, get_current_user, get_user_by_id, save_credentials
from services.sumsub import create_applicant, upload_id
from fastapi import Depends, HTTPException, UploadFile, File, status, APIRouter, Form, Request


validate = APIRouter()

ID_DOC_DIRECTORY = "IDs/"
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
        return file_path 
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
    user_id: int = Form(...),
    id_document: Optional[UploadFile] = File(None),
):
    # Retrieve the user by ID
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    email = user.email

    # Save ID document locally (if provided)
    id_document_path = (
        await save_file(id_document, ID_DOC_DIRECTORY) if id_document else None
    )

    try:
        # Create the applicant using Sumsub API
        applicant = create_applicant(user_id, email, phone_number, state)
        if not applicant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create applicant.",
            )

        # Upload the ID document to Sumsub (if provided)
        if id_document_path:
            upload_response = upload_id(applicant, id_document_path)
            if upload_response["status"] != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="ID upload failed."
                )

        # Save the user's credentials in the database
        save_credentials(
            city=city,
            state=state,
            street=street,
            country=country,
            phone_number=phone_number,
            user_id=user_id,
            zip_code=zip_code,
            id_document=id_document_path,
        )

        return {
            "status": status.HTTP_200_OK,
            "message": "Credentials collected and verified successfully",
            "applicant_id": applicant,  # Return the applicant ID
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during verification: {str(e)}",
        )
