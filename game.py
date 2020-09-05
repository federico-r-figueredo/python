
import simplegui
import math
import random


initial_Text_p = 1100
initial_Text_o = 900
initial_Text_n = 700
initial_Text_g = 600
velocity_Text = 1

countUp = 0
music_Count = 0
music_Count2 = 0
alien_position = random.randrange(100, 700)
alien_direction = random.choice([1, -1])
alien_height = 200
color_tick = 0

P_place = False
O_place = False
N_place = False
G_place = False
ASTEROIDS_place = False
music_Sync = False

WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
game_Start = False
rock_Tick = 0
firstrock_Place = False
rock_group = set()
missle_group = set()

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

alien = simplegui.load_image('http://pluspng.com/img-png/space-invaders-png-space-invaders-transparent-background-png-image-200.png')
    
startup_Music = simplegui.load_sound('https://raw.githubusercontent.com/Hiddentale/Test/master/ARCADE%202019%20ULTRACOMBO%20Login%20Screen%20-%20League%20of%20Legends.mp3')
startup_Music.set_volume(0.1)
    
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")


splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")


ship_info = ImageInfo([45, 45], [90, 90], 35) #Was 35 initially 
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")


missile_info = ImageInfo([5,5], [10, 10], 20, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")


asteroid_info = ImageInfo([45, 45], [90, 90], 90)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")


explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")


soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
ship_thrust_sound.set_volume(.4)
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")



soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")
soundtrack.set_volume(.2)

def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def color_timer():
    global color_tick
    if color_tick < 3:
        color_tick += 1
    else:
        color_tick = 0


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.thrusters = False
        self.ax = 0
        self.friction = 0.98
        
        
    def get_position(self):
        return self.pos
    
    
    def get_radius(self):
        return self.radius
        
    def draw(self,canvas):
        if self.thrusters == False:
            #self.sound.rewind()
            #self.sound.play()
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, 
                              self.image_size, self.angle) 
            
        elif self.thrusters == False and self.shrinkray == True:
            canvas.draw_image(self.image, [self.image_center[0] + 90, self.image_center[1]], 
                              self.image_size, self.pos, [self.radius, self.radius], self.angle)
        else:
            canvas.draw_image(self.image, [self.image_center[0] + 90, self.image_center[1]], 
                              self.image_size, self.pos, self.image_size, self.angle)
            
    def keydown_handler(self, key_Press):
        if simplegui.KEY_MAP['left'] == key_Press:
            self.angle_vel -= 0.04
    
        elif simplegui.KEY_MAP['right'] == key_Press:
            self.angle_vel += 0.04
        
        elif simplegui.KEY_MAP['up'] == key_Press:
            self.thrusters = True
            ship_thrust_sound.play()
            
            
            
        
    
    def keyup_handler(self, key_Press):
        if simplegui.KEY_MAP['left'] == key_Press:
            self.angle_vel += 0.04
    
        elif simplegui.KEY_MAP['right'] == key_Press:
            self.angle_vel -= 0.04
        elif simplegui.KEY_MAP['up'] == key_Press:
            self.thrusters = False
            ship_thrust_sound.pause()
        
    def update(self):
        for i in range(2):
            self.vel[i] *= self.friction
            
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.ax = angle_to_vector(self.angle)
        if self.thrusters == True:
            self.vel[0] += self.ax[0] * 0.1
            self.vel[1] += self.ax[1] * 0.1
            
        if self.pos[1] >= HEIGHT:
            self.pos[1] -= HEIGHT
            
        elif self.pos[1] <= 0:
            self.pos[1] += HEIGHT
            
        elif self.pos[0] >= WIDTH:
            self.pos[0] -= WIDTH
            
        elif self.pos[0] <= 0:
            self.pos[0] += WIDTH
            
    def shoot(self):
        global missle_group
        self.ax2 = angle_to_vector(self.angle)
        missle_velocity = 5
        missle_position = [self.pos[0] + self.radius * self.ax2[0], self.pos[1] + self.radius * self.ax2[1]]
        missle_group.add(Sprite(missle_position, [self.vel[0] + missle_velocity * self.ax2[0], 
                           self.vel[1] + missle_velocity * self.ax2[1]], self.angle, 
                           self.angle_vel, missile_image, missile_info, missile_sound))
            
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, [self.radius, self.radius], self.angle)
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def update(self):
        self.age += 1
        if self.age >= self.lifespan:
            return True
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        if self.pos[1] >= HEIGHT:
            self.pos[1] -= HEIGHT
            
        elif self.pos[1] <= 0:
            self.pos[1] += HEIGHT
            
        elif self.pos[0] >= WIDTH:
            self.pos[0] -= WIDTH
            
        elif self.pos[0] <= 0:
            self.pos[0] += WIDTH     
            
    def collide(self, other_object):
        distance = dist(other_object.get_position(), self.pos)
        if distance <= (self.radius + other_object.get_radius() - 40):
            return True

           
