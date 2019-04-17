import sys
import pygame

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Autômato Finito Não Determinístico")
icone = pygame.image.load('ICON32N.png')
pygame.display.set_icon(icone)
font = pygame.font.SysFont(None, 25)


#abertura de arquivos para leitura dos dados referentes ao AFN
# e de arquivos que servirão de entrada para o AFD e esclarecimentos gerais
f = open("casoAFN.txt","r")
out = open("out.txt","w")
eq = open("EquivalenciasAFN-AFD.txt","w")

#inicialização de variáveis glorais de propósito auxiliar
listaFinal = []
path = []
pathFinais = []
superCaminhos = []
possivel = False
def set_estados(listaEst):
    matches = [x for x in listaEst if (x not in listaFinal)]    #Função que retira a repetição de estados 
    return matches

def remove_vazio(lista):
    x = [a for a in lista if( len(a)>0)]  #função que remove listas vazias de lista abranjedora
    return x

def cria_delta(cadeiaDeEstados):
    delta = []
    for alf in alfabeto:                 # função auxiliar que calcula a progressão de estados 
        aux2 = []                        # do autômato
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
    
def preparaEstadosAFN_AFD():
    est = [estadoInicial]
    listaFinal.append([estadoInicial])    #função auxiliar que calcula os estados do AFD
                                          #com base nos estados do AFN
    flag = True
    while(flag):
        est =  cria_delta(est)
        if(len(est)==0):
            flag=False

    return remove_vazio(listaFinal)

def remove_vazio_e_junta(lista):
    x = [a for a in lista if( len(a)>0)]  #função que remove estados vazios e contatena os não
    aux =[]                               #vazios em uma lista
    for i in x:
        for j in i:
            aux.append(j)
    return aux

def preparaTransicoesAFN_AFD(estados):
    listaEst = []                       #Calcula as transições correspondentes ao AFD
                                        #tendo como base os estados do AFN
    for alf in alfabeto:
        for est in estados:
            prox = calculaProxEstado(est,alf)
            #print(est," lendo ",alf," vai para ",prox)
            listaEst.append((est,alf,remove_vazio_e_junta(prox)))       

    return listaEst

def simplifica_Transicoes(transicoesFinais):
    global equivalencias
    global transicoesSimplificadas            #função que simplifica os estados compostos
    global estadosFinaisSimplificados         #para estar no padrão do algoritmo do AFD
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

        aux2 = [[y] for y in aux]
        if (confere_final(aux2)):
            estadosFinaisSimplificados.append(equivalencias[str(aux)])
        
def calculaProxEstado(Q,simbol):
    aux = []        
    for q in Q:                            #função que dado calcula o prox conjunto de estados
        for t in transicoes:               #possíveis de transição a partir de um determinado 
            if(t[0]==q and t[1]==simbol):  #estado lendo determinado símbolo
                aux.append(t[2])
    return aux

def printa_estados(estadosF):
    for i in range(len(estadosF)):   #função que escreve no arquivo os estados do AFD
        y = str(estadosF[i])         # OBS: os estados estão simplificados
        out.write(str(equivalencias[y]))
        if(i<len(estadosF)-1):
            out.write(" ")
        else:
            out.write("\n")

def printa_alfabeto():
    for i in range(len(alfabeto)):     #função que escreve no arquivo o alfabeto do AFD
        out.write(str(alfabeto[i]))
        if(i<len(alfabeto)-1):
            out.write(" ")
        else:
            out.write("\n")

def printa_finais():
    l = list(set(estadosFinaisSimplificados))   #função que escreve no arquivo os estados finais do AFD
    for i in range(len(l)):                     # OBS: os estados estão simplificados
        out.write(str(l[i]))
        if(i<len(l)-1):
            out.write(" ")
        else:
            out.write("\n")

def printa_transicoes(t):
    for i in range(len(t)):
        out.write(str(t[i]).replace(" ",""))  #função que escreve no arquivo transições do AFD
        if(i<len(t)-1):                       # OBS: os estados estão simplificados
            out.write(" ")
        else:
            out.write("\n")

def printa_equivalencias():
    eq.write("Equivalência de estados entre o AFN e o AFD")  #prita no arquivo correspondete a relação de 
    eq.write("\n")                                           #equivalencia entre os estados do AFN e do AFD
    for l in listaFinal:
        eq.write(str(l).rstrip('\n'))
        eq.write(" no AFN equivale ao ".rstrip('\n'))
        eq.write(str(equivalencias[str(l)]).rstrip('\n'))
        eq.write(" no AFD\n")

