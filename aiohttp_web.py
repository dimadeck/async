
import jinja2

import aiohttp_jinja2
from aiohttp import web
from aiohttp_views import index


async def init_app():

    app = web.Application()
    app['websockets'] = {}
    app.on_shutdown.append(shutdown)
    aiohttp_jinja2.setup(
        app, loader=jinja2.PackageLoader('view', 'templates'))
    app.router.add_get('/', index)
    return app


async def shutdown(app):
    for ws in app['websockets'].values():
        await ws.close()
    app['websockets'].clear()


def main():
    app = init_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
