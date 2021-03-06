#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
	import pygame
	import json
	import zipfile
	import io
	import pickle
	import ConfigParser
	import re
	from itertools import chain
except ImportError, message:
    raise SystemExit,  "Unable to load module. {}".format(message)
    
pygame.init()

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message
        
def TextRectRender(string, font, rect, textcolour, backgroundcolour, justification=0): #Don't touch this
    finallines = []

    requestedlines = string.splitlines()

    for requestedline in requestedlines:
        if font.size(requestedline)[0] > rect.width:
            words = requestedline.split(' ')
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException, "The word " + word + " is too long to fit in the rect passed."
            accumulatedline = ""
            
            for word in words:
                test_line = accumulatedline + word + " "   
                if font.size(test_line)[0] < rect.width:
                    accumulatedline = test_line 
                else: 
                    finallines.append(accumulatedline) 
                    accumulatedline = word + " " 
            finallines.append(accumulatedline)
        else: 
            finallines.append(requestedline) 

    surface = pygame.Surface(rect.size, pygame.SRCALPHA) 
    surface.fill((150, 150, 150, 0))

    accumulatedheight = 0 
    for line in finallines: 
        if accumulatedheight + font.size(line)[1] >= rect.height:
            raise TextRectException, "Once wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, 1, textcolour)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulatedheight))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulatedheight))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulatedheight))
            else:
                raise TextRectException, "Invalid justification arg: " + str(justification)
        accumulatedheight += font.size(line)[1]

    return surface

def TextRender(text, colour, size, fontfile): #Function for rendering character and story text
	font = pygame.font.Font("fonts/{}.ttf".format(fontfile), size)
	textrender = font.render(text, 1, (colour))
	return textrender
	
def StoryData(table, value): #Parse story json file
	parsed_json = json.loads(storydata)
	json_data = parsed_json[table][value]
	return json_data
  
def LoadFromZip(location, name, filetype): #Load images, music and other content from zip file
	zipcontents = archive.read('{}/{}.{}'.format(location, name, filetype))
	bytesio = io.BytesIO(zipcontents) #Pygame won't accept files straight from zip. Do this so it can use them.
	return bytesio
	
def TransRect(width, height, r, g, b, aplha): #Used for rendering semi-transparent rects
	s = pygame.Surface((width, height), pygame.SRCALPHA)
	s.fill((r, g, b, aplha))
	return s
	
def MuteSound(audio):#Mutes game audio.
	if audio == True:
		pygame.mixer.music.pause()
		audio = False
	elif audio == False:
		pygame.mixer.music.unpause()
		audio = True
	return audio
	
def CharMove(x, y):
	characterrect.move_ip(x, y)
	return
	
def VideoPlay(videofile): #Plays videos, does nothing special.
	introvideo = pygame.movie.Movie('{}/{}.vnv'.format(avdir, videofile))
	introscreen = pygame.Surface(introvideo.get_size()).convert()
	introvideo.set_display(introscreen)
	introvideo.play()
	playing = True
	while playing:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				introvideo.stop()
				playing = False
				done = True
				
		screen.blit(introscreen,(0,0))
		pygame.display.update()
		click.tick(int(config.get('settings', 'videofps')))
		if introvideo.get_busy() == False:
			playing = False
	return

def StartAudio(audiofile): #Starts music playing, can be called at any point to change audio.
	pygame.mixer.init()
	pygame.mixer.music.load("{}/{}.vnm".format(avdir, audiofile))
	pygame.mixer.music.set_volume(float(config.get('settings', 'volume')))
	return
	
def BGLoad(): #Loads background image
	background = pygame.image.load(LoadFromZip(backgrounddir, StoryData(table, "background"), "jpg"))
	backgroundrect = background.get_rect()
	return background, backgroundrect
	
def CharLoad(): #Loads character image
	characterimage = pygame.image.load(LoadFromZip(characterdir, StoryData(table, "characterimage"), "png"))
	characterrect = characterimage.get_rect()
	CharMove(0, 0)
	return characterimage, characterrect
	
