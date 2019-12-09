from django.shortcuts import render
from .utils import is_pc
# Create your views here.

def contact(request):
    if is_pc(request.META['HTTP_USER_AGENT']):
        return render(request, 'contact_us.html')
    else:
        return render(request, 'contact_us_mobile.html')
