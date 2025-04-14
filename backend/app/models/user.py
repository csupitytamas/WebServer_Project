from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.config.db import Base  # gondoskodj róla, hogy Base innen legyen importálva

class Felhasznalo(Base):
    __tablename__ = 'felhasznalo'

    u_id = Column(Integer, primary_key=True, index=True)
    nev = Column(String(50), nullable=False)
    jelszo = Column(String(255), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    szerep = Column(Integer, nullable=False)
    bejelentkezes_idopontja = Column(TIMESTAMP, nullable=True)