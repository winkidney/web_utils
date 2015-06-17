# coding: utf-8
from django.http import HttpResponseBadRequest


class RestMixin(object):
    _methods = {
        "GET": "get",
        "POST": "post",
        "PUT": "put",
        "DELETE": "delete",
    }

    def __init__(self, decorators=None):
        decorators_seq = []

        if isinstance(decorators, (list, tuple)):
            for decorator in decorators:
                if not callable(decorator):
                    raise TypeError("Decorators must be callable: except callable, got %s" % decorator)
                decorators_seq.append(decorator)
        elif callable(decorators):
            decorators_seq.append(decorators)

        self.decorators = tuple(decorators_seq)

    def call(self, function, *args, **kwargs):
        for decorator in self.decorators:
                function = decorator(function)
        return function(self.request, *args, **kwargs)

    def __call__(self, request, *args, **kwargs):
        """
        :param request: django http request object
        :type request: django.http.request.HttpRequest
        :return: HttpResponse
        """
        self.request = request
        view_func_name = self._methods.get(request.method, None)
        if view_func_name is not None:
            return self.call(getattr(self, view_func_name), *args, **kwargs)
        else:
            return self.raise_400()

    @staticmethod
    def raise_400():
            return HttpResponseBadRequest("Method not implement.")

    def get(self, request, *args, **kwargs):
        return self.raise_400()

    def post(self, request, *args, **kwargs):
        return self.raise_400()

    def put(self, request, *args, **kwargs):
        return self.raise_400()

    def delete(self, request, *args, **kwargs):
        return self.raise_400()

    def render(self, template_name, context_dict=None, use_context=True, **kwargs):
        if use_context:
            return render_to_response(template_name, context_dict, context_instance=RequestContext(self.request), **kwargs)
        else:
            return render_to_response(template_name, context_dict, **kwargs)
