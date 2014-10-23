from django.utils.timezone import now
from apps.requestlog.models import RequestLog


class RequestLogMiddleware(object):
    current_request = None

    def process_request(self, request):
        self.current_request = RequestLog.objects.create(
            path=request.path,
            method=request.method,
            query=request.META['QUERY_STRING'],
            address=request.get_host(),
            time_start=now(),
            time_end=now(),
            response_code=0,
        )

    def process_response(self, request, response):
        self.current_request.response_code = response.status_code
        self.current_request.time_end = now()
        self.current_request.save()

        # update html with latest response_code if needed
        # (if we have placeholder for it)
        content = response.content.replace('%response_code%',
                                           str(response.status_code))
        response.content = content

        return response