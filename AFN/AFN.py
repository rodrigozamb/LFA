f = open("casoAFN.txt","r")
out = open("out.txt","w")

listaFinal = []

def set_estados(listaEst):
    matches = [x for x in listaEst if (x not in listaFinal)]    
    return matches

def remove_vazio(lista):
    x = [a for a in lista if( len(a)>0)]
    return x

def cria_delta(cadeiaDeEstados):
    delta = []
    for alf in alfabeto:
        aux2 = []
        for estadoAtual in cadeiaDeEstados:
            for tran in transicoes:
                if(tran[0] == estadoAtual and alf == tran[1] and len(tran[2])>0):
                    for k in tran[2]:
                        aux2.append(int(k))
        delta.append(aux2)
    listaSemRepeticao = set_estados(delta)
    
    if(len(listaSemRepeticao)>0):
        for k in listaSemRepeticao:
            listaFinal.append(k)
        for o in listaSemRepeticao:
            cria_delta(o)
        return listaSemRepeticao
    else:
        return []

def cria_delta2(cadeiaDeEstados):
    delta = []
    for alf in alfabeto:
        aux2 = []
        for estadoAtual in cadeiaDeEstados:
            for tran in transicoes:
                if(tran[0] == estadoAtual and alf == tran[1] and len(tran[2])>0):
                    for k in tran[2]:
                        aux2.append(int(k))
        delta.append(aux2)
    
def preparaEstadosAFN_AFD():
    est = [estadoInicial]
    listaFinal.append([estadoInicial])

    flag = True
    while(flag):
        est =  cria_delta(est)
        if(len(est)==0):
            flag=False

    #print("Estados do AFD = ",remove_vazio(listaFinal))
    
    return remove_vazio(listaFinal)

def remove_vazio_e_junta(lista):
    x = [a for a in lista if( len(a)>0)]
    aux =[]
    for i in x:
        for j in i:
            aux.append(j)
    return aux

def preparaTransicoesAFN_AFD(estados):
    listaEst = []
   
    for alf in alfabeto:
        for est in estados:
            prox = calculaProxEstado(est,alf)
            #print(est," lendo ",alf," vai para ",prox)
            listaEst.append((est,alf,remove_vazio_e_junta(prox)))       

    return listaEst

def calculaProxEstado(Q,simbol):
    aux = []
    for q in Q:
        for t in transicoes:
            if(t[0]==q and t[1]==simbol):
                aux.append(t[2])
    return aux

def printa_estados(estadosF):
    for i in range(len(estadosF)):
        y = str(estadosF[i]).replace(" ","")
        out.write(y)
        if(i<len(estadosF)-1):
            out.write(" ")
        else:
            out.write("\n")

def printa_alfabeto():
    for i in range(len(alfabeto)):
        out.write(str(alfabeto[i]))
        if(i<len(alfabeto)-1):
            out.write(" ")
        else:
            out.write("\n")

def printa_finais():
    for i in range(len(finaisI)):
        out.write(str(finaisI[i]))
        if(i<len(finaisI)-1):
            out.write(" ")
        else:
            out.write("\n")

def printa_transicoes(t):
    for i in range(len(t)):
        out.write(str(t[i]))
        if(i<len(t)-1):
            out.write(" ")
        else:
            out.write("\n")

def AFNtoAFD():
   
    printa_estados(estadosAFD)
    printa_alfabeto()
    out.write(str(estadoInicial))
    out.write("\n")
    printa_finais()
    printa_transicoes(transicoesFinais)

def pertence_alfabeto(a):
    
    for x in alfabeto:
        if x == a:        
            return  True

def confere_final(l):
    for f in finaisI:
        for i in l:
            for x in i:
                if(x == f):
                    return True
    return False

