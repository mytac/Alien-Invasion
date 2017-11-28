import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf

def run_game():
	#初始化，并创建屏幕对象
	pygame.init()
	ai_settings=Settings()
	screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption('Alien Invasion')

	#设置背景色
	ai_settings.bg_color=(230,230,230)

	#创建一个飞船
	ship=Ship(ai_settings,screen)
	#创建一个用于存储子弹的元组
	bullets=Group()

	#开始游戏主循环
	while True:
		gf.check_events(ai_settings,screen,ship,bullets)
		ship.update()
		gf.update_bullets(bullets)
		gf.update_screen(ai_settings,screen,ship,bullets)
		
		

run_game()