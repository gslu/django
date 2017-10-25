# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import blog.signals.handlers
