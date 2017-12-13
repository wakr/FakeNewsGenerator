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

main.py fetches original tweets from CNN and runs the generator. If there is already tweets saved to txt-file, program takes tweets from it. Program should print all information needed to successful generation.

Note! If the program prints that it found about over 100 000 different candidate tweet combinations, evaluation phase of them would take several minutes. 

