import hashlib
from passlib.context import CryptPolicy, CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreateSchema
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def normalize_password(password:str) -> str      :
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def create_user(db: Session, user: UserCreateSchema) :
    print("password 원본:", user.password1)
    print("normalize:", normalize_password(user.password1))
#    db_user = User(username=user.username,
#                   password = pwd_context.hash(normalize_password(user.password1)),
#                   email=user.email )
    db_user = User(username=user.username,
                   password = pwd_context.hash(user.password1),
                   email=user.email )

    db.add(db_user)
    db.commit()

def get_existing_user(db: Session, user: UserCreateSchema):
    return db.query(User).filter(
        (User.username == user.username) |
        (User.email == user.email)
    ).first()

def getuser(db: Session, userName:str):
    return db.query(User).filter(User.username == userName).first()