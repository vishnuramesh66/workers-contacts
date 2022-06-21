from sqlalchemy import Column, String, ForeignKey, Integer
from database import Base


class ContactData(Base):
    __tablename__ = "CONTACT_DETAILS"

    NAME = Column('NAME', String, primary_key=True, index=True)
    NUMBER = Column('PHONE NUMBER', String)



