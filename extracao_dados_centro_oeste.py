# bibliotecas para manipulacao de dados e de sistema
import csv, sys

# leitura e saida de arquivos .csv
csv_path = r'C:\Dev\Python\MICRODADOS_ENEM_2015.csv'
csv_output = r'C:Dev\Python\MICRODADOS_ENEM_CENTRO_OESTE_2015.csv'

# atributos selecionados do arquivo .csv
atributos = {'CO_UF_RESIDENCIA': 5, 'NU_IDADE': 16, 'TP_SEXO': 17, 'TP_ST_CONCLUSAO': 23,
    'TP_ESCOLA': 25, 'TP_ENSINO': 26, 'TP_COR_RACA': 28, 'NU_NOTA_CN': 96, 'NU_NOTA_CH': 97,
    'NU_NOTA_LC': 98, 'NU_NOTA_MT': 99, 'TP_LINGUA': 104, 'NU_NOTA_REDACAO': 115,
    'QS_ESCOLARIDADE_PAI': 116, 'QS_ESCOLARIDADE_MAE': 117, 'QS_QTD_RESIDENCIA': 120, 'QS_RENDA': 121,
    'QS_ATIVIDADE_REMUNERADA': 141, 'QS_ESCOLA_FUNDAMENTAL': 157, 'QS_ABANDONO_REPROVACAO_FUNDAMENTAL': 160,
    'QS_ESCOLA_MEDIO': 162, 'QS_ABANDONO_REPROVACAO_MEDIO': 165, 'NU_NOTA_MEDIA': 0, 'NU_NOTA_MEDIA_CAT': 0,
    'NU_IDADE_CAT': 0, 'QS_QTD_RESIDENCIA_CAT': 0}


# leitura do arquivo .csv
def reader_data(path):
    with open(path, 'r') as csv_file:
        count = 0
        reader = csv.reader(csv_file, delimiter = ',', quoting = csv.QUOTE_ALL)

        for row in reader:
            if count > 0: #exclusao de cabecalho da planilha
                yield row
            count+=1


# escrita do arquivo .csv
def write_data(path, data):
        with open(path, 'a', newline = '') as csv_file:
            writer = csv.writer(csv_file, delimiter = ',',  quotechar = '"')
            writer.writerows([data])


# verificacao de regiao (centro-oeste)
def is_regiao(data):
    regioes = ['DF', 'GO', 'MS', 'MT']
    cod_sigla = 5 # codigo da sigla
    return data[cod_sigla] in regioes


# verificacao de presencas do dia da prova
def is_presente(data):
    cod_presencas = [88, 89, 90, 91] # codigo de presencas
    for presenca in cod_presencas:
        if data[presenca] == '0' or data[presenca] == '2': # (0) faltou a prova ou (2) foi eliminado
            return False
    
    return True


# verificacao de candidato treineiro
def is_treineiro(data):
    cod_treineiro = 7 # codigo de candidato treineiro
    return data[cod_treineiro] == '0'


# verificacao se redacao e valida
def is_redacao_valida(data):
    cod_status_redacao = 109 # codigo de status da redacao
    return data[cod_status_redacao] == '1' # verificar se aluno nao foi eliminado na redacao


# limpeza de dados em brancos
def is_not_empty(data):
    for row in data:
        if row == '':
            return False

    return True


# execucao de selecao e limpeza dos dados
try:
    write_data(csv_output, atributos.keys()) # inclusao de cabecalho de atributos

    for row in reader_data(csv_path): # leitura no arquivo .csv original
        if is_regiao(row) and is_treineiro(row) and is_presente(row) and is_redacao_valida(row): # selecao dos dados
            row_atributos = []
            for key, value in atributos.items(): # atributos selecionados
                if value == 0:
                    row[value] = 0 
                row_atributos.append(row[value]) # inclusao apenas dos atributos selecionados
            if is_not_empty(row_atributos): # limpeza de dados
                write_data(csv_output, row_atributos) # inserir novos dados no arquivo .csv
except:
    print("Ooops!", sys.exc_info()) # informacao de erro