import bradesco_metricas
import bradesco_sinistro
import bradesco_fatura_tecnica
import minhas_udfs
import pandas as pd
import numpy as np
import math

# Roda métricas
metricas_sinistro = bradesco_metricas.concatenado_metricas_sinistro
metricas_premio = bradesco_metricas.concatenado_metricas_premio

# Roda sinistro
sinistro_apolices = bradesco_sinistro.concatenado_sinistro_apolices
sinistro_valores = bradesco_sinistro.concatenado_sinistro_valores

# Cria uma cópia do dataframe de sinistros
df_sinistro = sinistro_valores.copy()
# Renomeia as colunas para nos acharmos mais facilmente
df_sinistro.rename(
                   columns =
                             {
                              "NOME DO SEGURADO": "NM_TTLR",
                              "NÚMERO DO CERTIFICADO": "CD_TTLR",
                              "CÓDIGO DO PACIENTE": "CD_DPND",
                              "NOME DO PACIENTE": "NM_USRO",
                              "PLANO DO SEGURADO": "CD_PLNO",
                              "NÚMERO DA SUBFATURA": "CD_EMPR_GRPO",
                              "NOME DA SUBFATURA": "DS_EMPR_GRPO",
                              "NÚMERO DO CONTRATO": "CD_APLC",
                              "MATRÍCULA": 'CD_MATR',
                              "MATRICULA ESPECIAL": "CD_MATR_ESPC",
                              "CÓDIGO DO PROCEDIMENTO": "CD_SRVC",
                              "QUANTIDADE PROCEDIMENTOS": "QT_SRVC",
                              "NOME DO BENEFICIÁRIO": "NM_LCAL_UTLZ",
                              "CPF/CGC DO REFERENCIADO": "CD_LCAL_UTLZ",
                              "TIPO DO REFERENCIADO": "TP_LCAL_UTLZ", # Diferencial
                              "VALOR DO SINISTRO": "VL_PAGO_EVNT",
                              "VALOR PAGO": "VL_PAGO_USRO", # Diferencial
                              "VALOR DO RECIBO": "VL_RCBO",
                              "DATA DO PAGAMENTO(Y2K)": "DT_PGTO_EVNT",
                              "DATA DO EVENTO(Y2K)": "DT_ATND",
                              "DATA DE COMPETÊNCIA": "DT_REFR",
                              "DATA DE NASCIMENTO(Y2K)": "DT_NSCM",
                              "SEXO": "FL_SEXO", # pendente de-para
                              "GRAU DE PARENTESCO": "DS_GRAU_PARN", # pendente de-para
                              "ESPECIALIDADE": "NM_ESPC",
                              "TIPO DE EVENTO": "EVNT_OPRD" # pendente de-para
                             },
                   inplace = True
                  )
df_sinistro_columns = df_sinistro.columns

# De-para TIPO DA SUBFATURA
lista_valores = df_sinistro["TIPO DA SUBFATURA"].unique()
for valor in lista_valores:
    df_sinistro["TIPO DA SUBFATURA"] = minhas_udfs.substituir_valor(df_sinistro, "TIPO DA SUBFATURA", valor, metricas_sinistro, "TIPO DA SUBFATURA")

# De-para FL_SEXO
lista_valores = df_sinistro["FL_SEXO"].unique()
for valor in lista_valores:
    df_sinistro["FL_SEXO"] = minhas_udfs.substituir_valor(df_sinistro, "FL_SEXO", valor, metricas_sinistro, "SEXO")

# De-para DS_GRAU_PARN
lista_valores = df_sinistro["DS_GRAU_PARN"].unique()
for valor in lista_valores:
    df_sinistro["DS_GRAU_PARN"] = minhas_udfs.substituir_valor(df_sinistro, "DS_GRAU_PARN", valor, metricas_sinistro, "GRAU DE PARENTESCO")

