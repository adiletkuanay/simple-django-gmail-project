from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Message, Profile
from .forms import MessageForm
from .forms import RegistrationForm, LoginForm, EditProfileForm, EditUserForm

# Create your views here.
def main(request):
	return render(request, 'base.html')
#accounts
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'register.html', context)
def user_login(request):
	if request.method == 'POST':
		username =request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('')
		else:
			messages.info(request, 'Invalid Username or Password')
			return redirect('login')
	else:
		return render(request, 'login.html')
def logout_user(request):
	auth.logout(request)
	return redirect('') 
#message
def compose_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            sender = request.user
            recipient_username = form.cleaned_data['recipient']
            recipient = get_object_or_404(User, username=recipient_username)
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']

            message = Message(sender=sender, recipient=recipient, subject=subject, body=body)
            message.save()

            messages.success(request, 'Message sent successfully.')
            return redirect('inbox')  # Assuming you have an 'inbox' URL defined
    else:
        form = MessageForm()

    return render(request, 'compose.html', {'form': form})

@login_required
def inbox(request):
    received_messages = Message.objects.filter(recipient=request.user)
    return render(request, 'inbox.html', {'messages': received_messages})
@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, pk=message_id, recipient=request.user)
    if not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'message_detail.html', {'message': message})



@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

@login_required
def edit_profile(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = EditUserForm(instance=user)
        profile_form = EditProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})
from django.db.models import Q
from django.views.generic import ListView, View
def item_search(request):
    query = request.GET.get('search_query')
    if query:
        messages = Message.search(query)
    else:
        messages = Message.objects.none()
    context = {'messages': messages, 'query': query}
    return render(request, 'item_search.html', context)



from django.contrib.auth.decorators import user_passes_test
from .models import MessageRequest
@login_required
def create_message_request(request):
    if request.method == 'POST':
        recipient_username = request.POST.get('recipient')
        recipient = User.objects.get(username=recipient_username)  # Retrieve the recipient User instance
        subject = request.POST.get('subject')
        body = request.POST.get('body')

        message_request = MessageRequest.objects.create(
            sender=request.user,
            recipient=recipient,
            subject=subject,
            body=body
        )
        messages.success(request, 'Message request submitted successfully!')
        return redirect('message_request_list')
    return render(request, 'create_message_request.html')


@user_passes_test(lambda u: u.is_staff)
def approve_message_request(request, message_request_id):
    message_request = MessageRequest.objects.get(id=message_request_id)
    message_request.status = 'approved'
    message_request.save()
    message = Message.objects.create(
        sender=message_request.sender,
        recipient=message_request.recipient,
        subject=message_request.subject,
        body=message_request.body
    )
    message_request.message = message
    message_request.save()
    messages.success(request, 'Message request approved successfully!')
    return redirect('message_request_list')

@user_passes_test(lambda u: u.is_staff)
def reject_message_request(request, message_request_id):
    message_request = MessageRequest.objects.get(id=message_request_id)
    message_request.status = 'rejected'
    message_request.save()
    messages.success(request, 'Message request rejected successfully!')
    return redirect('message_request_list')

@login_required
def message_request_list(request):
    if request.user.is_staff:
        message_requests = MessageRequest.objects.all()
    else:
        message_requests = MessageRequest.objects.filter(sender=request.user)
    return render(request, 'message_request_list.html', {'message_requests': message_requests})


from django.contrib.auth.signals import user_logged_in
from django.shortcuts import get_object_or_404, render
def view_message(request, message_id):
    # Retrieve the message using the provided message_id
    message = get_object_or_404(Message, id=message_id)
    
    # Get the current last viewed messages from the session
    last_viewed = request.session.get('last_viewed_messages', [])
    
    # Add the current message_id to the last viewed list
    if message_id not in last_viewed:
        last_viewed.append(message_id)
    
    # Limit the last viewed list to 5 messages
    last_viewed = last_viewed[-5:]
    
    # Update the session data with the updated last viewed messages
    request.session['last_viewed_messages'] = last_viewed
    
    # Render the view_message template with the message
    return render(request, 'last_viewed_messages.html', {'message': message})

def last_viewed_messages(request):
    last_viewed = request.session.get('last_viewed_messages', [])[:5]  # Get last viewed messages from session, limiting to 5
    messages = []  # Create an empty list to hold the messages
    for message_id in last_viewed:
        message = get_object_or_404(Message, pk=message_id)  # Retrieve each message from the database
        messages.append(message)  # Add the message to the list
    return render(request, 'last_viewed_messages.html', {'messages': messages})

def reset_last_viewed_messages(sender, user, request, **kwargs):
    if 'last_viewed_messages' in request.session:
        del request.session['last_viewed_messages']

user_logged_in.connect(reset_last_viewed_messages)