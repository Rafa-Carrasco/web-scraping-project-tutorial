import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# descargar data 

url = "https://es.wikipedia.org/wiki/Leucocito"
response = requests.get(url, time.sleep(10))
soup = BeautifulSoup(response.text, 'html.parser')

# buscar html requerido 

table = soup.find('table', class_='wikitable')
headers = [header.text for header in table.find_all('th')]

rows = []
for row in table.find_all('tr')[1:]:  
    cells = row.find_all('td')
    rows.append([cell.text for cell in cells])

# crear DF
 
df = pd.DataFrame(rows, columns=headers)
# print(df.head())
# df.shape


# eliminar valores no utiles
df_final = df.drop(['Apariencia microscópica', 'Diagrama', '[7]\u200b Principal objetivo', '[4]\u200b Núcleo', '[4]\u200b Gránulos', '[4]\u200b Vida media[7]\u200b\n' ], axis=1)

# cambiar valores especificos

df_final.at[3, 'Diámetro (μm)'] = '7-15'
df_final.at[4, 'Diámetro (μm)'] = '12-15'

# eliminar caracteres % 

df_final['Porcentaje aproximado en adultos'] = df_final['Porcentaje aproximado en adultos'].str.replace('%', '').astype('float') / 100
print(df_final) 

# Conectar y crear base de datos
conn = sqlite3.connect('leucocito.db')

# Guardar el DataFrame en la base de datos
df_final.to_sql('leucocito', conn, if_exists='replace', index=False)

# Cerrar la conexión
conn.close()

# Conectar a la base de datos
conn = sqlite3.connect('leucocito.db')

# Leer los datos de la tabla
df_leido = pd.read_sql('SELECT * FROM leucocito', conn)

# Cerrar la conexión
conn.close()

# Mostrar los datos leídos
print("DataFrame leído de la base de datos:")
print(df_leido)


# Histogramas

df_final.hist(figsize=(10, 6), bins=10, color='red', edgecolor='black', grid=False)
plt.tight_layout()  
plt.show()


fig, axes = plt.subplots(1, 2, figsize=(15, 5))
axes[0].scatter(df_leido['Porcentaje aproximado en adultos'], df_leido['Tipo'], color='red')
axes[1].scatter(df_leido['Diámetro (μm)'], df_leido['Tipo'], color='blue')


# Gráfico de barras del departamento

df_leido['Diámetro (μm)'].value_counts().plot(kind='bar', color='salmon')
plt.xlabel('Porcentaje')
plt.title('diametro de leucocitos')
plt.show()