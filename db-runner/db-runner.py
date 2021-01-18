import psycopg2
import pandas as pd
import requests
import io

# clean csv
api_url = "https://raw.githubusercontent.com/OpportunityInsights/EconomicTracker/main/data/Womply%20Revenue%20-%20County%20-%20Daily.csv"
sort_string = 'countyfips'

s = requests.get(api_url).content
c=pd.read_csv(io.StringIO(s.decode('utf-8')))
df = pd.DataFrame(c)

# Filter by County
df = df.loc[df[sort_string] == 15007]
print(df)
df.to_csv('womply.csv', encoding='utf-8', index=False)

with open('womply.csv', 'r') as f:    
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="mysecretpassword", host="")
    cursor = conn.cursor()
    #cmd = 'COPY womply(year, month, day, countyfips, revenue_all) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)'
    cmd = '''CREATE TEMPORARY TABLE temporary_table ( 
            year INTEGER,
            month INTEGER,
            day INTEGER,
            countyfips INTEGER,
            revenue_all NUMERIC
            );
            COPY temporary_table(year, month, day, countyfips, revenue_all) FROM STDIN WITH (FORMAT CSV, HEADER TRUE)
            
            INSERT INTO womply (*)
            (SELECT DISTINCT * FROM temporary_table)
        '''
    cursor.copy_expert(cmd, f)
    conn.commit()
