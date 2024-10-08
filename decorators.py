from auth.models import CredentialStatus, Admin
from auth.session import *
from functools import wraps


def get_user_status(user_id: int) -> CredentialStatus:
    with Session(engine) as session:
        statement = select(CredentialStatus).where(CredentialStatus.user_id == user_id)
        result = session.exec(statement).first()
        return result


def verified_user(func):
    @wraps(func)
    async def wrapper(*args, token: str = Depends(get_current_user), **kwargs):
        try:

            current_user = await get_current_user(token)
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                )
            user_status = get_user_status(current_user)
            if not user_status or not user_status.is_verified:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User account not verified",
                )

            return await func(*args, **kwargs)

        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}",
            )

    return wrapper


def check_admin_status(user_id: int) -> bool:
    with Session(engine) as session:
        statement = select(Admin).where(Admin.id == user_id)
        admin = session.exec(statement).first()
        return bool(admin and admin.is_staff)


# def admin_required(func):
#     @wraps(func)
#     async def wrapper(*args, token: str = Depends(get_current_user), **kwargs):
#         try:
#             current_user = await get_current_user(token)
#             if not current_user:
#                 raise HTTPException(
#                     status_code=status.HTTP_401_UNAUTHORIZED,
#                     detail="Invalid authentication credentials",
#                 )
#             is_admin = check_admin_status(current_user)
#             if not is_admin:
#                 raise HTTPException(
#                     status_code=status.HTTP_403_FORBIDDEN,
#                     detail="Admin privileges required",
#                 )
#             return await func(*args, **kwargs)

#         except HTTPException as he:
#             raise he
#         except Exception as e:
#             raise HTTPException(
#                 status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 detail=f"An error occurred: {str(e)}",
#             )
#     return wrapper

