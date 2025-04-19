from django.urls import path, include
from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.MyLoginView.as_view(), name="login"),
    path("logout/", views.MyLogoutView, name="logout"),
    path("reset/", views.MyResetView.as_view(), name="reset"),
    path('reset/<uidb64>/<token>', views.MyPasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("reset/done/", views.MyResetDoneView.as_view(), name="reset_done"),
    path('profile/', views.Profile.as_view(), name='users-profile'),
    path('password-change/', views.MyPasswordChangeView.as_view(), name='password_change'),
]