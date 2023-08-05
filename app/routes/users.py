from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users


@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_pass = utils.hash_password(user.password)
    user.password = hashed_pass

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person does not exist")

    return user


@router.put("/{id}", response_model=schemas.UserResponse)
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.user_id == id)
    updated_user = query.first()

    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")

    query.update(user.dict(), synchronize_session=False)
    db.commit()
    db.refresh(updated_user)

    return updated_user


@router.delete("/{id}")
def get_user(id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == id)

    if not user:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Person does not exist")

    user.delete()
    db.commit()

    return response(status_code=status.HTTP_204_NO_CONTENT)
