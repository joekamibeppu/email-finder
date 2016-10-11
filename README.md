# email-finder
Tool to find email addresses from a domain.

### Dependencies

`find_email_addresses.py` has two dependencies: Requests and Beautiful Soup. Please run the following command to install these packages.

`$ pip install -r requirements.txt`

### Usage

`$ python find_email_addresses.py [domain name]`

### Degree of Completion
In its current state, the program can correctly print all email addresses from jana.com. The tool does not yet work on all websites. In order to work correctly for all domains, the program must handle webpages where the domain does not exactly match the hostname (eg. domain: mit.edu, hostname: web.mit.edu).

To enable better scalability, the program's recursive traversal method should be replaced with an iterative traversal method.
