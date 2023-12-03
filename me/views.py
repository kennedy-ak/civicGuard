from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import JsonResponse
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Policeprofile,CitizenProfile,Complains
from .forms import ProfileCreationForm, CitizenCreationForm, ComplainsForm


# Create your views here.

########################################################## POLICE RELATED VIEWS -##############################################################################################

def home(request):
    return render(request, 'me/index.html')

def police_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password  = request.POST['password']
        password2 = request.POST['password2']        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'ServiceID already in Use')
                return redirect('police-register')          
            
            else:
                user = User.objects.create_user(username=username,password=password)
                user.save()                
                #log user in and redirect to setting page
                
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                # create a profile object
                user_model = User.objects.get(username=username)
                new_police_profile = Policeprofile.objects.create(user=user_model,service_id=username)
                new_police_profile.save()
                return redirect('police-settings')
        else:
            messages.info(request,'Password Not Matching')
            return redirect('police-register')            

    else:
        return render(request, 'me/police_register.html')
    return render(request, 'me/police_register.html')
   
def police_login(request):
    all_police = Policeprofile.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']


        matched_id = all_police.filter(service_id__icontains=username)
        if matched_id.exists():
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('landing')
            else:
                messages.info(request, 'Credentials Invalid')
                return redirect('police-login')
        else:
            messages.info(request,'Information is not POlice')
            return redirect('police-login')
    return render(request, 'me/police_login.html')




@login_required(login_url='police-login')
def police_logout(request):
    auth.logout(request)

    return redirect('police-login')

@login_required(login_url='police-login')
@csrf_protect
def index_police(request):
    user_profile = get_object_or_404(Policeprofile, user=request.user)
    # # Assuming CitizenProfile has fields 'drivers_id' and 'ghanacard_id'
    # all_citizens = CitizenProfile.objects.all()



    # if request.method == "POST":
    #     query = request.POST.get('q', '')

    #     # Case-insensitive search for citizens whose driver's ID or GhanaCard ID contains the query
    #     matched_citizens = all_citizens.filter(drivers_license_id__icontains=query) | all_citizens.filter(ghana_card_id__icontains=query)
        
    #     if matched_citizens.exists():
    #         # Redirect to the first matching citizen
    #         return redirect('specific', identifier=matched_citizens.first().drivers_license_id)        
    #     else:
    #         # Handle the case where no matching citizens were found
    #         messages.info(request,"User does does not exist")
    #         return render(request, 'me/index_police.html', {"user": user_profile, "query": query})

    return render(request, 'me/index_police.html', {"user": user_profile})
def specific_user(request,id):
    return render(request 'me/specific.html')

@login_required(login_url='police-login')
def police_setting(request):
    if request.user.is_authenticated: 
 

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

            
                return redirect('landing')

        return render(request, 'me/police_setting.html', {'forms': ProfileCreationForm()})
    else:
        return render(request, 'me/police_setting.html', {'forms': ProfileCreationForm()})

@login_required(login_url='police-login')
def edit_setting(request):
    user_profile, created = Policeprofile.objects.get_or_create(user=request.user)
    msg = ""

    if request.method == "POST":
        form = ProfileCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile.image = form.cleaned_data['image']
            user_profile.rank = form.cleaned_data['rank']
            user_profile.first_name = form.cleaned_data['first_name']
            user_profile.last_name = form.cleaned_data['last_name']
            user_profile.save()
            msg = "Information Saved"
            return redirect('landing')
        else:
            msg = "Form is not valid. Check for errors."

    else:
        form = ProfileCreationForm(initial={
            'image': user_profile.image,
            'rank': user_profile.rank,
            'first_name': user_profile.first_name,
            'last_name': user_profile.last_name,
        })

    return render(request, 'me/edit_settings.html', {"user": user_profile, 'msg': msg, 'form': form})

######################################################### Citizen Related Views RELATED VIEWS -##############################################################################################

def citizen_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password  = request.POST['password']
        password2 = request.POST['password2']        
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username already in Use')
                return redirect('citizen-register')          
            
            else:
                user = User.objects.create_user(username=username,password=password)
                user.save()                
                #log user in and redirect to setting page
                
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                # create a profile object
                user_model = User.objects.get(username=username)
                new_citizen_profile = CitizenProfile.objects.create(user=user_model,username=username)
                new_citizen_profile.save()
                return redirect('citizen-setting')
        else:
            messages.info(request,'Password Not Matching')
            return redirect('citizen-register')

            

    else:
        return render(request, 'me/citizen_register.html')
    return render(request, 'me/citizen_register.html')

    return render(request, 'me/citizen_register.html')

