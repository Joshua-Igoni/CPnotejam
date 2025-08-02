from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


from notes.models import Note


def create_user(user_data):
    User = get_user_model()
    return User.objects.create_user(
        username=user_data['email'],
        email=user_data['email'],
        password=user_data['password']
    )


class NoteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user@example.com', email='user@example.com', password='secure_password')
        self.client.login(username='user@example.com', password='secure_password')

    def test_create_success(self):
        self.client.post(
            reverse('create_note'), {'name': 'pad', 'text': 'pad text'})
        self.assertEqual(1, Note.objects.count())

    def test_create_fail_required_fields(self):
        response = self.client.post(reverse('create_note'), {})
        self.assertEqual(
            set(['name', 'text']), set(response.context['form'].errors.keys()))

    def test_edit_success(self):
        note_data = {
            'name': 'note name',
            'text': 'note text'
        }
        note = Note.objects.create(user=self.user, **note_data)

        note_data['name'] = 'new name'
        response = self.client.post(
            reverse('edit_note', args=(note.id,)), note_data)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(note_data['name'], Note.objects.get(id=note.id).name)

    def test_another_user_cant_edit(self):
        user_data = {
            'email': 'another_user@example.com',
            'password': 'another_secure_password'
        }
        create_user(user_data)

        note_data = {
            'name': 'note name',
            'text': 'note text'
        }
        note = Note.objects.create(user=self.user, **note_data)

        client = Client()
        client.login(**user_data)
        response = client.post(reverse('edit_note', args=(note.id,)), {})
        self.assertEqual(404, response.status_code)

    def test_view_success(self):
        note_data = {
            'name': 'note name',
            'text': 'note text'
        }
        note = Note.objects.create(user=self.user, **note_data)
        response = self.client.get(reverse('view_note', args=(note.id,)), {})
        self.assertEqual(note, response.context['note'])

    def test_another_user_cant_view(self):
        user_data = {
            'email': 'another_user@example.com',
            'password': 'another_secure_password'
        }
        create_user(user_data)

        note_data = {
            'name': 'note name',
            'text': 'note text'
        }
        note = Note.objects.create(user=self.user, **note_data)

        client = Client()
        client.login(**user_data)
        response = client.get(reverse('view_note', args=(note.id,)), {})
        self.assertEqual(404, response.status_code)

    def test_delete_success(self):
        note_data = {
            'name': 'note name',
            'text': 'note text'
        }
        note = Note.objects.create(user=self.user, **note_data)
        self.client.post(reverse('delete_note', args=(note.id,)), {})
        self.assertEqual(0, Note.objects.count())

    def test_another_user_cant_delete(self):
        user_data = {
            'email': 'another_user@example.com',
            'password': 'another_secure_password'
        }
        create_user(user_data)

        note_data = {
            'name': 'note name',
            'text': 'note text'
        }
        note = Note.objects.create(user=self.user, **note_data)

        client = Client()
        client.login(**user_data)
        response = client.get(reverse('view_note', args=(note.id,)), {})
        self.assertEqual(404, response.status_code)
