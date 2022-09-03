from rest_framework import generics, permissions
from .serializers import MyCodeSerializer
from mycode.models import MyCode
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.db import IntegrityError

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=201)
        except IntegrityError:
            return JsonResponse({'error':'That username has already been taken. Please choose a new username'}, status=400)




class MyCodeListCreate(generics.ListCreateAPIView):
    serializer_class = MyCodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MyCode.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MyCodeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MyCodeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return MyCode.objects.filter(user=user)

