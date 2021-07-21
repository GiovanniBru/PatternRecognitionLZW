import PIL

def readData(numPerson, numDataPerPerson):        # Lê todas as imagens de uma determinada pessoa no banco de dados
    fileList = []
    for j in range(1,numDataPerPerson + 1):       
        fileList.append(PIL.Image.open('C:/Users/Giovanni/Desktop/orl_faces/s'+ str(numPerson) + "/" + str(j) +'.pgm'))
    return fileList
    
def dataToString(image):    # Transforma o dado (imagem) em uma String 
    message = ""
    for y in range(112):    
        for x in range(92):
            message = message + chr(image.getpixel((x,y)))
    return message

def alreadExist(simbol,dic):    # Verifica se o símbolo existe no dicionário e retorna seu índice 
    if simbol in dic:
        return dic.index(simbol)
    return -1

def LZW(k, message, dic):      # Algoritmo de Codificação LZW, retorna o dado codificado
    DataCod = []
    aux = ''
    i=0    
    for i in range(len(message)):    
        c = message[i]
        if alreadExist(aux+c,dic) != -1:      # Verifica se existe o simbolo atual 
            aux = aux + c
        else:    # Caso não exista, adiciona o índice do símbolo atual na saída e adiciona o símbolo atual + próximo símbolo como índices do Dicionário
            DataCod.append(alreadExist(aux,dic))
            if len(dic) < (2**k):   # Verifica se o Dicionário está cheio
                dic.append(aux+c)
            aux = c

        if (i+1)<len(message):    # Continua rodando até pegar todos os símbolos
            continue
        else:
            DataCod.append(alreadExist(aux,dic))
        
    return DataCod

def classification(person, k, outClassification, numPerson):      # Verifica se a imagem recebeu a classificação correta
    outputs = outClassification[((k-9)*(numPerson**2))+(numPerson*(person-1)):((k-9)*(numPerson**2))+(numPerson*(person))]
    outputSize = [len(output) for output in outputs]
    smallSize = min(outputSize)
    index = outputSize.index(smallSize)
    print("indice: " + str(index))
    if index == (person - 1):      # 1 = classificação correta
        return 1
    else:                           # 0 = classificação incorreta
        print("classificacao incorreta da pessoa: " + str(person))
        return 0