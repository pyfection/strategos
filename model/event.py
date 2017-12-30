

from sqlalchemy import Column, Boolean, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from model.base import Base


class Event(Base):
    type = Column(String, nullable=False)
    turn = Column(Integer, nullable=False)
    triggered = Column(Boolean, default=False)
    x = Column(Integer)
    y = Column(Integer)
    amount = Column(Integer)
    causer_id = Column(Integer, ForeignKey('actor.id'))
    causer = relationship("Actor", foreign_keys="Event.causer_id", back_populates="caused_events")
    perceiver_id = Column(Integer, ForeignKey('actor.id'))
    perceiver = relationship("Actor", foreign_keys="Event.perceiver_id", back_populates="perceived_events")
