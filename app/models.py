from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class URL(Base):
    __tablename__ = "urls"
    short_key = Column(String, primary_key=True)
    origin_url = Column(String, index=True)
    expires_at = Column(DateTime, nullable=True)
    click_cnt = Column(Integer, default=0)

    def is_expired(self):
        if self.expires_at:
            return datetime.utcnow() > self.expires_at
        return False
