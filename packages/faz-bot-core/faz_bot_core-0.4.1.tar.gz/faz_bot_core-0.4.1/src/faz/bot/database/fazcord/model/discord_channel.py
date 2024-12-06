from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from faz.bot.database.fazcord.model.base_fazcord_model import BaseFazcordModel

if TYPE_CHECKING:
    from faz.bot.database.fazcord.model.discord_guild import DiscordGuild
    from faz.bot.database.fazcord.model.track_entry import TrackEntry


class DiscordChannel(BaseFazcordModel):
    __tablename__ = "discord_channel"

    channel_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    channel_name: Mapped[str] = mapped_column(VARCHAR(36), nullable=False)
    guild_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("discord_guild.guild_id"))

    discord_guild: Mapped[DiscordGuild] = relationship(
        "DiscordGuild", back_populates="channels", lazy="selectin"
    )
    track_entry: Mapped[TrackEntry] = relationship(
        "TrackEntry", back_populates="channel", lazy="selectin", uselist=False
    )
