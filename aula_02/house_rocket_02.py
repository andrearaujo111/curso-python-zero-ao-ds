# Importa a bibliotecas Pandas
import pandas as pd
import plotly.express as px

# Carrega o arquivo csv
df = pd.read_csv('datasets/kc_house_data.csv')

# Tratamento de dados
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# PERGUNTA 1
print('1.Qual a data do imóvel mais antigo do portfólio?')
# ================================================================
ordena_data = df.sort_values('date', ascending=True).reset_index(drop=True)
print(f'R: {ordena_data.loc[0:10, "date"][0]}')
print('')

# PERGUNTA 2
print('2.Quantos imóveis possuem o número máximo de andares?')
# ================================================================
max_andares = df['floors'].drop_duplicates().sort_values(ascending=False).reset_index(drop=True)[0]
count_max_andares = len(df.loc[df["floors"] == max_andares, 'id'])
print(f'R: {count_max_andares} imóveis')
print('')

# PERGUNTA 3
print('3. Criar uma classificação para os imóveis, separando-os em baixo e alto padrão, de acordo com o preço.')
# ================================================================
df['standard'] = ''
df.loc[df['price'] > 540000, 'standard'] = 'high_stardard'
df.loc[df['price'] <= 540000, 'standard'] = 'low_stardard'
print(df[['id', 'price', 'standard']].head())
print('')

# PERGUNTA 4
print('4.Report ordenado por preço e contendo as informações: id, data, preço, quartos, tamanho do terreno e padrão')
# ================================================================
report = df[['id', 'date', 'price',
             'bedrooms', 'sqft_lot', 'standard']].sort_values('price', ascending=False).reset_index(drop=True)
report.to_csv('datasets/report_house_rocket_02.csv', index=False)
print('R: Arquivo gerado na pasta datasets')
print('')

# ================================================================
# NOVAS PERGUNTAS
# ================================================================

# PERGUNTA 1
# ================================================================
print('1. Crie uma nova coluna chamada: “property_age"')
df['property_age'] = df['date'].apply(lambda x: 'new_property' if x >= pd.to_datetime('2014-01-01', format='%Y-%m-%d')
                                      else 'old_property')
print(df['property_age'].head(3))
print('')

# PERGUNTA 2
# ================================================================
print('2. Crie uma nova coluna chamada: “dormitory_type”')
df['dormitory_type'] = df['bedrooms'].apply(lambda x: 'studio' if x == 1 else
                                                      'apartment' if x == 2 else
                                                      'house' if x > 2 else 'NA')
print(df[['bedrooms', 'dormitory_type']].head())
print('')

# PERGUNTA 3
# ================================================================
print('3. Crie uma nova coluna chamada: “condition type”')
df['condition_type'] = df['condition'].apply(lambda x: 'bad' if x <= 2 else
                                                       'regular' if x == 3 or x == 4 else
                                                       'good' if x > 4 else 'NA')
print(df[['condition', 'condition_type']].head(3))
print('')

# PERGUNTA 4
# ================================================================
print('4. Modifique o tipo da coluna “condition” para string')
df['condition'] = df['condition'].astype('string')
print(df['condition'].dtypes)
print('')

# PERGUNTA 5
# ================================================================
print('5.Delete as colunas “sqft_living15” e “sqft_lot15”')
cols = ['sqft_living15', 'sqft_lot15']
df = df.drop(cols, axis=1)
print(df.columns)
print('')

# PERGUNTA 6
# ================================================================
print('6. Modifique o TIPO da oluna “yr_build” para DATE')
df['yr_built'] = df['yr_built'].astype('int64')
df['yr_built'] = pd.to_datetime(df['yr_built'], format='%Y')
print(df['yr_built'].head(3))
print('')

# PERGUNTA 7
# ===============================================================
print('7. Modifique o TIPO da coluna “yr_renovated” para DATE')
df['yr_renovated'] = df['yr_renovated'].apply(lambda x: x if x == 0 else pd.to_datetime(x, format='%Y'))
print(df['yr_renovated'].head(5))
print('')

# PERGUNTA 8
# ===============================================================
print('8.Qual a data mais antiga de construção de um imóvel?')
mais_antiga = pd.DatetimeIndex(df['yr_built']).year
print(mais_antiga.min())
print('')

