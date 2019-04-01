
from django.urls import path,include
from .views import signup


app_name = 'registration'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]