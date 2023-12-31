import time
from colorsys import hsv_to_rgb
import subprocess
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789

# Create the display
cs_pin = DigitalInOut(board.CE0)
dc_pin = DigitalInOut(board.D25)
reset_pin = DigitalInOut(board.D24)
BAUDRATE = 24000000

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
# Input pins:
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT

# Turn on the Backlight
backlight = DigitalInOut(board.D26)
backlight.switch_to_output()
backlight.value = True

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for color.
width = disp.width
height = disp.height
image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Clear display.
disp.image(image)

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

udlr_fill = "#00FF00"
udlr_outline = "#00FFFF"
button_fill = "#FF00FF"
button_outline = "#FFFFFF"

fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

# 배경화면과 캐릭터에 사용될 이미지 불러오기
cat = Image.open("cat.png").convert("RGBA")
Fish_cat = Image.open("Fish_cat(1).png").convert("RGBA")
Background = Image.open("background.jpg").convert("RGBA")
result =0

while True:
    #배경화면 구현 및 물고기가 잡혔는지 아닌지에 따라 고양이 이미지 변경
    image.paste(Background, (0, 0))

    if(result==1) :
        image.paste(Fish_cat, (140, 90), Fish_cat) 
    else:
        image.paste(cat, (150, 80), cat) 
    
    # A키를 누름에 따라 낚시 화면 이동
    if not button_A.value:  # left pressed
        result = subprocess.run(["python", "main.py"])
    with open('result.txt', 'r') as file:                            
        result = int(file.read())
        
    # Display the Image
    disp.image(image)

    time.sleep(0.01)
