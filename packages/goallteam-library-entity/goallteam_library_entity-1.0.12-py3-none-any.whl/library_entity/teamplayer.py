"""Module Entity TeamPlayer"""
from sqlalchemy import  String,  PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class TeamPlayer(Base):
    """Entity TEAM_PLAYER"""
    __tablename__ = 'TEAM_PLAYER'
    player_id: Mapped[str] = mapped_column(String(255), ForeignKey('PLAYER.UUID'), name='PLAYER_ID')
    team_id: Mapped[str] = mapped_column(String(255), ForeignKey('TEAM.UUID'), nullable=False, name='TEAM_ID')



    __table_args__ = (
        PrimaryKeyConstraint('PLAYER_ID', 'TEAM_ID', name='team_player_pk'),
    )