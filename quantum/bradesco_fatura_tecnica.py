import os
import pandas as pd
import minhas_udfs


# Altera definição padrão de formato de decimais no pandas
pd.set_option('display.float_format', lambda x: '15.2f' % x)

# Parâmetros do layout da Bradesco
parametro_fatura_tecnica_header_widths = [1, 30, 35, 3, 3, 6, 3, 35, 6, 8, 50]
parametro_fatura_tecnica_header_headers = ["TIPO DE REGISTRO", "TIPO DE ARQUIVO", "NOME  DO ESTIPULANTE", "CÓDIGO DA COMPANHIA",
                                           "CÓDIGO DA SUCURSAL", "CÓDIGO DO CONTRATO", "CÓDIGO DO RAMO", "DESCRIÇÃO DO RAMO",
                                           "COMPETÊNCIA DA FATURA", "DATA DO PROCESSAMENTO", "FILLER"]
parametro_fatura_tecnica_subheader_widths = [1, 2, 4, 35, 138]
parametro_fatura_tecnica_subheader_headers = ["TIPO DE REGISTRO", "SEQUÊNCIA DA FATURA", "NÚMERO DA SUBFATURA", "NOME  DA SUBFATURA", "FILLER"]
parametro_fatura_tecnica_premio_widths = [1, 4, 7, 2, 35, 4, 8, 1, 1, 1, 4, 8, 2, 6, 15, 15, 2, 20, 12, 32]
parametro_fatura_tecnica_premio_headers = ["TIPO DE REGISTRO", "NÚMERO DA SUBFATURA", "NÚMERO DO CERTIFICADO", "COMPLEMENTO DO CERTIFICADO",
                                           "NOME DO SEGURADO/DEPENDENTE ", "INDIC. SUBF. ANTER/ATUAL", "DATA DE NASCIMENTO", "CÓDIGO SEXO",
                                           "CÓDIGO EST. CIVIL", "CÓD. GRAU PARENT. DEP.", "CÓDIGO DO PLANO", "DATA INÍCIO VIGÊNCIA",
                                           "TIPO DE LANÇAMENTO", "DATA DE LANÇAMENTO", "VALOR DO LANÇAMENTO", "PARTE DO SEGURADO",
                                           "CÓDIGO DO LANÇAMENTO", "CARGO / OCUPAÇÃO", "MATRICULA ESPECIAL", "FILLER"]

# Cria listas vazias para auxiliar o processo
lista_fatura_tecnica_arquivos = []
lista_fatura_tecnica_headers = []
lista_fatura_tecnica_subheaders = []
lista_fatura_tecnica_premio = []

# Busca os arquivos no diretório, e filtra para termos apenas os arquivos .txt
for arquivo_fatura_tecnica in list(map(lambda x: x.lower(), os.listdir())):
    if '.txt' in arquivo_fatura_tecnica:
        lista_fatura_tecnica_arquivos.append(arquivo_fatura_tecnica)

