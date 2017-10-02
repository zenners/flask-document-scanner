# flask-document-scanner

## Inspiration
I read this blog post. https://www.pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/
I wanted to use this a service to use to build applications with. The idea is to send the image you want over HTTP and get back the scanned image as a response.

![20161215-160329-largejpg](https://user-images.githubusercontent.com/3746914/31071089-537171da-a795-11e7-9d59-9acbcd2ccccd.jpg)


## Setup
I tested this with Python 3. Create your environment and install the packages with `pip install -r requirements.txt`.

## Running
Run with `python server.py`
With Postman or Curl, send a POST request with form-data, "file" is the key and the value is your image.
As a response, you should get the scanned image.

![20161215-160329-largejpg](https://user-images.githubusercontent.com/3746914/31070957-ead279f8-a794-11e7-9c77-33bfb8acab0e.jpg)

