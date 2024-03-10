# system and other dependencies
sudo apt update
sudo apt install -y python3 python3-pip

# scrapy setup
pip3 install scrapy

# selenium setup
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get -f install -y  # This fixes any dependency issues from the previous command

pip3 install selenium webdriver-manager

# clone repository
git clone https://github.com/jorgeiras/buscainstrumentos_scrapers.git

# get into the scrapers folder
cd buscainstrumentos_scrapers
cd scrapers

# exec scraper scripts
python3 guitarristasScrap.py
python3 hispasonicScrap.py
python3 reverbScrap.py
python3 soundmarketScrap.py

# get into the db loaders folder
cd ..
cd db_loaders

# exec db loader scripts
python3 db_load_guitarristas.py
python3 db_load_hispasonic.py
python3 db_load_reverb.py
python3 db_load_soundmarket.py