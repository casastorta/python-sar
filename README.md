SAR Python Module
=================

SAR Python module is a module written for parsing plain-text SAR files
(linux systat service output).

Note that it doesn't parse SAR binary files (`saXX`), but only ASCII files
(`sarXX`).

More info follows soon with further releases.


Plans for v2.0
---------------

General plans for v2.0 are:

* Complexity optimization of parsing process

* Exceptions thrown for **fatal** processing errors. Non-fatal errors
  will stay silent

* Unit testing

* Better documentation

* Change of the in-memory parsed SAR format is possible, although, at 
  this moment I find it unlikely.

If you are using current version of this module in your Python 
applications, please pin to version 1.x in your requirements not to 
experience broken compatibility in the future.