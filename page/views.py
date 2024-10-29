from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import CustomuserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status, generics


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomuserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user_id': user.id,
            'username': user.username,
        }, status=status.HTTP_200_OK)
