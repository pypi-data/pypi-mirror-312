from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from faz.bot.database.fazcord.model.base_fazcord_model import BaseFazcordModel

if TYPE_CHECKING:
    from faz.bot.database.fazcord.model.discord_channel import DiscordChannel


class DiscordGuild(BaseFazcordModel):
    __tablename__ = "discord_guild"

    guild_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    guild_name: Mapped[str] = mapped_column(VARCHAR(36), nullable=False)

    channels: Mapped[list[DiscordChannel]] = relationship(
        "DiscordChannel", back_populates="discord_guild", lazy="selectin"
    )
