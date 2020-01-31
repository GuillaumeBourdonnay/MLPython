from django.conf.urls   import url
from prediction         import views

urlpatterns = [
    url(r'^predict/$'              , views.predict),
    url(r'^incident/$'               , views.incident_list  ),
    url(r'^indicent/(?P<pk>[0-9]+)/$' , views.incident_detail),
]