def AFNtoAFD():
   
    printa_estados(estadosAFD)    #Função geral de faz a transição de AFN para AFD
    printa_alfabeto()
    out.write(str(estadoInicial))
    out.write("\n")
    printa_finais()
    printa_transicoes(transicoesSimplificadas)
    out.write(cadeia)
    printa_equivalencias()

def pertence_alfabeto(a):
                            #função que diz se um dado símbolo faz parte do alfabeto
    for x in alfabeto:      
        if x == a:        
            return  True

def confere_final(l):
    for f in finaisI:     #função que diz se algum dos estados de uma dada lista é um
        for i in l:       #estado de aceitação
            for x in i:
                if(x == f):
                    return True
    return False

teste = []
def AFN_solve():
    flag = False       #função de solução característica de um AFN
    
    interface_Start()
    op = resolve_AFN_RECURSIVO(estadoInicial ,0) 
    caminho = [int(x) for x in path]
    interface_End_Sucesso()
    

    if(op == -1):
        return False
    else:
        for ef in finaisI:
            if ef in pathFinais:
                return True

    return False

def resolve_AFN_RECURSIVO(q,num):
    global pathFinais
    global teste
    global progEstados
    global interSimbolo
    global superCaminhos
                                    #função recursiva que resolve o AFN, criando todo o
    if(num == len(cadeia)):         # caminho da recursão
        pathFinais.append(int(q))
        superCaminhos.append(progEstados)
        message("Encontramos um caminho completo.. Clique para continuar",(128,128,128),129,336)
        pygame.display.update()
        pausar()
        return 0

    if cadeia[num] not in alfabeto:
        interface_SymbolError(cadeia[num])
        return -1


    for i in transicoes:
        if(i[0]==q and i[1]==cadeia[num]):            
           
            for j in i[2]:
                path.append(j)
                teste.append(j)
                
                estAux = " -> "+str(j)
                progEstados += estAux
                interSimbolo = cadeia[num]
                screen.fill((0,0,0))
                layout(progEstados,interSimbolo)
                pygame.display.update()
                pygame.time.wait(600)

                print(q," lendo o símbolo ",cadeia[num]," leva ao estado ",j)
                resolve_AFN_RECURSIVO(int(j),num+1)    

                if teste != []:
                    
                    progEstados = progEstados[:-5]
                    interSimbolo = cadeia[num]
                    screen.fill((0,0,0))
                    alertBack = font.render("Backtracking..",True,(255,0,0))
                    screen.blit(alertBack, [300,28])
                    layout(progEstados,interSimbolo)
                    pygame.display.update()
                    pygame.time.wait(300)
                    
                    print("Voltando na recursão e excluindo o ultimo estado alcançado..")
                    print(teste,"\n")
                    del teste[-1]
                

def processaAFN3(q,num):
    print("Estado atual = ",q)    #função que utiliza os estados traduzidos para solucionar o AFN
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
    contCadeia=0                      #função geral para solucionar o AFN
    i = [estadoInicial]               # utilizando os dados traduzidos
    resp = processaAFN3(i,contCadeia)
    
    if(resp):
        print("O autômato reconhece a cadeia : ",cadeia)
    else:
        print("O autômato não reconhece a cadeia : ",cadeia)

branco = (250,250,250)
def pausar():
    while True:
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                return 0

def interface_vazio_Falha():
    screen.fill((0,0,0))
    font2 = pygame.font.Font("freesansbold.ttf",30)
    text_surface = font2.render("O AFN não reconhece a cadeia vazia",True,(255,0,0))
    screen.blit(text_surface,[70,182])
    message("Clique para fechar..",(255,255,255),150,320)
    pygame.display.update()
    pausar()

def interface_vazio_Sucesso():
    screen.fill((0,0,0))
    font2 = pygame.font.Font("freesansbold.ttf",30)
    text_surface = font2.render("O AFN reconhece a cadeia vazia",True,(0,255,0))
    screen.blit(text_surface,[70,182])
    message("Clique para fechar..",branco,150,320)
    pygame.display.update()
    pausar()

#inicialização e preenchimento de uma lista que armazenará os estados descritos
#no arquivo fonte do AFN
estadosI = []
for x in f.readline().split():
    estadosI.append(x)
print("Q = ",estadosI)

#inicialização e preenchimento de uma lista que armazenará os símbolos do alfabeto 
# especificado no arquivo fonte do AFN
alfabeto = []
for x in f.readline().split():
    alfabeto.append(x)
print("Alfabeto = ",alfabeto)

