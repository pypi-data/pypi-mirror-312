<p align="center">
    <img src="https://github.com/scape-agency/swing.dj/blob/85830584264bca52c02e1f0dcfa3648f84783805/res/swing-logo.png" width="20%" height="20%" alt="Django Swing Logo">
</p>
<h1 align='center' style='border-bottom: none;'>Swing Hello</h1>
<h3 align='center'>Django Swing Collection</h3>
<br/>

---

## Introduction

**Swing Hello** is a simple reusable Django application that provides basic views to demonstrate response handling and template rendering. It is designed to provide simple, yet effective functionality for greeting users through various forms and views. This package includes both function-based and class-based views for returning plain text and rendering templates with context. It showcases the best practices in Django app development, including internationalization, testing, and modular design.

---

## Features

- Function-based view returning a plain text "Hello!" response.
- Class-based view returning a plain text "Hello!" response.
- Function-based view rendering a template with a context.
- Class-based view rendering a template with a context.

---

## Installation

1. Ensure you have Django installed. If not, you can install it using pip:

   ```bash
   pip install django
   ```

2. Clone the repository or download the package and include it in your Django project.

## Setup

1. Add `swing_hello` to your Django project's `INSTALLED_APPS` in `settings.py`:

   ```python
   INSTALLED_APPS = [
       ...
       'swing_hello',
   ]
   ```

2. Include the `swing_hello` URLs in your project's `urls.py`:

   ```python
   from django.urls import path, include

   urlpatterns = [
       ...
       path('hello/', include('swing_hello.urls')),
   ]
   ```

---

## Usage

### Function-Based Views

- `hello_response_view`: Returns a plain text "Hello!" response.
- `hello_template_view`: Renders a template with a context.

### Class-Based Views

- `HelloResponseView`: Returns a plain text "Hello!" response.
- `HelloTemplateView`: Renders a template with a context.

### URL Patterns

The package provides the following URL patterns:

- `/hello/` - Renders the template with context using `HelloTemplateView`.
- `/hello/response` - Returns a plain text "Hello!" response using `HelloResponseView`.
- `/hello/template` - Renders the template with context using `HelloTemplateView`.

---

## Example Template

The package includes a simple HTML template `hello.html`:

```html
<!doctype html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f4f4f4;
        }
        .container {
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        h1 {
            margin-bottom: 20px;
            color: #333;
        }
        p {
            color: #666;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>{{ title }}</h1>
        <p>{{ content }}</p>
    </div>
</body>

</html>
```

---

## Project Structure

``` bash
swing_hello/
├── demo/                       # This directory contains a sample Django project for testing your reusable app (swing_hello).
│   ├── manage.py               # Entry point for managing the demo project.
│   ├── demo/
│   │   ├── __init__.py
│   │   ├── settings.py         # Configuration for the demo project.
│   │   ├── urls.py             # Main URL configuration for testing.
│   │   └── wsgi.py
│   └── db.sqlite3
├── src/
│   ├── swing_hello/            # Core directory of your reusable Django app.
│       ├── __init__.py         # Initializes the Python module.
│       ├── __main__.py
│       ├── apps.py             # Defines the app configuration for Django.
│       ├── urls.py             # URLs specific to this app.
│       ├── forms/              # Contains Django forms (e.g., form_hello.py).
│       │   ├── __init__.py
│       │   └── form_hello.py
│       ├── locale/             # Holds translation files for internationalization (e.g., en, nl).
│       │   ├── en/
│       │   │   └── ...
│       │   └── nl/
│       │       └── ...
│       ├── migrations/         # Contains migration scripts for the app.
│       │   ├── __init__.py
│       │   └── ...
│       ├── static/             # Stores app-specific static files (e.g., styles.css).
│       │   └── swing_hello/
│       │       └── styles.css
│       ├── templates/          # App-specific templates (e.g., hello_template.html).
│       │   └── swing_hello/
│       │       ├── hello_form.html
│       │       └── hello_template.html
│       ├── tests/              # Test cases for the app (e.g., test_hello_form.py).
│       │   ├── __init__.py
│       │   ├── test_hello_form.py
│       │   ├── test_hello_json.py
│       │   ├── test_hello_response.py
│       │   ├── test_hello_template.py
│       │   └── ...
│       └── views/              # App views organized by functionality (e.g., view_hello_form.py).
│           ├── __init__.py
│           ├── view_hello_form.py
│           ├── view_hello_json.py
│           ├── view_hello_response.py
│           ├── view_hello_template.py
│           └── ...
├── setup.py                    # Configuration for packaging and distributing the app.
├── README.md                   # Documentation for the repository.
└── LICENSE                     # Specifies the license for the project.
```

---

## Colophon

Made with ❤️ by **[Scape Agency](https://www.scape.agency)**

### Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

### License

This project is licensed under the BSD-3-Clause license. See the [LICENSE](LICENSE) file for details.

---
