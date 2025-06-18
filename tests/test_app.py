import pytest
import json
from unittest.mock import patch, MagicMock
from server.app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestApp:
    """Test cases for the Flask application."""

    def test_voice_endpoint_get(self, client):
        """Test the voice endpoint with GET request."""
        response = client.get('/voice')
        assert response.status_code == 200
        assert 'Hello! How can I help you today?' in response.data.decode()

    def test_voice_endpoint_post_no_speech(self, client):
        """Test the voice endpoint with POST request but no speech result."""
        response = client.post('/voice')
        assert response.status_code == 200
        assert 'Hello! How can I help you today?' in response.data.decode()

    @patch('server.app.call_langflow_api')
    def test_voice_endpoint_with_speech(self, mock_langflow, client):
        """Test the voice endpoint with speech result."""
        mock_langflow.return_value = "I understand your question about S3 buckets."
        
        response = client.post('/voice', data={'SpeechResult': 'Tell me about S3 buckets'})
        assert response.status_code == 200
        assert 'I understand your question about S3 buckets' in response.data.decode()
        mock_langflow.assert_called_once_with('Tell me about S3 buckets')

    def test_search_endpoint(self, client):
        """Test the search endpoint."""
        with patch('server.app.GoogleSearchAPIWrapper') as mock_search:
            # Mock the search results
            mock_instance = MagicMock()
            mock_instance.results.return_value = [
                {
                    'title': 'S3 Bucket Interview Questions',
                    'link': 'https://example.com/s3-questions',
                    'snippet': 'Common S3 bucket interview questions and answers'
                }
            ]
            mock_search.return_value = mock_instance
            
            response = client.get('/search')
            assert response.status_code == 200
            
            data = json.loads(response.data)
            assert data['status'] == 'success'
            assert data['results_count'] == 1
            assert len(data['results']) == 1
            assert data['results'][0]['title'] == 'S3 Bucket Interview Questions'

    @patch('server.app.call_langflow_api')
    def test_langflow_api_error_handling(self, mock_langflow, client):
        """Test error handling when Langflow API fails."""
        mock_langflow.return_value = "I'm sorry, I'm having trouble connecting to the AI service right now."
        
        response = client.post('/voice', data={'SpeechResult': 'test question'})
        assert response.status_code == 200
        assert 'having trouble connecting' in response.data.decode()

    def test_environment_variables_check(self):
        """Test that the app can start without environment variables (for testing)."""
        # This test ensures the app doesn't crash when env vars are missing
        assert app is not None
        assert hasattr(app, 'route')


if __name__ == '__main__':
    pytest.main([__file__]) 