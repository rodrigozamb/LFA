f = open("casoAFN.txt","r")

def set_estados(listaEst):
    matches = [x for x in listaEst if (x not in listaFinal)]    
    return matches

def cria_delta(x):
    delta = []
    for i in x:
        for j in transicoes:
            if(j[0] == i):
                if(len(j[2])>0):
                    delta.append([int(i) for i in j[2]])
   
    listaSemRepeticao = set_estados(delta)

    if(len(listaSemRepeticao)>0):
        for k in listaSemRepeticao:
            listaFinal.append(k)
        for o in listaSemRepeticao:
            cria_delta(o)

        return listaSemRepeticao
    else:
        return []

def AFNtoAFD():
    est = [estadoInicial]
    listaFinal.append([estadoInicial])

    flag = True
    while(flag):
        est =  cria_delta(est)
        if(len(est)==0):
            flag=False

    print("Estados do AFD = ",listaFinal)



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

listaFinal = []


AFNtoAFD()