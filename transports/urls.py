from django.urls import path

from . import views

urlpatterns = [
    path("transports/", views.transport_list, name="transport_list"),
    path("transports/recherche/", views.transport_search, name="transport_search"),
    path("transports/<int:pk>/", views.transport_detail, name="transport_detail"),
    path("transports/<int:pk>/retard/", views.transport_delay, name="transport_delay"),
    path("transports/<int:pk>/releves/", views.transport_readings, name="transport_readings"),
    path("transports/<int:pk>/cloturer/", views.transport_close, name="transport_close"),
    path("destinataires/", views.recipient_list, name="recipient_list"),
]
