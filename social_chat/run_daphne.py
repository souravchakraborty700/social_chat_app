# import os
# import django
# from daphne.cli import CommandLineInterface

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_chat.settings')  # Ensure this matches your project structure

# # Initialize Django
# django.setup()

# CommandLineInterface.entrypoint()
import os
import django
from daphne.cli import CommandLineInterface

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_chat.settings')

# Initialize Django
django.setup()

# Use the PORT environment variable provided by Heroku
port = os.environ.get('PORT', '8000')

# Correct way to call the entrypoint
CommandLineInterface().run(["daphne", "-b", "0.0.0.0", "-p", port, "social_chat.asgi:application"])


