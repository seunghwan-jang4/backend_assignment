from django.http import HttpResponse

def index(request): # 기본 인덱스 뷰 함수
    return HttpResponse("Hello, world!")