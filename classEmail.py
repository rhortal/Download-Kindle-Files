class Email:
    def __init__(self, subject, html_content):
        self.subject = subject
        self.html_content = html_content
        self.links = self.extract_links()

    def extract_links(self):
        #Extracts all links from the HTML content.
        soup = BeautifulSoup(self.html_content, 'html.parser')
        return [a['href'] for a in soup.find_all('a', href=True)]
    
    def filename(self):
        #Creates a string-safe filename to use for saving
        start = self.subject.find('\"') + 1  # +1 to exclude the first quote
        end = self.subject.find('\"', start)  # Find the next quote after the start
        return self.subject[start:end].replace('/', '-')