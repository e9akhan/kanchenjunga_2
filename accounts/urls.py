"""
    Module name :- urls
"""


from django.urls import path
from accounts.views import SignUp, Login, Logout, EditProfile, DeleteProfile


app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUp.as_view(), name='sign-up'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('edit-profile/<int:pk>/', EditProfile.as_view(), name='edit-profile'),
    path('delete-profile/<int:pk>/', DeleteProfile.as_view(), name='delete-profile')
]