# PERGUNTA 9
# ===============================================================
print('9.Qual a data mais antiga de renovação de um imóvel?')
sem_data_reforma = df['yr_renovated'] == 0
datas_reforma = df[~sem_data_reforma]['yr_renovated'].reset_index(drop=True)
mais_antiga_renovada = pd.DatetimeIndex(datas_reforma).year
print(mais_antiga_renovada.min())
print('')

# PERGUNTA 10
# ===============================================================
print('10.Quantos imóveis têm dois andares?')
dois_andares = df['floors'] == 2
print(df[dois_andares]['id'].count())
print('')

# PERGUNTA 11
# ===============================================================
print('11.Quantos imóveis estão com a condição igual a “regular” ?')
condicao_regular = df['condition_type'] == 'regular'
print(df[condicao_regular]['id'].count())
print('')

# PERGUNTA 12
# ===============================================================
print('12.Quantos imóveis estão com a condição igual a “bad”e possuem “vista para água” ?')
bad_e_vista_para_agua = ((df['condition_type'] == 'bad') & (df['waterfront'] == 1))
print(df[bad_e_vista_para_agua]['id'].count())
print('')

# PERGUNTA 13
# ===============================================================
print('13.Quantos imóveis estão com a condição igual a “good” e são “new_property”?')
good_e_new_property = ((df['condition_type'] == 'good') & (df['property_age']) == 'new_property')
print(df[good_e_new_property].shape[0])
print('')

# PERGUNTA 14
# ===============================================================
print('14.Qual o valor do imóvel mais caro do tipo “studio” ?')
studios = df['dormitory_type'] == 'studio'
print(df[studios]['price'].sort_values(ascending=False).reset_index(drop=True)[0])
print('')

# PERGUNTA 15
# ===============================================================
print('15.Quantos imóveis do tipo “apartment” foram reformados em 2015?')
df_reformados = df[~sem_data_reforma].reset_index(drop=True)
reformados_tipo_apartment = ((df_reformados['dormitory_type'] == 'apartment') &
                             (pd.DatetimeIndex(df_reformados['yr_renovated']) == 2015))
print(df_reformados[reformados_tipo_apartment].shape[0])
print('')

# PERGUNTA 16
# ===============================================================
print('16.Qual o maior número de quartos que um imóveis do tipo “house” possui ?')
df_house = df[df['dormitory_type'] == 'house']
print(df_house['bedrooms'].sort_values(ascending=False).reset_index(drop=True)[0])
print('')

# PERGUNTA 17
# ===============================================================
print('17.Quantos imóveis “new_property” foram reformados no ano de 2014?')
print(df.loc[((df['property_age'] == 'new_house') &
     (df['yr_renovated'] == '2014-01-01')), 'id'].size)
print('')

# PERGUNTA 18
# ===============================================================
print('18.Selecione as colunas: “id”, “date”, “price”, “floors”, “zipcode” pelo método:')
# Direto pelo nome das colunas
print(df[['id', 'date', 'price', 'floors', 'zipcode']].head(3))
# Pelos índices
indices = [0, 1, 2, 7, 16]
print(df.iloc[0:3, indices])
# Pelos índices das linhas e nomes das colunas
print(df.loc[0:2, ['id', 'date', 'price', 'floors', 'zipcode']])
print('')

# PERGUNTA 19
# ===============================================================
print('19.Salve um arquivo csv com somente as colunas do item 10 ao 17')
df.to_csv('datasets/report_house_rocket_v2', index=False)

# PERGUNTA 20
print('20. Mapa indicando onde as casas estão localizadas geograficamente.')
# ================================================================
df_map = df[['id', 'price', 'lat', 'long']]

hr_map = px.scatter_mapbox(df_map, lat='lat', lon='long', hover_name='id',
                           hover_data=['price'],
                           color_discrete_sequence=['darkgreen'],
                           zoom=6, height=300
                           )

hr_map.update_layout(mapbox_style='open-street-map')
hr_map.update_layout(height=600, margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
hr_map.write_html('datasets/house_rocket_map_01.html')
