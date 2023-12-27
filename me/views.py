from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.http import Http404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Policeprofile,CitizenProfile,Complains
from .forms import ProfileCreationForm, CitizenCreationForm, ComplainsForm, SetPasswordForm
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage



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
def file_complaint(request):
    # Ensure the user is logged in and is a police officer
    # if not request.user.is_authenticated or not request.user.policeprofile:
    #     return redirect('login')  # Redirect to the login page or handle authentication as needed

    officer = request.user.policeprofile  # Get the logged-in police officer

    if request.method == 'POST':
        form = ComplainsForm(request.POST, initial={'officer': officer})
        if form.is_valid():
            citizen_id = form.cleaned_data.get('citizen_id')

            # Check if the citizen with the provided ID exists
            if citizen_id:
                # Assuming that 'citizen_id' is a field in 'CitizenProfile'
                citizen_profile = get_object_or_404(CitizenProfile, drivers_license_id=citizen_id)
                
                
                # Create a Complains instance with the associated citizen_profile
                complaint = form.save(commit=False)
                complaint.officer = officer
                complaint.citizens = citizen_profile
                complaint.save()

                # Optionally, you can redirect the user to a success page
                messages.success(request, 'Complaint filed successfully!')
                return redirect('landing')
            else:
                messages.error(request, 'Citizen with the provided ID does not exist.')
    else:
        form = ComplainsForm(initial={'officer': officer})

    return render(request, 'me/complains.html', {'form': form})




@login_required(login_url='police-login')
def police_logout(request):
    auth.logout(request)

    return redirect('police-login')

@login_required(login_url='police-login')
@csrf_protect
def index_police(request):

    user_profile = get_object_or_404(Policeprofile, user=request.user)
    
    #allowing the police search
    if request.method == "POST":
        q = request.POST.get('q', '')
        
        if q:
            multiple_q = Q(drivers_license_id__icontains=q) | Q(ghana_card_id__icontains=q)
            data = CitizenProfile.objects.filter(multiple_q)
            
            if data.exists():
                return render(request, 'me/officer_dashboard.html', {"user": user_profile, "data": data, "query": q,'time':datetime.now()})
            else:
                messages.info(request, "No matching results found.")
        
    if request.method == "POST":
        all_complains = Complains.objects.filter(officer=user_profile,citizens__isnull=False)
        return render(request, 'me/officer_dashboard.html', {"user": user_profile, "all_complains": all_complains,'time':datetime.now()})

    return render(request, 'me/officer_dashboard.html', {"user": user_profile, 'time':datetime.now()})



def specific_user(request,id):

    user = CitizenProfile.objects.get(Q(drivers_license_id=id) | Q(ghana_card_id=id))  

    return render(request, 'me/specific.html',{'user':user})

# @login_required(login_url='police-login')
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

    return render(request, 'me/edit_police_settings.html', {"user": user_profile, 'msg': msg, 'form': form})

######################################################### Citizen Related Views RELATED VIEWS -##############################################################################################
@login_required
def password_change(request):
    user = request.user
    if request.method == "POST":
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect("citizen-login")
        else:
            for error in list(form.errors_values()):
                messages.error(request, error)
    form = SetPasswordForm(user)
    return render(request ,'me/password_reset_confirm.html',{'form':form})
 

def activate(request,uidb64,token):
    user= get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,"thank You for your email confirmation")
    else:
        messages.error(request,"Activation link is invalid")

    return redirect('citizen-setting')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your citizen account"
    message =  render_to_string("me/template_acivate_account.html",{
    'user': user.username,
    'domain':get_current_site(request).domain,
    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
    'token': account_activation_token.make_token(user),
    'protocol':'https'if request.is_secure() else 'http'
   } )
    email= EmailMessage(mail_subject,message,to=[to_email])
    if email.send():

        messages.success(request,f"Dear <b>{user} </b> please go to your email {to_email} inbox and click on it to activate the email")
    else:
        message.error(request,f"problem sending email to {to_email} check if you typed the correct thing")

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
                # user.is_active = False
                user.save()    
                # activateEmail(request, user ,email)   
                        
                #log user in and redirect to setting page
                
                user_login = auth.authenticate(username=username, password=password)
                print("user_login",user_login)
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

def citizen_homepage(request):
    user_profile = get_object_or_404(CitizenProfile, user=request.user)
    if request.method == "POST":
        all_complains = Complains.pending(citizens=user_profile)
        return render(request, 'me/driver_dashboard.html', {"user": user_profile, "all_complains": all_complains,'time':datetime.now()})

  

    return render(request, 'me/driver_dashboard.html',{"user":user_profile,'time':datetime.now()})

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
