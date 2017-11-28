# Tweet text screen scraper

This script uses [Selenium](http://www.seleniumhq.org/) to grab tweets text. For Python installation see
[Installation](http://selenium-python.readthedocs.io/installation.html#introduction) and remember to install
[drivers](http://selenium-python.readthedocs.io/installation.html#drivers) as well. Text are output to standard output.

# Usage:

python twitter_grabber.py \<username\> [-p <count>]

where

\<username\> is account to capture such as CNN

-p \<count\> is optional argument for how many pages should be capture default being five.

Examples:

Grab five pages of tweets from CNN:
python twitter_grabber.py CNN

Grab ten pages of tweets from CNN:
python twitter_grabber.py CNN -p 10

