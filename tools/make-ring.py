#!/usr/bin/env python3
"""
FLN ANIMATION KIT - ring band generator  (recipe 21, engine B)

Makes the outline asset for an object that is BAKED INTO a scene raster and so
cannot be outlined at runtime. Engine A (a sprite with its own alpha) needs none
of this - the browser derives that outline from the alpha and --ol-w sets the
thickness live.

The ring is COMPUTED from a silhouette, never hand-traced. Hand-tracing is why the
untidy outline kept coming back in HI01H01_L02_S04.

    # from a cut-out sprite (its alpha IS the silhouette)
    python make-ring.py --from-sprite tota.webp --w 1280 --h 724 \
                        --at 120,380 --scale 0.42 -o ring_tota_band.webp

    # from a hand-painted mask: white/opaque = the object, anything else = not
    python make-ring.py --from-mask tota_mask.png -o ring_tota_band.webp

    # print the CSS ready to paste (base64 - see WHY below)
    python make-ring.py --from-mask m.png -o r.webp --css --var --ol-band

Output is a full-frame RGBA WebP the same size as the scene, transparent except
for the ring. Because it is ~99% transparent it compresses to well under 1KB, so
inlining it as base64 costs almost nothing.

WHY BASE64, NOT A FILE PATH: a CSS mask/url() is fetched under CORS rules, and a
page loaded from file:// has origin "null", so a path is BLOCKED - in exactly the
Android WebView the activities ship in. <img src> is unaffected; masks are not.
Pass --css to get a paste-ready data: URI.

Needs Pillow:  pip install Pillow
"""
import argparse, base64, io, os, sys

try:
    from PIL import Image, ImageFilter, ImageChops
except ImportError:
    sys.exit("needs Pillow:  pip install Pillow")


def silhouette_from_sprite(path, canvas, at, scale):
    """Alpha of a cut-out sprite, pasted onto a scene-sized transparent canvas."""
    im = Image.open(path).convert("RGBA")
    if im.getchannel("A").getextrema()[0] == 255:
        sys.exit("%s is fully opaque - it has no alpha to trace. Either cut it out\n"
                 "first, or use --from-mask with a painted silhouette." % os.path.basename(path))
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))),
                       Image.LANCZOS)
    sil = Image.new("L", canvas, 0)
    sil.paste(im.getchannel("A"), at)
    return sil


def silhouette_from_mask(path, canvas):
    """Any image: opaque-and-light = object. Alpha wins if the file has one."""
    im = Image.open(path)
    if im.mode in ("RGBA", "LA") and im.convert("RGBA").getchannel("A").getextrema()[0] < 255:
        sil = im.convert("RGBA").getchannel("A")
    else:
        sil = im.convert("L")
    if canvas and sil.size != canvas:
        sil = sil.resize(canvas, Image.LANCZOS)
    return sil


def ring(sil, width, feather, inset):
    """
    Ring = dilate(sil, out) MINUS erode(sil, in).

    Morphology, not an edge filter. An edge filter gives a line whose thickness
    follows the local gradient, so it thins out wherever the art is soft - the
    outline then looks broken along exactly the fuzzy edges (hair, fur, leaves)
    where it is needed most.
    """
    sil = sil.point(lambda v: 255 if v > 128 else 0)          # harden first
    out = max(1, width - inset)
    grow = sil.filter(ImageFilter.MaxFilter(out * 2 + 1)) if out else sil
    shrink = sil.filter(ImageFilter.MinFilter(inset * 2 + 1)) if inset else sil
    band = ImageChops.subtract(grow, shrink)
    if feather:
        band = band.filter(ImageFilter.GaussianBlur(feather))
    return band


def main():
    p = argparse.ArgumentParser(add_help=True)
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--from-sprite", metavar="FILE", help="cut-out sprite; its alpha is the shape")
    src.add_argument("--from-mask", metavar="FILE", help="painted silhouette; light/opaque = object")
    p.add_argument("-o", "--out", required=True, help="output .webp")
    p.add_argument("--w", type=int, help="scene width  (default: the mask's)")
    p.add_argument("--h", type=int, help="scene height (default: the mask's)")
    p.add_argument("--at", default="0,0", help="x,y to paste a sprite at (--from-sprite)")
    p.add_argument("--scale", type=float, default=1.0, help="scale the sprite before pasting")
    p.add_argument("--width", type=int, default=6, help="ring thickness in px (default 6)")
    p.add_argument("--inset", type=int, default=1,
                   help="px of the ring that sits INSIDE the shape (default 1) - a ring "
                        "entirely outside reads as detached on a busy scene")
    p.add_argument("--feather", type=float, default=0.6, help="edge softness (default 0.6)")
    p.add_argument("--css", action="store_true", help="also print a paste-ready data: URI")
    p.add_argument("--var", default="--ol-band", help="custom property name for --css")
    a = p.parse_args()

    if a.from_sprite:
        if not (a.w and a.h):
            sys.exit("--from-sprite needs --w and --h (the SCENE size, so the band lines up)")
        canvas = (a.w, a.h)
        at = tuple(int(v) for v in a.at.split(","))
        sil = silhouette_from_sprite(a.from_sprite, canvas, at, a.scale)
    else:
        canvas = (a.w, a.h) if (a.w and a.h) else None
        sil = silhouette_from_mask(a.from_mask, canvas)

    band = ring(sil, a.width, a.feather, a.inset)
    if band.getextrema()[1] == 0:
        sys.exit("the ring came out empty - check the silhouette actually has content")

    # White pixels through the alpha: the CSS paints its own colour through this
    # mask, so ONE asset serves idle, correct, wrong and muted.
    out = Image.merge("RGBA", (Image.new("L", band.size, 255),) * 3 + (band,))
    out.save(a.out, "WEBP", lossless=True, quality=100, method=6)

    n = os.path.getsize(a.out)
    ink = 100.0 * sum(i * c for i, c in enumerate(band.histogram())) / (255.0 * band.size[0] * band.size[1])
    print("%s  %dx%d  %d bytes  ink %.2f%%" % (a.out, out.width, out.height, n, ink))
    if n > 8192:
        print("  ! larger than 8KB - unusual for a ring. Is the silhouette solid rather\n"
              "    than an outline? Check --width and the input mask.")
    if a.css:
        b64 = base64.b64encode(io.open(a.out, "rb").read()).decode()
        print("\n%s:url('data:image/webp;base64,%s');" % (a.var, b64))


if __name__ == "__main__":
    main()
