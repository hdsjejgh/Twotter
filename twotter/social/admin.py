from django.contrib import admin
from django.contrib.auth.models import Group,User
from .models import Profile, Twoot

# Register your models here.

#django automatically created a group model, it isnt needed
admin.site.unregister(Group)

class ProfileInline(admin.StackedInline):#used to display the profile of a user in
    model = Profile

class UserAdmin(admin.ModelAdmin): #the actual user thing that gets displayed in admin
    model = User
    fields = ["username"]
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin) #unregister and reregister the user model so it only shows the things in UserAdmin in the admin interface

admin.site.register(Twoot) #registers twoots in admin panel so you can see them





