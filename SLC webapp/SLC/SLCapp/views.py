from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from SLCapp.forms import UserForm, UserProfileForm, SignUpPictureForm, ChatBotResponseForm
from SLCapp.models import ChatBotResponse, ChatBotContext
import json
from watson_developer_cloud import ConversationV1
from parse_passport import parsePassport

import datetime


workspace_id = 'bb11e878-9e91-4e92-a27a-b871aa242360'

conversation = ConversationV1(
                        username='cb3e9502-08ae-49c3-8314-eeafa128333e',
                        password='ZPy4H2ylImMp',
                        version='2016-09-20')
def home(request):
    return render(request, 'SLCapp/home.html')

def signup_image(request):
    if request.method == 'POST':

        picture_form = SignUpPictureForm(data=request.POST)
      #  if picture_form.is_valid():
            
        
            #if 'picture' in request.FILES:
                # request.FILES['picture']
                # API IMAGE RECOGNITION
                # stuff happens
                # gets a string
                #
        result = 'P<GBRSCHNUR<<DANIEL<MARC<<<<<<<<<<<<<<<<<<<<' + '3046530706GBR7710104M1809223<<<<<<<<<<<<<<04'
        forename, surname, passportNo, DoB, gender, exp = parsePassport(result)
        print forename, surname, passportNo, DoB, gender, exp
        if exp < datetime.date:

            return render(request,
                    'SLCapp/signup.html',
                    {'user_form': UserForm(initial={'first_name':forename, 'last_name':surname}),
                    'profile_form': UserProfileForm(initial={'DoB':DoB, 'PassportNo':int(passportNo)}),
                    'registered': False})
        else:
            return render(request, 'SLCapp/signupimage.html',
                          {'picture_form':SignUpPictureForm(), 'errors':'Passport read is expired, if this is not the case please sign up manually'})

      #  else:
         #   print(picture_form.errors)

    else:
        picture_form = SignUpPictureForm()
    
        return render(request, 'SLCapp/signupimage.html',
                      {'picture_form':picture_form})


def signup(request):
        # A boolean value for telling the template
        # whether the registration was successful.
        # Set to False initially. Code changes value to
        # True when registration succeeds.
        registered = False
        print request.method
        print request.GET
        
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
    context_dict = {}

    if request.method == 'POST':
        form = ChatBotResponseForm(request.POST)
        if form.is_valid():
            chatBotResponse = form.save(commit=False)
            chat = ''
            result = ''
            chat = request.POST.get('request')

            previous_message = ChatBotContext.objects.filter(user=request.user)
            if previous_message:
                previous_message = previous_message[0]
                conversation_id = previous_message.conversation_id
                dialog_node = previous_message.dialog_node
                dialog_turn_counter = previous_message.dialog_turn_counter
                dialog_request_counter = previous_message.dialog_request_counter
                
                context = {"conversation_id":conversation_id, "system": {"dialog_stack":[{"dialog_node":dialog_node}],  \
                                                                         "dialog_turn_counter": dialog_turn_counter,  \
                                                                         "dialog_request_counter": dialog_request_counter},
                } 
                                                                         
                print context

                previous_message.delete()
                response = conversation.message(workspace_id=workspace_id, message_input={
                            'text': chat}, context=context)
                
            else:
                response = conversation.message(workspace_id=workspace_id, message_input={
                    'text': chat}, context={})
            
            result = str(json.loads(json.dumps(response))['output']['text'][0])
            context = json.loads(json.dumps(response))['context']

            conversation_id = str(context['conversation_id'])
            dialog_node = str(context['system']['dialog_stack'][0]['dialog_node'])
            dialog_turn_counter = int(context['system']['dialog_turn_counter'])
            dialog_request_counter = int(context['system']['dialog_request_counter'])
                
            ChatBotContext.objects.create(user=request.user, conversation_id=conversation_id, dialog_node=dialog_node, dialog_turn_counter=dialog_turn_counter, dialog_request_counter=dialog_request_counter)# defaultCounter=defaultCounter)

            chatBotResponse.user = request.user
            chatBotResponse.request = chat
            chatBotResponse.response = result
            chatBotResponse.save()
        else:
            print(form.errors)
        
    else:
        existing_context = ChatBotContext.objects.filter(user=request.user)
        if existing_context:
            existing_context.delete()
        
        current_messages = ChatBotResponse.objects.filter(user=request.user)
        if current_messages:
            current_messages.delete()
        context_dict['convo'] = []
        
    
    
    convo = ChatBotResponse.objects.filter(user=request.user)
    context_dict['convo'] = convo
    context_dict['chat_form'] = ChatBotResponseForm()
    
    return render(request, 'SLCapp/chat.html', context_dict)


