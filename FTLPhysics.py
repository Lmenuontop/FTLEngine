# FTLPhysics
# basic physics for FTLEngine
from FTLEngine import Engine
import math
eng = Engine()
eng.create_display(800, 600,  "hello")
#constants:
PIXELS_PER_METER = 100
WHITE = (255,255,255)
MAX_CIRCLES = 2**6**3 - 2 # max 64 bit integer or sum
gravity = 9.81 * PIXELS_PER_METER # 100 pixels = 1 meter
pi = math.pi

def apply_force(magnitude, direction):
    ...
    #finish this function, then write a book or sum
    
    

def intersect(x1, y1, radius1, x2, y2, radius2):
    distance_squared = (x2-x1)**2 + (y2-y1)**2
    radius_sum = radius1 + radius2
    if distance_squared <= radius_sum**2:
        return True
    else:
        return False

def calc_collision(circles):
    for c in range(len(circles)):
        for k in range(c+1,len(circles)):
            c1 = circles[c]
            c2 = circles[k]
            m1 = c1.mass
            m2 = c2.mass
            if intersect(c1.x, c1.y, c1.radius, c2.x, c2.y, c2.radius):
                dx = c2.x - c1.x
                dy = c2.y - c1.y
                distance = math.sqrt(dx**2 + dy**2)

                if distance == 0:
                    continue
                    
                #normals:
                nx = dx / distance
                ny = dy / distance
                tx = -ny #tangent
                ty = nx
                v1n = c1.velocityx * nx + c1.velocity * ny
                v1t = c1.velocityx * tx + c1.velocity * ty
                v2n = c2.velocityx * nx + c2.velocity * ny
                v2t = c2.velocityx * tx + c2.velocity * ty
                if v1n - v2n > 0:
                    v1n_new = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2) #1D elastic collision formula
                    v2n_new = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2)
                    c1.velocityx = v1n_new * nx + v1t * tx
                    c1.velocity = v1n_new * ny + v1t * ty
                    c2.velocityx = v2n_new * nx + v2t * tx
                    c2.velocity = v2n_new * ny + v2t * ty

#cicle:
class circle():
    def __init__(self, x, y, bounciness, colour):
        self.bounciness = bounciness #1-10
        self.weight = 100 #newtons
        self.g = 9.81 #meters
        self.mass = self.weight / self.g
        self.acceleration = gravity
        self.velocity = 0
        self.velocityx = 0
        self.x = x
        self.y = y
        self.radius = 10
        self.radius_meters = self.radius / PIXELS_PER_METER
        self.area = pi*(self.radius_meters)**2
        self.colour = colour
        #self.terminal_velocity = math.sqrt((2*self.mass*gravity) / (1.225*1.2*self.area)) #quadratic drag formula
        #w = mg
        #m = w/g
    def render(self):
        eng.draw_circle(self.x, self.y, self.radius, self.colour)
    
    def physics(self):
        
        gravity_force = self.mass * gravity # Newtons

        #air drag
        air_density = 1.225
        drag_coefficient = 1.2
        #Because drag always opposes the direction of motion:
        drag_force = (0.5 * air_density * drag_coefficient * self.area * self.velocity * abs(self.velocity)) #drag = 0.5*density*drag_coefficent*cross_sectional_area*speed_relative_to_air ^ 2
        
        #net force:
        net_force = gravity_force - drag_force
        #newtons second law:
        #F = ma
        #a = F/m
        acceleration = net_force / self.mass
        #apply acceleration to velocity
        self.velocity += acceleration * dt
        #apply velocity to position
        self.y += self.velocity * dt
        self.x += self.velocityx * dt
        
        #damping:
        damping = 0.98 #2%, loses 2% of velocity every frame
        self.velocity *= damping
        self.velocityx *= damping
        return self.x, self.y
    
    def border_collision(self):
        #if eng.border_collision(self.x,self.y,self.radius,self.radius):
        #self.x, self.y = eng.border_collision(self.x, self.y, self.radius, self.radius) 
        #self.y -= self.bounciness
        if self.y + self.radius >= 600:
            self.y = 600 - self.radius
            self.velocity = -self.velocity * (self.bounciness / 10)
        if self.y - self.radius <= 0:
            self.y = 1 + self.radius
            self.velocity = -self.velocity * (self.bounciness / 10) #take velocity, in the other direction and multiply it by the circle's bounce constant
        if self.x - self.radius <= 0:
            self.x = 1 + self.radius
            self.velocityx = -self.velocity * (self.bounciness / 10)
        if self.x + self.radius >= 800:
            self.x = 800 - self.radius
            self.velocityx = -self.velocityx * (self.bounciness / 10)
        
        return self.x, self.y

    #collision code using vector notmals and tangents and the 1d elastic collision formula
    
    
    def keyboard_movement(self):
        ...  
        return self.x, self.y
