import unittest
from bs4 import BeautifulSoup
from classEmail import Email

class TestEmail(unittest.TestCase):

    def setUp(self):
        # Sample HTML content and subject for testing
        self.subject = 'Test Email "My Test / Email"'
        self.html_content = '''
        <html>
            <body>
                <p>Check this out!</p>
                <a href="http://example.com/link1">Link 1</a>
                <a href="http://example.com/link2">Link 2</a>
                <a href="http://example.com/link3">Link 3</a>
            </body>
        </html>
        '''
        self.email = Email(subject=self.subject, html_content=self.html_content)

    def test_extract_links(self):
        # Test the link extraction functionality
        expected_links = [
            "http://example.com/link1",
            "http://example.com/link2",
            "http://example.com/link3"
        ]
        self.assertEqual(self.email.links, expected_links)

    def test_filename(self):
        # Test the filename generation functionality
        expected_filename = 'My Test - Email'  # Based on the subject
        self.assertEqual(self.email.filename(), expected_filename)

if __name__ == '__main__':
    unittest.main()