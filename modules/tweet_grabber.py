"""Twitter tweet screen scaper

This module collects tweets from Twitter using screen scraping. It uses Selenium
(http://www.seleniumhq.org/) to control browser and do screen scraping.

It will return obtained tweet texts as a Python list or, if used from command line,
it will print this list to standard output stream.

Usage:

As part of program:

import tweet_grabber as tg
tg.collect_tweets(username, [<pagecount>])

From command line:

python twitter_grabber.py <username> [-p <count>]

where

<username> is account to capture such as CNN
<pagecount> or -p <count> is optional argument for how many pages of tweets should be captured.
 If no value is given it defaults to five.

"""
import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def collect_tweets(username, pagecount=5):
    '''Collect list of texts from tweets by given username

    Username: Twitter username to collect tweets from. E.g. CNN
    Pagecount (optional): number of page scrolls to do to collect tweets
    '''

    # Create browser, URL and wait until browser has opened the page
    browser = webdriver.Chrome()
    base_url = 'https://twitter.com/'
    url = base_url + username
    browser.get(url)
    time.sleep(1)

    # Search for the HTML document body to send key presses to
    body = browser.find_element_by_tag_name('body')

    # Simulate keep presses based on pagecount
    for _ in range(pagecount):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)

    # Collect tweet-text elements from the broser
    tweet_texts = browser.find_elements_by_class_name('tweet-text')
    # and collect their text to list.
    tweets_lst = []
    for tweet in tweet_texts:
        txt = tweet.text
        # Ignore multiline tweets
        if txt.find('\n') < 0:
            tweets_lst.append(tweet.text)

    browser.close()

    return tweets_lst

#
# Main
#
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('username', action='store', type=str, \
        help='username whose tweets are scraped')
    parser.add_argument('-p', '--pagecount', action='store', \
        type=int, help='number of pages to retrieve')
    args = parser.parse_args()

    if args.pagecount:
        tweets = collect_tweets(args.username, args.pagecount)
    else:
        tweets = collect_tweets(args.username)

    # Output tweets from the list
    for tweet in tweets:
        print(tweet)
