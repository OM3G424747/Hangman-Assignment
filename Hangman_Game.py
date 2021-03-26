"""
TO DO:

Create a list with all letters from the alphabet 

pop a letter from the list after it's guessed by a player or the CPU
(create a main menu)set up the game for 2 player play or player VS CPU

add a library of words for the game

"""
#TODO - import all letters as game objects 

import pygame, random, os

Screen_Width = 1600
Screen_Height = 800
Screen_Title = "Hangman Game" #Sets name on gamewindow 
White_Colour = (255,255,255) #colours set according to RGB - R 255 G 255  B 255
Black_Colour = (0,0,0)
Red_Colour = (255,0,0)
Green_Colour = (0,255,0)
Blue_Colour = (0,0,255)
Grey_Colour = (100,100,100)
LightGrey_Colour = (200,200,200)
#TextWidth Dictionary contains width settings for each of the letters being used 
textWidth =  {"A": 26, "B": 20, "C": 22, "D": 26, "E": 17, "F": 17, "G": 24, "H": 28, "I": 13, "J": 16, "K": 25, "L": 19, "M": 33, "N": 28, "O": 25, "P": 19, "Q": 27, "R": 24, "S": 14, "T": 22, "U": 25, "V": 25, "W": 34, "X": 28, "Y": 25, "Z": 20}
#TextCentering Dictionary includes spacing to help center the text images based on their size
textCentering = {"A": 4, "B": 2, "C": 2, "D": 2, "E": 5, "F": 6, "G": 2, "H": 0, "I": 7, "J": 7, "K": 1, "L": 4, "M": 2, "N": 0, "O": 1, "P": 5, "Q": -4, "R": 3, "S": 7, "T": 3, "U": 1, "V": 2, "W": -3, "X": 0, "Y": 1, "Z": 3}
Clock = pygame.time.Clock()
Alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
Word_List = []
OpenFile = "assets/wordList.txt"
OpenFile = open(OpenFile)
for line in OpenFile:
    line = line.rstrip("\n")
    Word_List.append(line)

print(Word_List)
GuessList = []

#lists used for word selection list 
SelectionY_pos = [] #Yposition for word selection - Placed outside of gameloop to make text move
selectionRangeList = []


class GameObject: #class for defining game objects that will be drawn onto the game screen and moved arround
    def __init__(self, image_path, X_pos, Y_pos, Width, Height):
        Object_Image = pygame.image.load(image_path) #Loads image to be set
        self.Image = pygame.transform.scale(Object_Image, (Width, Height)) #Scales the image that's been loaded in 
        self.X_pos = X_pos
        self.Y_pos = Y_pos
        self.Width = Width
        self.Height = Height
    
    def Draw (self,background): #This function is used to draw the object on the game screen
        background.blit(self.Image,(self.X_pos,self.Y_pos)) #Blit funtion is used to draw imaghes to the game screen/ surface selected along with the X and Y Pos taken in the form of a tuple 

