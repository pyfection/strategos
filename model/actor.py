

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from model.base import Base


class Actor(Base):
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    owned_tiles = relationship("Tile", foreign_keys="Tile.owner_id")
    perceived_tiles = relationship("Tile", foreign_keys="Tile.perceiver_id")
    unplaced_units = Column(Integer, default=0)
