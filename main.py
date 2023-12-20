import random
import matplotlib.pyplot as plt
import perceptron

NUM_GERACOES = 500
NUM_INDIVIDUOS = 100
PORC_CROSS = 10/100
PORC_MUTACAO = 5/100

NUM_CAMADA_INTERMEDIRIA = 18
NUM_VETOR_ENTRADA = 9

def verifica_estado(tabuleiro:list):
    tabuleiro, quem_começou = tabuleiro[0],tabuleiro[1]
    vitoria = 0
    for i in range(0,9,3):
        if tabuleiro[0+i] == tabuleiro[1+i] and tabuleiro[1+i] == tabuleiro[2+i]:
            if tabuleiro[0+i] != 0:
                vitoria = tabuleiro[0+i]
                break
    for j in range(3):
        if tabuleiro[0+j] == tabuleiro[3+j] and tabuleiro[3+j] == tabuleiro[6+j]:
            if tabuleiro[0+j] != 0:
                vitoria = tabuleiro[0+j]
                break
    if tabuleiro[0] == tabuleiro[4] and tabuleiro[4] == tabuleiro[8]:
        if tabuleiro[0] != 0:
            vitoria = tabuleiro[0]

    elif tabuleiro[2] == tabuleiro[4] and tabuleiro[4] == tabuleiro[6]:
        if tabuleiro[2] != 0:
            vitoria = tabuleiro[2]
    return vitoria

def gera_tabuleiro(num_jogadas:int):
    tabuleiro = [0,0,0,
                 0,0,0,
                 0,0,0]
    lado = random.choice([-1,1])
    quem_começou = lado
    
    for i in range(num_jogadas):
        while True:
            index_tabuleiro = random.randint(0,8)
            if tabuleiro[index_tabuleiro] == 0:
                tabuleiro[index_tabuleiro] = lado
                lado *=-1
                break
    return tabuleiro, quem_começou

def mostra_tabuleiro(tabuleiro:list):
    tabuleiro, quem_começou = tabuleiro[0],tabuleiro[1]
    aux = []
    for i in tabuleiro:
        if i == -1:
            aux.append('X')
        elif i == 0:
            aux.append(' ')
        else:
            aux.append('O')
            
    print(f'-------\n|{aux[0]}|{aux[1]}|{aux[2]}|\n-------\n|{aux[3]}|{aux[4]}|{aux[5]}|\n-------\n|{aux[6]}|{aux[7]}|{aux[8]}|\n-------')

def conta_peças(tabuleiro:list):
    return tabuleiro.count(-1),tabuleiro.count(1)

def mov_valido(tabuleiro:list,escolha:list):
    tabuleiro, quem_começou = tabuleiro[0],tabuleiro[1]
    num_X, num_O = conta_peças(tabuleiro)
    if num_X < num_O:
        if -1 in escolha:
            index_lista = escolha.index(-1)
            if tabuleiro[index_lista] == 0:
                return True
            else:
                return False
        else:
            return False
    elif num_X > num_O:
        if 1 in escolha:
            index_lista = escolha.index(1)
            if tabuleiro[index_lista] == 0:
                return True
            else:
                return False
        else:
            return False
    else:
        if quem_começou in escolha:
            index_lista = tabuleiro.index(quem_começou)
            if tabuleiro[index_lista] == 0:
                return True
            else:
                return False
        else:
            return False

def faz_movimento(tabuleiro:list,escolha:list):
    if -1 in escolha:
        index_escolha = escolha.index(-1)
        tabuleiro[index_escolha] = -1
    else:
        index_escolha = escolha.index(1)
        tabuleiro[index_escolha] = 1
    return tabuleiro

def fitness(tabuleiro:list,escolha:list):
    pontuação = 10
    if -1 in escolha:
        escolha_num = -1
    else:
        escolha_num = 1
    if mov_valido(tabuleiro,escolha) == True:
        pontuação += 3
        tabuleiro_novo = faz_movimento(tabuleiro[0],escolha)
        estado_tabuleiro = verifica_estado([tabuleiro_novo,tabuleiro[1]])
        if estado_tabuleiro == escolha_num:
            pontuação +=7
    else:
        pontuação -= 10
    
    return pontuação

def população_inicial(num_individuos:int):
    aux = []
    for _ in range(num_individuos):
        aux.append(perceptron.vetor_peso_aleatorio(NUM_CAMADA_INTERMEDIRIA*NUM_VETOR_ENTRADA))
    return aux

def encontra_melhor(população:list,lista_fitness:list):
    index_melhor = lista_fitness.index(max(lista_fitness))
    melhor = população[index_melhor]
    fitness_melhor = lista_fitness[index_melhor]
    população.remove(melhor)
    lista_fitness.remove(fitness_melhor)
    return população,lista_fitness,melhor,fitness_melhor

