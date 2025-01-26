from django.shortcuts import render, redirect
from .models import Profile, Twoot
from django.contrib import messages
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        twoots = Twoot.objects.all().order_by("-created_at") #gets all twoots ordered newest to oldest
    return render(request, 'home.html',{"twoots":twoots})

def profile_list(request):
    if request.user.is_authenticated: #if user is logged in, go to the profile list page
        profiles = Profile.objects.exclude(user=request.user) #sends all profiles except user's profile to be displayed
        return render(request, 'profile_list.html',{'profiles':profiles})

    else: #if not logged in, redirect to home and send a warning message
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')

def profile(request, pk):
    if request.user.is_authenticated: #cannot view profiles unless logged in

        profile = Profile.objects.get(user_id=pk)
        twoots = profile.user.Twoots.all().order_by("-created_at") #gets all twoots made by user ordered newest to oldest
        #post form logic
        if request.method == "POST":
            user_profile = request.user.profile #user's profile
            action = request.POST['follow'] #gets value given by the form button
            if action == "unfollow": #unfollows currently selected profile
                user_profile.follows.remove(profile)
            elif action == "follow": #follows currently selected profile
                user_profile.follows.add(profile)
            user_profile.save() #saves changes

        return render(request, "profile.html", {"profile":profile,"twoots":twoots})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect('home')