class keyselection:
#TODO - unclude section in function to take mouse X & Y pos, and "Click" bool to confirm if a button is clicked - corrolate with list for input to guess the letter 
    def __init__(self, keyBoardLetters, keyGuessed, Game_Screen, StartX_pos, MouseX_pos, MouseY_pos, Click, KeyPress):
        self.Game_Screen = Game_Screen
        self.StartX_pos = StartX_pos
        self.guessedLetters = keyGuessed
        self.buttonX_posList = []
        self.buttonY_posList = []
        self.buttonWidth = 55 #sets width of keyboard buttons 
        self.buttonHeight = 55 #set height of keyboard buttons 
        self.buttonSpacing = self.buttonWidth + 17 #number added determines the spacing between buttons 
        self.letterSpacing = 10
        self.numberOfButtonsinRow = 10 
        self.rowButtonCounter = 0
        self.topRowY_pos = 550
        self.buttonCount = 0
        self.keyBoardLetters = keyBoardLetters
        buttonShadowSize = 5
        letterX_pos = 0
        defaultButtonColour = (250,250,250)
        highlightButtonColour = (100,250,250)
        buttonShadowColour = (100,100,100)
        numberOfRows = 0
        
       
    
        for Letter in self.keyBoardLetters:
            if self.buttonCount == 0: #used to check if starting point / upper right corner of keyselection
                self.buttonX_posList.append(self.StartX_pos)
                self.buttonY_posList.append(self.topRowY_pos)
                if Letter.capitalize() not in self.guessedLetters:
                    pygame.draw.rect(Game_Screen, buttonShadowColour, [self.buttonX_posList[self.buttonCount] + buttonShadowSize,self.topRowY_pos + buttonShadowSize,self.buttonWidth + buttonShadowSize,self.buttonHeight + buttonShadowSize]) #sets surface shadown behind button
                    
                    if KeyPress == Letter.capitalize():
                        pygame.draw.rect(Game_Screen, highlightButtonColour, [self.buttonX_posList[self.buttonCount] + buttonShadowSize -2,self.topRowY_pos + buttonShadowSize -2,self.buttonWidth + buttonShadowSize -2,self.buttonHeight + buttonShadowSize -2])
                        self.Game_Screen.blit(pygame.transform.scale(pygame.image.load("assets/"+Letter.capitalize()+".png"), (int(textWidth[Letter.capitalize()] *1.2)+ buttonShadowSize -2, int(21*1.2)+ buttonShadowSize -2)),(self.buttonX_posList[self.buttonCount] + 12+ buttonShadowSize -2,self.topRowY_pos + 15+ buttonShadowSize -2)) 
                        GuessList.append(Letter.capitalize())
                    
                    elif MouseX_pos >= self.buttonX_posList[self.buttonCount] and MouseX_pos <= self.buttonX_posList[self.buttonCount] + self.buttonWidth and MouseY_pos >= self.topRowY_pos and MouseY_pos <= self.topRowY_pos + self.buttonHeight and Click == False: #check for mouse over button
                        pygame.draw.rect(Game_Screen, highlightButtonColour, [self.buttonX_posList[self.buttonCount],self.topRowY_pos,self.buttonWidth,self.buttonHeight]) #sets surface, colour and X-pos,Y-pos+size for the rectangle to be drawn
                        self.Game_Screen.blit(pygame.transform.scale(pygame.image.load("assets/"+Letter.capitalize()+".png"), (int(textWidth[Letter.capitalize()] *1.2), int(21*1.2))),(self.buttonX_posList[self.buttonCount] + 12,self.topRowY_pos + 15)) 
                    
                    elif MouseX_pos >= self.buttonX_posList[self.buttonCount] and MouseX_pos <= self.buttonX_posList[self.buttonCount] + self.buttonWidth and MouseY_pos >= self.topRowY_pos and MouseY_pos <= self.topRowY_pos + self.buttonHeight and Click == True:
                        pygame.draw.rect(Game_Screen, highlightButtonColour, [self.buttonX_posList[self.buttonCount] + buttonShadowSize -2,self.topRowY_pos + buttonShadowSize -2,self.buttonWidth + buttonShadowSize -2,self.buttonHeight + buttonShadowSize -2])
                        self.Game_Screen.blit(pygame.transform.scale(pygame.image.load("assets/"+Letter.capitalize()+".png"), (int(textWidth[Letter.capitalize()] *1.2)+ buttonShadowSize -2, int(21*1.2)+ buttonShadowSize -2)),(self.buttonX_posList[self.buttonCount] + 12+ buttonShadowSize -2,self.topRowY_pos + 15+ buttonShadowSize -2)) 
                        GuessList.append(Letter.capitalize())
                    
                    else:
                        pygame.draw.rect(Game_Screen, defaultButtonColour, [self.buttonX_posList[self.buttonCount],self.topRowY_pos,self.buttonWidth,self.buttonHeight]) #sets surface, colour and X-pos,Y-pos+size for the rectangle to be drawn
                        self.Game_Screen.blit(pygame.transform.scale(pygame.image.load("assets/"+Letter.capitalize()+".png"), (int(textWidth[Letter.capitalize()] *1.2), int(21*1.2))),(self.buttonX_posList[self.buttonCount] + 12,self.topRowY_pos + 15)) 
                self.buttonCount = self.buttonCount + 1
                self.rowButtonCounter = self.rowButtonCounter + 1
            
            elif self.buttonCount > 0 and self.buttonCount < len(self.keyBoardLetters): #used to check continuation based on starting point 
                if self.rowButtonCounter == 0:  #used to check if it's the start of a new row or not. 0 = start of new row
                    self.buttonX_posList.append(self.StartX_pos )
                elif self.rowButtonCounter > 0: #used to see if it's the second button in a row being displayed or not
                    self.buttonX_posList.append(self.buttonX_posList[self.buttonCount - 1] + self.buttonSpacing )
                self.buttonY_posList.append(self.topRowY_pos)
                if Letter.capitalize() not in self.guessedLetters:
                    letterX_pos = self.buttonX_posList[self.buttonCount] + self.letterSpacing + textCentering[Letter.capitalize()] #variable used to calculate X_Pos of the letter
                    pygame.draw.rect(Game_Screen, buttonShadowColour, [self.buttonX_posList[self.buttonCount] + buttonShadowSize,self.topRowY_pos + buttonShadowSize,self.buttonWidth + buttonShadowSize,self.buttonHeight + buttonShadowSize]) #sets shadow on remaining alphabet buttons
                    
                    if KeyPress == Letter.capitalize():
                        pygame.draw.rect(Game_Screen, highlightButtonColour, [self.buttonX_posList[self.buttonCount] + buttonShadowSize -2,self.topRowY_pos + buttonShadowSize-2,self.buttonWidth + buttonShadowSize-2,self.buttonHeight + buttonShadowSize-2])
                        self.Game_Screen.blit(pygame.transform.scale(pygame.image.load("assets/"+Letter.capitalize()+".png"), (int(textWidth[Letter.capitalize()] *1.2) + buttonShadowSize-2, int(21*1.2)+ buttonShadowSize-2)),(letterX_pos + buttonShadowSize-2,self.buttonY_posList[self.buttonCount] + 15 + buttonShadowSize-2))
                        GuessList.append(Letter.capitalize())
                    
                    elif MouseX_pos >= self.buttonX_posList[self.buttonCount] and MouseX_pos <= self.buttonX_posList[self.buttonCount] + self.buttonWidth and MouseY_pos >= self.topRowY_pos and MouseY_pos <= self.topRowY_pos + self.buttonHeight and Click == False:
                        pygame.draw.rect(Game_Screen, highlightButtonColour, [self.buttonX_posList[self.buttonCount],self.buttonY_posList[self.buttonCount],self.buttonWidth,self.buttonHeight]) #sets surface, colour and X-pos,Y-pos+size for the rectangle to be drawn
                        self.Game_Screen.blit(pygame.transform.scale(pygame.image.load("assets/"+Letter.capitalize()+".png"), (int(textWidth[Letter.capitalize()] *1.2), int(21*1.2))),(letterX_pos,self.buttonY_posList[self.buttonCount] + 15)) 
                    
                    elif MouseX_pos >= self.buttonX_posList[self.buttonCount] and MouseX_pos <= self.buttonX_posList[self.buttonCount] + self.buttonWidth and MouseY_pos >= self.topRowY_pos and MouseY_pos <= self.topRowY_pos + self.buttonHeight and Click == True:
                        pygame.draw.rect(Game_Screen, highlightButtonColour, [self.buttonX_posList[self.buttonCount] + buttonShadowSize -2,self.topRowY_pos + buttonShadowSize-2,self.buttonWidth + buttonShadowSize-2,self.buttonHeight + buttonShadowSize-2])
                        self.Game_Screen.blit(pygame.transform.scale(pygame.image.load("assets/"+Letter.capitalize()+".png"), (int(textWidth[Letter.capitalize()] *1.2) + buttonShadowSize-2, int(21*1.2)+ buttonShadowSize-2)),(letterX_pos + buttonShadowSize-2,self.buttonY_posList[self.buttonCount] + 15 + buttonShadowSize-2)) 
                        GuessList.append(Letter.capitalize())
                    
                    else:
                        pygame.draw.rect(Game_Screen, defaultButtonColour, [self.buttonX_posList[self.buttonCount],self.buttonY_posList[self.buttonCount],self.buttonWidth,self.buttonHeight]) #sets surface, colour and X-pos,Y-pos+size for the rectangle to be drawn
                        self.Game_Screen.blit(pygame.transform.scale(pygame.image.load("assets/"+Letter.capitalize()+".png"), (int(textWidth[Letter.capitalize()] *1.2), int(21*1.2))),(letterX_pos,self.buttonY_posList[self.buttonCount] + 15))  
                        #buttonHoldCount = 0 #resets
                    #TODO - Update to center all letters based on their width!
                    
                    
                self.buttonCount = self.buttonCount + 1
                self.rowButtonCounter = self.rowButtonCounter + 1
                if self.rowButtonCounter == self.numberOfButtonsinRow: #condition to check if the max number of buttons for the row have been reached
                    self.topRowY_pos = self.topRowY_pos + self.buttonSpacing #Adjusts the Y_pos down based on button spacing
                    numberOfRows = numberOfRows + 1
                    self.numberOfButtonsinRow = self.numberOfButtonsinRow - numberOfRows #reduces the number of buttons in the row based on the number of rows on display
                    self.StartX_pos = self.StartX_pos + 50 #adds 50 points to the right of the X_Pos of the start of the previous row 
                    self.rowButtonCounter = 0 #resets counter for the start of a new row
            
            elif self.buttonCount == len(self.keyBoardLetters): #Resets the button count in the event all keys are drawn in a single row
                self.buttonCount = 0

            
