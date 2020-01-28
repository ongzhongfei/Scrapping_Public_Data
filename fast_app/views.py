from django.shortcuts import render
from fast_app.models import tenure_raw

# Create your views here.

def home_view(request):
    #### Getting the distinct groups
    distinct_group = tenure_raw.objects.values_list('group').distinct()
    #### Getting the distinct_dates. And only the last 10
    distinct_dates =  tenure_raw.objects.values_list('created_date').distinct().order_by('-created_date')[:10]
    distinct_dates = distinct_dates[::-1]

    #### Getting the last date
    latest_date    = tenure_raw.objects.values_list('created_date').last()[0]

    #### Getting the distinct_tenures
    distinct_tenures = tenure_raw.objects.values_list('tenure').distinct()

    #### Getting the query set of diff groups. Not good because it returns all date for a group
    # distinct_tenures = [tenure_raw.objects.filter(group=x[0]).distinct() for x in distinct_group]

    #### Getting the distinct tenure title for each group
    distinct_tenures_mgs = tenure_raw.objects.values_list('tenure').distinct().filter(group='Government Securities (Conventional)')
    distinct_tenures_mgi = tenure_raw.objects.values_list('tenure').distinct().filter(group='Government Securities (Islamic)')

    tenures = tenure_raw.objects.all()

    content = {
        'tenures' : tenures,
        'distinct_tenures' : distinct_tenures,
        'distinct_dates' : distinct_dates,
        'distinct_group' : distinct_group,
        'distinct_tenures_mgs' : distinct_tenures_mgs,
        'distinct_tenures_mgi' : distinct_tenures_mgi,
        'latest_date' : latest_date,
    }
    return render(request, 'home.html', content)