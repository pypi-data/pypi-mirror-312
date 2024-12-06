from __future__ import annotations

from datetime import datetime
from typing import Any, Sequence, TYPE_CHECKING

from faz.utils.database.base_repository import BaseRepository
import pandas
from sqlalchemy import and_
from sqlalchemy import Select
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from faz.bot.database.fazwynn.model.character_history import CharacterHistory

if TYPE_CHECKING:
    from faz.utils.database.base_mysql_database import BaseMySQLDatabase


class CharacterHistoryRepository(BaseRepository[CharacterHistory, Any]):
    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, CharacterHistory)

    async def select_between_period(
        self,
        character_uuid: bytes,
        period_begin: datetime,
        period_end: datetime,
        *,
        session: AsyncSession | None = None,
    ) -> Sequence[CharacterHistory]:
        """Selects records for a given player within a specified period.

        Args:
            player_uuid (bytes): The UUID of the player as a byte string.
            period_begin (datetime): The start of the period to filter records.
            period_end (datetime): The end of the period to filter records.
            session (AsyncSession | None, optional): An optional asynchronous session
                to use for the database query. If not provided, a new session is created
                internally.

        Returns:
            Sequence[PlayerHistory]: A sequence of `PlayerHistory` objects matching the
            specified criteria, sorted by `datetime` in ascending order.
        """
        stmt = self.__get_select_between_period_stmt(period_begin, period_end, character_uuid)
        async with self.database.must_enter_async_session(session) as ses:
            res = await ses.execute(stmt)
            return res.scalars().all()

    def select_between_period_as_dataframe(
        self,
        character_uuid: bytes,
        period_begin: datetime,
        period_end: datetime,
    ) -> pandas.DataFrame:
        """Selects records for a given player within a specified period and returns
        them as a pandas DataFrame. Sorted by datetime.

        Args:
            player_uuid (bytes): The UUID of the player as a byte string.
            period_begin (datetime): The start of the period to filter records.
            period_end (datetime): The end of the period to filter records.

        Returns:
            pandas.DataFrame: A DataFrame containing `PlayerHistory` records matching
            the specified criteria, sorted by `datetime` in ascending order.
        """
        stmt = self.__get_select_between_period_stmt(period_begin, period_end, character_uuid)
        res = pandas.read_sql_query(stmt, self.database.engine)
        return res

    def __get_select_between_period_stmt(
        self, period_begin: datetime, period_end: datetime, character_uuid: bytes
    ) -> Select:
        model = self.model
        stmt = (
            select(model)
            .where(
                and_(
                    model.datetime >= period_begin,
                    model.datetime <= period_end,
                    model.character_uuid == character_uuid,
                )
            )
            .order_by(self.model.datetime)
        )
        return stmt
