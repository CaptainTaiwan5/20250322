# 太空生存戰
import pygame
import random 
import os

FPS = 60 
WIDTH = 500     # 視窗寬 
HEIGHT = 600    # 視窗長

994# 設定每個顏色數值
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 遊戲初始化 and 創建視窗
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("第一個遊戲") # 設定視窗標題
clock = pygame.time.Clock()

# 載入圖片
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()

player_mini_img = pygame.transform.scale(player_img, (25, 19))  # 將飛船縮小
player_mini_img.set_colorkey(BLACK) # 設定飛船透明度
pygame.display.set_icon(player_mini_img)
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert() # 載入子彈圖檔

# 載入石頭的圖檔
rock_imgs = []
for i in range(7):
	rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())

# 載入爆炸、石頭的圖檔  
expl_anim = {}
expl_anim['lg'] = [] # 存放大石頭的list
expl_anim['sm'] = [] # 存放小石頭的list
expl_anim['player'] = [] # 存放飛船爆炸的list
for i in range(9):
	# 石頭圖檔
	expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
	expl_img.set_colorkey(BLACK) # 設定石頭的透明度
	expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))  # 將石頭圖檔放大
	expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))  # 將石頭的圖檔縮小

	# 飛船爆炸圖檔
	player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
	player_expl_img.set_colorkey(BLACK)
	expl_anim['player'].append(player_expl_img)

# 載入護盾、炮得圖檔
power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join("img", "shield.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("img", "gun.png")).convert()

# 載入音樂、音效
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.wav"))
expl_sounds = [
	pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
	pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]
pygame.mixer.music.load(os.path.join("sound", "background.wav"))
pygame.mixer.music.set_volume(0.4)

font_name = os.path.join("font.ttf") # 載入字型

def draw_text(surf, text, size, x, y): # OK
	font = pygame.font.Font(font_name, size) # 設定文字字型、大小
	text_surface = font.render(text, True, WHITE) # 設定文字顏色
	text_rect = text_surface.get_rect() # 建立成為rect物件

	# 設定文字位置
	text_rect.centerx = x 
	text_rect.top = y

	surf.blit(text_surface, text_rect) # 繪製到畫布上
 
def new_rock(): # OK
	r = Rock() #建立一個新的石頭物件
	all_sprites.add(r)
	rocks.add(r) # 新增到rock list

def draw_health(surf, hp, x, y): # OK
	if hp < 0:
		hp = 0
	BAR_LENGTH = 100 # 血條長度
	BAR_HEIGHT = 10  # 血條高度
	fill = (hp/100)*BAR_LENGTH # 現有生命值長度
	outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT) # 血條外框的rect物件
	fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT) # 實際血量的rect物件
	pygame.draw.rect(surf, GREEN, fill_rect) 		# 劃出實際血量
	pygame.draw.rect(surf, WHITE, outline_rect, 2)	# 畫出血條外框

def draw_lives(surf, lives, img, x, y): # OK
	for i in range(lives):
		img_rect = img.get_rect() 	# 建立一個rect物件
		# 設定愛心位置
		img_rect.x = x + 32*i  		
		img_rect.y = y

		surf.blit(img, img_rect) # 畫出愛心

def draw_init():    # OK
	screen.blit(background_img, (0,0)) # 繪製背景圖片

	# 繪製文字
	draw_text(screen, '太空生存戰!', 64, WIDTH/2, HEIGHT/4) 
	draw_text(screen, '← →移動飛船 空白鍵發射子彈~', 22, WIDTH/2, HEIGHT/2)
	draw_text(screen, '按任意鍵開始遊戲!', 18, WIDTH/2, HEIGHT*3/4)

	pygame.display.update() # 更新畫面

	waiting = True
	while waiting:  # 等待按下任何按鈕，開始遊戲
		clock.tick(FPS)
		# 取得輸入
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # 結束遊戲
				pygame.quit()
				return True
			elif event.type == pygame.KEYDOWN: #按下任何按鈕，遊戲開始
				waiting = False
				return False

