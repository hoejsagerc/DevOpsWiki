# Importing Standard python modules and open import from top-level package
from email.utils import decode_params
import sys
sys.path.append("...")

# Importing FastApi Modules
from fastapi.params import Depends
from fastapi import APIRouter, status, Response, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Importing SQLAlchemy modules
from sqlalchemy.orm import Session

# Importing controller local resources
from . import schema
from . import models
from . import crud

# Importing depencies
from dependencies import get_db
from routers.auth.crud import get_current_user



router = APIRouter(
    prefix='/api/v1/authentication'
)

@router.post(
    '/user', 
    response_model=schema.UserResponse, 
    summary="Create a mew user. Requires admin privileges",
    tags=['Authentication']
    )
def create_new_user(request: schema.User, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    """
    Sign up for an account
    - **username:** [required] => Enter a unique username
    - **email**: [required] => Enter unique email address. Will be used for notifications
    - **first_name**: [required] => Enter first name
    - **last_name**: [required] => Enter last name
    """
    if current_user.role == "admin":
        user = crud.get_user(request.username, db)
        if not user:
            new_user = crud.generate_user(request, db)
            return request
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to create a user")


@router.post(
    '/login', 
    summary="Sign in to retrieve JWT for authentication",
    tags=['Authentication']
)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Sign In
    - **username:** [required] => Enter the username of a valid account
    - **password:** [required] => Enter the password for the user
    This endpoint will return a JWT token to be used for authentication with all locked routes
    """
    user = crud.check_if_user_exists(request.username, db)
    crud.verify_password(request.password, user)

    access_token = crud.generate_token(
        data = {'sub': request.username}
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.delete(
    '/user',
    summary="Delete a user account",
    tags=['Authentication']
)
def delete_user(username: str, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    """
    Delete user [Authentication Required]
    - **username:** [required] => Enter the username of a valid account
    This endpoint will return a JWT token to be used for authentication with all locked routes
    """
    if current_user.role == 'admin' and username != current_user.username:
        action = crud.delete_user(username, db)
        if action == True:
            return {'message': f'user: {username} was deleted successfully'}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User: {username}, was not found in database")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to delete a user")