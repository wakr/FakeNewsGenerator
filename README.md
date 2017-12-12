# FakeNewsGenerator
Project for Computational Creativity 2017

## Install (WIP)

To install requirements:

		pip install -r requirements.txt

NOTE: Selenium requires appropriate driver for chosen browser and this is not installed by above command.
Presently this program uses Chrome as a browser, so you will need appropriate [driver](https://sites.google.com/a/chromium.org/chromedriver/downloads). See [Selenium](https://pypi.python.org/pypi/selenium/3.8.0) for more information on this.

After requirements installation, create Word2Vec -model that is needed for novelty evaluation: 

```
python3 modules/create_word2vec_model.py
```

Now you should have a file called Model in your data -directory. Then run main.py.