# De-para EVNT_OPRD
lista_valores = df_sinistro["EVNT_OPRD"].unique()
for valor in lista_valores:
    df_sinistro["EVNT_OPRD"] = minhas_udfs.substituir_valor(df_sinistro, "EVNT_OPRD", valor, metricas_sinistro, "TIPO DE EVENTO")

# De-para CODIGO AUTORIZAÇÃO
lista_valores = df_sinistro["CODIGO AUTORIZAÇÃO"].unique()
for valor in lista_valores:
    df_sinistro["CODIGO AUTORIZAÇÃO"] = minhas_udfs.substituir_valor(df_sinistro, "CODIGO AUTORIZAÇÃO", valor, metricas_sinistro, "TIPO DE EVENTO")

# De-para TIPO DO REFERENCIADO
lista_valores = df_sinistro["TP_LCAL_UTLZ"].unique()
for valor in lista_valores:
    df_sinistro["TP_LCAL_UTLZ"] = minhas_udfs.substituir_valor(df_sinistro, "TP_LCAL_UTLZ", valor, metricas_sinistro, "TIPO DO REFERENCIADO")

# Cria coluna com titularidade
df_sinistro["NM_CATG_USRO"] = np.where(df_sinistro["CD_DPND"] == 0, "T", "D")

# Cria coluna de rede ou reembolso
df_sinistro["NM_REDE_RMBL"] = np.where(df_sinistro["TP_LCAL_UTLZ"] == "", "R", "D")

# Cria novas colunas com referências
df_sinistro["CD_OPRD"] = 1
df_sinistro["CD_EMPR"] = 0

# Calcula a idade do usuário no momento de pagamento
df_sinistro["DT_NSCM"] = pd.to_datetime(df_sinistro["DT_NSCM"], errors='coerce')
df_sinistro["DT_PGTO_EVNT"] = pd.to_datetime(df_sinistro["DT_PGTO_EVNT"], errors='coerce')
df_sinistro['NR_IDDE'] = (df_sinistro['DT_PGTO_EVNT'] - df_sinistro['DT_NSCM']) / np.timedelta64(1, 'Y')
df_sinistro['NR_IDDE'] = df_sinistro['NR_IDDE'].apply(lambda x: math.floor(x))

# Cria coluna com faixa etária
df_sinistro["NM_FAIX_ETRA"] = ""

# Puxa o de-para dos serviços prestados
df_sinistro["DS_SRVC"] = df_sinistro["CD_SRVC"]

# # Cria o código de usuário
# df_sinistro["CD_USRO"] = df_sinistro.apply(lambda row: str(row.CD_TTLR) + "-" + str(row.CD_DPND))

# Puxa o dataframe final
# df_sinistro["CHAVE_JOIN"] = ""
# df_sinistro = df_sinistro[["DT_REFR", "NM_LCAL_UTLZ", "NM_ESPC", "DS_SRVC", "NM_REDE_RMBL", "CD_USRO"]]

# Roda prêmio
premio_headers = bradesco_fatura_tecnica.concatenado_fatura_tecnica_headers
premio_subheaders = bradesco_fatura_tecnica.concatenado_fatura_tecnica_subheaders
premio_valores = bradesco_fatura_tecnica.concatenado_fatura_tecnica_premio

# Cria uma cópia do dataframe de prêmio
df_premio = premio_valores.copy()
# Renomeia as colunas para nos acharmos mais facilmente
df_premio.rename(
                   columns =
                             {
                              "NÚMERO DA SUBFATURA": "CD_EMPR_GRPO",
                              "NÚMERO DO CERTIFICADO": "CD_TTLR",
                              "COMPLEMENTO DO CERTIFICADO": "CD_DPND",
                              "NOME DO SEGURADO/DEPENDENTE ": "NM_USRO",
                              "DATA DE NASCIMENTO": "DT_NSCM",
                              "CÓDIGO SEXO": "FL_SEXO",
                              "CÓDIGO EST. CIVIL": "DS_ESTD_CIVL",
                              "CÓD. GRAU PARENT. DEP.": "FL_GRAU_PRNT",
                              "CÓDIGO DO PLANO": "CD_PLNO",
                              "DATA INÍCIO VIGÊNCIA": "DT_ADMS",
                              "TIPO DE LANÇAMENTO": "TP_LCTO", #DIFERENCIAL
                              "DATA DE LANÇAMENTO": "DT_LCTO", #DIFERENCIAL
                              "CÓDIGO DO LANÇAMENTO": "CD_LCTO", #DIFERENCIAL
                              "VALOR DO LANÇAMENTO": "VL_LCTO",
                              "NÚMERO DA APÓLICE": "CD_APLC",
                              "DATA DE COMPETÊNCIA": "DT_REFR",
                              "NOME DO ESTIPULANTE": "DS_EMPR_GRPO",
                              "MATRICULA ESPECIAL": "CD_MATR_ESPC"
                             },
                   inplace = True
                  )

