# Importing standard python libs
from datetime import datetime, timedelta
import sys
import os
sys.path.append("...")

# Importing authentication local resources
from . import schema
from . import models

# Importing SQLAlchemy modules
from sqlalchemy.orm import Session

# Importing FastApi Modules
from fastapi import status, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer

# Importing dependencies
from dependencies import get_db

# Importing JWT Libs
from passlib.context import CryptContext
from jose import jwt, JWTError


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20


# Creating the password context
def pwd_context():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context


# Creating the OAuth2 Password Bearer
def oauth2_scheme():
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authentication/login")
    return oauth2_scheme


def generate_user(request: schema.User, db: Session):
    hashed_pwd = pwd_context().hash(request.password)
    new_user = models.User(
        first_name = request.first_name,
        last_name = request.last_name,
        username = request.username,
        #email = request.email,
        role = "user",
        hashed_password = hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(username: str, db: Session):
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        return user


def check_if_user_exists(username: str, db: Session):
    user = get_user(username, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username")
    else:
        return user


def verify_password(password: str, user: models.User):
    if not pwd_context().verify(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid password")


def generate_token(data: dict):
    """Method for generating a jwt token for authentication
    Args:
        data (dict): {sub': 'username'}
    Returns:
        string: returns an jwt encoded token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme())):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    print(token_data.username)
    user = get_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user



def delete_user(username: str, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.username == username).first()
    if user:
        db.query(models.User).filter(models.User.username == username).delete(synchronize_session=False)
        db.commit()
        return True
    else:
        return False
    