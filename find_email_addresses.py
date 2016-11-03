#!/usr/bin/env python
"""
Email scanner: prints all email addresses found on a domain.
Joe Kamibeppu | 10 Oct 2016
Dependencies:
    Beautiful Soup (pip install beautifulsoup4)
    Requests (pip install requests)
Usage:
    python find_email_addresses.py [domain name]
"""

import sys
import argparse
from urlparse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup, SoupStrainer

def find_emails(base_url):
    ''' finds email addresses by iteratively traversing through pages '''
    emails = set()
    to_visit = set()
    visited = set()

    to_visit.add(base_url)

    while len(to_visit) > 0:
        page = to_visit.pop()
        response = requests.get(page)
        visited.add(page)
        hrefs = BeautifulSoup(response.text, 'html.parser',
                              parse_only=SoupStrainer('a'))
        for email_href in hrefs.select('a[href^=mailto]'):
            emails.add(email_href.get('href').replace('mailto:', ''))
        for link in hrefs.select('a[href]'):
            new_url = urljoin(base_url, link['href'])
            if urlparse(new_url).hostname == urlparse(base_url).hostname:
                if new_url not in visited:
                    to_visit.add(new_url)
        if len(to_visit) > 500:
            print "More than 500 subpages have been found so far.", 
            print "Terminating the program."
            print_emails(emails)
            sys.exit()
        
    print_emails(emails)

def print_emails(emails):
    ''' prints all email addresses found '''
    print "Found these email addresses:"
    for email in emails:
        print email

def main(domain):
    ''' main function '''
    protocol = 'http://' # default is HTTP (some sites do not handle HTTPS)
    find_emails(protocol + domain)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='prints emails from a website')
    parser.add_argument('domain', type=str, help='the domain to be searched')
    args = parser.parse_args()
    main(args.domain)
