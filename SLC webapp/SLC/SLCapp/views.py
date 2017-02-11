from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from SLCapp.forms import UserForm, UserProfileForm, SignUpPictureForm


def home(request):
    return render(request, 'SLCapp/home.html')

def signup_image(request):
    if request.method == 'POST':

        sign_up_picture_form = SignUpPictureForm(data=request.POST)
        if sign_up_picture_form.is_valid():
            
        
            if 'picture' in request.FILES:
                None
                #API IMAGE RECOGNITION


            #auto fill form

        else:
            print(sign_up_picture_form.errors)

    else:
        sign_up_picture_form = SignUpPictureForm()
    
    return render(request, 'SLCapp/signupimage.html',
                  {'sign_up_picture_form':sign_up_picture_form)


def signup(request):
        # A boolean value for telling the template
        # whether the registration was successful.
        # Set to False initially. Code changes value to
        # True when registration succeeds.
        registered = False
        
        # If it's a HTTP POST, we're interested in processing form data.
        if request.method == 'POST':
                # Attempt to grab information from the raw form information.
                # Note that we make use of both UserForm and UserProfileForm.
                user_form = UserForm(data=request.POST)
                profile_form = UserProfileForm(data=request.POST)
                #profile_form = UserProfileForm(data=request.POST)
                
                # If the two forms are valid...
                if user_form.is_valid() and profile_form.is_valid():
                        # Save the user's form data to the database.
                        user = user_form.save()
                        
                        # Now we hash the password with the set_password method.
                        # Once hashed, we can update the user object.
                        user.set_password(user.password)
                        user.save()

                        profile = profile_form.save(commit=False)
                        profile.user = user

                        profile.save()
                        
                        registered = True
                else:
                        # Invalid form or forms - mistakes or something else?
                        # Print problems to the terminal.
                        print(user_form.errors, profile_form.errors)
        else:
                # Not a HTTP POST, so we render our form using two ModelForm instances.
                # These forms will be blank, ready for user input.
                user_form = UserForm()
                profile_form = UserProfileForm()
                
        # Render the template depending on the context.
        return render(request,
                        'SLCapp/signup.html',
                        {'user_form': user_form,
                        'profile_form': profile_form,
                        'registered': registered,
                        'autofilled':False})

def user_login(request):
        # If the request is a HTTP POST, try to pull out the relevant information.
        if request.method == 'POST':
                # Gather the username and password provided by the user.
                # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed
                # to request.POST['<variable>'], because the
                # request.POST.get('<variable>') returns None if the
                # value does not exist, while request.POST['<variable>']
                # will raise a KeyError exception.
                username = request.POST.get('username')
                password = request.POST.get('password')
                
                # Use Django's machinery to attempt to see if the username/password
                # combination is valid - a User object is returned if it is.
                user = authenticate(username=username, password=password)

                # If we have a User object, the details are correct.
                # If None (Python's way of representing the absence of a value), no user
                # with matching credentials was found.
                if user:
                        # Is the account active? It could have been disabled.
                        if user.is_active:
                                # If the account is valid and active, we can log the user in.
                                # We'll send the user back to the homepage.
                                login(request, user)
                                return HttpResponseRedirect(reverse('home'))
                        else:
                                # An inactive account was used - no logging in!
                                return render(request, 'SLCapp/login.html', {'errors':['Your SLC account is disabled',]})
                else:
                        # Bad login details were provided. So we can't log the user in.
                        print("Invalid login details: {0}, {1}".format(username, password))
                        return render(request, 'SLCapp/login.html', {'errors':['Invalid login details',]})

        # The request is not a HTTP POST, so display the login form.
        # This scenario would most likely be a HTTP GET.
        else:
                # No context variables to pass to the template system, hence the
                # blank dictionary object...
                return render(request, 'SLCapp/login.html', {})


    
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def chat(request):
    return render(request, 'SLCapp/chat.html')