def draw(canvas):
    global time, lives, score, game_Start, missle_group, rock_group
    global alien_position, alien_direction, alien_height
    
    # animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    
    
    # draw ship and sprites
    if game_Start == True:
        
        if lives <= 0:
            game_Start = False
            soundtrack.rewind()
            soundtrack.play()
            lives = 3
            ship_thrust_sound.rewind()
            rock_group = set()
            missle_group = set()
            score = 0
            
        rock_timer.start()
            
        if firstrock_Place == True:
            for rock in rock_group:
                rock.update()
                
        my_ship.update()
        for missle in missle_group:
            missle.update()
            
        canvas.draw_text('Lives: ' + str(lives), [20, 20], 16, "White")
        canvas.draw_text('Score: ' + str(score), [720, 20], 16, "White")
        my_ship.draw(canvas)
        for missle in missle_group:
            missle.draw(canvas)
        if firstrock_Place == True:
            if group_collide(rock_group, my_ship):
                lives -= 1
            else:
                for missle in missle_group:
                    if group_collide(rock_group, missle):
                        score += 10
            process_sprite_group(rock_group, canvas)
            process_sprite_group(missle_group, canvas)
         
    if game_Start == False:
        rock_timer.stop()
        
        if alien_position >= 760:
            alien_direction = -1
            alien_height += 5
            
        elif alien_position <= 30:
            alien_direction = 1
            alien_height += 15
        
        alien_position += alien_direction
        canvas.draw_image(alien, (200 / 2, 200 / 2), (200, 200), (alien_position, alien_height), (50, 50))
    
    if game_Start == False: #and music_Sync == True:
        global initial_Text_p, initial_Text_o, initial_Text_n, initial_Text_g
        global P_place, O_place, N_place, G_place, ASTEROIDS_place
        global velocity_Text
        
        
        if initial_Text_p >= 232 and ASTEROIDS_place == False and P_place == False:
            initial_Text_p -= 2 * velocity_Text
            velocity_Text += 0.7
            canvas.draw_text('W', [initial_Text_p, 120], 68, '#F0FFFF')
            if initial_Text_p <= 260:
                P_place = True
        else:
            canvas.draw_text('W', [232, 120], 68, '#F0FFFF')
            
            
        if P_place == True and ASTEROIDS_place == False:
            if initial_Text_o >= 271 and O_place == False:
                initial_Text_o -= 2 * velocity_Text
                velocity_Text += 0.04
                canvas.draw_text('I', [initial_Text_o, 120], 68, '#F0FFFF')
                if initial_Text_o <= 300:
                    O_place = True
            else:
                canvas.draw_text('I', [271, 120], 68, '#F0FFFF')
                
        if O_place == True and ASTEROIDS_place == False:
            if initial_Text_n >= 305 and N_place == False:
                initial_Text_n -= 2 * velocity_Text
                velocity_Text += 0.04
                canvas.draw_text('P', [initial_Text_n, 120], 68, '#F0FFFF')
                if initial_Text_n <= 345:
                    N_place = True
            else:
                canvas.draw_text('P', [305, 120], 68, '#F0FFFF')
        
        if N_place == True and ASTEROIDS_place == False:
            if initial_Text_g >= 325 and G_place == False:
                if initial_Text_n <= 350:
                    G_place = True
                    ASTEROIDS_place = True
                    
                initial_Text_g -= 2 * velocity_Text
                velocity_Text += 0.04
                canvas.draw_text('', [initial_Text_g, 120], 68, '#F0FFFF')
                
                if ASTEROIDS_place == True:
                    canvas.draw_text('', [330, 120], 68, '#F0FFFF')
        
        # Makes the word 'Asteroids' rotate colors
        if ASTEROIDS_place == True:
            if color_tick == 0:           		    
                canvas.draw_text('W', [232, 120], 68, '#87CEEB')
                canvas.draw_text('I', [268, 120], 68, '#B0E0E6')
                canvas.draw_text('P', [300, 120], 68, '#4682B4')
                canvas.draw_text('', [332, 120], 68, '#4169E1')
            
            elif color_tick == 1:
                canvas.draw_text('W', [232, 120], 68, '#4169E1')
                canvas.draw_text('I', [268, 120], 68, '#87CEEB')
                canvas.draw_text('P', [300, 120], 68, '#B0E0E6')
                canvas.draw_text('', [332, 120], 68, '#4682B4')
      
            elif color_tick == 2:
                canvas.draw_text('W', [232, 120], 68, '#4682B4')
                canvas.draw_text('I', [268, 120], 68, '#4169E1')
                canvas.draw_text('P', [300, 120], 68, '#87CEEB')
                canvas.draw_text('', [332, 120], 68, '#B0E0E6')
   
            elif color_tick == 3:
                canvas.draw_text('W', [232, 120], 68, '#B0E0E6')
                canvas.draw_text('I', [268, 120], 68, '#4682B4')
                canvas.draw_text('P', [300, 120], 68, '#4169E1')
                canvas.draw_text('', [332, 120], 68, '#87CEEB')
                
            canvas.draw_text('Press the Spacebar to start the game!', [170, 170], 32, 'white')      
        
