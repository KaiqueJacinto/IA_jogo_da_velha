import numpy as np
import random

def vetor_matriz(vetor_pesos:list,num_camada_int:int,len_entrada_sensor:int):
    aux = []
    for i in range(0,num_camada_int,len_entrada_sensor):
        aux.append(vetor_pesos[i:i+len_entrada_sensor:])
    return aux

def vetor_normalizado(vetor:list):
    aux = 0
    normalizado = []
    for item in vetor:
        aux += (item**2)
    
    aux = aux**(1/2)
    if aux != 0:
        for item in vetor:
            normalizado.append(item/aux)

        return normalizado
    else:
        return vetor

def vetor_peso_aleatorio(num_camada:int):
    aux = []
    for _ in range(num_camada*2):
        aux.append(random.choice([-1,1])*random.random())
    return aux
    
class rede_neural():
    def __init__(self,entrada_sensores:list,num_camada_intermediaria:int,pesos_primeiro:list,pesos_segundo:list):
        self.entrada_sensores = entrada_sensores
        self.num_camada_intermediaria = num_camada_intermediaria
        self.num_pesos_intermediario = len(entrada_sensores)*num_camada_intermediaria
        self.num_pesos_final = num_camada_intermediaria*len(entrada_sensores)
        self.pesos_primeiro = pesos_primeiro
        self.pesos_segundo = pesos_segundo
       
    def vetor_saida(self):
        matriz_primeiro = vetor_matriz(self.pesos_primeiro,self.num_pesos_intermediario,len(self.entrada_sensores))
        matriz_segundo = vetor_matriz(self.pesos_segundo,self.num_pesos_final,self.num_camada_intermediaria)
        
        vetor_camada_central = []
        vetor_camada_saida   = []
        
        for linha in matriz_primeiro:
            valor_unidade = 0
            for item in linha:
                valor_unidade += item*(self.entrada_sensores[linha.index(item)])
            vetor_camada_central.append(valor_unidade)
        
        vetor_central_normalizado = vetor_normalizado(vetor_camada_central)
        
        for linha in matriz_segundo:
            valor_unidade = 0
            for item in linha:
                valor_unidade += item*(vetor_central_normalizado[linha.index(item)])
            vetor_camada_saida.append(valor_unidade)
        
        return vetor_normalizado(vetor_camada_saida)
    
'''teste = rede_neural([1,-1,1,
                     1,0,0,
                     -1,0,0],
                    18,
                    vetor_peso_aleatorio(9*18),
                    vetor_peso_aleatorio(9*18))

print(teste.vetor_saida())'''