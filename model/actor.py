

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from model.base import Base


class Actor(Base):
    name = Column(String, nullable=False)
    owned_tiles = relationship("Tile", foreign_keys="Tile.owner_id")
    perceived_tiles = relationship("Tile", foreign_keys="Tile.perceiver_id")
