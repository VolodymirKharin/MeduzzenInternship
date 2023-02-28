from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, LargeBinary, func



Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, autoincrement=True, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_name = Column(String, nullable=False, unique=True)
    user_email = Column(String, nullable=False, unique=True)
    user_password = Column(LargeBinary, nullable=False)
    user_status = Column(Boolean, nullable=False)
