
from rest_framework import serializers
from .models import Product,Category
from .models import Topic
from .models import FriendList

from .models import OnboardingIndicator

class OnboardingIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingIndicator
        fields = ['id', 'user', 'step', 'marked_as_read', 'created_at', 'updated_at']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = Product
        fields = ['id', 'desc', 'price', 'image', 'category']

    def create(self, validated_data):
        category = validated_data.pop('category')['name']
        category, _ = Category.objects.get_or_create(name=category)
        validated_data['category'] = category
        product = Product.objects.create(**validated_data)
        return product
    
class FriendListSerializer(serializers.ModelSerializer):
    friends = serializers.StringRelatedField(many=True)
    class Meta:
        model = FriendList
        fields = '__all__'

from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

from .models import XboxTopic  # Import your XboxTopic model here

class XboxTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = XboxTopic
        fields = ['id', 'topic', 'text', 'author', 'created_at']  # Include 'created_at' field
