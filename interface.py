import pygame

a = "a -> n -> c"
print(a[::-1].replace("c >- ",""))
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Autômato Finito Não-Determinístico")

done = False
font = pygame.font.SysFont(None, 25)
aqui = "10010101101011"

def message(msg,color): 
    text = font.render(msg,True,color)
    screen.blit(text, [260,450])

def rev(s):
	return s[::-1]


X1 = 7
Y1 = 15
Xbase = 261
Ybase = 450
i = 0
while not done:
    # This event loop empties the event queue each frame.
    for event in pygame.event.get():
        # Quit by pressing the X button of the window.
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            i+=1
            Xbase+=8
             # MOUSEBUTTONDOWN events have a pos and a button attribute
            # which you can use as well. This will be printed once per
            # event / mouse click.
            print('In the event loop:', event.pos, event.button)
            aqui = rev(aqui)    
    screen.fill((0,0,0))
    pygame.draw.rect(screen, (255,0,0), (Xbase,Ybase,X1,Y1))
    message(aqui,(250,250,250))
    pygame.display.update() 
