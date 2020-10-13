import pygame.font

class Button:

    def __init__(self, ai_game, msg):
        #initialize button attribute
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #dimension and properties of a button
        self.width, self.height = 200, 50
        self.button_color = (255, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        #build the button rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        #Button message needs to be prepped only once
        self.__prep_msg(msg)

    def __prep_msg(self, msg):
        #turn message into a rendered image and center text on the buttom
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def daw_button(self):
        #draw blank button and then draw the message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
