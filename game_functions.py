import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

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

def check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y):
	"""在玩家单击play按钮时开始新游戏"""
	button_clicked=play_button.play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		# 重置游戏统计信息
		stats.reset_stats()
		stats.game_active=True
		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
		# 创建一群新的外星人，并让飞船居中
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()

def check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets):
	"""响应按键和鼠标按键"""
	for event in pygame.event.get():
		if event.type==pygame.QUIT:
			sys.exit()
		# 按下键盘
		elif event.type==pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y=pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,mouse_x,mouse_y)
		elif event.type==pygame.KEYDOWN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type==pygame.KEYUP:
			check_keyup_events(event,ship)

def update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button):
	"""更新屏幕上的图像，并切换到新屏幕"""
	# 每次循环都重绘屏幕
	screen.fill(ai_settings.bg_color)
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	# 如果游戏处于非活动状态，绘制play按钮
	if not stats.game_active:
		play_button.draw_button()
	# 最近绘制的屏幕可见
	pygame.display.flip()

def get_number_rows(ai_settings,ship_height,alien_height):
	"""计算屏幕可容纳多少行外星人"""
	avaliable_space_y=ai_settings.screen_height-3*alien_height-ship_height
	number_rows=int(avaliable_space_y/(2*alien_height))
	return number_rows


def get_number_aliens_x(ai_settings,ship_height,alien_width):
	"""计算每行可容纳多少个外星人"""
	avaliable_space_x=ai_settings.screen_width-2*alien_width #除去两边边距
	return int(avaliable_space_x/(2*alien_width)) #一行的外星人数量

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	"""创建一个外星人并将其放在当前行"""
	alien=Alien(ai_settings,screen)
	alien_width=alien.rect.width
	alien.x=(2*alien_number+1)*alien_width
	alien.rect.x=alien.x
	alien.rect.y=alien.rect.height+2*alien.rect.height*row_number
	aliens.add(alien)


def create_fleet(ai_settings,screen,ship,aliens):
	"""创建外星人群"""
	#创建一个外星人，并计算一行可容纳多少个外星人
	alien=Alien(ai_settings,screen)
	number_aliens_x=get_number_aliens_x(ai_settings,ship.rect.height,alien.rect.width)
	number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
	
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_number,row_number)

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets):
	"""响应被外星人撞到的飞船"""
	if stats.ships_left>0:
		# 余下的飞船数减1
		stats.ships_left-=1
		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
		#创建一群新外星人，将飞船放到屏幕就中央
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
		#暂停
		sleep(0.5)
	else:
		stats.game_active=False

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets):
	"""检查是否有外星人到达屏幕底部"""
	screen_rect=screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom>=screen_rect.bottom:
			#像飞船被撞到一样处理
			ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
			break



def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
	"""检查是否有外星人位于屏幕边缘，并更新整群外星人的位置"""
	check_fleet_edges(ai_settings,aliens)
	"""检查外星人是否到达底端"""
	check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets)
	"""更新外星人群中所有外星人的位置"""
	aliens.update()

	#检测外星人和飞船之间的碰撞
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,screen,ship,aliens,bullets)

def check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets):
	#检查是否有子弹击中了外星人
	#如果是这样，删除相应的子弹和外星人
	collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)

	if len(aliens)==0:
		#删除现有的子弹并新建一群外星人
		bullets.empty()
		create_fleet(ai_settings,screen,ship,aliens)

def update_bullets(ai_settings,screen,ship,aliens,bullets):
	"""更新子弹的位置，并删除已消失的子弹"""
	#更新子弹的位置
	bullets.update()
	check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets)
	#删除已经消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom<=0:
			bullets.remove(bullet)

def check_fleet_edges(ai_settings,aliens):
	"""有外星人到达边缘时采取相应的措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break

def change_fleet_direction(ai_settings,aliens):
	"""将整群外星人下移，并改变他们的方向"""
	for alien in aliens.sprites():
		alien.rect.y+=ai_settings.fleet_drop_speed
	ai_settings.fleet_direction*=-1
