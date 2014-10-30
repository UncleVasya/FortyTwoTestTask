import json
from django.http import HttpResponse


def render_to_json_response(context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)


class AjaxableUpdateMixin(object):
    def form_invalid(self, form):
        response = super(AjaxableUpdateMixin, self).form_invalid(form)
        if self.request.is_ajax():
            data = {
                'errors': form.errors
            }
            return render_to_json_response(data, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableUpdateMixin, self).form_valid(form)
        if self.request.is_ajax():
            return render_to_json_response(None)
        else:
            return response
