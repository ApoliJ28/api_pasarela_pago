from database.db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}
    
    id = Column(Integer, primary_key=True, index=True)
    mail = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    created_datetime = Column(DateTime)
    updated_datetime = Column(DateTime)
    
    orders = relationship("Order", back_populates="user")
