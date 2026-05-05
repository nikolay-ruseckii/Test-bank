from sqlalchemy import Column, Integer, Float, ForeignKey
from src.main.api.db.base import Base


class Credit(Base):
    __tablename__ = "credit"  # ⚠️ если не заработает — поменяем на "credits"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("account.id"))
    amount = Column(Float)
    term_months = Column(Integer)

    @staticmethod
    def get_credit_by_id(db, credit_id: int):
        return db.query(Credit).filter_by(id=credit_id).first()