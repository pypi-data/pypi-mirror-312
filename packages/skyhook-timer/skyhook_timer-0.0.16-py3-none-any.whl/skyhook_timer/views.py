from django.shortcuts import render
from .models import SkyhookTimer
# from django.contrib.auth.decorators import state_required

# @state_required(['Member'])
def skyhook_timer_view(request):
    # Get all timers for the member to view
    timers = SkyhookTimer.objects.all()

    # Render the view, allow "Members" to see but not interact with the data
    return render(request, 'skyhook_timer/view_timers.html', {'timers': timers})
