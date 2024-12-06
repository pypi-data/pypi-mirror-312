from __future__ import annotations

from typing import Any, TYPE_CHECKING

from faz.utils.database.base_repository import BaseRepository
from sortedcontainers.sortedlist import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from faz.bot.database.fazwynn.model.character_info import CharacterInfo

if TYPE_CHECKING:
    from faz.utils.database.base_mysql_database import BaseMySQLDatabase


class CharacterInfoRepository(BaseRepository[CharacterInfo, Any]):
    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, CharacterInfo)

    async def select_from_player(
        self, player_uuid: bytes, *, session: AsyncSession | None = None
    ) -> Sequence[CharacterInfo]:
        stmt = select(self.model).where(self.model.uuid == player_uuid)
        async with self.database.must_enter_async_session(session) as ses:
            res = await ses.execute(stmt)
            return res.scalars().all()
