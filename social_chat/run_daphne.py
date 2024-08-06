import os
import django
from daphne.cli import CommandLineInterface

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_chat.settings')  # Ensure this matches your project structure

# Initialize Django
django.setup()

CommandLineInterface.entrypoint()
