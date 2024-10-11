# Pyreact Framework

Pyreact is a Python-based web framework that combines server-side rendering with client-side interactivity. It allows for the creation of dynamic web applications using the simplicity of Python.

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
3. [Folder Structure](#folder-structure)
4. [Quick Start](#quick-start)
5. [Example App: Multi-feature Blog](#example-app-multi-feature-blog)
6. [Detailed Feature Usage](#detailed-feature-usage)

## Features

- Component-based architecture
- Server-side rendering
- Client-side routingPyreact Framework

Pyreact is a lightweight Python-based web framework that seamlessly blends server-side rendering with client-side interactivity. Designed for simplicity and efficiency, Pyreact empowers developers to build dynamic and responsive web applications using Python.

Table of Contents

1. Features


2. Prerequisites


3. Installation


4. Folder Structure


5. Quick Start


6. Example App: Multi-feature Blog


7. Detailed Feature Usage


8. Contributing


9. License



Features

Component-Based Architecture: Create reusable UI components with ease.

Server-Side Rendering (SSR): Enhance SEO and initial load times with SSR.

Client-Side Routing: Navigate between pages without full page reloads.

Automatic State Management: Manage global and component-specific state effortlessly.

Event Handling: Handle user interactions and events seamlessly.

Middleware and Hooks: Execute custom logic before and after requests.

Error Handling: Customize responses for different error scenarios.

Static File Serving: Serve CSS, JavaScript, images, and other static assets.

Build Mode with Hot Reloading: Enjoy rapid development with automatic page refreshes on code changes.

API Integration: Create RESTful API endpoints easily.

Component Importing: Organize components in separate files for better maintainability.


Prerequisites

Before getting started with Pyreact, ensure you have the following installed on your system:

Python 3.7 or higher: Download Python

pip: Python package installer (comes bundled with Python)

Git (optional, for cloning the repository): Download Git


Installation

1. Clone the Repository

git clone https://github.com/yourusername/pyreact.git
cd pyreact


2. Install Required Libraries

Pyreact relies on several Python libraries. Install them using pip:

pip install fastapi uvicorn watchdog beautifulsoup4

> Note: Since Pyreact is a custom framework, you may need to package and distribute it separately if you're planning to use it across multiple projects.





Folder Structure

Organize your Pyreact application with a clear and intuitive folder structure. Here's a recommended setup:

my_pyreact_app/
│
├── app.py                # Main application file
├── index.html            # Entry point HTML file
├── pyreact.py            # Pyreact framework module
├── static/               # Static assets
│   ├── styles.css        # CSS styles
│   └── scripts.js        # Client-side JavaScript
└── components/           # Reusable components
    ├── Header.py
    ├── Footer.py
    ├── BlogPost.py
    ├── CommentSection.py
    └── NewPostForm.py

Quick Start

Follow these steps to create and run your first Pyreact application.

1. Set Up the Project Directory

Create a new directory for your project and navigate into it:

mkdir my_pyreact_app
cd my_pyreact_app

2. Create the Folder Structure

Set up the necessary folders and files:

mkdir static components
touch app.py index.html pyreact.py static/styles.css static/scripts.js

3. Create the index.html File

Add the following content to index.html:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pyreact App</title>
    <!-- CSS files will be dynamically inserted here -->
</head>
<body>
    <div id="root">
        <!-- Content will be dynamically inserted here -->
    </div>
    <script>
        window.INITIAL_STATE = {};
        // Your frontend JavaScript here
    </script>
    <script src="/static/scripts.js"></script>
</body>
</html>

4. Create the Main Application File (app.py)

Add the following content to app.py:

from pyreact import pyreact, component, route
from components.Header import Header
from components.Footer import Footer

@component
def App(props):
    return f"""
    {Header(title="My Pyreact App")}
    <main>{props.get('children', 'Welcome to Pyreact!')}</main>
    {Footer()}
    """

@route("/")
async def home(request):
    return App(children="<h1>Hello, Pyreact!</h1>")

app = pyreact.create_app()

if _name_ == "_main_":
    pyreact.set_mode("build")  # or "use" for production
    pyreact.run(host="127.0.0.1", port=8000, reload=True)

5. Create Components

components/Header.py

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

components/Footer.py

from pyreact import component

@component
def Footer(props):
    return """
    <footer>
        <p>&copy; 2024 My Pyreact App</p>
    </footer>
    """

6. Run the Application

Start your Pyreact application by running:

python app.py

Open your browser and navigate to http://127.0.0.1:8000 to see your Pyreact app in action!

Example App: Multi-feature Blog

To demonstrate the full capabilities of Pyreact, let's build a feature-rich blog application. This example showcases component-based architecture, server-side rendering, client-side routing, state management, event handling, and more.

1. Project Structure

my_pyreact_app/
│
├── app.py
├── index.html
├── pyreact.py
├── static/
│   ├── styles.css
│   └── scripts.js
└── components/
    ├── Header.py
    ├── Footer.py
    ├── BlogPost.py
    ├── CommentSection.py
    └── NewPostForm.py

2. Main Application File (app.py)

from pyreact import pyreact, component, route, send_file, throw
from components.Header import Header
from components.Footer import Footer
from components.BlogPost import BlogPost
from components.CommentSection import CommentSection
from components.NewPostForm import NewPostForm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(_name_)

# Initialize global state
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
    logger.info(f"New post added: {title}")
    return {"newPost": new_post}

@pyreact.event_handler("addComment")
def add_comment(component_id, post_id, comment):
    post = next((p for p in pyreact.global_state['blog_posts'] if p['id'] == int(post_id)), None)
    if post:
        post['comments'].append(comment)
        logger.info(f"New comment added to post {post_id}: {comment}")
        return {"updatedComments": post['comments']}
    return {"error": "Post not found"}

@pyreact.before_request
def before_request():
    logger.info("Processing a new request...")

@pyreact.after_request
def after_request(response):
    logger.info("Request processed.")
    return response

@pyreact.errorhandler(404)
def not_found_error(error):
    return throw(content="<p>404 - Not Found</p>", status_code=404)

app = pyreact.create_app()
pyreact.add_global_css_file("/static/styles.css")

if _name_ == "_main_":
    pyreact.set_mode("build")  # or "use" for production
    pyreact.set_static_dir("static")
    pyreact.run(host="127.0.0.1", port=8000, reload=True)

3. Component Definitions

components/Header.py

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

components/Footer.py

from pyreact import component

@component
def Footer(props):
    return """
    <footer>
        <p>&copy; 2024 My Pyreact Blog</p>
    </footer>
    """

components/BlogPost.py

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

components/CommentSection.py

from pyreact import component

@component
def CommentSection(props):
    post_id = props['post_id']
    return f"""
    <section id="comments">
        <h3>Comments</h3>
        <ul id="comment-list"></ul>
        <form id="comment-form" onsubmit="return false;">
            <textarea id="comment-text" required placeholder="Add a comment..."></textarea>
            <button onclick="addComment({post_id})">Add Comment</button>
        </form>
    </section>
    <script>
    async function addComment(postId) {{
        const commentText = document.getElementById('comment-text').value;
        if (!commentText.trim()) {{
            alert('Comment cannot be empty.');
            return;
        }}
        const result = await pyreact.triggerEvent('addComment', postId, commentText);
        if (result.updatedComments) {{
            const commentList = document.getElementById('comment-list');
            commentList.innerHTML = result.updatedComments.map(comment => <li>${{comment}}</li>).join('');
            document.getElementById('comment-text').value = '';
        }} else if (result.error) {{
            alert(result.error);
        }}
    }}
    </script>
    """

components/NewPostForm.py

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
    async function addPost() {{
        const title = document.getElementById('post-title').value;
        const content = document.getElementById('post-content').value;
        if (!title.trim() || !content.trim()) {{
            alert('Title and content cannot be empty.');
            return;
        }}
        const result = await pyreact.triggerEvent('addPost', title, content);
        if (result.newPost) {{
            alert('New post created!');
            document.getElementById('post-title').value = '';
            document.getElementById('post-content').value = '';
            // Optionally, refresh the post list or navigate to the new post
            window.location.href = /post/${{result.newPost.id}};
        }} else {{
            alert('Error creating post.');
        }}
    }}
    </script>
    """

4. Static Assets

static/styles.css

body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}

header, footer {
    background-color: #333;
    color: white;
    padding: 1em;
}

header h1, footer p {
    margin: 0;
}

nav a {
    color: white;
    margin-right: 1em;
    text-decoration: none;
}

main {
    padding: 2em;
}

form {
    margin-top: 1em;
}

input, textarea {
    width: 100%;
    padding: 0.5em;
    margin-bottom: 1em;
}

button {
    padding: 0.5em 1em;
}

static/scripts.js

class Pyreact {
    constructor() {
        this.state = window.INITIAL_STATE || {};
        this.components = {};
        this.eventListeners = {};
        this.observer = new MutationObserver(this.handleMutations.bind(this));
        this.initialize();
    }

    initialize() {
        document.addEventListener('DOMContentLoaded', () => {
            this.initializeComponents();
            this.setupRouting();
            this.setupWebSocket();
            this.observeDOM();
        });
    }

    initializeComponents() {
        const componentElements = document.querySelectorAll('[data-pyreact-component]');
        componentElements.forEach(element => {
            const componentName = element.getAttribute('data-pyreact-component');
            this.initializeComponent(componentName, element);
        });
        this.loadCustomComponents();
    }

    retriggerCSS() {
        const links = document.querySelectorAll('link[rel="stylesheet"], style');
        links.forEach(link => {
            if (link.tagName === 'LINK') {
                const clonedLink = link.cloneNode();
                const href = link.getAttribute('href');
                clonedLink.href = ${href.split('?')[0]}?v=${Date.now()};
                link.parentNode.replaceChild(clonedLink, link);
            } else if (link.tagName === 'STYLE') {
                const clonedStyle = document.createElement('style');
                clonedStyle.textContent = link.textContent;
                link.parentNode.replaceChild(clonedStyle, link);
            }
        });
    }

    loadCustomComponents() {
        const componentTags = document.querySelectorAll('component');
        componentTags.forEach(this.loadComponent.bind(this));
    }

    initializeComponent(name, element) {
        if (!this.components[name]) {
            this.components[name] = {
                elements: [element],
                state: this.state[name] || {},
                id: element.getAttribute('data-component-id')
            };
        } else {
            this.components[name].elements.push(element);
        }
        this.setupComponentEventListeners(element);
    }

    setupComponentEventListeners(element) {
        const events = ['click', 'input', 'change', 'submit'];
        events.forEach(eventType => {
            const eventElements = element.querySelectorAll([data-event="${eventType}"]);
            eventElements.forEach(el => {
                const handlerName = el.getAttribute(data-${eventType}-handler);
                if (handlerName) {
                    el.addEventListener(eventType, async (event) => {
                        event.preventDefault();
                        await this.triggerEvent(handlerName, event);
                    });
                }
            });
        });
    }

    observeDOM() {
        const config = { attributes: true, childList: true, subtree: true, attributeFilter: ['data-link', 'data-props', 'data-replace', 'data-event-click', 'data-event-input', 'data-event-change', 'data-event-submit'] };
        this.observer.observe(document.body, config);
    }

    handleMutations(mutations) {
        mutations.forEach(mutation => {
            if (mutation.type === 'attributes') {
                this.handleAttributeChange(mutation.target, mutation.attributeName);
            } else if (mutation.type === 'childList') {
                mutation.addedNodes.forEach(node => {
                    if (node.nodeType === Node.ELEMENT_NODE) {
                        if (node.tagName.toLowerCase() === 'component') {
                            this.loadComponent(node);
                        }
                        const components = node.querySelectorAll('component');
                        components.forEach(this.loadComponent.bind(this));
                    }
                });
            }
        });
    }

    handleAttributeChange(element, attributeName) {
        if (element.tagName.toLowerCase() === 'component') {
            if (['data-link', 'data-props', 'data-replace'].includes(attributeName)) {
                this.loadComponent(element);
            }
        } else if (attributeName.startsWith('data-event-')) {
            const eventType = attributeName.replace('data-event-', '');
            const handlerName = element.getAttribute(data-${eventType}-handler);
            if (handlerName) {
                element.addEventListener(eventType, async (event) => {
                    event.preventDefault();
                    await this.triggerEvent(handlerName, event);
                });
            }
        }
    }

    async loadComponent(tag) {
        const link = tag.getAttribute('data-link');
        const props = JSON.parse(tag.getAttribute('data-props') || '{}');
        const replace = tag.getAttribute('data-replace') === 'true';
        
        try {
            const componentHtml = await this.fetchComponent(link, props);
            
            if (replace) {
                tag.outerHTML = componentHtml;
            } else {
                tag.innerHTML = componentHtml;
            }
            
            this.retriggerCSS();
            this.setupComponentEventListeners(tag.parentNode);
        } catch (error) {
            console.error('Error loading component:', error);
            tag.innerHTML = <p>Error loading component.</p>;
        }
    }

    async fetchComponent(link, props) {
        const response = await fetch('/api/load-component', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ component_name: link, props: props })
        });
        if (!response.ok) {
            throw new Error(Failed to load component: ${link});
        }
        return await response.text();
    }

    async updateComponents() {
        const updatePromises = Object.keys(this.components).map(name => this.updateComponent(name));
        await Promise.all(updatePromises);
    }

    async updateComponent(name) {
        try {
            const response = await this.getFromServer(/api/component/${name});
            if (!response) return;

            const newHtml = response;
            const elements = document.querySelectorAll([data-pyreact-component="${name}"]);
            elements.forEach(el => {
                el.innerHTML = newHtml;
                this.initializeComponent(name, el);
            });
        } catch (error) {
            console.error('Update error:', error);
        }
    }

    setupRouting() {
        document.body.addEventListener('click', (e) => {
            const link = e.target.closest('[data-pyreact-link]');
            if (link && link.getAttribute('href').startsWith('/')) {
                e.preventDefault();
                this.navigate(link.href);
            }
        });

        window.addEventListener('popstate', () => {
            this.updateContent(window.location.pathname);
        });
    }

    async navigate(url) {
        history.pushState(null, '', url);
        await this.updateContent(url);
    }

    async updateContent(url) {
        try {
            const response = await fetch(url, {
                headers: { 'X-Requested-With': 'XMLHttpRequest' }
            });
            if (!response.ok) {
                throw new Error(`Failed to fet
- Automatic state management
- Event handling
- Middleware and hooks
- Error handling
- Static file serving
- Build mode with hot reloading
- API integration
- Component importing from separate files

## Installation

To use Pyreact, you need to have Python installed on your system. You can download this repository and install the required libraries using the following command:


```

pip install fastapi uvicorn watchdog beautifulsoup4

```

(Note: As this is a custom framework, you may need to package and distribute it separately)

##Folder Structure

```
my_pyreact_app/
│
├── app.py
├── index.html
├── pyreact.py
├── static/
│   ├── styles.css
│   └── scripts.js
└── components/
    ├── component1.py
    ├── component2.py
    └── component3.py
```

## Quick Start

1. Create a new directory for your project and set up the folder structure as shown above.
2. Create your main `app.py` file:

```python
from pyreact import pyreact, component, route
from components.Header import Header
from components.Footer import Footer

@component
def App(props):
    return f"""
    {Header(title="My Pyreact App")}
    <main>{props.get('children', 'Welcome to Pyreact!')}</main>
    {Footer()}
    """

@route("/")
async def home(request):
    return App(children="<h1>Hello, Pyreact!</h1>")

app = pyreact.create_app()

if __name__ == "__main__":
    pyreact.set_mode("build") # or "use"
    pyreact.run("app:app", host="127.0.0.1", port=8000, reload=True)
```

3. Run your app:

```
python app.py
```

Visit `http://127.0.0.1:8000` in your browser to see your Pyreact app in action!

## Example App: Multi-feature Blog

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

## Detailed Feature Usage

1. **Components**: Create reusable components using the `@component` decorator.
2. **Routing**: Define routes using the `@route` decorator.
3. **State Management**: Use `pyreact.global_state` to manage application state.
4. **Event Handling**: Create event handlers with `@pyreact.event_handler`.
5. **Component Tag**: Use `<component>` tags to dynamically load components.
6. **Middleware and Hooks**: Use `@pyreact.before_request` and `@pyreact.after_request` for request processing.
7. **Error Handling**: Define custom error handlers with `@pyreact.errorhandler`.
8. **Static Files**: Serve static files from the `static` directory.
9. **Build Mode**: Enable hot reloading with `pyreact.set_mode("build")`.
10. **API Integration**: Create API endpoints using the `@route` decorator with different HTTP methods.

This README provides a comprehensive guide to using the Pyreact framework, including an example blog application that demonstrates all of its features. Users can use this as a starting point to build their own Pyreact applications.
