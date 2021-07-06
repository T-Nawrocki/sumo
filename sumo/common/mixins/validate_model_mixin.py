class ValidateModelMixin:
    """
    Mixin for models to be validated with the full_clean() method before saving.
    """

    def save(self, *args, **kwargs):
        """Calls full_clean() before saving"""
        self.full_clean()
        super(ValidateModelMixin, self).save(*args, **kwargs)
