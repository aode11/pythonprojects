import os
import pandas as pd
import minhas_udfs

# Altera definição padrão de formato de decimais no pandas
pd.set_option('display.float_format', lambda x: '15.2f' % x)

# Parâmetros do layout da Bradesco
parametro_sinistro_apolice_widths = [1, 15, 6, 4, 6, 362, 6, 8, 92]
parametro_sinistro_apolice_headers = ["TIPO DE ARQUIVO", "TIPO DE REGISTRO", "NÚMERO DA APÓLICE", "DATA DE COMPETÊNCIA", "DATA DE PROCESSAMENTO",
                                      "FILLER", "DATA DE COMPETÊNCIA(Y2K)", "DATA DE PROCESSAMENTO(Y2K)", "FILLER"]
parametro_sinistro_valores_widths = [1, 3, 35, 2, 7, 10, 35, 2, 35, 35, 1, 10, 8, 2, 6, 14, 6, 6, 10, 2, 112, 6, 1, 1, 2, 14, 12, 2, 2, 14, 1, 14,
                                     14, 20, 8, 4, 8, 8, 8, 8, 1, 10]
parametro_sinistro_valores_headers = ["TIPO DE REGISTRO", "NÚMERO DA SUBFATURA", "NOME DA SUBFATURA", "TIPO DA SUBFATURA", "NÚMERO DO CERTIFICADO",
                                      "MATRÍCULA", "NOME DO SEGURADO", "CÓDIGO DO PACIENTE", "NOME DO PACIENTE", "NOME DO BENEFICIÁRIO",
                                      "TIPO DE EVENTO", "NÚMERO DO DOCUMENTO", "CÓDIGO DO PROCEDIMENTO", "QUANTIDADE PROCEDIMENTOS",
                                      "DATA DO PAGAMENTO", "VALOR PAGO", "DATA DO EVENTO", "NÚMERO DO CONTRATO", "CÓDIGO DO REFERENCIADO",
                                      "SADT PARA PACIENTE INTERNADO", "FILLER", "DATA DE NASCIMENTO", "SEXO", "GRAU DE PARENTESCO", "ESPECIALIDADE",
                                      "VALOR DO SINISTRO", "MATRICULA ESPECIAL", "FILLER", "CODIGO AUTORIZAÇÃO", "CPF/CGC DO REFERENCIADO",
                                      "TIPO DO REFERENCIADO", "VALOR DE INSS OU ISS", "VALOR DE INSS OU ISS", "CARGO DO SEGURADO",
                                      "DATA DE ADMISSÃO", "PLANO DO SEGURADO", "CDB", "DATA DO PAGAMENTO(Y2K)", "DATA DO EVENTO(Y2K)",
                                      "DATA DE NASCIMENTO(Y2K)", "TROCA DE ACOMODAÇÃO", "VALOR DO RECIBO"]

# Cria listas vazias para auxiliar o processo
lista_sinistro_arquivos = []
lista_sinistro_apolices = []
lista_sinistro_valores = []

# Busca os arquivos no diretório, e filtra para termos apenas os arquivos .txt
for arquivo_sinistro in list(map(lambda x: x.lower(), os.listdir())):
    if '.txt' in arquivo_sinistro:
        lista_sinistro_arquivos.append(arquivo_sinistro)

