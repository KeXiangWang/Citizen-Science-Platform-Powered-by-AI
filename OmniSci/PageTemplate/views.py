from django.shortcuts import render
from django.http import HttpResponse
# ================================================================
#   Copyright (C) 2019 OmniSci. All rights reserved.
#
#   Title：views.py
#   Author：Feyoe Xia
#   Time：2019-04-01 22:20:39
#   Description：
#
# ================================================================

def show_template(request):
    return render(request,'page_template.html',)