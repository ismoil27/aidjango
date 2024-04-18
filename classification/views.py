import os
import zipfile
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from ultralytics import YOLO

def detect_objects(image_path):
    # Initialize YOLO model
    model = YOLO("/path/to/best.pt")  # Replace "/path/to/best.pt" with the actual path to your YOLO model

    # Detect objects in the image
    results = model(image_path)

    # Process the detection results as needed
    return results

def home(request):
    if request.method == 'POST' and request.FILES.getlist('images'):
        uploaded_files = request.FILES.getlist('images')
        detection_results = []

        for uploaded_file in uploaded_files:
            if uploaded_file.name.endswith('.zip'):
                # Extract the contents of the zip file
                with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                    temp_dir = os.path.join('/tmp', uploaded_file.name)
                    zip_ref.extractall(temp_dir)
                    
                    # Process each extracted file
                    extracted_files = os.listdir(temp_dir)
                    for extracted_file in extracted_files:
                        # Save the extracted files to a temporary location
                        fs = FileSystemStorage()
                        with open(os.path.join(temp_dir, extracted_file), 'rb') as file:
                            filename = fs.save(extracted_file, file)
                            uploaded_file_path = fs.url(filename)
                            
                            # Perform object detection on the extracted file
                            detection_result = detect_objects(uploaded_file_path)
                            detection_results.append(detection_result)
                            # Process the detection results as needed

                # Optionally, delete the temporary directory after processing
                os.rmdir(temp_dir)
            else:
                # Save the uploaded file to a temporary location
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name, uploaded_file)
                uploaded_file_path = fs.url(filename)
                
                # Perform object detection on the uploaded file
                detection_result = detect_objects(uploaded_file_path)
                detection_results.append(detection_result)
                # Process the detection results as needed

        return render(request, 'images_result.html', {'detection_results': detection_results})

    return render(request, 'home.html')




@csrf_exempt
def handle_zip(request):
    if request.method == 'POST' and request.FILES.get('zip_file'):
        zip_file = request.FILES['zip_file']

        # Create a temporary directory to extract the zip file
        temp_dir = os.path.join('/tmp', zip_file.name)

        try:
            # Extract the contents of the zip file
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Process each extracted file
            extracted_files = os.listdir(temp_dir)
            for extracted_file in extracted_files:
                # Save the extracted files to a temporary location
                fs = FileSystemStorage()
                with open(os.path.join(temp_dir, extracted_file), 'rb') as file:
                    filename = fs.save(extracted_file, file)
                    uploaded_file_path = fs.url(filename)
                    
                    # Perform object detection on the extracted file
                    # detection_results = detect_objects(uploaded_file_path)
                    # Process the detection results as needed

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        finally:
            # Delete the temporary directory after processing
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)

        return JsonResponse({'message': 'Zip file uploaded and extracted successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request'}, status=400)





def images_result(request):
    return render(request, 'images_result.html')




# login view business logic
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'success.html')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'login.html')