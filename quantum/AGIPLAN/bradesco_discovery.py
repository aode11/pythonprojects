import pandas as pd
import bradesco_sinistro
import bradesco_fatura_tecnica
import bradesco_metricas
import minhas_udfs
    
# Exporta os findings para um Excel, a fim de validar a transformação
writer = pd.ExcelWriter(minhas_udfs.call_today() + 'DiscoveryBradesco.xlsx', engine='xlsxwriter')

# Roda sinistro
bradesco_sinistro.concatenado_sinistro_apolices.to_excel(writer, sheet_name = "Sinistro - Apólices", index = False)
bradesco_sinistro.concatenado_sinistro_valores.to_excel(writer, sheet_name = "Sinistro - Valores", index = False)

# Roda prêmio
bradesco_fatura_tecnica.concatenado_fatura_tecnica_headers.to_excel(writer, sheet_name = "Prêmio - Headers", index = False)
bradesco_fatura_tecnica.concatenado_fatura_tecnica_subheaders.to_excel(writer, sheet_name = "Prêmio - Subheaders", index = False)
bradesco_fatura_tecnica.concatenado_fatura_tecnica_subheaders.to_excel(writer, sheet_name = "Prêmio - Valores", index = False)

# Roda métricas
bradesco_metricas.concatenado_metricas_sinistro.to_excel(writer, sheet_name = "Sinistro - Métricas", index = False)
bradesco_metricas.concatenado_metricas_premio.to_excel(writer, sheet_name = "Prêmio - Métricas", index = False)

# Salva e fecha o Excel
writer.save()
writer.close()