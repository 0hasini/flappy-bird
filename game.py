import pygame as pg
import sys
import time
from bird import Bird
from pipe import Pipe

pg.init()

class Game:
    def __init__(self):
        # setting window config
        self.width = 1000
        self.height = 730
        self.scale_factor = 1.5
        self.win = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.move_speed = 250

        # Initialize game state variables
        self.is_enter_pressed = False
        self.pipes = []
        self.pipe_generate_counter = 71
        self.score = 0
        self.font = pg.font.Font(None, 40)
        self.game_active = False  # Track if the game is currently active

        self.setUpBgAndGround()
        self.resetGame()  # Initialize the game state
        self.gameLoop()

    def resetGame(self):
        """Reset the game to its initial state."""
        self.bird = Bird(self.scale_factor)
        self.is_enter_pressed = False
        self.pipes = []
        self.pipe_generate_counter = 71
        self.score = 0
        self.game_active = True  # Set the game to active

    def gameLoop(self):
        last_time = time.time()
        while True:
            # calculating delta time
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        if not self.game_active:  # Restart if the game is over
                            self.resetGame()
                        else:
                            self.is_enter_pressed = True
                            self.bird.update_on = True
                    if event.key == pg.K_SPACE and self.is_enter_pressed:
                        self.bird.flap(dt)

            if self.game_active:
                self.updateEverything(dt)
                self.checkCollisions()

            self.drawEverything()
            pg.display.update()
            self.clock.tick(60)

    def checkCollisions(self):
        # Check if the bird has collided with the ground or pipes
        if self.bird.rect.bottom > 568:  # Bird hits the ground
            self.game_active = False
            self.is_enter_pressed = False
        if len(self.pipes) > 0 and (
            self.bird.rect.colliderect(self.pipes[0].rect_down) or
            self.bird.rect.colliderect(self.pipes[0].rect_up)
        ):  # Bird hits a pipe
            self.game_active = False
            self.is_enter_pressed = False

    def updateEverything(self, dt):
        if self.is_enter_pressed:
            # Moving the ground
            self.ground1_rect.x -= (self.move_speed * dt)
            self.ground2_rect.x -= (self.move_speed * dt)

            if self.ground1_rect.right < 0:
                self.ground1_rect.x = self.ground2_rect.right
            if self.ground2_rect.right < 0:
                self.ground2_rect.x = self.ground1_rect.right

            # Generating pipes
            if self.pipe_generate_counter > 70:
                self.pipes.append(Pipe(self.scale_factor, self.move_speed))
                self.pipe_generate_counter = 0

            self.pipe_generate_counter += 1

            # Moving the pipes
            for pipe in self.pipes:
                pipe.update(dt)
            
            # Removing pipes if out of screen and incrementing score if passed
            if len(self.pipes) != 0:
                if self.pipes[0].rect_up.right < self.bird.rect.left:
                    self.pipes.pop(0)
                    self.score += 1  # Increment score when a pipe passes

            # Moving the bird
            self.bird.update(dt)

    def drawEverything(self):
        self.win.blit(self.bg_img, (0, -250))
        for pipe in self.pipes:
            pipe.drawPipe(self.win)
        self.win.blit(self.ground1_img, self.ground1_rect)
        self.win.blit(self.ground2_img, self.ground2_rect)
        self.win.blit(self.bird.image, self.bird.rect)

        # Render and display the score on the screen
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.win.blit(score_text, (50, 50))

        # Display Game Over message if the game is not active
        if not self.game_active:
            game_over_text = self.font.render("Game Over! Press Enter to Restart", True, (255, 0, 0))
            self.win.blit(game_over_text, (self.width // 2 - game_over_text.get_width() // 2, self.height // 2))

    def setUpBgAndGround(self):
        # Loading images for bg and ground
        self.bg_img = pg.transform.scale_by(pg.image.load("bg.jpg").convert(), self.scale_factor)
        self.ground1_img = pg.transform.scale_by(pg.image.load("ground.jpg").convert(), self.scale_factor)
        self.ground2_img = pg.transform.scale_by(pg.image.load("ground.jpg").convert(), self.scale_factor)

        
        self.ground1_rect = self.ground1_img.get_rect()
        self.ground2_rect = self.ground2_img.get_rect()

        self.ground1_rect.x = 0
        self.ground2_rect.x = self.ground1_rect.right
        self.ground1_rect.y = 568
        self.ground2_rect.y = 568
    
game = Game()