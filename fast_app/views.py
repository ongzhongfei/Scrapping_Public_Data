from django.shortcuts import render
from fast_app.models import tenure_raw

# Create your views here.

def home_view(request):

    #### Getting the distinct_dates. And only the last 10
    distinct_dates =  tenure_raw.objects.values_list('created_date').distinct().order_by('-created_date')[:10]
    distinct_dates = distinct_dates[::-1]
    #### Getting the distinct_tenures
    distinct_tenures = tenure_raw.objects.values_list('tenure').distinct()

    tenures = tenure_raw.objects.all()

    content = {
        'tenures' : tenures,
        'distinct_tenures' : distinct_tenures,
        'distinct_dates' : distinct_dates,
    }
    return render(request, 'home.html', content)