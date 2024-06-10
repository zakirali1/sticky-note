from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.notes_all, name='notes_all'),
    path('manage_notes/', views.manage_notes, name='manage_notes'),
    path('delete-note/', views.delete_note, name='delete_note'),
    path('update-note/<int:pk>/', views.update_note, name='update_note'),
]
