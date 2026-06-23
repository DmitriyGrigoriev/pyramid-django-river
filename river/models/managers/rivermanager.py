from django_cte import CTEQuerySet
from django.db.models.manager import BaseManager

from river.config import app_config


class RiverQuerySet(CTEQuerySet):
    def first(self):
        if app_config.IS_MSSQL:
            return next(iter(self), None)
        else:
            return super(RiverQuerySet, self).first()


class RiverManager(BaseManager.from_queryset(RiverQuerySet)):
    pass
