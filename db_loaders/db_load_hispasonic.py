import psycopg2

csv_file_path = '../scrapers/hispasonic.csv'

# connect to database
conn = psycopg2.connect(database='instrCopyDB', user='postgres', password='admin', host='localhost', port='5432')
cursor = conn.cursor()

#creacion de tabla temporal 
cursor.execute('CREATE TEMP TABLE temp_table_hispasonic (LIKE "buscainstrumentos_API_instrument" INCLUDING ALL)')
conn.commit()

#cargar data en la tabla temporal 
copy_sql = """
           COPY temp_table_hispasonic (category,expiration,image,link,location,name,price,publish,website) FROM stdin WITH CSV HEADER
           DELIMITER as ','
           """
with open(csv_file_path, 'r', encoding='utf-8', errors='replace') as f:
    cursor.copy_expert(sql=copy_sql, file=f)
conn.commit()

#cargar data de la tabla temporal a la tabla final
cursor.execute("""
                INSERT INTO "buscainstrumentos_API_instrument" (name, price, link, website, image, location, category, expiration, publish)
                SELECT name, price, link, website, image, location, category, expiration, publish FROM temp_table_hispasonic
                ON CONFLICT (link) DO NOTHING;
            """)
conn.commit()
        
#eliminar la tabla temporal
cursor.execute("DROP TABLE temp_table_hispasonic")
cursor.close()
conn.close()

        