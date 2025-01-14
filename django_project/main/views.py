from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')  # 템플릿을 렌더링
