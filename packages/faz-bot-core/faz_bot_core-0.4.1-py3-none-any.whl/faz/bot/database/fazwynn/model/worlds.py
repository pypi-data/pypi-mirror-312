from datetime import datetime

from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.dialects.mysql import SMALLINT
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from faz.bot.database.fazwynn.model.base_fazwynn_model import BaseFazwynnModel


class Worlds(BaseFazwynnModel):
    __tablename__ = "worlds"

    name: Mapped[str] = mapped_column(VARCHAR(16), nullable=False, primary_key=True)
    player_count: Mapped[int] = mapped_column(SMALLINT(unsigned=True), nullable=False)
    time_created: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
