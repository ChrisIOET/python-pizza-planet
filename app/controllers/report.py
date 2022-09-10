from app.repositories.managers import ReportManager
from .base import BaseController


class ReportController(BaseController):
    manager = ReportManager

    @classmethod
    def obtain_report(cls):
        return ReportManager.obtain_all_data_from_customers(), None
