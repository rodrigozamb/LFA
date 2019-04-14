
f = open("./AFN/out.txt","r")

def automato(cadeia):
    print("cadeia = ",cadeia,"\n")

    i = estadoInicial
    for simbolo in cadeia:
        if simbolo not in alfabeto:
            print("O autômato rejeita esta cadeia")
            return False
    
        #podemos melhorar o desempenho aprimorando essa busca
        for t in transicoes:
            if(t[0]==i and t[1]==simbolo):
                print("Usando a transição - ",t)
                print("Estado ",i," lendo o símbolo ",simbolo," leva ao estado ", t[2],"\n")
                i = t[2]
                break
                

    if i in finais:
        print("O autômato aceita esta cadeia, estado final obtido :",i)
        return True
    else:
        print("O autômato rejeita esta cadeia, estado final obtido :",i)
        return False



estados = []
for x in f.readline().split():
    estados.append(x)

print("Q = ",estados)

alfabeto = []
for x in f.readline().split():
    alfabeto.append(x)
print("Alfabeto = ",alfabeto)

estadoInicial = int(f.readline()[0])
print("Estado Inicial = ",estadoInicial)

finais = []
for x in f.readline().split():
    finais.append(int(x))
print("Estados Finais = ",finais)


transicoes = []
for x in f.readline().split():
    t = (int(x[1]),x[3],int(x[5]))
    transicoes.append(t)

print("Delta = ",transicoes)

automato(f.readline())