#can do cloth sims once this is done
class spring():
    def __init__(self, circle1, circle2, target_length, colour):
        self.circle1 = circle1
        self.circle2 = circle2

        self.target_length = target_length
        self.colour = colour
        # icreasing this makes things like soft-bodies stay together instead of falling apart
        # it's the strength of the spring
        self.force = 100
        self.length = math.sqrt((circle2.x - circle1.x)**2 + (circle2.y - circle1.y)**2)


    def physics(self):
        self.x1 = self.circle1.x
        self.y1 = self.circle1.y
        self.x2 = self.circle2.x
        self.y2 = self.circle2.y

        
        #self.distX = (self.circle1.x + self.circle1.velocityx*10) - (self.circle2.x + self.circle2.velocityx*10)
        #self.distY = (self.circle1.y + self.circle1.velocity*10) - (self.circle2.y + self.circle2.velocity*10)
        #self.distance = math.hypot(self.distX, self.distY) # same as: self.distance = math.sqrt((self.distX)**2 + (self.distY)**2)
        #predicted positions didn't work :(
        self.distX = self.circle1.x - self.circle2.x
        self.distY = self.circle1.y - self.circle2.y

        self.distance = math.hypot(self.distX, self.distY)
        #if self.distance < 0.00001:
        #    return
        strength = self.force
        if self.distance > 0:
            self.circle1.velocityx += -self.distX * (1 - self.target_length/self.distance)/2 * strength/10
            self.circle1.velocity  += -self.distY * (1 - self.target_length/self.distance)/2 * strength/10
            self.circle2.velocityx +=  self.distX * (1 - self.target_length/self.distance)/2 * strength/10
            self.circle2.velocity  +=  self.distY * (1 - self.target_length/self.distance)/2 * strength/10


    def render(self):
        eng.draw_line((self.x1, self.y1),(self.x2, self.y2),self.colour)



class rectangle(circle):
    def __init__(self, x, y, width, height, bounciness, colour):
        self.bounciness = bounciness #1-10
        self.width = width
        self.height = height
        self.weight = 100 #newtons
        self.g = 9.81 #meters
        self.mass = self.weight / self.g
        self.acceleration = gravity
        self.velocity = 0
        self.velocityx = 0
        self.x = x
        self.y = y
        self.radius = self.width
        self.radius_meters = self.radius / PIXELS_PER_METER
        self.area = pi*(self.radius_meters)**2
        self.colour = colour
        
    def render(self):
        eng.draw_rectangle(self.x, self.y, self.width, self.height, self.colour)

#brotato comic code doesnt have ligatures... I mean I did pirate it... Better than courier new ngl...

"""
#example usage:
"""
circles = [circle(100,100, 8, (0,0,255)), circle(200,200,8,(255,0,10)), circle(300, 300, 8, (0, 255, 0))] # list of every circle
springs = []
squares = [rectangle(100, 100, 10, 10, 8, (255,255,255))]

for p in range(0, (len(circles) - 1)):
    springs.append(spring(circles[p], circles[p+1], 150, WHITE))
"""
#chat:
circles = [
    circle(150, 100, 8, WHITE),  # 0 top
    circle(185, 115, 8, WHITE),  # 1
    circle(205, 150, 8, WHITE),  # 2
    circle(185, 185, 8, WHITE),  # 3
    circle(150, 200, 8, WHITE),  # 4 bottom
    circle(115, 185, 8, WHITE),  # 5
    circle(95, 150, 8, WHITE),   # 6
    circle(115, 115, 8, WHITE),  # 7
]

springs = [
    # outer ring
    spring(circles[0], circles[1], 37, WHITE),
    spring(circles[1], circles[2], 40, WHITE),
    spring(circles[2], circles[3], 40, WHITE),
    spring(circles[3], circles[4], 37, WHITE),
    spring(circles[4], circles[5], 37, WHITE),
    spring(circles[5], circles[6], 40, WHITE),
    spring(circles[6], circles[7], 40, WHITE),
    spring(circles[7], circles[0], 37, WHITE),

    # cross-bracing
    spring(circles[0], circles[2], 65, WHITE),
    spring(circles[1], circles[3], 65, WHITE),
    spring(circles[2], circles[4], 65, WHITE),
    spring(circles[3], circles[5], 65, WHITE),
    spring(circles[4], circles[6], 65, WHITE),
    spring(circles[5], circles[7], 65, WHITE),
    spring(circles[6], circles[0], 65, WHITE),
    spring(circles[7], circles[1], 65, WHITE),
]

dv = eng.devmode(True)
circle_count = 3
while True:
    dt = eng.clock.tick(60) / 1000
    eng.begin_frame()
    

    for c in circles:
        c.physics()
        c.border_collision()
        c.render()
        
        
    
    for s in springs:
        s.physics()
        s.render()

    #for q in squares:
     #   q.physics()
      #  q.border_collision()
       # q.render()
      
    
    circles[2].keyboard_movement()
    calc_collision(circles)
    eng.handle_events()
    if eng.last_click and circle_count < MAX_CIRCLES:
        x,y = eng.last_click
        circles.append(circle(x, y, 8, WHITE))
        eng.debug_log("New circle created", dv)
        circle_count += 1



    
    eng.end_frame()
#end
"""

