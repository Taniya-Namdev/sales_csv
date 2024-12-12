# csv_app/views.py

from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
import os
from django.conf import settings

def create_db(file_path):
    try:
        df = pd.read_csv(file_path, delimiter=',')
        print(df)
        # Add further processing logic here, e.g., saving data to the database
    except FileNotFoundError:
        return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def upload_file(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return Response({"error": "No file found in the request."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the uploaded file manually within MEDIA_ROOT
        uploaded_file = request.FILES['file']
        relative_path = os.path.join('files', uploaded_file.name)
        full_path = default_storage.save(relative_path, ContentFile(uploaded_file.read()))
        file_path = os.path.join(settings.MEDIA_ROOT, relative_path)
        
        # Process the file
        create_db(file_path)
        
        return Response({"message": "File uploaded and processed successfully!"}, status=status.HTTP_201_CREATED)
    return Response({"error": "File upload failed."}, status=status.HTTP_400_BAD_REQUEST)
