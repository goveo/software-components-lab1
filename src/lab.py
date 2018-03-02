from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re
import xmlparser


parser = xmlparser.Parser("urls.xml")

links = parser.getArrayAttributes('link')
depth = int(parser.getOneAttribute('depth'))

new_urls = deque(links)
processed_urls = set()
emails = set()

visited = 0
current_depth = 0


def getEmailsFromHtml(html):
    return set(re.findall(
        r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", html, re.I))

def printEmails():
    if (len(emails) == 0):
	    print("Pages don't have emails")
    else:
        print("Emails on pages : ")
        for email in emails:
            print(email)



def getLinksInHtml(html):
    soup = BeautifulSoup(html, "html.parser")
    links = []

    for anchor in soup.find_all("a"):

        if "href" in anchor.attrs:
            link = anchor.attrs["href"]
        else:
            link = ''

        if link.startswith('/'):
            link = base_url + link
        elif not link.startswith('http'):
            link = path + link

        if link.endswith(';'):
            continue

        if not link in new_urls and not link in processed_urls:
            links.append(link)

    return links


for current_depth in range(depth + 1):
    urls_of_this_depth = []

    while len(new_urls):
        print('{0} links on depth #{1} left'.format(
            len(new_urls), current_depth))
        visited = visited + 1

        # move next url from the queue to the set of processed urls
        url = new_urls.popleft()
        processed_urls.add(url)

        # extract base url to resolve relative links
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        print("Visited %s" % (url))
        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        # find emails
        page_html = response.text
        new_emails = getEmailsFromHtml(page_html)
        emails.update(new_emails)

        new_urls_from_current_page = getLinksInHtml(page_html)

        for link in new_urls_from_current_page:
            urls_of_this_depth.append(link)

    for newlink in urls_of_this_depth:
        new_urls.append(newlink)

    current_depth = current_depth + 1

parser.writeArrayToFile('emails.xml', 'emails', 'email', emails)