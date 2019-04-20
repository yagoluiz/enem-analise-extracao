# bibliotecas para manipulacao de dados e de sistema
import csv, sys 

# leitura e saida de arquivos .csv
csv_path = r'C:\Dev\Python\MICRODADOS_ENEM_CENTRO_OESTE_2015.csv'
csv_output = r'C:\Dev\Python\MICRODADOS_ENEM_CENTRO_OESTE_CATEGORIZADOS_2015.csv'

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
            if count > 0: # exclusao de cabecalho da planilha
                yield row
            count+=1


# escrita do arquivo .csv
def write_data(path, data):
        with open(path, 'a', newline = '') as csv_file:
            writer = csv.writer(csv_file, delimiter = ',',  quotechar = '"')
            writer.writerows([data])


# categorizacao situacao de conclucao
def category_situacao_conclucao(data):
    cod_atributo = 3 # codigo do atributo
    # categorias do atributo
    categoria = {'1': 'Ja conclui o Ensino Medio',
        '2': 'Estou cursando e concluirei o Ensino Medio em 2015', 
        '3': 'Estou cursando e concluirei o Ensino Medio apos 2015', 
        '4': 'Nao conclui e nao estou cursando o Ensino Medio'} 

    for row in data[cod_atributo]:
        for key, value in categoria.items():
            if row == key:
                data[cod_atributo] = value # inclusao da categorizacao
                break


# categorizacao da escola estudada
def category_escola(data):
    cod_atributo = 4 # codigo do atributo
    # categorias do atributo
    categoria = {'1': 'Nao Respondeu',
        '2': 'Publica', 
        '3': 'Privada', 
        '4': 'Exterior'} 

    for row in data[cod_atributo]:
        for key, value in categoria.items():
            if row == key:
                data[cod_atributo] = value # inclusao da categorizacao
                break


# categorizacao do tipo de ensino
def category_ensino(data):
    cod_atributo = 5 # codigo do atributo
    # categorias do atributo
    categoria = {'1': 'Ensino Regular',
        '2': 'Educacao Especial - Mobilidade Substitutiva', 
        '3': 'Educacao de Jovens e Adultos'}

    for row in data[cod_atributo]:
        for key, value in categoria.items():
            if row == key:
                data[cod_atributo] = value # inclusao da categorizacao
                break


# categorizacao do tipo ra raca declarada
def category_raca(data):
    cod_atributo = 6 # codigo do atributo
    # categorias do atributo
    categoria = {'0': 'Nao declarado',
        '1': 'Branca', 
        '2': 'Preta', 
        '3': 'Parda',
        '4': 'Amarela', 
        '5': 'Indigena',
        '6': 'Sem informacao'} 

    for row in data[cod_atributo]:
        for key, value in categoria.items():
            if row == key:
                data[cod_atributo] = value # inclusao da categorizacao
                break


# categorizacao da lingua para prova de lingua estrangeira
def category_lingua(data):
    cod_atributo = 11 # codigo do atributo
    # categorias do atributo
    categoria = {'0': 'Ingles', '1': 'Espanhol'}

    for row in data[cod_atributo]:
        for key, value in categoria.items():
            if row == key:
                data[cod_atributo] = value # inclusao da categorizacao
                break


# categorizacao do nivel de escolaridade dos pais
def category_escolaridade(data):
    cod_atributos = [13, 14] # posicao dos atributos (QS_ESCOLARIDADE_PAI e QS_ESCOLARIDADE_MAE)
    # categorias do atributo
    category = {'A': 'Nunca estudou',
        'B': 'Nao completou a 4 serie/5 ano do Ensino Fundamental',
        'C': 'Completou a 4 serie/5 ano, mas nao completou a 8 serie/9 ano do Ensino Fundamental',
        'D': 'Completou a 8 serie/9 ano do Ensino Fundamental, mas nao completou o Ensino Medio',
        'E': 'Completou o Ensino Medio, mas nao completou a Faculdade',
        'F': 'Completou a Faculdade, mas nao completou a Pos-graduacao',
        'G': 'Completou a Pos-graduacao',
        'H': 'Nao sei'}

    for atributo in cod_atributos:
        for row in data[atributo]:
            for key, value in category.items():
                if row == key:
                    data[atributo] = value # inclusao da categorizacao
                    break