def stringToText(string, X_pos, Y_pos, Game_Screen ):
    X_posList = []
    counter = 0
    spacing = 25
    X_posList.append(X_pos)
    for Letter in string:
        if Letter == " ":
            X_posList.append( X_posList[counter] + spacing )
            counter = counter + 1
            if counter > len(string):
                counter = 0
        else:
            Game_Screen.blit(pygame.transform.scale(pygame.image.load("assets/"+Letter.capitalize()+".png"), (textWidth[Letter.capitalize()] , 21)),(X_posList[counter] + textCentering[Letter.capitalize()],Y_pos))
            X_posList.append( X_posList[counter] + spacing - textCentering[Letter.capitalize()] )#+ textCentering[Letter.capitalize()])
            counter = counter + 1
            if counter > len(string):
                counter = 0

def wordLength(Word):
    Length = 0
    for Letter in Word:
        #check letter list and add letter together 
        Length = Length + textCentering[Letter.capitalize()]
        
    return Length


class Game:
    Tick_Rate = 60 #Change to set framerate
    
    
    def __init__ (self, title, width, height):
        self.title = title
        self.width = width
        self.height = height 
        self.Game_Screen = pygame.display.set_mode((width, height)) #Creates the window being displayed 
        self.Game_Screen.fill(LightGrey_Colour) #Sets the default colour of the displayed window 
        pygame.display.set_caption(title)

