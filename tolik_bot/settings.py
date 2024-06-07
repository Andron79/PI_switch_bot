import os

DEBUG = os.getenv('DEBUG', '').lower() in ('true', 't', '1', 'yes', 'y')
