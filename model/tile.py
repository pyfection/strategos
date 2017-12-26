

from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from model.base import Base


class Tile(Base):
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    owner_id = Column(Integer, ForeignKey('actor.id'))
    owner = relationship("Actor", foreign_keys="Tile.owner_id", back_populates="owned_tiles")
    perceiver_id = Column(Integer, ForeignKey('actor.id'))
    perceiver = relationship("Actor", foreign_keys="Tile.perceiver_id", back_populates="perceived_tiles")
    units = Column(Integer, default=0)
