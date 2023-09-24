from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import View
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator


def signup(request):
    if request.method=="POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]
        
        if pass1!=pass2:
            
            # return HttpResponse("Password doesn't match !")
            messages.warning(request,"Password doesn't match !")
            return render(request,'signup.html')
        try:
            if User.objects.get(username=email):
                 messages.info(request,"User Already Exist. Please register using another email")
                 return render(request,'signup.html')
                
        except Exception as identifier:
            pass
        user = User.objects.create_user(email,email,pass1,first_name=fname,last_name=lname)
        user.is_active=False
        user.save()
        
        email_subject = "GadgetBazar Registration Confirmation"
        email_message = render_to_string('activate.html',{
            'user': user,
            'domain' : 'gadgetbazar.onrender.com',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token' :  generate_token.make_token(user),
        })

        send_mail(
            email_subject,
            email_message,
            "GadgetBazar",
            [email],
        )
        
        messages.success(request,"An email has been sent to your email address containing an activation link.Please click on the link to activate your account.")

        return redirect('/auth/login')
    
    return render(request,'signup.html')


class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account Activated Successfully")
            return redirect('/auth/login')
        return render(request,'activatefail.html')

def login_user(request):

    if request.method=="POST":
        email = request.POST["email"]
        password = request.POST["pass"]
        myuser=authenticate(username=email,password=password)

        if myuser is not None:
            login(request,myuser)
            # messages.success(request,"Login Successful!")
            
            return redirect("home")
        else:
            messages.warning(request,"Invalid Credentials !")
            
            return redirect('/auth/login')

    return render(request,'login.html')


def logout_user(request):
    logout(request)
    messages.info(request,"User Logged Out Successfully !")
    return redirect('/auth/login')


class RequestResetEmailView(View):
    def get(self,request):
        return render(request,'request-reset-email.html')
    
    def post(self,request):
        email=request.POST['email']
        user=User.objects.filter(email=email)

        if user.exists():
            email_subject='Reset Your Password'
            message=render_to_string('reset-user-password.html',{
                'domain':'gadgetbazar.onrender.com',
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0])
            })

            send_mail(
                email_subject,
                message,
                "GadgetBazar",
                [email],
            )
            # email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            # email_message.send()

            messages.info(request,f"WE HAVE SENT YOU AN EMAIL WITH INSTRUCTIONS ON HOW TO RESET THE PASSWORD" )
            return render(request,'request-reset-email.html')
        else:
            messages.info(request,f"Email not Found !! Please give valid email " )
            return render(request,'request-reset-email.html')

class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)

            if  not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Password Reset Link is Invalid")
                return render(request,'request-reset-email.html')

        except DjangoUnicodeDecodeError as identifier:
            pass

        return render(request,'set-new-password.html',context)

    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'set-new-password.html',context)
        
        try:
            user_id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password Reset Success Please Login with NewPassword")
            return redirect('/auth/login/')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something Went Wrong")
            return render(request,'set-new-password.html',context)

        return render(request,'set-new-password.html',context)