import pygame

class Slider:
    slider_selected = None
    
    def __init__(self, default_val:float, min_val:float, max_val:float, step:int, 
                 topleft:pygame.Vector2, width:int, height:int, bar_color:tuple, slider_circle_rad:int, 
                 slider_circle_color:tuple, label:str, font_size:int, text_color:tuple) -> None:
        
        self.previous_value = default_val
        self.current = default_val
        self.min_val = min_val
        self.max_val = max_val
        self.step = step
        
        self.slider_circle_rad = slider_circle_rad
        self.slider_rect = pygame.rect.Rect(topleft.x, topleft.y, width, height)
        
        self.slider_circle_rect = pygame.rect.Rect(0, 0, slider_circle_rad * 2, slider_circle_rad * 2)
        self.slider_circle_rect.center = pygame.Vector2(((self.current - self.min_val) / (self.max_val - self.min_val)) \
                                                        * self.slider_rect.width + self.slider_rect.left
                                                        , self.slider_rect.centery)
        
        self.bar_color = bar_color
        self.slider_circle_color = slider_circle_color
        
        self.in_hold = False
        
        
        self.font_size = font_size
        self.font = pygame.font.SysFont('Arial', font_size)
        self.text_color = text_color
        
        self.label = self.font.render(label, False, self.text_color)
        self.text = self.font.render(str(default_val), False, self.text_color)
        
    def slide(self):
        mouse_pos = pygame.mouse.get_pos()
        
        def round_to_nearest(number, x):
            if x == 0: raise ValueError("Cannot round to the nearest 0.")

            rounded_number = round(number / x) * x
            return rounded_number
        
        if pygame.mouse.get_pressed()[0]:
            if (self.slider_circle_rect.collidepoint(mouse_pos) or self.in_hold) \
                and self.slider_rect.x <= mouse_pos[0] <= self.slider_rect.right \
                and (Slider.slider_selected in [None, self]):
                    
                self.slider_circle_rect.centerx = mouse_pos[0]
                self.in_hold = True
                
                self.current = (((self.slider_circle_rect.centerx - self.slider_rect.left) / self.slider_rect.width) \
                               * (self.max_val - self.min_val)) + self.min_val
                self.current = round_to_nearest(self.current, self.step)
                
                Slider.slider_selected = self
        else:
            self.in_hold = False
            Slider.slider_selected = None
            
        self.text = self.font.render(str(self.current), False, self.text_color)
            
        return self.current
        
    def draw(self, display):
        pygame.draw.rect(display, self.bar_color, self.slider_rect)
        pygame.draw.circle(display, self.slider_circle_color, self.slider_circle_rect.center, self.slider_circle_rad)
        
        display.blit(self.label, pygame.Vector2(self.slider_rect.x, self.slider_rect.y - self.font_size - 5))
        display.blit(self.text, pygame.Vector2(self.slider_rect.right + 10, self.slider_rect.y - 5))