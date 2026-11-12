from unittest.mock import patch

from django.test import TestCase
from .models import VerifiedEmail


class OTPFlowTests(TestCase):
	def test_login_screen_shows_first_step(self):
		response = self.client.get('/')

		self.assertContains(response, 'ACCESS / 01')
		self.assertContains(response, '01 <b>/</b> 02', html=True)

	def test_stylesheet_is_served(self):
		response = self.client.get('/static/app/site.css')

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, '--forest: #173c34;')

	@patch('app.views.send_mail')
	def test_login_sends_code_and_redirects_to_verification(self, send_mail_mock):
		response = self.client.post('/', {'email': 'person@example.com'})

		self.assertRedirects(response, '/verify/')
		self.assertRegex(self.client.session['user_otp'], r'^\d{6}$')
		send_mail_mock.assert_called_once()
		self.assertEqual(send_mail_mock.call_args.args[3], ['person@example.com'])

	def test_valid_code_renders_success_and_consumes_code(self):
		session = self.client.session
		session['user_email'] = 'person@example.com'
		session['user_otp'] = '123456'
		session.save()

		response = self.client.post('/verify/', {'user_otp': '123456'})

		self.assertTemplateUsed(response, 'app/success.html')
		self.assertContains(response, 'person@example.com')
		self.assertNotIn('user_otp', self.client.session)
		self.assertTrue(VerifiedEmail.objects.filter(email='person@example.com').exists())

	def test_invalid_code_renders_failure(self):
		session = self.client.session
		session['user_otp'] = '123456'
		session.save()

		response = self.client.post('/verify/', {'user_otp': '000000'})

		self.assertTemplateUsed(response, 'app/failure.html')
		self.assertEqual(VerifiedEmail.objects.count(), 0)

	def test_verifying_same_email_twice_keeps_one_record(self):
		VerifiedEmail.objects.create(email='person@example.com')
		session = self.client.session
		session['user_email'] = 'PERSON@example.com'
		session['user_otp'] = '123456'
		session.save()

		self.client.post('/verify/', {'user_otp': '123456'})

		self.assertEqual(VerifiedEmail.objects.count(), 1)

	def test_verification_without_session_renders_failure(self):
		response = self.client.get('/verify/')

		self.assertTemplateUsed(response, 'app/failure.html')

	def test_verification_screen_shows_session_email(self):
		session = self.client.session
		session['user_email'] = 'person@example.com'
		session['user_otp'] = '123456'
		session.save()

		response = self.client.get('/verify/')

		self.assertContains(response, 'person@example.com')
		self.assertContains(response, 'ACCESS / 02')
		self.assertContains(response, '02 <b>/</b> 02', html=True)
