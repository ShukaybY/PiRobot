"""
eye_lib.py — reusable eye-pattern toolkit for a 128x64 monochrome OLED
(e.g. SSD1306), designed and testable entirely on a Mac with Pillow.

Coordinate system matches the physical display: (0,0) top-left,
x increases right, y increases down.

Zones (yours):
    LEFT_EYE  = (10, 10, 60, 54)
    RIGHT_EYE = (68, 10, 118, 54)
    symmetric around x = 64
"""
from PIL import Image, ImageDraw, ImageChops

WIDTH, HEIGHT = 128, 64
LEFT_EYE = (10, 10, 60, 54)     # x0, y0, x1, y1
RIGHT_EYE = (68, 10, 118, 54)
CENTER_X = 64


def new_canvas():
    """Black 1-bit canvas, same shape as the physical display."""
    return Image.new("1", (WIDTH, HEIGHT), 0)


def zone_center(zone):
    x0, y0, x1, y1 = zone
    return ((x0 + x1) / 2, (y0 + y1) / 2)


def zone_size(zone):
    x0, y0, x1, y1 = zone
    return (x1 - x0, y1 - y0)


def draw_rounded_eye(draw, zone, open_amount=1.0, radius_ratio=0.35,
                      x_offset=0, y_offset=0, fill=1):
    """
    Classic rounded-rectangle 'robot eye'.
    open_amount: 0.05 (near-closed sliver) .. 1.0 (fully open)
    x_offset/y_offset: shift the eye within its zone (look direction),
                        in pixels, positive = right/down.
    """
    x0, y0, x1, y1 = zone
    w, h = zone_size(zone)
    cx, cy = zone_center(zone)

    open_amount = max(0.05, min(1.0, open_amount))
    eye_h = h * open_amount
    ey0 = cy - eye_h / 2 + y_offset
    ey1 = cy + eye_h / 2 + y_offset
    ex0 = x0 + x_offset
    ex1 = x1 + x_offset

    radius = min(w, eye_h) * radius_ratio
    draw.rounded_rectangle([ex0, ey0, ex1, ey1], radius=radius, fill=fill)


def draw_circle_eye(draw, zone, open_amount=1.0, x_offset=0, y_offset=0, fill=1):
    """Round eye — reads as cuter / more curious than the rounded-rect."""
    w, h = zone_size(zone)
    cx, cy = zone_center(zone)
    d = min(w, h) * max(0.05, open_amount)
    cx += x_offset
    cy += y_offset
    draw.ellipse([cx - d / 2, cy - d / 2, cx + d / 2, cy + d / 2], fill=fill)


def apply_lid(draw, zone, top_cut=0.0, bottom_cut=0.0, slant=0.0):
    """
    Erase (fill=0) a wedge from the top and/or bottom of an already-drawn
    eye — this is how you get angry / sad / sleepy looks on top of a
    rounded rect or circle.
    top_cut/bottom_cut: 0..1 fraction of zone height to remove.
    slant: -1..1, tilts the cut line (negative = higher on the left side
           of the zone).
    """
    x0, y0, x1, y1 = zone
    w, h = zone_size(zone)
    if top_cut > 0:
        skew = slant * w / 2
        draw.polygon([
            (x0, y0), (x1, y0),
            (x1, y0 + h * top_cut - skew), (x0, y0 + h * top_cut + skew)
        ], fill=0)
    if bottom_cut > 0:
        skew = slant * w / 2
        draw.polygon([
            (x0, y1 - h * bottom_cut + skew), (x1, y1 - h * bottom_cut - skew),
            (x1, y1), (x0, y1)
        ], fill=0)


def render_expression(left_fn, right_fn=None, mirror=True):
    """
    left_fn(draw, zone) draws the left eye onto LEFT_EYE.
    - If right_fn is given, it's called with RIGHT_EYE as-is (use this
      for winks / asymmetric expressions).
    - Else if mirror=True (default), the left eye is flipped across
      x=64 to build the right eye automatically — guarantees perfect
      symmetry for free.
    """
    img = new_canvas()
    draw = ImageDraw.Draw(img)
    left_fn(draw, LEFT_EYE)

    if right_fn is not None:
        right_fn(draw, RIGHT_EYE)
    elif mirror:
        tmp = new_canvas()
        ImageDraw.Draw(tmp).__class__  # no-op, keeps linters quiet
        tdraw = ImageDraw.Draw(tmp)
        left_fn(tdraw, LEFT_EYE)
        flipped = tmp.transpose(Image.FLIP_LEFT_RIGHT)
        img = ImageChops.logical_or(img, flipped)
    return img


def scaled_preview(img, scale=8, grid_zones=None):
    """
    Upscale with nearest-neighbor so a 128x64 image is actually readable
    on a laptop screen. Optionally overlay zone rectangles for calibration.
    """
    big = img.convert("RGB").resize((WIDTH * scale, HEIGHT * scale), Image.NEAREST)
    if grid_zones:
        d = ImageDraw.Draw(big)
        for z in grid_zones:
            x0, y0, x1, y1 = [v * scale for v in z]
            d.rectangle([x0, y0, x1, y1], outline=(255, 0, 0), width=1)
    return big
