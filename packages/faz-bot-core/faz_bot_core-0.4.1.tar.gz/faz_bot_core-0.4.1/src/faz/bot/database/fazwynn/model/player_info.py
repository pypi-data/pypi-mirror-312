from __future__ import annotations

from datetime import datetime as dt
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from faz.bot.database.fazwynn.model.base_fazwynn_model import BaseFazwynnModel

if TYPE_CHECKING:
    from faz.bot.database.fazwynn.model.character_info import CharacterInfo
    from faz.bot.database.fazwynn.model.guild_info import GuildInfo
    from faz.bot.database.fazwynn.model.player_history import PlayerHistory


class PlayerInfo(BaseFazwynnModel):
    __tablename__ = "player_info"

    uuid: Mapped[bytes] = mapped_column(BINARY(16), primary_key=True, nullable=False)
    latest_username: Mapped[str] = mapped_column(VARCHAR(16), nullable=False)
    first_join: Mapped[dt] = mapped_column(DATETIME, nullable=False)
    guild_uuid: Mapped[bytes | None] = mapped_column(
        BINARY(16), ForeignKey("guild_info.uuid"), default=None, nullable=True
    )

    guild: Mapped[GuildInfo | None] = relationship(
        "GuildInfo", back_populates="members", lazy="selectin"
    )
    characters: Mapped[list[CharacterInfo]] = relationship(
        "CharacterInfo", back_populates="player", lazy="selectin"
    )

    latest_stat: Mapped[PlayerHistory] = relationship(
        "PlayerHistory",
        primaryjoin="and_(PlayerHistory.uuid == PlayerInfo.uuid, "
        "PlayerHistory.datetime == (select(func.max(PlayerHistory.datetime))"
        ".where(PlayerHistory.uuid == PlayerInfo.uuid)"
        ".scalar_subquery()))",
        viewonly=True,
        uselist=False,
    )

    stat_history: Mapped[list[PlayerHistory]] = relationship(
        "PlayerHistory",
        back_populates="player_info",
        order_by="PlayerHistory.datetime.desc()",
        lazy="selectin",
    )
