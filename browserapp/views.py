#from django.shortcuts import render
from django.shortcuts import (get_object_or_404, render, redirect)
from django.contrib import messages
from django.http import HttpResponse
from .models import Games, Publishers, UserGames
from .forms import GameForm, PublisherForm, UserForm

from django.views.generic import View
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from django.db.models import Q # Used for advanced querying

from django.core.exceptions import PermissionDenied


# Create your views here.

# Check if a user is an admin or superuser
def is_admin(user):
   # return user.groups.filter(name='GamesAdminUsers').exists()
   if (user.groups.filter(name='GamesAdminUsers').exists() or user.is_superuser):
    return True
 

def index_view(request):
    # dictionary for initial data with
    # field names as keys

    context ={}
    # add the dictionary during initialization
    context["game_list"] = Games.objects.all()
    return render(request, "browserapp/index.html", context)


def detail_view(request, gid):
    context ={}
    # add the dictionary during initialization
    currentGame = get_object_or_404(Games, pk = gid)

    if request.user.is_authenticated:
        currentUser = request.user # Fetches the current user's user ID
        context["gameInLibrary"] = UserGames.objects.filter(Q(user = currentUser) & Q(game = currentGame)).count()
    

    context["game"] = get_object_or_404(Games, pk=gid) # fetches the current game object
    context["publisher"] = Games.objects.select_related('gamePublisher') # Gets the related publisher

    # Checks if the game is already in the user's library. Should be a boolean variable but it is currently not
    

    return render(request, "browserapp/detail_view.html", context)
    

def create_view(request):

    if(not(is_admin(request.user))):
        raise PermissionDenied()

    context ={}
    # Fix form error messages when using request.files
    form = GameForm(request.POST or None)
    if(request.method == 'POST'):
        form = GameForm(request.POST, request.FILES or None) # We only request files if we press submit not before
        if form.is_valid(): # Checks if form is valid
            form.save() # adds to database
            messages.add_message(request, messages.SUCCESS, 'Game Created') # sends user a django message
            return redirect('browserapp:browse_index') # redirects to the index view

        else:
            messages.add_message(request, messages.ERROR, 'Invalid Form Data; Game not created') # Django error message
           # print(form.errors.as_data()) # Debug forms
            context['form'] = form
            return render(request, "browserapp/create_view.html", context) # Sends us back to the upload form
    else:
        print("Here!!!!!!!!!!")
        context['form']= form
        return render(request, "browserapp/create_view.html", context) # Generates the form if the link does not have POST data attached


def update_view(request, gid):

    if(not(is_admin(request.user))):
        raise PermissionDenied()

    context ={}
    # fetch the object related to passed id
    obj = get_object_or_404(Games, pk = gid) # gid is the primary key

    # pass the object as instance in form

    form = GameForm(request.POST or None, instance = obj)
    # save the data from the form and redirect to detail_view
    if form.is_valid():
        # Very important! to stop form validation errors before submit, use request.FILES after checking form is valid
        form = GameForm(request.POST, request.FILES or None, instance = obj)
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Game Updated') # Django success message

        return redirect('browserapp:browse_detail', gid=gid)
    
    else:
        #messages.add_message(request, messages.ERROR, 'Invalid Form Data; Game not created')
        print(form.errors.as_data())
        #context['form'] = form 

    # add form dictionary to context
    context["form"] = form

    return render(request, "browserapp/update_view.html", context) # Send us to the form


def delete_view(request, gid):

    if(not(is_admin(request.user))):
        raise PermissionDenied()

    # fetch the object related to passed id
    obj = get_object_or_404(Games, pk = gid)
    # delete object
    obj.delete()
    messages.add_message(request, messages.SUCCESS, 'Game Deleted')
    # after deleting redirect to index view
    return redirect('browserapp:browse_index')


# Publisher CRUD views

def pubIndex_view(request):
    context = {}
    context["publisher_list"] = Publishers.objects.all() # Gets all of the publisher objects in the database
    return render(request, "browserapp/pubIndex.html", context) # Sends us to the index view for publishers

