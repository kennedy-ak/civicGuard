from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Policeprofile
from .forms import ProfileCreationForm


# Create your views here.

############################################# POLICE RELATED VIEWS -##############################################################################################
def home(request):
    return render(request, 'me/index.html')


def police_landing(request):

    return render(request, 'me/police_landing.html')

def police_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password  = request.POST['password']
        password2 = request.POST['password2']        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'ServiceID already in Use')
                return redirect('police-register')          
            
            else:
                user = User.objects.create_user(username=username,password=password)
                user.save()                
                #log user in and redirect to setting page
                
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                # create a profile object
                user_model = User.objects.get(username=username)
                new_police_profile = Policeprofile.objects.create(user=user_model,id_user= user_model.id,service_id=username)
                new_police_profile.save()
                return redirect('police-settings')
        else:
            messages.info(request,'Password Not Matching')
            return redirect('police-register')

            

    else:
        return render(request, 'me/police_register.html')
    return render(request, 'me/police_register.html')
    
def police_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('landing')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('police-login')
    return render(request, 'me/police_login.html')


def police_logout(request):
    auth.logout(request)

    return redirect('police-login')

def index_police(request):
    user_profile = get_object_or_404(Policeprofile, user=request.user)
    # user_profile = Policeprofile.objects.get(user=request.user)
    print(user_profile.service_id)
    return render(request, 'me/index_police.html',{"user":user_profile})



def police_setting(request):
    user_profile, created = Policeprofile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileCreationForm(request.POST, request.FILES)
        if form.is_valid():
            rank = form.cleaned_data['rank']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            image = form.cleaned_data['image']

            user_profile.image = image
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.rank = rank
            user_profile.save()

            print("User profile saved successfully")  # Add this line for debugging

            return redirect('landing')

    print("Form is not valid or not a POST request")  # Add this line for debugging
    return render(request, 'me/police_setting.html', {'forms': ProfileCreationForm()})





############################################# Citizen Related Views RELATED VIEWS -##############################################################################################


def citizen_landing(request):

    return render(request, 'me/citizen_landing.html')

def citizen_register(request):

    return render(request, 'me/citizen_register.html')


def citizen_login(request):
    return render(request, 'me/citizen_login.html')

def citizen_setting(request):
    pass

def citizen_logout(request):
    pass

def citizen_homepage(request):
    pass