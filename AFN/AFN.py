f = open("casoAFN.txt","r")
out = open("out.txt","w")
eq = open("EquivalenciasAFN-AFD.txt","w")
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

def simplifica_Transicoes(transicoesFinais):
    global equivalencias
    global transicoesSimplificadas
    global estadosFinaisSimplificados
    c=0
    for i in transicoesFinais:
        (x,y,z) = i
        if str(x) not in equivalencias:
            equivalencias[str(x)] = c
            c+=1
    
    for tra in transicoesFinais:
        (x,y,z) = tra
        xs = equivalencias[str(x)]
        ys = int(y)
        aux = [int (a) for a in z]
        zs = equivalencias[str(aux)]
        transicoesSimplificadas.append((xs,ys,zs))

        if (confere_final([aux])):
            estadosFinaisSimplificados.append(equivalencias[str(aux)])
        
    
    

def calculaProxEstado(Q,simbol):
    aux = []
    for q in Q:
        for t in transicoes:
            if(t[0]==q and t[1]==simbol):
                aux.append(t[2])
    return aux

def printa_estados(estadosF):
    print("asdas   ",estadosF)
    for i in range(len(estadosF)):
        y = str(estadosF[i])
        out.write(str(equivalencias[y]))
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
    l = list(set(estadosFinaisSimplificados))
    for i in range(len(l)):
        out.write(str(l[i]))
        if(i<len(l)-1):
            out.write(" ")
        else:
            out.write("\n")

def printa_transicoes(t):
    for i in range(len(t)):
        out.write(str(t[i]).replace(" ",""))
        if(i<len(t)-1):
            out.write(" ")
        else:
            out.write("\n")

def printa_equivalencias():
    eq.write("Equivalência de estados entre o AFN e o AFD")
    eq.write("\n")
    for l in listaFinal:
        eq.write(str(l).rstrip('\n'))
        eq.write(" no AFN equivale ao ".rstrip('\n'))
        eq.write(str(equivalencias[str(l)]).rstrip('\n'))
        eq.write(" no AFD\n")


def AFNtoAFD():
   
    printa_estados(estadosAFD)
    printa_alfabeto()
    out.write(str(estadoInicial))
    out.write("\n")
    printa_finais()
    printa_transicoes(transicoesSimplificadas)
    out.write(cadeia)
    printa_equivalencias()

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


testando = []
testando2 = []

def AFN_solve():
    flag = False
    op = resolve_AFN_RECURSIVO(estadoInicial ,0)
    caminho = [int(x) for x in testando]
    #print(caminho)
    #print(testando2)
    if(op == -1):
        return False
    else:
        for ef in finaisI:
            if ef in testando2:
                return True

    return False

def resolve_AFN_RECURSIVO(q,num):
    global testando2

    #print("n = ",num , "tam = ",len(cadeia))
    if(num == len(cadeia)):
      
      
        #print("q = ",q,"n = ",num , "tam = ",len(cadeia))
        testando2.append(int(q))
        return 0

    if cadeia[num] not in alfabeto:
        return -1

    for i in transicoes:
        if(i[0]==q and i[1]==cadeia[num]):
            
            for j in i[2]:
                testando.append(j)
                resolve_AFN_RECURSIVO(int(j),num+1)

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

def resolve_AFN_AFDMODE(cadeiai):
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

transicoesSimplificadas = []
equivalencias = {}
estadosFinaisSimplificados = []


cadeia = input("Digite a cadeia a ler analisada pelo autômato:")
while True:
    
    if cadeia != '':
        break
    else:
        print("Este autômato não reconhece cadeias vazias")
        cadeia = input("Por favor insira uma nova cadeia: ")



estadosAFD = preparaEstadosAFN_AFD()
transicoesFinais = preparaTransicoesAFN_AFD(estadosAFD)


listaFinal = remove_vazio(listaFinal)
#resolve_AFN_AFDMODE(list(cadeia[0]))
#print(estadosAFD)

if(AFN_solve()):
    print("O AFN aceita a cadeia : ",cadeia)
else:
    print("O AFN não aceita a cadeia : ",cadeia)
simplifica_Transicoes(transicoesFinais)

AFNtoAFD()
print(equivalencias)
print(transicoesSimplificadas)
print(listaFinal)
print(list(set(estadosFinaisSimplificados)))