from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('add/', views.add_student, name='add_student'),
    path('students/', views.list_students, name='list_students'),
    path('student/<int:student_id>/', views.update_student, name='update_student'),   # PUT
    path('student/<int:student_id>/delete/', views.delete_student, name='delete_student'), # DELETE
    path('', views.index, name='index'),
]

