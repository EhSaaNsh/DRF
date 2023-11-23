from . import views
from django.urls import path
from rest_framework.authtoken import views as auth_view



app_name = 'accounts'

urlpatterns = [
    path('register/', views.APIRegisterView.as_view()),
    path('api-token-auth/', auth_view.obtain_auth_token),
    path('follow/<int:user_id>/', views.UserFollowView.as_view()),
    path('unfollow/<int:user_id>/', views.UserUnFollowView.as_view()),
    path('following/', views.UserFollowingListView.as_view()),
    path('followers/', views.UserFollowersListView.as_view()),

]