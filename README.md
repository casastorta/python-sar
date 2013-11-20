SAR Python Module
=================

SAR Python module is a module written for parsing plain-text SAR files
(linux systat service output).

Note that it doesn't parse SAR binary files (`saXX`), but only ASCII files
(`sarXX`). Also, please note that yet it doesn't handle timestamps in 12-hour
format (AM/PM), but only in 24-hour format, which basically means it
parses auto-generated `sarXX` files, but not output from the `sar -A`
command.

More info follows soon with further releases.
