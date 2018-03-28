from django.test import TestCase

from pawpals.views import *
from pawpals.models import *
from django.urls import *
from pawpals.urls import *
from django.contrib.auth.models import User #Required to chevk for login_required views



class Login_test(TestCase):

    def test_login(self):

        # First check for the default behavior
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, '/pawpals/login/')

        # Then override the LOGIN_URL setting
        with self.settings(LOGIN_URL='/wrongURL/login/'):
            response = self.client.get('/requests/') #requires login, so will redirect
            self.assertRedirects(response, '/pawpals/login/?next=/pawpals/login/requests/')

class SheltersView_test(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/pawpals/shelters/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('shelters'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'pawpals/shelters.html')

    def test_context_is_passed_test(self):
        response = self.client.get(reverse('shelters'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('shelters' in response.context)


#tests passed in this view will confirm that decorators are working
class edit_profile_view_test(TestCase):

    def setUp(self):
        #Create a dummy user to test
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('edit'))
        self.assertRedirects(resp, '/pawpals/login/?next=/pawpals/edit/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('edit'))

         #Check that user is logged in
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #Check that the response is "success"
        self.assertEqual(resp.status_code, 200)

         #Check we used correct template
        self.assertTemplateUsed(resp, 'pawpals/edit.html')

class decorators_test(TestCase):

    def setUp(self):
        #Create two dummy users to test (one manager and one standard)
        test_user1 = User.objects.create_user(username='testuser1', password='12345', is_standard = True)
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='12345', is_manager = True)
        test_user2.save()


    def test_redirect_if_wrong_user_type(self):
        login = self.client.login(username='testuser2', password='12345')
        response = self.client.get('pawpals/request/bailey-1/') #using existing dog request page
        #should make you login with needed usertype account
        self.assertRedirects(response, 'pawpals/login/?next=/pawpals/request/bailey-1/')

    def test_stay_if_right_user_type(self):
        login = self.client.get(username='testuser1', password='12345')
        response = self.client.get('pawpals/request/bailey-1/') #existing dog request next_page
        #should give "success" response
        self.assertEqual(response.status_code, 200)
