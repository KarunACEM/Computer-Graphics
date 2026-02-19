import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 1000, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart Traffic System - Synced Final Version")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

ROAD = (50, 50, 50)
GRASS = (34, 139, 34)
WHITE = (255, 255, 255)
YELLOW = (255, 200, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
CAR_COLORS = {"N": (0, 120, 255), "S": (255, 100, 100), "E": (255, 255, 0), "W": (0, 200, 0)}

green_duration = 8
yellow_duration = 2
current_phase = "NS"
light_state = "GREEN"
timer_seconds = 0
active_vehicle = {"N": None, "S": None, "E": None, "W": None}

class Vehicle:
    def __init__(self, direction):
        self.direction = direction
        self.speed = 5
        self.width, self.height = 30, 50
        self.crossed = False
        self.color = CAR_COLORS[direction]
        
        if direction == "N":
            self.x = WIDTH//2 - 40 
            self.y = -60
        elif direction == "S":
            self.x = WIDTH//2 + 10
            self.y = HEIGHT + 60
        elif direction == "E":
            self.x = WIDTH + 60
            self.y = HEIGHT//2 - 40
        elif direction == "W":
            self.x = -60
            self.y = HEIGHT//2 + 10 

    def move(self):
        center_zone = 100
        if self.direction == "N" and self.y > HEIGHT//2 - center_zone: self.crossed = True
        if self.direction == "S" and self.y < HEIGHT//2 + center_zone: self.crossed = True
        if self.direction == "E" and self.x < WIDTH//2 + center_zone: self.crossed = True
        if self.direction == "W" and self.x > WIDTH//2 - center_zone: self.crossed = True
        if not self.crossed:
            if self.direction in ["N","S"] and current_phase!="NS":
                if self.direction=="N" and self.y+self.height>HEIGHT//2-150: return
                if self.direction=="S" and self.y<HEIGHT//2+150: return
            if self.direction in ["E","W"] and current_phase!="EW":
                if self.direction=="E" and self.x<WIDTH//2+150: return
                if self.direction=="W" and self.x+self.width>WIDTH//2-150: return
        if self.direction=="N": self.y+=self.speed
        elif self.direction=="S": self.y-=self.speed
        elif self.direction=="E": self.x-=self.speed
        elif self.direction=="W": self.x+=self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

def draw_roads():
    screen.fill(GRASS)
    pygame.draw.rect(screen, ROAD, (0, HEIGHT//2-120, WIDTH, 240))
    pygame.draw.rect(screen, ROAD, (WIDTH//2-120, 0, 240, HEIGHT))
    for i in range(0, WIDTH, 40): pygame.draw.line(screen,YELLOW,(i,HEIGHT//2),(i+20,HEIGHT//2),4)
    for i in range(0, HEIGHT, 40): pygame.draw.line(screen,YELLOW,(WIDTH//2,i),(WIDTH//2,i+20),4)
    pygame.draw.line(screen,WHITE,(WIDTH//2-60,0),(WIDTH//2-60,HEIGHT),3)
    pygame.draw.line(screen,WHITE,(WIDTH//2+60,0),(WIDTH//2+60,HEIGHT),3)
    pygame.draw.line(screen,WHITE,(0,HEIGHT//2-60),(WIDTH,HEIGHT//2-60),3)
    pygame.draw.line(screen,WHITE,(0,HEIGHT//2+60),(WIDTH,HEIGHT//2+60),3)

def draw_lights():
    ns_color = GREEN if current_phase=="NS" else RED
    ew_color = GREEN if current_phase=="EW" else RED
    if light_state=="YELLOW":
        if current_phase=="NS": ns_color=YELLOW
        else: ew_color=YELLOW
    pygame.draw.circle(screen, ns_color, (WIDTH//2-80, HEIGHT//2-160),22)
    pygame.draw.circle(screen, ns_color, (WIDTH//2+80, HEIGHT//2+160),22)
    pygame.draw.circle(screen, ew_color, (WIDTH//2+160, HEIGHT//2-80),22)
    pygame.draw.circle(screen, ew_color, (WIDTH//2-160, HEIGHT//2+80),22)

def update_lights():
    global timer_seconds, current_phase, light_state
    timer_seconds += clock.get_time()/1000
    if light_state=="GREEN" and timer_seconds>=green_duration:
        light_state="YELLOW"
        timer_seconds=0
    elif light_state=="YELLOW" and timer_seconds>=yellow_duration:
        current_phase="EW" if current_phase=="NS" else "NS"
        light_state="GREEN"
        timer_seconds=0

def draw_timer():
    remaining = max(0,int(green_duration-timer_seconds)) if light_state=="GREEN" else max(0,int(yellow_duration-timer_seconds))
    text = font.render(f"{current_phase} {light_state} Timer: {remaining}", True, WHITE)
    screen.blit(text,(20,20))

running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
    draw_roads()
    update_lights()
    for d in active_vehicle:
        if active_vehicle[d] is None: active_vehicle[d]=Vehicle(d)
    for d in list(active_vehicle.keys()):
        vehicle = active_vehicle[d]
        if vehicle:
            vehicle.move()
            vehicle.draw()
            if vehicle.x<-100 or vehicle.x>WIDTH+100 or vehicle.y<-100 or vehicle.y>HEIGHT+100: active_vehicle[d]=None
    draw_lights()
    draw_timer()
    pygame.display.update()

pygame.quit()

sys.exit()