def citizen_login(request):
    all_citizens = CitizenProfile.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        matched_username = all_citizens.filter(username__icontains=username)
        if matched_username.exists():
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request,user)
                print("login-passed")
                return redirect('home-page')
            else:
                messages.info(request, 'Credentials Invalid')
                return redirect('citizen-login')
        else:
            messages.info(request ,"A Citizen with those Credentials does not exit")
            return redirect('citizen-login')
    return render(request, 'me/citizen_login.html',)

@login_required(login_url='citizen-login')
def citizen_setting(request):
    # user_profile, created = Policeprofile.objects.get_or_create(user=request.user)

    citizen_profile ,created = CitizenProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = CitizenCreationForm(request.POST, request.FILES)
        if form.is_valid():
           
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            ghana_card_id = form.cleaned_data['ghana_card_id']
            ghana_card_front_image = form.cleaned_data['ghana_card_image_front']
            ghana_card_back_image = form.cleaned_data['ghana_card_image_back']
            drivers_id = form.cleaned_data['drivers_license_id']
            drivers_license_image = form.cleaned_data['drivers_license_image']
            post_address = form.cleaned_data['post_address']
            phone_number = form.cleaned_data['phone_number']

            if CitizenProfile.objects.filter(drivers_license_id=drivers_id).exists():
                messages.info(request,"The Drivers Id Provides already exist")
                return redirect('citizen-settings')
            elif CitizenProfile.objects.filter(ghana_card_id=ghana_card_id).exists():
                messages.info(request, "Ghana card already in use")
                return redirect('citizen-settings')

            else:

                citizen_profile.first_name = first_name
                citizen_profile.last_name = last_name
                citizen_profile.ghana_card_id = ghana_card_id
                citizen_profile.ghana_card_image_front = ghana_card_front_image
                citizen_profile.ghana_card_image_back = ghana_card_back_image
                citizen_profile.drivers_license_id = drivers_id
                citizen_profile.driver_license_Image_front = drivers_license_image
                citizen_profile.postal_address = post_address
                citizen_profile.phone_number = phone_number

                citizen_profile.save()
                
                return redirect('home-page')

            


    return render(request,'me/citizen_setting.html',{'form':CitizenCreationForm()})


@login_required(login_url='citizen-login')
def citizen_logout(request):
    auth.logout(request)

    return redirect('citizen-login')

@login_required(login_url='citizen-login')
def citizen_homepage(request):
    user_profile = get_object_or_404(CitizenProfile, user=request.user)
  

    return render(request, 'me/index-citizen.html',{"user":user_profile})

@login_required(login_url='citizen-login')
def edit_citizen_setting(request):
    citizen_profile ,created = CitizenProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = CitizenCreationForm(request.POST,request.FILES)
        if form.is_valid():
            citizen_profile.first_name = form.cleaned_data['first_name']
            citizen_profile.last_name = form.cleaned_data['last_name']
            # citizen_profile.ghana_card_id = form.cleaned_data['ghana_card_id']
            # citizen_profile.ghana_card_image_front = form.cleaned_data['ghana_card_image_front']
            # citizen_profile.ghana_card_image_back = form.cleaned_data['ghana_card_image_back']
            # citizen_profile.drivers_license_id = form.cleaned_data['drivers_license_id']
            # citizen_profile.driver_license_Image_front = form.cleaned_data['drivers_license_image']
            citizen_profile.postal_address = form.cleaned_data['post_address']
            citizen_profile.phone_number = form.cleaned_data['phone_number']
            citizen_profile.save()
            return redirect('home-page')
            
    else:
        form = CitizenCreationForm(initial={
            'first_name':citizen_profile.first_name,
            'last_name':citizen_profile.last_name,
            'ghana_card_id' : citizen_profile.ghana_card_id,
            'ghana_card_image_front': citizen_profile.ghana_card_image_front,
            'ghana_card_image_back': citizen_profile.ghana_card_image_back,
            'drivers_license_id': citizen_profile.drivers_license_id,
            'drivers_license_image':citizen_profile.driver_license_Image_front,
            'post_address': citizen_profile.postal_address,
            'phone_number':citizen_profile.phone_number

        })

    return render(request,'me/edit_citizen_setting.html',{'form':form})

def test(request):
    return render(request, 'me/test.html')
