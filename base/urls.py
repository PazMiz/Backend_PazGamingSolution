from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import (
    MyTokenObtainPairView,
    LogoutView,
    register,
    get_photo_data,
    ProductList,
    ProductCreate,
    ProductDetail,
    ProductUpdate,
    ProductDelete,
    TopicViewSet,
    TopicCreateView,
    TopicListView,
    TopicDetailView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetDoneView,
    FriendListView,
    FriendDetailView,
    AddFriendView,
    XboxTopicViewSet,
    XboxTopicDetailView,
    CreateXboxTopicView,
    DeleteXboxTopicView,
    OnboardingIndicatorViewSet
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

# Setup API routers for topics
topic_router = DefaultRouter()
topic_router.register(r'topics', TopicViewSet)

# Create a router and register our viewsets with it.
onboarding_router = DefaultRouter()
onboarding_router.register(r'indicators', OnboardingIndicatorViewSet, basename='onboarding-indicator')

urlpatterns = [
    path('', include(topic_router.urls)),  # Include topic router urls
    path('onboarding/', include(onboarding_router.urls)),  # Include onboarding router under 'onboarding/'

    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('register/', register, name='register'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('reset_password/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset_password/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),

    path('photos/', get_photo_data, name='get_photo_data'),

    path('products/', ProductList.as_view(), name='product-list'),
    path('products/create/', ProductCreate.as_view(), name='product-create'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('products/<int:pk>/update/', ProductUpdate.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDelete.as_view(), name='product-delete'),
    
    path('topics/create/', TopicCreateView.as_view(), name='create_topic'),
    path('topics/list/', TopicListView.as_view(), name='list_topics'),
    path('topics/detail/<int:pk>/', TopicDetailView.as_view(), name='detail_topic'),
    
    path('friends/', FriendListView.as_view(), name='friend_list'),
    path('friends/<int:pk>/', FriendDetailView.as_view(), name='friend_detail'),
    path('friends/add/', AddFriendView.as_view(), name='add_friend'),

    path('xboxtopics/', XboxTopicViewSet.as_view({'get': 'list'}), name='xbox_topic_list'),
    path('xboxtopics/<int:pk>/', XboxTopicDetailView.as_view(), name='xbox_topic_detail'),
    path('xboxtopics/create/', CreateXboxTopicView.as_view(), name='create_xbox_topic'),
    path('xboxtopics/<int:pk>/delete/', DeleteXboxTopicView.as_view(), name='delete_xbox_topic'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
