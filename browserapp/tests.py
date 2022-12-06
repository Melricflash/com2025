from django.test import TestCase
from django.db.backends.sqlite3.base import IntegrityError
from django.db import transaction

from .models import Games, Publishers, UserGames, User
from django.urls import reverse

from django.core.files.uploadedfile import SimpleUploadedFile

from django.core.exceptions import ValidationError

from .forms import GameForm, PublisherForm

from django.test.utils import override_settings

from django.contrib.auth.models import Group

# Create your tests here.

# Tests have to start with test_ !!


# Every view has been tested fairly thoroughly, publisher and game create views are found in PublisherTests and GameTests

# When running these tests, junk testing files are left in the media folder as it tests file uploading, does not affect tests but
# due to the quantity of tests, will leave a 'large' amount

# Can use override settings to potentially delete the files after tests have run but have not implemented yet



class PublisherTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        publisher1Image = SimpleUploadedFile(name='publisher1Image.jpg', content=b'', content_type='image/jpeg')
        publisher1 = Publishers(publisherName = "Publisher 1", publisherDescription = "Publisher 1 Description", publisherImage = publisher1Image)
        publisher1.save()

        # Adding a user to the database
        user1 = User(username='user1', email='user1@email.com')
        user1.set_password('MyPassword123')
        user1.save()

        # Create GamesAdminUsers group
        group_name = "GamesAdminUsers"
        cls.group = Group(name=group_name)
        cls.group.save()

        # Adding an admin to the database
        user2 = User(username = 'user2', email = 'user2@email.com')
        user2.set_password('MyPassword123')
        user2.full_clean
        user2.save()
        group = Group.objects.get(name = 'GamesAdminUsers')
        user2.groups.add(group)


    # Checking if a publisher saves to the database correctly
    def test_savePublisherToDatabase(self):
        db_count = Publishers.objects.all().count()
       # print("Current Publishers in database test_saveGameToDatabase: " + str(db_count))
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'', content_type='image/jpeg')
        testpublisher = Publishers(publisherName = "Publisher 2", publisherDescription = "Publisher 2 Description", publisherImage = TestPublisherImage)
        
        testpublisher.full_clean
        testpublisher.save()

        self.assertEqual(db_count+1, Publishers.objects.all().count())

    # Checking if a publisher is saved with a duplicate name
    def test_duplicatename(self):

        # TestGameImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'', content_type='image/jpeg')
        # testpublisher = Publishers(publisherName = "Publisher 20", publisherDescription = "Publisher 2 Description", publisherImage = TestGameImage)
        # testpublisher.save()

        db_count = Publishers.objects.all().count()
        #print("Current Publishers in database: " + str(db_count))
        TestPublisherImage2 = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'', content_type='image/jpeg')
        testpublisher2 = Publishers(publisherName = "Publisher 1", publisherDescription = "Publisher 2 Description", publisherImage = TestPublisherImage2)

        #with self.assertRaises(IntegrityError):

        try:
            with transaction.atomic():
                testpublisher2.save()
        except IntegrityError:
            pass
        self.assertNotEqual(db_count+1, Publishers.objects.all().count())

    # Testing to see if a publisher can be created with missing information
    def test_missingdata(self):
        testpublisher = Publishers(publisherName = "Publisher 21")

        # Calling full clean on an invalid data object will raise a validation error
        self.assertRaises(ValidationError, testpublisher.full_clean)

    # Testing to see if a publisher is created using valid POST data
    def test_publisherPOSTcreate(self):
        login = self.client.login(username='user2', password='MyPassword123')
        # Get the publisher count before
        db_count = Publishers.objects.all().count()
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')

        # Data to be sent through POST
        data = {
            'publisherName': "Test Publisher 22",
            'publisherDescription': "Publisher Description",
            'publisherImage': TestPublisherImage
            
        }

        # Posting the data to the view
        response = self.client.post(reverse('browserapp:publisher_upload'), data = data, follow=True)
        # Checking if the publisher was successfully added
        self.assertContains(response, "Publishers")
        self.assertEqual(Publishers.objects.count(), db_count+1)
        # Checking to see if the POST request was valid and redirected OK
        # Response would be 302 without redirect
        self.assertEqual(response.status_code, 200)

    # Testing to see if a publisher is not created using invalid POST data
    def test_publisherInvalidPOSTcreate(self):
        login = self.client.login(username='user2', password='MyPassword123')
        db_count = Publishers.objects.all().count()
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')

        data = {
            'publisherName': "Test Publisher 22",
            # Missing publisherDescription data
            'publisherImage': TestPublisherImage
            
        }

        # Send POST to view
        response = self.client.post(reverse('browserapp:publisher_upload'), data = data, follow=True)
        # Check that the HTTP response given back was 200 (POST Invalid)
        self.assertEqual(response.status_code, 200)
        # Check no redirect
        self.assertNotContains(response, "Publishers")
        # Checking that the publisher was not added to database
        self.assertNotEqual(Publishers.objects.count(), db_count+1)


    def test_publisherInvalidUserCreate(self):
        login = self.client.login(username='user1', password='MyPassword123')
        db_count = Publishers.objects.all().count()
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')

        data = {
            'publisherName': "Test Publisher 22",
            # Missing publisherDescription data
            'publisherImage': TestPublisherImage
            
        }

        # Send POST to view
        response = self.client.post(reverse('browserapp:publisher_upload'), data = data)
        # Check that the HTTP response given back was 200 (POST Invalid)
        self.assertEqual(response.status_code, 403)
        # Checking that the publisher was not added to database
        self.assertNotEqual(Publishers.objects.count(), db_count+1)

    # Testing creating a publisher using a form with valid data
    def test_publisherformvalid(self):
        login = self.client.login(username='user2', password='MyPassword123')
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')

        data = {
            'publisherName': 'Test Publisher 4',
            'publisherDescription': 'Test Description 4'
        }

        files_data = {
            'publisherImage': TestPublisherImage
        }

        form = PublisherForm(data = data, files = files_data)
        #print(form)

        self.assertTrue(form.is_valid())

    # Test using form to create publisher with duplicate name
    def test_publisherformDuplicateName(self):
        login = self.client.login(username='user2', password='MyPassword123')
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')

        data = {
            'publisherName': 'Publisher 1',
            'publisherDescription': 'Test Description 4'
        }

        files_data = {
            'publisherImage': TestPublisherImage
        }

        form = PublisherForm(data = data, files = files_data)
        #print(form)

        self.assertFalse(form.is_valid())

    
    def test_publisherforminvalid(self):
        login = self.client.login(username='user2', password='MyPassword123')
        # The publisher image is not correct, missing gif header
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'', content_type='image/gif')

        data = {
            'publisherName': 'Test Publisher 4',
            'publisherDescription': 'Test Description 4'
        }

        files_data = {
            'publisherImage': TestPublisherImage
        }

        form = PublisherForm(data = data, files = files_data)
        #print(form)

        self.assertFalse(form.is_valid())

    


class GameTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Add a publisher to database to allow us to create games
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher1 = Publishers(publisherName = "Publisher 1", publisherDescription = "Publisher 1 Description", publisherImage = TestPublisherImage)
        publisher1.full_clean
        publisher1.save()

        # Adding a user to the database
        user1 = User(username='user1', email='user1@email.com')
        user1.set_password('MyPassword123')
        user1.save()

        # Create GamesAdminUsers group
        group_name = "GamesAdminUsers"
        cls.group = Group(name=group_name)
        cls.group.save()

        # Adding an admin to the database
        user2 = User(username = 'user2', email = 'user2@email.com')
        user2.set_password('MyPassword123')
        user2.full_clean
        user2.save()
        group = Group.objects.get(name = 'GamesAdminUsers')
        user2.groups.add(group)

    def test_saveGametoDatabase(self):
        TestGameImage = SimpleUploadedFile(name='TestGameImage.gif', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher = Publishers.objects.get(publisherID = 1)
        dbcount = Games.objects.all().count()

        game = Games(title = "Game 1", description = "Game description", cheatData = "N/A", coverImage = TestGameImage, gamePublisher = publisher)

        game.full_clean
        game.save()

        self.assertEqual(dbcount+1, Games.objects.all().count())

    def test_duplicateGameName(self):
        TestGameImage = SimpleUploadedFile(name='TestGameImage.gif', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher = Publishers.objects.get(publisherID = 1)

        # Setup an existing game in the database
        game = Games(title = "Game 1", description = "Game 1 description", cheatData = "IHATETESTING: Unlock All", coverImage = TestGameImage, gamePublisher = publisher)
        game.full_clean
        game.save()

        # Retrieve the number of games in the index
        dbcount = Games.objects.all().count()

        # Try adding a game with a duplicate title
        game2 = Games(title = "Game 1", description = "Game 2 description", cheatData = "SERIOUSLYTHISWASAHEADACHE: Unlock All", coverImage = TestGameImage, gamePublisher = publisher)

        try:
            with transaction.atomic():
                game2.save() # Attempt to save the game to database
        except IntegrityError: # If there is an integrity error, skip this
            pass
        # Check that the total game count has not increased
        self.assertNotEqual(dbcount+1, Games.objects.all().count())

    def test_missingdata(self):
        game = Games(title = "Game 1", description = "Game 1 description")

        self.assertRaises(ValidationError, game.full_clean)


    def testGameCreationPOST(self):
        login = self.client.login(username='user2', password='MyPassword123')
        dbcount = Games.objects.all().count()
        TestGameImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')

        # Get the correct publisher to link our game to, MUST USE .pk for specifying the foreign key publisher
        publisher = Publishers.objects.get(publisherID = 1).pk
        
        # Data to POST
        data = {
            'title': 'Game 1',
            'description': 'Game 1 Description',
            'cheatData': 'N/A',
            'coverImage': TestGameImage,
            'gamePublisher': publisher
        }

        # POST data to our view
        response = self.client.post(reverse('browserapp:browse_upload'), data = data, follow=True)
        # Checking for a 200 found response, meaning successful 302 and 200 redirect
        self.assertEqual(response.status_code, 200)
        # Making sure we get redirected
        self.assertContains(response, "Games")
        # Check that the game was added to the database
        self.assertEqual(Games.objects.count(), dbcount+1)
        #print(response)

    def testInvalidGameCreationPOST(self):
        login = self.client.login(username='user2', password='MyPassword123')
        dbcount = Games.objects.all().count()
        TestGameImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')

        # Get the correct publisher to link our game to, MUST USE .pk for specifying the foreign key publisher
        publisher = Publishers.objects.get(publisherID = 1).pk
        
        # Data to POST
        data = {
            # Missing Title
            'description': 'Game 1 Description',
            'cheatData': 'N/A',
            'coverImage': TestGameImage,
            'gamePublisher': publisher
        }

        # POST data to our view
        response = self.client.post(reverse('browserapp:browse_upload'), data = data, follow=True)
        # Checking for a 302 found response / Checking 200 redirect
        self.assertNotEqual(response.status_code, 200)
        self.assertNotContains(response, "Games")
        # Check that the game was added to the database
        self.assertNotEqual(Games.objects.count(), dbcount+1)
        #print(response)

    def testInvalidGameCreationPOST(self):
        login = self.client.login(username='user1', password='MyPassword123')
        dbcount = Games.objects.all().count()
        TestGameImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')

        # Get the correct publisher to link our game to, MUST USE .pk for specifying the foreign key publisher
        publisher = Publishers.objects.get(publisherID = 1).pk
        
        # Data to POST
        data = {
            # Missing Title
            'description': 'Game 1 Description',
            'cheatData': 'N/A',
            'coverImage': TestGameImage,
            'gamePublisher': publisher
        }

        # POST data to our view
        response = self.client.post(reverse('browserapp:browse_upload'), data = data)
        # Checking for a 403 forbidden response
        self.assertEqual(response.status_code, 403)
        # Check that the game was added to the database
        self.assertNotEqual(Games.objects.count(), dbcount+1)
        #print(response)

    

    def test_GameFormValid(self):
        login = self.client.login(username='user2', password='MyPassword123')
        TestGameImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher = Publishers.objects.get(publisherID = 1)

        data = {
            'title': 'Test Publisher 4',
            'description': 'Test Description 4',
            'cheatData': 'N/A',
            'coverImage': TestGameImage,
            'gamePublisher': publisher
        }

        files_data = {
            'coverImage': TestGameImage
        }

        form = GameForm(data = data, files = files_data)
        #print(form)

        self.assertTrue(form.is_valid())

    def test_GameFormInvalid(self):
        login = self.client.login(username='user2', password='MyPassword123')
        TestGameImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher = Publishers.objects.get(publisherID = 1)

        # Data to create form with
        data = {
            'title': 'Test Publisher 4',
            # Missing Description
            'cheatData': 'N/A',
            'coverImage': TestGameImage,
            # Missing Publisher
        }

        files_data = {
            'coverImage': TestGameImage
        }

        form = GameForm(data = data, files = files_data)
        #print(form)

        # Check that the form is not valid
        self.assertFalse(form.is_valid())

    # Testing creating a game using the form with a duplicate name
    def test_GameFormDuplicateName(self):
        login = self.client.login(username='user2', password='MyPassword123')
        TestGameImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher = Publishers.objects.get(publisherID = 1)

        # Adding a game to the database
        game = Games(title = "Game 1", description = "Game 1 description", cheatData = "IHATETESTING: Unlock All", coverImage = TestGameImage, gamePublisher = publisher)
        game.full_clean
        game.save()

        
        data = {
            'title': 'Game 1', # Duplicate game name
            'description': 'Test Description 4',
            'cheatData': 'N/A',
            'coverImage': TestGameImage,
            'gamePublisher': publisher
        }

        files_data = {
            'coverImage': TestGameImage
        }

        form = GameForm(data = data, files = files_data)
        #print(form)

        self.assertFalse(form.is_valid())


    def test_GameModelDeleteCascade(self):
        login = self.client.login(username='user2', password='MyPassword123')
        TestGameImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher = Publishers.objects.get(publisherID = 1)

        # Adding a game to the database
        game = Games(title = "Game 1", description = "Game 1 description", cheatData = "IHATETESTING: Unlock All", coverImage = TestGameImage, gamePublisher = publisher)
        game.full_clean
        game.save()

        dbcount = Games.objects.all().count()

        publisher.delete()

        self.assertEqual(dbcount-1, Games.objects.all().count())


class UserGamesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
    # Add a publisher to database to allow us to create games
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher1 = Publishers(publisherName = "Publisher 1", publisherDescription = "Publisher 1 Description", publisherImage = TestPublisherImage)
        publisher1.full_clean
        publisher1.save()

    # Adding a user to the database
        user1 = User(username='user1', email='user1@email.com')
        user1.set_password('MyPassword123')
        user1.save()

    # Adding a game to the database
        TestGameImage = SimpleUploadedFile(name='TestGameImage.gif', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher = Publishers.objects.get(publisherID = 1)
        game = Games(title = "Game 1", description = "Game 1 description", cheatData = "IHATETESTING: Unlock All", coverImage = TestGameImage, gamePublisher = publisher)
        game.full_clean
        game.save()

    # Testing adding a game to the database
    def test_addUserGame(self):
        # Get number of objects in UserGames
        dbcount = UserGames.objects.all().count()

        # Logging in
        login = self.client.login(username='user1', password='MyPassword123')

        # Get the current game and current user, we dont use .pk at the end as we dont use choices
        currentUser = User.objects.get(pk=1)
        currentGame = Games.objects.get(gameID = 1)

        newentry = UserGames(user = currentUser, game = currentGame)

        # Add to database
        newentry.full_clean
        newentry.save()

        # Check if this was successful
        self.assertEqual(dbcount+1, UserGames.objects.all().count())


    def test_UserDeleteCascade(self):
        # Creating a new entry to UserGames
        currentUser = User.objects.get(pk=1)
        currentGame = Games.objects.get(gameID = 1)
        newentry = UserGames(user = currentUser, game = currentGame)
        newentry.full_clean
        newentry.save()

        dbcount = UserGames.objects.all().count()
        
        # Attempt to delete the current user
        currentUser.delete()

        # Check that the whole entry was deleted
        self.assertEqual(dbcount-1, UserGames.objects.all().count())

    def test_GameDeleteCascade(self):
        # Creating a new entry to UserGames
        currentUser = User.objects.get(pk=1)
        currentGame = Games.objects.get(gameID = 1)
        newentry = UserGames(user = currentUser, game = currentGame)
        newentry.full_clean
        newentry.save()

        dbcount = UserGames.objects.all().count()
        
        # Attempt to delete the current game from its model
        currentGame.delete()

        # Check that the whole entry was deleted
        self.assertEqual(dbcount-1, UserGames.objects.all().count())

    
    def test_PublisherDeleteCascade(self):
        # Creating a new entry to UserGames
        currentUser = User.objects.get(pk=1)
        currentGame = Games.objects.get(gameID = 1)
        newentry = UserGames(user = currentUser, game = currentGame)
        newentry.full_clean
        newentry.save()

        dbcount = UserGames.objects.all().count()
        
        currentPublisher = Publishers.objects.get(publisherID = 1)
        
        # Attempt to delete the current user
        currentPublisher.delete()

        # Check that the whole entry was deleted
        self.assertEqual(dbcount-1, UserGames.objects.all().count())

class GameDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Adding a publisher
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher1 = Publishers(publisherName = "Publisher 1", publisherDescription = "Publisher 1 Description", publisherImage = TestPublisherImage)
        publisher1.full_clean
        publisher1.save()

        # Adding a game to the database
        TestGameImage = SimpleUploadedFile(name='TestGameImage.gif', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher = Publishers.objects.get(publisherID = 1)
        game = Games(title = "Game 1", description = "Game 1 description", cheatData = "IHATETESTING: Unlock All", coverImage = TestGameImage, gamePublisher = publisher)
        game.full_clean
        game.save()

        # Adding a user to the database
        user1 = User(username='user1', email='user1@email.com')
        user1.set_password('MyPassword123')
        user1.save()

        # Create GamesAdminUsers group
        group_name = "GamesAdminUsers"
        cls.group = Group(name=group_name)
        cls.group.save()

        # Adding an admin to the database
        user2 = User(username = 'user2', email = 'user2@email.com')
        user2.set_password('MyPassword123')
        user2.full_clean
        user2.save()
        group = Group.objects.get(name = 'GamesAdminUsers')
        user2.groups.add(group)


    def test_nologinDetailView(self):
        game = Games.objects.get(gameID = 1)

        url = reverse('browserapp:browse_detail', kwargs={'gid': game.gameID})
        # Fetch the detail view
        response = self.client.get(url)

        # Check that the url was found
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'browserapp/detail_view.html')

        self.assertContains(response, "Game 1")
        self.assertContains(response, "Game 1 description")
        self.assertContains(response, 'IHATETESTING: Unlock All')
        #self.assertContains(response, 'By <a class = "card-link" href = "/browse/publishers/1"><strong>Publisher 1</strong> </a>')
        
        self.assertContains(response, 'Publisher 1')

        self.assertNotContains(response, 'Edit')
        self.assertNotContains(response, 'Delete')
        self.assertNotContains(response, 'Add to MyGames')
        #print(response.content)

    def test_loginDetailView(self):
        game = Games.objects.get(gameID = 1)

        login = self.client.login(username='user1', password='MyPassword123')

        url = reverse('browserapp:browse_detail', kwargs={'gid': game.gameID})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'browserapp/detail_view.html')

        self.assertContains(response, "Game 1")
        self.assertContains(response, "Game 1 description")
        #self.assertContains(response, 'By <a class = "card-link" href = "/browse/publishers/1"><strong>Publisher 1</strong> </a>')
        
        self.assertContains(response, 'Publisher 1')
        self.assertContains(response, 'IHATETESTING: Unlock All')

        self.assertNotContains(response, 'Edit')
        self.assertNotContains(response, 'Delete')
        self.assertContains(response, 'Add to MyGames')
        #print(response.content)

    def test_AdminloginDetailView(self):
        game = Games.objects.get(gameID = 1)

        login = self.client.login(username='user2', password='MyPassword123')

        url = reverse('browserapp:browse_detail', kwargs={'gid': game.gameID})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'browserapp/detail_view.html')

        self.assertContains(response, "Game 1")
        self.assertContains(response, "Game 1 description")
        self.assertContains(response, 'IHATETESTING: Unlock All')
        #self.assertContains(response, 'By <a class = "card-link" href = "/browse/publishers/1"><strong>Publisher 1</strong> </a>')
        
        self.assertContains(response, 'Publisher 1')

        self.assertContains(response, 'Edit')
        self.assertContains(response, 'Delete')
        self.assertContains(response, 'Add to MyGames')
        #print(response.content)

class GameUpdateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Adding a publisher
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher1 = Publishers(publisherName = "Publisher 1", publisherDescription = "Publisher 1 Description", publisherImage = TestPublisherImage)
        publisher1.full_clean
        publisher1.save()

        # Adding a game to the database
        TestGameImage = SimpleUploadedFile(name='TestGameImage.gif', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher = Publishers.objects.get(publisherID = 1)
        game = Games(title = "Game 1", description = "Game 1 description", cheatData = "IHATETESTING: Unlock All", coverImage = TestGameImage, gamePublisher = publisher)
        game.full_clean
        game.save()

        # Adding a game to the database
        TestGameImage = SimpleUploadedFile(name='TestGameImage.gif', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher = Publishers.objects.get(publisherID = 1)
        game = Games(title = "Game 2", description = "Game 1 description", cheatData = "IHATETESTING: Unlock All", coverImage = TestGameImage, gamePublisher = publisher)
        game.full_clean
        game.save()

        # Adding a user to the database
        user1 = User(username='user1', email='user1@email.com')
        user1.set_password('MyPassword123')
        user1.save()

        # Create GamesAdminUsers group
        group_name = "GamesAdminUsers"
        cls.group = Group(name=group_name)
        cls.group.save()

        # Adding an admin to the database
        user2 = User(username = 'user2', email = 'user2@email.com')
        user2.set_password('MyPassword123')
        user2.full_clean
        user2.save()
        group = Group.objects.get(name = 'GamesAdminUsers')
        user2.groups.add(group)
    
    def test_validUpdateForm(self):
        login = self.client.login(username='user2', password='MyPassword123')
        # Fetch the current game and publisher
        currentGame = Games.objects.get(gameID = 1)
        currentPublisher = Publishers.objects.get(publisherID = 1).pk

        url = reverse('browserapp:browse_edit', kwargs={'gid': currentGame.gameID})

        #data to edit view
        data = {
            'title': 'Game 1',
            'description': 'Game 1 description',
            'cheatData': 'N/A', # Changed cheatData
            'coverImage': currentGame.coverImage,
            'gamePublisher': currentPublisher
        }

        # Post to edit view
        response = self.client.post(url, data = data, follow=True)
        
        # Check that the view is valid
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, currentGame.title)
        # Refresh the object
        currentGame.refresh_from_db()
        # Check the game's cheat data was updated
        self.assertEqual(currentGame.cheatData, "N/A")

    def test_invalidUserUpdateForm(self):
        login = self.client.login(username='user1', password='MyPassword123')
        # Fetch the current game and publisher
        currentGame = Games.objects.get(gameID = 1)
        currentPublisher = Publishers.objects.get(publisherID = 1).pk

        url = reverse('browserapp:browse_edit', kwargs={'gid': currentGame.gameID})

        #data to edit view
        data = {
            'title': 'Game 1',
            'description': 'Game 1 description',
            'cheatData': 'N/A', # Changed cheatData
            'coverImage': currentGame.coverImage,
            'gamePublisher': currentPublisher
        }

        # Post to edit view
        response = self.client.post(url, data = data)
        
        # Check that the view is invalid
        self.assertEqual(response.status_code, 403)
        # Refresh the object
        currentGame.refresh_from_db()
        # Check the game's cheat data was updated
        self.assertNotEqual(currentGame.cheatData, "N/A")

    def test_invalidUpdateForm(self):
        login = self.client.login(username='user2', password='MyPassword123')
        currentGame = Games.objects.get(gameID = 1)
        currentPublisher = Publishers.objects.get(publisherID = 1).pk

        url = reverse('browserapp:browse_edit', kwargs={'gid': currentGame.gameID})

        data = {
            'title': 'Game 2', # Game title no longer unique
            'description': 'Game 1 description',
            'cheatData': 'N/A', # Changed cheatData
            'coverImage': currentGame.coverImage,
            'gamePublisher': currentPublisher
        }

        response = self.client.post(url, data = data)

        # Check that the view raises an error for invalid game name
        self.assertEqual(response.status_code, 200)

class PublisherUpdateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Adding a publisher
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher1 = Publishers(publisherName = "Publisher 1", publisherDescription = "Publisher 1 Description", publisherImage = TestPublisherImage)
        publisher1.full_clean
        publisher1.save()

        # Adding a second publisher
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher1 = Publishers(publisherName = "Publisher 2", publisherDescription = "Publisher 1 Description", publisherImage = TestPublisherImage)
        publisher1.full_clean
        publisher1.save()

        # Adding a user to the database
        user1 = User(username='user1', email='user1@email.com')
        user1.set_password('MyPassword123')
        user1.save()

        # Create GamesAdminUsers group
        group_name = "GamesAdminUsers"
        cls.group = Group(name=group_name)
        cls.group.save()

        # Adding an admin to the database
        user2 = User(username = 'user2', email = 'user2@email.com')
        user2.set_password('MyPassword123')
        user2.full_clean
        user2.save()
        group = Group.objects.get(name = 'GamesAdminUsers')
        user2.groups.add(group)

    def test_validUpdateForm(self):
        login = self.client.login(username='user2', password='MyPassword123')
        # Retrieve the publisher we want to edit
        currentPublisher = Publishers.objects.get(publisherID = 1)
        # URL to send POST data to
        url = reverse('browserapp:publisher_edit', kwargs = {'pid': currentPublisher.publisherID})
        # Data to send through POST
        data = {
            'publisherName': "Publisher 1",
            'publisherDescription': "Publisher 2's New Description", # Changed the description
            'publisherImage': currentPublisher.publisherImage
        }
        # POSTING
        response = self.client.post(url, data = data)
        # Checking if the URL is valid
        self.assertEqual(response.status_code, 302)
        # Refresh the object in the database
        currentPublisher.refresh_from_db()
        # Check that the description successfully changed
        self.assertEqual(currentPublisher.publisherDescription, "Publisher 2's New Description")

    def test_invalidUpdateForm(self):
        login = self.client.login(username='user2', password='MyPassword123')
        currentPublisher = Publishers.objects.get(publisherID = 1)

        url = reverse('browserapp:publisher_edit', kwargs = {'pid': currentPublisher.publisherID})

        data = {
            'publisherName': "Publisher 2", # There is already a game in the database called this
            'publisherDescription': "Publisher 2's New Description", # Changed the description
            'publisherImage': currentPublisher.publisherImage
        }

        # Posting data
        response = self.client.post(url, data = data, follow=True)
        # Checking to see that the POST is invalid
        self.assertEqual(response.status_code, 200)

    def test_invalidUserPubUpdateForm(self):
        login = self.client.login(username='user1', password='MyPassword123')
        # Retrieve the publisher we want to edit
        currentPublisher = Publishers.objects.get(publisherID = 1)
        # URL to send POST data to
        url = reverse('browserapp:publisher_edit', kwargs = {'pid': currentPublisher.publisherID})
        # Data to send through POST
        data = {
            'publisherName': "Publisher 1",
            'publisherDescription': "Publisher 2's New Description", # Changed the description
            'publisherImage': currentPublisher.publisherImage
        }
        # POSTING
        response = self.client.post(url, data = data)
        # Checking if the URL is invalid
        self.assertEqual(response.status_code, 403)
        # Refresh the object in the database
        currentPublisher.refresh_from_db()
        # Check that the description did not change
        self.assertNotEqual(currentPublisher.publisherDescription, "Publisher 2's New Description")

class GameDeleteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Adding a publisher
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher1 = Publishers(publisherName = "Publisher 1", publisherDescription = "Publisher 1 Description", publisherImage = TestPublisherImage)
        publisher1.full_clean
        publisher1.save()

        # Adding a user to the database
        user1 = User(username='user1', email='user1@email.com')
        user1.set_password('MyPassword123')
        user1.save()

        # Create GamesAdminUsers group
        group_name = "GamesAdminUsers"
        cls.group = Group(name=group_name)
        cls.group.save()

        # Adding an admin to the database
        user2 = User(username = 'user2', email = 'user2@email.com')
        user2.set_password('MyPassword123')
        user2.full_clean
        user2.save()
        group = Group.objects.get(name = 'GamesAdminUsers')
        user2.groups.add(group)

        # Adding a game to the database
        TestGameImage = SimpleUploadedFile(name='TestGameImage.gif', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher = Publishers.objects.get(publisherID = 1)
        game = Games(title = "Game 1", description = "Game 1 description", cheatData = "IHATETESTING: Unlock All", coverImage = TestGameImage, gamePublisher = publisher)
        game.full_clean
        game.save()

    def test_deleteGamefromDB(self):
        login = self.client.login(username='user2', password='MyPassword123')
        dbcount = Games.objects.all().count()
        currentGame = Games.objects.get(gameID = 1)
        url = reverse('browserapp:browse_delete', kwargs = {'gid': currentGame.gameID})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(dbcount-1, Games.objects.all().count())

    def test_invaliddeleteGamefromDB(self):
        login = self.client.login(username='user1', password='MyPassword123')
        dbcount = Games.objects.all().count()
        currentGame = Games.objects.get(gameID = 1)
        url = reverse('browserapp:browse_delete', kwargs = {'gid': currentGame.gameID})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(dbcount-1, Games.objects.all().count())

    def test_invaliddeleteGamefromDB_notAGame(self):
        login = self.client.login(username='user2', password='MyPassword123')
        dbcount = Games.objects.all().count()
        # This is not a game!
        url = reverse('browserapp:browse_delete', kwargs = {'gid': 90000})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(dbcount-1, Games.objects.all().count())


class PublisherDeleteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Adding a publisher
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher1 = Publishers(publisherName = "Publisher 1", publisherDescription = "Publisher 1 Description", publisherImage = TestPublisherImage)
        publisher1.full_clean
        publisher1.save()

        # Adding a user to the database
        user1 = User(username='user1', email='user1@email.com')
        user1.set_password('MyPassword123')
        user1.save()

        # Create GamesAdminUsers group
        group_name = "GamesAdminUsers"
        cls.group = Group(name=group_name)
        cls.group.save()

        # Adding an admin to the database
        user2 = User(username = 'user2', email = 'user2@email.com')
        user2.set_password('MyPassword123')
        user2.full_clean
        user2.save()
        group = Group.objects.get(name = 'GamesAdminUsers')
        user2.groups.add(group)

    def test_deletePublisherfromDB(self):
        # User is an admin
        login = self.client.login(username='user2', password='MyPassword123')
        dbcount = Publishers.objects.all().count()
        currentPublisher = Publishers.objects.get(publisherID = 1)
        url = reverse('browserapp:publisher_delete', kwargs = {'pid': currentPublisher.publisherID})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(dbcount-1, Publishers.objects.all().count())

    def test_invaliddeletePublisherfromDB(self):
        # User is not an admin
        login = self.client.login(username='user1', password='MyPassword123')
        dbcount = Publishers.objects.all().count()
        currentPublisher = Publishers.objects.get(publisherID = 1)
        url = reverse('browserapp:publisher_delete', kwargs = {'pid': currentPublisher.publisherID})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)
        self.assertNotEqual(dbcount-1, Publishers.objects.all().count())

    def test_invaliddeletePublisherfromDB_notAPublisher(self):
        # User is not an admin
        login = self.client.login(username='user2', password='MyPassword123')
        dbcount = Publishers.objects.all().count()
        url = reverse('browserapp:publisher_delete', kwargs = {'pid': 900000})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(dbcount-1, Publishers.objects.all().count())

class GameIndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Adding a publisher
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher1 = Publishers(publisherName = "Publisher 1", publisherDescription = "Publisher 1 Description", publisherImage = TestPublisherImage)
        publisher1.full_clean
        publisher1.save()

        # Adding a game to the database
        TestGameImage = SimpleUploadedFile(name='TestGameImage.gif', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher = Publishers.objects.get(publisherID = 1)
        game = Games(title = "Game 1", description = "Game 1 description", cheatData = "IHATETESTING: Unlock All", coverImage = TestGameImage, gamePublisher = publisher)
        game.full_clean
        game.save()

        # Adding a game to the database
        publisher = Publishers.objects.get(publisherID = 1)
        game = Games(title = "Game 2", description = "Game 2 description", cheatData = "IHATETESTING: Unlock All", coverImage = TestGameImage, gamePublisher = publisher)
        game.full_clean
        game.save()

        # Adding a user to the database
        user1 = User(username='user1', email='user1@email.com')
        user1.set_password('MyPassword123')
        user1.save()

        # Create GamesAdminUsers group
        group_name = "GamesAdminUsers"
        cls.group = Group(name=group_name)
        cls.group.save()

        # Adding an admin to the database
        user2 = User(username = 'user2', email = 'user2@email.com')
        user2.set_password('MyPassword123')
        user2.full_clean
        user2.save()
        group = Group.objects.get(name = 'GamesAdminUsers')
        user2.groups.add(group)

    # Testing w/o logging in
    def test_nologinIndexView(self):
        # Index view URL
        url = reverse('browserapp:browse_index')
        # Client attempts to contact the URL
        response = self.client.get(url)
        # Checking valid URL
        self.assertEqual(response.status_code, 200)
        # Checking view uses the correct template
        self.assertTemplateUsed(response, 'browserapp/index.html')

        # Checking the correct game data is on screen
        self.assertContains(response, "Game 1")
        self.assertContains(response, "Game 1 description")

        self.assertContains(response, 'Game 2')
        self.assertContains(response, 'Game 2 description')

        # Users can see this button w/o login in
        self.assertContains(response, 'BROWSE PUBLISHERS')
        # Only admins can see this button
        self.assertNotContains(response, 'UPLOAD A GAME')

    # Testing logging in as standard user
    def test_standardUserIndexView(self):
        # Logging in as a standard user
        login = self.client.login(username='user1', password='MyPassword123')
        
        url = reverse('browserapp:browse_index')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'browserapp/index.html')

        self.assertContains(response, "Game 1")
        self.assertContains(response, "Game 1 description")

        self.assertContains(response, 'Game 2')
        self.assertContains(response, 'Game 2 description')

        self.assertContains(response, 'BROWSE PUBLISHERS')
        # Only Admins can see this button, even though a user is logged in
        self.assertNotContains(response, 'UPLOAD A GAME')

    # Testing logging in as admin
    def test_adminUserIndexView(self):
        # Logging in as an Admin
        login = self.client.login(username='user2', password='MyPassword123')
        
        url = reverse('browserapp:browse_index')

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'browserapp/index.html')

        self.assertContains(response, "Game 1")
        self.assertContains(response, "Game 1 description")

        self.assertContains(response, 'Game 2')
        self.assertContains(response, 'Game 2 description')

        self.assertContains(response, 'BROWSE PUBLISHERS')
        # Admin should be able to see this button aswell
        self.assertContains(response, 'UPLOAD A GAME')

class PublisherIndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Adding a publisher
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher1 = Publishers(publisherName = "Publisher 1", publisherDescription = "Publisher 1 Description", publisherImage = TestPublisherImage)
        publisher1.full_clean
        publisher1.save()

        # Adding another publisher
        publisher1 = Publishers(publisherName = "Publisher 2", publisherDescription = "Publisher 2 Description", publisherImage = TestPublisherImage)
        publisher1.full_clean
        publisher1.save()

        # Adding a user to the database
        user1 = User(username='user1', email='user1@email.com')
        user1.set_password('MyPassword123')
        user1.save()

        # Create GamesAdminUsers group
        group_name = "GamesAdminUsers"
        cls.group = Group(name=group_name)
        cls.group.save()

        # Adding an admin to the database
        user2 = User(username = 'user2', email = 'user2@email.com')
        user2.set_password('MyPassword123')
        user2.full_clean
        user2.save()
        group = Group.objects.get(name = 'GamesAdminUsers')
        user2.groups.add(group)

    # Testing w/o logging in
    def test_nologinPublisherIndex(self):
        # Index view URL
        url = reverse('browserapp:publisher_index')
        # Client attempts to contact the URL
        response = self.client.get(url)
        # Checking valid URL
        self.assertEqual(response.status_code, 200)
        # Checking view uses the correct template
        self.assertTemplateUsed(response, 'browserapp/pubIndex.html')

        # Checking the correct publisher data is on screen
        self.assertContains(response, "Publisher 1")
        self.assertContains(response, "Publisher 1 Description")

        self.assertContains(response, 'Publisher 2')
        self.assertContains(response, 'Publisher 2 Description')

        # Users can see this button w/o login in
        self.assertContains(response, 'BROWSE GAMES')
        # Only admins can see this button
        self.assertNotContains(response, 'UPLOAD A PUBLISHER')

    # Testing logging in as standard user
    def test_standardLoginPublisherIndex(self):
        # Login as standard user
        login = self.client.login(username='user1', password='MyPassword123')
        # Index view URL
        url = reverse('browserapp:publisher_index')
        # Client attempts to contact the URL
        response = self.client.get(url)
        # Checking valid URL
        self.assertEqual(response.status_code, 200)
        # Checking view uses the correct template
        self.assertTemplateUsed(response, 'browserapp/pubIndex.html')

        # Checking the correct publisher data is on screen
        self.assertContains(response, "Publisher 1")
        self.assertContains(response, "Publisher 1 Description")

        self.assertContains(response, 'Publisher 2')
        self.assertContains(response, 'Publisher 2 Description')

        # Users can see this button w/o login in
        self.assertContains(response, 'BROWSE GAMES')
        # Only admins can see this button
        self.assertNotContains(response, 'UPLOAD A PUBLISHER')

    # Testing logging in as admin
    def test_adminLoginPublisherIndex(self):
        # Login as admin
        login = self.client.login(username='user2', password='MyPassword123')
        # Index view URL
        url = reverse('browserapp:publisher_index')
        # Client attempts to contact the URL
        response = self.client.get(url)
        # Checking valid URL
        self.assertEqual(response.status_code, 200)
        # Checking view uses the correct template
        self.assertTemplateUsed(response, 'browserapp/pubIndex.html')

        # Checking the correct publisher data is on screen
        self.assertContains(response, "Publisher 1")
        self.assertContains(response, "Publisher 1 Description")

        self.assertContains(response, 'Publisher 2')
        self.assertContains(response, 'Publisher 2 Description')

        # Users can see this button w/o login in
        self.assertContains(response, 'BROWSE GAMES')
        # Only admins can see this button
        self.assertContains(response, 'UPLOAD A PUBLISHER')

class PublisherDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Adding a publisher
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher1 = Publishers(publisherName = "Publisher 1", publisherDescription = "Publisher 1 Description", publisherImage = TestPublisherImage)
        publisher1.full_clean
        publisher1.save()

        #TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher2 = Publishers(publisherName = "Publisher 2", publisherDescription = "Publisher 2 Description", publisherImage = TestPublisherImage)
        publisher2.full_clean
        publisher2.save()

        # Adding a game and linking to publisher 2
        TestGameImage = SimpleUploadedFile(name='TestGameImage.gif', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher2obj = Publishers.objects.get(publisherID = 2)
        game = Games(title = "Game 1", description = "Game 1 description", cheatData = "IHATETESTING: Unlock All", coverImage = TestGameImage, gamePublisher = publisher2obj)
        game.full_clean
        game.save()

        # Adding a user to the database
        user1 = User(username='user1', email='user1@email.com')
        user1.set_password('MyPassword123')
        user1.save()

        # Create GamesAdminUsers group
        group_name = "GamesAdminUsers"
        cls.group = Group(name=group_name)
        cls.group.save()

        # Adding an admin to the database
        user2 = User(username = 'user2', email = 'user2@email.com')
        user2.set_password('MyPassword123')
        user2.full_clean
        user2.save()
        group = Group.objects.get(name = 'GamesAdminUsers')
        user2.groups.add(group)

    def test_nologinDetailView(self):
        # Get the publisher we want to see the detail view for
        publisher = Publishers.objects.get(publisherID = 1)
        # Client goes to this link
        url = reverse('browserapp:publisher_detail', kwargs={'pid': publisher.publisherID})
        # Fetch the detail view
        response = self.client.get(url)

        # Check that the url was found
        self.assertEqual(response.status_code, 200)
        # Check that the view uses the correct template
        self.assertTemplateUsed(response, 'browserapp/pubDetail.html')

        # Check that the correct publisher information show
        self.assertContains(response, "Publisher 1")
        self.assertContains(response, "Publisher 1 Description")
        
        # Non admins should not see these buttons
        self.assertNotContains(response, 'Edit')
        self.assertNotContains(response, 'Delete')
        #print(response.content)

    def test_loginDetailView(self):
        # Login as a normal user
        login = self.client.login(username='user1', password='MyPassword123')
        publisher = Publishers.objects.get(publisherID = 1)

        url = reverse('browserapp:publisher_detail', kwargs={'pid': publisher.publisherID})
        # Fetch the detail view
        response = self.client.get(url)

        # Check that the url was found
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'browserapp/pubDetail.html')

        self.assertContains(response, "Publisher 1")
        self.assertContains(response, "Publisher 1 Description")
        # User should still not see these buttons
        self.assertNotContains(response, 'Edit')
        self.assertNotContains(response, 'Delete')
        #print(response.content)

    def test_loginDetailView(self):
        # Login as an admin
        login = self.client.login(username='user2', password='MyPassword123')
        publisher = Publishers.objects.get(publisherID = 1)

        url = reverse('browserapp:publisher_detail', kwargs={'pid': publisher.publisherID})
        # Fetch the detail view
        response = self.client.get(url)

        # Check that the url was found
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'browserapp/pubDetail.html')

        self.assertContains(response, "Publisher 1")
        self.assertContains(response, "Publisher 1 Description")
        # Admin can now see these buttons
        self.assertContains(response, 'Edit')
        self.assertContains(response, 'Delete')

    # Testing publisher detail view that has a game linked with them
    def test_publisherwithGameDetail(self):
        # Login as an admin
        login = self.client.login(username='user2', password='MyPassword123')
        publisher = Publishers.objects.get(publisherID = 2)

        url = reverse('browserapp:publisher_detail', kwargs={'pid': publisher.publisherID})
        # Fetch the detail view
        response = self.client.get(url)

        # Check that the url was found
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'browserapp/pubDetail.html')

        self.assertContains(response, "Publisher 2")
        self.assertContains(response, "Publisher 2 Description")

        # Checking to see if we can see the linked games
        self.assertContains(response, 'Game 1')
        self.assertContains(response, 'Game 1 description')
        # Admin can now see these buttons
        self.assertContains(response, 'Edit')
        self.assertContains(response, 'Delete')

        #print(response.content)


class MyGamesIndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Adding a publisher
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher1 = Publishers(publisherName = "Publisher 1", publisherDescription = "Publisher 1 Description", publisherImage = TestPublisherImage)
        publisher1.full_clean
        publisher1.save()

        # Adding a game
        TestGameImage = SimpleUploadedFile(name='TestGameImage.gif', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher = Publishers.objects.get(publisherID = 1)
        game = Games(title = "Game 1", description = "Game 1 description", cheatData = "IHATETESTING: Unlock All", coverImage = TestGameImage, gamePublisher = publisher)
        game.full_clean
        game.save()

        # Adding another game
        TestGameImage = SimpleUploadedFile(name='TestGameImage.gif', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher = Publishers.objects.get(publisherID = 1)
        game = Games(title = "Game 2", description = "Game 2 description", cheatData = "IHATETESTING: Unlock All", coverImage = TestGameImage, gamePublisher = publisher)
        game.full_clean
        game.save()

        # Adding a user to the database
        user1 = User(username='user1', email='user1@email.com')
        user1.set_password('MyPassword123')
        user1.save()

        # Adding another user to the database
        user2 = User(username='user2', email='user2@email.com')
        user2.set_password('MyPassword123')
        user2.save()

        # # Adding games to library for User 1
        currentUser = User.objects.get(pk=1)
        currentGame = Games.objects.get(gameID = 1)

        newentry = UserGames(user = currentUser, game = currentGame)

        # Add to database
        newentry.full_clean
        newentry.save()

        # # Adding games to library for User 2
        currentUser2 = User.objects.get(pk=2)
        currentGame2 = Games.objects.get(gameID = 2)

        newentry2 = UserGames(user = currentUser2, game = currentGame2)

        # Add to database
        newentry2.full_clean
        newentry2.save()

    # Test what user1 can see in their library
    def test_user1MyGames(self):
        # Get the expected game
        gameInLibrary = Games.objects.get(gameID = 1)
        # Get the unexpected game
        wrongGameInLibrary = Games.objects.get(gameID = 2)
        # Login as user1
        login = self.client.login(username='user1', password='MyPassword123')

        url = reverse('browserapp:myGamesIndex')

        response = self.client.get(url)

        # Check that URL is valid
        self.assertEqual(response.status_code, 200)

        # Welcome message contains user1
        self.assertContains(response, 'user1')
        # Check that the expected game can be seen
        self.assertContains(response, gameInLibrary.title)
        # Check that the unexpected game cannot be seen
        self.assertNotContains(response, wrongGameInLibrary.title)
        #print(response.content)

    # Test what user2 can see in their library
    def test_user2MyGames(self):
        # Get the expected game
        gameInLibrary = Games.objects.get(gameID = 2)
        # Get the unexpected game
        wrongGameInLibrary = Games.objects.get(gameID = 1)
        # Login as user1
        login = self.client.login(username='user2', password='MyPassword123')

        url = reverse('browserapp:myGamesIndex')

        response = self.client.get(url)

        # Check that URL is valid
        self.assertEqual(response.status_code, 200)

        # Welcome message contains user1
        self.assertContains(response, 'user2')
        # Check that the expected game can be seen
        self.assertContains(response, gameInLibrary.title)
        # Check that the unexpected game cannot be seen
        self.assertNotContains(response, wrongGameInLibrary.title)
        #print(response.content)

    # Checking that not logged in user gets redirected to log in page
    def test_nologinMyGames(self):
        url = reverse('browserapp:myGamesIndex')

        response = self.client.get(url, follow=True)

        self.assertContains(response, 'Log In')

class AJAXAddGameTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Adding a publisher
        TestPublisherImage = SimpleUploadedFile(name='TestPublisherImage.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher1 = Publishers(publisherName = "Publisher 1", publisherDescription = "Publisher 1 Description", publisherImage = TestPublisherImage)
        publisher1.full_clean
        publisher1.save()

        # Adding a game
        TestGameImage = SimpleUploadedFile(name='TestGameImage.gif', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher = Publishers.objects.get(publisherID = 1)
        game = Games(title = "Game 1", description = "Game 1 description", cheatData = "IHATETESTING: Unlock All", coverImage = TestGameImage, gamePublisher = publisher)
        game.full_clean
        game.save()

        # Adding a user to the database
        user1 = User(username='user1', email='user1@email.com')
        user1.set_password('MyPassword123')
        user1.save()

    # Send a valid AJAX request to the view
    def AJAXValidResponseTest(self):
        # login as user1
        login = self.client.login(username='user1', password='MyPassword123')
        currentGame = Games.objects.get(gameID = 1)

        url = reverse('browserapp:addGametoLibrary')

        # data to send to view
        data = {
            'gameID': currentGame.gameID
        }

        # Requires adding JSON header and XML header
        response = self.client.get(url, data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        # Check valid URL
        self.assertEqual(response.status_code, 200)
        # Check JSON response gives us an updatedLibrary true variable
        self.assertContains(response, 'true')
        #print(response.content)

    # Send an invalid AJAX request, user is not logged in
    def AJAXLoggedOutResponseTest(self):
        # User is not logged in
        currentGame = Games.objects.get(gameID = 1)

        url = reverse('browserapp:addGametoLibrary')

        data = {
            'gameID': currentGame.gameID
        }

        response = self.client.get(url, data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        # Checking that the response is invalid, view is not processed
        self.assertEqual(response.status_code, 302)

        
    # 04/Dec/2022 18:24:35] "GET /browse/add?gameID=16 HTTP/1.1" 200 24
    #[04/Dec/2022 18:24:35] "GET /browse/16 HTTP/1.1" 200 7418

        

    









    
    

