#GAME LOOP ----------------------------------------------------------------------------------------------------------------------------------------------------------------
    def run_game_loop (self):
        click = False
        Game_Over = False
        Round_Over = False
        GameMenu = True
        Game_On = False
        OnePlayerGame = False #sets game into a state where you play against the CPU
        TwoPlayerGame = False #sets game into a two player state where you play against another player 
        ChooseWord = False
        RandomWord = False
        KeyLetter = ""
        letterGuessed = ""
        turn = ""
        onScreenKeyBoard = "qwertyuiopasdfghjklzxcvbnm"
        Word = ""
        PlayerWin = False
        #ammount of turns to take with each difficulty setting
       
        Easy = 16
        Medium = 12
        Hard = 8
        Difficulty = Medium #Defaults to medium 


 
        title = GameObject("assets/Menu/Title.png", 650,100,896,110) 
        onePlayer = GameObject("assets/Menu/singlePlayer.png", 1225,400,233,34)
        twoPlayer = GameObject("assets/Menu/2Player.png", 1225,475,241,34)
        selectWord = GameObject("assets/Menu/selectWord.png", 1115,400,367,36)
        randomWord = GameObject("assets/Menu/randomWord.png", 1115,475,442,36)
        
        outline = GameObject("assets/Hangman.png", -300,-100,1131,1601)
        
        A = GameObject("assets/A.png", 100,100,26,21)
        B = GameObject("assets/B.png", 100,100,20,21)
        C = GameObject("assets/C.png", 100,100,22,21)
        D = GameObject("assets/D.png", 100,100,26,21)
        E = GameObject("assets/E.png", 100,100,17,21)
        F = GameObject("assets/F.png", 100,100,17,21)
        G = GameObject("assets/G.png", 100,100,24,22)
        H = GameObject("assets/H.png", 100,100,28,21)
        I = GameObject("assets/I.png", 100,100,13,21)
        J = GameObject("assets/J.png", 100,100,16,21)
        K = GameObject("assets/K.png", 100,100,25,21)
        L = GameObject("assets/L.png", 100,100,19,21)
        M = GameObject("assets/M.png", 100,100,33,21)
        N = GameObject("assets/N.png", 100,100,28,21)
        O = GameObject("assets/O.png", 100,100,25,21)
        P = GameObject("assets/P.png", 100,100,19,21)
        Q = GameObject("assets/Q.png", 100,100,27,21)
        R = GameObject("assets/R.png", 100,100,24,21)
        S = GameObject("assets/S.png", 100,100,14,21)
        T = GameObject("assets/T.png", 100,100,22,22)
        U = GameObject("assets/U.png", 100,100,25,21)
        V = GameObject("assets/V.png", 100,100,25,21)
        W = GameObject("assets/W.png", 100,100,34,21)
        X = GameObject("assets/X.png", 100,100,28,21)
        Y = GameObject("assets/Y.png", 100,100,25,21)
        Z = GameObject("assets/Z.png", 100,100,20,22)
        


        while Game_Over == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Game_Over = True
                keys = pygame.key.get_pressed()
                mousePos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    click = False


                if keys[pygame.K_ESCAPE] == True:
                    Game_Over = True 


