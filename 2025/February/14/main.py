#!/usr/local/bin/python3
from email.utils import parseaddr as validate1 # from python
from email_validator import validate_email as validate2 # https://pypi.org/project/email-validator/
from validate_email import validate_email as validate3 # https://pypi.org/project/validate_email/
from validators import email as validate4 # https://pypi.org/project/validators/

flag = 'ictf{REDACTED}'

email = input('Email: ')

if validate1(email) == ('', ''):
    print("bad")
    exit()

try:
    validate2(email, check_deliverability=False) 
except Exception as e:
    print("bad")
    exit()

if not validate3(email):
    print("bad")
    exit()

if not validate4(email):
    print("bad")
    exit()

exec(email)