# Roda para todos os arquivos .txt
for arquivo_sinistro in lista_sinistro_arquivos:
            
    # Usa as variáveis definidas inicialmente para importar o arquivo delimitado por largura em dataframes
    dataframe_sinistro_apolices = pd.read_fwf(
                                              arquivo_sinistro,
                                              encoding = "ISO-8859-1",
                                              header = None,
                                              widths = parametro_sinistro_apolice_widths
                                             )
    dataframe_sinistro_valores = pd.read_fwf(
                                             arquivo_sinistro,
                                             encoding = "ISO-8859-1",
                                             header = None,
                                             widths = parametro_sinistro_valores_widths
                                            )
    
    # Dá o nome das colunas de cada dataframe
    dataframe_sinistro_apolices.columns = parametro_sinistro_apolice_headers
    dataframe_sinistro_valores.columns = parametro_sinistro_valores_headers
    
    # Filtra os dataframes para apenas trazerem os dados corretos de cada layout
    dataframe_sinistro_apolices = dataframe_sinistro_apolices.loc[dataframe_sinistro_valores["TIPO DE REGISTRO"] == "H"]
    dataframe_sinistro_valores = dataframe_sinistro_valores.loc[dataframe_sinistro_valores["TIPO DE REGISTRO"] == "M"]
    
    # Verifica se o que estamos tratando é um arquivo de sinistro
    if len(dataframe_sinistro_apolices) > 0:
        if dataframe_sinistro_apolices.iloc[0]["TIPO DE REGISTRO"] == "SINISTROS PAGOS":
        
            # Derruba colunas desnecessárias
            dataframe_sinistro_apolices = dataframe_sinistro_apolices.drop(
                                                                           ["TIPO DE ARQUIVO", "TIPO DE REGISTRO", "FILLER", "DATA DE COMPETÊNCIA",
                                                                           "DATA DE PROCESSAMENTO"],
                                                                           axis='columns'
                                                                          )
            dataframe_sinistro_valores = dataframe_sinistro_valores.drop(["TIPO DE REGISTRO", "FILLER", "DATA DO PAGAMENTO", "DATA DO EVENTO",
                                                                          "DATA DE NASCIMENTO"],
                                                                          axis='columns')
            
            # Ajusta formatos de colunas
            minhas_udfs.column_to_datetime(dataframe_sinistro_apolices, "DATA DE COMPETÊNCIA(Y2K)", '%Y%m', '01/%m/%Y')
            minhas_udfs.column_to_datetime(dataframe_sinistro_apolices, "DATA DE PROCESSAMENTO(Y2K)", '%Y%m%d', '%d/%m/%Y')
            minhas_udfs.column_to_datetime(dataframe_sinistro_valores, "DATA DE ADMISSÃO", '%Y%m%d', '%d/%m/%Y')
            minhas_udfs.column_to_datetime(dataframe_sinistro_valores, "DATA DO PAGAMENTO(Y2K)", '%Y%m%d', '%d/%m/%Y')
            minhas_udfs.column_to_datetime(dataframe_sinistro_valores, "DATA DO EVENTO(Y2K)", '%Y%m%d', '%d/%m/%Y')
            minhas_udfs.column_to_datetime(dataframe_sinistro_valores, "DATA DE NASCIMENTO(Y2K)", '%Y%m%d', '%d/%m/%Y')
            minhas_udfs.column_to_currency(dataframe_sinistro_valores, "VALOR PAGO")
            minhas_udfs.column_to_currency(dataframe_sinistro_valores, "VALOR DO SINISTRO")
            minhas_udfs.column_to_currency(dataframe_sinistro_valores, "VALOR DE INSS OU ISS")
            minhas_udfs.column_to_currency(dataframe_sinistro_valores, "VALOR DO RECIBO")
        
            # Traz os parâmetros para o dataframe de dados
#            dataframe_sinistro_valores["NÚMERO DA APÓLICE"] = dataframe_sinistro_apolices.iloc[0]["NÚMERO DA APÓLICE"]
            dataframe_sinistro_valores["DATA DE COMPETÊNCIA"] = dataframe_sinistro_apolices.iloc[0]["DATA DE COMPETÊNCIA(Y2K)"]
            
            # Traz o nome do arquivo para o dataframe de apolices
            dataframe_sinistro_apolices["ARQUIVO"] = arquivo_sinistro
            
            # Concatena os dataframes nas nossas listas
            lista_sinistro_apolices.append(dataframe_sinistro_apolices)
            lista_sinistro_valores.append(dataframe_sinistro_valores)

# Concatena a lista em dataframes a serem exportados
concatenado_sinistro_apolices = pd.concat(lista_sinistro_apolices)
concatenado_sinistro_valores = pd.concat(lista_sinistro_valores)