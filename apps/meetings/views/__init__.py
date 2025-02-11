# apps/meetings/views/__init__.py
from .base import dashboard, director_dashboard
from .crud import (
    meeting_create,
    meeting_detail,
    meeting_update,
    meeting_delete
)
from .lists import meeting_list
from .calendar import calendar_view

__all__ = [
    'dashboard',
    'director_dashboard',
    'meeting_create',
    'meeting_detail',
    'meeting_update',
    'meeting_delete',
    'meeting_list',
    'calendar_view'
]