from django.db import models

from sumo.common.mixins.validate_model_mixin import ValidateModelMixin


class Basho(ValidateModelMixin, models.Model):
    pass
