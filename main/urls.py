from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views.catalog import catalog
from .views.favourite import favourite
from .views.org_login import OrgLogin
from .views.org_profile import org_profile
from .views.profile import profile
from .views.login import Login, logout
from .views.reg import Signup
from .views.home import index
from .views.org_reg import OrgSignup
from .views.rentobject import rentobject
from .views.api import OrderList_detail

urlpatterns = [
    path('', index, name='home'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout, name='logout'),
    path('profile', profile, name='profile'),
    path('org_profile', org_profile, name='org_profile'),
    path('org_reg', OrgSignup.as_view(), name='org_reg'),
    path('org_login', OrgLogin.as_view(), name='org_login'),
    path('catalog', catalog, name='catalog'),
    path('rentobject', rentobject, name='rentobject'),
    path('favourite', favourite, name='favourite'),
    path('orderslist/', OrderList_detail),
]
if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


