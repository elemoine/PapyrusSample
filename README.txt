PapyrusSample
=============

Run with Waitress
-----------------

Run PapyrusSample:

    pserve development.ini --reload


Run with uWSGI
--------------

Install uWSGI in the virtualenv:

    pip install uwsgi

Run PapyrusSample:

    uwsgi -H /home/elemoine/.virtualenvs/papyrus_mapnik --http :9090 --ini-paste production.ini
