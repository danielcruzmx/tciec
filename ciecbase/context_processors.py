from django.conf import settings

def from_settings(request):
    return {
        'ENV_LOGO': settings.ENV_LOGO,
    }