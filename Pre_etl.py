
##################################################
# **Pré Processamento de dados**                  #
# **Dev: Gabriel Prata                            #
# **Data**: 03/09/2024                            #
# **Última modificação**: 08/09/2024              #
# **Contexto**: Anatel reclamações                #
##################################################

import os
import numpy as np
import pandas as pd
import time

df_anatel = pd.read_csv('reclamacoes_contexto.csv.bz2',
                        encoding="utf-8", sep=';', compression='bz2')

# Data frame com o historico de reclamações
df_hist_rec = (df_anatel[["Ano", "UF", "Serviço", "Marca", "Assunto", "SOLICITAÇÕES"]]
               [(df_anatel["TipoAtendimento"] == "Reclamação")]
               ).groupby(["Ano", "UF", "Serviço", "Marca", "Assunto"])['SOLICITAÇÕES'].sum().reset_index()

# Exportar para csv
df_hist_rec.to_csv('df_hist_rec.csv',  encoding="Latin 1",
                   sep=';', index=False)

# Dataframe agrupado, somente com informação de FIBRA
df_anatel_rec = (df_anatel[["Ano", "Mês", "AnoMês", "UF", "CanalEntrada", "Condição", "TipoAtendimento", "Serviço", "Marca", "Assunto", "Problema", "SOLICITAÇÕES"]]
                 [(df_anatel["TipoAtendimento"] == "Reclamação")
                  & (df_anatel["Serviço"] == "SCM")]
                 ).groupby(["Ano", "Mês", "AnoMês", "UF", "CanalEntrada", "Condição", "TipoAtendimento", "Serviço", "Marca", "Assunto", "Problema"])['SOLICITAÇÕES'].sum().reset_index()

# Exportar para csv
inicio = time.time()  # iniciar contagem do tempo de execução
df_anatel_rec.to_csv('df_anatel_rec.csv.bz2',  encoding="Latin 1",
                     sep=';', index=False, compression='bz2')

fim = time.time()
log_bz2 = fim-inicio
mem_zip = os.path.getsize("df_anatel_rec.csv.bz2")
mem_use = df_anatel.memory_usage(index=True, deep=True).sum()

print('--------------------------------------------------------------------------------------')
print(f"Tempo de compressão: {log_bz2:.2f}s")
print(f"Tamanho do Dataframe: {((mem_use)/1073741824).round(2)} Gb")
print(f"Tamanho do arquivo: {(np.int64(mem_zip)/1048576).round(2)} Mb")