# categorizacao da renda familiar
def category_renda(data):
    cod_atributo = 16 # codigo do atributo

    # categorizacao de acordo com a tabela do IBGE (salario minimo = RS 937,00)
    for row in data[cod_atributo]:
        if row == 'A' or row == 'B' or row == 'C' or row == 'D' or row == 'E':
            data[cod_atributo] = 'Ate RS 1.874,00' # ate 2 salarios minimos (E)
        elif row == 'F' or row == 'G' or row == 'H':
            data[cod_atributo] = 'RS 1.874,01 a RS 3.748,00' # de 2 a 4 salarios minimos (D)
        elif row == 'I' or row == 'J' or row == 'K' or row == 'L' or row == 'M' or row == 'N':
            data[cod_atributo] = 'RS 3.748,01 a RS 9.370,00' # de 4 a 10 salarios minimos (C)
        elif row == 'O' or row == 'P':
            data[cod_atributo] = 'RS 9.370,01 a RS 18.740,00' # de 10 a 20 salarios minimos (B)
        else: # row == 'Q'
            data[cod_atributo] = 'RS 18.740,01 ou mais' # acima de 20 salarios minimos (A)

# categorizacao do tipo de atividade de trabalho
def category_atividade_remunerada(data):
    cod_atributo = 17 # codigo do atributo
    # categorias do atributo
    category = {'A': 'Nao, nunca trabalhei',
        'B': 'Sim, ja trabalhei, mas nao estou trabalhando',
        'C': 'Sim, estou trabalhando'}

    for row in data[cod_atributo]:
        for key, value in category.items():
            if row == key:
                data[cod_atributo] = value # inclusao da categorizacao
                break


# categorizacao do tipo de escola cursada no ensino fundamental
def category_escola_fundamental(data):
    cod_atributo = 18 # codigo do atributo
    # categorias do atributo
    category = {'A': 'Somente em escola publica',
        'B': 'A maior parte em escola publica',
        'C': 'Somente em escola particular',
        'D': 'A maior parte em escola particular',
        'E': 'Somente em escola indigena',
        'F': 'A maior parte em escola indigena',
        'G': 'Somente em escola situada em comunidade quilombola',
        'H': 'A maior parte em escola situada em comunidade quilombola'}
    
    for row in data[cod_atributo]:
        for key, value in category.items():
            if row == key:
                data[cod_atributo] = value # inclusao da categorizacao
                break


# categorizacao do abandono no ensino fundamental e ensino medio
def category_abandono_reprovacao_fundamental_medio(data):
    cod_atributos = [19, 21] # codigos do atributos
    # categorias do atributo
    category = {'A': 'Nao abandonei, nem fui reprovado',
        'B': 'Nao abandonei, mas fui reprovado',
        'C': 'Abandonei, mas nao fui reprovado',
        'D': 'Abandonei e fui reprovado'}
    
    for atributo in cod_atributos:
        for row in data[atributo]:
            for key, value in category.items():
                if row == key:
                    data[atributo] = value # inclusao da categorizacao
                    break


# categorizacao do tipo de escola cursada no ensino media
def category_escola_medio(data):
    cod_atributo = 20 # codigo do atributo
    # categorias do atributo
    category = {'A': 'Somente em escola publica',
        'B': 'Parte em escola publica e parte em escola privada sem bolsa de estudo integral',
        'C': 'Parte em escola publica e parte em escola privada com bolsa de estudo integral',
        'D': 'Somente em escola privada sem bolsa de estudo integral',
        'E': 'Somente em escola privada com bolsa de estudo integral'}
    
    for row in data[cod_atributo]:
        for key, value in category.items():
            if row == key:
                data[cod_atributo] = value # inclusao da categorizacao
                break