def pubCreate_view(request):

    if(not(is_admin(request.user))):
        raise PermissionDenied()

    context ={}
    form = PublisherForm(request.POST or None)
    if(request.method == 'POST'):
        form = PublisherForm(request.POST, request.FILES or None) # Again only request files if the data is POST
        if form.is_valid(): # Checks if the form is valid
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Publisher Created')
            return redirect('browserapp:publisher_index')

        else:
            messages.add_message(request, messages.ERROR, 'Invalid Form Data; Publisher not created')
            context['form'] = form 
            return render(request, "browserapp/pubCreate.html", context) # Regenerate form
    else:
        context['form']= form
        return render(request, "browserapp/pubCreate.html", context) # Generate form


def pubDetail_view(request, pid):
    context ={}
    # add the dictionary during initialization

    context["publisher"] = get_object_or_404(Publishers, pk=pid) # Fetch the related publisher
    context["game_list"] = Games.objects.filter(gamePublisher = pid) # Get the games related to the publisher

    return render(request, "browserapp/pubDetail.html", context)


def pubEdit_view(request, pid):

    if(not(is_admin(request.user))):
        raise PermissionDenied()

    context ={}
    # fetch the object related to passed id
    obj = get_object_or_404(Publishers, pk = pid)

    # pass the object as instance in form

    form = PublisherForm(request.POST or None, instance = obj)
    # save the data from the form and
    # redirect to detail_view

    if form.is_valid():
        form = PublisherForm(request.POST, request.FILES or None, instance = obj) # again request files only if post otherwise form breaks
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Publisher Updated')

        return redirect('browserapp:publisher_detail', pid=pid)

    # add form dictionary to context
    
    context["form"] = form

    return render(request, "browserapp/pubUpdate.html", context)



def pubDelete_view(request, pid):

    if(not(is_admin(request.user))):
        raise PermissionDenied()

    # fetch the object related to passed id
    obj = get_object_or_404(Publishers, pk = pid)
    # delete object
    obj.delete()
    messages.add_message(request, messages.SUCCESS, 'Publisher Deleted')

    # after deleting redirect to index view
    return redirect('browserapp:publisher_index')


# Unused function for adding game to user's myGames page. Only use if AJAX button kills itself or whatever
# You can stay :)
class toggleGameView(View):
    def get(self, request):
        gid = request.GET.get('gameID')
        currentGame = get_object_or_404(Games, pk = gid)

        currentGame.addedToLibrary = not(currentGame.addedToLibrary)
        currentGame.save()

        return JsonResponse({'libraryUpdated': True, 'gid': gid, 'libraryStatus': currentGame.addedToLibrary}, status = 200)

@login_required # User must sign in before visiting the page
def myGamesIndex(request):
    context = {}

    currentUser = request.user
    
    # Gets all the games associated with the current user
    context["currentUser"] = currentUser
    context["game_list"] = Games.objects.filter(gameID__in=UserGames.objects.filter(user=currentUser).values_list('game'))

    return render(request, "browserapp/myGamesIndex.html", context)

@login_required
def addGametoLibrary(request): #, gid

    currentUser = request.user # Get the current User's UserID

    currentGameGET = request.GET.get('gameID') # Fetches the game id from the get request
    currentGame = get_object_or_404(Games, pk = currentGameGET) # Get the current game object

    # Check if the game already exists
    isGameinLibrary = UserGames.objects.filter(Q(user = currentUser) & Q(game = currentGame)).count()

    if (isGameinLibrary == 0): # Should be using a boolean value to check for true or false, but this works too
        newEntry = UserGames(user=currentUser, game=currentGame) # Creates a new entry to database
        newEntry.save() # Save to Database
    
    else:
        currentEntry = UserGames.objects.filter(Q(user = currentUser) & Q(game = currentGame)) # Finds the game object in table
        currentEntry.delete() # Delete from Database

    return JsonResponse({'libraryUpdated': True}, status = 200) # Sends a JSON response back to AJAX





    