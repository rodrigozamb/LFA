import re


def Diff(li1, li2): 
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2] 
    return li_dif 

class Gramatica:
    
    def __init__(self,nome,V,T,P,S):
        self.nome = nome
        self.V = V
        self.T = T
        self.P = P
        self.S = S
        self.simbolos = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

        for i in self.V:
            self.simbolos.remove(i)

    def printa_V(self):
        print(self.V)
    def printa_T(self):
        print(self.T)
    def printa_P(self):
        print(self.P)

    def elimina_simbolos_inuteis(self):
        aux = [x[0] for x in self.P]
        
        inuteis = [x for x in self.V if (x not in aux)]
        
        for inu_Simb in inuteis:
            for Trans in self.P:
                ladoDir = Trans[1]
                if inu_Simb in ladoDir:
                    self.P.remove(Trans)
        self.V = Diff(self.V,inuteis)
        
        aux2 = [x[1] for x in self.P]
        
        naoChegaveis = self.V

        toremove=[]
        
        for i in self.V:
            f=False
            for j in aux2:
                #print(i," esta em ",j,' ??')
                if i in str(j):
                    #print('sim\n',"removemos - ",i)
                    f=True
            if f == False:
                toremove.append(i)
        flag = True
        while(flag):
            flag=False
            for i in self.P:
                if i[0] in toremove:
                    self.P.remove(i)
                    flag=True
                

        for i in toremove:
            self.V.remove(i)

    def elimina_eproducoes(self):
        produzemE = list(filter(lambda x : '$' in x[1] ,self.P)) 
        #print(produzemE)
        self.P = list(filter(lambda x : x[1] != '$',self.P))
        
        for i in produzemE:
            aux = list(filter(lambda x: x[0]==i[0] and i[0] in x[1],self.P))

            for i in aux:
               aux2 = str(i[1])
               aux2 = aux2.translate({ord(i[0]):None}) 
               self.P.append([i[0],aux2])
        
        self.P = list(filter(lambda x : x[1] != '',self.P))            
        
    def elimina_Transicoes_unitarias(self):
        for i in self.P:
            if(i[1] in self.V):
                print(i)
                aSerInserido = list(filter(lambda x : x[0] == i[1],self.P))
                for j in aSerInserido:
                    self.P.append([i[0],j[1]])
                self.P.remove(i)        



    def fnc(self):
        # retirar variaveis e terminais que estiverem juntos
        aux = []
        for i in self.T:
            aux.append((i,self.simbolos.pop()))
        aux = dict(aux)
        for transicoes in self.P:
            palavra = transicoes[1]
            if cadeia_producao(self,palavra) == True:
                for i in palavra:
                    if(i in self.T):
                        palavra = palavra.replace(i,aux[i])
            transicoes[1] = palavra 
        for i in aux:  # coloca transições finalizadoras
            self.P.append([aux[i],i])


        for p in self.P:
            if(soh_finais(self,p[1])==False and len(p[1])>2):
                string = p[1]
                
                novo = procura_t(self,string[1::])
                if(novo !='*'):
                    string = string[0]+novo
                    p[1]=string   

                else:
                    novo = self.simbolos.pop()
                    self.P.append([novo,string[1::]])
                    string = string[0]+novo
                    p[1]=string
        

        for i in aux:
            achou=0
            for j in self.P:
                if aux[i] in j[1]:
                    achou=1 
            if achou == 0:
                a = [aux[i],i]
                self.P.remove(a)
        print(self.P)

def procura_t(G,y):
    for i in G.P:
        if y == i[1]:
            return i[0]
    return '*'

def soh_finais(G,l):
    for i in l:
        if i in G.V:
            return False
    return True

def cadeia_producao(G,l):
    tem_V=0
    tem_F=0
    for i in l:
        if i in G.V:
            tem_V=1
        if i in G.T:
            tem_F=1
    if(tem_F==1 and tem_V==1):
        return True
    else:
        return False

#G = Gramatica('Automato',['S','A','B','C','Z'],['a','b','c'],[['S','aSAa'],['S','bBb'],['S','$'],['S','aAAa'],['A','a'],['A','$'],['A','S'],['C','c'],['C','$'],['Z','A']],'S')
G = Gramatica('Automato',['S'],['a','b','c'],[['S','a'],['S','b'],['S','c'],['S','SaSS']],'S')
G.printa_V()
G.printa_P()

G.elimina_simbolos_inuteis()
print('pos conv')
#G.printa_V()
#G.printa_P()


print("e - prods")
G.elimina_eproducoes()
#G.printa_P()

print("prod unitarias")
G.elimina_Transicoes_unitarias()
#G.printa_P()

print('testando FNC')
G.fnc()