class Player(pygame.sprite.Sprite): # 任務三
	def __init__(self): # OK
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(player_img, (50, 38)) # 飛船圖檔
		self.image.set_colorkey(BLACK) # 設定飛船的透明度
		self.rect = self.image.get_rect() 
		self.radius = 20
		# pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.speedx = 8		# 左右移動的速度
		self.health = 100 	# 生命值
		self.lives = 3		# 三次的機會
		self.hidden = False
		self.hide_time = 0
		self.gun = 1 		# 一次發出炮的數量
		self.gun_time = 0

	def update(self): # OK
		now = pygame.time.get_ticks()
		if self.gun > 1 and now - self.gun_time > 5000: # 超過可使用兩個砲火的時間，扣除一個砲火
			self.gun -= 1
			self.gun_time = now

		if self.hidden and now - self.hide_time > 1000: # 如果飛船是隱藏起來，且隱藏的時間超過限定時間，則顯示在畫面中下方
			self.hidden = False
			self.rect.centerx = WIDTH / 2
			self.rect.bottom = HEIGHT - 10

		key_pressed = pygame.key.get_pressed() # 獲得鍵盤事件
		if key_pressed[pygame.K_RIGHT]: # 往右移動
			self.rect.x += self.speedx
		if key_pressed[pygame.K_LEFT]:  # 往左移動
			self.rect.x -= self.speedx

		if self.rect.right > WIDTH:  # 超出右邊邊界，有永遠保持在右邊的邊界旁
			self.rect.right = WIDTH  
		if self.rect.left < 0:		 # 超出左邊邊界，有永遠保持在左邊的邊界旁
			self.rect.left = 0

	def shoot(self): # OK
		if not(self.hidden): # 如果飛船是顯示的狀況
			if self.gun == 1: 
				bullet = Bullet(self.rect.centerx, self.rect.top) # 建立一個飛彈物件
				all_sprites.add(bullet) 
				bullets.add(bullet) 
				shoot_sound.play() # 播放子彈音效
			elif self.gun >=2:
				bullet1 = Bullet(self.rect.left, self.rect.centery) # 建立一個飛彈物件
				bullet2 = Bullet(self.rect.right, self.rect.centery)# 建立一個飛彈物件
				all_sprites.add(bullet1)
				all_sprites.add(bullet2)
				bullets.add(bullet1)
				bullets.add(bullet2)
				shoot_sound.play() # 播放子彈音效

	def hide(self): # OK
		self.hidden = True
		self.hide_time = pygame.time.get_ticks() # 紀錄開始隱藏的時間
		self.rect.center = (WIDTH/2, HEIGHT+500)

	def gunup(self): # OK
		self.gun += 1
		self.gun_time = pygame.time.get_ticks() # 紀錄有兩顆砲火的時間

class Rock(pygame.sprite.Sprite): # 任務四
	def __init__(self): # OK
		pygame.sprite.Sprite.__init__(self)
		self.image_ori = random.choice(rock_imgs) # 隨機選擇一個石頭的圖檔
		self.image_ori.set_colorkey(BLACK) # 設定透明度
		self.image = self.image_ori.copy()
		self.rect = self.image.get_rect() # 建立rect物件
		self.radius = int(self.rect.width * 0.85 / 2) # 決定石頭的分數
		# pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
		# 隨機生成石頭位置
		self.rect.x = random.randrange(0, WIDTH - self.rect.width) 
		self.rect.y = random.randrange(-180, -100)

		# 隨機決定投烙下的方向、速度
		self.speedy = random.randrange(2, 5)
		self.speedx = random.randrange(-3, 3)

		self.total_degree = 0 # 設定一開始轉動的度數為0

		# 隨機決定轉動的方向、速度
		self.rot_degree = random.randrange(-3, 3)

	def rotate(self): # OK
		self.total_degree += self.rot_degree # 增加轉動的度數
		self.total_degree = self.total_degree % 360 # 保持在360度以內

		self.image = pygame.transform.rotate(self.image_ori, self.total_degree) # 旋轉圖片
		center = self.rect.center
		self.rect = self.image.get_rect() 
		self.rect.center = center

	def update(self): # OK
		self.rotate() # 旋轉石頭

		# 更新石頭的座標
		self.rect.y += self.speedy
		self.rect.x += self.speedx

		# 若是超出遊戲視窗(上、左、右)，重新random位置跟移動方向、速度
		if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0: 
			self.rect.x = random.randrange(0, WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100, -40)
			self.speedy = random.randrange(2, 10)
			self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite): # 任務五
	def __init__(self, x, y): # OK
		pygame.sprite.Sprite.__init__(self)
		self.image = bullet_img # 子彈圖檔
		self.image.set_colorkey(BLACK) # 設定透明度
		self.rect = self.image.get_rect() 
		self.rect.centerx = x 
		self.rect.bottom = y
		self.speedy = -10 # 設定子彈移動速度

	def update(self): # OK
		self.rect.y += self.speedy #　根據移動速度，移動子彈

		if self.rect.bottom < 0: # 超出螢幕時，刪除子彈
			self.kill()

