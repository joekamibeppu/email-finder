#!/usr/bin/env python
"""
Email scanner: prints all email addresses found on a domain's website.
Joe Kamibeppu | 10 Oct 2016
Dependencies:
    Beautiful Soup (pip install beautifulsoup4)
    Requests (pip install requests)
Usage:
    python find_email_addresses.py [domain name]
Needs work:
    - This program does not yet handle all websites. It works correctly
    for the 'jana.com' domain.
    - This program recursively traverses through webpages. In order for this
    program to scale, the recursive method should be replaced with an
    iterative method.
    - Line 27: refine email regex pattern
"""

import re
import argparse
from urlparse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup, SoupStrainer

def find_emails(url, emails, visited):
    ''' finds email addresses by recursively traversing through pages '''
    #TODO: refine email regex pattern
    email_pattern = r'\w[\w._-]*@[\w._-]*' + visited[0] # contains domain name
    response = requests.get(url)
    emails += re.findall(email_pattern, response.text)
    visited.append(url)

    for link in BeautifulSoup(response.text, 'html.parser',
                              parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            new_url = urljoin(url, link['href'])
            if urlparse(new_url).hostname == urlparse(url).hostname:
                if new_url not in visited:
                    emails += find_emails(new_url, emails, visited)

    return emails

def print_emails(emails):
    ''' prints all email addresses found '''
    print "Found these email addresses:"
    emails = set(emails)
    for email in emails:
        print email

def main(domain):
    ''' main function '''
    emails = []
    visited = [domain]     # preserve domain in first index
    prefix = 'http://www.' # default is HTTP (some sites do not handle HTTPS)
    emails = find_emails(prefix + args.domain, emails, visited)
    print_emails(emails)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='prints emails from a website')
    parser.add_argument('domain', type=str, help='the domain to be searched')
    args = parser.parse_args()
    main(args.domain)
