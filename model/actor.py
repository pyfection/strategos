

from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from model.base import Base


class Actor(Base):
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    current_turn = Column(Integer, default=0)
    unplaced_units = Column(Integer, default=0)
    owned_tiles = relationship("Tile", foreign_keys="Tile.owner_id")
    perceived_tiles = relationship("Tile", foreign_keys="Tile.perceiver_id")
    caused_events = relationship("Event", foreign_keys="Event.causer_id")
    perceived_events = relationship("Event", foreign_keys="Event.perceiver_id")
