
from django.shortcuts import render
from .models import Feedbacks, TheLostItems

# This function is used to list founditems feddbacks in airport staff dashboard.
    # From database it will get all the feedbacks.
        # From database it will get all the fonditems that are marked as found.
            # It will show them as list in dashboard  for my application.

def airportstaffdashboard(request):
    feedbacks_list = Feedbacks.objects.all()
    founditems_list = TheLostItems.objects.filter(found=True)
    context = {
        'feedbacks_list': feedbacks_list,
        'founditems_list': founditems_list,
    }
    return render(request, 'airport_staff/airport_staff_dashboard.html', context)