from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response

from knox.models import AuthToken

from .models import Profile
from .serializers import CreateUserSerializer, UserSerializer, LoginUserSerializer, CreateProfileSerializer, ProfileSerializer


class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    permission_classes = [
        permissions.AllowAny  # check django default premissions.
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            # Returns a tuple (instance,token) need token
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    permission_classes = [
        permissions.AllowAny  # check django default premissions.
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class UserAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self):
        return self.request.user

    # update user information
    def update(self, request, *args, **kwargs):
        # update transaction
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class CreateProfileAPI(generics.GenericAPIView):
    serializer_class = CreateProfileSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        total = serializer.save()
        return Response({
            # Reponse is not necessary.
        })


class ProfileAPI(generics.ListAPIView):
    serializer_class = ProfileSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise Exception("Unauthorized Access")
        # queryset = Transaction.objects.filter(author=user)
        queryset = Profile.objects.filter(user=user)
        return queryset

    # def get_object(self):
    #     return self.request.total
