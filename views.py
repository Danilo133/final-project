from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from petnica.models import Profile
from file_upload.models import SubmittedRecord
import json
from django.utils import timezone

@login_required
def recordsPage(request):
    user = get_object_or_404(User, id=request.user.id)
    profile = get_object_or_404(Profile, user=request.user)
    approved_filter = request.GET.get('approved')
    
    if approved_filter is None:
        pending_records = SubmittedRecord.objects.filter(approved=None)
    elif approved_filter.lower() == 'true':
        pending_records = SubmittedRecord.objects.filter(approved=True)
    elif approved_filter.lower() == 'false':
        pending_records = SubmittedRecord.objects.filter(approved=False)

    user_data = json.dumps({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'firstName': user.first_name,
        'lastName': user.last_name
    })

    records_data = []
    for record in pending_records:
        record_fields = {field.name: field.value_from_object(record) for field in record._meta.fields}
        if record.approved_by:
            record_fields['approved_by_email'] = record.approved_by.email
            record_fields['approved_by_full_name'] = f"{record.approved_by.first_name} {record.approved_by.last_name}"
        if record.rejected_by:
            record_fields['rejected_by_email'] = record.rejected_by.email
            record_fields['rejected_by_full_name'] = f"{record.rejected_by.first_name} {record.rejected_by.last_name}"
        records_data.append(record_fields)

    return render(request, 'recordsPage.html', {
        'user': user,
        'profile': profile,
        'user_data': user_data,
        'records_data': records_data,
        'approved_filter': approved_filter  
    })

@login_required
def approve_record(request, record_id):
    record = get_object_or_404(SubmittedRecord, id=record_id)
    record.approved = True
    record.approved_by = request.user
    record.rejected_by = None
    record.last_update = timezone.now()
    record.save()
    return redirect('recordsPage')

@login_required
def reject_record(request, record_id):
    record = get_object_or_404(SubmittedRecord, id=record_id)
    record.approved = False
    record.rejected_by = request.user
    record.approved_by = None
    record.last_update = timezone.now()
    record.save()
    return redirect('recordsPage')

@login_required
def revoke_status(request, record_id):
    record = get_object_or_404(SubmittedRecord, id=record_id)
    record.approved = None
    record.approved_by = None
    record.rejected_by = None
    record.last_update = timezone.now()
    record.save()
    return redirect('recordsPage')