def cruzamento(pai:list,mae:list):
    vetor_pai,fitness_pai = pai
    vetor_mae,fitness_mae = mae
    vetor_filho = []
    for i in range(len(vetor_pai)):
        if random.random() < PORC_MUTACAO:
                vetor_filho.append(random.choice([-1,1])*random.random())
        else:
            soma_pais = (fitness_pai+fitness_mae)
            if soma_pais == 0:
                soma_pais =1
            if random.random() < fitness_pai/soma_pais:
                vetor_filho.append(vetor_pai[i])    
            else:
                vetor_filho.append(vetor_mae[i])
    return vetor_filho
                
def nova_populacao(população:list,lista_fitness:list):
    populacao_gerada = []
    melhores = []
    fitness_melhores = []
    for _ in range(6):
        população,lista_fitness,melhor,fitness_melhor = encontra_melhor(população,lista_fitness)
        melhores.append(melhor)
        populacao_gerada.append(melhor)
        fitness_melhores.append(fitness_melhor)
    
    for i in range(len(melhores)-1):
        for j in range(i+1,len(melhores),1):
            filho = cruzamento([melhores[i],fitness_melhores[i]],
                                               [melhores[j],fitness_melhores[j]])
            if not(filho in populacao_gerada):
                populacao_gerada.append(filho)
    while len(populacao_gerada) < NUM_INDIVIDUOS:
        if len(lista_fitness) >0:
            população,lista_fitness,melhor,fitness_melhor = encontra_melhor(população,lista_fitness)
        else:
            populacao_gerada.append(perceptron.vetor_peso_aleatorio(NUM_CAMADA_INTERMEDIRIA*NUM_VETOR_ENTRADA))
        for i in range(3):
            if len(populacao_gerada) == NUM_INDIVIDUOS:
                break
            else:
                if len(lista_fitness) >0:
                    população,lista_fitness,melhor2,fitness_melhor2 = encontra_melhor(população,lista_fitness)
                    filho = cruzamento([melhor,fitness_melhor],[melhor2,fitness_melhor2])
                    if not(filho in populacao_gerada):
                        populacao_gerada.append(filho)
                else:
                    populacao_gerada.append(perceptron.vetor_peso_aleatorio(NUM_CAMADA_INTERMEDIRIA*NUM_VETOR_ENTRADA))
    return populacao_gerada

def vetor_escolha_arrumado(vetor_saida_rede:list):
    aux = [0,0,0,
           0,0,0,
           0,0,0]
    maximo = max(vetor_saida_rede)
    minimo = min(vetor_saida_rede)
    if maximo > (minimo*(-1)):
        index_maximo = vetor_saida_rede.index(maximo)
        aux[index_maximo] = 1
    else:
        index_minimo = vetor_saida_rede.index(minimo)
        aux[index_minimo] = -1
    return aux
   
def main():
    RODADAS_POR_INDIVIDUO = 10
    populacao_ini = população_inicial(NUM_INDIVIDUOS)
    lista_fitness = []
    todos_fitness = []
    fitness_geracoes = []

    for geracao in range(NUM_GERACOES):
        fitness_total = []
        print(geracao)
        if geracao == 0:
            populacao = populacao_ini
        else:
            populacao = nova_populacao(populacao,lista_fitness)
            lista_fitness = []
        #print('----------')
        #print(populacao[58:60:])
        #print('----------')
        for individuo in populacao:
            fitnes_total_individuo = 0
            for _ in range(RODADAS_POR_INDIVIDUO):
                while True:
                    tabuleiro = gera_tabuleiro(random.randint(1,8))
                    if verifica_estado(tabuleiro) == 0:
                        break
                pesos_primeiro,pesos_segundo = individuo[:len(individuo)//2:],individuo[len(individuo)//2::]
                rede_individuo = perceptron.rede_neural(tabuleiro[0],
                                                        NUM_CAMADA_INTERMEDIRIA,
                                                        pesos_primeiro,
                                                        pesos_segundo)
                vetor_saida_rede = rede_individuo.vetor_saida()
                escolha = vetor_escolha_arrumado(vetor_saida_rede)
                fitnes_total_individuo += fitness(tabuleiro,escolha)
            lista_fitness.append(fitnes_total_individuo/RODADAS_POR_INDIVIDUO)
            fitness_total.append(fitnes_total_individuo/RODADAS_POR_INDIVIDUO)
        fitness_geracoes.append(sum(fitness_total)/NUM_INDIVIDUOS)
        todos_fitness.append(fitness_total)
    #print(fitness_geracoes)
    lista_melhores = []
    for i in todos_fitness:
        lista_melhores.append(max(i))
    print(lista_melhores)
    plt.plot(list(range(1,len(fitness_geracoes)+1,1)),fitness_geracoes,label='media')
    plt.plot(list(range(1,len(fitness_geracoes)+1,1)),lista_melhores)
    plt.show()
        

main()

'''tabuleiro = [[-1,1,1,
             0,1,0,             
             0,0,-1,],1]#gera_tabuleiro(8)
tabuleiro = gera_tabuleiro(5)
### -1 = X e 1 = O
mostra_tabuleiro(tabuleiro)#tabuleiro)
print(verifica_estado(tabuleiro))
print(mov_valido(tabuleiro,[0,0,0,
                            0,0,0,
                            0,1,0]))'''