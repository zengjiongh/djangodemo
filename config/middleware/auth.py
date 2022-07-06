from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ##寻找URL
        if request.path_info in ["/login/", "/image/code/"]:
            return

        info = request.session.get('info')
        if info:
            return
        return redirect('/login/')
