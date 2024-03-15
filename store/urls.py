"""
    Module name :- urls
"""


from django.urls import path
from store.views import Dashboard, CreateEquipmentType, UpdateEquipmentType, ListEquipment, CreateEquipment, UpdateEquipment, DeleteEquipment, DetailEquipment, ListAllocation

app_name = 'store'


urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('add-equipment-type/', CreateEquipmentType.as_view(),name='add-equipment-type'),
    path('update-equipment-type/<slug:slug>/', UpdateEquipmentType.as_view(), name='update-equipment-type'),
    path('equipments/<str:equipment_type>/', ListEquipment.as_view(), name='equipments'),
    path('add-equipment/', CreateEquipment.as_view(), name='add-equipment'),
    path('update-equipment/<slug:slug>/', UpdateEquipment.as_view(), name='update-equipment'),
    path('delete-equipment/<slug:slug>/', DeleteEquipment.as_view(), name='delete-equipment'),
    path('detail-equipment/<slug:slug>/', DetailEquipment.as_view(), name='detail-equipment'),
    path('allocations', ListAllocation.as_view(), name='allocations')
]