import pygame, sys, random

# hàm vẽ sàn
def ve_san() :
    man_hinh.blit(san, (san_x_pos,660))
    man_hinh.blit(san, (san_x_pos+432,660))
# Hàm tạo ống
def tao_ong():
    random_pipe_pos = random.choice(chieu_cao_ong)
    bottom_pipe = be_mat_ong_tao_ra.get_rect(midtop =(650,random_pipe_pos+90))
    top_pipe = be_mat_ong_tao_ra.get_rect(midtop =(650,random_pipe_pos-700))
    return bottom_pipe,top_pipe
# Hàm di chuyển ống
def di_chuyen_ong(pipes):
    for pipe in pipes:
        pipe.centerx -= 4
    return pipes
#Hàm vẽ ống
def ve_ong(pipes):
    for pipe in pipes:
        if pipe.bottom >= 550:
            man_hinh.blit(be_mat_ong_tao_ra,pipe)
        else:
            flip_pipe = pygame.transform.flip(be_mat_ong_tao_ra,False,True) 
            #Làm cho ống nó lật ngược lại
            man_hinh.blit(flip_pipe,pipe)
#Hàm xử lý va chạm
def kiem_tra_va_cham(pipes):
    for pipe in pipes :
        if doi_hinh_chu_nhat.colliderect(pipe):
            am_thanh_va_cham.play()
            return False
    if doi_hinh_chu_nhat.top < 30 or doi_hinh_chu_nhat.bottom >= 810:
            return False
    return True

def xoay_doi_tuong(bat1):
    new_bat = pygame.transform.rotozoom(bat1,di_chuyen_cua_doi*2,1)
    return new_bat
#hàm xử lý khi đang bay hình ảnh chú chim 
def hoat_anh_cua_doi():
    new_bat = danh_sach_doi[gia_tri_cua_doi]
    new_doi_hinh_chu_nhat = new_bat.get_rect(center = (100, doi_hinh_chu_nhat.centery))
    return new_doi_hinh_chu_nhat
#Hàm in điểm ra màn hình
def hien_thi_diem(game_state):
    if game_state == 'main game':
        diem_surface = font_chu_cua_tro_choi.render(str(int(diem)),True,(110,255,250))
        diem_rect = diem_surface.get_rect(center = (216,100))
        man_hinh.blit(diem_surface,diem_rect)
    if game_state == 'game_over':
        diem_surface = font_chu_cua_tro_choi.render(f'Score: {int(diem)}',True,(110,255,250))
        diem_rect = diem_surface.get_rect(center = (216,100))
        man_hinh.blit(diem_surface,diem_rect)

        diem_cao_surface = font_chu_cua_tro_choi.render(f'High Score: {int(diem_cao)}',True, (255,255,255))
        diem_cao_rect = diem_cao_surface.get_rect(center = (216,630))
        man_hinh.blit(diem_cao_surface,diem_cao_rect)
#hàm cập nhật điểm
def cap_nhat_diem_hien_tai(diem,diem_cao):
    if diem > diem_cao:
        diem_cao = diem
    return diem_cao  

#Đây là phần xư lý âm thanh cho các file .wav
pygame.mixer.pre_init(frequency=44100,size=16,channels=2,buffer=512)

pygame.init()
pygame.display.set_caption("Flappy bat")
man_hinh = pygame.display.set_mode((432,810))
clock = pygame.time.Clock()
font_chu_cua_tro_choi = pygame.font.Font("04B_19.ttf",45)


# Biến
do_roi = 0.7  #Độ rơi
di_chuyen_cua_doi = -10  #
hoat_dong_cua_tro_choi = True 
diem = 0    #Điểm
diem_cao = 0  #Điểm cao
#chèn hinh_nen_game
hinh_nen_game = pygame.image.load("assets/background-cyperpunk.png").convert()
hinh_nen_game = pygame.transform.scale2x(hinh_nen_game)
#chèn sàn
san = pygame.image.load("assets/floor.png").convert()
san = pygame.transform.scale2x(san)
san_x_pos = 0    
#Tạo chim
doi_xuong = pygame.transform.scale2x(pygame.image.load("assets/bat2.png")).convert_alpha()
doi_can_bang = pygame.transform.scale2x(pygame.image.load("assets/bat2.png")).convert_alpha()
doi_len= pygame.transform.scale2x(pygame.image.load("assets/bat2.png")).convert_alpha()
# bat = pygame.transform.scale2x(pygame.image.load("assets/sea_horse.png")).convert_alpha
danh_sach_doi = [doi_xuong,doi_can_bang,doi_len] 
gia_tri_cua_doi = 0
bat = danh_sach_doi[gia_tri_cua_doi]

