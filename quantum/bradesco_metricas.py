import pandas as pd

## Cria de-paras para o arquivo de Sinistro

# Tipo da Subfatura
dataframe_metricas_subfatura = pd.DataFrame({
    "TIPO": "SINISTRO",
    "PARAMETRO": 1,
    "METRICA": "TIPO DA SUBFATURA",
    "VALOR": [1, 2, 3],
    "TRADUCAO": ["Técnica", "Cancelada", "Administrativa"]})

# Tipo do Evento
dataframe_metricas_evento = pd.DataFrame({
    "TIPO": "SINISTRO",
    "PARAMETRO": 2,
    "METRICA": "TIPO DE EVENTO",
    "VALOR": [1, 2, 3, 4, 5, 6, 7, 8, 9, 0],
    "TRADUCAO": ["Consulta", "Evento", "Desp. Hosp", "Hon. Méd.", "Ex. Simples", "Ex. Espec", "Cl. Esp", "Farmácia", "Ter Inf", "Sin Man"]})

# Sexo
dataframe_metricas_sexo = pd.DataFrame({
    "TIPO": "SINISTRO",
    "PARAMETRO": 3,
    "METRICA": "SEXO",
    "VALOR": [1, 2],
    "TRADUCAO": ["Masculino", "Feminino"]})

# Grau de Parentesco
dataframe_metricas_parentesco = pd.DataFrame({
    "TIPO": "SINISTRO",
    "PARAMETRO": 4,
    "METRICA": "GRAU DE PARENTESCO",
    "VALOR": [1, 2, 3, 4, 5, 6, 7, 8, 0],
    "TRADUCAO": ["Cônjuge", "Filho", "Mãe", "Pai", "Sogro", "Sogra", "Tutelado", "Outros", "Titular"]})

# Código Autorização
dataframe_metricas_autorizacao = pd.DataFrame({
    "TIPO": "SINISTRO",
    "PARAMETRO": 5,
    "METRICA": "CODIGO AUTORIZAÇÃO",
    "VALOR": [1, 2, 3, 4, 5, 6, 7, 8, 9],
    "TRADUCAO": ["Segurado Novo", "Extravio ou perda do cartão", "Admissional", "Demissional", "Periódico", "Acidente de trabalho", "Outros", "Assistência a demitidos", "Medicina social"]})

# Tipo do Referenciado
dataframe_metricas_referenciado = pd.DataFrame({
    "TIPO": "SINISTRO",
    "PARAMETRO": 6,
    "METRICA": "TIPO DO REFERENCIADO",
    "VALOR": ["", "F", "J"],
    "TRADUCAO": ["Reembolso", "Física", "Jurídica"]})

# Cria uma lista com os dataframes
lista_metricas_sinistro = [dataframe_metricas_subfatura, dataframe_metricas_evento, dataframe_metricas_sexo, dataframe_metricas_parentesco, dataframe_metricas_autorizacao, dataframe_metricas_referenciado]

# Concatena os dataframes na lista
concatenado_metricas_sinistro = pd.concat(lista_metricas_sinistro)

### Cria de-paras para as métricas da Fatura Tecnica

# Código Est. Civil
dataframe_metricas_sexo = pd.DataFrame({
    "TIPO": "PREMIO",
    "PARAMETRO": 1,
    "METRICA": "SEXO",
    "VALOR": [1, 2],
    "TRADUCAO": ["Masculino", "Feminino"]})

# Código Est. Civil
dataframe_metricas_estado_civil = pd.DataFrame({
    "TIPO": "PREMIO",
    "PARAMETRO": 2,
    "METRICA": "CÓDIGO EST. CIVIL",
    "VALOR": [1, 2, 3, 4],
    "TRADUCAO": ["Solteiro", "Casado", "Viúvo", "Outros"]})

# Grau de Parentesco
dataframe_metricas_parentesco = pd.DataFrame({
    "TIPO": "PREMIO",
    "PARAMETRO": 3,
    "METRICA": "GRAU DE PARENTESCO",
    "VALOR": [1, 2, 3, 4, 5, 6, 7, 8],
    "TRADUCAO": ["Cônjuge", "Filho", "Mãe", "Pai", "Sogro", "Sogra", "Tutelado", "Outros"]})

# Tipo de Lançamento
dataframe_metricas_lancamento = pd.DataFrame({
    "TIPO": "PREMIO",
    "PARAMETRO": 4,
    "METRICA": "TIPO DE LANÇAMENTO",
    "VALOR": [" ", "AC", "AD", "AM", "AR", "CM", "CR", "IM", "IR", "RM", "RR", "TM", "TR"],
    "TRADUCAO": ["Segurados Remanescentes", "Acerto Prêmio Cobrança", "Acerto Prêmio Devolução", "Alterações no Mês", "Alterações Retroativas", "Cancelamentos no Mês", "Cancelamentos Retroativos", "Inclusões no Mês", "Inclusões Retroativas", "Reativações no Mês", "Reativações Retroativas", "Transferências no Mês", "Transferências Retroativas"]})

# Cria uma lista com os dataframes
lista_metricas_premio = [dataframe_metricas_sexo, dataframe_metricas_estado_civil, dataframe_metricas_parentesco, dataframe_metricas_lancamento]

# Concatena os dataframes na lista
concatenado_metricas_premio = pd.concat(lista_metricas_premio)