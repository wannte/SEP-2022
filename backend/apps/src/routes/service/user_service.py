from fastapi import Depends, Header
from sqlalchemy.orm import Session

from apps.src.sql.database import get_db
from apps.src.sql.model import User


def get_user(student_id: str = Header(...), db: Session = Depends(get_db)):
    return db.query(User).filter(User.student_id == student_id).first()

class UserService():
    @staticmethod
    def get_user_by_student_id(student_id: str, db: Session):
        return db.query(User).filter(User.student_id == student_id).first()

    @staticmethod
    def create_user(user: User, db: Session):
        try:
            db.add(user)
            db.commit()
            return user
        except Exception as e:
            print(e)
            return None
    
    @staticmethod
    def update_user(user: User, db: Session):
        try:
            db.commit()
            db.refresh(user)
            return user
        except Exception as e:
            print(e)
            return None