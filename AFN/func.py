
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
    print(listaEst)
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
    estad = preparaEstadosAFN_AFD()
    printa_estados(estad)
    printa_alfabeto()
    out.write(str(estadoInicial))
    out.write("\n")
    printa_finais()
    printa_transicoes(preparaTransicoesAFN_AFD(estad))

def pertence_alfabeto(a):
    if a in alfabeto:
        return True
    else:
        return False

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
            if(t[0]==int(i) and t[1]==cadeia[pos]):
                pos+=1
                print(q," lendo ",cadeia[pos]," leva a ",t[2])
                for es in t[2]:
                    if es != []:
                        processaAFN(es)
    return False





def processaAFN2(q,pos):

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
    
    print(q ," lendo ",cadeia)

    print(q,"\n\n",transicoes)

    for i in q:
        for t in transicoes:
            
            if(t[0]==i and t[1]==cadeia[pos]):
                pos+=1
                print(q," lendo ",cadeia[pos]," leva a ",t[2])
                for es in t[2]:
                    if es != []:
                        processaAFN2(es)
    print("deu ruim")
    return False





def resolve_AFN(cadeia):
    contCadeia=0
    print(processaAFN2(list(cadeia[0]),contCadeia))