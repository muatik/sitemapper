### Site mapper
A python application that generates a site map. Starting from the given url, it traverses all the links found in the site and returns a list of links.

[![Build Status](https://travis-ci.org/muatik/sitemapper.svg?branch=master)](https://travis-ci.org/muatik/sitemapper)


### Run
```sh
git clone git@github.com:muatik/sitemapper.git
pip install -r requirements.txt
cd sitemapper
python app.py --help
python app.py --url https://muatik.github.io/
```

### Test
Install pytest, `pip install pytest` and issue the following commands.
```sh
git clone git@github.com:muatik/sitemapper.git
pip install -r requirements.txt
cd sitemapper
pytest tests
```
