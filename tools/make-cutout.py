#!/usr/bin/env python3
"""
FLN ANIMATION KIT - cut-out converter  (recipe 21, engine A)

Turns an OPAQUE object card - the 1024x1024 kind with a flat cream background that
the art pipeline produces - into a real alpha cut-out, so recipe 21 engine A can
outline it. Engine A derives its outline from the alpha channel; given an opaque
rectangle it faithfully outlines the rectangle, which is never what anyone wants.

Most object art in this fleet already has alpha and needs none of this. Check first:

    python make-cutout.py --check assets/Images/*.webp

Then convert only the ones that need it:

    python make-cutout.py obj_kela.webp -o obj_kela_cut.webp
    python make-cutout.py obj_*.webp --in-place --suffix _cut

How it works: the background colour is taken from the corners, then flooded inward
from the border. Only background CONNECTED TO THE EDGE is removed, so a white glass
or a cream wall inside the object keeps its pixels - a plain colour-key would punch
holes straight through them.

Needs Pillow:  pip install Pillow
"""
import argparse, glob, os, sys
from collections import deque

try:
    from PIL import Image, ImageFilter
except ImportError:
    sys.exit("needs Pillow:  pip install Pillow")


def bg_colour(px, w, h):
    """Median of the four corners - robust to one corner holding a stray pixel."""
    pts = []
    for x, y in ((2, 2), (w - 3, 2), (2, h - 3), (w - 3, h - 3)):
        pts.append(px[x, y][:3])
    pts.sort(key=lambda c: sum(c))
    return pts[len(pts) // 2]


def cut(im, tol, feather):
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    bg = bg_colour(px, w, h)

    # flood from every border pixel that still looks like the background
    seen = bytearray(w * h)
    q = deque()

    def near(c):
        return (abs(c[0] - bg[0]) + abs(c[1] - bg[1]) + abs(c[2] - bg[2])) <= tol * 3

    for x in range(w):
        for y in (0, h - 1):
            if not seen[y * w + x] and near(px[x, y]):
                seen[y * w + x] = 1; q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if not seen[y * w + x] and near(px[x, y]):
                seen[y * w + x] = 1; q.append((x, y))

    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and near(px[nx, ny]):
                seen[ny * w + nx] = 1
                q.append((nx, ny))

    mask = Image.new("L", (w, h), 255)
    mp = mask.load()
    n = 0
    for y in range(h):
        row = y * w
        for x in range(w):
            if seen[row + x]:
                mp[x, y] = 0; n += 1
    if feather:
        mask = mask.filter(ImageFilter.GaussianBlur(feather))
    im.putalpha(mask)
    return im, bg, 100.0 * n / (w * h)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("files", nargs="+", help="images to convert (globs ok)")
    p.add_argument("-o", "--out", help="output file (single input only)")
    p.add_argument("--suffix", default="_cut", help="suffix when converting many (default _cut)")
    p.add_argument("--tol", type=int, default=26, help="background colour tolerance (default 26)")
    p.add_argument("--feather", type=float, default=0.6, help="edge softness (default 0.6)")
    p.add_argument("--trim", action="store_true", help="crop to the object's bounding box")
    p.add_argument("--check", action="store_true", help="report only - convert nothing")
    a = p.parse_args()

    files = []
    for f in a.files:
        files += sorted(glob.glob(f)) or [f]

    need = 0
    for f in files:
        if not os.path.exists(f):
            print("  missing:", f); continue
        im = Image.open(f)
        if im.convert("RGBA").getchannel("A").getextrema()[0] == 0:
            if a.check: print("  ok, has alpha   :", os.path.basename(f))
            continue
        need += 1
        if a.check:
            print("  OPAQUE, needs cut:", os.path.basename(f), "%dx%d" % im.size)
            continue

        out, bg, pct = cut(im, a.tol, a.feather)
        if pct < 4:
            print("  ! %s: only %.1f%% removed - the background may not be flat, or the\n"
                  "    object reaches the edge. Check the result before shipping it."
                  % (os.path.basename(f), pct))
        if a.trim:
            b = out.getbbox()
            if b: out = out.crop(b)
        dst = a.out if (a.out and len(files) == 1) else \
            os.path.splitext(f)[0] + a.suffix + ".webp"
        out.save(dst, "WEBP", lossless=True, quality=100, method=6)
        print("  %-28s bg%s  %.1f%% removed -> %s (%d bytes)"
              % (os.path.basename(f), bg, pct, os.path.basename(dst), os.path.getsize(dst)))

    if a.check:
        print("\n%d of %d file(s) are opaque and need converting." % (need, len(files)))


if __name__ == "__main__":
    main()
