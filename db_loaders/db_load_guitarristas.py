from scrapy.loader.processors import MapCompose
import psycopg2
import os

csv_file_path = '../scrapers/guitarristas.csv'

# connect to database
conn = psycopg2.connect(database=os.environ.get('DB_NAME'), user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASS'), host=os.environ.get('DB_HOST'), port=os.environ.get('DB_PORT'))
cursor = conn.cursor()

#creacion de tabla temporal 
cursor.execute('CREATE TEMP TABLE temp_table_guitarristas (LIKE "buscainstrumentos_API_instrument" INCLUDING ALL)')
conn.commit()

#cargar data en la tabla temporal 
copy_sql = """
           COPY temp_table_guitarristas (category,expiration,image,link,location,name,price,publish,website) FROM stdin WITH CSV HEADER
           DELIMITER as ','
           """
with open(csv_file_path, 'r', encoding='utf-8', errors='replace') as f:
    cursor.copy_expert(sql=copy_sql, file=f)
conn.commit()

#cargar data de la tabla temporal a la tabla final
cursor.execute("""
                INSERT INTO "buscainstrumentos_API_instrument" (name, price, link, website, image, location, category, expiration,publish)
                SELECT name, price, link, website, image, location, category, expiration,publish FROM temp_table_guitarristas
                ON CONFLICT (link) DO NOTHING;
            """)
conn.commit()
        
#eliminar la tabla temporal
cursor.execute("DROP TABLE temp_table_guitarristas")
cursor.close()
conn.close()
