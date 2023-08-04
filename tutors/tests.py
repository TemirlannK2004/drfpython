import requests
from unittest import TestCase, mock
from rest_framework import status
from .models import TutorRequest

class PatchTestCase(TestCase):
    def setUp(self):
        self.mock_request = mock.Mock()
        self.mock_request.data = {
            'tutor_request_id': 1,
            'status': 'pending'
        }
        self.mock_tutor_request = mock.Mock()
        self.mock_tutor_request.id = 1
        self.mock_tutor_request.tutor_id = 1
        self.mock_tutor_request.status = 'pending'
        self.mock_tutor_request.save.return_value = None
        self.mock_tutor_request.DoesNotExist = TutorRequest.DoesNotExist

        self.mock_response = mock.Mock()

    @mock.patch('requests.post')
    @mock.patch('TutorRequest.objects.get')
    def test_patch_valid_status(self, mock_get, mock_post):
        mock_get.return_value = self.mock_tutor_request
        mock_post.return_value.status_code = 200

        response = self.client.patch('/api/tutors/1', self.mock_request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Successfully'})

    @mock.patch('requests.post')
    @mock.patch('TutorRequest.objects.get')
    def test_patch_invalid_status(self, mock_get, mock_post):
        mock_get.return_value = self.mock_tutor_request
        mock_post.return_value.status_code = 400

        response = self.client.patch('/api/tutors/1', self.mock_request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Invalid status value'})

    @mock.patch('requests.post')
    @mock.patch('TutorRequest.objects.get', side_effect=TutorRequest.DoesNotExist)
    def test_patch_tutor_request_not_found(self, mock_get, mock_post):
        mock_post.return_value.status_code = 400

        response = self.client.patch('/api/tutors/1', self.mock_request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'error': 'Tutor request not found'})

    @mock.patch('requests.post', side_effect=requests.exceptions.RequestException)
    @mock.patch('TutorRequest.objects.get')
    def test_patch_request_failed(self, mock_get, mock_post):
        mock_get.return_value = self.mock_tutor_request

        response = self.client.patch('/api/tutors/1', self.mock_request)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data, {'error': 'Failed'})