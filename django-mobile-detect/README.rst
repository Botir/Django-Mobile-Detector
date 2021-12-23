Django Mobile Detector
======================

Mobile Detect is a lightweight Python package for detecting mobile devices (including tablets).
It uses the User-Agent string combined with specific HTTP headers to detect the mobile environment.

PHP
===
this package development based from php big repository `Mobile-Detect <https://github.com/serbanghita/mobile-detect>`_

.. image:: http://demo.mobiledetect.net/logo-github.png

Installation
============
1. Python package install::

    pip install django-mobile-detect


2. Add ```mobiledetect``` to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'mobiledetect',
    ]

3. Middleware::

    MIDDLEWARE_CLASSES = (
        '...',
        'mobiledetect.middleware.DetectMiddleware',
        '...'
    )

View Usage
----------

You can use in views

    Check if the device is mobile.

::

    request.device.is_mobile

|

    Check if the device is a tablet.

::

    request.device.is_tablet
