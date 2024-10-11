# Pyreact Framework

Pyreact is a lightweight Python-based web framework that seamlessly blends server-side rendering with client-side interactivity. Designed for simplicity and efficiency, Pyreact empowers developers to build dynamic and responsive web applications using Python.

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Folder Structure](#folder-structure)
5. [Quick Start](#quick-start)
6. [Example App: Multi-feature Blog](#example-app-multi-feature-blog)
7. [Detailed Feature Usage](#detailed-feature-usage)
8. [Contributing](#contributing)
9. [License](#license)

## Features

- **Component-Based Architecture**: Create reusable UI components with ease.
- **Server-Side Rendering (SSR)**: Enhance SEO and initial load times with SSR.
- **Client-Side Routing**: Navigate between pages without full page reloads.
- **Automatic State Management**: Manage global and component-specific state effortlessly.
- **Event Handling**: Handle user interactions and events seamlessly.
- **Middleware and Hooks**: Execute custom logic before and after requests.
- **Error Handling**: Customize responses for different error scenarios.
- **Static File Serving**: Serve CSS, JavaScript, images, and other static assets.
- **Build Mode with Hot Reloading**: Enjoy rapid development with automatic page refreshes on code changes.
- **API Integration**: Create RESTful API endpoints easily.
- **Component Importing**: Organize components in separate files for better maintainability.

## Prerequisites

Before getting started with Pyreact, ensure you have the following installed on your system:

- Python 3.7 or higher: [Download Python](https://www.python.org/downloads/)
- pip: Python package installer (comes bundled with Python)
- Git (optional, for cloning the repository): [Download Git](https://git-scm.com/downloads)

## Installation

1. Clone the Repository:
   ```
   git clone https://github.com/yourusername/pyreact.git
   cd pyreact
   ```

2. Install Required Libraries:
   ```
   pip install fastapi uvicorn watchdog beautifulsoup4
   ```

> Note: Since Pyreact is a custom framework, you may need to package and distribute it separately if you're planning to use it across multiple projects.

## Folder Structure

Organize your Pyreact application with a clear and intuitive folder structure:

```
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
```

## Quick Start

Follow these steps to create and run your first Pyreact application:

1. Set Up the Project Directory:
   ```
   mkdir my_pyreact_app
   cd my_pyreact_app
   ```

2. Create the Folder Structure:
   ```
   mkdir static components
   touch app.py index.html pyreact.py static/styles.css static/scripts.js
   ```

3. Create the `index.html` File:
   ```html
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
   ```

4. Create the Main Application File (`app.py`):
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
       pyreact.set_mode("build")  # or "use" for production
       pyreact.run(host="127.0.0.1", port=8000, reload=True)
   ```

5. Create Components:
   
   `components/Header.py`:
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

   `components/Footer.py`:
   ```python
   from pyreact import component

   @component
   def Footer(props):
       return """
       <footer>
           <p>&copy; 2024 My Pyreact App</p>
       </footer>
       """
   ```

6. Run the Application:
   ```
   python app.py
   ```

   Open your browser and navigate to `http://127.0.0.1:8000` to see your Pyreact app in action!

## Example App: Multi-feature Blog

For a more comprehensive example showcasing Pyreact's capabilities, refer to the [Example App: Multi-feature Blog](#example-app-multi-feature-blog) section in the full documentation.

## Detailed Feature Usage

For detailed information on how to use specific features of Pyreact, please refer to the full documentation.

## Contributing

We welcome contributions to the Pyreact Framework! Please read our contributing guidelines before submitting pull requests.

## License

Pyreact is released under the [MIT License](https://opensource.org/licenses/MIT).
