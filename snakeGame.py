import os, sys, random, math, time
import pygame
from pygame.locals import *

# Game parameters
defaultWidth = 1200
defaultHeight = 900
gameTileSize = 20

scoreBoardHeight = 100

# Color RGB Presets
blackColor = (0, 0, 0)
athensGray = (214, 218, 219)
woodBrown = (48, 39, 27)
topaz = (255, 191, 128)

# Colors to use for sprites
snakeColor = (68, 105, 125)
boardColor = (105, 225, 65)
cherryColor = (225, 65, 105)

# Game board refresh time
intervalTime = 0.03

class Board:
    """ Class to represent the board """
    def __init__(self, width, height):
        """
            Board class constructor - Initializes board based on length and width parameters
            Arguments: 
                width (Integer) - Board width
                height (Integer) - Board height
            Returns: None
        """
        pygame.init()

        # Initialize window
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Snake")

        # Board background
        self.windowBackground = pygame.image.load('woodbackground.jpg')
        self.windowBackground = pygame.transform.scale(self.windowBackground, (width, height - scoreBoardHeight))

        # Cherry Image
        self.cherryImg = pygame.image.load('cherryImg.jpg')
        self.cherryImg = pygame.transform.scale(self.cherryImg, (round(gameTileSize * 1.5), round(gameTileSize * 1.5)))

        # "Score" WordArt Image
        self.scoreImg = pygame.image.load('scoreImg.png')
        self.scoreImg = pygame.transform.scale(self.scoreImg, (round(width * 0.2), round(scoreBoardHeight * 0.8)))

        # Score-board background
        self.scoreBackground = pygame.image.load('scoreBoardBackground.jpg')
        self.scoreBackground = pygame.transform.scale(self.scoreBackground, (round(width), round(scoreBoardHeight)))

        # Font for displaying score - Supplied with the repository
        self.scoreFont = pygame.font.Font('batmanforeveralternate.ttf', round(scoreBoardHeight * 0.5))

        pygame.display.update()

        self.width = width
        self.height = height

        # Board row and column limits
        self.cols = math.floor(width/gameTileSize)
        self.rows = math.floor((height - scoreBoardHeight)/gameTileSize)
        
        self.cherryPosition = None

        # Create a Snake object
        self.snake = Snake(self)

        # Create the first cherry on the board
        self.setNewCherry(self.snake.occupiedPositions)
    
    def checkBoundary(self, newPosition):
        """
            Function to check if a new position falls outside the board boundary i.e. is invalid
            Arguments: 
                newPosition - Tuple with 2 integers (x and y coordinates)
            Returns: True if valid and False otherwise
        """
        if((0 <= newPosition[0] <= width - 1) and (0 <= newPosition[1] <= height - 1)):
            return True
        else:
            return False
    
    def convertPosition(self, newPosition):
        """
            Function to convert a position to fall within the board boundaries
            Arguments: 
                newPosition - Tuple with 2 integers (x and y coordinates)
            Returns: Converted Tuple with 2 integers (x and y coordinates)
        """
        returnTuple = (newPosition[0] % self.cols, newPosition[1] % self.rows)
        return returnTuple
    
    def setNewCherry(self, occupiedPositions):
        """
            Generates a new cherry on the board for the snake to eat and grow using random integers
            Picks a position not already occupied by the snake
            Arguments:
                occupiedPositions - List of positions (tuples) occupied by the snake
        """
        newCherryX = occupiedPositions[0][0]
        newCherryY = occupiedPositions[0][1]

        # Make sure cherry doesn't overlap with Snake
        while((newCherryX, newCherryY) in occupiedPositions):
            newCherryX = random.randint(0, self.cols - 2)
            newCherryY = random.randint(0, self.rows - 2)
        
        # Initialize cherry center and surrounding 8 squares as cherry positions
        self.cherryPosition = (newCherryX, newCherryY)
        self.cherryPositions = []
        self.cherryPositions.append(self.cherryPosition)
        
        cherryPos2 = (newCherryX + 1, newCherryY)
        cherryPos3 = (newCherryX + 1, newCherryY + 1)
        cherryPos4 = (newCherryX, newCherryY + 1)
        cherryPos5 = (newCherryX - 1, newCherryY)
        cherryPos6 = (newCherryX - 1, newCherryY - 1)
        cherryPos7 = (newCherryX, newCherryY - 1)
        cherryPos8 = (newCherryX - 1, newCherryY + 1)
        cherryPos9 = (newCherryX + 1, newCherryY - 1)
        self.cherryPositions.append(cherryPos2)
        self.cherryPositions.append(cherryPos3)
        self.cherryPositions.append(cherryPos4)
        self.cherryPositions.append(cherryPos5)
        self.cherryPositions.append(cherryPos6)
        self.cherryPositions.append(cherryPos7)
        self.cherryPositions.append(cherryPos8)
        self.cherryPositions.append(cherryPos9)     
    
    def gameEnd(self):
        """
            Function to handle event post game loss
        """
        # Load and display Game End message
        endGame = pygame.image.load('gameEnd.png')
        self.window.blit(endGame, (self.width/8 , self.height/2))
        pygame.display.update()

        # Wait for mouse click or quit to exit
        while True:
            for event in pygame.event.get():
                if(event.type == MOUSEBUTTONUP or event.type == QUIT):
                    pygame.quit()
                    sys.exit(0)
        
    def moveSnake(self):
        """ 
            Function to move snake on the board by calling underlying snake object
            Also checks to see if cherry was eaten and generates a new cherry
            Arguments: None
            Returns: None
        """
        # Call underlying Snake object's makeMove function
        moveValid, ateCherry = self.snake.makeMove(self.snake.currDirection)

        if(moveValid == False):
            # End the game if move was invalid
            self.gameEnd()
        else:
            # If a valid move
            if(ateCherry == True):
                self.setNewCherry(self.snake.occupiedPositions)

        # Redraw all sprites        
        self.updateBoard()
        
    def updateBoard(self):
        """
            Draws sprites and objects onto screen
            Arguments: None
            Returns: None
        """
        # Draw window and score-board backgrounds
        self.window.blit(self.windowBackground, (0, 0))
        self.window.blit(self.scoreBackground, (0, self.height - scoreBoardHeight))
        
        # Draw border between board and score-board
        borderRect = pygame.Rect(0, 0, self.width, self.height - scoreBoardHeight)
        pygame.draw.rect(self.window, athensGray, borderRect, 5)
        
        # Render score
        scoreText = self.scoreFont.render(str(self.snake.cherriesEaten * 100), True, athensGray, woodBrown)
        self.window.blit(scoreText, (self.width * 0.22, (self.height - scoreBoardHeight) + scoreBoardHeight * 0.1, self.width * 0.2, scoreBoardHeight))


        # Draw snake body
        for posTuple in self.snake.occupiedPositions:
            rectPositionX = gameTileSize * posTuple[0]
            rectPositionY = gameTileSize * posTuple[1]

            pygame.draw.circle(self.window, snakeColor, (rectPositionX, rectPositionY), gameTileSize/2)
            
        cherryRectX = gameTileSize * self.cherryPosition[0]
        cherryRectY = gameTileSize * self.cherryPosition[1]

        # Draw cherry
        self.window.blit(self.cherryImg, (cherryRectX, cherryRectY))

        # Draw "Score" WordArt
        self.window.blit(self.scoreImg, (0, self.height - scoreBoardHeight))
       
        pygame.display.update()

    def runGame(self):
        """
            Main loop to run the game. Handles events from PyGame and calls underlying functions as needed
            Arguments: None
            Returns: None
        """
        # Update the board before starting
        self.updateBoard()

        # Loop to update the board every intervalTime seconds
        while(True):
            for event in pygame.event.get():
                if(event.type == QUIT):
                    # Handle close button click
                    pygame.quit()
                    sys.exit(0)
                elif(event.type == KEYDOWN):
                    # Handle key presses to change snake direction
                    if(event.key == K_LEFT and self.snake.currDirection != 'right'):
                        self.snake.currDirection = 'left'
                    elif(event.key == K_RIGHT and self.snake.currDirection != 'left'):
                        self.snake.currDirection = 'right'
                    elif(event.key == K_UP and self.snake.currDirection != 'down'):
                        self.snake.currDirection = 'up'
                    elif(event.key == K_DOWN and self.snake.currDirection != 'up'):
                        self.snake.currDirection = 'down'
                
            time.sleep(intervalTime)
            
            # Move snake - If no keys are pressed, continues moving in earlier direction
            self.moveSnake()
            # Update board after move
            self.updateBoard()



