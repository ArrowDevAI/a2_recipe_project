import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_project.settings')

print(f"Using settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

application = get_wsgi_application()
