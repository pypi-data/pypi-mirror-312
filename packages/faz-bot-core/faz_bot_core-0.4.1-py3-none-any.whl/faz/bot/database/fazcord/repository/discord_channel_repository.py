from __future__ import annotations

from typing import Any, TYPE_CHECKING

from faz.utils.database.base_repository import BaseRepository

from faz.bot.database.fazcord.model.discord_channel import DiscordChannel

if TYPE_CHECKING:
    from faz.utils.database.base_mysql_database import BaseMySQLDatabase


class DiscordChannelRepository(BaseRepository[DiscordChannel, Any]):
    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, DiscordChannel)
