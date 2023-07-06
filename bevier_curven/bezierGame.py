import pygame
import sys
import random
from .colors import *
from .position import Position
from .utils import *
from .button import Button

def startBezierGame():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    font = pygame.font.Font("freesansbold.ttf", 24)
    fps = 60

    #time
    t1 = 0
    t2 = 0
    speed = 0.004

    #set control points
    dragging = None
    controlPoints = [Position(100, 100), Position(300, 450), Position(500, 100), Position(700, 450)]

    curvePoints = []

    #obstacles variables
    obstacle1_xPos = random.randint(300, 350)
    obstacle2_xPos = random.randint(450, 500)
    obstacle1_height = random.randint(280, 330)
    obstacle2_height = random.randint(280, 330)

    #instantiate Buttons
    startButton = Button(630, 530, 150, 50, black, "Start", white, False, True)
    drawButton = Button(630, 530, 150, 50, black, "Draw", white, False, False)
    nextButton = Button(450, 530, 150, 50, black, "Next", white, False, False)
    
    #define booleans
    started = False
    gameStarted = False
    drawLine = False
    drawn = False
    next = False
    
    running = True

    while running:
        screen.fill(white)
        clock.tick(fps)
        pygame.display.set_caption("Bezier Curve")

        if started == True:
            #draw draw and next Button once game started
            drawButton.draw(screen, font)
            nextButton.draw(screen, font)
            startButton.isEnabled = False
            drawButton.isEnabled = True
            nextButton.isEnabled = True

            # instantiate obstacles
            obstacle1 = pygame.Rect(obstacle1_xPos, 0, 25, obstacle1_height)
            obstacle2 = pygame.Rect(obstacle2_xPos, 510 - obstacle2_height, 25, obstacle2_height)
            
            # draw obstacles
            pygame.draw.rect(screen, red, obstacle1)
            pygame.draw.rect(screen, red, obstacle2)

            # Check for collision
            for point in curvePoints:
                if obstacle1.collidepoint(point) or obstacle2.collidepoint(point):
                    curvePoints.clear()
                    drawn = False
                    t2 = 1
                    break
        else:
            startButton.draw(screen, font)
        
        # seperate Menu from Curve
        pygame.draw.line(screen, grey, (0, 510), (screen.get_width(), 510), 1)

        for event in pygame.event.get():
            #checks for Mouse events
            if t2 >= 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:

                        #Check if Button is clicked
                        startButton.checkClick()
                        started = startButton.isClicked
                        drawButton.checkClick()
                        drawLine = drawButton.isClicked
                        nextButton.checkClick()
                        next = nextButton.isClicked

                        #set t2 count for bezier to 0 when User clicks draw
                        if drawLine == True and drawn == False:
                            t2 = 0
                        
                        #set Game up when User clicks start
                        if started == True and drawn == False:
                            curvePoints.clear()
                            if gameStarted == False:
                                controlPoints = [Position(100, 100), Position(300, 450), Position(500, 100), Position(700, 450)]
                                gameStarted = True

                        #defines dragging as index of controll points
                        for num, controlPoint in enumerate(controlPoints):
                            if controlPoint.collidepoint(event.pos):
                                dragging = num
            
                #sets dragging to None if Mouse Button is not clicked
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        dragging = None

                #if mouse is clicked and aimed at a control point, as long as the Bezier Curve is not drawn, the controll point will change towards the Mouse Position
                elif event.type == pygame.MOUSEMOTION and dragging is not None and drawn == False:
                        #set boundaries for dragging the Controll points within Windows size
                        if (event.pos[0] < 800 and event.pos[0] > 0) and (event.pos[1] < 500 and event.pos[1] > 0):
                            if started == True:
                                #if the Game started first and last Points are only able to go to a certain area
                                if dragging == 0:
                                    if event.pos[0] < 200:
                                        controlPoints[dragging].x, controlPoints[dragging].y = event.pos
                                elif dragging == 3:
                                    if event.pos[0] > 550:
                                        controlPoints[dragging].x, controlPoints[dragging].y = event.pos
                                else:
                                    controlPoints[dragging].x, controlPoints[dragging].y = event.pos
                            else:
                                #if the Game didnt started the Points are freely movable
                                controlPoints[dragging].x, controlPoints[dragging].y = event.pos
                            
                            #clear Bezier curve
                            curvePoints.clear()

                            #if game didnt start draw the Bezier curve directly when a point changes position
                            if started == False:
                                for t2 in range(101):
                                    t2 /= 100.0
                                    cubicBezierCurve(controlPoints, t1, t2, screen, curvePoints)

            #Quit pygame
            if event.type == pygame.QUIT:
                running = False
                pygame.QUIT

        #draw straight lines in between Control points
        for i in range(len(controlPoints) - 1):
            pygame.draw.line(screen, grey, (controlPoints[i].x, controlPoints[i].y), (controlPoints[i + 1].x, controlPoints[i + 1].y), 1)

        #draw Castljau Alorithm and Bezeir curve
        cubicBezierCurve(controlPoints, t1, t2, screen, curvePoints)

        #draw control points
        for controlPoint in controlPoints:
            controlPoint.point(screen, grey)

        #reset t1 to redraw Casteljau Algorithm
        if t1 >= 1:
            t1 = 0

        #check if Game is currently drawing a Line and sets boolean to stop interacting with Control Points
        if drawLine == True:
            drawn = True
            drawLine = False
            drawButton.isClicked = False

        #checks if the next Button is clicked and resets the Level
        elif next == True:
            #set Position and height of obstacles randomly
            obstacleRandomPos = random.choice([random.randint(250, 350), random.randint(450, 500)])
            obstacle1_xPos = obstacleRandomPos
            if obstacleRandomPos >= 250 and obstacleRandomPos <=350:
                obstacle2_xPos = random.randint(450, 500)
            else:
                obstacle2_xPos = random.randint(250, 350)

            obstacle1_height = random.randint(280, 330)
            obstacle2_height = random.randint(280, 330)

            #sets Booleans so Control Points are interactible again
            drawn = False
            next = False
            nextButton.isClicked = False
            curvePoints.clear()

        #sets t2 to draw Bezier curve till t2 >= 1
        if t2 <= 1:
            t2 += speed

        t1 += speed

        pygame.display.update()

    pygame.quit()