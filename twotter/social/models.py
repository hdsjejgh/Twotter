from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Profile(models.Model): #profile model is in every user model
    user = models.OneToOneField(User, on_delete=models.CASCADE) #each user has one unique profile
    follows = models.ManyToManyField("self", #follows contain any amount of other profiles
                                     related_name="followed_by",
                                     symmetrical=False, #so following doesn't have to go both ways
                                     blank=True) #following can be blank
    def __str__(self): #so the profile is displayed as the username
        return self.user.username

@receiver(post_save,sender=User)#when user is created, call this function
def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile = Profile(user=instance) #automatically creates profile when user is made
        user_profile.save()
        user_profile.follows.set([instance.profile.id]) #makes profil follow themselves
        user_profile.save()