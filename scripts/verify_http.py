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
    if os.environ.get('RUN_BROWSER_TESTS') == 'true':
        from playwright.sync_api import sync_playwright, expect
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            try:
                for width in [1440, 390]:
                    page = browser.new_page(viewport={'width': width, 'height': 900})
                    errors = []
                    page.on('pageerror', lambda error: errors.append(str(error)))
                    def open_dashboard(route, heading):
                        response = page.goto(base + route)
                        assert response.status == 200, route
                        expect(page.get_by_role('heading', name=heading, exact=True)).to_be_visible()
                        if width < 992:
                            page.locator('.navbar-toggler').click()
                            expect(page.locator('.navbar-collapse')).to_be_visible()
                    for area, links in [
                        ('Student', [('Home', 'Home'), ('Catalog', 'Catalog'), ('Calendar', 'Calendar')]),
                        ('Admin', [('Major', 'Majors'), ('Course', 'Courses'), ('Student', 'Students')]),
                    ]:
                        for label, controller in links:
                            open_dashboard('/' + area + '/Dashboard/Index', area + ' Dashboard')
                            page.get_by_role('link', name=label, exact=True).click()
                            expect(page.locator('body')).to_contain_text(
                                f'{area} Area - {controller} Controller - Index Action')
                    open_dashboard('/', 'Student Dashboard')
                    page.get_by_role('link', name='Admin', exact=True).click()
                    expect(page.get_by_role('heading', name='Admin Dashboard', exact=True)).to_be_visible()
                    if width < 992:
                        page.locator('.navbar-toggler').click()
                    page.get_by_role('link', name='View Site', exact=True).click()
                    expect(page.get_by_role('heading', name='Student Dashboard', exact=True)).to_be_visible()
                    assert not errors, errors
                    page.close()
                    print(f'PASS: Chromium navigation and responsive menu at {width}px.')
            finally:
                browser.close()
finally:
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
