from django.apps import AppConfig
from django.urls import reverse_lazy

class SkyhookTimerPlugin(AppConfig):
    name = 'skyhook_timer'
    verbose_name = 'Skyhook Timer'
    nav_menu_name = 'Skyhook Timer'  # This will be the label in the nav bar
    nav_menu_url = reverse_lazy('skyhook_timer:skyhook_timer_view')  # Link to the view that shows timers
    nav_icon = 'fas fa-clock'  # Optional: set an icon from FontAwesome (or use your own)