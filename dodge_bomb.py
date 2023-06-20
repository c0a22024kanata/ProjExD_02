import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
delta = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}

def check_bound(rect: pg.Rect) ->tuple[bool,bool]:
    """
    こうかとんRect　爆弾Rectが画面外　or 画面内かを判定する関数
    引数　こうかとんRect or 爆弾Rect
    戻り値　横方向、縦方向の判定結果タプル(True:画面内/False:画面外)    
    """
    yoko,tate=True,True
    if rect.left < 0 or WIDTH < rect.right: 
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:
        tate=False
    return yoko,tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)

    bd_img=pg.Surface((20,20)) # 練習１
    pg.draw.circle(bd_img,(255,0,0),(10,10),10)
    bd_img.set_colorkey((0,0,0))
    x=random.randint(0,WIDTH)
    y=random.randint(0,HEIGHT)
    kk_img_2 = pg.transform.flip(kk_img, True, False)  # rotozoomするためのflipしたこうかとんの画像
    # こうかとんの画像方向の辞書
    kk_imgs = {
        (+5, 0): kk_img_2,  # 右方向こうかとんの画像
        (+5, -5): pg.transform.rotozoom(kk_img_2, 45, 1.0),  # 右上方向こうかとんの画像
        (0, -5): pg.transform.rotozoom(kk_img_2, 90, 1.0),  # 上方向こうかとんの画像
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 1.0),  # 左上方向こうかとんの画像
        (-5, 0): kk_img,  # 左方向こうかとんの画像
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 1.0),  # 左下方向こうかとんの画像
        (0, +5): pg.transform.rotozoom(kk_img_2, -90, 1.0),  # 下方向こうかとんの画像
        (+5, +5): pg.transform.rotozoom(kk_img_2, -45, 1.0),  # 右下方向こうかとんの画像
        }
    kk_img1 = kk_imgs[+5, 0]

    clock = pg.time.Clock()
    tmr = 0
    bd_rect=bd_img.get_rect()
    bd_rect.center=x,y
    vx,vy=+5,+5
    kk_rect=kk_img1.get_rect()
    kk_rect.center=900,400




    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if kk_rect.colliderect(bd_rect):
            print("ゲームオーバー")
            return
         
        key_list = pg.key.get_pressed()
        sum_mv=[0,0]
        for k, mv in delta.items():
            if key_list[k]:
                sum_mv[0]+=mv[0]
                sum_mv[1]+=mv[1]
        #kk_rot_img=kk_imgs[tuple(sum_mv)]
        kk_rect.move_ip(sum_mv)

        if check_bound(kk_rect) != (True,True):
            kk_rect.move_ip(-sum_mv[0],-sum_mv[1])

        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rect)
        screen.blit(bd_img,bd_rect)
        bd_rect.move_ip(vx,vy)
        yoko,tate=check_bound(bd_rect)

        if sum_mv[0] != 0 or sum_mv[1] != 0:  # 飛ぶ方向に従ってこうかとん画像を切り替える
            kk_img = kk_imgs[tuple(sum_mv)]
        screen.blit(kk_img, kk_rect)

        if not yoko:
            vx *=-1
        if not tate:
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()