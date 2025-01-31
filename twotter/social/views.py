from django.shortcuts import render, redirect
from .models import Profile, Twoot
from django.contrib import messages
from .forms import TwootForm, RegisterForm
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def home(request):
    if request.user.is_authenticated: #if user logged in
        form = TwootForm(request.POST or None) #create form
        if request.method=="POST":
            if form.is_valid(): #if valid twoot
                twoot = form.save(commit=False)
                twoot.user = request.user
                twoot.save() #add new twoot
                messages.success(request, ("Twoot Posted")) #show success message
                return redirect('home')
        twoots = Twoot.objects.all().order_by("-created_at") #gets all twoots ordered newest to oldest
        return render(request, 'home.html',{"twoots":twoots,"form":form})
    else: #only show twoots (not form) when user not logged in
        twoots = Twoot.objects.all().order_by("-created_at") #gets all twoots ordered newest to oldest
        return render(request, 'home.html', {"twoots": twoots})

def profile_list(request):

    profiles = Profile.objects.all() if not request.user.is_authenticated else Profile.objects.exclude(user=request.user)  # sends all profiles except user's profile (if logged in) to be displayed
    return render(request, 'profile_list.html', {'profiles': profiles})

def profile(request, pk):
    if request.user.is_authenticated: #cannot view profiles unless logged in
        try:
            profile = Profile.objects.get(user_id=pk)
            twoots = profile.user.Twoots.all().order_by("-created_at") #gets all twoots made by user ordered newest to oldest
        except:
            profile = None
            twoots=None
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

def login_user(request):
    if request.method == "POST": #if attempting to log in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password) #user = None if invalid username or password
        if user is not None: #if valid username or password
            login(request,user)
            messages.success(request, ("Successfully logged in"))
            return redirect('home')
        else: #if invalid username or password
            messages.success(request, ("Invalid username or password"))
            return redirect('login')

    else: #if just openning the page
        return render(request, 'login.html',{})


def logout_user(request): #justs logs the user out
    logout(request)
    messages.success(request, ("Successfully logged out"))
    return redirect('home')

def register_user(request):
    form = RegisterForm() #creates new instance of registration form
    if request.method == "POST": #if user tries to register
        form = RegisterForm(request.POST)
        if form.is_valid(): #if valid info
            form.save() #creates iser
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password) #logs user in
            login(request, user)
            messages.success(request, ("Account registered successfully"))
            return redirect('home')

    return render(request, 'register_user.html', {'form':form}) #displays the form

