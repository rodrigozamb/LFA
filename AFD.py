import pygame
f = open("./AFN/out.txt","r")

def automato(cadeia):
    global progEstados
    global progCadeia
    global interSimbolo 
    global interEstadoAtual
    global interTransicao
    print("cadeia = ",cadeia,"\n")
    
    interface_Start()

    i = estadoInicial
    for simbolo in cadeia:
        if simbolo not in alfabeto:
            pausar()
            interface_SymbolError(simbolo)
            print("O autômato rejeita esta cadeia")
            return False

        for t in transicoes:
            
            if(t[0]==i and t[1]==simbolo):
                interEstadoAtual = str(i)
                interSimbolo = str(simbolo)
                interTransicao = str(t)
                cadAux = " "+str(simbolo)
                estAux = " -> "+str(t[0])
                progCadeia  += cadAux
                progEstados += estAux
                print("Usando a transição - ",t)
                print("Estado ",i," lendo o símbolo ",simbolo," leva ao estado ", t[2],"\n")
                i = t[2]
                break
                
        pausar()
        screen.fill((0,0,0))
        layout(progEstados,progCadeia,interEstadoAtual,interSimbolo,interTransicao)
        pygame.display.update()
        

    if i in finais:
        pausar()
        print("O autômato aceita esta cadeia, estado final obtido :",i)
        estAux = " -> "+str(i)
        progEstados += estAux
        screen.fill((0,0,0))
        layout(progEstados,progCadeia,interEstadoAtual,interSimbolo,interTransicao)
        pygame.display.update()
        pausar()
        interface_End_Sucesso()
        pygame.quit()
        return True
    else:
        pausar()
        print("O autômato rejeita esta cadeia, estado final obtido :",i)
        estAux = " -> "+str(i)
        progEstados += estAux
        screen.fill((0,0,0))
        layout(progEstados,progCadeia,interEstadoAtual,interSimbolo,interTransicao)
        pygame.display.update()
        pausar()
        interface_End_Falha()
        pygame.quit()
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

cadeia = f.readline()

########################### Inteface Gráfica AFD##################################################


pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Autômato Finito Determinístico")
icone = pygame.image.load('ICON32.png')
pygame.display.set_icon(icone)

font = pygame.font.SysFont(None, 25)

def message(msg,color,x,y): 
    text = font.render(msg,True,color)
    screen.blit(text, [x,y])

def rev(s):
	return s[::-1]

def pausar():
    while True:
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                return 0

def layout(progEstados,progCadeia,interEstadoAtual,interSimbolo,interTransicao):
    message("Histórico de estados:",branco,28,5)
    message(progEstados,branco,28,24)
    message("Cadeia já analisada:",branco,375,5)
    message(progCadeia,branco,375,24)
    message("Estado Atual",branco,260,206)
    message(interEstadoAtual,branco,311,225)
    message("Simbolo Atual",branco,60,291)
    message(interSimbolo,branco,117,310)
    message("Transição",branco,480,291)
    message(interTransicao,branco,486,310)

def interface_Start():
    screen.fill((0,0,0))
    font2 = pygame.font.Font("freesansbold.ttf",30)
    text_surface = font2.render("Autômato Finito Determinístico",True,(126,45,126))
    screen.blit(text_surface,[70,182])
    message("Clique para iniciar o processo..",branco,150,320)
    pygame.display.update()
    
def interface_End_Sucesso():

    screen.fill((0,0,0))
    font2 = pygame.font.Font("freesansbold.ttf",30)
    text_surface = font2.render("O Autômato reconhece a cadeia",True,(51,255,51))
    screen.blit(text_surface,[70,182])
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
branco = (250,250,250)


automato(cadeia)