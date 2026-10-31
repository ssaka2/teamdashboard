"""Verify the published MVC app, including routes and local static assets."""
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

published = Path(sys.argv[1]).resolve()
with socket.socket() as sock:
    sock.bind(('127.0.0.1', 0))
    port = sock.getsockname()[1]
base = f'http://127.0.0.1:{port}'
env = dict(os.environ, ASPNETCORE_ENVIRONMENT='Production', ASPNETCORE_URLS=base)
proc = subprocess.Popen(['dotnet', str(published / 'Group3Blackboard.dll')], cwd=published, env=env)
def read(route):
    with urlopen(base + route, timeout=5) as response:
        assert response.status == 200, route
        return response.read().decode()
try:
    for attempt in range(60):
        if proc.poll() is not None:
            raise RuntimeError(f'Application exited: {proc.returncode}')
        try:
            read('/')
            break
        except (URLError, TimeoutError):
            time.sleep(0.5)
    else:
        raise RuntimeError('Application did not become ready')
    for route, expected in [('/', 'Student Dashboard'), ('/Student/Dashboard/Index', 'Student Dashboard'), ('/Admin/Dashboard/Index', 'Admin Dashboard')]:
        assert expected in read(route), route
    for area, controllers in [('Student', ['Home', 'Catalog', 'Calendar']), ('Admin', ['Majors', 'Courses', 'Students'])]:
        for controller in controllers:
            route = f'/{area}/{controller}/Index'
            assert read(route) == f'{area} Area - {controller} Controller - Index Action', route
    for route in ['/lib/bootstrap/css/bootstrap.min.css', '/lib/bootstrap/js/bootstrap.bundle.min.js', '/css/site.css']:
        assert len(read(route)) > 100, route
    try:
        read('/route-that-does-not-exist')
        raise AssertionError('Missing route returned success')
    except HTTPError as error:
        assert error.code == 404, error.code
    print('PASS: 9 page routes, 3 static assets, and missing-route handling in Production.')
finally:
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
