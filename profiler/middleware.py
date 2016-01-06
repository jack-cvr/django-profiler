try:
    import cProfile as profile
except ImportError:
    import profile

try:
    from cStringIO import StringIO
except:
    from io import StringIO

import pstats

from django.conf import settings
from django.http import QueryDict
from django.utils.html import linebreaks


class ProfilerMiddleware(object):

    KWARGS = ('prof', 'sort', 'stats', 'callers', 'callees')

    def process_request(self, request):
        if 'prof' in request.GET:
            request.ORIGINAL_GET = request.GET
            params = QueryDict('', mutable=True)
            params.update(request.GET)
            for key in self.KWARGS:
                if key in params:
                    del params[key]
            request.GET = QueryDict(params.urlencode())
            request.profiler = profile.Profile()
            request.profiler.enable()

    def process_response(self, request, response):
        if hasattr(request, 'profiler'):
            request.profiler.create_stats()
            io = StringIO()

            sort = request.ORIGINAL_GET.get('sort', 'cumulative')
            stats_args = []
            for arg in request.ORIGINAL_GET.get('stats', '').split(','):
                if arg.replace('.', '').isdigit():
                    arg = float(arg) if '.' in arg else int(arg)
                stats_args.append(arg)

            stats = (
                pstats.Stats(request.profiler, stream=io).sort_stats(sort))
            if 'callers' in request.ORIGINAL_GET:
                stats.print_callers(*stats_args)
            elif 'callees' in request.ORIGINAL_GET:
                stats.print_callees(*stats_args)
            else:
                stats.print_stats(*stats_args)

            lines = []
            for line in linebreaks(io.getvalue()).split('<br />'):
                lines.append('<pre>{0}</pre>'.format(line))
            response.content = '''
                <style>
                pre:nth-child(even) {{ background: rgb(242, 242, 242); }}
                </style>
                {body}
            '''.format(body=''.join(lines))
        return response