class Snake:
    """Class to represent the snake and hold all related properties"""
    def __init__(self, board):
        """
            Constructor for Snake. Constructs a Snake of length 2 with the head located at (0, 1) by default.
            Arguments: None
            Returns: None
        """
        self.length = 2
        self.cherriesEaten = 0
        self.headPosition = (0, 1)
        self.occupiedPositions = [self.headPosition, (0, 0)]
        self.currDirection = 'right'
        self.board = board
        
    def changeDirection(self, direction):
        """ Changes the current movement direction of the snake """
        self.currDirection = direction

    def ateCherry(self):
        """
            Function to perform activities after a cherry has been eaten.
            Grows 2 circles after each eaten cherry
            Arguments: None
            Returns: None
        """
        self.length += 2
        self.cherriesEaten += 1
    
    def makeMove(self, direction):
        """
            Function to move the snake in a specified direction on the board
            Arguments:
                Direction: String to indicate movement direction ('up', 'down', 'left' or 'right')
            Returns:
                (True, True) if move was valid and cherry was eaten
                (True, False) if move was valid but cherry wasnt eaten
                (False, False) if move was invalid i.e. the snake hit itself
        """
        ateCherry = False      

        # Calculate new position
        if(direction == 'left'):
            newPosition = (self.headPosition[0] - 1, self.headPosition[1])
        elif(direction == 'right'):
            newPosition = (self.headPosition[0] + 1, self.headPosition[1])
        elif(direction == 'up'):
            newPosition = (self.headPosition[0], self.headPosition[1] - 1)
        elif(direction == 'down'):
            newPosition = (self.headPosition[0], self.headPosition[1] + 1)

        # Convert new position to avoid crossing board boundaries
        newPosition = self.board.convertPosition(newPosition)       
        
        if(newPosition not in self.occupiedPositions):
            # No snake collision with itself detected
            self.headPosition = newPosition
            
            # Insert new headPositioninto occupiedPositions
            self.occupiedPositions.insert(0, (newPosition))

            if(newPosition in self.board.cherryPositions):
                # If cherry eaten, grow by adding additional position to occupiedPositions i.e. add 2 pop 1 overall in this funtion
                self.ateCherry()
                ateCherry = True
                self.occupiedPositions.insert(-1, self.occupiedPositions[-1])

            else:
                # If no cherry, remove one position from tail since new head has been inserted above to maintain length
                self.occupiedPositions.pop()

            return (True, ateCherry)

        else:
            # Snake collision detected so the move is invalid
            return (False, False)


if(__name__ == "__main__"):
    # Initialize board and run game
    board = Board(defaultWidth, defaultHeight)
    board.runGame()
