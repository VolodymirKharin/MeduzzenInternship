from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "user_table"

    user_id = Column("user_id", Integer, autoincrement=True, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    user_name = Column("user_name", String, nullable=False, unique=True)
    user_email = Column("user_email", String, nullable=False, unique=True)
    user_password = Column("user_password", String, nullable=False)
    user_status = Column("user_status", Boolean, nullable=False)

    company = relationship("Company", back_populates="user")


class Company(Base):
    __tablename__ = "company_table"

    company_id = Column("company_id", Integer, autoincrement=True, primary_key=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    company_name = Column("company_name", String, nullable=False, unique=True)
    company_description = Column("company_description", String(250))
    owner_id = Column("owner_id", Integer, ForeignKey("user_table.user_id"), nullable=False)

    user = relationship("User", back_populates="company")

