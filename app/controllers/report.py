from typing import Any

from sqlalchemy.exc import SQLAlchemyError

from app.repositories.managers import ReportManager
from .base import BaseController


class ReportController(BaseController):
    manager = ReportManager

    @classmethod
    def obtain_report(cls) -> dict[str, Any]:
        try:
            return ReportManager.obtain_report_data(), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)