#TODO - update include an update on the KeyLetter variable to the keyboard letter
                if keys[pygame.K_a] == True: #Checks for A Key - to be repeated for entire keyboard
                    KeyLetter = "A"
                elif keys[pygame.K_b] == True: #Checks for B Key - to be repeated for entire keyboard
                    KeyLetter = "B"
                elif keys[pygame.K_c] == True: #Checks for C Key - to be repeated for entire keyboard
                    KeyLetter = "C"
                elif keys[pygame.K_d] == True: #Checks for D Key - to be repeated for entire keyboard
                    KeyLetter = "D"
                elif keys[pygame.K_e] == True: #Checks for E Key - to be repeated for entire keyboard
                    KeyLetter = "E"
                elif keys[pygame.K_f] == True: #Checks for F Key - to be repeated for entire keyboard
                    KeyLetter = "F"
                elif keys[pygame.K_g] == True: #Checks for G Key - to be repeated for entire keyboard
                    KeyLetter = "G"
                elif keys[pygame.K_h] == True: #Checks for H Key - to be repeated for entire keyboard
                    KeyLetter = "H"
                elif keys[pygame.K_i] == True: #Checks for I Key - to be repeated for entire keyboard
                    KeyLetter = "I"
                elif keys[pygame.K_j] == True: #Checks for J Key - to be repeated for entire keyboard
                    KeyLetter = "J"
                elif keys[pygame.K_k] == True: #Checks for K Key - to be repeated for entire keyboard
                    KeyLetter = "K"
                elif keys[pygame.K_l] == True: #Checks for L Key - to be repeated for entire keyboard
                    KeyLetter = "L"
                elif keys[pygame.K_m] == True: #Checks for M Key - to be repeated for entire keyboard
                    KeyLetter = "M"
                elif keys[pygame.K_n] == True: #Checks for N Key - to be repeated for entire keyboard
                    KeyLetter = "N"
                elif keys[pygame.K_o] == True: #Checks for O Key - to be repeated for entire keyboard
                    KeyLetter = "O"
                elif keys[pygame.K_p] == True: #Checks for P Key - to be repeated for entire keyboard
                    KeyLetter = "P"
                elif keys[pygame.K_q] == True: #Checks for Q Key - to be repeated for entire keyboard
                    KeyLetter = "Q"
                elif keys[pygame.K_r] == True: #Checks for R Key - to be repeated for entire keyboard
                    KeyLetter = "R"
                elif keys[pygame.K_s] == True: #Checks for S Key - to be repeated for entire keyboard
                    KeyLetter = "S"
                elif keys[pygame.K_t] == True: #Checks for T Key - to be repeated for entire keyboard
                    KeyLetter = "T"
                elif keys[pygame.K_u] == True: #Checks for U Key - to be repeated for entire keyboard
                    KeyLetter = "U"
                elif keys[pygame.K_v] == True: #Checks for V Key - to be repeated for entire keyboard
                    KeyLetter = "V"
                elif keys[pygame.K_w] == True: #Checks for W Key - to be repeated for entire keyboard
                    KeyLetter = "W"
                elif keys[pygame.K_x] == True: #Checks for X Key - to be repeated for entire keyboard
                    KeyLetter = "X"
                elif keys[pygame.K_y] == True: #Checks for Y Key - to be repeated for entire keyboard
                    KeyLetter = "Y"
                elif keys[pygame.K_z] == True: #Checks for Z Key - to be repeated for entire keyboard
                    KeyLetter = "Z"
                else:
                    KeyLetter = ""

            #function used to check how many turns are left by comparing the letters guessed with the letter in the word being guessed 
            def guessCheck(Guesslist, Word):
                score = 0
                for Letter in GuessList:
                    if Letter.capitalize() not in list(Word.upper()):
                        score = score + 1
                        print(score) #TODO - work on method to blit hangman on screen
                return score
            
            def winCheck(Guesslist, Word):
                score = 0
                for Letter in Word:
                    if Letter.capitalize() in GuessList:
                        score = score + 1
                        print(score) #TODO - work on method to blit hangman on screen
                if score == len(Word):
                    print("True")
                    return True

            def guessRemaining(Number, Difficulty):
                DisplayX_pos = 100
                DisplayY_pos = 100
                totalLeft = Difficulty - Number
                if totalLeft == 16:
                    stringToText("Sixteen guesses remain", DisplayX_pos, DisplayY_pos, self.Game_Screen)
                elif totalLeft == 15:
                    stringToText("Fifteen guesses remain", DisplayX_pos, DisplayY_pos, self.Game_Screen)
                elif totalLeft == 14:
                    stringToText("Fourteen guesses remain", DisplayX_pos, DisplayY_pos, self.Game_Screen)
                elif totalLeft == 13:
                    stringToText("Thirteen guesses remain", DisplayX_pos, DisplayY_pos, self.Game_Screen)
                elif totalLeft == 12:
                    stringToText("Twelve guesses remain", DisplayX_pos, DisplayY_pos, self.Game_Screen)
                elif totalLeft == 11:
                    stringToText("Eleven guesses remain", DisplayX_pos, DisplayY_pos, self.Game_Screen)
                elif totalLeft == 10:
                    stringToText("Ten guesses remain", DisplayX_pos, DisplayY_pos, self.Game_Screen)
                elif totalLeft == 9:
                    stringToText("Nine guesses remain", DisplayX_pos, DisplayY_pos, self.Game_Screen)
                elif totalLeft == 8:
                    stringToText("Eight guesses remain", DisplayX_pos, DisplayY_pos, self.Game_Screen)
                elif totalLeft == 7:
                    stringToText("Seven guesses remain", DisplayX_pos, DisplayY_pos, self.Game_Screen)
                elif totalLeft == 6:
                    stringToText("Six guesses remain", DisplayX_pos, DisplayY_pos, self.Game_Screen)
                elif totalLeft == 5:
                    stringToText("Five guesses remain", DisplayX_pos, DisplayY_pos, self.Game_Screen)
                elif totalLeft == 4:
                    stringToText("Four guesses remain", DisplayX_pos, DisplayY_pos, self.Game_Screen)
                elif totalLeft == 3:
                    stringToText("Three guesses remain", DisplayX_pos, DisplayY_pos, self.Game_Screen)
                elif totalLeft == 2:
                    stringToText("Two guesses remain", DisplayX_pos, DisplayY_pos, self.Game_Screen)
                elif totalLeft == 1:
                    stringToText("One guess remains", DisplayX_pos, DisplayY_pos, self.Game_Screen)
                
                    
            def displayLetter( Letter ):
                if Letter.capitalize() == "A":
                    A.Draw(self.Game_Screen)
                elif Letter.capitalize() == "B":
                    B.Draw(self.Game_Screen)
                elif Letter.capitalize() == "C":
                    C.Draw(self.Game_Screen)
                elif Letter.capitalize() == "D":
                    D.Draw(self.Game_Screen)
                elif Letter.capitalize() == "E":
                    E.Draw(self.Game_Screen)
                elif Letter.capitalize() == "F":
                    F.Draw(self.Game_Screen)
                elif Letter.capitalize() == "G":
                    G.Draw(self.Game_Screen)
                elif Letter.capitalize() == "H":
                    H.Draw(self.Game_Screen)
                elif Letter.capitalize() == "I":
                    I.Draw(self.Game_Screen)
                elif Letter.capitalize() == "J":
                    J.Draw(self.Game_Screen)
                elif Letter.capitalize() == "K":
                    K.Draw(self.Game_Screen)
                elif Letter.capitalize() == "L":
                    L.Draw(self.Game_Screen)
                elif Letter.capitalize() == "M":
                    M.Draw(self.Game_Screen)
                elif Letter.capitalize() == "N":
                    N.Draw(self.Game_Screen)
                elif Letter.capitalize() == "O":
                    O.Draw(self.Game_Screen)
                elif Letter.capitalize() == "P":
                    P.Draw(self.Game_Screen)
                elif Letter.capitalize() == "Q":
                    Q.Draw(self.Game_Screen)
                elif Letter.capitalize() == "R":
                    R.Draw(self.Game_Screen)
                elif Letter.capitalize() == "S":
                    S.Draw(self.Game_Screen)
                elif Letter.capitalize() == "T":
                    T.Draw(self.Game_Screen)
                elif Letter.capitalize() == "U":
                    U.Draw(self.Game_Screen)
                elif Letter.capitalize() == "V":
                    V.Draw(self.Game_Screen)
                elif Letter.capitalize() == "W":
                    W.Draw(self.Game_Screen)
                elif Letter.capitalize() == "X":
                    X.Draw(self.Game_Screen)
                elif Letter.capitalize() == "Y":
                    Y.Draw(self.Game_Screen)
                elif Letter.capitalize() == "Z":
                    Z.Draw(self.Game_Screen)
                
            def changeLetterPos(Letter, newX_pos, newY_pos ):
                
                if Letter.capitalize() == "A":
                    A.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    A.Y_pos = newY_pos
                elif Letter.capitalize() == "B":
                    B.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    B.Y_pos = newY_pos
                elif Letter.capitalize() == "C":
                    C.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    C.Y_pos = newY_pos
                elif Letter.capitalize() == "D":
                    D.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    D.Y_pos = newY_pos
                elif Letter.capitalize() == "E":
                    E.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    E.Y_pos = newY_pos
                elif Letter.capitalize() == "F":
                    F.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    F.Y_pos = newY_pos
                elif Letter.capitalize() == "G":
                    G.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    G.Y_pos = newY_pos
                elif Letter.capitalize() == "H":
                    H.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    H.Y_pos = newY_pos
                elif Letter.capitalize() == "I":
                    I.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    I.Y_pos = newY_pos
                elif Letter.capitalize() == "J":
                    J.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    J.Y_pos = newY_pos
                elif Letter.capitalize() == "K":
                    K.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    K.Y_pos = newY_pos
                elif Letter.capitalize() == "L":
                    L.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    L.Y_pos = newY_pos
                elif Letter.capitalize() == "M":
                    M.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    M.Y_pos = newY_pos
                elif Letter.capitalize() == "N":
                    N.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    N.Y_pos = newY_pos
                elif Letter.capitalize() == "O":
                    O.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    O.Y_pos = newY_pos
                elif Letter.capitalize() == "P":
                    P.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    P.Y_pos = newY_pos
                elif Letter.capitalize() == "Q":
                    Q.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    Q.Y_pos = newY_pos
                elif Letter.capitalize() == "R":
                    R.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    R.Y_pos = newY_pos
                elif Letter.capitalize() == "S":
                    S.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    S.Y_pos = newY_pos
                elif Letter.capitalize() == "T":
                    T.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    T.Y_pos = newY_pos
                elif Letter.capitalize() == "U":
                    U.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    U.Y_pos = newY_pos
                elif Letter.capitalize() == "V":
                    V.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    V.Y_pos = newY_pos
                elif Letter.capitalize() == "W":
                    W.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    W.Y_pos = newY_pos
                elif Letter.capitalize() == "X":
                    X.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    X.Y_pos = newY_pos
                elif Letter.capitalize() == "Y":
                    Y.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    Y.Y_pos = newY_pos
                elif Letter.capitalize() == "Z":
                    Z.X_pos = newX_pos + textCentering[Letter.capitalize()]
                    Z.Y_pos = newY_pos


            #ToDo - possibly add option for AI difficulty to increase     
            if GameMenu == True and OnePlayerGame == False and TwoPlayerGame == False:
                self.Game_Screen.fill(LightGrey_Colour)
                outline.Draw(self.Game_Screen)
                title.Draw(self.Game_Screen)
                onePlayer.Draw(self.Game_Screen)
                twoPlayer.Draw(self.Game_Screen)
                stringToText("Choose your difficulty", 650, 400, self.Game_Screen)
                stringToText("Easy for sixteen turns", 650, 475, self.Game_Screen)
                stringToText("Medium for twelve turns", 650, 510, self.Game_Screen)
                stringToText("Hard for eight turns", 650, 540, self.Game_Screen)


                numSelect = random.randint(0,len(Word_List)) #selects a random int to correlate with a word in the word list 
                if event.type == pygame.MOUSEBUTTONDOWN and mousePos[0] >= onePlayer.X_pos and mousePos[1] >= onePlayer.Y_pos and mousePos[0] <= onePlayer.X_pos + 233 and mousePos[1] <=  onePlayer.Y_pos + 34:
                    print(mousePos)
                    print("You clicked on One Player Mode")
                    if click == True:
                        OnePlayerGame = True
                        click = False
                elif mousePos[0] >= twoPlayer.X_pos and mousePos[1] >= twoPlayer.Y_pos and mousePos[0] <= twoPlayer.X_pos + 241 and mousePos[1] <=  twoPlayer.Y_pos + 34:
                    print(mousePos)
                    print("You clicked on Two Player Mode")
                    if click == True:
                        OnePlayerGame = True
                        click = False
                

            

            elif GameMenu == True and RandomWord == False and ChooseWord == False :
                self.Game_Screen.fill(LightGrey_Colour)
                outline.Draw(self.Game_Screen)
                title.Draw(self.Game_Screen)
                selectWord.Draw(self.Game_Screen)
                randomWord.Draw(self.Game_Screen)
                if mousePos[0] >= selectWord.X_pos and mousePos[1] >= selectWord.Y_pos and mousePos[0] <= selectWord.X_pos + 367 and mousePos[1] <=  selectWord.Y_pos + 36:
                    if click == True:
                        ChooseWord = True
                        click = False
                elif mousePos[0] >= randomWord.X_pos and mousePos[1] >= randomWord.Y_pos and mousePos[0] <= randomWord.X_pos + 442 and mousePos[1] <=  randomWord.Y_pos + 36:
                    if click == True:
                        RandomWord = True
                        click = False
                        print (RandomWord)
                        

                #add if statement for if ChooseWord == True
                #if ChooseWord == True, display a list of words

            elif GameMenu == True and RandomWord == True or ChooseWord == True :
                self.Game_Screen.fill(LightGrey_Colour)
                
