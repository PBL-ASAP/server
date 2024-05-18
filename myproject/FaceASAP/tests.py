from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

class UploadVideoTest(TestCase):
    def test_upload_video(self):
        with open('test_video.mp4', 'rb') as video:
            response = self.client.post('/upload/', {'video': video})
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json())
