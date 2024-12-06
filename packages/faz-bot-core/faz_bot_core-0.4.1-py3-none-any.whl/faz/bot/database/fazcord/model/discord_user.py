from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from faz.bot.database.fazcord.model.base_fazcord_model import BaseFazcordModel

if TYPE_CHECKING:
    from faz.bot.database.fazcord.model.track_entry import TrackEntry


class DiscordUser(BaseFazcordModel):
    __tablename__ = "discord_user"

    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR(36), nullable=False)

    track_entries: Mapped[list[TrackEntry]] = relationship(
        "TrackEntry", back_populates="creator", lazy="selectin"
    )
