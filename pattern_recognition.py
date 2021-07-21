import matplotlib.pyplot as plt
import time
import random
from classes import readData, LZW, dataToString, classification

# Parameters: 
numPerson = 10  # Número de pessoas que a vai ser testado
numDataPerPerson = 10  # Número de imagens por pessoa
maxK = 17 # K Máximo
minK = 9  # K Mínimo
timeK = [] #Tempos para criação dos dicionarios para cada K
outputs= []   # Saidas geradas por cada imagem
dataDicts = []  # Dicionarios de cada pessoa
dataTest = [random.randint(0,9) for i in range(numPerson)]  # Escolhe de maneira randômica as imagens de teste
outClassification= [] # Saidas geradas pela classificação
timeClassification = [] # Tempos para classificação
accuracy = [] # Quantidade de acertos

# Criação do Dicionário inicializado com a Tabela ASCII: 
sizeDict = 256
Dictionary = [chr(i) for i in range(sizeDict)]

for k in range(minK, maxK):		# Gera um dicionário por pessoa para cada K
    initialTime = time.time()
    for person in range(1, numPerson + 1):
        dataTrain = readData(person, numDataPerPerson)
        del dataTrain[dataTest[person - 1]]  # Retira a imagem escolhida para teste 
        dic = Dictionary[0:] 
        for j in range(numDataPerPerson - 1): 
            image = dataTrain[j]
            message = dataToString(image)
            output = LZW(k, message, dic)
        dataDicts.append(dic)
    timeK.append(time.time() - initialTime)

# Classificação:
for k in range(minK, maxK): # Compara o dado de Teste com cada Dicionário criado
    initialTime = time.time()
    for person in range(1, numPerson+1):
        dataTrain = readData(person)
        image = dataTrain[dataTest[person-1]]
        message = dataToString(image)
        for j in range((k-minK)*numPerson, ((k-minK)*numPerson) + numPerson):
            dic = dataDicts[j]
            output = LZW(k, message, dic)
            outClassification.append(output)
    timeClassification.append(time.time() - initialTime)

# Contagem dos Acertos: 
for k in range(minK, maxK):
    correctClass = 0
    for person in range(1, numPerson+1):
        result = classification(person, k, outClassification, numPerson)
        if result == 1:
            correctClass += 1
    accuracy.append(correctClass)
    
accuracy = [100*(hits/numPerson) for hits in accuracy]

plt.figure()
plt.title('Taxa de Acertos x K')
plt.ylabel('Taxa de Acertos')
plt.xlabel('K')
plt.plot(list(range(minK,maxK)), accuracy)
plt.grid(True)

timeClassification = [time/60 for time in timeClassification]

plt.figure()
plt.title('Tempo de Processamento x K')
plt.ylabel('Tempo(minutos)')
plt.xlabel('K')
plt.plot(list(range(minK,maxK)), timeClassification)
plt.grid(True)