# Reseta o índice do dataframe de prêmio
df_premio = df_premio.reset_index(drop=True)

# Ajusta sinal do prêmio
df_premio["VL_LCTO"] = np.where((df_premio["CD_LCTO"] >= 50) & (df_premio["CD_LCTO"] <= 99), -df_premio["VL_LCTO"], df_premio["VL_LCTO"])

# Puxa valores de franquia
df_premio_frnq = df_premio.loc[df_premio["TP_LCTO"] == "RS"].copy()
df_premio_frnq["TP_VL_LCTO"] = "VL_FRNQ"
df_premio_frnq["VL_FRNQ"] = df_premio_frnq["VL_LCTO"]

# Puxa valores de aporte
df_premio_aprt = df_premio.loc[
                               ((df_premio["TP_LCTO"] == "AC") & (df_premio["VL_LCTO"] >= 0) & ("APORTE" in df_premio["NM_USRO"])) |
                               ((df_premio["TP_LCTO"] == "AC") & (df_premio["VL_LCTO"] >= 50000))
                              ].copy()
df_premio_aprt["TP_VL_LCTO"] = "VL_APRT"
df_premio_aprt["VL_APRT"] = df_premio_aprt["VL_LCTO"]

# Puxa valores de acerto
df_premio_acrt = df_premio.loc[
                               (df_premio["TP_LCTO"] == "AD") | (df_premio["TP_LCTO"] == "AC")
                              ].copy()
df_premio_acrt["TP_VL_LCTO"] = "VL_ACRT"
df_premio_acrt["VL_ACRT"] = df_premio_acrt["VL_LCTO"]

# Puxa os índices dos dataframes de aporte e acerto para listas
df_premio_acrt_indices = df_premio_acrt.index.tolist()
df_premio_aprt_indices = df_premio_aprt.index.tolist()

# Deleta do dataframe de acerto os índices que já existem no dataframe de aporte
for aprt in df_premio_aprt_indices:
    if aprt in df_premio_acrt_indices:
        df_premio_acrt_indices.remove(aprt)
df_premio_acrt = df_premio_acrt[df_premio_acrt.index.isin(df_premio_acrt_indices)]

# Puxa os valores de prêmio
df_premio_prem = df_premio.loc[(df_premio["TP_LCTO"] != "RS") & (df_premio["TP_LCTO"] != "AC") & (df_premio["TP_LCTO"] != "AD")].copy()
df_premio_prem["TP_VL_LCTO"] = "VL_PREM"
df_premio_prem["VL_PREM"] = df_premio_prem["VL_LCTO"]

# Concatena os dataframes
df_premio = df_premio_prem.append(df_premio_frnq.append(df_premio_aprt.append(df_premio_acrt)))
df_premio = df_premio.drop(columns=["VL_LCTO"])

# Ajusta variáveis separadas de prêmio
minhas_udfs.column_to_currency(df_premio, "VL_PREM")
minhas_udfs.column_to_currency(df_premio, "VL_ACRT")
minhas_udfs.column_to_currency(df_premio, "VL_APRT")
minhas_udfs.column_to_currency(df_premio, "VL_FRNQ")