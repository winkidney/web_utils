# coding: utf-8
from pyramid import threadlocal


def get_route_from_request(request):
    """
    :type request: pyramid.request.Request
    """

    return get_route_from_registry(request.registry)


def get_route_from_registry(registry=None):
    """
    Return route's names from given registry, if registry is None,
     try `pyramid.threadloacl` to get routes.
    :type registry: pyramid.registry
    """
    route_names = []
    if registry is None:
        registry = threadlocal.get_current_registry()
    routes = registry.introspector.get_category('routes')
    for route in routes:
        route_name = route['introspectable']['name']
        if not route_name.startswith('__'):
            route_names.append(route_name)
    return route_names


class BaseHandler(object):

    def __init__(self, request):
        self.request = request


class ListBaseHandler(BaseHandler):

    def __init__(self, request):
        """
        :type request: pyramid.request.Request
        """
        super(ListBaseHandler, self).__init__(request)
        self.page = _safe_get_int_arg(self.request.GET.get('page'), 1)
        self.limit = _safe_get_int_arg(self.request.GET.get("limit"), 30, nmin=1, nmax=50)
        self.start = (self.page-1)*self.limit
        self.end = self.page*self.limit