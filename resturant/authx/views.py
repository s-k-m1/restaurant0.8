import secrets
from django.urls import reverse
from django.shortcuts import render,redirect


from .models import CustomUser, Profile



from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm


from .models import Otp

from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail

# Create your views here.
"""
def registerPage(request):
    if request.method == "POST":
        data = request.POST
        fname = data["fullName"]
        phone = data["phoneNumber"]
        uname = data["username"]
        email = data["email"]
        password = data["password"]
        confirm_password = data["confirmPassword"]


        if password == confirm_password:
            if CustomUser.objects.filter(username=uname).exists():
                messages.error(request, "Username already exists")
                return redirect('register')
            
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
                return redirect('register')

            CustomUser.objects.create_user(full_name=fname, phone_number=phone, username=uname, email=email, password=password)
            messages.success(request, "Register successfully")
            return redirect('register')
        else:
            messages.error(request, "Password do not match")
            return redirect('register')         #url ko name = "register" waala register ho

    return render(request, "auth/Register.html")
"""

"""
#now including validation
def registerPage(request):
    if request.method == "POST":
        data = request.POST
        fname = data["fullName"]
        phone = data["phoneNumber"]
        uname = data["username"]
        email = data["email"]
        password = data["password"]
        confirm_password = data["confirmPassword"]


        if password == confirm_password:
            try:
                validate_password(password)

                if CustomUser.objects.filter(username=uname).exists():
                    messages.error(request, "Username already exists")
                    return redirect('register')
                
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists")
                    return redirect('register')
                
                CustomUser.objects.create_user(full_name=fname, phone_number=phone, username=uname, email=email, password=password)
                messages.success(request, "Register successfully")
                return redirect('register')
            except ValidationError as e:
                for err in e.messages:
                    messages.error(request, err)
                return redirect('register')

        else:
            messages.error(request, "Password do not match")
            return redirect('register')         #url ko name = "register" waala register ho

    return render(request, "auth/Register.html")
"""
def registerPage(request):
    if request.method == "POST":
        data = request.POST
        fname = data["fullName"]
        phone = data["phoneNumber"]
        uname = data["username"]
        email = data["email"]
        password = data["password"]
        confirm_password = data["confirmPassword"]

        if password == confirm_password:
            try:
                # user = CustomUser(full_name=fname, phone_number=phone, username=uname, email=email)
                # validate_password(password, user)
                validate_password(password)

                #for more validation
                if not re.search(r'[A-Z]', password):
                    messages.error(request, "Password must contain atleast one capital letter")
                    return redirect('register')
                
                if not re.search(r'\d', password):
                    messages.error(request, "Password must contain digit")
                    return redirect('register')
                
               #special character
                # Check for at least one special character[i.e. @, #, $, !, %, *, ^, +, =, ?, /, :, ;, etc., and underscore(_)]
                if not re.search(r'[\W_]', password):        # \W matches any non-word character (special characters)
                    messages.error(request, "Password must have atleast one special character!")
                    return redirect('register')

                if CustomUser.objects.filter(username=uname).exists():
                    messages.error(request, "Username already exists")
                    return redirect('register')
                
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists")
                    return redirect('register')
                
                if CustomUser.objects.filter(phone_number=phone).exists():
                    messages.error(request, "Phone number already exists")
                    return redirect('register')
                
                CustomUser.objects.create_user(full_name=fname, phone_number=phone, username=uname, email=email, password=password)
                messages.success(request, "Register successfully")
                return redirect('register')
            except ValidationError as e:
                for err in e.messages:
                    messages.error(request, err)
                return redirect('register')

        else:
            messages.error(request, "Password do not match")
            return redirect('register')         #url ko name = "register" waala register ho

    return render(request, "auth/Register.html")

"""
def loginPage(request):
    if request.method == "POST":
        data = request.POST
        em = data["email"]
        psw = data["password"]

        # user = authenticate(request, email=em, password=psw)     #user(user object) or None
        user = authenticate(email=em, password=psw)     #user(user object) or None

        if user is not None:            #if user
            login(request,user)
            return redirect('menu_page')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')

    return render(request, "auth/Login.html")

"""

def loginPage(request):
    if request.method == "POST":
        data = request.POST
        em = data["email"]
        psw = data["password"]

        remember_me = data.get("rem_me")
        # print("===================================", remember_me)

        # user = authenticate(request, email=em, password=psw)     #user(user object) or None
        user = authenticate(email=em, password=psw)     #user(user object) or None

        if user is not None:            #if user
            login(request,user)
            if remember_me:     #if True
                # request.session.set_expiry(22)      #add session     #login unitl 22 second but logout after 22 second
                request.session.set_expiry(86400)      #add session     #login for 1 day(i.e. 86400 second) but logout after 24 hour
            else:
                request.session.set_expiry(0)       #destrory session  #logout when browser close

            return redirect('menu_page')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')

    return render(request, "auth/Login.html")


def logout_function(request):
    logout(request)
    messages.success(request, "logout successfully")
    return redirect('login')

@login_required(login_url="login")    
def changePassword(request):
    form = PasswordChangeForm(user=request.user)    
    if request.method == "POST":
        #receive form data
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Password change sucessfully")
            return redirect('login')
    return render(request, "auth/ChangePassword.html", {"form":form})




