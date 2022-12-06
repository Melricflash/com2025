from django.db import models
from django.contrib.auth.models import User


# SuperUser: melric, superpassword

# Create your models here.

class Publishers(models.Model):

    def __str__(self):
        return self.publisherName # Used to see models by name

    publisherID = models.BigAutoField(auto_created = True, primary_key = True)
    publisherName = models.CharField(max_length = 128, unique = True)
    publisherDescription = models.TextField()
    addedTime = models.DateTimeField(auto_now_add = True)
    updatedTime = models.DateTimeField(auto_now = True)
    publisherImage = models.ImageField(upload_to = 'images/publishers') # uploads to media/images/publishers

    # On deletion of a publisher, the associated games should also be deleted. Use a foreign key to use on_delete, cascade

class Games(models.Model):

    def __str__(self):
        return self.title # Used to see models by name

    gameID = models.BigAutoField(auto_created = True, primary_key = True)
    title = models.CharField(max_length = 128, unique = True)
    description = models.TextField()
    cheatData = models.TextField(default = "")
    addedTime = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    coverImage = models.ImageField(upload_to = 'images/gamecovers') # upload to media/images/gamecovers

    # Removed cover banners for now as they are not used
    #coverBanner = models.ImageField(upload_to = 'images/gamebanners') # upload to media/images/gamebanners

    #addedToLibrary = models.BooleanField(default=False) # Obsolete field, not used anymore by functions

    gamePublisher = models.ForeignKey(Publishers, on_delete = models.CASCADE) # Foreign key to Publishers, links a publisher to a game

    # Note, a game must have a publisher associated with it

    class Meta:
        indexes = [models.Index(fields = ['title']), ]


# Many to Many model, used for MyGames (Library) functionality.

class UserGames(models.Model):

    def __str__(self):
        return str(self.user) + ": " + str(self.game) # Used to see models by name

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Games, on_delete=models.CASCADE)

