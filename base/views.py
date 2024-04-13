from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import OnboardingIndicator
from .serializers import OnboardingIndicatorSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView
from django.http import JsonResponse
from django.core import serializers
from django.core.files.base import ContentFile
from django.conf import settings
from PIL import Image
from io import BytesIO
import secrets
from rest_framework import viewsets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Product, Profile, BlacklistedToken, Topic, FriendList
from .serializers import ProductSerializer, TopicSerializer, FriendListSerializer


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import logging

logger = logging.getLogger(__name__)

from django.contrib.auth import authenticate
from django.http import JsonResponse
import json

from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.middleware.csrf import get_token

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import XboxTopic
from .serializers import XboxTopicSerializer

# # # # # # # # # # # # # PCTopics # # # # # # # # # # # # # # # # 

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class TopicCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = TopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TopicListView(APIView):
    def get(self, request, format=None):
        topics = Topic.objects.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

class TopicDetailView(APIView):
    def get_object(self, pk):
        try:
            return Topic.objects.get(pk=pk)
        except Topic.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        topic = self.get_object(pk)
        if topic:
            serializer = TopicSerializer(topic)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        topic = self.get_object(pk)
        if topic:
            serializer = TopicSerializer(topic, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        topic = self.get_object(pk)
        if topic:
            topic.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

# # # # # # # # # # # # # PCTopics Ends # # # # # # # # # # # # # # # # 

#### Login ######## Login ######## Login Start ####


def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        user_data = {
            'user_id': user.id,  # This sends the user ID to the client
            'access_token': AccessToken,  # Example token
        }
        print("Sending user data:", user_data)  # Debug print to check what's being sent
        return JsonResponse(user_data)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
    

        ######### Login Ends #####
        
        
### Register Start #######

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')  # Get email from request data

    if not username or not password or not email:
        return Response({'error': 'Username, password, and email are required'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)

    # Handle the uploaded photo
    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        # Resize and save the photo to the user's profile
        img = Image.open(photo)
        img.thumbnail((200, 200))  # Resize the image to fit within 200x200 pixels
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        user.customuser.photo.save(photo.name, ContentFile(thumb_io.getvalue()))

    return Response({'message': 'User registered successfully'})

            ############    Register Ends #############



# File uploads ######

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES:
        uploaded_file = request.FILES['file']
        # Process the uploaded file as needed
        # Save the file to a desired location, e.g., using `uploaded_file.save()`
        return JsonResponse({'message': 'File uploaded successfully.'})
    return JsonResponse({'error': 'Invalid request.'}, status=400)

def get_photo_data(request):
    tasks = Task.objects.all()
    photo_data = [TaskSerializer(task).data for task in tasks]
    return JsonResponse(photo_data, safe=False)


### End Files #######



   ########## On Boarding ######
   
@method_decorator(csrf_exempt, name='dispatch')
class OnboardingIndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = OnboardingIndicatorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return onboarding indicators for the logged-in user only."""
        return OnboardingIndicator.objects.filter(user=self.request.user)

    @method_decorator(csrf_exempt)
    @action(detail=True, methods=['post'], url_path='mark_as_read')
    def mark_as_read(self, request, pk=None):
        onboarding_step = self.get_object()
        if onboarding_step.user != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        if not onboarding_step.marked_as_read:
            onboarding_step.marked_as_read = True
            onboarding_step.save()
            return Response({'status': 'Marked as read'}, status=status.HTTP_200_OK)

        # Respond with 200 OK even if no change was made to signify the request was processed successfully
        return Response({'status': 'Already marked as read'}, status=status.HTTP_200_OK)

##### End boarding


###### Product Start #######
class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductUpdate(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDelete(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return JsonResponse(serializer.data, safe=False)

###### Product Ends #######


 ##Password Change logics #####
 
class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        # Process the form and send the password reset email
        response = super().form_valid(form)
        
        # Return a JSON response indicating the success of the email sending process
        return JsonResponse({'message': 'Password reset email has been sent.'})

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        form.save()
        return JsonResponse({'message': 'Password has been reset successfully.'})

class CustomPasswordResetDoneView(PasswordResetDoneView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'message': 'Password reset completed.'})



##### Password Change ends #####


 ### Logout Method ###
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header is None:
                raise TokenError('Access token not provided')

            access_token = auth_header.split(' ')[1]
            token = AccessToken(access_token)

            # Perform any additional logic for logout

            return Response({'message': 'Logout successful'}, status=200)
        except TokenError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

 ### Logout Method Ends ###


## Obtain Token + Userid data ##
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({'user_id': self.user.id})  # Add user_id to the token response
        return data

 
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Add CSRF token to response
        csrf_token = get_token(request)
        response.data.update({"csrf_token": csrf_token})
        return response

    # Add any other custom fields or methods to your user model

    def __str__(self):
        return self.username
    

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        new_refresh_token = response.data.get('refresh')
        if new_refresh_token:
            response.set_cookie('refresh_token', new_refresh_token, httponly=True, samesite='Strict')
        return response

## End Obtain Token + Userid data ### 



######### Friends list #####

class FriendListView(generics.ListCreateAPIView):
    queryset = FriendList.objects.all()
    serializer_class = FriendListSerializer

class FriendDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FriendList.objects.all()
    serializer_class = FriendListSerializer

class AddFriendView(generics.CreateAPIView):
    queryset = FriendList.objects.all()
    serializer_class = FriendListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Assuming the request data includes the user and friend usernames
            user = request.user  # Assuming you have authentication in place
            friend_usernames = serializer.validated_data['friends']

            # Retrieve the user's friend list
            friend_list, created = FriendList.objects.get_or_create(user=user)

            # Add friends to the friend list
            for username in friend_usernames:
                friend = User.objects.get(username=username)
                friend_list.friends.add(friend)

            return Response({'message': 'Friends added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


               ######  Friendlist END ###########



###### XBOX Start Methods #######

class XboxTopicViewSet(viewsets.ModelViewSet):
    queryset = XboxTopic.objects.all()
    serializer_class = XboxTopicSerializer
    #permission_classes = [IsAuthenticated]

class CreateXboxTopicView(generics.CreateAPIView):
    queryset = XboxTopic.objects.all()
    serializer_class = XboxTopicSerializer

    def perform_create(self, serializer):
        # Get the username from the request data
        username = self.request.data.get('author')

        # Get the user object based on the username
        user = User.objects.get(username=username)

        # Associate the user with the XboxTopic
        serializer.save(author=user)

class XboxTopicDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = XboxTopic.objects.all()
    serializer_class = XboxTopicSerializer
    
    
class DeleteXboxTopicView(generics.DestroyAPIView):
    queryset = XboxTopic.objects.all()
    serializer_class = XboxTopicSerializer

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#### XBOX Method Ends ####