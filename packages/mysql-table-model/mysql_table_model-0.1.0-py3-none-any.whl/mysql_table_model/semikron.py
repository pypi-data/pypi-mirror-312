"""塞米控数据表模型."""
import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base


BASE = declarative_base()


# pylint: disable=R0903
class DbcLinkTray(BASE):
    """DbcLinkTray class."""
    __tablename__ = "dbc_link_tray"

    dbc_code = Column(String(50), primary_key=True, unique=True, nullable=False)
    dbc_state = Column(Integer, nullable=True)
    tray_code = Column(String(50), nullable=True)
    tray_index = Column(Integer, nullable=True)
    lot_name = Column(String(50), nullable=True)
    lot_article_name = Column(String(50))
    updated_at = Column(DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))


class LotInfo(BASE):
    """LotInfo class."""
    __tablename__ = "lot_info"

    lot_name = Column(String(50), primary_key=True, unique=True, nullable=False)
    lot_article_name = Column(String(50), nullable=True)
    lot_quality = Column(Integer, nullable=True)
    lot_state = Column(Integer, nullable=True)
    recipe_name = Column(String(50), nullable=True)
    point_name = Column(String(50), nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())
    created_at = Column(DateTime, default=datetime.datetime.now())
