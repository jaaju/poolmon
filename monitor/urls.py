from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import (
    RegisterPoolOwner,
    Login,
    AddPool,
    ListPools,
    PostPoolReading,
    ListPoolReading,
)

urlpatterns = [
    url(r'^register$', RegisterPoolOwner.as_view(), name='register'),
    url(r'^login/', Login.as_view(), name='login'),
    url(r'^logout$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^add-pool$', AddPool.as_view(), name='add-pool'),
    url(r'^post-pool-reading', PostPoolReading.as_view(),
        name='post-pool-reading'),
    url(r'^readings$', ListPoolReading.as_view(), name='readings'),
    url(r'^$', ListPools.as_view(), name='pools'),
]