# Tạo timer cho bat 
doi_bay  = pygame.USEREVENT + 1  
pygame.time.set_timer(doi_bay,250)
doi_hinh_chu_nhat = bat.get_rect(center=(100,380))
#bat = pygame.image.load("assets/images/bluebat-midflap.png").convert_alpha()
#bat = pygame.transform.scale2x(bat)
# Tạo ống
be_mat_ong_tao_ra = pygame.image.load("assets/pipe-gray.png").convert()
be_mat_ong_tao_ra = pygame.transform.scale2x(be_mat_ong_tao_ra)
danh_sach_ong = [] 
# tạo timer
sinh_ra_ong = pygame.USEREVENT   # bien sinh_ra_ong tao thoi gian spawn ong
pygame.time.set_timer(sinh_ra_ong, 1200)
#chieu cao cua ong
chieu_cao_ong = [300,400,450] 
#Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load("assets/Main-game.png")).convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (216,364))
#chèn âm thanh
am_thanh_dap_canh = pygame.mixer.Sound("sound/sfx_wing.wav")
am_thanh_va_cham = pygame.mixer.Sound("sound/sfx_hit.wav")
am_thanh_diem = pygame.mixer.Sound("sound/sfx_point.wav")
am_thanh_diem_countdown = 100
# Vòng lặp while true để thực hiện game hoạt động
while True:

    for event in pygame.event.get():   #Bắt sự kiện 
        if event.type == pygame.QUIT:   #Khi người chơi bấm vào nút x sẽ thoát khỏi trò chơi
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and hoat_dong_cua_tro_choi:   # khi người chơi nhấn nút space bar sẽ bắt dầu chơi và bắt đâu trò chơi
                di_chuyen_cua_doi = 0
                di_chuyen_cua_doi -= 12
                am_thanh_dap_canh.play()
            if event.key == pygame.K_SPACE and hoat_dong_cua_tro_choi==False:
                hoat_dong_cua_tro_choi = True
                danh_sach_ong.clear()
                doi_hinh_chu_nhat.center = (100,300)
                di_chuyen_cua_doi = 0
                diem = 0
        if event.type == sinh_ra_ong:
            danh_sach_ong.extend(tao_ong())
        if event.type == doi_bay:
            if gia_tri_cua_doi < 2 :
                gia_tri_cua_doi += 1
            else:
                gia_tri_cua_doi = 0
            doi_hinh_chu_nhat = hoat_anh_cua_doi()
    man_hinh.blit(hinh_nen_game,(0,0))
    # btn1.draw()
    if hoat_dong_cua_tro_choi :
        # Chim di chuyển và đi qua ống
        di_chuyen_cua_doi += do_roi
        rotated_bat  = xoay_doi_tuong(bat) 
        doi_hinh_chu_nhat.centery += di_chuyen_cua_doi
        man_hinh.blit(rotated_bat, doi_hinh_chu_nhat)
        hoat_dong_cua_tro_choi = kiem_tra_va_cham(danh_sach_ong)
         #Của ống 
        danh_sach_ong = di_chuyen_ong(danh_sach_ong)
        ve_ong(danh_sach_ong)
        #Điểm
        diem += 0.01
        hien_thi_diem("main game")
        am_thanh_diem_countdown -= 100
        if am_thanh_diem_countdown <= 0:
            am_thanh_diem.play()
            am_thanh_diem_countdown = 100
    else:
        man_hinh.blit(game_over_surface,game_over_rect)
        diem_cao = cap_nhat_diem_hien_tai(diem,diem_cao)
        hien_thi_diem("game_over")
        game_over = pygame.transform.scale2x(pygame.image.load("assets/gameover.png"))
    # Của sàn 
    san_x_pos -= 1
    ve_san()
    if san_x_pos <= -432:
        san_x_pos = 0
    
    pygame.display.update()
    clock.tick(90) # Điều khiển  thời gian FPS 120 


    