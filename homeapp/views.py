from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ContactForm
from browserapp.forms import UserForm

from browserapp.models import Games # Import Games model from the browserapp

from django.contrib import messages

from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

# Create your views here.

# Returns the homepage at homeapp/home.html inside the templates folder at templates/homeapp

def home(request):
    # import models and dynamically generate the homepage
    context = {}

    # Dynamic Game Counter
    dynamicgamecount = Games.objects.all().count()
   # gamecounter = '1'

    if dynamicgamecount == 3 or dynamicgamecount >= 3:
        #gamecounter = 3
        context["dgcounter"] = 3
        #print("Reached 3")
        #print("It actually " + str(dynamicgamecount))
    elif dynamicgamecount == 2:
        #gamecounter = 2
        #context["gamecount"] = 2
        context["dgcounter"] = 2
        #print("Reached 2")
    else:
        #gamecounter = 1
        #context["gamecount"] = 1
        context["dgcounter"] = 1
        #print("Reached 1")
        #print("It actually " + str(dynamicgamecount))
        
        # DGcounter is used for adjusting bootstrap grids dynamically so cards dont overlap

    # Generate random 3 games as our top rated list, this is done because there is no rating functionality yet
    context["toprated_list"] = Games.objects.all().order_by('?')[:3]

    # Generate the three most recently added games
    context["recentgames_list"] = Games.objects.all().order_by('-addedTime')[:3]

    


    return render(request, 'homeapp/home.html', context)



def contact(request):
    if request.method == "GET":
        form = ContactForm() # Sets up new variable form as the base contact form found in form.py
        print("Sent GET LULZ")
    else:
        print("POST!")
        form = ContactForm(request.POST) # Sets up new variable using the data submitted by the user
        if form.is_valid():
            # form.cleaned_data: extracts the data from the form and puts into variables
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = name + ':\n' + form.cleaned_data['message'] # Combines name with message to fit within policy
            try:
                send_mail(subject, message, email, ['myemail@mydomain.com']) # Sends the email using the arguments
        
            except BadHeaderError:
                messages.add_message(request, messages.ERROR, 'Message Not Sent') # Error message to user 
                return HttpResponse("Invalid header found.") # Incase of bad header (Something wrong w/ request sent in)
            
            messages.add_message(request, messages.SUCCESS, 'Message Sent')
            return redirect(reverse('homeapp:home')) # Redirects us to the homepage if form was sent

        else:
            messages.add_message(request, messages.ERROR, 'Invalid Form Data; Message Not Sent')

    return render(request, 'homeapp/contact.html', {"form": form}) # Shows the form if request method was GET


class RegisterUser(CreateView):
    model = User
    form_class = UserForm
    template_name = 'homeapp/register.html'

    success_url = reverse_lazy('login')

