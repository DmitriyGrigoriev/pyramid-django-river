"""
Per-process кэш для Workflow объектов.

Устраняет повторные запросы к river_workflow таблице
при выполнении переходов (approve, signals и т.д.).
"""
import logging

from river.models import Workflow

LOGGER = logging.getLogger(__name__)

_workflow_cache = {}


def get_workflow(content_type, field_name):
    """Получает Workflow из кэша или БД."""
    key = (content_type.pk, field_name)
    if key not in _workflow_cache:
        LOGGER.debug("[WORKFLOW-CACHE] MISS key=%s, loading from DB", key)
        _workflow_cache[key] = Workflow.objects.filter(
            content_type=content_type, field_name=field_name
        ).select_related('initial_state').first()
    else:
        LOGGER.debug("[WORKFLOW-CACHE] HIT key=%s", key)
    return _workflow_cache[key]


def get_workflow_or_raise(content_type, field_name):
    """Получает Workflow из кэша или БД, бросает исключение если не найден."""
    wf = get_workflow(content_type, field_name)
    if wf is None:
        raise Workflow.DoesNotExist(
            f"Workflow not found for content_type={content_type}, field_name={field_name}"
        )
    return wf


def clear_cache():
    """Очищает кэш (при необходимости, например в тестах)."""
    _workflow_cache.clear()
