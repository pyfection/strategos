

from sqlalchemy import Column, String, Float, Integer

from model.base import Base


class World(Base):
    current_turn = Column(Integer, default=0)
    # name = Column(String)
    # unit = Column(String)
    # x = Column(Float)
    # y = Column(Float)
    # velocity = Column(Float, default=1.)  # 1.0 == 1 Tile per tick
    # destination_x = Column(Float)
    # destination_y = Column(Float)
    # color = Column(String)
    # view_range = Column(Integer, default=10)
