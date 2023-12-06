import time
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
import subprocess

cs_pin = DigitalInOut(board.CE0)
dc_pin = DigitalInOut(board.D25)
reset_pin = DigitalInOut(board.D24)
BAUDRATE = 24000000

udlr_fill = "#00FF00"
udlr_outline = "#00FFFF"

spi = board.SPI()
disp = st7789.ST7789(
    spi,
    height=240,
    y_offset=80,
    rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT

button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT

width = disp.width
height = disp.height
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)
fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

#사용할 이미지들 선언
caught_fish_image = Image.open("Red_Snapper.png")
caught_fish_image = caught_fish_image.resize((20, 20))

Unknown_fish = Image.open("Fish.png")

line_image = Image.open("낚시바늘.png")
line_image = line_image.resize((10, 20))

Background = Image.open("배경화면.jpg")
num_fish = 3  # Change the number of fish as needed

#물고기 구현
fish_list = []
for _ in range(num_fish):
    fish = {
        "x": random.randint(0, width),
        "y": random.randint(0, height),
        "dx": random.choice([-2, -1, 1, 2]),
        "dy": random.choice([-2, -1, 1, 2]),
        "caught" : False,
        "state" : 1,
        "state_change_time": time.time()
    }
    fish_list.append(fish)

# 낚시대 충돌 범위 구현
line_x = width // 2
line_y = 0
line_length = 10
#잡힌 물고기 체크 변수 선언
caught_fish = None

while True:
    image.paste(Background, (0, 0))

    #좌측 상단 거리 표시
    A = str(240-line_y)
    draw.text((0, 0), A, font=fnt, fill=(255,255,255))

    #잡힌 물고기 일정시간마다 조이스틱 조작 발동용 변수
    current_time = time.time()

    #잡힌 물고기와 그렇지 않은 물고기 움직임 및 이미지 구현
    for fish in fish_list:

        if fish["caught"]:
            image.paste(caught_fish_image, (line_x, line_y-10))
            line_x += random.choice([-2, -4, -6, 2, 4, 6])
            line_y += random.choice([-2, -4, -6])
            if current_time - fish["state_change_time"] > 3 :
                fish["state"] = 3 - fish["state"]
                fish["state_change_time"] = time.time()
            
            if fish["state"] == 1 :
                right_fill = 0
                if not button_R.value:  # right pressed
                    right_fill = udlr_fill
                    line_y += 2
                draw.polygon([
                    (80, 60), (44, 42), (44, 82)], outline=udlr_outline, fill=right_fill
                    )        
            else :   
                left_fill = 0
                if not button_L.value:  # left pressed
                    left_fill = udlr_fill
                    line_y += 2
                draw.polygon([(0, 60), (36, 42), (36, 81)], outline=udlr_outline, fill=left_fill)
            
        else :
            image.paste(Unknown_fish, ((fish["x"]-12), fish["y"]))
            fish["x"] += fish["dx"]
            fish["y"] += fish["dy"]

            if fish["x"] < 0 or fish["x"] > width or fish["y"] < 0 or fish["y"] > height:
                fish["dx"] = random.choice([-2, -1, 1, 2])
                fish["dy"] = random.choice([-2, -1, 1, 2])

            if (
                fish["x"]-12  <= line_x <= fish["x"] + 12
                and fish["y"]-10 <= line_y <= fish["y"] + line_length
                and caught_fish == None
                ):
                fish["caught"] = True
                caught_fish = fish

    #물고기가 잡히지 않은 상태라면 낚시 바늘 표시
    if (caught_fish == None):
        image.paste(line_image, (line_x, line_y))
            

    disp.image(image)         

    #조이스틱 조작에 따른 낚시 바늘 움직임 구현
    if not button_U.value:
        line_y -= 5

    if not button_D.value:
        line_y += 5

        if not button_R.value:
            line_x += 3

        if not button_L.value:
            line_x -= 3

    #낚시 바늘이 화면 밖으로 벗어났을 때 동작 구현
    if line_y > height:
        if caught_fish:
            if not button_B.value :
                with open('result.txt', 'w') as file:
                    file.write('1')
                subprocess.run(["python", "test.py"])
        else:
            with open('result.txt', 'w') as file:
                file.write('0')
            subprocess.run(["python", "test.py"])


    if line_y < -10 or (line_y<100 and line_x < 0) or (line_y<100 and line_x > 240) :
        with open('result.txt', 'w') as file:
            file.write('0')
        subprocess.run(["python", "test.py"])
    
    line_y = min(height, line_y - 1)    

    time.sleep(0.1)

