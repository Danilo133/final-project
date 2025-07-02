from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from petnica.models import Profile
from django.contrib.auth.models import User
from django.utils import timezone
from .models import SubmittedRecord, Plant
import json
from django.http import JsonResponse
import botocore.config
import boto3
import os
import re
from .models import SubmittedRecord, Plant
from pprint import pprint

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

@login_required
def uploadHomePage(request):
    user = get_object_or_404(User, id=request.user.id)
    profile = get_object_or_404(Profile, user=request.user)
    plants = Plant.objects.all()
    
    plants_data = json.dumps([{'id': plant.id, 'serbian_name': plant.serbian_name, 'latin_name': plant.latin_name} for plant in plants])
    user_data = json.dumps({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'firstName': user.first_name,
        'lastName': user.last_name
    })

    return render(request, 'uploadPage.html', {
        'user': user,
        'profile': profile,
        'user_data': user_data,
        'plants_data': plants_data
    })


def uploadFormSubmit(request):
    try:
        if request.method == 'POST':

            datetime = request.POST.get('datetime')
            formatted_photoshoot_date = timezone.datetime.strptime(datetime, '%Y-%m-%dT%H:%M').date()
            locality = request.POST.get('locality')
            plant_name_serbian = request.POST.get('plant_name_serbian')
            plant_name_latin = request.POST.get('plant_name_latin')
            plant_species_id = request.POST.get('plant_species_serbian')
            about = request.POST.get('about')
            session_id = request.POST.get('sessionID')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            photos = request.FILES.getlist('photos')

            session = boto3.Session(
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name='us-east-1'
            )
            s3_client = session.client('s3')

            bucket_name = 'petnica-web'
            prefix = f'{session_id}/' 
            s3_objects = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

            file_urls = []
            if 'Contents' in s3_objects:
                for obj in s3_objects['Contents']:
                    file_url = f"https://{bucket_name}.s3.amazonaws.com/{obj['Key']}"
                    file_urls.append(file_url)

            plant_species = Plant.objects.get(id=plant_species_id)
            plant_species_serbian = plant_species.serbian_name
            plant_species_latin = plant_species.latin_name

            record = SubmittedRecord(
                first_name=first_name,
                last_name=last_name,
                email=email,
                photoshoot_date=formatted_photoshoot_date,
                location=locality,
                plant_name_serbian=plant_name_serbian,
                plant_name_latin=plant_name_latin,
                plant_species_serbian=plant_species_serbian,
                plant_species_latin=plant_species_latin,
                about=about,
                file_names=[photo.name for photo in photos],
                file_urls=file_urls,
                session_id=session_id,
                approved=None
            )

            record.save()

            return JsonResponse({'message': 'Form data received successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Invalid request method'}, status=400)
    except Plant.DoesNotExist:
        return JsonResponse({'message': 'Plant species not found'}, status=404)
    except Exception as e:
        print(f'Error: {str(e)}')
        return JsonResponse({'message': 'An unexpected error occurred', 'error': str(e)}, status=500)
    

def generate_presigned_url(request):

    session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-1'
    )

    s3_client = session.client("s3", config=botocore.config.Config(signature_version='s3v4'))

    content_type = request.GET.get('content_type')
    batch_path = request.GET.get('batch_path')
    file_name_raw = request.GET.get('file_name')
    file_name = clean_string_for_bucket(file_name_raw)

    if not content_type:
        return JsonResponse({'error': 'Missing content type'}, status=400)
    elif not batch_path:
        return JsonResponse({'error': 'Missing batch path'}, status=400)
    elif not file_name:
        return JsonResponse({'error': 'Missing file name'}, status=400)

    key = f"{batch_path}/{file_name}"
    print(key)
    try:
        presigned_url = s3_client.generate_presigned_url('put_object',
                                                 Params={'Bucket': 'petnica-web',
                                                         'Key': key,
                                                         'ContentType': content_type},
                                                 ExpiresIn=3600)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'url': presigned_url})


def clean_string_for_bucket(value):
    if value is None:
        return ''
    value = re.sub(r'[^\w\s.]', '_', value)
    value = re.sub(r'_{2,}', '_', value)
    return value.strip()


