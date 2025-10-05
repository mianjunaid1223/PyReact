<div align="center">
  <img src="static/PyReact-logo.png" alt="PyReact Logo" width="300"/>
  
  # PyReact Framework
  
  **A Python-based web framework that combines server-side rendering with client-side interactivity**
  
  [![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green.svg)](https://fastapi.tiangolo.com/)
  [![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
  
</div>

---

## 📖 Overview

PyReact is a Python-based web framework that combines server-side rendering with client-side interactivity. It allows for the creation of dynamic web applications using the simplicity of Python, bringing a React-like component architecture to Python web development.

## 📋 Table of Contents

1. [Features](#-features)
2. [Installation](#-installation)
3. [Folder Structure](#-folder-structure)
4. [Quick Start](#-quick-start)
5. [Core Concepts](#-core-concepts)
   - [Components](#components)
   - [Routing](#routing)
   - [State Management](#state-management)
   - [Event Handling](#event-handling)
6. [Example App: Multi-feature Blog](#-example-app-multi-feature-blog)
7. [API Reference](#-api-reference)
8. [Configuration](#-configuration)
9. [Deployment](#-deployment)
10. [Troubleshooting](#-troubleshooting)
11. [Contributing](#-contributing)
12. [License](#-license)

## ✨ Features

- **🧩 Component-Based Architecture**: Create reusable UI components with Python decorators
- **⚡ Server-Side Rendering (SSR)**: Fast initial page loads with server-rendered HTML
- **🔀 Client-Side Routing**: Seamless navigation without full page reloads
- **🔄 Automatic State Management**: Built-in global state management system
- **🎯 Event Handling**: Powerful event system with custom handlers
- **🔌 Middleware & Hooks**: Request/response processing with before/after hooks
- **❌ Error Handling**: Custom error handlers for graceful error management
- **📁 Static File Serving**: Easy static asset management
- **🔥 Hot Reloading**: Instant feedback during development with build mode
- **🌐 API Integration**: RESTful API support with multiple HTTP methods
- **📦 Modular Components**: Import components from separate files for better organization
- **🎨 CSS Management**: Global and component-level CSS support
- **🔌 WebSocket Support**: Real-time communication capabilities
- **📝 Form Handling**: Easy form submission and validation

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Install Dependencies

To use PyReact, you need to install the required dependencies:

```bash
pip install fastapi uvicorn watchdog beautifulsoup4
```

### Clone the Repository

```bash
git clone https://github.com/mianjunaid1223/PyReact.git
cd PyReact
```

### Verify Installation

Run the example app to verify everything is working:

```bash
python app.py
```

Visit `http://127.0.0.1:3000` in your browser to see the PyReact demo.

> **Note**: PyReact is currently a custom framework. Future releases may include pip package distribution.

## 📁 Folder Structure

```
my_pyreact_app/
│
├── app.py                 # Main application file with routes and configuration
├── index.html            # Base HTML template
├── pyreact.py            # Core PyReact framework code
├── static/               # Static assets directory
│   ├── styles.css        # Global styles
│   ├── pyreact.js        # Client-side PyReact code
│   └── PyReact-logo.png  # Logo and other images
└── components/           # Reusable component directory
    ├── __init__.py       # Package initializer
    ├── Header.py         # Example: Header component
    ├── Footer.py         # Example: Footer component
    ├── BlogPost.py       # Example: BlogPost component
    └── image.py          # Example: Image component
```

### Key Files Explained

- **`app.py`**: Entry point of your application. Define routes, components, and app configuration here.
- **`pyreact.py`**: The core framework file containing PyReact classes and methods.
- **`index.html`**: Base HTML template that PyReact uses to render components.
- **`static/`**: Directory for static files (CSS, JavaScript, images, fonts, etc.)
- **`components/`**: Directory containing reusable component definitions.

## 🚀 Quick Start

### Step 1: Create Your First Component

Create a simple component in `app.py`:

```python
from pyreact import pyreact, component, route

@component
def HelloWorld(props):
    name = props.get('name', 'World')
    return f"""
    <div>
        <h1>Hello, {name}!</h1>
        <p>Welcome to PyReact Framework</p>
    </div>
    """
```

### Step 2: Define a Route

Map a URL to your component:

```python
@route("/")
async def home(request):
    return HelloWorld(name="PyReact Developer")
```

### Step 3: Initialize and Run

Set up the PyReact application:

```python
# Create the app instance
app = pyreact.create_app()

# Configure settings
pyreact.set_static_dir("static")
pyreact.add_global_css_file("styles.css")
pyreact.set_mode("build")  # Enable hot reloading

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=3000, reload=True)
```

### Step 4: Run Your App

```bash
python app.py
```

Visit `http://127.0.0.1:3000` in your browser to see your PyReact app in action!

## 💡 Core Concepts

### Components

Components are the building blocks of PyReact applications. They are reusable, isolated pieces of UI that can be composed together.

#### Creating a Component

Use the `@component` decorator to create a component:

```python
from pyreact import component

@component
def Button(props):
    text = props.get('text', 'Click Me')
    color = props.get('color', 'blue')
    return f"""
    <button style="background-color: {color}; padding: 10px 20px;">
        {text}
    </button>
    """
```

#### Using Components

Components can be used within other components:

```python
@component
def App(props):
    return f"""
    <div>
        <h1>My App</h1>
        {Button(text="Submit", color="green")}
        {Button(text="Cancel", color="red")}
    </div>
    """
```

#### Component Props

Props (properties) are passed to components to customize their behavior:

```python
@component
def UserCard(props):
    user = props.get('user', {})
    return f"""
    <div class="user-card">
        <h2>{user.get('name', 'Unknown')}</h2>
        <p>Email: {user.get('email', 'N/A')}</p>
        <p>Role: {user.get('role', 'User')}</p>
    </div>
    """

# Usage
user_data = {"name": "John Doe", "email": "john@example.com", "role": "Admin"}
UserCard(user=user_data)
```

### Routing

PyReact provides a powerful routing system for handling different URLs.

#### Basic Routing

```python
from pyreact import route

@route("/")
async def home(request):
    return "<h1>Home Page</h1>"

@route("/about")
async def about(request):
    return "<h1>About Page</h1>"
```

#### Dynamic Routes

Use route parameters for dynamic URLs:

```python
@route("/user/<user_id>")
async def user_profile(request, user_id):
    return f"<h1>User Profile: {user_id}</h1>"

@route("/post/<int:post_id>")
async def blog_post(request, post_id):
    # post_id is automatically converted to integer
    return f"<h1>Blog Post #{post_id}</h1>"
```

#### HTTP Methods

Support multiple HTTP methods on the same route:

```python
@route("/api/data", methods=["GET", "POST"])
async def api_data(request):
    if request.method == "GET":
        return pyreact.jsonify(data=["item1", "item2"])
    elif request.method == "POST":
        data = await request.json()
        return pyreact.jsonify(status="success", received=data)
```

### State Management

PyReact includes a global state management system for sharing data across components.

#### Global State

```python
from pyreact import pyreact

# Initialize global state
pyreact.global_state['user'] = {"name": "John", "logged_in": True}
pyreact.global_state['posts'] = []

# Access state in routes or components
@route("/profile")
async def profile(request):
    user = pyreact.global_state.get('user', {})
    return f"<h1>Welcome, {user.get('name')}!</h1>"

# Update state
@route("/logout")
async def logout(request):
    pyreact.global_state['user']['logged_in'] = False
    return "<h1>Logged out successfully</h1>"
```

### Event Handling

PyReact provides a powerful event handling system for client-server communication.

#### Server-Side Event Handlers

Define event handlers with the `@pyreact.event_handler` decorator:

```python
@pyreact.event_handler("updateCount")
def update_count(component_id, value):
    current = pyreact.global_state.get('count', 0)
    pyreact.global_state['count'] = current + int(value)
    return {"newCount": pyreact.global_state['count']}
```

#### Client-Side Event Triggering

Trigger events from the client using JavaScript:

```javascript
<button onclick="handleClick()">Increment</button>
<script>
function handleClick() {
    pyreact.triggerEvent('updateCount', 1).then((result) => {
        console.log('New count:', result.newCount);
    });
}
</script>
```

#### Complete Event Example

```python
@component
def Counter(props):
    return """
    <div>
        <h2>Counter: <span id="count">0</span></h2>
        <button onclick="increment()">+1</button>
        <button onclick="decrement()">-1</button>
    </div>
    <script>
    function increment() {
        pyreact.triggerEvent('updateCount', 1).then((result) => {
            document.getElementById('count').textContent = result.newCount;
        });
    }
    function decrement() {
        pyreact.triggerEvent('updateCount', -1).then((result) => {
            document.getElementById('count').textContent = result.newCount;
        });
    }
    </script>
    """

@pyreact.event_handler("updateCount")
def update_count(component_id, value):
    current = pyreact.global_state.get('count', 0)
    pyreact.global_state['count'] = current + int(value)
    return {"newCount": pyreact.global_state['count']}
```

## 📝 Example App: Multi-feature Blog

Let's create a blog application that demonstrates all the features of Pyreact. We'll create the main `app.py` file and several components.

### app.py

```python
from pyreact import pyreact, component, route, send_file, throw
from components.Header import Header
from components.Footer import Footer
from components.BlogPost import BlogPost
from components.CommentSection import CommentSection
from components.NewPostForm import NewPostForm

# Global state for our blog posts and comments
pyreact.global_state['blog_posts'] = [
    {"id": 1, "title": "First Post", "content": "This is our first blog post.", "comments": []},
    {"id": 2, "title": "Second Post", "content": "This is our second blog post.", "comments": []},
]

@component
def App(props):
    return f"""
    {Header(title="My Pyreact Blog")}
    <main id="content">
        {props.get('children', '<p>Welcome to my blog!</p>')}
    </main>
    {Footer()}
    """

@route("/")
async def home(request):
    posts = pyreact.global_state['blog_posts']
    post_list = "".join([f'<li><a href="/post/{post["id"]}" data-pyreact-link>{post["title"]}</a></li>' for post in posts])
    return App(children=f"""
        <h2>Recent Posts</h2>
        <ul>{post_list}</ul>
        <component data-link="/new-post-form" data-props='{{}}'></component>
    """)

@route("/post/<post_id>")
async def blog_post(request, post_id):
    post = next((p for p in pyreact.global_state['blog_posts'] if p['id'] == int(post_id)), None)
    if post:
        return App(children=f"""
            {BlogPost(post=post)}
            {CommentSection(post_id=post['id'])}
        """)
    else:
        return throw(content="<p>404 - Post not found</p>", status_code=404)

@route("/new-post-form")
async def new_post_form(request):
    return NewPostForm()

@route("/api/posts", methods=["GET", "POST"])
async def api_posts(request):
    if request.method == "GET":
        return pyreact.jsonify(posts=pyreact.global_state['blog_posts'])
    elif request.method == "POST":
        data = await request.json()
        new_post = {
            "id": len(pyreact.global_state['blog_posts']) + 1,
            "title": data['title'],
            "content": data['content'],
            "comments": []
        }
        pyreact.global_state['blog_posts'].append(new_post)
        return pyreact.jsonify(status="success", post=new_post)

@pyreact.event_handler("addPost")
def add_post(component_id, title, content):
    new_post = {
        "id": len(pyreact.global_state['blog_posts']) + 1,
        "title": title,
        "content": content,
        "comments": []
    }
    pyreact.global_state['blog_posts'].append(new_post)
    return {"newPost": new_post}

@pyreact.event_handler("addComment")
def add_comment(component_id, post_id, comment):
    post = next((p for p in pyreact.global_state['blog_posts'] if p['id'] == int(post_id)), None)
    if post:
        post['comments'].append(comment)
        return {"updatedComments": post['comments']}
    return {"error": "Post not found"}

@pyreact.before_request
def before_request():
    print("Processing request...")

@pyreact.after_request
def after_request(response):
    print("Request processed.")
    return response

@pyreact.errorhandler(404)
def not_found_error(error):
    return throw(content="<p>404 - Not Found</p>", status_code=404)

app = pyreact.create_app()
pyreact.add_global_css_file("/static/styles.css")

if __name__ == "__main__":
    pyreact.set_mode("build")
    pyreact.set_static_dir("static")
    pyreact.run("app:app", host="127.0.0.1", port=8000, reload=True)
```

### components/Header.py

```python
from pyreact import component

@component
def Header(props):
    return f"""
    <header>
        <h1>{props.get('title', 'My Blog')}</h1>
        <nav>
            <a href="/" data-pyreact-link>Home</a>
        </nav>
    </header>
    """
```

### components/Footer.py

```python
from pyreact import component

@component
def Footer(props):
    return """
    <footer>
        <p>&copy; 2024 My Pyreact Blog</p>
    </footer>
    """
```

### components/BlogPost.py

```python
from pyreact import component

@component
def BlogPost(props):
    post = props['post']
    return f"""
    <article>
        <h2>{post['title']}</h2>
        <p>{post['content']}</p>
    </article>
    """
```

### components/CommentSection.py

```python
from pyreact import component

@component
def CommentSection(props):
    post_id = props['post_id']
    return f"""
    <section id="comments">
        <h3>Comments</h3>
        <ul id="comment-list"></ul>
        <form id="comment-form" onsubmit="return false;">
            <textarea id="comment-text" required></textarea>
            <button onclick="addComment({post_id})">Add Comment</button>
        </form>
    </section>
    <script>
    function addComment(postId) {{
        const commentText = document.getElementById('comment-text').value;
        pyreact.triggerEvent('addComment', postId, commentText).then((result) => {{
            if (result.updatedComments) {{
                const commentList = document.getElementById('comment-list');
                commentList.innerHTML = result.updatedComments.map(comment => `<li>${{comment}}</li>`).join('');
                document.getElementById('comment-text').value = '';
            }}
        }});
    }}
    </script>
    """
```

### components/NewPostForm.py

```python
from pyreact import component

@component
def NewPostForm(props):
    return """
    <form id="new-post-form" onsubmit="return false;">
        <h3>Create New Post</h3>
        <input type="text" id="post-title" placeholder="Title" required>
        <textarea id="post-content" placeholder="Content" required></textarea>
        <button onclick="addPost()">Create Post</button>
    </form>
    <script>
    function addPost() {
        const title = document.getElementById('post-title').value;
        const content = document.getElementById('post-content').value;
        pyreact.triggerEvent('addPost', title, content).then((result) => {
            if (result.newPost) {
                alert('New post created!');
                document.getElementById('post-title').value = '';
                document.getElementById('post-content').value = '';
            }
        });
    }
    </script>
    """
```

## 📚 API Reference

### PyReact Core Methods

#### `pyreact.create_app()`

Creates and returns a FastAPI application instance.

```python
app = pyreact.create_app()
```

#### `pyreact.set_mode(mode)`

Sets the application mode. Use `"build"` for development with hot reloading.

```python
pyreact.set_mode("build")  # Development mode with hot reloading
pyreact.set_mode("use")    # Production mode
```

#### `pyreact.set_static_dir(directory)`

Sets the directory for static files.

```python
pyreact.set_static_dir("static")
```

#### `pyreact.add_global_css_file(css_file)`

Adds a global CSS file to all pages.

```python
pyreact.add_global_css_file("styles.css")
pyreact.add_global_css_file("/static/theme.css")
```

#### `pyreact.jsonify(**kwargs)`

Returns a JSON response.

```python
@route("/api/data")
async def get_data(request):
    return pyreact.jsonify(
        status="success",
        data={"key": "value"}
    )
```

#### `pyreact.send_file(file_data, file_name, content_type)`

Sends a file as a response.

```python
@route("/download")
async def download(request):
    with open("document.pdf", "rb") as f:
        data = f.read()
    return await pyreact.send_file(data, "document.pdf", "application/pdf")
```

### Decorators

#### `@component`

Defines a reusable component.

```python
from pyreact import component

@component
def MyComponent(props):
    return "<div>Component content</div>"
```

#### `@route(path, methods=["GET"])`

Defines a route handler.

```python
from pyreact import route

@route("/", methods=["GET"])
async def home(request):
    return "<h1>Home</h1>"

@route("/api/submit", methods=["POST", "PUT"])
async def submit(request):
    data = await request.json()
    return pyreact.jsonify(received=data)
```

#### `@pyreact.event_handler(event_name)`

Defines a server-side event handler.

```python
@pyreact.event_handler("myEvent")
def handle_my_event(component_id, *args):
    # Process event
    return {"result": "success"}
```

#### `@pyreact.before_request`

Defines a function to run before each request.

```python
@pyreact.before_request
def before_request():
    print("Request started")
    # Add authentication, logging, etc.
```

#### `@pyreact.after_request`

Defines a function to run after each request.

```python
@pyreact.after_request
def after_request(response):
    print("Request completed")
    # Modify response headers, add logging, etc.
    return response
```

#### `@pyreact.errorhandler(code_or_exception)`

Defines a custom error handler.

```python
@pyreact.errorhandler(404)
def not_found(error):
    return "<h1>404 - Page Not Found</h1>", 404

@pyreact.errorhandler(500)
def server_error(error):
    return "<h1>500 - Internal Server Error</h1>", 500
```

### Dynamic Component Loading

Use `<component>` tags to dynamically load components:

```python
@component
def Parent(props):
    return """
    <div>
        <h1>Parent Component</h1>
        <component data-link="/child-component" data-props='{"name": "John"}'></component>
    </div>
    """

@route("/child-component")
async def child_component(request):
    return ChildComponent(name=request.query_params.get('name', 'Guest'))
```

## ⚙️ Configuration

### Application Settings

Configure your PyReact application in `app.py`:

```python
from pyreact import pyreact
import uvicorn

# Create app instance
app = pyreact.create_app()

# Set static directory
pyreact.set_static_dir("static")

# Add global CSS files
pyreact.add_global_css_file("styles.css")
pyreact.add_global_css_file("theme.css")

# Set development/production mode
pyreact.set_mode("build")  # Development with hot reload
# pyreact.set_mode("use")  # Production

# Initialize global state
pyreact.global_state['app_name'] = "My PyReact App"
pyreact.global_state['version'] = "1.0.0"

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=3000,
        reload=True,
        log_level="info"
    )
```

### Environment-Specific Configuration

```python
import os

# Determine environment
ENV = os.getenv("ENVIRONMENT", "development")

if ENV == "production":
    pyreact.set_mode("use")
    HOST = "0.0.0.0"
    PORT = 8080
    RELOAD = False
else:
    pyreact.set_mode("build")
    HOST = "127.0.0.1"
    PORT = 3000
    RELOAD = True

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host=HOST, port=PORT, reload=RELOAD)
```

### Custom Index HTML

Modify `index.html` to customize the base template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My PyReact App</title>
    <!-- Global CSS files will be inserted here -->
</head>
<body>
    <div id="root">
        <!-- Components will be rendered here -->
    </div>
    <script>
        window.INITIAL_STATE = {};
    </script>
    <script src="/static/pyreact.js"></script>
</body>
</html>
```

## 🚢 Deployment

### Development Server

For development with hot reloading:

```bash
python app.py
```

Or using uvicorn directly:

```bash
uvicorn app:app --host 127.0.0.1 --port 3000 --reload
```

### Production Deployment

#### 1. Using Uvicorn

```bash
# Install production server
pip install uvicorn[standard]

# Run with multiple workers
uvicorn app:app --host 0.0.0.0 --port 8080 --workers 4
```

#### 2. Using Gunicorn with Uvicorn Workers

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080
```

#### 3. Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8080

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]
```

Build and run:

```bash
docker build -t pyreact-app .
docker run -p 8080:8080 pyreact-app
```

#### 4. Using Nginx as Reverse Proxy

Nginx configuration (`/etc/nginx/sites-available/pyreact`):

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /path/to/your/app/static/;
    }

    location /ws {
        proxy_pass http://127.0.0.1:8080/ws;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue: Module not found errors

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**: Install required dependencies
```bash
pip install fastapi uvicorn watchdog beautifulsoup4
```

#### Issue: Port already in use

**Problem**: `OSError: [Errno 48] Address already in use`

**Solution**: Kill the process using the port or use a different port
```bash
# Find process using port 3000
lsof -ti:3000 | xargs kill -9

# Or change the port in app.py
uvicorn.run("app:app", host="127.0.0.1", port=3001, reload=True)
```

#### Issue: Hot reload not working

**Problem**: Changes to files don't trigger automatic reload

**Solution**: Ensure build mode is enabled
```python
pyreact.set_mode("build")
```

#### Issue: Static files not loading

**Problem**: CSS/JS files return 404 errors

**Solution**: Verify static directory configuration
```python
# In app.py
pyreact.set_static_dir("static")
pyreact.add_global_css_file("styles.css")  # Don't include "static/" prefix
```

#### Issue: Components not rendering

**Problem**: Components appear as empty divs

**Solution**: Check component decorator and return statement
```python
# Correct
@component
def MyComponent(props):
    return "<div>Content</div>"

# Incorrect - missing @component decorator
def MyComponent(props):
    return "<div>Content</div>"
```

#### Issue: WebSocket connection fails

**Problem**: Real-time features not working

**Solution**: Ensure WebSocket route is accessible
```python
# Check that your server allows WebSocket connections
# If behind a proxy, configure WebSocket forwarding
```

### Debug Mode

Enable detailed logging for debugging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=3000, reload=True, log_level="debug")
```

## 🤝 Contributing

We welcome contributions to PyReact! Here's how you can help:

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in [GitHub Issues](https://github.com/mianjunaid1223/PyReact/issues)
2. If not, create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (Python version, OS, etc.)

### Contributing Code

1. **Fork the repository**
   ```bash
   git clone https://github.com/mianjunaid1223/PyReact.git
   cd PyReact
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Write clean, documented code
   - Follow existing code style
   - Add tests if applicable

4. **Test your changes**
   ```bash
   python app.py
   # Test the functionality
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "Add: your feature description"
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Go to the repository on GitHub
   - Click "New Pull Request"
   - Describe your changes

### Development Guidelines

- Follow PEP 8 style guidelines
- Write clear, descriptive commit messages
- Document new features in the README
- Keep changes focused and atomic
- Test thoroughly before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Inspired by React's component architecture
- Uses [Uvicorn](https://www.uvicorn.org/) as the ASGI server
- Styling with [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)

## 📞 Support

- **Documentation**: [GitHub Repository](https://github.com/mianjunaid1223/PyReact)
- **Issues**: [GitHub Issues](https://github.com/mianjunaid1223/PyReact/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mianjunaid1223/PyReact/discussions)

---

<div align="center">
  Made with ❤️ by the PyReact Team
  
  **[⭐ Star us on GitHub](https://github.com/mianjunaid1223/PyReact)**
</div>
