import uuid
from functools import wraps
import json
from fastapi import FastAPI, Request, Response, HTTPException, File, UploadFile, Form, WebSocket
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import base64
from typing import Any, Callable, Dict, List, Optional, Union
import mimetypes
import io, os
import uvicorn
import asyncio
import watchdog.events
import watchdog.observers
import time
from bs4 import BeautifulSoup

def ttb(text: str) -> str:
    base64_encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    return str(base64_encoded)

class Component:
    def __init__(self, render_func):
        self.render_func = render_func
        self.props = {}
        self.state = {}
        self.effects = []
        self.id = ttb(str(uuid.uuid4()))
        self.css_files = []

    def set_props(self, props):
        self.props = props

    def set_state(self, new_state):
        self.state.update(new_state)
        return self.render()

    def use_effect(self, effect_func, dependencies=None):
        self.effects.append((effect_func, dependencies))

    def render(self):
        return self.render_func(self.props)

    def add_css_file(self, css_file):
        self.css_files.append(self.static_dir+'/'+css_file)

class PyreactApp:
    def __init__(self):
        self.app = None
        self.components = {}
        self.routes = {}
        self.global_state = {}
        self.event_handlers = {}
        self.before_request_funcs = []
        self.after_request_funcs = []
        self.error_handlers = {}
        self.request = None
        self.global_css_files = []
        self.mode = "build"
        self.websocket_clients = set()
        self.static_dir = "static"
        self.static_timestamp = int(time.time())
        self.index_html = self.load_index_html()

    def load_index_html(self):
        with open('index.html', 'r') as file:
            return file.read()

    def component(self, func):
        @wraps(func)
        def wrapper(**props):
            component = Component(func)
            component.set_props(props)
            content = component.render()
            soup = BeautifulSoup(content, 'html.parser')
            
            root_elements = soup.find_all(recursive=False)
            
            if len(root_elements) == 1:
                # Single root element
                root = root_elements[0]
                root['data-pyreact-component'] = func.__name__
                root['data-component-id'] = component.id
                
                # Append style attribute
                existing_style = root.get('style', '')
                root['style'] = f"{existing_style};" if existing_style else ''
                
                return str(soup)
            else:
                # Multiple root elements, wrap in a div
                wrapper = soup.new_tag('div')
                wrapper['data-pyreact-component'] = func.__name__
                wrapper['data-component-id'] = component.id
                wrapper['data-wraper'] = 'true'
                
                # Move all content into the wrapper
                for element in root_elements:
                    wrapper.append(element.extract())
                
                soup.append(wrapper)
                return str(soup)
        
        self.components[func.__name__] = wrapper
        return wrapper

    def route(self, path, methods=None):
        if methods is None:
            methods = ["GET"]

        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                return await func(*args, **kwargs)
            self.routes[path] = {"func": wrapper, "methods": methods}
            return wrapper
        return decorator

    async def render_route(self, path, method, request: Request, **kwargs):
        for route_path, route_data in self.routes.items():
            if self._match_route(path, route_path) and method in route_data["methods"]:
                route_kwargs = self._extract_route_params(path, route_path)
                route_kwargs.update(kwargs)
                route_kwargs['request'] = request
                result = await route_data["func"](**route_kwargs)
                
                if callable(result) and hasattr(result, '__name__'):
                    result = result()

                return result

        error_handler = self.error_handlers.get(404)
        if error_handler:
            return error_handler(request)
        else:
            return HTMLResponse(content="<p>404 - Not Found</p>", status_code=404)

    def _match_route(self, path, route_path):
        path_parts = path.split('/')
        route_parts = route_path.split('/')
        if len(path_parts) != len(route_parts):
            return False
        for path_part, route_part in zip(path_parts, route_parts):
            if route_part.startswith('<') and route_part.endswith('>'):
                continue
            if path_part != route_part:
                return False
        return True

    def _extract_route_params(self, path, route_path):
        params = {}
        path_parts = path.split('/')
        route_parts = route_path.split('/')
        for path_part, route_part in zip(path_parts, route_parts):
            if route_part.startswith('<') and route_part.endswith('>'):
                param_name = route_part[1:-1]
                params[param_name] = path_part
        return params

    def before_request(self, f: Callable[[], Any]):
        self.before_request_funcs.append(f)
        return f

    def after_request(self, f: Callable[[Response], Response]):
        self.after_request_funcs.append(f)
        return f

    def errorhandler(self, code_or_exception):
        def decorator(f):
            self.error_handlers[code_or_exception] = f
            return f
        return decorator

    def add_global_css_file(self, css_file):
        self.global_css_files.append(self.static_dir+'/'+css_file)

    def _get_css_links(self):
        css_links = ''
        for css_file in self.global_css_files:
            with open(css_file, 'r') as file:
                css = file.read()
            css_links += f'<style id="pyreact-style" data-id={self.static_timestamp}>{css}</style>'
        return css_links

    def create_app(self):
        app = FastAPI()
        app.mount("/static", StaticFiles(directory=self.static_dir), name="static")

        @app.middleware("http")
        async def process_request(request: Request, call_next):
            self.request = request
            for func in self.before_request_funcs:
                result = func()
                if isinstance(result, Response):
                    return result

            response = await call_next(request)
            response.headers["X-Framework-Name"] = "Pyreact"

            for func in self.after_request_funcs:
                response = func(response) or response

            return response

        @app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await websocket.accept()
            self.websocket_clients.add(websocket)
            try:
                while True:
                    await websocket.receive_text()
            except:
                self.websocket_clients.remove(websocket)

        @app.post("/api/event")
        async def handle_event(request: Request):
            data = await request.json()
            event_name = data.get('event_name')
            args = data.get('args', [])
            component_id = data.get('component_id')

            if event_name in self.event_handlers:
                result = self.event_handlers[event_name](component_id, *args)
                if isinstance(result, str):
                    return HTMLResponse(content=result)
                elif isinstance(result, dict):
                    return JSONResponse(content=result)
                else:
                    return JSONResponse(content={"result": result, "newState": self.global_state})
            else:
                return JSONResponse(content={"error": "Event handler not found"}, status_code=404)

        @app.post("/api/load-component")
        async def api_load_component(request: Request):
            data = await request.json()
            component_name = data.get('component_name')

            if component_name is None:
                return JSONResponse(content={"error": "component_name is required"}, status_code=400)

            props = data.get('props', {})
            
            if component_name.startswith('/'):
                content = await self.render_route(component_name, "GET", request, **props)
            else:
                content = await self.load_component(component_name, props)

            return HTMLResponse(content=str(content))

        @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
        async def serve(request: Request, path: str = ""):
            try:
                content = await self.render_route(f"/{path}" if path else "/", request.method, request)

                if isinstance(content, (HTMLResponse, JSONResponse, RedirectResponse, FileResponse, StreamingResponse)):
                    return content

                html_content = self.index_html.replace(
                    "<!-- CSS files will be dynamically inserted here -->",
                    self._get_css_links()
                ).replace(
                    "<!-- Content will be dynamically inserted here -->",
                    content
                ).replace(
                    "window.INITIAL_STATE = {};",
                    f"window.INITIAL_STATE = {json.dumps(self.global_state)};"
                )

                return HTMLResponse(content=html_content)
            except Exception as e:
                status_code = getattr(e, 'status_code', 500)
                error_handler = self.error_handlers.get(status_code, self.error_handlers.get(Exception))
                if error_handler:
                    return error_handler(e)
                raise


        @app.post("/api/load-component")
        async def api_load_component(request: Request):
            data = await request.json()
            component_name = data.get('component_name')

            if component_name is None:
                return JSONResponse(content={"error": "component_name is required"}, status_code=400)

            props = data.get('props', {})
            
            if component_name.startswith('/'):
                content = await self.render_route(component_name, "GET", request, **props)
            else:
                content = await self.load_component(component_name, props)

            return HTMLResponse(content=str(content))
        self.app = app
        return app
    async def send_file(self, file_data, file_name=None, content_type=None):
        if isinstance(file_data, str):
            file_data = file_data.encode('utf-8')

        if not content_type:
            content_type = mimetypes.guess_type(file_name)[0] if file_name else 'application/octet-stream'

        headers = {}
        if file_name:
            headers["Content-Disposition"] = f'attachment; filename="{file_name}"'

        return StreamingResponse(
            io.BytesIO(file_data),
            media_type=content_type,
            headers=headers
        )

    async def receive_file(self, file: UploadFile = File(...)):
        contents = await file.read()
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "contents": contents
        }

    def redirect(self, location: str, code: int = 302) -> RedirectResponse:
        return RedirectResponse(url=location, status_code=code)

    def jsonify(self, *args, **kwargs) -> JSONResponse:
        return JSONResponse(content=dict(*args, **kwargs))

    def abort(self, code: int, description: Optional[str] = None):
        error_handler = self.error_handlers.get(code)
        if error_handler:
            return error_handler()
        raise HTTPException(status_code=code, detail=description)

    def event_handler(self, event_name):
        def decorator(func):
            self.event_handlers[event_name] = func
            return func
        return decorator

    async def load_component(self, component_name, props):
        if component_name in self.components:
            component_func = self.components[component_name]
            return component_func(**props)
        else:
            return f"<p>Component '{component_name}' not found</p>"

    def run(self, web, host: str = "127.0.0.1", port: int = 3000, reload: bool = False):
        if not self.app:
            self.create_app()
        
        if self.mode == "build":
            self.run_development(web, host, port, reload)
        else:
            uvicorn.run(web, host=host, port=port)

    def run_development(self, web: str, host: str, port: int, reload: bool):
        class FileChangeHandler(watchdog.events.FileSystemEventHandler):
            def __init__(self, app):
                self.app = app

            def on_modified(self, event):
                if event.src_path.endswith(('.py', '.js', '.css', '.html')):
                    print(f"File changed: {event.src_path}")
                    asyncio.create_task(self.app.reload_clients())

        async def reload_clients(self):
            print("Reloading clients...")
            self.static_timestamp = int(time.time())
            for client in self.websocket_clients:
                try:
                    await client.send_text("reload")
                except Exception as e:
                    print(f"Error reloading client: {e}")
                    self.websocket_clients.remove(client)

        self.reload_clients = reload_clients

        observer = watchdog.observers.Observer()
        handler = FileChangeHandler(self)
        observer.schedule(handler, path='.', recursive=True)
        observer.schedule(handler, path=self.static_dir, recursive=True)
        observer.start()

        uvicorn.run(web, host=host, port=port, reload=reload)

    def set_mode(self, mode: str):
        if mode not in ["build", "use"]:
            raise ValueError("Mode must be either 'build' or 'use'")
        self.mode = mode

    def set_static_dir(self, directory: str):
        self.static_dir = directory

pyreact = PyreactApp()
component = pyreact.component
route = pyreact.route
send_file = pyreact.send_file
receive_file = pyreact.receive_file
throw = HTMLResponse
JSON_Response = JSONResponse
