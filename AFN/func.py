

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

def intercade_vazio_Sucesso():
    screen.fill((0,0,0))
    font2 = pygame.font.Font("freesansbold.ttf",30)
    text_surface = font2.render("O Autômato reconhece a cadeia vazia",True,(0,255,0))
    screen.blit(text_surface,[70,182])
    message("Clique para fechar..",branco,150,320)
    pygame.display.update()
    pausar()

def interface_vazio_Falha():
    screen.fill((0,0,0))
    font2 = pygame.font.Font("freesansbold.ttf",30)
    text_surface = font2.render("O Autômato não reconhece a cadeia vazia",True,(255,0,0))
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
branco = (250,250,250)



#pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Autômato Finito Não Determinístico")
icone = pygame.image.load('ICON32N.png')
pygame.display.set_icon(icone)

font = pygame.font.SysFont(None, 25)
