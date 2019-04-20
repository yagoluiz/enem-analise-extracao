library(readr) # biblioteca para leitura de arquivos externos
library(ggplot2) # biblioteca para geracao de graficos
library(dplyr) # biblioteca para manipulacao de dados
library(arules) # biblioteca para algoritmo apriori
library(arulesViz) # biblioteca para geracao de grafico de regras de associacao

# leitura do arquivo .csv
csv_enem <- read_csv("C:/Dev/R/MICRODADOS_ENEM_CENTRO_OESTE_CATEGORIZADOS_2015.csv")

# visualizacao do arquivo .csv
View(csv_enem)

# visualizacao em nova janela
windows()

# ------------------------------ EXPLORACAO DOS DADOS ------------------------------ #

# grafico blox-plot das medias das notas em relacao ao sexo
qplot(data=csv_enem, x=csv_enem$TP_SEXO, y=csv_enem$NU_NOTA_MEDIA, ylab="Média de Notas", xlab="Sexo", geom="boxplot")

# grafico de de barras com a quantidade de pessoas nas UF's por renda declarada
qplot(data=csv_enem, x=csv_enem$CO_UF_RESIDENCIA, fill=csv_enem$QS_RENDA, ylab="Renda", xlab="UF") + scale_fill_discrete(name="Renda declarada")

# histograma com desempenho dos alunos
qplot(x=csv_enem$NU_NOTA_MEDIA, xlab="Desempenho dos Alunos", binwidth=15, geom="histogram", col=I("black")) + ylab("Quantidade")

# ------------------------------ MINERACAO DOS DADOS ------------------------------ #

# transformar fatores de dataframe
csv_frame <- as.data.frame(unclass(csv_enem))

# visualizar tipo de dados do frame
str(csv_frame)

# visualizar sumarizacao dos dados
summary(csv_frame)

# frame com todos os dados categoricos
frame_alg <- csv_frame[,c('NU_IDADE_CAT', 'TP_SEXO', 'TP_ESCOLA', 'TP_ENSINO', 'TP_ST_CONCLUSAO',
                        'TP_COR_RACA', 'TP_LINGUA', 'NU_NOTA_MEDIA_CAT', 'QS_ESCOLARIDADE_PAI',
                        'QS_ESCOLARIDADE_MAE', 'QS_RENDA', 'QS_QTD_RESIDENCIA_CAT',
                        'QS_ABANDONO_REPROVACAO_FUNDAMENTAL', 'QS_ABANDONO_REPROVACAO_MEDIO',
                        'QS_ESCOLA_FUNDAMENTAL', 'QS_ESCOLA_MEDIO')]

# algoritmo apriori nos dados categorizados
alg_apriori <- apriori(frame_alg, parameter = list(support = 0.1, confidence = 0.8))

# grafico de suporte e confianca das regras geradas
plot(alg_apriori)

# matriz com regras geradas
plot(alg_apriori, method="matrix", measure="lift", control=list(reorder=TRUE))

# ordenar resultado para organizar frame
alg_apriori <- sort(alg_apriori, by = "support")

# resultado do algoritmo em frame
result_apriori = data.frame(  
  antecedente = labels(lhs(alg_apriori)),  
  consequente = labels(rhs(alg_apriori)),  
  alg_apriori@quality)

# resultado com suporte minimo de 70%
result_apriori <- filter(result_apriori, result_apriori$support >= 0.7)

# frame com todos os dados do questionario socieconomico
frame_qs_alg <- csv_frame[,c('NU_NOTA_MEDIA_CAT', 'QS_ESCOLARIDADE_PAI', 'QS_ESCOLARIDADE_MAE', 'QS_RENDA',
                            'QS_QTD_RESIDENCIA_CAT', 'QS_ATIVIDADE_REMUNERADA', 'QS_ABANDONO_REPROVACAO_FUNDAMENTAL',
                            'QS_ABANDONO_REPROVACAO_MEDIO', 'QS_ESCOLA_FUNDAMENTAL', 'QS_ESCOLA_MEDIO')]

# algoritmo apriori no dados socieconomicos
alg_qs_apriori <- apriori(frame_qs_alg, parameter = list(support = 0.1, confidence = 0.8))

# grafico de suporte e confianca das regras geradas
plot(alg_qs_apriori)

# grafo das regras geradas
plot(alg_qs_apriori, method="graph", control=list(type="items"))

# matriz com regras geradas
plot(alg_qs_apriori, method="matrix", measure="lift", control=list(reorder=TRUE))

# ordenar resultado para organizar frame
alg_qs_apriori <- sort(alg_qs_apriori, by = "support")

# resultado do algoritmo em frame
alg_qs_apriori = data.frame(  
  antecedente = labels(lhs(alg_qs_apriori)),  
  consequente = labels(rhs(alg_qs_apriori)),  
  alg_qs_apriori@quality)

# resultado com suporte minimo de 50%
alg_qs_apriori <- filter(alg_qs_apriori, alg_qs_apriori$support >= 0.5)

# ------------------------------ ANALISE MINERACAO DOS DADOS ------------------------------ #

# grafico de barras com a media das notas em relacao a renda declarada
qplot(data=csv_enem, x=csv_enem$QS_RENDA, fill=csv_enem$NU_NOTA_MEDIA_CAT, ylab="Quantidade", xlab="Renda") + scale_fill_discrete(name="Pontuação")

# grafico de barras com a escola e renda declarada
qplot(data=csv_enem, x=csv_enem$TP_ESCOLA, fill=csv_enem$QS_RENDA, ylab="Quantidade", xlab="Tipo de escola") + scale_fill_discrete(name="Renda declarada")

# grafico de barras com a escola e a media das notas
qplot(data=csv_enem, x=csv_enem$TP_ESCOLA, fill=csv_enem$NU_NOTA_MEDIA_CAT, ylab="Quantidade", xlab="Tipo de escola") + scale_fill_discrete(name="Pontuação")