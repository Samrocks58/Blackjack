import pygame, random, time, os
from tkinter import messagebox as mb, Tk

pygame.init()
pygame.display.init()

Red=(255, 0, 0)
width=int(1200)
height=int(675)
HitButton=pygame.image.load(r"Hit Button.png")
StandButton=pygame.image.load(r"Stand Button.png")
SplitButton=pygame.image.load(r"splitButton.png")
Button_width=HitButton.get_width()
Button_height=HitButton.get_height()

cardPics={}
OpponentCardPics={}
suites = ["H", "D", "S", "C"]
values = [i for i in "234567890JQKA"]
card_width=int(113*2)
card_height=int(157*2)
opponent_Card_Width=175
opponent_Card_Height=244
max_width=1200-card_width
max_height=675-card_height

for suite in suites:
    for value in values:
        cardname=value+suite
        cardDirect=r'C:\Users\smprc\AppData\Local\Programs\Microsoft VS Code\coding files\CardPics\ '
        cardDirect = cardDirect[:-1]
        cardDirect += cardname
        cardDirect += ".png"
        cardPics[cardname] = pygame.image.load(cardDirect)
        cardPics[cardname] = pygame.transform.scale(cardPics[cardname], (card_width, card_height))
        OpponentCardPics[cardname] = pygame.transform.scale(cardPics[cardname], (opponent_Card_Width, opponent_Card_Height))
# print(f"width: {cardPics[cardname].get_width()} height: {cardPics[cardname].get_height()}")


poker_green=(0, 128, 43)
Black=(255, 255, 255)
screen = pygame.display.set_mode((width, height))
screen.fill(poker_green)
GlobMoving=False
GlobSplitting=False
sameCard=False
hasSplit=False

def create_deck():
    func_list=[]
    for suit in suites:
        for v in values:
            func_list.append(v+suit)
    return func_list

