from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from django.test import TestCase
from django.contrib.auth.models import User
from myapp.models import Interest

class LoginTestCase(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_successful(self):
        response = self.client.post('/myapp/api/login/', {
            'username': 'testuser',
            'password': 'testpassword'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login successful')

    def test_login_unsuccessful(self):
        response = self.client.post('/myapp/api/login/', {
            'username': 'wronguser',
            'password': 'wrongpassword'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid credentials', response.json().get('error', ''))

    def test_login_user_does_not_exist(self):
        response = self.client.post('/myapp/api/login/', {
            'username': 'nonexistentuser',
            'password': 'testpassword'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid credentials', response.json().get('error', ''))


class InterestTestCase(TestCase):
    
    def setUp(self):
        # Create two users
        self.sender = User.objects.create_user(username='senderuser', password='testpassword')
        self.recipient = User.objects.create_user(username='recipientuser', password='testpassword')
    
    def test_send_and_receive_interest(self):
        # Log in as sender and send an interest
        self.client.login(username='senderuser', password='testpassword')
        response = self.client.post(f'/myapp/api/send-interest/{self.recipient.id}/', {'message': 'Hi, let’s connect!'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Log out and then log in as recipient to check received interests
        self.client.logout()
        self.client.login(username='recipientuser', password='testpassword')
        
        response = self.client.get('/myapp/api/received-interests/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        interests = response.json()
        self.assertIsInstance(interests, list)
        self.assertEqual(len(interests), 1)
        
        first_interest = interests[0]
        self.assertEqual(first_interest['sender__username'], 'senderuser')
        self.assertEqual(first_interest['message'], 'Hi, let’s connect!')
        
        # Accept the interest
        interest_id = first_interest['id']
        response = self.client.post(f'/myapp/api/accept-interest/{interest_id}/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        # Verify that the interest has been accepted
        interest = Interest.objects.get(id=interest_id)
        self.assertTrue(interest.accepted)

class BasicChatTests(TestCase):

    def setUp(self):
        # Create two users and an interest
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.interest = Interest.objects.create(sender=self.user1, recipient=self.user2, message='Hi!')

    def test_access_chat_page(self):
        # Log in as user1
        self.client.login(username='user1', password='password')

        # Access the chat page
        response = self.client.get(f'/chat/{self.interest.id}/')

        # Print the actual status code and content for debugging
        print("Status Code:", response.status_code)
        print("Response Content:", response.content.decode())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are chatting with')


