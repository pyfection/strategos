

from sqlalchemy import Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from model.base import Base


class Tile(Base):
    x = Column(Float)
    y = Column(Float)
    owner_id = Column(Integer, ForeignKey('actor.id'))
    owner = relationship("Actor", back_populates="tiles")
    units = Column(Integer, default=0)
