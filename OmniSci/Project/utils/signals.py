# from django.contrib.auth.models import User
from Project.models import ProjectInfo
from django.db import models
from haystack import signals


class UserOnlySignalProcessor(signals.BaseSignalProcessor):
    def setup(self):
        # Listen only to the ``ProjectInfo`` model.
        models.signals.post_save.connect(self.handle_save, sender=ProjectInfo)
        models.signals.post_delete.connect(self.handle_delete, sender=ProjectInfo)

    def teardown(self):
        # Disconnect only for the ``ProjectInfo`` model.
        models.signals.post_save.disconnect(self.handle_save, sender=ProjectInfo)
        models.signals.post_delete.disconnect(self.handle_delete, sender=ProjectInfo)