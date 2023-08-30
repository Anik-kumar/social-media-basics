from jose import jwt, JWTError
from datetime import datetime,  timedelta
from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session

from . import schemas, database, models
from fastapi.security.oauth2 import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# secret key
# algorithms
#

SECRET_KEY = "asdf8asdf98a7s9df6a897s6dy8f7tasdf76sa8d7fastyd8f7adg836t"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 120


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)

    to_encode.update({"exp": expire})

    key = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return key


def verify_access_token(token: str, credentials_exception):

    try:
        # print("token ", token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get('user_id')

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.user_id == token.id).first()

    print("user ", user.email)
    if not user.email:
        return credentials_exception

    return user

