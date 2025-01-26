from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Twoot(models.Model): #model for a twooter (offbrand tweet)
    user = models.ForeignKey( #many to one relationship between twoot and user, since many tweets can belong to one user
        User,
        related_name="Twoots", #so you can access twoots of a user
        on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=256) #max character count for twoot is 256
    created_at = models.DateTimeField(auto_now_add=True) #created at date is used for sorting

    def __str__(self):
        return f"(@{self.user})  \"{self.body}\"" #represents twoots in admin panel



class Profile(models.Model): #profile model is in every user model
    user = models.OneToOneField(User, on_delete=models.CASCADE) #each user has one unique profile
    #user automatically gets linked to profile when profile is linked to it
    follows = models.ManyToManyField("self", #follows contain any amount of other profiles
                                     related_name="followed_by", #so you can see every profile that follows this one
                                     symmetrical=False, #so following doesn't have to go both ways
                                     blank=True) #following can be blank
    date_modified = models.DateTimeField(User, auto_now=True) #last time a profile was modified
    def __str__(self): #so the profile is displayed as the username
        return self.user.username

@receiver(post_save,sender=User)#when user is created, call this function
def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile = Profile(user=instance) #automatically creates profile when user is made
        user_profile.save()
        user_profile.follows.set([instance.profile.id]) #makes profile follow themselves
        user_profile.save()