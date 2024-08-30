from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from config import config

from .base import Base


class EnteredUsers(Base):
    __tablename__ = "entered_users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, default=config.admin.username)
    ip = Column(String(16), nullable=True)
    entered_at = Column(DateTime, default=datetime.now)
