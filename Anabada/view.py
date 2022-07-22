from django.shortcuts import render
from rest_framework.views import APIView


class Main(APIView):
    def get(self, request):
        print('겟')
        return render(request, "Anabada/main.html")

    def post(self, request):
        print('포스트')
        return render(request, "Anabada/main.html")
