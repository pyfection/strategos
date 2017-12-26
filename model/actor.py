

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from model.base import Base


class Actor(Base):
    name = Column(String)
    tiles = relationship("Tile")