#Main GameLoop ----------------------------------------------------------------------------------------------------------------------------------------------
                if GameMenu == True and Game_On == True and Round_Over == False:
#TODO - add a function to wipe the guesslist at the start if a new round                   

                    X_posList = []
                    Counter = 0
                    ### CONTINUE HERE!!!!!!!!!!!!!!!!!! 
                    #TODO - create a funciton to check if all the letters have been guessed and increase score by 1                       
                    keyboard = keyselection(onScreenKeyBoard, GuessList, self.Game_Screen, 450, mousePos[0], mousePos[1], click, KeyLetter)
                    
                    guessRemaining(guessCheck(GuessList , Word), Difficulty)
                    if guessCheck(GuessList , Word) >= Difficulty:
                        Round_Over = True
                    elif winCheck(GuessList, Word) == True:
                        PlayerWin = True
                        Round_Over = True    
                    wordCenter = len(Word) *33
                    for Letter in Word:
                        Letter = Letter
                        Y_pos = 400 #Yposition of where the word will be displayed
                        X_pos = 800 - wordCenter /2
                        if Counter >= 1:
                            X_posList.append(X_posList[Counter - 1] + 33)
                            changeLetterPos(Letter, X_posList[Counter], Y_pos )
                            if Letter.capitalize() in GuessList:
                                displayLetter(Letter)
                            pygame.draw.rect(self.Game_Screen, (123,101,21), [X_posList[Counter],Y_pos + 25,27,4]) #sets surface, colour and X-pos,Y-pos+size for the rectangle to be drawn
                            Counter = Counter + 1
                            if Counter == len(Word):
                                Counter = 0
                                
                        elif Counter == 0:
                            X_posList.append(X_pos) # set starting postion of first letter 
                            changeLetterPos(Letter ,X_posList[Counter], Y_pos)
                            if Letter.capitalize() in GuessList:
                                displayLetter(Letter)
                            pygame.draw.rect(self.Game_Screen, (123,101,21), [X_posList[Counter],Y_pos + 25,27,4]) #sets surface, colour and X-pos,Y-pos+size for the rectangle to be drawn
                            Counter = Counter + 1
                
                #display when the round is over and max number of tries have been reached 
                elif GameMenu == True and Round_Over == True: 
                    self.Game_Screen.fill(LightGrey_Colour)
                    outline.Draw(self.Game_Screen)
                    stringToText("Round Over", 750, 500, self.Game_Screen )
                    if PlayerWin == True:
                        stringToText("You Win", 750, 550, self.Game_Screen )
                    elif PlayerWin == False:
                        stringToText("You Lose", 750, 550, self.Game_Screen )

                    #display if player won or lost 
                    #display current scoreboared
                
                elif ChooseWord == True:
                    
                    startingX_pos = 800
                    startingY_pos = -40
                    textHeight = 21
                    Counter = 0
                    startingRange = 1
                    endingRange = 23
                    scrollSpeed = 40
                    spaceBetweenWords = 40
                    
                    #create list with the list positions for words
                    #SelectionY_pos list moved to outside of gameloop, or else text won't move

                    for i in range(startingRange,endingRange):
                        if len(selectionRangeList) < endingRange - 1:
                            SelectionY_pos.append(startingY_pos)
                            selectionRangeList.append(Counter)
                        Counter = Counter + 1
                        startingY_pos = startingY_pos + spaceBetweenWords
                        wordWidth = 0
                       
                        wordSpace = len(Word_List[selectionRangeList[i-1]]) * 25 - wordLength(Word_List[selectionRangeList[i-1]]) #Calculated the spaced taken up by the word on screen for centering 
                        
                        #Prints and displayed the word with a highlight when the mouse is over it 
                        if mousePos[0] >= startingX_pos and mousePos[0] <= startingX_pos + len(Word_List[selectionRangeList[i-1]]) * 25 and mousePos[1] >= SelectionY_pos[i-1] and mousePos[1] <= SelectionY_pos[i-1] + textHeight:
                            stringToText(Word_List[selectionRangeList[i-1]], startingX_pos - wordSpace /2 , SelectionY_pos[i-1], self.Game_Screen)
                            pygame.draw.rect(self.Game_Screen, (255,0,0), [startingX_pos - wordSpace /2 ,SelectionY_pos[i-1],len(Word_List[selectionRangeList[i-1]]) * 25 - wordLength(Word_List[selectionRangeList[i-1]]) ,textHeight])
                            if click == True:
                                Word = Word_List[selectionRangeList[i-1]]
                                Game_On = True  
                        #Prints test when the mouse isn't hovering over it 
                        else: 
                            stringToText(Word_List[selectionRangeList[i-1]], startingX_pos - wordSpace /2, SelectionY_pos[i-1], self.Game_Screen)

                        if keys[pygame.K_DOWN] == True:
                            #use list of numbers to blit a different word onto the screan, and increase those numbers as the screen scrolls down 
                            SelectionY_pos[i-1] = SelectionY_pos[i-1] + scrollSpeed
                            if SelectionY_pos[i-1] >= Screen_Height + spaceBetweenWords :
                                selectionRangeList[i-1] = selectionRangeList[i-1] - endingRange 
                                print(selectionRangeList)
                                SelectionY_pos[i-1] = 0 - spaceBetweenWords

                        elif keys[pygame.K_UP] == True: #continue Here - add a selection to increment the list 
                            SelectionY_pos[i-1] = SelectionY_pos[i-1] - scrollSpeed
                            if SelectionY_pos[i-1] < 0 - spaceBetweenWords :
                                selectionRangeList[i-1] = selectionRangeList[i-1] + endingRange 
                                print(selectionRangeList)
                                SelectionY_pos[i-1] = Screen_Height
                                
                        else:    
                            SelectionY_pos[i-1] = SelectionY_pos[i-1]
                            #stringToText(Word_List[i-1], startingX_pos, SelectionY_pos[i-1], self.Game_Screen)
                        
                elif RandomWord == True:
                    Word = Word_List[numSelect]
                    Game_On = True

                        
                        

                        
                
                       



               
                #add if statement for if ChooseWord == True
                #if ChooseWord == True, display a list of words, ask other player to look away 



            pygame.display.update() #Updates the current frame after completing the loop
            Clock.tick(self.Tick_Rate) #Sets the frame rate per second

pygame.init()

new_game = Game(Screen_Title,Screen_Width,Screen_Height) #creates a new game part of the "game class"

new_game.run_game_loop() #Starts the game loop as defined in the class to continue looping until the game over state becomes true 

pygame.quit()
quit()