"""
expressions.py — a small preset library of eye expressions built on eye_lib.
Each function returns a finished PIL Image (mode '1', 128x64).
"""
from PIL import ImageDraw
from eye_lib import (
    LEFT_EYE, RIGHT_EYE, draw_rounded_eye, draw_circle_eye, apply_lid,
    render_expression, new_canvas,
)


def neutral():
    def L(draw, zone):
        draw_rounded_eye(draw, zone, open_amount=1.0)
    return render_expression(L)


def blink(open_amount=0.08):
    def L(draw, zone):
        draw_rounded_eye(draw, zone, open_amount=open_amount)
    return render_expression(L)


def happy():
    # top stays round, bottom gets cut into a big curve -> ^-shaped eye
    def L(draw, zone):
        draw_rounded_eye(draw, zone, open_amount=1.0)
        apply_lid(draw, zone, bottom_cut=0.55)
    return render_expression(L)


def sad():
    # outer corners cut low, inner corners high -> classic sad slant
    def L(draw, zone):
        draw_rounded_eye(draw, zone, open_amount=1.0)
        apply_lid(draw, zone, top_cut=0.35, slant=0.6)
    return render_expression(L)


def angry():
    def L(draw, zone):
        draw_rounded_eye(draw, zone, open_amount=1.0)
        apply_lid(draw, zone, top_cut=0.4, slant=-0.7)
    return render_expression(L)


def sleepy():
    def L(draw, zone):
        draw_rounded_eye(draw, zone, open_amount=0.35)
    return render_expression(L)


def surprised():
    def L(draw, zone):
        draw_circle_eye(draw, zone, open_amount=1.0)
    return render_expression(L)


def curious_look(direction="left"):
    # both eyes shift together toward one side, still symmetric shapes
    off = -8 if direction == "left" else 8

    def L(draw, zone):
        draw_rounded_eye(draw, zone, open_amount=0.9, x_offset=off)

    def R(draw, zone):
        draw_rounded_eye(draw, zone, open_amount=0.9, x_offset=off)

    return render_expression(L, right_fn=R, mirror=False)


def wink(side="left"):
    img = new_canvas()
    draw = ImageDraw.Draw(img)

    if side == "left":
        # Closed side is the left-zone eye as seen in the physical layout.
        # The open side must be the neutral right-eye shape, not a mirrored
        # or re-used left-zone function.
        draw_rounded_eye(draw, LEFT_EYE, open_amount=0.08)
        draw_rounded_eye(draw, RIGHT_EYE, open_amount=1.0)
    else:
        draw_rounded_eye(draw, LEFT_EYE, open_amount=1.0)
        draw_rounded_eye(draw, RIGHT_EYE, open_amount=0.08)

    return img


PRESETS = {
    "neutral": neutral,
    "blink": blink,
    "happy": happy,
    "sad": sad,
    "angry": angry,
    "sleepy": sleepy,
    "surprised": surprised,
    "look_left": lambda: curious_look("left"),
    "look_right": lambda: curious_look("right"),
    "wink_left": lambda: wink("left"),
    "wink_right": lambda: wink("right"),
}
