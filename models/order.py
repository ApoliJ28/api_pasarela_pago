from database.db import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"schema": "payment"}
    
    id =  Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    total = Column(Float)
    is_paid = Column(Boolean, default=False)
    reference = Column(String)
    created_by = Column(Integer, ForeignKey("auth.users.id"))
    created_datetime = Column(DateTime)
    updated_datetime = Column(DateTime)

    user = relationship("User", back_populates="orders")