def processaAFN(q,pos):

    if(pertence_alfabeto(cadeia[pos]) == False):
        print("simbolo ",cadeia[pos]," eh invalido")
        print("nao certinho")
        return False

        
    if(pos == len(cadeia)-1):
        if(confere_final(q)==True):
            print("chegou em estado final")
            print("Certinho")
            return True
        else:
            print("nao chegou em estado final")        
            print("nao certinho")
            return False
    
    print("aaaaaaaa")
    for i in q:
        for t in transicoes:
            if(t[0]==i and t[1]==cadeia[pos]):
                pos+=1
                print(q," lendo ",cadeia[pos]," leva a ",t[2])
                for es in t[2]:
                    if es != []:
                        processaAFN(es)
    return False

def processaAFN2(q,num):
    print("Estado atual = ",q)
    print("simbolo atual = ",cadeia[num]," pos = ",num)
    if(not pertence_alfabeto(cadeia[num]) or q==[]):
        print('4')
        return False
    
    proxEstados = []
    for s in q:
        for est in transicoesFinais:
            if(est[0] == s and est[1]==cadeia[num] and est[2]!= []):
                proxEstados.append(est[2])

    print("proxEstados = ",proxEstados)
    prox= []
    for i in proxEstados:
        prox.append([int(x) for x in i])
   
    print("prox = ",prox)

    if(len(cadeia)-num == 1):
        print("chegamos no final da cadeia = ",cadeia[num])
        if(confere_final(prox)):
            print("estados chegados = ",prox," - finais = ",finaisI)
            print("3")
            return True
        else:
            print(1)
            return False     
    else:
        
        for i in prox:
            print("vai para ",i,"\n")
            processaAFN2(i,num+1)
            print(2)
            return 
           

def processaAFN3(q,num):
    print("Estado atual = ",q)
    print("simbolo atual = ",cadeia[num]," pos = ",num)

    if(not pertence_alfabeto(cadeia[num]) or q==[]):
        print('O símbolo ',cadeia[num]," não faz parte do alfabeto")
        return False
    r=[]
    for i in transicoesFinais:
        if(i[0] == q and i[1]==cadeia[num] and i[2] != []):
            r = i[2]

    prox= [int(x) for x in r]

    if(len(cadeia)-num == 1):
        print("chegamos no final da cadeia = ",cadeia[num])
        for i in finaisI:
            if i in prox:
                print("estado ",i," chegado , de = ",prox," - finais = ",finaisI)
                return True
        
        print("ERRO - estados chegados = ",prox," - finais = ",finaisI)
        return False
    else:
        print("vai para ",prox,"\n")
        return processaAFN3(prox,num+1)


def resolve_AFN(cadeiai):
    contCadeia=0
    i = [estadoInicial]
    resp = processaAFN3(i,contCadeia)
    
    if(resp):
        print("O autômato reconhece a cadeia : ",cadeia)
    else:
        print("O autômato não reconhece a cadeia : ",cadeia)

estadosI = []
for x in f.readline().split():
    estadosI.append(x)

print("Q = ",estadosI)

alfabeto = []
for x in f.readline().split():
    alfabeto.append(x)
print("Alfabeto = ",alfabeto)

estadoInicial = int(f.readline()[0])
print("Estado Inicial = ",estadoInicial)

finaisI = []
for x in f.readline().split():
    finaisI.append(int(x))
print("Estados Finais = ",finaisI)

transicoes = []
for x in f.readline().split():
    aux = x.split(",")
    aux[2] = aux[2].replace(")","").replace("[","").replace("]","").replace(";","")
    t = (int(x[1]),x[3],list(aux[2]))
    transicoes.append(t)

print("Delta = ",transicoes,"\n")

cadeia = input("Digite a cadeia a ler analisada pelo autômato:")
while True:
    
    if cadeia != '':
        break
    else:
        print("Este autômato não reconhece cadeias vazias")
        cadeia = input("Por favor insira uma nova cadeia: ")



estadosAFD = preparaEstadosAFN_AFD()
transicoesFinais = preparaTransicoesAFN_AFD(estadosAFD)

AFNtoAFD()
listaFinal = remove_vazio(listaFinal)
resolve_AFN(list(cadeia[0]))
print(transicoesFinais)
print(estadosAFD)