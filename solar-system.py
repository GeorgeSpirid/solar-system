import pygame
import math
# to initialize the module
pygame.init()

WIDTH,HEIGHT=1650,1000
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE=(255,255,255)
YELLOW=(255,255,0)
BLUE=(100,149,237)
RED=(188,39,50)
DARK_GREY=(80,78,81)
DEEP_BLUE=(0,50,150)
MINT=(152,255,152)
LAVENDER=(230,230,250)
AQUA=(0,255,255)

FONT=pygame.font.SysFont("comicsans",16)

class Planet:
    AU=149.6e6*1000
    G=6.67428e-11
    SCALE=25/AU # 1 AU = 100 pixels
    TIMESTEP=3600*24 # a day

    def __init__(self,x,y,radius,color,mass):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.mass=mass
        
        self.orbit=[]
        self.sun=False
        self.distance_to_sun=0

        self.x_vel=0
        self.y_vel=0

    def draw(self,win):
        x=self.x*self.SCALE+WIDTH/2
        y=self.y*self.SCALE+HEIGHT/2

        if len(self.orbit)>2:
            updated_points=[]
            for point in self.orbit:
                x,y=point
                x=x*self.SCALE+WIDTH/2
                y=y*self.SCALE+HEIGHT/2
                updated_points.append((x,y))
            pygame.draw.lines(win,self.color,False,updated_points,2)

        pygame.draw.circle(win,self.color,(x,y),self.radius)
        
        if not self.sun:
            distance_text=FONT.render(f"{round(self.distance_to_sun/1000,1)}km",1,WHITE)
            win.blit(distance_text,(x-distance_text.get_width()/2,y))


    def attraction(self,other):
        other_x,other_y=other.x,other.y
        distance_x=other_x-self.x
        distance_y=other_y-self.y
        distance=math.sqrt(distance_x**2+distance_y**2)

        if other.sun:
            self.distance_to_sun=distance
        
        force=self.G*self.mass*other.mass/distance**2
        theta=math.atan2(distance_y,distance_x)
        force_x=math.cos(theta)*force
        force_y=math.sin(theta)*force
        return force_x,force_y
    
    def update_position(self,planets):
        total_fx=total_fy=0
        for planet in planets:
            if self==planet:
                continue

            fx,fy=self.attraction(planet)
            total_fx+=fx
            total_fy+=fy

        self.x_vel+=total_fx/self.mass*self.TIMESTEP
        self.y_vel+=total_fy/self.mass*self.TIMESTEP

        self.x+=self.x_vel*self.TIMESTEP
        self.y+=self.y_vel*self.TIMESTEP
        self.orbit.append((self.x,self.y))


def main():
    run=True
    clock=pygame.time.Clock()

    sun=Planet(0,0,10,YELLOW,1.98892*10**30)
    sun.sun=True

    earth=Planet(-1*Planet.AU,0,10,BLUE,5.9742*10*24)
    earth.y_vel=29.783*1000

    mars=Planet(-1.524*Planet.AU,0,5.3,RED,6.39*10*23)
    mars.y_vel=24.077*1000

    mercury=Planet(0.387*Planet.AU,0,3.8,DARK_GREY,3.30*10*23)
    mercury.y_vel=47.4*1000

    venus=Planet(0.723*Planet.AU,0,9.5,WHITE,4.8685*10**24)
    venus.y_vel=-35.02*1000

    #jupiter=Planet(5.20*Planet.AU,0,112,DEEP_BLUE,1.9*10**27)
    jupiter=Planet(5.20*Planet.AU,0,50,DEEP_BLUE,1.9*10**27)
    jupiter.y_vel=13.07*1000

    #saturn=Planet(9.58*Planet.AU,0,94.5,MINT,5.68*10**26)
    saturn=Planet(9.58*Planet.AU,0,45,MINT,5.68*10**26)
    saturn.y_vel=9.69*1000

    uranus=Planet(19.22*Planet.AU,0,40.1,LAVENDER,8.68*10*25)
    uranus.y_vel=6.81*1000

    neptune=Planet(30.05*Planet.AU,0,3.88,AQUA,1.02*10**26)
    neptune.y_vel=5.43*1000

    planets=[sun,earth,mars,mercury,venus,jupiter,saturn,uranus,neptune]

    while run:
        # max of fps
        clock.tick(60)
        WIN.fill((0,0,0))

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
        
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

if __name__=="__main__":
    main()