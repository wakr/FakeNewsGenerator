# FakeNewsGenerator
Project for Computational Creativity 2017

## Install (WIP)

To install requirements:

		pip install -r requirements.txt

NOTE: Selenium requires appropriate driver for chosen browser and this is not installed by above command.
Presently this program uses Chrome as a browser, so you will need appropriate [driver](https://sites.google.com/a/chromium.org/chromedriver/downloads). See [Selenium](https://pypi.python.org/pypi/selenium/3.8.0) for more information on this.

After requirements installation, download Word2Vec model from https://drive.google.com/file/d/1jXxEfznmBGphznZHY9W6AT39yye8hAC6/view?usp=sharing , and place it to data -folder. 

## Usage 


		python main.py

main.py fetches original tweets from CNN and runs the generator. If there is already tweets saved to txt-file, program takes tweets from it. Program should print all information needed to successful generation and finally print the generated tweet.

### Note! 
If the program prints that it found about over 100 000 different candidate tweet combinations, evaluation phase of them would take several minutes. 

## Project description 

This project description is aimed for non-technical people and full project descriptions can be found from our take-home exams. 

The goal of our system is to create fake news. When we then thought about what fake news actually means, we decided to define fake news as negative news for our prototype system. Our domain is thus news. 

First our system fetches tweets from CNN and preprocesses them a little. Then it generates "fake news" tweet from one tweet. Generator works so that it tries to replace adjectives, nouns and verbs with different ways with usually more negative words than the original words. The system evaluates different candidate tweets and decides which is best. Finally system outputs the tweet. 