class Explosion(pygame.sprite.Sprite): # OK
	def __init__(self, center, size):
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.image = expl_anim[self.size][0] # 設定為爆炸圖list的第一張圖片
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0 	# 第幾張圖檔的index
		self.last_update = pygame.time.get_ticks() # 紀錄最後一次更新圖檔的時間
		self.frame_rate = 50 # 更新的速度

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate: # 上一次更新到現在，已經超過更新時間，更新圖檔
			self.last_update = now # 更新最後一次的時間
			self.frame += 1 # 更變圖檔index
			if self.frame == len(expl_anim[self.size]): # 超過圖檔的數量，刪除此爆炸物建
				self.kill()
			else:
				self.image = expl_anim[self.size][self.frame] # 必更圖檔
				center = self.rect.center
				self.rect = self.image.get_rect()
				self.rect.center = center

class Power(pygame.sprite.Sprite): # OK
	def __init__(self, center):
		pygame.sprite.Sprite.__init__(self)
		self.type = random.choice(['shield', 'gun']) # 隨機生成護盾、砲彈
		self.image = power_imgs[self.type] # 獲得圖檔
		self.image.set_colorkey(BLACK) # 設定透明度
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.speedy = 3 # 設定下降速度

	def update(self):
		self.rect.y += self.speedy # 更新道具的位置
		if self.rect.top > HEIGHT: # 超出視窗範圍，刪除道具
			self.kill()


pygame.mixer.music.play(-1)

# 遊戲迴圈
show_init = True
running = True
while running:
	if show_init:
		close = draw_init() #顯示初始遊戲畫面
		if close:
			break
		show_init = False
		# 建立pygame Group物件
		all_sprites = pygame.sprite.Group()
		rocks = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		powers = pygame.sprite.Group()

		player = Player() # 宣告一個player物件
		all_sprites.add(player)
		for i in range(8):
			new_rock() # 生成8個新的石頭

		score = 0
	
	clock.tick(FPS)
	# 取得輸入
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE: # 按下空白建，射出子彈
				player.shoot()

	# 更新遊戲
	all_sprites.update()

	# 判斷石頭 子彈相撞
	hits = pygame.sprite.groupcollide(rocks, bullets, True, True)
	for hit in hits: # 處理每個撞擊事件
		random.choice(expl_sounds).play() # 發出銷毀石頭的音效
		score += hit.radius # 加上該石頭相對應的分數
		expl = Explosion(hit.rect.center, 'lg') # 建立爆炸物件(大)
		all_sprites.add(expl)
		if random.random() > 0.9: # 隨機掉落道具
			pow = Power(hit.rect.center) # 建立道具物件
			all_sprites.add(pow) 
			powers.add(pow) 
		new_rock() # 新增一個石頭

	# 判斷石頭 飛船相撞
	hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
	for hit in hits: # 處理每個撞擊事件
		new_rock()
		player.health -= hit.radius * 2 	# 更新飛船的血條
		expl = Explosion(hit.rect.center, 'sm') # 建立爆炸物建(小)
		all_sprites.add(expl)
		if player.health <= 0: # 當血量小0
			death_expl = Explosion(player.rect.center, 'player') # 建立爆炸物件(飛船爆炸)
			all_sprites.add(death_expl)
			die_sound.play() 	# 撥放死亡音效
			player.lives -= 1 	# 扣除一次機會
			player.health = 100 # 更新血條為100
			player.hide()		# 將飛船隱藏
			
	# 判斷寶物 飛船相撞
	hits = pygame.sprite.spritecollide(player, powers, True)
	for hit in hits: # 處理每個撞擊事件
		# 護盾事件
		if hit.type == 'shield': 
			player.health += 20 # 增加血量
			if player.health > 100:
				player.health = 100
			shield_sound.play() # 撥放音效

		# 砲火事件
		elif hit.type == 'gun':
			player.gunup() 	# 新增砲火數量
			gun_sound.play()# 播放音效 

	if player.lives == 0 and not(death_expl.alive()): # 沒有機會且血條為0，顯示初始畫面
		show_init = True

	# 畫面顯示
	screen.fill(BLACK)
	screen.blit(background_img, (0,0))
	all_sprites.draw(screen) # 將所有的物件顯示在螢幕上
	draw_text(screen, str(score), 18, WIDTH/2, 10) 	# 顯示分數
	draw_health(screen, player.health, 5, 15)		# 顯示血條
	draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15) # 顯示機會
	pygame.display.update()

pygame.quit()