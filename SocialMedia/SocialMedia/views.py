from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
    user = request.user
    text = "Hello "
    
    context = {
        'user': user,
        'text': text
    }
    return render(request, 'main/home.html',context)
    # return HttpResponse("Trang chu")