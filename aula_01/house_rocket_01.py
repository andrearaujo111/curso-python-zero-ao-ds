# Imports
import pandas as pd

# Importing csv file
df = pd.read_csv('datasets/kc_house_data.csv')
# print(df.columns)

# Pergunta 1
print('1. Quantos imóveis estão disponíveis para compra?')
print(f'R: {len(df.id.unique())}')
print('')

# Pergunta 2
# A coluna id e date não são atributos das casas, por isso estão sendo desconsideradas
print('2. Quantos atributos cada imóvel possui? (nº de quartos, número de garagens, m2, etc).')
attributes = df.drop(["id", "date"], axis=1).columns.tolist()
print(f'R: {len(attributes)}')
print('')

# Pergunta 3
print('3. Quais são esses atributos?')
print(f'R: {attributes}')
print('')

# Pergunta 4
print('4. Qual imóvel mais caro do portfólio?')
response_four = df[['id', 'price']].sort_values('price', ascending=False).reset_index(drop=True)[:1]
print(f'R: É o imóvel id:{response_four.id[0]} com o valor de ${response_four.price[0]}')
print('')

# Pergunta 5
print('5.Qual imóvel com maior número de quartos?')
response_five = df[["id", "bedrooms"]].sort_values("bedrooms", ascending=False).reset_index(drop=True)[:1]
print(f'R: É o imóvel id:{response_five.id[0]} com {response_five.bedrooms.values[0]} quartos')
print('')

# Pergunta 6
print('6. Qual a soma de quartos do conjunto de dados?')
print(f'R: {df["bedrooms"].sum()}')
print('')

# Pergunta 7
print('7. Quantos imóveis possuem 2 banheiros?')
two_bathrooms = df['bathrooms'] == 2
print(f'R: {len(df[two_bathrooms].id.drop_duplicates())}')
print('')

# Pergunta 8
print('8. Qual o preço médio de todos os imóveis no conjunto de dados?')
house_prices = df['price'].drop_duplicates()
print(f'R: $ {round(house_prices.mean(), 2)}')
print('')

# Pergunta 9
print('9. Qual o preço médio imóveis com 2 banheiros?')
print(f'R: $ {round(df[two_bathrooms].price.mean(), 2)}')
print('')

# Pergunta 10
print('10. Qual o preço mínimo entre os imóveis com 3 quartos?')
three_bedrooms = df['bedrooms'] == 3
lowest_price_3_bedrooms = df[three_bedrooms][["id", 'price']].sort_values('price', ascending=True).reset_index(drop=True)
print(f'R: O imóvel é o id: {lowest_price_3_bedrooms.id[0]} e o seu preço é: {lowest_price_3_bedrooms.price[0]}')
print('')

# Pergunta 11
print('11. Quantos imóveis possuem mais de 300 m² na sala de estar?')
df['m2'] = df['sqft_living'] * 0.093
print(f'R: {len(df.loc[df.m2 > 300, "id"])}')
print('')

# Pergunta 12
print('12. Quantos imóveis tem mais de 2 andares?')
two_floors = df['floors'] > 2
print(f'R: {df[two_floors].id.size}')
print('')

# Pergunta 13
print('13. Quantos imóveis tem vista para água?')
print(f'R: {int(df.waterfront.value_counts()[1:].values)}')
print('')

# Pergunta 14
print('14. Dos imóveis com vista para água, quantas possuem 3 quartos?')
waterfrontbedrooms = ((df['waterfront'] == 1) & (df['bedrooms'] == 3))
print(f'R: {df[waterfrontbedrooms].id.count()}')
print('')

# Pergunta 15
print('15. Dos imóveis com mais de 300 m² de sala de estar, quantos tem mais de 2 banheiros?')
m2_bathrooms = ((df['m2'] > 300) & (df['bathrooms'] > 2))
print(f'R: {df[m2_bathrooms].id.count()}')
