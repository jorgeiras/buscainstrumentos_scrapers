import psycopg2
import csv
import os

csv_file_path = '../db_loaders/soundmarket.csv'
csv_file_path_clean = '../db_loaders/soundmarket_clean.csv'

#clean csv duplicates 
unique_links = set()
clean_rows = []

with open(csv_file_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['link'] not in unique_links:
            clean_rows.append(row)
            unique_links.add(row['link'])

# Write the cleaned rows back to a new CSV file
with open(csv_file_path_clean, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=reader.fieldnames)
    writer.writeheader()
    writer.writerows(clean_rows)


# connect to database
conn = psycopg2.connect(os.environ.get('DB_NAME'), os.environ.get('DB_USER'), os.environ.get('DB_PASS'), os.environ.get('DB_HOST'), os.environ.get('DB_PORT'))
cursor = conn.cursor()

#creacion de tabla temporal 
cursor.execute('CREATE TEMP TABLE temp_table_soundmarket (LIKE "instrCopyAPI_instrument" INCLUDING ALL)')
conn.commit()

#cargar data en la tabla temporal 
copy_sql = """
           COPY temp_table_soundmarket (category,image,link,name,price,website) FROM stdin WITH CSV HEADER
           DELIMITER as ','
           """
with open(csv_file_path_clean, 'r', encoding='utf-8', errors='replace') as f:
    cursor.copy_expert(sql=copy_sql, file=f)
conn.commit()

#cargar data de la tabla temporal a la tabla final
cursor.execute("""
                INSERT INTO "instrCopyAPI_instrument" (name, price, link, website, image, location, category, expiration, publish)
                SELECT name, price, link, website, image, location, category, expiration, publish FROM temp_table_soundmarket
                ON CONFLICT (link) DO NOTHING;
            """)
conn.commit()
        
#eliminar la tabla temporal
cursor.execute("DROP TABLE temp_table_soundmarket")
cursor.close()
conn.close()