Dublin Bus on Bluemix
=============================

Web app page
-----------------------
[Dublinbus on Bluemix](http://dublin-bus.mybluemix.net/stopid/262)

Description
-----------------------
Given a specific bus stop, this web application can quickly consult the RTPI API, return real time information of all bus routes and display on the web page. 

* A MongoDB is working behind the scene and records all requests so far;
* AngularJS is working to rendering JSON files for "search by route" service;
* It is hosted on IBM Bluemix using CloudFoundry Python buildpack; 

Notes
-----
* 09Nov2014: working on this app to make it work with Mongodb

* 10Nov2014: now this app is working with Mongodb

* 05FEB2015: complete "search by bus stop" service

* 22FEB2015: add "search by route" service

* 24FEB2015: start to work on "search on map" service

* 2MAR2015: rebuilt "search by route" service using AngularJS

Credit
-----------------------
This web app is using [Flask microframework](http://flask.pocoo.org/) and built by [Cloud Foundry buildpack for python](https://github.com/cf-buildpacks/compile-extensions.git), following [Henrik's tutorial](http://blog.4loeser.net/2014/06/some-fun-with-bluemix-cloud-foundry.html) and based on [a sample Python web application](https://github.com/michaljemala/hello-python). Special thanks to [this gist](https://gist.github.com/lucasmcastro/9654941).
