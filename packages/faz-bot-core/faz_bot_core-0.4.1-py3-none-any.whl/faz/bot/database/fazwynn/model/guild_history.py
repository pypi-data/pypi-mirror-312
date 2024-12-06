from __future__ import annotations

from datetime import datetime as dt
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.dialects.mysql import SMALLINT
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from faz.bot.database.fazwynn.model._unique_id_model import UniqueIdModel

if TYPE_CHECKING:
    from faz.bot.database.fazwynn.model.guild_info import GuildInfo


class GuildHistory(UniqueIdModel):
    __tablename__ = "guild_history"

    uuid: Mapped[bytes] = mapped_column(
        BINARY(16), ForeignKey("guild_info.uuid"), nullable=False, primary_key=True
    )
    level: Mapped[float] = mapped_column(DECIMAL(5, 2, unsigned=True), nullable=False)
    territories: Mapped[int] = mapped_column(SMALLINT(unsigned=True), nullable=False)
    wars: Mapped[int] = mapped_column(INTEGER(unsigned=True), nullable=False)
    member_total: Mapped[int] = mapped_column(TINYINT(unsigned=True), nullable=False)
    online_members: Mapped[int] = mapped_column(TINYINT(unsigned=True), nullable=False)
    datetime: Mapped[dt] = mapped_column(DATETIME, nullable=False, primary_key=True)
    unique_id: Mapped[bytes] = mapped_column(BINARY(16), nullable=False)

    guild_info: Mapped[GuildInfo] = relationship(
        "GuildInfo",
        back_populates="stat_history",
    )

    __table_args__ = (
        Index(None, datetime.desc()),
        Index(None, uuid),
        UniqueConstraint(unique_id),
    )
