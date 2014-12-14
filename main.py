# https://www.youtube.com/watch?v=fwyFTVJoppA

from ws2812 import WS2812
import pyb

SIZE = 144
MAX_SCORE = 10
INITIAL_SPEED = 0.7

leds = WS2812(spi_bus=1, led_count=SIZE)
pin = pyb.Pin(pyb.Pin.board.X4, pyb.Pin.IN, pyb.Pin.PULL_DOWN)
switch = pyb.Switch()

micros = pyb.Timer(2, prescaler=83, period=0x3fffffff)


ball_pos = 0
ball_velocity = INITIAL_SPEED
scores = [0, 0]


def frames_gen(micros):
    """Yields inintervals no larger than 10ms (10000 microsesonds)"""
    micros.counter(0)
    while True:
        yield
        while micros.counter() < 10000:
            pass
        micros.counter(0)

frames = frames_gen(micros)


def set_background():
    """Compute the background (empty strip + goals), copy it to the LED buffer
    """
    global background
    background = [(0, 0, 0) for i in range(SIZE)]
    for i in range(scores[0], MAX_SCORE):
        background[i] = (1, 0, 0)
    for i in range(scores[1], MAX_SCORE):
        background[-i-1] = (0, 0, 1)
    leds.fill_buf(background)


def blink(color, num=5):
    """Blink the whole strip num times"""
    for n in range(num):
        leds.show([color for i in range(SIZE)])
        for i in range(5):
            next(frames)
        leds.show(background)
        for i in range(5):
            next(frames)


def end(color):
    """Set color of middle of strip, and end the game"""
    set_background()
    for i in range(MAX_SCORE + 3, SIZE - MAX_SCORE - 3):
        background[i] = color
    leds.show(background)
    raise RuntimeError('Game Over')


set_background()

prev_switch = prev_pin = False

for f in frames:

    # Move the ball
    leds.update_buf([background[int(ball_pos)]], start=int(ball_pos))
    ball_pos += ball_velocity

    # Goal handling
    if ball_pos >= SIZE:
        ball_pos = SIZE - 1
        ball_velocity = -INITIAL_SPEED
        blink((1, 0, 0))
        set_background()
        scores[1] += 1
        if scores[1] > MAX_SCORE:
            end((1, 0, 0))
            break
    elif ball_pos < 0:
        ball_pos = 0
        ball_velocity = INITIAL_SPEED
        blink((0, 0, 1))
        set_background()
        scores[0] += 1
        if scores[0] > MAX_SCORE:
            end((0, 0, 1))
            break

    # Button handling
    now_pin = pin.value()
    now_switch = switch()
    if now_pin and not prev_pin:
        leds.update_buf([(0, 1, 0)], start=0)
        if ball_velocity < 0 and ball_pos < 9:
            ball_velocity = (MAX_SCORE - ball_pos) * 0.2
    else:
        leds.update_buf(background[:1], start=0)
    if now_switch and not prev_swich:
        leds.update_buf([(0, 1, 0)], start=SIZE-1)
        if ball_velocity > 0 and ball_pos > SIZE - 9:
            ball_velocity = (SIZE - ball_pos - MAX_SCORE) * 0.2
    else:
        leds.update_buf(background[-1:], start=SIZE-1)
    prev_pin = now_pin
    prev_swich = now_switch

    # Draw the buffer!
    leds.update_buf([(1, 1, 1)], start=int(ball_pos))
    leds.send_buf()