def process_sprite_group(set, canvas):
    for object in set:
        object.draw(canvas)
        if object.update():
            set.remove(object)
  
            
        
    
def group_collide(group, other_object):
    global rock_group
    temp_group = set(group)
    for object in temp_group:
        if object.collide(other_object):
            temp_group.remove(object)
            rock_group = temp_group
            return True

def keydown_handler(key_Press):
    global game_Start
    if game_Start == False:
        if simplegui.KEY_MAP['space'] == key_Press:
            game_Start = True
    if game_Start == True:        
        my_ship.keydown_handler(key_Press)
        if simplegui.KEY_MAP['space'] == key_Press:
            my_ship.shoot()

def keyup_handler(key_Press):
        my_ship.keyup_handler(key_Press)
        
        
            
# timer handler that spawns a rock    
def rock_spawner():
    global rock_Tick, firstrock_Place, a_rock, rock_group
    rock_Position = [random.randrange(0, WIDTH),random.randrange(0, HEIGHT)]
    rock_arc = random.random() * .2 - .1
    rock_velocity = [random.randrange(-3, 3), random.randrange(-3, 3)]
    
    firstrock_Place = True
    if len(rock_group) < 12:
        rock_group.add(Sprite(rock_Position, rock_velocity, 0, rock_arc, asteroid_image, asteroid_info))
    print len(rock_group)
 
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites

my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)

color_timer_handler = simplegui.create_timer(150, color_timer)

rock_timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
soundtrack.play()
color_timer_handler.start()
frame.start()