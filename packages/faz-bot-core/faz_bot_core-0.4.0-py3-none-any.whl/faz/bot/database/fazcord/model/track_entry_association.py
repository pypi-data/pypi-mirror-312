from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import BINARY
from sqlalchemy import ForeignKey
from sqlalchemy import INTEGER
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from faz.bot.database.fazcord.model.base_fazcord_model import BaseFazcordModel

if TYPE_CHECKING:
    from faz.bot.database.fazcord.model.track_entry import TrackEntry


class TrackEntryAssociation(BaseFazcordModel):
    __tablename__ = "track_entry_associations"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    track_entry_id: Mapped[int] = mapped_column(
        INTEGER, ForeignKey("track_entry.id", ondelete="CASCADE"), nullable=False
    )
    associated_value: Mapped[bytes] = mapped_column(BINARY(16), nullable=False)

    track_entry: Mapped[TrackEntry] = relationship(
        "TrackEntry", back_populates="associations", lazy="selectin"
    )

    __table_args__ = (UniqueConstraint(track_entry_id, associated_value),)
