import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView


class KakaoLoginView(APIView):

    def get(self, request):
        # kakao code 요청
        kakao_auth_uri = "https://kauth.kakao.com/oauth/authorize?response_type=code"
        client_id = "7e3239b54ab4208760ff31bb0f3d67ed"
        redirect_uri = "http://127.0.0.1:8000/kakao/oauth/callback"
        uri = f'{kakao_auth_uri}&client_id={client_id}&redirect_uri={redirect_uri}'

        res = redirect(uri)
        return res


class KakaoCallbackView(APIView):

    def get(self, request):
        auth_code = request.GET.get('code')
        kakao_token_api = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': "7e3239b54ab4208760ff31bb0f3d67ed",
            'redirect_uri': "http://127.0.0.1:8000/kakao/oauth/callback",
            'code': auth_code
        }

        token_response = requests.post(kakao_token_api, data=data)

        access_token = token_response.json().get('access_token')
        user_info_response = requests.get('https://kapi.kakao.com/v2/user/me',
                                          headers={'Authorization': f'Bearer ${access_token}'})

        return JsonResponse({"user_info": user_info_response.json()})
