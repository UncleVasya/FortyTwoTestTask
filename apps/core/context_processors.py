from django.conf import settings


def settings_adder_processor(request):
    return {'settings': settings}
