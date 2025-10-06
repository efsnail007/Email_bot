from django.urls import path

from .views import EmailAPI, EmailDetailAPI, UserAPI, UserDetailAPI

urlpatterns = [
    path("user/", UserAPI.as_view(), name="user_set"),
    path("user/<int:tg_id>/", UserDetailAPI.as_view(), name="user_detail"),
    path("user/<int:tg_id>/email/", EmailAPI.as_view(), name="email"),
    path(
        "user/<int:tg_id>/email/<str:pk>/",
        EmailDetailAPI.as_view(),
        name="email_detail",
    ),
]
