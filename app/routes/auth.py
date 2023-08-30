from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(tags=['Authentication'])


@router.post("/login", response_model=schemas.Token)
def login(user_details: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    query = db.query(models.User).filter(models.User.email == user_details.username).first()
    hashed_password = utils.hash_password(user_details.password)

    if not query:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    result = utils.verify_password(user_details.password, query.password)

    if not result:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = oauth2.create_access_token(data={"user_id": query.user_id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
