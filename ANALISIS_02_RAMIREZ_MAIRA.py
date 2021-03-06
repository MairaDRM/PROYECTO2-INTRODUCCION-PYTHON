# -*- coding: utf-8 -*-
"""
Created on Sun Jan  9 01:34:21 2022

@author: labsim
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 11:51:25 2022

@author: labsim
"""
# importación de librerias
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#%%
"""
Para leer el archivo csv que contiene la base de datos de Synergy logistics 
usamos la funcion read_csv de pandas, indicando los siguientes parametros para 
procesar adecuadamente cada tipo de dato:
    
    index_col=0         # para decir que el register_id es el indice.
    encoding='utf-8'    # para indicar que nuestro documento incluye caracteres
                        # de este tipo.
    parse_dates=[4, 5]  # le estamos especificando aqui que la columna 4 y 5
                        # contienen fechas y quiero que las procese como tal.
"""
#register_id, direction, origin, destination, year, date, product, 
#transport_mode, company_name, total_value

synergy_dataframe = pd.read_csv('synergy_logistics_database.csv',
                                index_col=0, encoding='utf-8',
                                parse_dates=[4, 5])


#%%
"""
Parametros para mejorar las graficas.
"""

plt.style.use('bmh')
n=10
cmap = plt.cm.get_cmap('GnBu')
color = cmap(np.linspace(.4,.8, n))

cmap2 = plt.cm.get_cmap('BuGn')
color2 = cmap2(np.linspace(.4,.8, n))


#%%

#Separación de los datos entre exportaciones e importaciones

exports = synergy_dataframe[synergy_dataframe['direction'] == 'Exports'].copy()
imports = synergy_dataframe[synergy_dataframe['direction'] == 'Imports'].copy()

#%%
"""
OPCIÓN 1

Synergy logistics está considerando la posibilidad de enfocar sus esfuerzos 
en las 10 rutas más demandadas. Segun los flujos de importación y exportación,
¿cuáles son esas 10 rutas?

"""

# Combinacion unica de 'origin' y 'destination'. para obtener la información
#de cada ruta

#función para contabilizar el uso de las rutas y sacar el top10
def sol_1(df1, p, color, orden):
    comb_df1 = df1.groupby(by=['origin', 'destination'])
    descripcion_df1 = comb_df1.describe()['total_value']
    frec_df1= descripcion_df1['count']
    frec_df1_sort=frec_df1.sort_values(ascending=orden)

    top10_df1=frec_df1_sort.head(p).sort_values(ascending=True).plot(
        kind='barh',  xlabel='RUTA', title='Demanda 2015-2020', color=color,  
        xlim=(0,500))        
                 
    plt.show()
    
    return top10_df1

demanda_exports = sol_1(exports, 10, color, False)
demanda_exports_menos = sol_1(exports, 10, color, True)
demanda_imports = sol_1(imports, 10, color2, False)
demanda_imports_menos = sol_1(imports, 10, color2, True)

#%%
"""
OPCIÓN 2

Medio de transporte utilizado. ¿Cuáles son los 3 medios de transporte
más importantes para Synergy logistics considerando el valor de las
importaciones y exportaciones? ¿Cuál es medio de transporte que podrían
reducir? 


"""
#Promedio de la gananacia de cada medio de transpote
transportes=synergy_dataframe.groupby(by=['transport_mode'])
descrip_transportes = transportes.describe()['total_value']
mean_transportes=descrip_transportes['mean']. plot(kind='pie', 
                                              autopct='%1.1f%%',
                                              shadow=True, startangle=90,
                                              colormap='Set2', label=
                                              'Medios de transportes',
                                              title='Aportaciones promedio')

plt.tight_layout()
plt.show()

#aportación total 
datos = synergy_dataframe.copy()
# Creo la columna de year_month, que usare como marca
datos['year'] = datos['date'].dt.strftime('%Y')
datos_year = datos.groupby(['year', 'transport_mode'])
# La serie que nos interesa es la de sum para el valor total.
serie = datos_year.count()['total_value']
# serrie a df
dym = serie.to_frame().reset_index()
# le damos la forma que queremos
dym = dym.pivot('year', 'transport_mode', 'total_value').plot(kind='bar',
                                                              colormap='Set2',
                                                              ylabel=
                                                              'Aportación',
                                                              title=
                                   'Aportación anual de los medios de transporte')


# Grafico


#%%
"""
OPCIÓN 3

Si Synergy Logistics quisiera enfocarse en los países que le generan el 80% 
del valor de las exportaciones e importaciones ¿en qué grupo de países debería 
enfocar sus esfuerzos?


"""




def sol_3(df, p):
    pais_total_value = df.groupby('origin').sum()['total_value'].reset_index()
    total_value_for_percent = pais_total_value['total_value'].sum()
    pais_total_value['percent'] = 100 * pais_total_value['total_value'] / total_value_for_percent
    pais_total_value.sort_values(by='percent', ascending=False, inplace=True)
    pais_total_value['cumsum'] = pais_total_value['percent'].cumsum()
    lista_reducida = pais_total_value[pais_total_value['cumsum'] < p]
    
    return lista_reducida
res1_exports = sol_3(exports, 80)
res1_imports = sol_3(imports, 80)

res_exports = sol_3(exports, 80).plot(kind='bar', x='origin', y='percent',
                                      colormap='tab20', color=color)
res_imports = sol_3(imports, 80).plot(kind='bar', x='origin', y='percent',
                                      color=color2, ylabel=('%'), 
                                      title=
                                      ('% de Contribución a las ganancias totales'
                                       ))



#%%
"""
Adicionales
"""
datos = synergy_dataframe.copy()
# Creo la columna de year_month, que usare como marca
datos['year'] = datos['date'].dt.strftime('%Y')
datos_year = datos.groupby(['year', 'transport_mode'])
# La serie que nos interesa es la de sum para el valor total.
serie = datos_year.count()['total_value']
# serrie a df
dym = serie.to_frame().reset_index()
# le damos la forma que queremos
dym = dym.pivot('year', 'transport_mode', 'total_value').plot(kind='bar',
                                                              colormap='Set2',
                                                              ylabel=
                                                              'Aportación',
                                                              title=
                                   'Aportación anual de los medios de transporte')

