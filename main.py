import pygame,sys,random
from pygame.locals import *
from virus import Virus
from doctor import Doctor
import matplotlib.pyplot as plt

#Initialize all of the pygame modules
pygame.init()

#Set up and configure the font object for rendering text display
pygame.font.init()
font = pygame.font.SysFont("Helvetica",70)

#Set up and configure the screen and clock objects
screen_info = pygame.display.Info()
width,height = size = screen_info.current_w,screen_info.current_h
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

#Color Constants
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)

#This is a boolean flag used to create a temporary pause between successive rounds
round_over = False

#These global variables are used for collecting data about the simulation
    #Test data stores the set of data for each round of the simulation
    #Tests keeps track of the total number of tests performed
    #Case samples is the maximum number of tests performed in a trial
    #Success is the number of successful tests in a trial run
test_data = []
tests = 0
success = 0
case_samples = 10

#These are the main parameter that affect the outcome of the simulation
    #doc_num -> starting number of doctors
    #bac_num -> starting number of bacteria/virus particles
    #split_time -> the time interval at which the germs/bacteria undergo fission and duplicate
doc_num = 50
bac_num = 5
split_time = 500

#A global variable used to toggle on and off the game canvas;  we can turn off the game canvas in order
#   to allow the simulation to run faster
display = True

#Sprite groups for keeping track of bacteria and doctors
bacteria = pygame.sprite.Group()
doctors = pygame.sprite.Group()

#Boolean flag for stopping the game loop
done = False



def init():
    global round_over
    global split_time,bac_num,doc_num

    round_over = False
    bacteria.empty()
    doctors.empty()
    for i in range(bac_num):
        new_virus = Virus((random.randint(50,width-50),random.randint(50,height-50)),split_time)
        bacteria.add(new_virus)

    for i in range(doc_num):
        new_doctor = Doctor((random.randint(50,width-50),random.randint(50,height-50)))
        doctors.add(new_doctor)

def process_events():
    global display,screen,done
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if event.type == KEYDOWN:
            if event.key == K_f:
                screen = pygame.display.set_mode(size,FULLSCREEN)
            if event.key == K_d:
                screen = pygame.display.set_mode(size)
            if event.key == K_a:
                display = not display




def timeout():
    for i in range(100):
        clock.tick(60)
        process_events()



def end_of_round():
    global tests,success,test_data,case_samples
    global split_time, doc_num, bac_num, done
    if display:
        timeout()
    tests += 1
    if tests >= case_samples:
        test_data.append([doc_num,bac_num,split_time,tests,success/tests*100])
        result = test_data[-1]
        print(result)
        success_rate = result[-1]
        if success_rate == 0:
            doc_num += 5
        elif success_rate <= 50:
            doc_num += 3
        elif success_rate <= 75:
            doc_num += 1
        else:
            split_time = round(split_time*0.9)
            if split_time <= 10:
                done = True

    init()


def process_data():
    global display

    x = []
    y = []
    for row in test_data:
        if row[-1] >= 75:
            x.append(row[2])
            y.append(row[0])
    fig = plt.figure()
    plt.scatter(x,y)
    plt.title("Doctors needed to stop outbreak")
    plt.xlabel("Split Time")
    plt.ylabel("Doctors Needed")
    fig.savefig("data.png")


def main():
    global round_over
    global done, success
    global split_time,bac_num,doc_num
    init()
    while not done:
        if display:
            clock.tick(60)
        process_events()

        text = None
        text_rect = None
        if len(bacteria) >= split_time*bac_num:
            text = font.render("You were overrun",False,RED)
            text_rect = text.get_rect()
            round_over = True
        elif len(bacteria) == 0:
            text = font.render("Outbreak controlled", False, RED)
            text_rect = text.get_rect()
            round_over = True
            success += 1
        else:
            text = font.render("Bacteria: {}".format(len(bacteria)), False, RED)
            text_rect = text.get_rect()
            bacteria.update()
            doctors.update()
            pygame.sprite.groupcollide(bacteria,doctors,True,False)


        if display:
            screen.fill(WHITE)
            bacteria.draw(screen)
            doctors.draw(screen)
            screen.blit(text,text_rect)
            pygame.display.flip()

        if round_over:
            end_of_round()
    process_data()


    pygame.quit()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