def resetPasswordEmailSend(request):
    if request.method == "POST":
        data = request.POST
        em = data["email"]

        #At first, check user exist or not using this email
        if not CustomUser.objects.filter(email=em).exists():
            messages.error(request, "Invalid email address")
            return redirect('reset_password_email_send')
        
                 
        user = CustomUser.objects.get(email=em)
        #Delete previous otp of this user
        # otp = Otp.objects.filter(user=user)
        # otp.delete()
        #===== in one line =========
        Otp.objects.filter(user=user).delete()
        
        #====== now generate otp in database and send it in email =======
        #======= generate 6 digit opt ==========
        otp = ''.join(secrets.choice("0123456789") for _ in range(6))
       #save into database
        Otp.objects.create(
            user=user,
            otp=otp,
            created_at=timezone.now(),
            expired_at=timezone.now()+timedelta(minutes=5)
        )
        #send email
        subject = "OTP Verification",
        message =  f'''
                    Your Otp is {otp}.
                    Please verify within 5 minute.
                    Do not share it with anyone.
                    '''

        from_email = "skycse001@gmail.com"
        recipient_list = [em]

        import threading
        #send
        #send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list, fail_silently=False)
        t1 = threading.Thread(
            target=send_mail,
            args=(subject, message, from_email, recipient_list, False),
            daemon=True
        )
        t1.start()

        messages.success(request, "OTP sent successfully. Please check your email.")
        
        
        return redirect(reverse('verify_otp') + f'?user_id={user.id}')
    return render(request, "auth/reset-password/ResetPasswordEmailSend.html")


#=======user_id methods passings throughs urls ==============
def verifyOtp(request):
    user_id = request.GET.get("user_id") # Get from URL
    
    if request.method == "POST":
        otp_input = request.POST.get("otp")
        user = CustomUser.objects.get(id=user_id)

        otp_record = Otp.objects.filter(
            user=user, 
            otp=otp_input,
            expired_at__gte=timezone.now()).first()

        if otp_record:
            otp_record.delete()
            # ==========pass user_id to the URL==========
            return redirect(reverse('reset_password') + f'?user_id={user_id}')
        else:
            messages.error(request, "Invalid or expired OTP")
            
    return render(request, "auth/reset-password/VerifyOtp.html", {"user_id": user_id})

def resetPassword(request):
    user_id = request.GET.get('user_id')

    if not user_id:
        return redirect('reset_password_email_send')

    if request.method == "POST":
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect(request.path + f'?user_id={user_id}')

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found")
            return redirect('reset_password_email_send')

        user.set_password(new_password)
        user.save()

        messages.success(request, "Password reset successful!")
        return redirect('login')

    return render(request, "auth/reset-password/ResetPasswordForm.html", {
        "user_id": user_id
    })
"""
#=======section methods ===============
def verifyOtp(request):
    user_id = request.GET.get("user_id")

    if not user_id:
        messages.error(request, "Invalid request")
        return redirect('reset_password_email_send')

    try:
        user = CustomUser.objects.get(id=user_id)
    except (CustomUser.DoesNotExist, ValueError):
        messages.error(request, "User not found")
        return redirect('reset_password_email_send')

    if request.method == "POST":
        otp_input = request.POST.get("otp")

        #====== otp check correct and not expired=========
        otp_record = Otp.objects.filter(
            user=user, 
            otp=otp_input,
            expired_at__gte=timezone.now()
        ).first()

        if not otp_record:
            messages.error(request, "Invalid or expired OTP")
            return redirect(reverse('verify_otp') + f'?user_id={user_id}')
        otp_record.delete()

        request.session['verified_user_id'] = user.id
        return redirect('reset_password')

    return render(request, "auth/reset-password/VerifyOtp.html", {
        "user_id": user_id
    })
    
def resetPassword(request):
    user_id = request.session.get('verified_user_id')
    
    if not user_id:
        messages.error(request, "Unauthorized access. Please verify your OTP first.")
        return redirect('reset_password_email_send')

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return redirect('reset_password_email_send')

    if request.method == "POST":
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "auth/reset-password/ResetPasswordForm.html")

        try:
            validate_password(new_password, user)
            user.set_password(new_password)
            user.save()
            
            #====after succesful password save then destroy session====
            del request.session['verified_user_id']
            
            messages.success(request, "Password reset successfully. Please login.")
            return redirect('login')
        except ValidationError as e:
            for err in e.messages:
                messages.error(request, err)

    return render(request, "auth/reset-password/ResetPasswordForm.html")
    """
    
@login_required(login_url="login")
def profilePage(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    return render(request, "profiles/profile.html", {
        "profile": profile
    })


@login_required(login_url="login")
def editProfile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        user = request.user
        user.full_name = request.POST.get("full_name")
        user.save()

    #gender ko lagi 
        profile.gender = request.POST.get("gender")
        profile.date_of_birth = request.POST.get("date_of_birth")

    #pic accept garna ko lagi
        if "profile_pic" in request.FILES:
            profile.profile_pic = request.FILES["profile_pic"]
        profile.save()

    #Sucess message ko lagi
        messages.success(request, "Profile updated successfully")
        return redirect("profile")
    
    

    return render(request, "profiles/editprofile.html", {
        "profile": profile
    })