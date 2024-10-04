import pandas as pd

file = 'Produtos.xlsx'
df1 = pd.read_excel(file, sheet_name='C. Civil')
df2 = pd.read_excel(file, sheet_name='Perfil Pesado')
df3 = pd.read_excel(file, sheet_name='Indústria')
df4 = pd.read_excel(file, sheet_name='Planos e Tubos')

union = pd.concat([df1, df2, df3, df4], ignore_index=True)
union.rename(columns={'Linha': 'line', 'Codigo ': 'code', 'Nome': 'name', 'Peso': 'weight', 'Tamanho': 'size'}, inplace=True)
union.insert(1, 'id', range(1, 1 + len(union)))
union.to_json('products.json', index=False, force_ascii=False, orient='records')
