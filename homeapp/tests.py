from urllib import response
from django.test import TestCase
from django.urls import reverse

from browserapp.models import Games, Publishers, User
from django.core.files.uploadedfile import SimpleUploadedFile

from django.core.mail import outbox

# Create your tests here.

class HomePageTests(TestCase):
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
        

    # Basic homepage testing
    def test_basichomepage(self):
        # Get the homepage URL
        response = self.client.get(reverse('homeapp:home'))
        # Check that the homepage is valid
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Welcome to ')
        self.assertContains(response, 'Cheats sourced and provided by Melric')

        self.assertContains(response, 'Top Rated Games')
        self.assertContains(response, 'Most Recent Games')
        # Check we can see the current added game in homepage
        self.assertContains(response, 'Game 1')
        # We shouldnt see another game in here
        self.assertNotContains(response, 'Game 2')

    def test_addGamehomepage(self):
        # Adding a second game to database
        TestGameImage = SimpleUploadedFile(name='TestGameImage.gif', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        publisher = Publishers.objects.get(publisherID = 1)
        game = Games(title = "Game 2", description = "Game 2 description", cheatData = "IHATETESTING: Unlock All", coverImage = TestGameImage, gamePublisher = publisher)
        game.full_clean
        game.save()

        response = self.client.get(reverse('homeapp:home'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Welcome to ')
        self.assertContains(response, 'Cheats sourced and provided by Melric')

        self.assertContains(response, 'Top Rated Games')
        self.assertContains(response, 'Most Recent Games')
        # We should be able to see both games on the homepage
        self.assertContains(response, 'Game 1')
        self.assertContains(response, 'Game 2')

class ContactPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        return

    def testbasic_contact(self):
        # Reverse allows us to reverse search the url by using the name given to it
        # Allows us to change the url in one place without having to change it everywhere
        response = self.client.get(reverse('homeapp:contact')) 
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Want to request a game?')
        self.assertContains(response, 'Cheats sourced and provided by Melric')

    def validContactPOST(self):
        # Get the url to send POST data to
        url = reverse('homeapp:contact')

        # Contact form fields
        data = {
            'name': "Test Name",
            'email': "test@test.com",
            'subject': "Test Subject",
            'message': "Test Message"
        }

        # Posting to view
        response = self.client.post(url, data = data, follow=True)

        # Check that the post data was valid and had no errors
        self.assertEqual(response, 302)

        # Checking if an email was sent and the contents
        self.assertEqual(len(outbox), 1)
        self.assertEqual(outbox[0].name, 'Test Name')
        self.assertEqual(outbox[0].email, 'test@test.com')
        self.assertEqual(outbox[0].subject, 'Test Subject')
        self.assertEqual(outbox[0].message, 'Test Message')

    def invalidContactPOST(self):
        # Get the url to send POST data to
        url = reverse('homeapp:contact')

        # Contact form fields
        data = {
            'name': "Test Name",
            'email': "test", # Invalid Email
            'subject': "Test Subject",
            'message': "Test Message"
        }

        # Posting to view
        response = self.client.post(url, data = data)

        # Check that the post data was invalid and had errors
        self.assertEqual(response, 200)

        # Checking an email was not sent
        self.assertNotEqual(len(outbox), 1)
    