def MainMenu(): #Display main menu title/options. This is only temporary and will be redone when the rest of the game works fine.
	if mainmenurendered == False:
		screen.blit(BGLoad()[0], BGLoad()[1])
	
		MainMenuTitle = config.get('vn_info', 'mainmenutitle')
		Dev_Info = config.get('vn_info', 'devinfo')
		Copyright = config.get('vn_info', 'copyright')
		#Game title
		screen.blit(TextRender(MainMenuTitle, BLACK, 39, 'titles'), (3, 5))
		screen.blit(TextRender(Dev_Info, BLACK, 16, 'titles'), (350, 50))
		screen.blit(TextRender(Copyright, BLACK, 10, 'titles'), (600, 588))
		
		#Background for options
		screen.blit(TransRect(142, 50, 191, 191, 191, 150), (15,535)) #w h r g b a
		screen.blit(TransRect(142, 50, 191, 191, 191, 150), (172,535))
		screen.blit(TransRect(142, 50, 191, 191, 191, 150), (329,535))
		screen.blit(TransRect(142, 50, 191, 191, 191, 150), (486,535))
		screen.blit(TransRect(142, 50, 191, 191, 191, 150), (643,535))
		
		#Options
		screen.blit(TextRender("(P)lay", BLACK, menubuttons, 'main'), (55, 547))
		screen.blit(TextRender("(L)oad", BLACK, menubuttons, 'main'), (210, 547))
		screen.blit(TextRender("(O)ptions", BLACK, menubuttons, 'main'), (353, 547))
		screen.blit(TextRender("(I)nfo", BLACK, menubuttons, 'main'), (527, 547))
		screen.blit(TextRender("(Q)uit", BLACK, menubuttons, 'main'), (682, 547))
	else:
		pass
	return
	
def DebugInfo(): #Puts Debug info on screen if DebugMode is set true in config.sec
	if config.get('settings', 'debug') == 'True':
		charname = re.sub('[<>]', '', character)
		screen.blit(TextRender('CS: {}'.format(currentscene), RED, 16, 'debug'), (10, 10))
		screen.blit(TextRender('CC: {}'.format(charname), RED, 16, 'debug'), (10, 25))
		screen.blit(TextRender('DN: {}'.format(done), RED, 16, 'debug'), (10, 40))
		screen.blit(TextRender('DM: {}'.format(devmode), RED, 16, 'debug'), (10, 55))
		screen.blit(TextRender('AP: {}'.format(pygame.mixer.music.get_busy()), RED, 16, 'debug'), (10, 70))
		screen.blit(TextRender('AM: {}'.format(audio), RED, 16, 'debug'), (10, 85))
		screen.blit(TextRender('AL: {}'.format(config.get('settings', 'volume')), RED, 16, 'debug'), (10, 100))
	else:
		pass
	return
	
config = ConfigParser.ConfigParser()
config.read('dat/config.sec')	

#Directory info
backgrounddir = config.get('dirs', 'backgrounddir')
characterdir = config.get('dirs', 'characterdir')
avdir = config.get('dirs', 'avdir')
uidir = config.get('dirs', 'uidir')
otherdir = config.get('dirs', 'otherdir')

#Set the zip file that contains resources
archive = zipfile.ZipFile("{}".format(config.get('files', 'assets')), "r")

#Set window size, give title and set if the game should run full screen or windowed.
width = int(config.get('settings', 'windowwidth'))
height = int(config.get('settings', 'windowheight'))
size = (width, height)
pygame.display.set_caption("{}".format(config.get('vn_info', 'windowtitle')))

if config.get('settings', 'fullscreen') == 'True':
	screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
else:
	screen = pygame.display.set_mode(size)

#Commonly used colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (235,16,16)

#Common font sizes
charactername = int(config.get('fonts', 'charactername'))
storysize = int(config.get('fonts', 'storysize'))
menubuttons = int(config.get('fonts', 'menubuttons'))

#Set fonts
regularfont = pygame.font.Font("{}".format(config.get('files', 'regularfont')), storysize)
debugfont = config.get('files', 'debugfont')

#Open and read story contents from json file
storyconfigread = open("{}".format(config.get('files', 'storycontent')), 'r')
storydata = storyconfigread.read()

#Inital json data to grab. We need this to start the story.
table = config.get('json_info', 'initaltable')
character = StoryData(table, "character")
storytext = StoryData(table, "dialog") 

#Load first bg/char to the screen and load inital music
background = pygame.image.load(LoadFromZip(backgrounddir, StoryData(table, "background"), "jpg"))
backgroundrect = background.get_rect()
characterimage = pygame.image.load(LoadFromZip(characterdir, StoryData(table, "characterimage"), "png"))
characterrect = characterimage.get_rect()
currentscene = "A" #This is just garbage, this variable gets changed later.
click = pygame.time.Clock()
CharMove(100,150)
StartAudio('music')

#Set inital variables for the main loop
done = False
audio = True
fromgame = False
mainmenurendered = False
devmode = config.get('settings', 'devmode')

if devmode == 'False':
	menu = False
	intro = True
	
elif devmode == 'True':
	menu = True
	intro = False
	pygame.mixer.music.play()
