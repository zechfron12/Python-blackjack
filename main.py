from tkinter import *
import random
from time import sleep
from PIL import Image,ImageTk #For image resize


#Game Logic
colors = ['clubs', 'diamonds', 'hearts', 'spades']
names = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
cardsValue = {'ace': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'jack': 10, 'queen': 10, 'king': 10}

#Each position has 2 values [name, color]
playerCards = []
dealerCards = []
myDeck = []

playerScore = 0
dealerScore = 0

def create_a_deck():
  deck = []
  for v in names: #distribute cards
    for c in colors:
      deck.append((v,c))

  random.shuffle(deck)
  return deck

myDeck = create_a_deck()

def calculate_score(cards):
  score = 0
  for card in cards: 
    if (card[0] == 'ace' and score > 10):
      score += 1
    else:
      score += cardsValue.get(card[0])

  return score

def hit(cards, entity):
  global playerScore, dealerScore, playerCards, dealerCards
  global myDeck
  global hitButton, standButton

  randomPosition = random.randint(0, len(myDeck) - 1)
  cards.append(myDeck[randomPosition])
  myDeck.pop(randomPosition)

  score =  calculate_score(cards)

  if entity == "PLAYER":
    playerScore = score
    print("PLAYER CARDS: ", playerCards)
    print("SCORE: ", playerScore)
  else: 
    dealerScore = score
    print("DEALER CARDS: ", dealerCards)
    print("SCORE: ", dealerScore)

  draw_canvas()

  #First player to hit above 21 loses
  if playerScore > 21:
    canvas.create_text(60, 575,text='You Lost!',fill='red',font='Times 18')
    hitButton['state'] = DISABLED
    standButton['state'] = DISABLED

  if dealerScore > 21:
    canvas.create_text(60, 575,text='You Win!',fill='green',font='Times 18')
    hitButton['state'] = DISABLED
    standButton['state'] = DISABLED



def stand():
  global playerScore, dealerScore, playerCards, dealerCards, window
  global myDeck
  global hitButton, standButton

  while dealerScore <= playerScore:
    hit(dealerCards, "DEALER")
    sleep(1)

  if dealerScore < 22:
    canvas.create_text(60, 575,text='You Lost!',fill='red',font='Times 18')
    hitButton['state'] = DISABLED

  standButton['state'] = DISABLED

def draw_canvas():
  global canvas, playerCards, dealerCards, bgImage, bg, dealerScore, playerScore

  cardStartPos = 100 # X value for card iamges

  for card in playerCards:
   fileName = "cards/{}_of_{}.png".format(card[0], card[1])

   cardImage = Image.open(fileName).resize((130, 180))
   bgImage.paste(cardImage, (cardStartPos,360))
   cardStartPos+=20 # Move nex image to right

  cardStartPos = 100

  for card in dealerCards:
   fileName = "cards/{}_of_{}.png".format(card[0], card[1])

   cardImage = Image.open(fileName).resize((130, 180))

   bgImage.paste(cardImage, (cardStartPos,60))
   cardStartPos+=20

  bg = ImageTk.PhotoImage(bgImage)

  canvas.delete(ALL)

  canvas.create_image( 0, 0, image = bg, anchor = "nw")
  canvas.create_text(60,30,text="Dealer:",fill='white',font='Times 18')
  canvas.create_text(60, 330,text='Player:',fill='white',font='Times 18')

  canvas.create_text(120, 30, text=str(dealerScore), fill='white', font='Times 18')
  canvas.create_text(120, 330,text=str(playerScore), fill='white', font='Times 18')
  canvas.update()


def init():
  global playerScore, dealerScore, playerCards, dealerCards, playerScoreTk, dealerScoreTk
  global hitButton, standButton, bg, bgImage
  global myDeck
  global canvas

  hitButton['state'] = NORMAL
  standButton['state'] = NORMAL

  playerScore = 0
  dealerScore = 0

  playerCards.clear()
  dealerCards.clear()

  myDeck = create_a_deck()

  bgImage = Image.open("table_bg.png").resize((600,600))
  bg = ImageTk.PhotoImage(bgImage) 

  #Extract and delete cards from deck
  #First and second card goes to PLAYER
  randomPosition = random.randint(0, len(myDeck) - 1)
  playerCards.append(myDeck[randomPosition])
  myDeck.pop(randomPosition)

  randomPosition = random.randint(0, len(myDeck) - 1)
  playerCards.append(myDeck[randomPosition])
  myDeck.pop(randomPosition)

  #Third card goes to DEALER
  randomPosition = random.randint(0, len(myDeck) - 1)
  dealerCards.append(myDeck[randomPosition])
  myDeck.pop(randomPosition)

  playerScore = calculate_score(playerCards)
  dealerScore = calculate_score(dealerCards)

  print("PLAYER CARDS: ", playerCards)
  print("SCORE: ", playerScore)
  print("DEALER CARDS: ", dealerCards)
  print("SCORE: ", dealerScore)

  draw_canvas()




#User interface
window = Tk()
window.title("Blackjack")

bgImage = Image.open("table_bg.png").resize((600,600)) #inserting background image
bg = ImageTk.PhotoImage(bgImage) #make it work with Tk


canvas = Canvas(window, height = 600, width = 600) #Canvas for displaying cards and the score
canvas.create_image( 0, 0, image = bg, anchor = "nw") #including backgroun image
canvas.pack(fill="both", expand=True) #insert canvas in the main window


#Implement buttons
startButton = Button(window,text='START', command=init,
    bg='#45b592',
    fg='#ffffff',
    bd=1,
    height=2,
    width=28)
startButton.pack(side=LEFT)

hitButton = Button(window,text='HIT', command=lambda: hit(playerCards, "PLAYER"), #using lambda for parsing arguments
    bg='#45b592',
    fg='#ffffff',
    bd=1,
    height=2,
    width=28)
hitButton.pack(side=LEFT)

standButton = Button(window,text='STAND', command=stand,
    bg='#45b592',
    fg='#ffffff',
    bd=1,
    height=2,
    width=28)
standButton.pack(side=LEFT)

window.mainloop()
