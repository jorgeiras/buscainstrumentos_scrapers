# system and other dependencies
sudo apt update
sudo apt install -y python3 python3-pip

# scrapy setup
pip3 install scrapy

# reverb libraries setup 
pip install requests_cache
pip install ipython

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

# setup ES locale
sudo locale-gen es_ES.UTF-8
sudo update-locale

# exec scraper scripts
#scrapy runspider guitarristasScrap.py -o guitarristas.csv -t csv
#scrapy runspider hispasonicScrap.py -o hispasonic.csv -t csv
#python3 reverbScrap.py
python3 soundmarketScrap.py

# get into the db loaders folder
cd ..
cd db_loaders

# exec db loader scripts
#python3 db_load_guitarristas.py
#python3 db_load_hispasonic.py
#python3 db_load_reverb.py
python3 db_load_soundmarket.py