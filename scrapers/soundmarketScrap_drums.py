
import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver # pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import csv


def parse_precio(texto):
            texto_nuevo = texto.replace('€', '')
            texto_nuevo = texto_nuevo.replace('$', '')
            texto_nuevo = texto_nuevo.replace(',', '.')
            return texto_nuevo

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)



# Asi podemos setear el user-agent en selenium
#opts = Options()
#opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
#driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=opts)

# Voy a la pagina que quiero
driver.get('https://soundsmarket.com/servicios/compraventa/percusion')
sleep(2)
driver.refresh() # Solucion de un bug extraño en Windows en donde los anuncios solo cargan al hacerle refresh a la página
sleep(4) # Esperamos que cargue el boton

cookiesAcceptButton = driver.find_element(By.XPATH, '//div[@id="cookies_main"]//button[@class="lcc-button js-lcc-accept"]')
try:
    cookiesAcceptButton.click()
except Exception as e:
    print('ERROR AL ACEPTAR COOKIES')
    print(e)

# Busco el boton para cargar mas informacion
boton = driver.find_element(By.XPATH, '//button[@class="stw-flex stw-justify-center stw-border stw-border-orange stw-rounded-sm stw-bg-orange stw-p-2 stw-text-center stw-text-lg stw-font-bold stw-text-white stw-mt-10 stw-mx-auto stw-w-60 stw-cursor-pointer hover:stw-bg-orange-light hover:stw-border-orange-light hover:stw-text-white"]')
               
initial_count = len(driver.find_elements(By.XPATH, '//div[@class="stw-flex stw-w-full stw-overflow-x-auto stw-pb-1.5 stw-flex-wrap"]/div'))
while True: # Voy a darle click en cargar mas 3 veces
    try:
        # le doy click
        boton.click()
        print('------SE CLICKO EL BOTON-----')
        # espero que cargue la informacion dinamica
        sleep(random.uniform(8.0, 10.0))

        new_count = len(driver.find_elements(By.XPATH, '//div[@class="stw-flex stw-w-full stw-overflow-x-auto stw-pb-1.5 stw-flex-wrap"]/div'))
        if new_count == initial_count:
            print('No new items loaded.')
            break  # Break the loop if no new items were added
        initial_count = new_count 
        
        # busco el boton nuevamente para darle click en la siguiente iteracion
        boton = driver.find_element(By.XPATH, '//button[@class="stw-flex stw-justify-center stw-border stw-border-orange stw-rounded-sm stw-bg-orange stw-p-2 stw-text-center stw-text-lg stw-font-bold stw-text-white stw-mt-10 stw-mx-auto stw-w-60 stw-cursor-pointer hover:stw-bg-orange-light hover:stw-border-orange-light hover:stw-text-white"]')
        
    except Exception as e:
        # si hay algun error, rompo el lazo. No me complico.
        print('------ERROR AL CLICKAR-----')
        print(e)
        break

# Encuentro cual es el XPATH de cada elemento donde esta la informacion que quiero extraer
# Esto es una LISTA. Por eso el metodo esta en plural
guitarras = driver.find_elements(By.XPATH, '//div[@class="stw-flex stw-w-full stw-overflow-x-auto stw-pb-1.5 stw-flex-wrap"]/div')



with open('soundmarket.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['category', 'image', 'link', 'name', 'price', 'website' ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()


    # Recorro cada uno de los anuncios que he encontrado
    for guitarra in guitarras:
        try:
            # Por cada anuncio hallo el precio
            precio = guitarra.find_element(By.XPATH, './/span[@class="stw-text-orange"]').text
            precio_clean = parse_precio(precio)
            print (precio_clean)
            # Por cada anuncio hallo la descripcion
            titulo = guitarra.find_element(By.XPATH, './/span[@class="stw-font-bold stw-line-clamp-2 stw-text-sm stw-leading-tight stw-pt-1"]').text
            print (titulo)
            imagen = guitarra.find_element(By.XPATH, './/img').get_attribute('src')
            print (imagen)
            link = guitarra.find_element(By.XPATH, './a').get_attribute('href')
            print (link)
            item = {
                'category': "baterias", 
                'image': imagen,
                'link': link,
                'name': titulo,
                'price': precio_clean,
                'website': "soundmarket"
            }
            writer.writerow(item)
        except Exception as e:
            print ('Anuncio carece de precio o descripcion')
            print(e)


        
