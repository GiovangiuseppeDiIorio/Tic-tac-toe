# Gioco tris o tic tac toe, creato dallo studente di ing. informatica Giovangiuseppe Di Iorio

import pygame, random

pygame.init() # Inizializzo il gioco

CLOCK = pygame.time.Clock() # Per gli FPS

LARGHEZZA, ALTEZZA = 800, 600
SCHERMO = pygame.display.set_mode((LARGHEZZA, ALTEZZA)) # larghezza, altezza

def immagine_in_scala(file:str, LARGHEZZA_ICONA:int = 40, ALTEZZA_ICONA:int = 40):
    # Prende il percorso del documento del file, e in base alla larghezza e altezza ridimensiona
    immagine = pygame.image.load(file)
    trasformato = pygame.transform.scale(immagine, (LARGHEZZA_ICONA, ALTEZZA_ICONA))
    return trasformato

# Immagini
LARGHEZZA_ICONA, ALTEZZA_ICONA = 40, 40
ICONA_FINESTRA = pygame.image.load("img/icona.png")
SFONDO = immagine_in_scala("img/sfondo.png", 1000, 1000)
ICONA = immagine_in_scala("img/icona.png", 90, 90)
ICONA_AUDIO = immagine_in_scala("img/audio.png")
ICONA_NOAUDIO = immagine_in_scala("img/no-audio.png")
ICONA_EXIT = immagine_in_scala("img/exit.png")

ICONA_GIOCA = immagine_in_scala("img/gioca.png")
ICONA_O = immagine_in_scala("img/o blu.png", 90, 90)
ICONA_X = immagine_in_scala("img/x rossa.png", 90, 90)

# Colori
ROSSO = (255, 0, 0)
VERDE = (0, 255, 0)
BLU = (0, 0, 255)
NERO = (0, 0, 0)
BIANCO = (255, 255, 255)

