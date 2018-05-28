import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull
import time

brightness = 0.0
target = 0.5

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=brightness)
pixels.fill((255, 255, 255))

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

button_left = DigitalInOut(board.BUTTON_A)
button_left.direction = Direction.INPUT
button_left.pull = Pull.DOWN

button_right = DigitalInOut(board.BUTTON_B)
button_right.direction = Direction.INPUT
button_right.pull = Pull.DOWN

press = DigitalInOut(board.A1)
press.direction = Direction.INPUT
press.pull = Pull.UP

rotary_left = DigitalInOut(board.A2)
rotary_left.direction = Direction.INPUT
rotary_left.pull = Pull.DOWN

rotary_right = DigitalInOut(board.A3)
rotary_right.direction = Direction.INPUT
rotary_right.pull = Pull.DOWN

previous = (False, False)

while True:
    # An amount and direction of brightness change will be stored here
    vector = 0

    # Light up the red LED when any button is pressedself.
    # It's an easy way to see if the program is running on a board.
    led.value = button_left.value or button_right.value or not press.value

    # Read the rotary encoder state and detect direction of rotation
    # See https://en.wikipedia.org/wiki/Rotary_encoder#Incremental_rotary_encoder
    rotary = (not rotary_left.value, not rotary_right.value)

    if previous != rotary and previous == (False, False):
        if rotary[0]:
            # Turning counter-clockwise
            vector = -10
        else:
            # Turning clockwise
            vector = 10

    previous = rotary

    # The brightness is always "pulled" toward the target value
    diff = target - brightness
    vector = vector + (diff / 5)


    # Read on-board buttons and apply the input to the vector
    if button_left.value:
        # Decrease brightness
        vector = vector - 1

    if button_right.value:
        # Increase brightness
        vector = vector + 1


    # Change brightness according to the vector
    step = vector / 1000
    brightness = max(min(brightness + step, 1), 0)
    pixels.brightness = brightness
