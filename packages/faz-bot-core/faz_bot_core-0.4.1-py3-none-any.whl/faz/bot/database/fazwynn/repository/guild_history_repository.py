from __future__ import annotations

from datetime import datetime
from typing import Any, TYPE_CHECKING

from faz.utils.database.base_repository import BaseRepository
import pandas
from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.sql import Select

from faz.bot.database.fazwynn.model.guild_history import GuildHistory

if TYPE_CHECKING:
    from faz.utils.database.base_mysql_database import BaseMySQLDatabase


class GuildHistoryRepository(BaseRepository[GuildHistory, Any]):
    def __init__(self, database: BaseMySQLDatabase) -> None:
        super().__init__(database, GuildHistory)

    def select_between_period_as_dataframe(
        self,
        guild_uuid: bytes,
        period_begin: datetime,
        period_end: datetime,
    ) -> pandas.DataFrame:
        """Selects records for a given guild within a specified period and returns
        them as a pandas DataFrame. Sorted by datetime.

        Args:
            guild_uuid (bytes): The UUID of the guild.
            period_begin (datetime): The start of the period to filter records.
            period_end (datetime): The end of the period to filter records.

        Returns:
            pandas.DataFrame: A DataFrame containing `PlayerHistory` records matching
            the specified criteria, sorted by `datetime` in ascending order.
        """
        stmt = self.__get_select_between_period_stmt(period_begin, period_end, guild_uuid)
        res = pandas.read_sql_query(stmt, self.database.engine)
        return res

    def __get_select_between_period_stmt(
        self, period_begin: datetime, period_end: datetime, uuid: bytes
    ) -> Select:
        model = self.model
        stmt = (
            select(model)
            .where(
                and_(
                    model.datetime >= period_begin,
                    model.datetime <= period_end,
                    model.uuid == uuid,
                )
            )
            .order_by(self.model.datetime)
        )
        return stmt
