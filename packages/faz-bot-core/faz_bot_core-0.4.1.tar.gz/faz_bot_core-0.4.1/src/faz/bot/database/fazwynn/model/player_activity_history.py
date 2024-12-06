from datetime import datetime as dt

from sqlalchemy import Index
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from faz.bot.database.fazwynn.model.base_fazwynn_model import BaseFazwynnModel


class PlayerActivityHistory(BaseFazwynnModel):
    __tablename__ = "player_activity_history"

    uuid: Mapped[bytes] = mapped_column(BINARY(16), nullable=False, primary_key=True)
    logon_datetime: Mapped[dt] = mapped_column(DATETIME, nullable=False, primary_key=True)
    logoff_datetime: Mapped[dt] = mapped_column(DATETIME, nullable=False)

    __table_args__ = (
        Index(None, logon_datetime.desc()),
        Index(None, logoff_datetime.desc()),
    )
