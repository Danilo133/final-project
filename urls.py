from django.urls import path
from .views import recordsPage, approve_record, reject_record, revoke_status

urlpatterns = [
    path('', recordsPage, name='recordsPage'),
    path('records/approve/<int:record_id>/', approve_record, name='approve_record'),
    path('records/reject/<int:record_id>/', reject_record, name='reject_record'),
    path('records/revoke_status/<int:record_id>/', revoke_status, name='revoke_status'),
]
