import pygame
import json
from random import randint, randrange
pygame.init()

# load font
font20 = pygame.font.Font('Nunito-Regular.ttf', 24)
def displayText(text, x, y, colour, size):
    fontObj = pygame.font.Font('Nunito-Regular.ttf', size)
    textObj = fontObj.render(text, True, colour)
    textRect = textObj.get_rect()
    textRect.center = (x, y)
    screen.blit(textObj, textRect)
# colour tuples
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
PURPLE = (80, 1, 199)

# Initialise screen
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
# frame rate
clock = pygame.time.Clock()
FPS = 60

# Player class
class Player:
  # Take the initial position,
  # dimensions, speed and color of the object
  def __init__(self, posx, posy, width, height, speed, colour):
    self.posx = posx
    self.posy = posy
    self.width = width
    self.height = height
    self.speed = speed
    self.colour = colour
    # Rect that is used to control the
    # position and collision of the object
    self.objectRect = pygame.Rect(posx, posy, width, height)
    # Object that is blit on the screen
    self.object = pygame.draw.rect(screen, self.colour, self.objectRect)

  # Used to display the object on the screen
  def display(self):
    self.object = pygame.draw.rect(screen, self.colour, self.objectRect)

  # Used to update the state of the object
  # yFac represents the direction of the striker movement
  # if yFac == -1 ==> The object is moving upwards
  # if yFac == 1 ==> The object is moving downwards
  # if yFac == 0 ==> The object is not moving
  def update(self, yFac):
    self.posy = self.posy + self.speed * yFac

    # Restricting the striker to be below
    # the top surface of the screen
    if self.posy <= 0:
      self.posy = 0
    # Restricting the striker to be above
    # the bottom surface of the screen

    elif self.posy + self.height >= HEIGHT:
      self.posy = HEIGHT - self.height

    # Updating the rect with the new values
    self.objectRect = (self.posx, self.posy, self.width, self.height)

  # Used to render the score on to the screen
  # First, create a text object using the font.render() method
  # Then, get the rect of that text using the get_rect() method
  # Finally blit the text on to the screen
  def displayScore(self, text, score, x, y, colour):
    text = font20.render(text + str(score), True, colour)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)

  def getRect(self):
    return self.objectRect

# Ball object
class Ball:

  def __init__(self, posx, posy, radius, speed, colour):
    self.posx = posx
    self.posy = posy
    self.radius = radius
    self.speed = speed
    self.colour = colour
    self.xFac = 1
    self.yFac = -1
    # setup circle
    self.ball = pygame.draw.circle(screen, self.colour, (self.posx, self.posy), self.radius)
    self.firstTime = 1
  def display(self):
    
    self.ball = pygame.draw.circle(screen, self.colour, (self.posx, self.posy), self.radius)
  def update(self):
    self.posx += self.speed * self.xFac
    self.posy += self.speed * self.yFac

    # Check if the ball is at the top or bottom of the window
    # Invert the yFac to reflect the ball
    if self.posy <= 0 or self.posy >= HEIGHT:
      self.colour = (randint(30,255),randint(30,255),randint(30,255))
      self.yFac *= -1
      if self.speed < 10:
        self.speed = self.speed * 1.1
    # If the ball touches the left wall for the first time, we know that that player 2 has scored.
    # Set firstTime to 0 returning 1, firstTime is set so that the condition is only ever met once
    # 'debouncing' the scoring
    if self.posx <= 0 and self.firstTime:
      self.colour = (randint(30,255),randint(30,255),randint(30,255))
      self.firstTime = 0
      if self.speed < 10:
        self.speed = self.speed * 1.1
      return 1
    elif self.posx >= WIDTH and self.firstTime:
      self.colour = (randint(30,255),randint(30,255),randint(30,255))
      self.firstTime = 0
      if self.speed < 10:
        self.speed = self.speed * 1.1
      return -1
    
    else:
      return 0
    
  # Resets the ball position to the centre
  def reset(self):
    if self.speed >= 4: 
      self.speed -= 1
    self.posx = WIDTH // 2
    self.posy = HEIGHT // 2
    self.xFac = (-1)
    print(self.xFac)
    self.firstTime = 1
  # Reflects ball on the x axis
  def hit(self):
    self.xFac *= -1
  def getRect(self):
    return self.ball

# Game Manage
def main():
  # State flags
  menu = True
  running = False
  #gameover = False


  # Create players
  playerWidth = 15
  playerHeight = 150
  player1 = Player(30, 0, playerWidth, playerHeight, 10, GREEN)
  player2 = Player(WIDTH-40, 0, playerWidth, playerHeight, 10, RED)
  ball = Ball(WIDTH//2, HEIGHT//2, radius=7, speed=4, colour=WHITE)
  listOfPlayers = [player1, player2]
  player1Score, player2Score = 0,0
  player1YFac, player2YFac = 0, 0 

  #display menu
  while menu:
    screen.fill(PURPLE)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        menu = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          running = True
          menu = False
    displayText("pong", WIDTH//2, HEIGHT//2 - 100, WHITE, 96)
    displayText("Press space to start", WIDTH//2, HEIGHT//2 + 10, WHITE, 20)
    displayText("Player one uses W & S", WIDTH//2, HEIGHT//2 + 30, WHITE, 20)
    displayText("Player two uses up & down", WIDTH//2, HEIGHT//2 + 50, WHITE, 20)
    # Load in highscores and display them
    with open("highscore.json", 'rb') as filehandle:
      highscoreJSONObject = json.loads(filehandle.read())
      p1highscore = highscoreJSONObject["player1"]
      p2highscore = highscoreJSONObject["player2"]
    displayText(f"Player one high score: {p1highscore}", WIDTH//2, HEIGHT//2 + 90, WHITE, 20)
    displayText(f"Player two high score: {p2highscore}", WIDTH//2, HEIGHT//2 + 110, WHITE, 20)

    pygame.display.update()
    # keep frame rate
    clock.tick(FPS)

  while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        with open("highscore.json", 'w') as filehandle:
          if player1Score >= p1highscore:
            highscoreJSONObject["player1"] = player1Score
          if player2Score >= p2highscore:
            highscoreJSONObject["player2"] = player2Score
          filehandle.write(json.dumps(highscoreJSONObject))

        running = False
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
          player2YFac = -1
        if event.key == pygame.K_DOWN:
          player2YFac = 1
        if event.key == pygame.K_w:
          player1YFac = -1
        if event.key == pygame.K_s:
          player1YFac = 1
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            player2YFac = 0
        if event.key == pygame.K_w or event.key == pygame.K_s:
            player1YFac = 0
    for player in listOfPlayers:
      if pygame.Rect.colliderect(ball.getRect(), player.getRect()):
        ball.hit()
    player1.update(player1YFac)
    player2.update(player2YFac)
    point = ball.update()
    # -1 -> player_1 has scored
    # +1 -> player_2 has scored
    #  0 -> None of them scored
    if point == -1:
        player1Score += 1
    elif point == 1:
        player2Score += 1

    if point:   # Someone has scored a point and the
      # ball is out of bounds. So, we reset it's position
        ball.reset()

    # Displaying the objects on the screen
    player1.display()
    player2.display()
    ball.display()

    # Displaying the scores of the players
    player1.displayScore("Player1 : ", player1Score, 100, 20, WHITE)
    player2.displayScore("Player2 : ", player2Score, WIDTH-100, 20, WHITE)

    pygame.display.update()
    # Adjusting the frame rate
    clock.tick(FPS)

  #while gameover:

if __name__ == "__main__":
  main()
  pygame.quit()