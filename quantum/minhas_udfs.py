import pandas as pd
from datetime import datetime
from datetime import date

# UDF para lidar com ajuste de formato de datas em colunas do pandas
def column_to_datetime(df, df_column, informat, outformat):
    df[df_column] = pd.to_datetime(df[df_column], format=informat, errors='coerce').dt.strftime(outformat)
    return column_to_datetime

# UDF para ajustar colunas de valores monetários do pandas
def column_to_currency(df, df_column):
    try:
        df[df_column] = pd.to_numeric(df[df_column])
    except:
        df[df_column] = df[df_column]
    df[df_column] = df[df_column].div(100)
    return column_to_currency

# UDF para chamar uma string com timestamp formatado
def call_timestamp():
    return datetime.now().strftime('[%Y-%m-%d_-_%Hh%Mm%Ss]')

# UDF para chamar uma string data formatada
def call_today():
    return datetime.now().strftime('[%Y-%m-%d]')

def substituir_valor(df, df_column, df_value, df_lookup, df_lookup_term):
    return df[df_column].replace(df_value, df_lookup["TRADUCAO"].loc[(df_lookup.METRICA == df_lookup_term) & (df_lookup.VALOR == df_value)].str.cat())

# UDF para lidar com diversos formatos de data
def ajustar_data(text):
    for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            return text