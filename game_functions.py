import sys

import pygame
from bullet import Bullet
from alien import Alien

def fire_bullets(ai_settings,screen,ship,bullets):
	#创建子弹，并将其加入到编组bullets中
	if len(bullets)<ai_settings.bullets_allowed:
		new_bullet=Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)	

def check_keydown_events(event,ai_settings,screen,ship,bullets):
	"""响应按键"""
	if event.key==pygame.K_RIGHT:
		#向右移动
		ship.moving_right=True
	elif event.key==pygame.K_LEFT:
		#向左移动
		ship.moving_left=True
	elif event.key==pygame.K_SPACE:
		fire_bullets(ai_settings,screen,ship,bullets)
	elif event.key==pygame.K_q:
		#按下q退出程序
		sys.exit()

def check_keyup_events(event,ship):
	"""响应松开"""
	if event.key==pygame.K_RIGHT:
		#向右平移
		ship.moving_right=False
	elif event.key==pygame.K_LEFT:
		#向左平移
		ship.moving_left=False


def check_events(ai_settings,screen,ship,bullets):
	"""响应按键和鼠标按键"""
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
		# 按下键盘
		elif event.type==pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type==pygame.KEYUP:
			check_keyup_events(event,ship)

def update_screen(ai_settings,screen,ship,aliens,bullets):
	"""更新屏幕上的图像，并切换到新屏幕"""

	#每次循环都重绘屏幕
	screen.fill(ai_settings.bg_color)
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	# 最近绘制的屏幕可见
	pygame.display.flip()

def create_fleet(ai_settings,screen,aliens):
	"""创建外星人群"""
	#创建一个外星人，并计算一行可容纳多少个外星人
	#外星人的间距为外星人宽度
	alien=Alien(ai_settings,screen)
	alien_width=alien.rect.width
	avaliable_space_x=ai_settings.screen_width-2*alien_width #除去两边边距
	number_aliens_x=int(avaliable_space_x/(2*alien_width)) #一行的外星人数量

	#创建第一行外星人
	for alien_number in range(number_aliens_x):
		# 创建一个外星人并将其加入当前行
		alien=Alien(ai_settings,screen)
		alien.x=(2*alien_number+1)*alien_width
		alien.rect.x=alien.x
		aliens.add(alien)

def update_bullets(bullets):
	"""更新子弹的位置，并删除已消失的子弹"""
	#更新子弹的位置
	bullets.update()
	#删除已经消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom<=0:
			bullets.remove(bullet)
