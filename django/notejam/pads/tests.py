from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from notejam.tests import create_user
from pads.models import Pad


class PadTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user@example.com', email='user@example.com', password='secure_password')
        self.client.login(username='user@example.com', password='secure_password')

    def _create_pads(self, pads):
        return [
            (lambda pad: Pad.objects.create(name=pad, user=self.user).id)(pad)
            for pad in pads
        ]

    def test_create_success(self):
        self.client.post(reverse('create_pad'), {'name': 'pad'})
        self.assertEqual(1, Pad.objects.count())

    def test_create_fail_required_name(self):
        response = self.client.post(reverse('create_pad'), {})
        self.assertIn('name', response.context['form'].errors)

    def test_edit_success(self):
        id = self._create_pads(['pad'])[0]
        data = {'name': 'new name'}
        response = self.client.post(reverse('edit_pad', args=(id,)), data)
        self.assertRedirects(response, reverse('view_pad_notes', args=(id,)))
        self.assertEqual(data['name'], Pad.objects.get(id=id).name)

    def test_another_user_cant_edit_pad(self):
        user_data = {
            'email': 'another_user@example.com',
            'password': 'another_secure_password'
        }
        create_user(user_data)

        client = Client()
        client.login(**user_data)
        id = self._create_pads(['pad'])[0]
        response = client.post(reverse('edit_pad', args=(id,)), {})
        self.assertEqual(404, response.status_code)
