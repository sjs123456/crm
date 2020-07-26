'''
@Author: Jinsong Shi
@Date: 2020-07-26 05:37:21
@LastEditors: Jinsong Shi
@LastEditTime: 2020-07-26 14:25:38
@Description: file content
'''

from django.urls import path
from student import views

urlpatterns = [
    path('/', views.student_list, name = 'stu_index')
]