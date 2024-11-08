import unittest
from unittest.mock import patch, MagicMock
from main import (
    load_environment_variables,
    fetch_emails,
    process_emails,
    download_links,
    upload_to_cloud,
)

class TestEmailProcessing(unittest.TestCase):

    @patch('main.load_dotenv')
    @patch('os.getenv')
    def test_load_environment_variables(self, mock_getenv, mock_load_dotenv):
        mock_getenv.side_effect = lambda k, d=None: {
            'IMAP_SERVER': 'mock_imap_server',
            'EMAIL_ADDRESS': 'mock_email',
            'APP_PASSWORD': 'mock_password',
            'ATTACHMENT_PATH': 'mock_attachment_path',
            'DAYS_BACK': '7',
            'RCLONE': 'mock_rclone',
            'RCLONE_PATH': 'mock_rclone_path'
        }.get(k, d)
        
        env_vars = load_environment_variables()
        
        self.assertEqual(env_vars['IMAP_SERVER'], 'mock_imap_server')
        self.assertEqual(env_vars['EMAIL_ADDRESS'], 'mock_email')
        self.assertEqual(env_vars['APP_PASSWORD'], 'mock_password')
        self.assertEqual(env_vars['ATTACHMENT_PATH'], 'mock_attachment_path')
        self.assertEqual(env_vars['DAYS_BACK'], 7)
        self.assertEqual(env_vars['RCLONE'], 'mock_rclone')
        self.assertEqual(env_vars['RCLONE_PATH'], 'mock_rclone_path')
    """ 
    @patch('imap_tools.MailBox')
    def test_fetch_emails(self, mock_mailbox):
        # Create a mock email message
        mock_message = MagicMock()
        mock_message.subject = 'from your Kindle'
        mock_message.html = 'This is a test email.'

        # Set up MailBox mock
        mock_mailbox_instance = MagicMock()
        mock_mailbox.return_value = mock_mailbox_instance
        mock_mailbox_instance.login.return_value = None  # Simulate successful login
        mock_mailbox_instance.fetch.return_value = [mock_message]  # Return our mock message

        # Call the function under test
        fetched_emails = fetch_emails('mock_imap_server', 'mock_email', 'mock_password', 7)

        # Assertions
        self.assertEqual(len(fetched_emails), 1)
        self.assertEqual(fetched_emails[0].subject, 'from your Kindle')

    """
    def test_process_emails(self):
        from classEmail import Email
        mock_message = MagicMock()
        mock_message.subject = 'Test Email'
        mock_message.html = '<p>This is a test email content.</p>'
        
        emails = process_emails([mock_message])
        
        self.assertEqual(len(emails), 1)
        self.assertIsInstance(emails[0], Email)
        self.assertEqual(emails[0].subject, 'Test Email')

    @patch('requests.get')
    @patch('os.makedirs')
    @patch('os.path.isfile')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_download_links(self, mock_open, mock_isfile, mock_makedirs, mock_requests_get):
        mock_requests_get.return_value.content = b'Test file content.'
        mock_isfile.return_value = False

        class MockEmail:
            def extract_links(self):
                return ['http://example.com/test1', 'http://example.com/test2']

            def filename(self):
                return 'test_email'

        mock_emails = [MockEmail()]
        download_links(mock_emails, 'mock_attachment_path')

        mock_requests_get.assert_called()
        mock_open.assert_called()  # Check if open() was called
        self.assertTrue(mock_makedirs.called)

"""     @patch('call_rclone')
    def test_upload_to_cloud(self, mock_call_rclone):
        upload_to_cloud('mock_rclone', 'mock_attachment_path', 'mock_rclone_path')
        mock_call_rclone.assert_called_once_with('copy', 'mock_attachment_path', 'mock_rclone_path')
"""
if __name__ == '__main__':
    unittest.main()
