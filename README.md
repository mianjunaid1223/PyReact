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
- Client-side routing
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
