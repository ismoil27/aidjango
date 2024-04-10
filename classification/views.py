from django.shortcuts import render

def home(request):
    return render(request, 'home.html')




def images_result(request):
    return render(request, 'images_result.html')