from django.urls import path
from django.contrib.auth.decorators import login_required

from pads.views import (
    PadCreateView, PadNotesListView, PadUpdateView, PadDeleteView
)

urlpatterns = [
    path('create/', login_required(PadCreateView.as_view()), name='create_pad'),
    path('<int:pk>/', login_required(PadNotesListView.as_view()), name='view_pad_notes'),
    path('<int:pk>/delete/', login_required(PadDeleteView.as_view()), name='delete_pad'),
    path("pads/<int:pk>/edit/", PadUpdateView.as_view(), name="edit_pad"),
]