# Roda para todos os arquivos .txt
for arquivo_fatura_tecnica in lista_fatura_tecnica_arquivos:
    
    # Usa as variáveis definidas inicialmente para importar o arquivo delimitado por largura em dataframes
    dataframe_fatura_tecnica_headers = pd.read_fwf(
                                                   arquivo_fatura_tecnica, 
                                                   encoding = "ISO-8859-1",
                                                   header = None,
                                                   widths = parametro_fatura_tecnica_header_widths
                                                  )
    dataframe_fatura_tecnica_subheaders = pd.read_fwf(
                                                      arquivo_fatura_tecnica,
                                                      encoding = "ISO-8859-1",
                                                      header = None,
                                                      widths = parametro_fatura_tecnica_subheader_widths
                                                     )
    dataframe_fatura_tecnica_premio = pd.read_fwf(
                                                  arquivo_fatura_tecnica,
                                                  encoding = "ISO-8859-1",
                                                  header = None,
                                                  widths = parametro_fatura_tecnica_premio_widths
                                                 )
    
    # Dá o nome das colunas de cada dataframe
    dataframe_fatura_tecnica_headers.columns = parametro_fatura_tecnica_header_headers
    dataframe_fatura_tecnica_subheaders.columns = parametro_fatura_tecnica_subheader_headers
    dataframe_fatura_tecnica_premio.columns = parametro_fatura_tecnica_premio_headers
    
    # Altera o tipo de variável da primeira coluna dos dataframes, para maior consistência
    dataframe_fatura_tecnica_headers["TIPO DE REGISTRO"] = pd.to_numeric(
                                                                         dataframe_fatura_tecnica_headers["TIPO DE REGISTRO"],
                                                                         errors='coerce'
                                                                        )
    dataframe_fatura_tecnica_subheaders["TIPO DE REGISTRO"] = pd.to_numeric(
                                                                            dataframe_fatura_tecnica_subheaders["TIPO DE REGISTRO"],
                                                                            errors='coerce'
                                                                           )
    dataframe_fatura_tecnica_premio["TIPO DE REGISTRO"] = pd.to_numeric(
                                                                        dataframe_fatura_tecnica_premio["TIPO DE REGISTRO"],
                                                                        errors='coerce'
                                                                       )
    
    # Filtra os dataframes para apenas trazerem os dados corretos de cada layout
    dataframe_fatura_tecnica_headers = dataframe_fatura_tecnica_headers.loc[dataframe_fatura_tecnica_headers["TIPO DE REGISTRO"] == 1]
    dataframe_fatura_tecnica_subheaders = dataframe_fatura_tecnica_subheaders.loc[dataframe_fatura_tecnica_subheaders["TIPO DE REGISTRO"] == 2]
    dataframe_fatura_tecnica_premio = dataframe_fatura_tecnica_premio.loc[dataframe_fatura_tecnica_premio["TIPO DE REGISTRO"] == 3]
    
    # Verifica se o que estamos tratando é um arquivo de fatura tecnica
    if len(dataframe_fatura_tecnica_headers) > 0:
        if dataframe_fatura_tecnica_headers.iloc[0]["TIPO DE ARQUIVO"] == "FATURA TECNICA":
            
            # Derruba colunas desnecessárias
            dataframe_fatura_tecnica_headers = dataframe_fatura_tecnica_headers.drop(
                                                                                     ["TIPO DE REGISTRO", "FILLER", "TIPO DE ARQUIVO"],
                                                                                     axis='columns'
                                                                                    )
            dataframe_fatura_tecnica_subheaders = dataframe_fatura_tecnica_subheaders.drop(
                                                                                           ["TIPO DE REGISTRO", "FILLER"],
                                                                                           axis='columns'
                                                                                          )
            dataframe_fatura_tecnica_premio = dataframe_fatura_tecnica_premio.drop(
                                                                                   ["TIPO DE REGISTRO", "FILLER"],
                                                                                   axis='columns'
                                                                                  )
            
            # Ajusta formatos de colunas
            minhas_udfs.column_to_datetime(dataframe_fatura_tecnica_headers, "COMPETÊNCIA DA FATURA", '%Y%m', '01/%m/%Y')
            minhas_udfs.column_to_datetime(dataframe_fatura_tecnica_headers, "DATA DO PROCESSAMENTO", '%Y%m%d', '%d/%m/%Y')
            minhas_udfs.column_to_datetime(dataframe_fatura_tecnica_premio, "DATA DE NASCIMENTO", '%d%m%Y', '%d/%m/%Y')
            minhas_udfs.column_to_datetime(dataframe_fatura_tecnica_premio, "DATA INÍCIO VIGÊNCIA", '%d%m%Y', '%d/%m/%Y')
            minhas_udfs.column_to_datetime(dataframe_fatura_tecnica_premio, "DATA DE LANÇAMENTO", '%d%m%Y', '%d/%m/%Y')
            minhas_udfs.column_to_currency(dataframe_fatura_tecnica_premio, "VALOR DO LANÇAMENTO")
            minhas_udfs.column_to_currency(dataframe_fatura_tecnica_premio, "PARTE DO SEGURADO")
            dataframe_fatura_tecnica_premio["CÓDIGO DO LANÇAMENTO"] = pd.to_numeric(
                                                                                    dataframe_fatura_tecnica_premio["CÓDIGO DO LANÇAMENTO"],
                                                                                    errors='coerce'
                                                                                   )
            
    
            # Traz os parâmetros para o dataframe de dados
            dataframe_fatura_tecnica_premio["NÚMERO DA APÓLICE"] = dataframe_fatura_tecnica_headers.iloc[0]["CÓDIGO DO CONTRATO"]
            dataframe_fatura_tecnica_premio["DATA DE COMPETÊNCIA"] = dataframe_fatura_tecnica_headers.iloc[0]["COMPETÊNCIA DA FATURA"]
            dataframe_fatura_tecnica_premio["NOME DO ESTIPULANTE"] = dataframe_fatura_tecnica_headers.iloc[0]["NOME  DO ESTIPULANTE"]
            
            # Traz o nome do arquivo para o dataframe de apolices
            dataframe_fatura_tecnica_headers["ARQUIVO"] = arquivo_fatura_tecnica
            
            # Concatena os dataframes nas nossas listas
            lista_fatura_tecnica_headers.append(dataframe_fatura_tecnica_headers)
            lista_fatura_tecnica_subheaders.append(dataframe_fatura_tecnica_subheaders)
            lista_fatura_tecnica_premio.append(dataframe_fatura_tecnica_premio)

# Concatena a lista em dataframes a serem exportados
concatenado_fatura_tecnica_headers = pd.concat(lista_fatura_tecnica_headers)
concatenado_fatura_tecnica_subheaders = pd.concat(lista_fatura_tecnica_subheaders)
concatenado_fatura_tecnica_premio = pd.concat(lista_fatura_tecnica_premio)