# inclusao da media aritmetica das provas
def media_notas_aritmetica(data):
    cod_atributos = [7, 8, 9, 10, 12] # codigos do atributos
    cod_atributo_nota = 22 # codigo para novo atributo
    notas = []

    # busca das notas para calculo
    for atributo in cod_atributos:
        notas.append(float(data[atributo]))

    media_aritmetica = float(sum(notas) / 5.0) # calculo da media aritmetica
    data[cod_atributo_nota] = '{0:.1f}'.format(media_aritmetica) # inclusao da media aritmetica


# categorizacao da media aritmetica das provas
def category_media_notas(data):
    cod_atributo = 23 # codigo do atributo para categorizacao
    cod_atributo_nota = 22 # codigo do atributo com a media aritmetica

    nota = float(data[cod_atributo_nota])

    # categorizacao das notas
    if nota <= 200.0:
        data[cod_atributo] = 'Ate 200 pontos'
    elif nota <= 300.0:
        data[cod_atributo] = '201 a 300 pontos'
    elif nota <= 400.0:
        data[cod_atributo] = '301 a 400 pontos'
    elif nota <= 500.0:
        data[cod_atributo] = '401 a 500 pontos'
    elif nota <= 600.0:
        data[cod_atributo] = '501 a 600 pontos'
    elif nota <= 700.0:
        data[cod_atributo] = '601 a 700 pontos'
    elif nota <= 800.0:
        data[cod_atributo] = '701 a 800 pontos'
    elif nota <= 900.0:
        data[cod_atributo] = '801 a 900 pontos'
    else:
        data[cod_atributo] = 'Maior que 900 pontos'


# categorizacao da idade do candidato
def category_idade(data):
    cod_atributo = 24 # codigo do atributo para categorizacao
    cod_atributo_idade = 1 # codigo do atributo com a idade
    
    idade = int(data[cod_atributo_idade])
    
    # categorizacao das idades
    if idade <= 20:
        data[cod_atributo] = 'Ate 20 anos'
    elif idade <= 25:
        data[cod_atributo] = '21 a 25 anos'
    elif idade <= 30:
        data[cod_atributo] = '26 a 30 anos'
    else:
        data[cod_atributo] = 'Maior que 30 anos'


# categorizacao da quantidade de pessoas morando por residencia
def category_quantidade_pessoas_residencia(data):
    cod_atributo = 25 # codigo do atributo par categorizacao
    cod_atributo_qtd_pessoas = 15 # codigo a quantidade de pessoas declaradas

    qtd = int(data[cod_atributo_qtd_pessoas])
    
    # categorizacao da quantidade de pessoas
    if qtd <= 2:
        data[cod_atributo] = 'Ate 2 pessoas'
    elif qtd <= 5:
        data[cod_atributo] = '3 a 5 pessoas'
    elif qtd <= 10:
        data[cod_atributo] = '6 a 10 pessoas'
    else:
        data[cod_atributo] = 'Maior que 10 pessoas'


# execucao da categorizacao dos dados
try:
    write_data(csv_output, atributos.keys()) # inclusao de cabecalho de atributos

    for row in reader_data(csv_path):  # leitura no arquivo .csv original
        # categorizacao dos atributos
        category_situacao_conclucao(row)
        category_escola(row)
        category_ensino(row)
        category_raca(row)
        category_lingua(row)
        category_escolaridade(row)
        category_renda(row)
        category_atividade_remunerada(row)
        category_escola_fundamental(row)
        category_abandono_reprovacao_fundamental_medio(row)
        category_escola_medio(row)
        media_notas_aritmetica(row) # inclusao do atributo com media aritmetica das notas
        category_media_notas(row)
        category_idade(row)
        category_quantidade_pessoas_residencia(row)
        write_data(csv_output, row) # inserir novos dados no arquivo .csv
except:
    print("Ooops!", sys.exc_info()) # informacao de erro