from __future__ import annotations

from typing import Any, TYPE_CHECKING

from faz.utils.database.base_repository import BaseRepository

from faz.bot.database.fazwynn.model.fazdb_uptime import FazdbUptime

if TYPE_CHECKING:
    from faz.utils.database.base_mysql_database import BaseMySQLDatabase


class FazdbUptimeRepository(BaseRepository[FazdbUptime, Any]):
    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, FazdbUptime)
