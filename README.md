A python application that generate a site map. Starting from the given url, it traverses all the links found in the site and returns a list of links.

### Run
```sh
git clone git@github.com:muatik/sitemapper.git
pip install -r requirements.txt
cd sitemapper
python app.py
```

### Test
Install pytest, `pip install pytest` and issue the following commands.
```sh
git clone git@github.com:muatik/sitemapper.git
pip install -r requirements.txt
cd sitemapper
pytest tests
```