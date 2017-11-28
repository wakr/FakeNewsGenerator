import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def collect_tweets(username, pagecount=5):
    browser = webdriver.Chrome()
    base_url = 'https://twitter.com/'
    url = base_url + username
    browser.get(url)
    time.sleep(1)

    body = browser.find_element_by_tag_name('body')

    for _ in range(pagecount):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.2)

    tweets = browser.find_elements_by_class_name('tweet-text')
    for tweet in tweets:
        print(tweet.text)

    browser.close()

#
# Main
#
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('username', action='store', type=str, help='username whose tweets are scraped')
    parser.add_argument('-p', '--pagecount', action='store', type=int, help='number of pages to retrieve')
    args = parser.parse_args()

    if args.pagecount:
        collect_tweets(args.username, args.pagecount)
    else:
        collect_tweets(args.username)

