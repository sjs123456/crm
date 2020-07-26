'''
@Author: Jinsong Shi
@Date: 2020-07-26 03:17:19
@LastEditors: Jinsong Shi
@LastEditTime: 2020-07-26 14:39:26
@Description: file content
'''
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "index.html")


def customer_list(request):
    return render(request, "sales/customers.html")