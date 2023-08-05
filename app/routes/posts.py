from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    # print(posts)
    if posts:
        return posts
    else:
        return None


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, response: Response,db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    post_query.delete(synchronize_session=False)
    db.commit()

    return response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db)):

    query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = query.first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")

    query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(updated_post)

    return updated_post

