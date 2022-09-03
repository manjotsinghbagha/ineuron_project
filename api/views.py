from rest_framework import generics, permissions
from .serializers import MyCodeSerializer
from mycode.models import MyCode
from django.contrib.auth import get_user_model



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

