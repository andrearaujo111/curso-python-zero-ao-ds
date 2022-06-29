# Importa a biblioteca Pandas
import pandas as pd
import numpy as np

# Carrega o arquivo csv
df = pd.read_csv('datasets/kc_house_data.csv')

# # Convete a variável "date" para o formato de data
# df['date'] = pd.to_datetime(df['date'])
#
# # Mostra as primeiras seis linhas
# print(df.head(6))
#
# # Mostra na tela os tipos das variáveis
# print(df.dtypes)

# ================================================================
# COMO CONVERTER TIPOS
# ================================================================

# print('Novos Tipos')
#
# # Inteiro --> Float
# df['bedrooms'] = df['bedrooms'].astype(float)
#
# # Float --> Inteiro
# df['bedrooms'] = df['bedrooms'].astype('int64')
#
# # Inteiro --> String
# df['bedrooms'] = df['bedrooms'].astype(str)
#
# # String --> Inteiro
# df['bedrooms'] = df['bedrooms'].astype('int64')
#
# print(df.dtypes)
# print(df.bedrooms.head(3))

# ================================================================
# CRIANDO NOVAS VARIÁVEIS
# ================================================================

# Criando coluna com um mesmo valor
# df['nome'] = 'andre'
# df['idade'] = 25
# df['data_nascimento'] = pd.to_datetime('1996-08-11')

# ================================================================
# DELETANDO VARIÁVEIS
# ================================================================
# print(df.columns)
# cols = ['nome', 'idade', 'data_nascimento']
# df = df.drop(cols, axis=1)
# print(df.columns)

# ================================================================
# SELECÃO DE DADOS
# ================================================================

# # Pelo nome da coluna
# print(df[['id', 'date']])

# # Pelos índices das linhas e colunas
# dados[linhas, colunas]
# print(df.iloc[0:10, 0:3])
# # Puxa todas as colunas
# print(df.iloc[0:10, :])

# # Pelos índices das linhas e nomes das colunas
# print(df.loc[0:10, 'price'])
# # Maos de uma coluna
# print(df.loc[0:10, ['price', 'id']])

# Pelos índices booleanos
cols =  [True, False, True, True, False, True, False,
         True, False, True, True, False, True, False,
         True, False, True, True, False, True, False
        ]
print(df.loc[0:10, cols])