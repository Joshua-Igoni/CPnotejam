from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from notejam.health import healthz

from users.views import (SignupView, SigninView, AccountSettingsView, ForgotPasswordView)
from notes.views import NoteListView, NoteCreateView

urlpatterns = [
    path('healthz/', healthz, name='healthz'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('account/', login_required(AccountSettingsView.as_view()), name='account_settings'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('signout/', LogoutView.as_view(next_page='/'), name='signout'),

    path('notes/', include('notes.urls')),
    path('pads/', include('pads.urls')),

    path('', NoteListView.as_view(), name='notes'),
    path('', NoteListView.as_view(), name='home'),
    path('create/', NoteCreateView.as_view(), name='create_note'),
]
