from django.test import TestCase
from django.urls import reverse
from .models import Sticky_Notes
from .forms import StickyForm

# creating my test classes
class FormTest(TestCase):

 # create a new form with the fields expected filled in
    def setUp(self):
        Sticky_Notes.objects.create(title='Test Form', things_to_do='Sample task 1')
        Sticky_Notes.objects.create(title='Test Title', things_to_do='Sample task 2')

# function that tests if the new forms have the correct titles 
    def test_title(self):
        form = Sticky_Notes.objects.get(title='Test Form')
        self.assertEqual(form.title, 'Test Form')

# test checks that the content is filled in correctly

    def test_content(self):
        form = Sticky_Notes.objects.get(title='Test Form')
        self.assertEqual(form.things_to_do, 'Sample task 1')

    def test_second_content(self):
        form = Sticky_Notes.objects.get(title='Test Title')
        self.assertEqual(form.things_to_do, 'Sample task 2')

# test to check that the correct URL is loaded as landing

    def test_sticky_list(self):
        response = self.client.get(reverse('notes_all'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Form')

# tests to check my views logic

class ManageNotesViews(TestCase):
    
    def test_manage_notes_post(self):
        url = reverse('manage_notes')
        data = {
            'title': 'Test Note',
            'things_to_do': 'Sample task'
        }
        response = self.client.post(url, data)
        
        # Check redirected to 'notes_all'
        self.assertEqual(response.status_code, 302)  # 302 indicates redirection
        self.assertRedirects(response, reverse('notes_all'))

    def test_manage_notes_get(self):
        url = reverse('manage_notes')
        response = self.client.get(url)
        
        # Check form is rendered on GET request
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sticky_notes/sticky_form.html')
        self.assertIsInstance(response.context['form'], StickyForm)

class DeleteNoteViewTest(TestCase):
    
    def setUp(self):
        self.note = Sticky_Notes.objects.create(title='Test Note', things_to_do='Sample task')

    def test_delete_note(self):
        url = reverse('delete_note')
        data = {
            'note_id': self.note.id
        }
        response = self.client.post(url, data, content_type='application/json')
        
        # Check note deleted successfully
        self.assertEqual(response.status_code, 404)
        

      
class UpdateNoteViewTest(TestCase):
    
    def setUp(self):
        self.note = Sticky_Notes.objects.create(title='Test Note', things_to_do='Sample task')

    def test_update_note_post(self):
        url = reverse('update_note', kwargs={'pk': self.note.pk})
        data = {
            'title': 'Updated Note',
            'things_to_do': 'Updated task'
        }
        response = self.client.post(url, data)
        
        # Check note updated successfully and redirected to 'notes_all'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes_all'))

    def test_update_note_get(self):
        url = reverse('update_note', kwargs={'pk': self.note.pk})
        response = self.client.get(url)
        
        # Check form is rendered on GET request and contains correct data
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sticky_notes/update_form.html')
        self.assertIsInstance(response.context['form'], StickyForm)
        self.assertEqual(response.context['note'], self.note)
