from django.urls import path
from . import views
from .views import NoteDetailView

urlpatterns = [
    path('', views.NoteListView.as_view(), name='notes'),
    path('create/', views.NoteCreateView.as_view(), name='create_note'),
    path('note/<int:pk>/', NoteDetailView.as_view(), name='view_note'),
    path('<int:pk>/edit/', views.NoteUpdateView.as_view(), name='edit_note'),
    path('<int:pk>/delete/', views.NoteDeleteView.as_view(), name='delete_note'),
]