class deck:
    def __init__(self):
        self.cards=create_deck()
        self.end_pos=[7, 14]
        self.image=pygame.image.load(r"C:\Users\smprc\Downloads\Desktop Folder\New Face Down Card.jpg")
        self.image=pygame.transform.scale(self.image, (226, 314))
        self.center=[self.end_pos[0]+(card_width//2), self.end_pos[1]+(card_height//2)]
        self.Rect=self.image.get_rect(center=(self.center))
    def move_card(self, cardObject):
        global GlobMoving
        ending_positionX, ending_positionY=cardObject.end_pos
        differenceX=(ending_positionX-self.end_pos[0])//70
        differenceY=(ending_positionY-self.end_pos[1])//70
        cardObject.MoveX=differenceX
        cardObject.MoveY=differenceY
        cardObject.moving=True
        GlobMoving=True
    def split_card(self, cardObject):
        global GlobSplitting
        differenceX=cardObject.end_pos[0]//70
        cardObject.MoveX=differenceX
        cardObject.moving=True
        cardObject.active_pos=cardObject.end_pos
        GlobSplitting=True
    def Restart(self):
        self.cards=create_deck()

def calculate_score(list):
    Ace=False
    NumAce=0
    total_score=0
    for i in list:
        Value=list[i].card[0]
        if Value in "23456789":
            total_score += int(Value)
        elif Value in "0JQK":
            total_score += 10
        elif Value == "A":
            Ace=True
            NumAce += 1
            total_score += 11
    if Ace:
        for i in range(NumAce):
            if total_score > 21:
                total_score -= 10
    return total_score

class Hand():
    def __init__(self):
        self.hand={}
        self.Value = self.score()
    def score(self):
        return calculate_score(self.hand)
    def addCard(self, Card):
        self.hand[Card.id] = Card
        self.Value = self.score()
    def removeCard(self, Card):
        del self.hand[Card.id]
        self.Value = self.score()

Deck=deck()
OpponentCards={}
Hand1=Hand()
Hand2=Hand()
ChosenHand = Hand1
playedHands=0

class Card(pygame.Rect):
    def __init__(self, id, startingcard):
        global Deck
        randCardInt=random.randint(0, len(Deck.cards)-1)
        new_card = Deck.cards[randCardInt]
        Deck.cards.remove(new_card)
        self.card=new_card
        # if id > 2:
        #     self.card=new_card
        # if id == 1:
        #     self.card = "0H"
        # if id == 2:
        #     self.card = "0S"
        self.starting=startingcard
        self.MoveX=0
        self.MoveY=0
        self.moving=False
        self.showed=True
        self.image=cardPics[self.card]
        self.id=id
        self.active_pos=[7, 14]
        self.end_pos=self.get_pos(self.id)
        ChosenHand.addCard(self)
    def get_pos(self, ID):
        spacing=14
        if ID == 1:
            return [max_width, max_height]
        else:
            total_spacing=card_width+spacing
            return [max_width-total_spacing*(ID-1), max_height]

class OpponentCard():
    def __init__(self, id, start):
        randCard=random.randint(0, len(Deck.cards)-1)
        new_card = Deck.cards[randCard]
        Deck.cards.remove(new_card)
        self.card=new_card
        self.starting=start
        self.MoveX=0
        self.MoveY=0
        self.image=OpponentCardPics[self.card]
        self.face_down_image=pygame.transform.scale(Deck.image, (self.image.get_width(), self.image.get_height()))
        self.moving=False
        if id == 1:
            self.showed = False
        else:
            self.showed=True
        OpponentCards[new_card] = self
        self.id=id
        self.active_pos=[7, 14]
        self.end_pos=self.get_position()
    def get_position(self):
        OpponentMaxWidth=1200-opponent_Card_Width
        spacing=3
        if self.id == 1:
            return [OpponentMaxWidth, 14]
        else:
            total_spacing=opponent_Card_Width+spacing
            return [OpponentMaxWidth-total_spacing*(self.id-1), 14]

msg1=""
msg2=""

def Restart():
    global gameover, GlobMoving, gameoverCounter, OpponentCards, round, cardpos, old_round, Standed, msg1, msg2, ended, Deck, sameCard, hasSplit, Hand1, Hand2, ChosenHand, playedHands
    del OpponentCards
    OpponentCards={}
    cardpos=(0, 0)
    gameover=False
    GlobMoving=False
    gameoverCounter=0
    Hand1=Hand()
    Hand2=Hand()
    ChosenHand=Hand1
    playedHands=0
    round=0
    old_round=0
    Standed=False
    ended=False
    sameCard=False
    hasSplit=False
    msg1=""
    msg2=""
    gameloop()

def check_score(score):
    if score > 21:
        return True
        
def Game_Over():
    global ChosenHand, gameover, Standed, playedHands
    root=Tk()
    root.wm_withdraw()
    if not hasSplit:
        MsgBox=mb.askyesno("You Busted!!!", "Do you want to play again?")
        if MsgBox:
            root.destroy()
            Restart()
        elif not MsgBox:
            root.destroy()
            quit()
    else:
        if ChosenHand == Hand1:
            MsgBox = mb.showinfo("You Busted On Your First Hand!! Time To Go To The Second!!")
            playedHands += 1
        else:
            MsgBox = mb.showinfo("You Busted On Your Second Hand!!")
            playedHands += 1
            Standed = True
        root.destroy()
        gameover=False
        ChosenHand = Hand2


def Opponent_Show():
    global OpponentCards
    for card in OpponentCards:
        if OpponentCards[card].id == 1:
            OpponentCards[card].showed = True
    
def Opponent_Hit():
    global OpponentCards, Deck
    if len(Deck.cards) <= 3:
        Deck.Restart()
    new_id=len(OpponentCards) + 1
    OpponentCard(new_id, True)

def hit_or_miss():
    global OpponentCards, msg1, msg2
    draw_card=False
    OpponentScore=calculate_score(OpponentCards)
    CardScore=calculate_score(ChosenHand.hand)
    if check_score(CardScore):
        Game_Over()
    if len(list(ChosenHand.hand.values())) == 5:
        msg1="You Won!!!"
        msg2="You Won!!! You drew five cards!! Do you want to play again?"
    if OpponentScore >= 17:
        Opponent_Show()
        if OpponentScore > CardScore:
            msg1="You Lost!!!"
            msg2="You Lost!!! Do you want to play again?"
        if CardScore > OpponentScore:
            msg1="You Won!!!"
            msg2="You Won!!! Do you want to play again?"
        if CardScore == OpponentScore:
            msg1="Push!!!"
            msg2="You Tied With The Computer!!! Do you want to play again?"
    if OpponentScore > 21:
        msg1="The Dealer Busted!!!"
        msg2="You Won!!! Do you want to play again?"
    if OpponentScore <= 16:
        if len(OpponentCards) == 5:
            msg1="You Lost!!!"
            msg2="The computer managed to draw five cards!!! Do you want to play again?"
        if len(OpponentCards) < 5:
            Opponent_Hit()
            draw_card=True
    if CardScore == 21:
        if OpponentScore == 21:
            msg1="Blackjack Push!!!"
            msg2="You both got Blackjack!!! Do you want to play again?"
        else:
            msg1="Blackjack!!!"
            msg2="You Won!!! Do you want to play again?"
    if OpponentScore == 21:
        if CardScore == 21:
            msg1="Blackjack Push!!!"
            msg2="You both got Blackjack!!! Do you want to play again?"
        else:
            msg1="Dealer Blackjack!!!"
            msg2="You Lost!!! Do you want to play again?"
    return draw_card

def end_popup(message1, message2):
    root=Tk()
    root.wm_withdraw()
    MsgBox=mb.askyesno(message1, message2)
    if MsgBox:
        root.destroy()
        Restart()
    elif not MsgBox:
        root.destroy()
        quit()

def create_card():
    global Deck
    if len(Deck.cards) <= 4:
        Deck.Restart()
        Deck.cards=create_deck()
        create_card()
        return True
    cardNum=len(ChosenHand.hand)
    if cardNum < 5:
        if ChosenHand == Hand1:
            Nextid=ChosenHand.hand[list(ChosenHand.hand.keys())[-1]].id + 1
        elif ChosenHand == Hand2:
            Nextid=ChosenHand.hand[list(ChosenHand.hand.keys())[-1]].id - 1
        Card(Nextid, False)
        Deck.move_card(ChosenHand.hand[list(ChosenHand.hand.keys())[-1]])
    elif cardNum == 5:
        root=Tk()
        root.wm_withdraw()
        MsgBox=mb.askyesno("You Won!!!", "You Won!!! You drew five cards!! Do you want to play again?")
        if MsgBox:
            root.destroy()
            Restart()
        elif not MsgBox:
            root.destroy()
            quit()

# start_time=time.perf_counter()
# FPSlist=[]

cardpos=(0, 0)
OpponentCardPos=(0, 0)
gameover=False
gameoverCounter=0
HitButtonRect=HitButton.get_rect(center=(Deck.Rect.right+5+Button_width//2, Deck.Rect.top+Button_height//2))
StandButtonRect=StandButton.get_rect(center=(Deck.Rect.right+5+Button_width//2, Deck.Rect.top+75+Button_height//2))
SplitButtonRect=SplitButton.get_rect(center=(Deck.Rect.right+5+Button_width//2, Deck.Rect.top+150+Button_height//2))
round=0
Standed=False
ended=False

def find_average(list):
    sum=0
    for i in list:
        if i < 750:
            sum += i
    return sum//len(list)

def gameloop():
    global gameover, GlobMoving, gameoverCounter, HitButton, StandButton, OpponentCards, round, Card, OpponentCard, Standed, old_round, msg1, msg2, ended, GlobSplitting, sameCard, hasSplit, ChosenHand, Hand2, Hand1, playedHands
    while True:
        # end_time=time.perf_counter()
        # FPSlist.append(int((end_time-start_time)**-1))
        # os.system('cls')
        # print(f"Average FPS: {find_average(FPSlist)}")
        # start_time=time.perf_counter()
        if round == 50:
            Card(1, True)
        elif round == 100:
            OpponentCard(1, True)
        elif round == 150:
            Card(2, True)
        elif round == 200:
            OpponentCard(2, True)
            if ChosenHand.hand[list(ChosenHand.hand.keys())[0]].card[0] == ChosenHand.hand[list(ChosenHand.hand.keys())[1]].card[0]:
                sameCard=True
        if round <= 200:
            round += 1

        pygame.display.flip()
        screen.fill(poker_green)
        screen.blit(Deck.image, Deck.end_pos)        
        screen.blit(HitButton, (Deck.Rect.right+5, Deck.Rect.top))
        screen.blit(StandButton, (Deck.Rect.right+5, Deck.Rect.top+75))
        if sameCard and not hasSplit and len(ChosenHand.hand) == 2:
            screen.blit(SplitButton, (Deck.Rect.right+5, Deck.Rect.top+150))

        if Standed:
            if (not hasSplit) or (ChosenHand == Hand2) or (playedHands == 2):
                # if gameoverCounter >= 2:
                maxValue = max(Hand1.Value, Hand2.Value)
                if Hand1.Value == maxValue and Hand1.Value <= 21:
                    ChosenHand=Hand1
                elif Hand2.Value > 21 and Hand1.Value <= 21:
                    ChosenHand=Hand1
                Opponent_Show()
                interval=75
                if round == old_round + interval:
                    HitBool=hit_or_miss()
                    if not HitBool:
                        Opponent_Show()
                        OpponentCards[list(OpponentCards.keys())[0]].showed = True
                    old_round=round
                    if calculate_score(OpponentCards) >= 17:
                        ended=True
                if round <= 201+interval*4:
                    round += 1
            else:
                ChosenHand = Hand2
                Standed=False
                playedHands += 1
        for i in OpponentCards:
            if not OpponentCards[i].starting:
                OpponentCardPos=OpponentCards[i].active_pos
            elif OpponentCards[i].starting:
                OpponentCardPos=OpponentCards[i].end_pos
            if OpponentCards[i].showed:
                screen.blit(OpponentCards[i].image, OpponentCardPos)
            elif OpponentCards[i].showed == False:
                screen.blit(OpponentCards[i].face_down_image, OpponentCardPos)

        for card in list(list(ChosenHand.hand.values())):
            if not card.starting:
                cardpos=card.active_pos
            elif card.starting:
                if not GlobSplitting:
                    cardpos=card.end_pos
                elif GlobSplitting:
                    if card.id == 2:
                        cardpos=card.active_pos
                    else:
                        cardpos=card.end_pos
            if card.showed:
                screen.blit(card.image, cardpos)

        if ended:
            Opponent_Show()
            if not HitBool:
                end_popup(msg1, msg2)
        if gameover:
            gameoverCounter += 1
            if gameoverCounter % 2 == 0:
                Game_Over()
        if GlobMoving:
            for card in ChosenHand.hand.values():
                if card.moving:
                    if card.active_pos[0] >= card.end_pos[0]:
                        card.active_pos=card.end_pos
                        GlobMoving=False
                        card.moving=False
                        gameover = check_score(calculate_score(ChosenHand.hand))
                    if card.active_pos[1] >= card.end_pos[1]:
                        card.active_pos=card.end_pos
                        GlobMoving=False
                        card.moving=False
                        gameover = check_score(calculate_score(ChosenHand.hand))
                    else:
                        card.active_pos[0] += card.MoveX
                        card.active_pos[1] += card.MoveY
        if GlobSplitting:
            for card in list(ChosenHand.hand.values()):
                if card.moving:
                    if card.active_pos[0] <= 14:
                        card.active_pos[0] = 14
                        card.end_pos[0] = 14
                        GlobSplitting=False
                        card.moving=False
                        time.sleep(0.2)
                        Hand1.removeCard(card)
                        card.id=5
                        Hand2.addCard(card)
                        break
                    else:
                        card.active_pos[0] -= card.MoveX
        for event in pygame.event.get():
            if not GlobMoving:
                if round > 200:
                    if not Standed:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mousepos=pygame.mouse.get_pos()
                            if HitButtonRect.collidepoint(mousepos):
                                create_card()
                            if StandButtonRect.collidepoint(mousepos):
                                Standed=True
                                old_round=round
                            if SplitButtonRect.collidepoint(mousepos):
                                if not hasSplit:
                                    Deck.split_card(ChosenHand.hand[list(ChosenHand.hand.keys())[1]])
                                    hasSplit=True
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_q:
                    quit()
                if event.key == pygame.K_r:
                    Restart()
                if event.key == pygame.K_i:
                    print(f"Hand 1: {len(Hand1.hand)}\nHand2: {len(Hand2.hand)}")
            if event.type == pygame.QUIT:
                quit()
gameloop()