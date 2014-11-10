import json
from django.core import serializers
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, render_to_response
from django.template.loader import get_template, render_to_string


def render_to_json_response(context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)


class AjaxableResponseMixin(object):
    def render_to_response(self, context):
        if self.request.is_ajax():
            context['csrf_token'] = get_token(self.request)
            return render_to_json_response({
                'table': render_to_string('requestlog/requests_table_body.html', context)
            })
        else:
            return super(AjaxableResponseMixin, self).render_to_response(context)
