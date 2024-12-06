# Dropzone Repackaged for Django

[Dropzone](TODO) packaged in a Django reusable app.

This package includes only the original JS and CSS files.


## Installation

    pip install django-js-lib-dropzone

## Usage

1. Add `"js_lib_dropzone"` to your `INSTALLED_APPS` setting like this::

       INSTALLED_APPS = [
           ...
           "js_lib_dropzone",
           ...
       ]

2. In your template use:
   
       {% load static %}
   
   ...
   
       <link rel="stylesheet" href="{%static "js_lib_dropzone/dropzone.css" %}">
   
   ...
   
       <script src="{%static "js_lib_dropzone/js/dropzone.js" %}"></script>
