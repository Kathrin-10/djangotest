from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.models import User
from .models import Friend, Message,User  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(mail_subject, message, 'admin@example.com', [email])
            return render(request, 'forgot_password.html', {'message': 'Password reset link has been sent to your email'})
        except User.DoesNotExist:
            return render(request, 'forgot_password.html', {'message': 'Email not registered'})
    return render(request, 'forgot_password.html')




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            name = form.cleaned_data.get('name')
            gender = form.cleaned_data.get('gender')
            dob = form.cleaned_data.get('dob')
            email = form.cleaned_data.get('email')
            Friend.objects.create(user=user, name=name, gender=gender, dob=dob, email=email)
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f'{field.label}: {error}')
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index') 
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

def index(request):
    friends = Friend.objects.all()
    return render(request, 'index.html', {'friends': friends})




@login_required
def chat(request, friend_id):
    friend = get_object_or_404(Friend, id=friend_id)
    friend_user = friend.user  # Get the User associated with the Friend

    if request.method == 'POST':
        message_text = request.POST.get('message')
        if message_text:
            Message.objects.create(sender=request.user, friend=friend, text=message_text)

    messages = Message.objects.filter(
        (Q(sender=request.user) & Q(friend=friend)) |
        (Q(sender=friend_user) & Q(friend__user=request.user))
    ).order_by('timestamp')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        messages_data = [{'id': msg.id, 'text': msg.text, 'sender': msg.sender.id if msg.sender else None} for msg in messages]
        return JsonResponse({'friend': {'name': friend.name}, 'messages': messages_data})

    return render(request, 'chat.html', {'friend': friend, 'messages': messages})

@login_required
def delete_message(request, message_id):
    if request.method == 'POST':
        message = get_object_or_404(Message, id=message_id)
        if message.sender == request.user or message.friend.user == request.user:
            message.delete()
            return JsonResponse({'status': 'success', 'message': 'Message deleted successfully.'})
        return JsonResponse({'status': 'error', 'message': 'You are not authorized to delete this message.'})
