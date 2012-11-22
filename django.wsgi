import sys
import site
import os

STAGE = False

vepath = '/var/www/blog/venv/lib/python2.7/site-packages'

prev_path = list(sys.path)

site.addsitedir(vepath)

sys.path.append('/var/www/blog/blog')

new_sys_path = [p for p in sys.path if p not in prev_path]
for item in new_sys_path:
        sys.path.remove(item)
sys.path[:0] = new_sys_path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "./")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))


from django.core.handlers.wsgi import WSGIHandler
os.environ["DJANGO_SETTINGS_MODULE"] = 'settings'
application = WSGIHandler()