#inicialização e atribuição de valor de uma variável que armazenará o estado inicial 
# do autômato
estadoInicial = int(f.readline()[0])
print("Estado Inicial = ",estadoInicial)

#inicialização e preenchimento de uma lista que armazenará os estados de aceitação 
# especificados no arquivo fonte do AFN
finaisI = []
for x in f.readline().split():
    finaisI.append(int(x))
print("Estados Finais = ",finaisI)

#inicialização e preenchimento de uma lista de tuplas que armazenará as transições de estados 
#especificados no arquivo fonte do AFN
transicoes = []
for x in f.readline().split():
    aux = x.split(",")
    aux[2] = aux[2].replace(")","").replace("[","").replace("]","").replace(";","")
    t = (int(x[1]),x[3],list(aux[2]))
    transicoes.append(t)

print("Delta = ",transicoes,"\n")

#declaração de variáveis auxiliares na conversão de AFN para AFD
transicoesSimplificadas = []
equivalencias = {}
estadosFinaisSimplificados = []

def message(msg,color,x,y): 
    text = font.render(msg,True,color)
    screen.blit(text, [x,y])


#inicialização de leitura da cadeia a ser processada pelo autômato
cadeia = input("Digite a cadeia a ler analisada pelo autômato:")

if (estadoInicial in finaisI and cadeia ==''):
    interface_vazio_Sucesso()
    pygame.display.update()
else:
    if (estadoInicial not in finaisI and cadeia ==''):
        interface_vazio_Falha()
        pygame.display.update()
    else:
        possivel = True

#coversão de estados do autômato AFN para estados de um AFD
estadosAFD = preparaEstadosAFN_AFD()

#Conversão das transições do autômato AFN para transições de um AFD
transicoesFinais = preparaTransicoesAFN_AFD(estadosAFD)

#formatação da lista auxiliar de estados do AFD
listaFinal = remove_vazio(listaFinal)

#resolve_AFN_AFDMODE(list(cadeia[0]))
#print(estadosAFD)


#simplifica as transições de estados de forma que o algoritmo do AFD
#consiga ler propriamente
simplifica_Transicoes(transicoesFinais)

#Função que gera o arquivo fonte base para o AFD
AFNtoAFD()

###############################################################################


def rev(s):
	return s[::-1]


def layout(progEstados,interSimbolo):
    message("Progressão Recursiva:",branco,28,28)
    message(progEstados,branco,40,220)
    message("Símbolo atual:",branco,328,70)
    message(interSimbolo,branco,328,85)
    
def interface_Start():
    screen.fill((0,0,0))
    font2 = pygame.font.Font("freesansbold.ttf",30)
    text_surface = font2.render("Autômato Finito Não Determinístico",True,(225,158,0))
    screen.blit(text_surface,[70,182])
    message("Clique para iniciar o processo..",branco,150,320)
    pygame.display.update()
    pausar()

def interface_End_Sucesso():

    screen.fill((0,0,0))
    message("O Autômato reconhece as cadeias",branco,30,52)

    q = 120
    for i in superCaminhos:

        if(eh_valida(i)):
            message(str(i),(0,255,0),140,q)
        else:
            message(str(i),(255,0,0),140,q)
        q+=18

    message("Clique para fechar..",branco,150,320)
    pygame.display.update()
    pausar()

def interface_End_Falha():

    screen.fill((0,0,0))
    font2 = pygame.font.Font("freesansbold.ttf",30)
    text_surface = font2.render("O Autômato não reconhece a cadeia",True,(204,0,0))
    screen.blit(text_surface,[70,182])
    message("Clique para fechar..",branco,150,320)
    pygame.display.update()
    pausar()





def eh_valida(l):
    a = l[::-1]
    if int(a[0]) in finaisI:
        return True
    else:
        return False

def interface_SymbolError(s):

    screen.fill((0,0,0))
    font2 = pygame.font.Font("freesansbold.ttf",30)
    aux = "Símbolo inválido identificado - '"+s+"'"
    text_surface = font2.render(aux,True,(0,38,153))
    screen.blit(text_surface,[70,182])
    message("Clique para fechar..",branco,150,320)
    pygame.display.update()
    pausar()

progEstados = ""
progCadeia = ""
interSimbolo = ""
interEstadoAtual = ""
interTransicao = ""




if possivel == True:        
    #resolve o AFN na sua forma característica 
    if(AFN_solve()):
        print("O AFN aceita a cadeia : ",cadeia)
    else:
        print("O AFN não aceita a cadeia : ",cadeia)
