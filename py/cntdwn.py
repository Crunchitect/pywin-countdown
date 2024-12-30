import PIL, PIL.Image, pygame, win32api, win32con, win32gui, random
from datetime import datetime
from math import floor
pygame.init()

FUCHSIA = (255, 0, 128)
FPS = 120

screen = pygame.display.set_mode((0, 0), pygame.NOFRAME | pygame.RESIZABLE | pygame.FULLSCREEN)
clock = pygame.Clock()

hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*FUCHSIA), 0, win32con.LWA_COLORKEY)

nums = {str(i): f"./imgs/num/{i}.png" for i in range(9+1)}
nums[":"] = "./imgs/num/colon.png"

def pil_img2surf(pil_image):
    im = pygame.image.frombytes(pil_image.tobytes(), pil_image.size, pil_image.mode).convert_alpha()
    # im.set_colorkey(FUCHSIA)
    return im

def blit_rotate(surf, filename, pos, angle):
    img = PIL.Image.open(filename).convert('RGBA')
    rotated_img = img.rotate(-angle%360, expand=1)
    surf_img = pil_img2surf(rotated_img)
    surf_rect = surf_img.get_rect().center
    surf.blit(surf_img, [a - b for a, b in zip(pos, surf_rect)])

def get_transform(time, origin, angular_dir):
    POSITION_JERK = 1200
    X_DAMPENING = 0.2
    ANGULAR_ACCEL = 20
    
    position = (origin[0] + POSITION_JERK * X_DAMPENING * angular_dir * time ** 3,
                origin[1] + POSITION_JERK * time ** 3)
    angle = ANGULAR_ACCEL * (angular_dir - 0.5) * time ** 2
    return position, angle

def format_timedelta(value, time_format="{days} days, {hours2}:{minutes2}:{seconds2}"):

    if hasattr(value, 'seconds'):
        seconds = value.seconds + value.days * 24 * 3600
    else:
        seconds = int(value)

    seconds_total = seconds

    minutes = int(floor(seconds / 60))
    minutes_total = minutes
    seconds -= minutes * 60

    hours = int(floor(minutes / 60))
    hours_total = hours
    minutes -= hours * 60

    days = int(floor(hours / 24))
    days_total = days
    hours -= days * 24

    years = int(floor(days / 365))
    years_total = years
    days -= years * 365

    return time_format.format(**{
        'seconds': seconds,
        'seconds2': str(seconds).zfill(2),
        'minutes': minutes,
        'minutes2': str(minutes).zfill(2),
        'hours': hours,
        'hours2': str(hours).zfill(2),
        'days': days,
        'years': years,
        'seconds_total': seconds_total,
        'minutes_total': minutes_total,
        'hours_total': hours_total,
        'days_total': days_total,
        'years_total': years_total,
    })

t = 0
display_time = format_timedelta(datetime(2025, 1, 1, 0, 0, 0) - datetime.now(), "{days}:{hours2}:{minutes2}:{seconds2}")
old_display_time = display_time
flags = [[0, False, 0]] * len(display_time)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    dt = clock.tick(FPS) / 1000
    t += dt
    
    display_time = format_timedelta(datetime(2025, 1, 1, 0, 0, 0) - datetime.now(), "{days}:{hours2}:{minutes2}:{seconds2}")
    screen.fill(FUCHSIA)
    width = 120 * len(display_time)
    # if display_time != old_display_time:
    #     print("!")
    for i, char in enumerate(display_time):
        old_char = old_display_time[i]
        if old_char != char:
            flags[i] = [0.8, True, random.random(), char, old_char]
    for i, flag in enumerate(flags):
        time, tick, direc, *chars = flag
        if tick:
            if time < 0:
                flags[i] = [0, False, 0]
                blit_rotate(screen, nums[display_time[i]], ((i * 120) + screen.get_width() // 4, screen.get_height() // 2), 0)
                continue
            char, old_char = chars
            blit_rotate(screen, nums[char], ((i * 120) + screen.get_width() // 4, screen.get_height() // 2), 0)
            blit_rotate(screen, nums[old_char], *get_transform(
                    0.8 - time + (i * 0.01),
                    ((i * 120) + screen.get_width() // 4, screen.get_height() // 2),
                    direc
                )
            )
            flags[i][0] -= dt
        else:
            blit_rotate(screen, nums[display_time[i]], ((i * 120) + screen.get_width() // 4, screen.get_height() // 2), 0)
        
    pygame.display.flip()
    old_display_time = display_time