# Font
FONT_TITOLO = pygame.font.Font("Violet Smile.ttf", (LARGHEZZA*ALTEZZA)//6000)
FONT = pygame.font.Font("Violet Smile.ttf", (LARGHEZZA*ALTEZZA)//12000)

pygame.display.set_caption("Tris") # Titolo finestra
pygame.display.set_icon(ICONA_FINESTRA) # Icona finestra

# Musica di sottofondo
pygame.mixer.music.load("music/soundtrack.mp3")

# Variabili
no_audio = True # Per l'audio
sch_prin = True # Schermata principale, False se il player gioca
gioca = False # Se vero si inizia il gioco, e la sch_prin diventa False
giocatore1 = True # Inserisco True per far iniziare il giocatore 1
posizioni_in_x = [285, 395, 505] # Prende i centri in x delle singole caselle
posizioni_in_y = [165, 275, 385] # Prende i centri in y delle singole caselle
griglia = [
    [-1,-1,-1],
    [-1,-1,-1],
    [-1,-1,-1]
]
CENTRO = LARGHEZZA/2-105
VERTICALE = ALTEZZA//12


def click_su(x,y, var_x, var_y, pos_ogg_x, pos_ogg_y): # Verifica se è stato eseguito il click nell'area (x,y)

    differenza_x = pos_ogg_x - var_x
    somma_x = pos_ogg_x + var_x
    differenza_y = pos_ogg_y - var_y
    somma_y = pos_ogg_y + var_y

    if differenza_x <= x <= somma_x and differenza_y <= y <= somma_y:
        return True
    return False

def rettangolo(x, y, larghezza, altezza, bordo = 3, colore = BIANCO):
    pygame.draw.rect(SCHERMO, colore, pygame.Rect(x-10, y, larghezza, altezza),  bordo)    

def bottone(x, y, testo, icona, larghezza, altezza, bordo = -1, colore = BIANCO):
    stampa(x, y, testo)
    SCHERMO.blit(icona, (x+125, y+10))
    rettangolo(x, y, larghezza, altezza, bordo, colore)

def stampa(x, y, testo, colore = BIANCO, font = FONT):
    Testo = font.render(testo, True, colore)
    SCHERMO.blit(Testo, (x, y))

def audio(audio): # Attiva / disattiva l'audio di gioco
    if audio:
        pygame.mixer.music.play(-1) # La musica viene messa in loop
    else:
        pygame.mixer.music.pause() # Stoppo la musica

# Schermata principale
def schermata_principale():

    SCHERMO.blit(SFONDO, (0, 0)) # Inserisce lo sfondo
    
    stampa(CENTRO, ALTEZZA//12, "Tris", BIANCO, FONT_TITOLO)
    SCHERMO.blit(ICONA,  (LARGHEZZA/2+45, ALTEZZA//8.5-10))

    bottone(CENTRO, VERTICALE+130, "Gioca", ICONA_GIOCA, CENTRO//1.5, (VERTICALE+130)//2.9)
    bottone(CENTRO, VERTICALE+210, "Audio", ICONA_AUDIO, CENTRO//1.5, (VERTICALE+210)//4)
    bottone(CENTRO, VERTICALE+300, "Esci", ICONA_EXIT, CENTRO//1.5, (VERTICALE+300)//6)

def crea_griglia():
    for x in range(230, 451, 110):
        for y in range(110, 331, 110):
            rettangolo(x, y, 110-5, 110-5,1, NERO)

def casella_selezionata(x, y):
    for i in range(len(posizioni_in_x)):
        for j in range(len(posizioni_in_y)):
            if click_su(x, y, 40, 40, posizioni_in_x[i], posizioni_in_y[j]):
                return (i, j)

def libero(x, y):
    casella = casella_selezionata(x, y)
    if casella != None:
        x_cas = casella[0]
        y_cas = casella[1]
        if griglia[x_cas][y_cas] == -1:
            return True
    return False

def posiziona(x, y, giocatore1):
    casella = casella_selezionata(x, y)
    if casella != None:
        x_cas = casella[0]
        y_cas = casella[1]
        if libero(x, y):
            if giocatore1:
                griglia[x_cas][y_cas] = 1 # Giocatore 1 (X)
            else:
                griglia[x_cas][y_cas] = 0 # Giocatore 2 (O)

def inserisci_foto():
    for i in range(len(griglia)):
        for j in range(len(griglia[0])):
            if griglia[i][j] == 1: # Giocatore 1 (X)
                SCHERMO.blit(ICONA_X, (posizioni_in_x[i]-60,posizioni_in_y[j]-50))
            elif griglia[i][j] == 0: # Giocatore 2 (O)
                SCHERMO.blit(ICONA_O, (posizioni_in_x[i]-60,posizioni_in_y[j]-50))

def verifica_riga(riga):
    for i in range(len(griglia)):
        primo_elemento = griglia[0][riga]
        successivi_al_primo = griglia[i][riga]
        if primo_elemento == -1 or primo_elemento != successivi_al_primo:
            return False
    return True

def verifica_colonna(colonna):
    for i in range(len(griglia)):
        primo_elemento = griglia[colonna][0]
        successivi_al_primo = griglia[colonna][i]
        if primo_elemento == -1 or primo_elemento != successivi_al_primo:
            return False
    return True

def verifica_diagonale_principale():
    for i in range(len(griglia)):
        elemento = griglia[0][0]
        succ_elemento = griglia[i][i]
        if elemento == -1 or elemento != succ_elemento:
            return False
    return True

def verifica_diagonale_secondaria():
    for i in range(len(griglia)):
        elemento = griglia[0][-1]
        succ_elemento = griglia[i][-i-1]
        if elemento == -1 or elemento != succ_elemento:
            return False
    return True

def verifica_vittoria():
# se l'utente ha fatto tris in diagonale, orizonatale o verticale ha vinto, ritorna True, altrimenti False.
    for i in range(len(griglia)):
        if verifica_riga(i):
            return griglia[0][i]
        elif verifica_colonna(i):
            return griglia[i][0]
        elif verifica_diagonale_principale():
            return griglia[0][0]
        elif verifica_diagonale_secondaria():
            return griglia[0][-1]
    return False

def vittoria():
    # l'utente le uniche possibilità che ha è quella di chiudere il gioco di riprovare.
    val_vincitore = verifica_vittoria()
    complimenti = "Complimenti hai vinto, giocatore: "
    if val_vincitore == 0:
        stampa(CENTRO-200, ALTEZZA//2, complimenti+"O", BLU, FONT)
    else:
        stampa(CENTRO-200, ALTEZZA//2, complimenti+"X", BLU, FONT)
    stampa(CENTRO-55, ALTEZZA/1.2, "Premi P per uscire", ROSSO, FONT)
    stampa(CENTRO-105, ALTEZZA/12, "Premi R per ricominciare", VERDE, FONT)

def reset_griglia():
    for i in range(len(griglia)):
        for j in range(len(griglia)):
            griglia[i][j] = -1

while True:

    if sch_prin:
        schermata_principale()
    else:
        SCHERMO.blit(SFONDO, (0,0))
        crea_griglia()
        if giocatore1:
            stampa(CENTRO-110, ALTEZZA//12, "Tocca al giocatore 1 (X)", BLU)
        else:
            stampa(CENTRO-110, ALTEZZA//12, "Tocca al giocatore 2 (O)", VERDE)
        inserisci_foto()
        if verifica_vittoria() != False:
            SCHERMO.blit(SFONDO, (0,0))
            vittoria()
    
    stampa(CENTRO-55, ALTEZZA/1.2, "Premi P per uscire", VERDE, FONT)

    for evento in pygame.event.get():
        x, y = pygame.mouse.get_pos()
        # rettangolo(x,y-5, 10,10,0,BLU) # Per il debug, mi dice dove si muove il cursore

        if evento.type == pygame.MOUSEBUTTONDOWN:
            # rettangolo(x,y-5, 10,10,0,VERDE) # Per il debug, mi dice dove clicca il cursore
            
            # Per la schermata di gioco
            if sch_prin == False:

                if libero(x, y):
                    posiziona(x, y, giocatore1)
                    if giocatore1:
                        giocatore1 = False
                    else:
                        giocatore1 = True

            # Per la schermata principale
            if sch_prin:

                # Click su Gioca
                if click_su(x, y, 200, 25, CENTRO, VERTICALE+150):
                    sch_prin = False
                    
                # Click su Audio
                if click_su(x, y, 200, 27, CENTRO, VERTICALE+230):
                    if no_audio == False:
                        audio(no_audio)
                        no_audio = True
                    else:
                        audio(no_audio)
                        no_audio = False

                # Click su Esci
                if click_su(x, y, 200, 25, CENTRO, VERTICALE+320):
                    pygame.quit() # Chiude il gioco
                    exit() # Chiude il programma

        if evento.type == pygame.KEYDOWN:

            # Per resettare il gioco
            if sch_prin == False and evento.key == pygame.K_r:
                sch_prin = True
                giocatore1 = True
                reset_griglia()

            # Per chiudere il gioco ovunque ci si trova
            if evento.key == pygame.K_p:
                pygame.quit() # Chiude il gioco
                exit() # Chiude il programma

    pygame.display.flip() # Per i rettangoli
    pygame.display.update() # Aggiorna la finestra
    CLOCK.tick(30) # Setta gli FPS bloccati a 30