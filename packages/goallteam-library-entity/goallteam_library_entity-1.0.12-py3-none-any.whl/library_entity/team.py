"""Module Entity Team"""
from datetime import datetime
from sqlalchemy import String, Integer, DateTime,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Team(Base):
    """Entity Team"""
    __tablename__ = 'TEAM'
    uuid:Mapped[int]= mapped_column(String(255), primary_key=True,unique=True,nullable=False,name='UUID')
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey('CITY.ID'), name='CITY_ID')
    coach_id: Mapped[str] = mapped_column(String(255), ForeignKey('PLAYER.UUID'),nullable=True, name='COACH_ID')
    captain: Mapped[str] = mapped_column(String(255), ForeignKey('PLAYER.UUID'), nullable=False, name='CAPTAIN_ID')
    matchesWon:Mapped[int]= mapped_column(Integer,nullable=True, default=0, name='MATCHES_WON')
    lostMatches:Mapped[int]= mapped_column(Integer, nullable=True,default=0, name='LOST_MATCHES')
    tiedMatches:Mapped[int]= mapped_column(Integer,  nullable=True,default=0, name='TIED_MATCHES')
    numberPlayers:Mapped[int]= mapped_column(Integer,nullable=False, default=0, name='NUMBER_PLAYERS')
    logoUrl:Mapped[str]= mapped_column(String(500),nullable=False, name='LOGO_URL')
    category:Mapped[str]= mapped_column(String(255), name='CATEGORY')
    name:Mapped[str]= mapped_column(String(500), unique=True,nullable=False,name='NAME')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, name='CREATED_AT')
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, name='UPDATED_AT')