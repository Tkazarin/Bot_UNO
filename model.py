from sqlalchemy import Column, Integer, String, Text

from db import Base


class Participants(Base):
    __tablename__ = "participant"

    id_participant = Column(Integer, primary_key=True)
    authorization = Column(String(3), nullable=False)
    chat_id_participant = Column(Integer, nullable=False)
    tg_id_participant = Column(Integer, nullable=False)