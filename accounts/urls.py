from django.urls import path
from accounts import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path('api-token-auth/', obtain_auth_token),
    path('get_profile/', views.get_profile, name="get_profile"),
    path('crawl_pdf/', views.crawl_pdf, name="crawl_pdf"),
]
