from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.template.defaultfilters import truncatechars 
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
        

class BlacklistedToken(models.Model):
    token = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]



class Topic(models.Model):
    topic = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photos', null=True, blank=True, default='/placeholder.png')
    author = models.CharField(max_length=255)
    text = models.TextField(default='default_text')  # Add a default value

    def __str__(self):
        return self.topic

class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend_list')
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='user_friends')

    def __str__(self):
        return f"Friends of {self.user.username}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship to the User model
    # Add additional fields for your user profile here
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.user.username  # You can return any field that represents the profile


class XboxTopic(models.Model):
    # Other fields
    topic = models.CharField(max_length=255)
    text = models.TextField()
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic


from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='photos', null=True, blank=True, default='/placeholder.png')
    desc = models.CharField(max_length=50, null=True, blank=True)
    price = models.IntegerField()
    createdTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.desc
    
    @property
    def short_description(self):
        return truncatechars(self.desc, 20)

    def admin_photo(self):
        return mark_safe('<img src="{}" width="100" />'.format(self.image.url))

    admin_photo.short_description = 'Image'
    admin_photo.allow_tags = True

    def __str__(self):
        return f'{self.desc} {self.price} {self.image}'



from django.conf import settings

class OnboardingIndicator(models.Model):
    ONBOARDING_STEPS = (
        ('terms_of_use', 'Terms of Use'),
        ('Gaming Social Solutions By Paz Please Mark As Read', 'My Games Screen'),
        ('messages', 'Messages Screen'),
        ('profile_setup', 'Profile Setup'),
        ('notifications', 'Notifications Setup'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    step = models.CharField(max_length=50, choices=ONBOARDING_STEPS)
    marked_as_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.step} - {'Read' if self.marked_as_read else 'Unread'}"
