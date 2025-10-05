from sqlalchemy import select
from db import session_maker
from model import Participants

class DAO:
    @classmethod
    def find_all_participants(cls):
        with session_maker() as session:
            query = select(Participants)
            participants = session.execute(query)
            return participants.scalars().all()

    @classmethod
    def find_participant(cls, chat_id_participant):
        with session_maker() as session:
            query = select(Participants).where(Participants.chat_id_participant == chat_id_participant)
            participant = session.execute(query).scalars().first()
            return participant

    @classmethod
    def create_participant(cls, participant: Participants):
        with session_maker() as session:
            if DAO.find_participant(participant.chat_id_participant):
                return None
            session.add(participant)
            session.commit()
            return participant

    @classmethod
    def define_authorization(cls, id_participant):
        with session_maker() as session:
            query = select(Participants).where(Participants.chat_id_participant == id_participant)
            participant = session.execute(query).scalars().first()
            if participant:
                return participant.authorization

    @classmethod
    def find_all_refery(cls):
        with session_maker() as session:
            query = select(Participants).where(Participants.authorization == 'REF' or Participants.authorization == 'ADM')
            participants = session.execute(query)
            return participants.scalars().all()

    @classmethod
    def delete_participant(cls, chat_id_participant):
        with session_maker() as session:
            query = select(Participants).where(Participants.chat_id_participant == chat_id_participant)
            participant = session.execute(query).scalars().first()
            if participant:
                session.delete(participant)
                session.commit()
