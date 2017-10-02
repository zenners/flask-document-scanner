# flask-document-scanner

## Inspiration
I read this blog post. https://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/
I wanted to use this a service to use to build applications with. The idea is to send the image you want over HTTP and get back the scanned image as a response.

## Setup
I tested this with Python 3. Create your environment and install the packages with `pip install -r requirements.txt`.

## Running
Run with `python server.py`
With Postman or Curl, send a POST request with form-data, "file" is the key and the value is your image.
As a response, you should get the scanned image.
