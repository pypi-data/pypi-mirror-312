from PySimultan2 import Content, TaxonomyMap

from .core.user import UserManager
user_manager = UserManager()

import nicegui.binding
nicegui.binding.MAX_PROPAGATION_TIME = 0.1

from .main_ui import run_ui
from .views.detail_views import DetailView
from .core.mappers import MethodMapper, Mapping, ViewManager


__all__ = ['run_ui', 'user_manager', 'Content', 'TaxonomyMap', 'DetailView', 'MethodMapper', 'Mapping', 'ViewManager']
