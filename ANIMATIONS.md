# FLN Animation Kit

Every reusable animation in the FLN fleet, in one place: the effects, how to install
them, and the reasoning behind each one. This is the only document - `index.html`
is the only other thing you need to open.

```
fln-animation-kit/
  ANIMATIONS.md    this file - effects, install steps, gotchas, the keyframe catalogue
  index.html       open it: all seven effects running, with sound and old-vs-new
  assets/          art the preview borrows from the activities
  sfx/             the sound files, and where they came from
  tools/           two scripts, needed only for recipe 21 on awkward art
```

**Live preview:** https://claude.ai/code/artifact/f8c434a5-fc40-49c9-a4ea-9d6f5df9227d

**Using one:** open the preview, pick the effect, find its recipe below, read its
**Gotchas**, then follow **Installing an effect** at the end of this file.

---

## Before you paste anything

**One caveat on the preview:** the sky tile renders in px, not `vmax`, so its density and
speed are not faithful at tile size. Every other effect in the preview is true to life.


Four things cause almost every bug in this codebase:

- **Later rules win.** Stylesheets are append-only patch stacks. `#nudgeHand` is declared 3x,
  `.phase-gate` 7x, `audioPulse` 14x. Grep *every* rule for a selector before reusing pixel offsets.
- **Some effects are already there but dead.** A blanket `animation:none !important` kills the mascot
  bob and button pulses in MTKGA01/MTKGA02. A rule existing does not mean it runs.
- **Assets do not ship everywhere.** Check the target folder directly, never a sibling.
- **Two engine generations.** Split-file activities take CSS/JS in separate files; `_dist` activities
  are single-file build outputs where everything goes inline.

## Status

| Effect | State |
|---|---|
| 1. Start screen stars (drift) | Installed, shipping |
| 2. Start screen stars (tap to burst) | Installed, shipping |
| 3. Nudge hand press | Built, in the preview; not installed |
| 4. Nudge hand tap ripple | Built, in the preview; not installed |
| 7. Correct answer confetti | **Rebuilt** - replaces the shipped version; in the preview, not installed |
| 8. Celebration star burst | **Retuned** - fewer stars, slower; in the preview, not installed |
| 19. Correct answer select | **Built** - supersedes recipe 9; in the preview, not installed |
| 20. Wrong answer select | **Built** - supersedes recipe 11; in the preview, not installed |
| 21. Tap the object (any shape) | **Built** - generalises recipe 10; in the preview, not installed |
| 22. Sound | **Built** - 7 synthesised cues shared by every effect; in the preview, not installed |
| 5-6, 9-18 | Documented from existing code; not yet rolled out as a deliberate pass |

The kit code is **not byte-identical to what ships** - it fixes five known defects, listed under
*Deviations* in `ANIMATIONS.md`. A diff against a live activity will differ, by design.

## The answer-feedback pair

Recipes **19 (correct select)** and **20 (wrong select)** are the two effects a child sees most
often in a session, and they are designed as a set:

- both put the mark on the tile's **border**, never a fill - no green flood, no tick, no cross
- both keep the tile's own word or digit fully legible, including once eliminated
- correct **persists** (it is the answer); wrong **releases** (there is another attempt)
- both survive the reduced-motion kill-switch with the mark intact and the decoration gone

Recipe 19 is the tile-level confirm and recipe 7 (confetti) is the room-level celebration -
they are meant to run together, not as alternatives. Install 19 and 20 in the same pass or the
two halves of the feedback will not match.

**Both run off one tempo**, so they cannot drift apart:

```css
:root{ --fx-beat:.4s;    /* the shipped buzzShake tempo - wrong runs exactly one beat */
       --fx-reward:2; }  /* correct runs this many beats */
```

Nothing else carries a duration - the JS reads these two numbers from CSS rather than keeping
its own copy. If the correct answer feels too fast or too slow, change `--fx-reward` and only
the reward stretches; change `--fx-beat` and the whole pair retimes together.

## Outlining objects that are all different shapes

Recipe **21** is the look-and-find / "tap the right thing" case: white outline at rest,
red and a wiggle when wrong, green when correct - on a girl, a parrot, a banana, a
cupboard, without a traced path for any of them. Two engines, one set of state classes:

- **`.ol-alpha`** - the object is its own element with real transparency. The browser
  derives the outline from its alpha. **No per-object asset**, thickness is a live
  variable, and the outline follows automatically when the art is re-exported. Use this
  unless you cannot. Verified on 18 unrelated objects - people, buildings, a football, a
  microphone, a teacup - with the same two classes and no per-object work. If a file is
  an opaque card rather than a cut-out (22 of 175 in this fleet), run
  [`tools/make-cutout.py`](tools/make-cutout.py) over it once.
- **`.ol-band`** (documented, no preview tile) - the object is a region of a baked scene
  raster and cannot be moved or filtered on its own. Ships one ~1KB ring band per object, generated by
  [`tools/make-ring.py`](tools/make-ring.py), painted through a mask so one asset serves all four
  states.

Two things bite here, both documented in the recipe: a CSS mask **cannot** load from a
file path on `file://` (inline it as base64), and a band must **never** be transformed
or the ring slides off the art it is tracing.

**Engine B is not optional here.** `HIKGH01_L02_S03` currently ships a duplicate of each
scene with the outlines painted in - 254KB of `_tap` rasters to do what 5KB of ring
bands do, and in white only, all-or-nothing. Engine A would replace all of it, but only
once the art pipeline can hand over a character-free background plate; today every scene
has its cast baked in.

## Sound

Recipe **22** adds seven cues - correct, wrong, pick, confetti, celebrate, star-pop, tick -
shared by every effect, and they are **real recordings**, not synthesis. Three rounds of
synthesised cues were rejected as machine-like before that lesson landed.

`sfx/` holds CC0 files from [Kenney](https://kenney.nl) (public domain, no attribution
required); the end screen keeps the fleet's own `sfx_celebrate.ogg`. They were picked by
**measuring** candidates - warmth, tonality, attack, and pitch direction - not by filename.
The brightest steel-drum jingle was rejected because it *falls* 7.8 semitones: it is a lose
stinger, and by name there was no way to tell.

Swap in your own audio with one line: `FLNMotion.sfx.files.correct = "…"`. Sound plays only
on a deliberate action - nothing on page load - and each card header has a speaker that mutes
that card alone.

## Scope

The kit does **not** consolidate the seven duplicate copies of these effects into a shared library,
and does not modify any activity folder. Both are separate, larger decisions.

---

Every animation in the FLN fleet, in one place. 147 keyframes, 7 activities, no shared library.

**See the installed effects:** open [`index.html`](index.html) - recipes 1 and 2.
**Judge / tune the sky effect:** open the preview full-screen - real
`vmax` CSS, real stage scaling, live controls, fps meter.
Recipes 3-18 are marked **Reference only** - documented from existing code, not installed, no
preview tile.
**Installing one:** use **Installing an effect**.
**Sharing this:** see the top of this file.

**Status:** Recipe 1 + 2 (sky drift + tap burst) are installed and shipping. Recipes 7, 8, 19,
20, 21 and 22 are built and in the preview, not yet installed. The rest are documented from existing
code, not yet rolled out as a deliberate pass.

---

## Rules - read once

| # | Rule |
|---|---|
| R1 | Stage is a fixed **1333x750** box scaled by `--scale`. Design px inside it, `vmax` for full-viewport layers. Never use raw `getBoundingClientRect()` deltas - divide by `--scale`. |
| R2 | Portrait **rotates** the stage 90°, it does not letterbox. Fixed overlays must mirror `html.rotated`. |
| R3 | Classic `<script>` only. No ES modules - they break `file://` and the single-file `_dist` build. |
| R4 | Never let an error strand `#bootLoader`. Wrap every `init()` in `try/catch`. |
| R5 | Reduced motion needs **both** halves: the CSS kill-switch and a JS guard. Only 1 of 7 activities has both today. |
| R6 | Touch listeners must be `{passive:false}`. A capture-phase multi-touch killer runs upstream (Android WebView ignores `user-scalable=no`). |
| R7 | Keyframes camelCase + family prefix; classes kebab-case + same prefix. `popUp`, `fadeIn`, `slideIn`, `shake`, `confettiFall` are **already taken everywhere**. |
| R8 | Use existing tokens with fallbacks: `var(--correct, #00B132)`, `--wrong`, `--selected`, `--navy`, `--font-hi`. |
| R9 | New asset = new entry in `ASSET_BYTES` (a byte-**size** map, not base64). |
| R10 | Never edit `ENGINE_VERSION`. `verify_bundle.py` hard-fails on divergence. |
| R11 | CSS must not rely on source order. **Grep every rule touching a selector before reusing px offsets** - `#nudgeHand` is declared 3x, `.phase-gate` 7x, `audioPulse` 14x. |

### Paste these once per activity

```css
/* ===== FLN ANIMATION KIT: reduced-motion BEGIN ===== */
html.no-anim *, html.no-anim *::before, html.no-anim *::after{
  animation:none!important; transition:none!important;
}
@media (prefers-reduced-motion: reduce){
  *, *::before, *::after{ animation:none!important; transition:none!important; }
}
/* ===== FLN ANIMATION KIT: reduced-motion END ===== */
```

```js
/* ===== FLN ANIMATION KIT: core BEGIN ===== */
(function(){ "use strict";
  var M = window.FLNMotion = window.FLNMotion || {};
  M.still = function(){
    try{ return document.documentElement.classList.contains("no-anim") ||
      (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches); }
    catch(_){ return false; }
  };
  M.scale = function(){
    try{ return parseFloat(getComputedStyle(document.documentElement)
      .getPropertyValue("--scale")) || 1; }catch(_){ return 1; }
  };
  M.rect = function(r, sw){                    // screen rect -> stage coords (R1/R2)
    var s = M.scale();
    if(document.documentElement.classList.contains("rotated")){
      return { left:(r.top - sw.top)/s, top:(sw.right - r.right)/s, w:r.height/s, h:r.width/s };
    }
    return { left:(r.left - sw.left)/s, top:(r.top - sw.top)/s, w:r.width/s, h:r.height/s };
  };
  M.guard = function(fn){                      // R4
    try{ fn(); }catch(e){ try{ console.warn("[animation-kit]", e && e.message); }catch(_){} }
  };
  var _actx = null;
  M.audio = function(){
    try{
      var AC = window.AudioContext || window.webkitAudioContext; if(!AC) return null;
      _actx = _actx || new AC();
      if(_actx.state === "suspended") _actx.resume();
      return _actx;
    }catch(_){ return null; }
  };
  M.ready = function(fn){
    if(document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  };
})();
/* ===== FLN ANIMATION KIT: core END ===== */
```

---

## The fleet

| Folder | Layout | Gen |
|---|---|---|
| `HI01H02_L01_S01_dist/` | single-file HTML, `SwiftPAL` is the bus | 1 |
| `HI01H01_L02_S04_dist/` | single-file HTML, `GameBus` + inlined bridge | 2 |
| `MTKGA01_L01_S01/` | split files, no bridge | 3 early |
| `HI01H05_L02_S01/` | split + slim bridge | 3 |
| `MTKGA01_L01_S03_DELIVERY (2)/` | split + slim bridge | 3 late |
| `MTKGA02_L01_S01/` | split + slim bridge | 3 late |
| `HIKGH03_..._Sanket_Board_Pehchano/` | split + `preloader.js` + full bridge | 4 |

- Split files: CSS → end of `style.css`, JS → end of `app.js`, markup → `index.html`.
- `_dist` files: everything goes inside the single `<style>` / `<script>` block. These are build
  outputs; editing them is a patch, not a fix.

### What each activity already has in its code

| Effect | H01H01 | H01H02 | H01H05 | MTK01S01 | MTK01S03 | MTK02 | HIKGH03 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Sky drift + burst | yes | yes | yes | yes | yes | yes | yes |
| Nudge press | - | - | yes | yes | yes | yes | yes |
| Nudge tap-ripple | - | - | demo | yes | ball | yes | - |
| Mascot star-from-circle | yes | yes | yes | yes | yes | yes | - |
| Confetti | yes | yes | yes | yes | yes | yes | yes |
| Canvas starBurst | yes | yes | yes | yes | yes | yes | yes |
| Outline-only correct | yes | - | - | - | yes | yes | - |
| Contour-ring outline | yes | - | - | - | - | - | - |
| Phase gate | yes | yes | yes | yes | yes | yes | yes |
| Block Town | yes | yes | - | yes | yes | yes | - |
| Ambient wind/sway | - | - | yes | - | yes | yes | - |

---

# Recipes

---

## 1. Start screen stars (drift)

**▶ Preview:** `index.html#sky-drift` (one card shows both) · **Installed: yes**

Stars, twinkles, rings and dots fly straight out from screen centre, fade in past the card, exit the
frame, restart from the middle.

| | |
|---|---|
| Source | `MTKGA01_L01_S03_DELIVERY (2)/style.css:3385-3485` |
| Assets | `bgdeco_star.svg`, `bgdeco_star_o.svg`, `bgdeco_spark.svg`, **`startnew_bg_plain.webp`** |
| Needs | `--scale` on `<html>`, `body.is-start`/`is-end`, `html.rotated` |
| Rules | R1, R2, R5 |

> **Must do first:** swap `.start-bg` to `startnew_bg_plain.webp`. The decorations are painted into
> `startnew_bg.webp`. Skip this and you get two sets of stars - one frozen, one moving.

```css
/* ===== FLN ANIMATION KIT: sky-drift BEGIN ===== */
.start-bg{background-image:url("assets/UI/startnew_bg_plain.webp");}   /* mandatory */

.sg-glow,.sg-sky{position:fixed;inset:0;pointer-events:none;display:none;z-index:1;}
body.is-start .sg-glow,body.is-start .sg-sky,
body.is-end   .sg-glow,body.is-end   .sg-sky{display:block;}
html.rotated .sg-glow,html.rotated .sg-sky{                            /* R2 */
  inset:auto;left:50%;top:50%;width:100vh;height:100vw;
  transform:translate(-50%,-50%) rotate(90deg);}

.sg-glow{opacity:.75;background:radial-gradient(ellipse 38% 25% at 50% 79%,
  rgba(255,255,255,.34) 0%,rgba(255,255,255,.13) 45%,rgba(255,255,255,0) 72%);
  animation:sgBreathe 6.5s ease-in-out infinite;}
@keyframes sgBreathe{0%,100%{opacity:.55;}50%{opacity:1;}}

/* hole punched over the centre card - it is translucent, so elements showed through.
   1114x456 design px, tracked by --scale. Hard edge: a real occlusion boundary. */
.sg-sky{overflow:hidden;
  --sg-hole-w:calc(1074px * var(--scale,1));   /* 40px inside the card's rounded corners */
  --sg-hole-h:calc(416px * var(--scale,1));
  -webkit-mask-image:linear-gradient(#000,#000),linear-gradient(#000,#000);
          mask-image:linear-gradient(#000,#000),linear-gradient(#000,#000);
  -webkit-mask-size:100% 100%,var(--sg-hole-w) var(--sg-hole-h);
          mask-size:100% 100%,var(--sg-hole-w) var(--sg-hole-h);
  -webkit-mask-position:center,center; mask-position:center,center;
  -webkit-mask-repeat:no-repeat,no-repeat; mask-repeat:no-repeat,no-repeat;
  -webkit-mask-composite:xor; mask-composite:exclude;
}
/* end screen has no visible occluder, so a hard edge reads as a sliced crescent.
   Soft radial hole sized to the mascot instead. */
body.is-end .sg-sky{
  --sg-hole-w:calc(800px * var(--scale,1));
  --sg-hole-h:calc(800px * var(--scale,1));
  -webkit-mask-image:linear-gradient(#000,#000),
                     radial-gradient(closest-side,#000 71%,rgba(0,0,0,0) 100%);
          mask-image:linear-gradient(#000,#000),
                     radial-gradient(closest-side,#000 71%,rgba(0,0,0,0) 100%);
}

.sg-sky i{position:absolute;left:50%;top:50%;width:var(--s);aspect-ratio:1;
  margin:calc(var(--s) / -2) 0 0 calc(var(--s) / -2);
  background:center/contain no-repeat;opacity:0;
  animation:sgFly var(--t) linear infinite;animation-delay:var(--d);}
.sg-sky .s1{background-image:url("assets/UI/bgdeco_star.svg");}
.sg-sky .s2{background-image:url("assets/UI/bgdeco_star_o.svg");}
.sg-sky .s3{background-image:url("assets/UI/bgdeco_spark.svg");}
.sg-sky .s4{border-radius:50%;border:.22vmax solid rgba(255,255,255,.92);}
.sg-sky .s5{border-radius:50%;background:rgba(255,255,255,.92);}

/* transform keyed ONLY at 0% and 100% - that is what makes the path a straight ray */
@keyframes sgFly{
  0%{transform:translate(var(--x1),var(--y1));opacity:0;}
  10%{opacity:var(--o);}
  84%{opacity:var(--o);}
  100%{transform:translate(var(--x2),var(--y2));opacity:0;}
}

/* glow: static shadow, animated opacity = composited. See Deviations. */
.sg-sky i::after{content:"";position:absolute;inset:0;border-radius:inherit;
  background:inherit;border:inherit;
  filter:drop-shadow(0 0 7px rgba(255,255,255,.95));
  opacity:0;will-change:opacity;
  animation:sgGlowOpacity var(--g) ease-in-out infinite alternate;
  animation-delay:var(--gd);}
@keyframes sgGlowOpacity{from{opacity:0;}to{opacity:1;}}
/* ===== FLN ANIMATION KIT: sky-drift END ===== */
```

```html
<div class="start-bg" aria-hidden="true"></div>
<div class="sg-glow"  aria-hidden="true"></div>
<div class="sg-sky"   aria-hidden="true"></div>
<div class="end-bg"   aria-hidden="true"></div>
```

```js
/* ===== FLN ANIMATION KIT: sky-drift BEGIN ===== */
(function(){ "use strict";
  var M = window.FLNMotion;

  function build(o){
    var sky = typeof o.container === "string" ? document.querySelector(o.container) : o.container;
    if(!sky) return null;
    sky.textContent = "";
    var maxSize = 0, frag = document.createDocumentFragment();

    o.layers.forEach(function(L, li){
      for(var i = 0; i < o.lanes; i++){
        var a = ((360 / o.lanes) * i + L.rot) * Math.PI / 180;
        var cos = Math.cos(a), sin = Math.sin(a);
        var size = +((o.size[0] + Math.random() * (o.size[1] - o.size[0])) * L.scale).toFixed(2);
        if(size > maxSize) maxSize = size;
        var dur = +(o.dur[0] + Math.random() * (o.dur[1] - o.dur[0])).toFixed(1);
        var el = document.createElement("i");
        el.className = o.shapes[(i + li) % o.shapes.length];
        el.style.cssText =
          "--s:"  + size + "vmax;" +
          "--x1:" + (o.r0 * cos).toFixed(2) + "vmax;--y1:" + (o.r0 * sin).toFixed(2) + "vmax;" +
          "--x2:" + (o.r1 * cos).toFixed(2) + "vmax;--y2:" + (o.r1 * sin).toFixed(2) + "vmax;" +
          "--t:"  + dur + "s;" +
          "--d:-" + (Math.random() * dur).toFixed(1) + "s;" +     // negative = de-sync
          "--g:"  + (o.glow[0] + Math.random() * (o.glow[1] - o.glow[0])).toFixed(1) + "s;" +
          "--gd:-" + (Math.random() * 4).toFixed(1) + "s;" +
          "--o:"  + (o.opacity[0] + Math.random() * (o.opacity[1] - o.opacity[0])).toFixed(2) + ";";
        frag.appendChild(el);
      }
    });
    sky.appendChild(frag);

    // collision proof: lane arc at the tightest radius must be >= 1.5x the largest element
    var arc = (2 * Math.PI * o.r0) / o.lanes, ok = arc >= maxSize * 1.5;
    if(!ok && o.warn !== false){
      console.warn("[animation-kit] sky lanes too tight: arc " + arc.toFixed(2) +
        "vmax vs element " + maxSize.toFixed(2) + "vmax. Reduce lanes or size.");
    }
    return { arc:arc, maxSize:maxSize, safe:ok, count:sky.children.length };
  }

  M.sky = {
    defaults: {
      container:".sg-sky", lanes:29,
      layers:[{rot:0,scale:1},{rot:6.2,scale:0.62},{rot:-6.2,scale:0.55}],
      r0:22, r1:72, size:[0.8,2.6], dur:[18,34], glow:[3.0,4.8],
      opacity:[0.62,0.92], shapes:["s1","s2","s3","s4","s5"], warn:true
    },
    init: function(opts){
      var o = Object.assign({}, this.defaults, opts || {}), res = null;
      M.guard(function(){ res = build(o); });
      return res;
    }
  };
  M.ready(function(){ M.guard(function(){ if(!window.__skyManual) M.sky.init(); }); });
})();
/* ===== FLN ANIMATION KIT: sky-drift END ===== */
```

**Options**

| Key | Default | Effect |
|---|---|---|
| `container` | `".sg-sky"` | Layer to fill. Cleared first. |
| `lanes` | `29` | Elements per layer. More = tighter arc; watch the console warning. |
| `layers` | 3 | `{rot, scale}` each - same lanes rotated and shrunk. |
| `r0` / `r1` | `22` / `72` | Spawn / exit radius in vmax. `r0` must stay behind the card. |
| `size` | `[0.8, 2.6]` | vmax, before layer scale. |
| `dur` | `[18, 34]` | Lap seconds. |
| `glow` | `[3.0, 4.8]` | Twinkle cycle. Keep shorter than the lap. |
| `opacity` | `[0.62, 0.92]` | Peak opacity. |
| `shapes` | all 5 | `s1` star, `s2` outline star, `s3` spark, `s4` ring, `s5` dot. |
| `warn` | `true` | Console-warn if lanes are too tight. |

Returns `{arc, maxSize, safe, count}`.

**Why lanes, not random** - random placement clumps and collides. Evenly spaced lanes make overlap
impossible, and the guarantee is checkable.

**Why `vmax`** - it tracks the layer width in both orientations. A `vmax` layer **cannot be tested
in a small preview pane**; verify full-screen.

**Why negative `--d`** - CSS animations start at page load. A random negative delay scatters
elements along their laps so the field looks established, not launched all at once.

**Gotchas**
- Doubled stars → you skipped the `_plain` background swap.
- Nothing renders → `body.is-start` / `is-end` never set.
- Hole drifts → `--scale` not set on `<html>`.
- Detaches in portrait → you dropped the `html.rotated` rule.
- Each kit ships its own `startnew_bg.webp` (different md5s). `_plain` is a drop-in for all of them.

**Deviations**
- Runtime generator replaces 87 static `<i>` elements. Set `window.__skyManual = true` to paste
  static markup instead.
- `sgGlow` (animated `filter`) → `sgGlowOpacity` (animated opacity on a pseudo-element). The
  original animates `drop-shadow` on 87 elements at once - uncomposited, repaints every frame.
  **Verify full-screen on a real device**; original is in the catalogue.

**Assets** - full SVG source, so no binary copying:

```svg
<!-- assets/UI/bgdeco_star.svg -->
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><path d="M32 5.5c1.6 0 3 .9 3.7 2.4l6.1 12.4 13.7 2c1.6.2 3 1.4 3.5 3s.1 3.3-1.1 4.4l-9.9 9.6 2.3 13.6c.3 1.6-.4 3.3-1.7 4.2s-3.1 1.1-4.6.3L32 51l-12.2 6.4c-1.5.8-3.2.7-4.6-.3s-2-2.6-1.7-4.2l2.3-13.6-9.9-9.6c-1.2-1.1-1.6-2.9-1.1-4.4s1.9-2.7 3.5-3l13.7-2 6.1-12.4C29 6.4 30.4 5.5 32 5.5z" fill="#fff"/></svg>

<!-- assets/UI/bgdeco_star_o.svg -->
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><path d="M32 5.5c1.6 0 3 .9 3.7 2.4l6.1 12.4 13.7 2c1.6.2 3 1.4 3.5 3s.1 3.3-1.1 4.4l-9.9 9.6 2.3 13.6c.3 1.6-.4 3.3-1.7 4.2s-3.1 1.1-4.6.3L32 51l-12.2 6.4c-1.5.8-3.2.7-4.6-.3s-2-2.6-1.7-4.2l2.3-13.6-9.9-9.6c-1.2-1.1-1.6-2.9-1.1-4.4s1.9-2.7 3.5-3l13.7-2 6.1-12.4C29 6.4 30.4 5.5 32 5.5z" fill="none" stroke="#fff" stroke-width="4.5" stroke-linejoin="round"/></svg>

<!-- assets/UI/bgdeco_spark.svg -->
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><path d="M32 2c1.6 12.6 15.4 26.4 30 30-14.6 3.6-28.4 17.4-30 30-1.6-12.6-15.4-26.4-30-30C16.6 28.4 30.4 14.6 32 2z" fill="#fff"/></svg>
```

---

## 2. Start screen stars (tap to burst)

**▶ Preview:** `index.html#sky-drift` (one card shows both) · **Installed: yes**

Tap a drifting element: white-blue flash, then 16 particles of **the same shape** in 6 hues, arcing
out under gravity, with a synthesised pop. The element returns on its next lap.

| | |
|---|---|
| Source | `MTKGA01_L01_S03_DELIVERY (2)/app.js:5284-5402` (byte-identical in all 7) |
| Assets | none - shapes are inline `data:` URI masks |
| Needs | Recipe 1 installed |
| Rules | R4, R5, R6 |

```css
/* ===== FLN ANIMATION KIT: sky-burst BEGIN ===== */
.sg-sky i.popped{visibility:hidden;}
.sg-burst{position:fixed;z-index:95;width:0;height:0;pointer-events:none;}

/* data URIs, not file refs - external SVG masks are blocked under file:// */
.sg-burst.k-star{--shape:url("data:image/svg+xml,%3Csvg%20width=%2264%22%20height=%2264%22%20viewBox=%220%200%2064%2064%22%20xmlns=%22http://www.w3.org/2000/svg%22%3E%3Cpath%20d=%22M32%205.5c1.6%200%203%20.9%203.7%202.4l6.1%2012.4%2013.7%202c1.6.2%203%201.4%203.5%203s.1%203.3-1.1%204.4l-9.9%209.6%202.3%2013.6c.3%201.6-.4%203.3-1.7%204.2s-3.1%201.1-4.6.3L32%2051l-12.2%206.4c-1.5.8-3.2.7-4.6-.3s-2-2.6-1.7-4.2l2.3-13.6-9.9-9.6c-1.2-1.1-1.6-2.9-1.1-4.4s1.9-2.7%203.5-3l13.7-2%206.1-12.4C29%206.4%2030.4%205.5%2032%205.5z%22%20fill=%22%23fff%22/%3E%3C/svg%3E");}
.sg-burst.k-spark{--shape:url("data:image/svg+xml,%3Csvg%20width=%2264%22%20height=%2264%22%20viewBox=%220%200%2064%2064%22%20xmlns=%22http://www.w3.org/2000/svg%22%3E%3Cpath%20d=%22M32%202c1.6%2012.6%2015.4%2026.4%2030%2030-14.6%203.6-28.4%2017.4-30%2030-1.6-12.6-15.4-26.4-30-30C16.6%2028.4%2030.4%2014.6%2032%202z%22%20fill=%22%23fff%22/%3E%3C/svg%3E");}
.sg-burst.k-dot{--shape:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='30' fill='%23fff'/%3E%3C/svg%3E");}

.sg-burst .fl{position:absolute;left:0;top:0;
  width:calc(var(--bs) * 3);height:calc(var(--bs) * 3);
  margin:calc(var(--bs) * -1.5) 0 0 calc(var(--bs) * -1.5);border-radius:50%;
  background:radial-gradient(circle,rgba(244,250,255,1) 0%,
    rgba(96,165,250,.92) 38%,rgba(30,58,138,0) 76%);
  animation:sgFlash .36s ease-out forwards;}

/* solid fill + two colour drop-shadows; they respect the mask alpha, so the halo
   follows the star silhouette rather than a box */
.sg-burst i{position:absolute;left:0;top:0;width:var(--ps);height:var(--ps);
  margin:calc(var(--ps) / -2) 0 0 calc(var(--ps) / -2);
  background:currentColor;
  -webkit-mask:var(--shape) center/contain no-repeat;
          mask:var(--shape) center/contain no-repeat;
  filter:drop-shadow(0 0 3px currentColor) drop-shadow(0 0 8px currentColor);
  animation:sgSpark var(--sd) cubic-bezier(.12,.72,.24,1) forwards;
  animation-delay:var(--sdl);}

@keyframes sgFlash{0%{transform:scale(.15);opacity:1;}100%{transform:scale(1.6);opacity:0;}}
@keyframes sgSpark{           /* --gy = gravity drop */
  0%{transform:translate(0,0) scale(.35);opacity:0;}
  14%{opacity:1;transform:translate(calc(var(--dx) * .3),calc(var(--dy) * .3)) scale(1.12);}
  100%{transform:translate(var(--dx),calc(var(--dy) + var(--gy))) scale(.3);opacity:0;}
}
/* ===== FLN ANIMATION KIT: sky-burst END ===== */
```

```js
/* ===== FLN ANIMATION KIT: sky-burst BEGIN ===== */
(function(){ "use strict";
  var M = window.FLNMotion;

  function boom(o){                      // sine thud + noise tail + square crackles
    var actx = M.audio(); if(!actx) return;
    try{
      var t = actx.currentTime, out = actx.createGain();
      out.gain.value = o.volume; out.connect(actx.destination);

      var tg = actx.createGain();
      tg.gain.setValueAtTime(0.9, t);
      tg.gain.exponentialRampToValueAtTime(0.0001, t + 0.16);
      tg.connect(out);
      var osc = actx.createOscillator();
      osc.type = "sine";
      osc.frequency.setValueAtTime(420, t);
      osc.frequency.exponentialRampToValueAtTime(90, t + 0.16);
      osc.connect(tg); osc.start(t); osc.stop(t + 0.18);

      var n = actx.sampleRate * 0.45;
      var buf = actx.createBuffer(1, n, actx.sampleRate), d = buf.getChannelData(0);
      for(var i = 0; i < n; i++) d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / n, 2.6);
      var src = actx.createBufferSource(); src.buffer = buf;

      for(var c = 0; c < o.crackles; c++){
        var cg = actx.createGain(), ct = t + 0.10 + Math.random() * 0.30;
        cg.gain.setValueAtTime(0.0001, ct);
        cg.gain.exponentialRampToValueAtTime(0.18, ct + 0.006);
        cg.gain.exponentialRampToValueAtTime(0.0001, ct + 0.07);
        cg.connect(out);
        var co = actx.createOscillator();
        co.type = "square";
        co.frequency.setValueAtTime(1500 + Math.random() * 2200, ct);
        co.connect(cg); co.start(ct); co.stop(ct + 0.08);
      }
      var bp = actx.createBiquadFilter();
      bp.type = "bandpass"; bp.frequency.value = 3400; bp.Q.value = 0.8;
      var ng = actx.createGain();
      ng.gain.setValueAtTime(0.0001, t);
      ng.gain.exponentialRampToValueAtTime(0.5, t + 0.03);
      ng.gain.exponentialRampToValueAtTime(0.0001, t + 0.45);
      src.connect(bp); bp.connect(ng); ng.connect(out); src.start(t + 0.02);
    }catch(_){}
  }

  function pop(el, r, o){
    el.classList.add("popped");
    // respawn on the next FLIGHT lap - the glow cycle is much shorter, so filter by name
    el.addEventListener("animationiteration", function back(e){
      if(e.animationName !== "sgFly") return;
      el.classList.remove("popped");
      el.removeEventListener("animationiteration", back);
    });

    var kind = "k-dot", cls = el.classList;
    for(var ci = 0; ci < cls.length; ci++){ if(o.kind[cls[ci]]) kind = o.kind[cls[ci]]; }

    var bs = Math.max(11, r.width);
    var b = document.createElement("div");
    b.className = "sg-burst " + kind;
    b.style.left = (r.left + r.width / 2) + "px";
    b.style.top  = (r.top  + r.height / 2) + "px";
    b.style.setProperty("--bs", bs + "px");
    b.appendChild(document.createElement("div")).className = "fl";

    var k = 0;
    for(var g = 0; g < o.rings.length; g++){
      var R = o.rings[g], off = Math.random() * Math.PI * 2;
      for(var i = 0; i < R.n; i++, k++){
        var a = off + i / R.n * Math.PI * 2;
        var dist = bs * R.rad * (0.78 + Math.random() * 0.44);
        var p = document.createElement("i");
        p.style.cssText =
          "--ps:"  + (bs * R.size * (0.8 + Math.random() * 0.5)).toFixed(1) + "px;" +
          "--dx:"  + (Math.cos(a) * dist).toFixed(1) + "px;" +
          "--dy:"  + (Math.sin(a) * dist).toFixed(1) + "px;" +
          "--gy:"  + (dist * o.gravity).toFixed(1) + "px;" +
          "--sd:"  + (R.dur + Math.random() * 0.22).toFixed(2) + "s;" +
          "--sdl:" + (Math.random() * 0.06).toFixed(3) + "s;" +
          "color:" + o.hues[k % o.hues.length];
        b.appendChild(p);
      }
    }
    document.body.appendChild(b);
    if(o.sound) boom(o);
    setTimeout(function(){ b.remove(); }, o.life);
  }

  M.skyBurst = {
    defaults: {
      container:".sg-sky", when:["is-start","is-end"],
      rings:[{n:9,rad:3.1,size:.58,dur:.80},{n:7,rad:1.8,size:.78,dur:.62}],
      hues:["#FCB717","#3B7DD8","#21A74A","#E5484D","#7048D6","#F1781D"],
      kind:{s1:"k-star",s2:"k-star",s3:"k-spark",s4:"k-dot",s5:"k-dot"},
      gravity:0.42, pad:12, padRatio:0.7, minAlpha:0.08, life:1200,
      sound:true, volume:0.22, crackles:4
    },
    init: function(opts){
      var o = Object.assign({}, this.defaults, opts || {});
      M.guard(function(){
        var sky = typeof o.container === "string"
          ? document.querySelector(o.container) : o.container;
        if(!sky) return;
        // capture phase: .sg-sky is pointer-events:none, so hit-test by rect (R6)
        document.addEventListener("pointerdown", function(e){
          if(M.still()) return;
          if(!o.when.some(function(c){ return document.body.classList.contains(c); })) return;
          var els = sky.querySelectorAll("i:not(.popped)");
          for(var i = 0; i < els.length; i++){
            var el = els[i], r = el.getBoundingClientRect();
            if(r.width < 2) continue;
            var pad = Math.max(o.pad, r.width * o.padRatio);   // ~4px targets need slack
            if(e.clientX < r.left - pad || e.clientX > r.right  + pad ||
               e.clientY < r.top  - pad || e.clientY > r.bottom + pad) continue;
            if(parseFloat(getComputedStyle(el).opacity) < o.minAlpha) continue;
            // claim the tap, or it also fires the button under the star
            e.stopPropagation(); e.preventDefault();
            pop(el, r, o);
            return;
          }
        }, true);
      });
    }
  };
  M.ready(function(){ M.guard(function(){ M.skyBurst.init(); }); });
})();
/* ===== FLN ANIMATION KIT: sky-burst END ===== */
```

**Options**

| Key | Default | Effect |
|---|---|---|
| `container` | `".sg-sky"` | Layer to hit-test. |
| `when` | `["is-start","is-end"]` | Body classes it is live on. |
| `rings` | 9@3.1x + 7@1.8x | 16 particles total. `n` count, `rad` distance, `size` scale, `dur` seconds. |
| `hues` | 6 kit colours | Cycled by index so every burst shows the full palette. |
| `kind` | s1/s2→star, s3→spark, s4/s5→dot | Shape class → burst mask. |
| `gravity` | `0.42` | Downward drop as a fraction of travel. `0` = flat spray. |
| `pad` / `padRatio` | `12` / `0.7` | Hit-box slack. Do not lower. |
| `minAlpha` | `0.08` | Faded elements cannot be popped. |
| `life` | `1200` | ms before removal. Must exceed the longest particle. |
| `sound` / `volume` / `crackles` | `true` / `0.22` / `4` | Audio. |

**Why manual hit-testing** - making `.sg-sky` interactive would put an invisible full-screen layer
over every button.

**Why the generous hit box** - smallest elements are ~4px. `max(12, width*0.7)` gives ~28x28px.

**Gotchas**
- Remove `stopPropagation()`/`preventDefault()` and the tap also fires the button underneath.
- Replace the data URIs with file refs and masks vanish under `file://`.
- Shipped code calls the gravity var `--g`, colliding with the sky's glow-duration `--g`. Kit uses
  `--gy`. Do not mix shipped CSS with kit JS.

**Deviations** - `--g`→`--gy`; `classList.forEach`→index loop; `M.still()` guard added; hard-coded
values→options.

---

## 3. Nudge hand press (hesitation hint)

**▶ Preview:** `index.html#nudge-ripple` (the press is shown in that card) · **Built, not yet installed**

The guiding hand that appears when a child hesitates. Six treatments exist; **use C**.

| Treatment | Keyframes | Motion |
|---|---|---|
| A | `nhPress` + `nhFx` | Two-layer, clip-path split; ring appears at contact |
| B | `nhTapHand` + `nhTapFx` | Inset-split; finger +7px, dots pop |
| **C** | `nhTapNew` / `nhTapP` | Plain press, contact held 45-62% ← recommended |
| D | `nhSimple` | Bare `scale(.88)` |
| E | `demoTapNew` / `demoTapP` | Tutorial hand, 1.1s |
| F | `nudgeMove` | Naive bob - **DEAD**, overridden everywhere |

```css
/* ===== FLN ANIMATION KIT: nudge-press BEGIN ===== */
@keyframes nhTapNew{
  0%,100%{transform:translateY(0) scale(1);}
  45%{transform:translateY(6px) scale(.93);}
  62%{transform:translateY(6px) scale(.93);}   /* contact HELD 45->62% */
}
@keyframes demoTapNew{0%,100%{transform:scale(1);}48%{transform:scale(.9);}64%{transform:scale(.9);}}
@keyframes nhPress{0%,100%{transform:scale(1);}40%,58%{transform:scale(.9);}}
@keyframes nhFx{0%,34%{opacity:0;transform:scale(.55);}46%{opacity:1;transform:scale(1);}
  58%{opacity:1;transform:scale(1.02);}78%,100%{opacity:0;transform:scale(1.12);}}

#nudgeHand{position:absolute;width:86px;height:108px;pointer-events:none;
  opacity:0;transition:opacity .2s ease;z-index:40;}
#nudgeHand.show{opacity:1;}
#nudgeHand img{width:100%;height:100%;object-fit:contain;
  animation:nhTapNew 1.3s ease-in-out infinite;}
/* ===== FLN ANIMATION KIT: nudge-press END ===== */
```

```js
/* ===== FLN ANIMATION KIT: nudge BEGIN ===== */
(function(){ "use strict";
  var M = window.FLNMotion;
  function place(el, o){
    var nh = document.getElementById(o.hand); if(!nh || !el) return;
    var host = document.querySelector(o.host); if(!host) return;
    var r = el.getBoundingClientRect(), sw = host.getBoundingClientRect(), s = M.scale();
    nh.style.left = ((r.left - sw.left)/s + r.width/s/2 + o.dx) + "px";
    nh.style.top  = ((r.top  - sw.top )/s + r.height/s   + o.dy) + "px";
    nh.classList.add("show");
  }
  M.nudge = {
    defaults:{ hand:"nudgeHand", host:".slide-stage", dx:-48, dy:-30, oneHand:true },
    pointAt: function(el, opts){
      var o = Object.assign({}, this.defaults, opts || {});
      M.guard(function(){
        if(M.still()) return;
        if(o.oneHand) document.querySelectorAll(".demo-hand").forEach(function(h){ h.remove(); });
        place(el, o);
      });
    },
    after: function(target, ms, opts){            // returns cancel()
      var o = Object.assign({}, this.defaults, opts || {}), t = null;
      M.guard(function(){
        if(!ms || M.still()) return;
        t = setTimeout(function(){
          var el = (typeof target === "string") ? document.querySelector(target) : target;
          if(el) place(el, o);
        }, ms);
      });
      return function(){ clearTimeout(t); };
    },
    hide: function(opts){
      var o = Object.assign({}, this.defaults, opts || {});
      var nh = document.getElementById(o.hand); if(nh) nh.classList.remove("show");
    }
  };
})();
/* ===== FLN ANIMATION KIT: nudge END ===== */
```

**Options** - `hand` (element id), `host` (positioning context), `dx`/`dy` (offset from target
bottom-centre), `oneHand` (clear stray demo hands).

**Gotchas**
- Position against `.slide-stage`, not `.stage` - otherwise the hand sits ~140px (header) too low.
- `dy` is per call site: `-30` general, `-6` nav button, `-56` overlapping a tile.
- Never show a tap hand and a drag hand at once.

---

## 4. Nudge hand tap ripple

**▶ Preview:** `index.html#nudge-ripple` · **Built, not yet installed** - real assets, shipped geometry

Two wavefronts and three sparks break out of the fingertip exactly as the hand makes contact.

| | |
|---|---|
| Source | `MTKGA02_L01_S01/style.css:2536-2562` |
| Assets | `nudge_fx_ring_inner.svg`, `nudge_fx_ring_outer.svg`, `nudge_fx_sparks.svg` |
| Needs | Recipe 3 treatment C |

```css
/* ===== FLN ANIMATION KIT: nudge-ripple BEGIN ===== */
/* Each layer is on a 120-unit square canvas centred on the ripple origin, so
   background-size:contain + transform-origin:50% 50% scales it about the fingertip.
   GEOMETRY: #nudgeHand is 86x108; nudge_hand_new.svg (75x94, viewBox 33 24 75 94)
   renders at object-fit:contain scale 1.1467 -> fingertip at (34.2, 15.8).
   The 94.6px FX square is offset to centre exactly there. */
#nudgeHand .nh-tapfx{position:absolute;width:94.6px;height:94.6px;
  left:-13.08px;top:-31.48px;pointer-events:none;}
#nudgeHand .nh-tapfx i{position:absolute;inset:0;display:block;
  background-repeat:no-repeat;background-position:center;background-size:contain;
  transform-origin:50% 50%;opacity:0;}
#nudgeHand .nh-tapfx .fx-ro{background-image:url(assets/UI/nudge_fx_ring_outer.svg);
  animation:nhRippleOuter 1.3s ease-out infinite;}
#nudgeHand .nh-tapfx .fx-ri{background-image:url(assets/UI/nudge_fx_ring_inner.svg);
  animation:nhRippleInner 1.3s ease-out infinite;}
#nudgeHand .nh-tapfx .fx-sp{background-image:url(assets/UI/nudge_fx_sparks.svg);
  animation:nhSparkPop 1.3s ease-out infinite;}

/* inner leads, outer trails - one ripple rolling out */
@keyframes nhRippleInner{0%,38%{opacity:0;transform:scale(.30);}47%{opacity:1;transform:scale(.74);}
  70%{opacity:.5;transform:scale(1.10);}90%,100%{opacity:0;transform:scale(1.34);}}
@keyframes nhRippleOuter{0%,45%{opacity:0;transform:scale(.55);}56%{opacity:.95;transform:scale(.88);}
  78%{opacity:.4;transform:scale(1.20);}96%,100%{opacity:0;transform:scale(1.46);}}
@keyframes nhSparkPop{0%,42%{opacity:0;transform:scale(.55);}52%{opacity:1;transform:scale(1);}
  68%{opacity:1;transform:scale(1.06);}86%,100%{opacity:0;transform:scale(1.18);}}
/* ===== FLN ANIMATION KIT: nudge-ripple END ===== */
```

```html
<div id="nudgeHand">
  <span class="nh-tapfx"><i class="fx-ro"></i><i class="fx-ri"></i><i class="fx-sp"></i></span>
  <img src="assets/UI/nudge_hand_new.svg" alt="">
</div>
```

**Object-independent - the target never enters the maths.** The FX square is anchored to the
fingertip *inside the hand box*, not to the thing being tapped. Apple, tile, book, bin: identical.
The hand itself carries no `left`/`top` in CSS - `FLNMotion.nudge.pointAt(el)` measures the target
and sets them (Recipe 3). What must be rechecked per game is the **hand box size**, not the object.

**Sync by duration, never delay** - press and all three layers run the same 1.3s, staggered by
keyframe percentages. CSS animations start at page load, not when `.show` is added, so equal
durations are the only thing keeping them locked. A delay drifts.

**Class is `nh-tapfx`, not `nh-fx`** - legacy `.nh-fx` rules (`display:none !important`) exist in
several games and would silently kill it.

**Rescaling** - if `#nudgeHand` is not 86x108, scale *every* px value (square + both offsets) by the
same factor. Valid only because both boxes share the SVG's 75:94 ratio. For 56x70 the factor is 0.65.

**Gotchas**
- The three FX assets do **not** ship with every game. Check the target folder directly.
- R11 applies hard: one game has a later `#nudgeHand{width:56px;height:70px}` FORK PATCH that wins.
  Grep every rule before reusing offsets.
- Not every `.glide` hand is a drag. A hand that travels and *rests* is a tap and gets the ripple.

---

## 5. Demo hand drag (how-to-drag hint)

**Reference only** - not installed, not in the preview.

A hand glides from source to target, optionally with a faint clone of the tile beneath it. Loops
every 1.8s until the child touches anything.

Source: `MTKGA02_L01_S01/app.js:1318-1390`

```css
.demo-hand{position:absolute;width:80px;height:100px;pointer-events:none;z-index:41;
  animation:demoTapNew 1.1s ease-in-out infinite;}
.demo-ghost{position:absolute;pointer-events:none;opacity:.45;z-index:39;
  transition:left 1s ease, top 1s ease;}
```

```js
/* ===== FLN ANIMATION KIT: demo-drag BEGIN ===== */
(function(){ "use strict";
  var M = window.FLNMotion, _stop = null;

  function glide(fromEl, toEl, onDone, o){
    var stage = document.querySelector(o.host); if(!stage) return;
    document.querySelectorAll(".demo-hand, .demo-ghost").forEach(function(h){ h.remove(); });
    var sw = stage.getBoundingClientRect(), s = M.scale();
    var r1 = fromEl.getBoundingClientRect(), r2 = toEl.getBoundingClientRect();
    var ghost = null;

    if(o.ghost){
      var drop = toEl.querySelector(o.dropInto) || toEl;
      var rz = drop.getBoundingClientRect();
      var gw = r1.width/s, gh = r1.height/s;
      ghost = fromEl.cloneNode(true);
      ghost.classList.add("demo-ghost");
      ghost.classList.remove("dragging","snapped");
      ghost.removeAttribute("id");
      ghost.style.left = ((r1.left - sw.left)/s) + "px";
      ghost.style.top  = ((r1.top  - sw.top )/s) + "px";
      stage.appendChild(ghost);
      requestAnimationFrame(function(){ requestAnimationFrame(function(){
        ghost.style.left = ((rz.left - sw.left)/s + rz.width/s/2  - gw/2) + "px";
        ghost.style.top  = ((rz.top  - sw.top )/s + rz.height/s/2 - gh/2) + "px";
      }); });
    }

    var hand = document.createElement("img");
    hand.src = o.art; hand.className = "demo-hand";
    hand.style.left = ((r1.left - sw.left)/s + r1.width/s/2  + o.dx) + "px";
    hand.style.top  = ((r1.top  - sw.top )/s + r1.height/s/2 + o.dy) + "px";
    stage.appendChild(hand);
    // double rAF: lay out at the start position BEFORE attaching the transition,
    // or it jumps straight to the end
    requestAnimationFrame(function(){ requestAnimationFrame(function(){
      hand.style.transition = "left " + o.travel + "ms ease, top " + o.travel + "ms ease";
      hand.style.left = ((r2.left - sw.left)/s + r2.width/s/2  + o.dx) + "px";
      hand.style.top  = ((r2.top  - sw.top )/s + r2.height/s/2 + o.dy) + "px";
    }); });
    setTimeout(function(){
      hand.remove(); if(ghost) ghost.remove(); if(onDone) onDone();
    }, o.travel + 350);
  }

  M.demoDrag = {
    defaults:{ host:".slide-stage", art:"assets/UI/nudge_hand_new.svg",
               dx:-40, dy:-16, travel:1000, every:1800, ghost:false, dropInto:".bin-items" },
    once: function(fromEl, toEl, onDone, opts){
      var o = Object.assign({}, this.defaults, opts || {});
      M.guard(function(){ if(!M.still()) glide(fromEl, toEl, onDone, o); });
    },
    loop: function(fromEl, toEl, opts){          // returns stop()
      var o = Object.assign({}, this.defaults, opts || {});
      if(_stop) _stop();
      var stage = document.querySelector(o.host), timer = null, stopped = false;
      var stop = function(){
        if(stopped) return; stopped = true;
        clearTimeout(timer);
        document.querySelectorAll(".demo-hand, .demo-ghost").forEach(function(h){ h.remove(); });
        if(stage) stage.removeEventListener("pointerdown", stop, true);
        if(_stop === stop) _stop = null;
      };
      var cycle = function(){
        if(stopped) return;
        if(!document.contains(fromEl) || fromEl.classList.contains("snapped") ||
           !document.contains(toEl)){ stop(); return; }
        glide(fromEl, toEl, null, o);
        timer = setTimeout(cycle, o.every);
      };
      M.guard(function(){
        if(M.still()) return;
        if(stage) stage.addEventListener("pointerdown", stop, true);  // capture: beat drag handlers
        _stop = stop; cycle();
      });
      return stop;
    }
  };
})();
/* ===== FLN ANIMATION KIT: demo-drag END ===== */
```

**Options** - `host`, `art`, `dx`/`dy`, `travel` (ms), `every` (loop interval), `ghost`, `dropInto`.

**Gotchas**
- The double `requestAnimationFrame` is load-bearing.
- Stop listener is capture-phase so it beats drag handlers.
- Loop self-cancels when the slide changes - the stage is rebuilt between slides.

---

## 6. Mascot reaction (Swifty)

**Reference only** - not installed, not in the preview.

The mascot pops and the celebration star escapes the circular avatar instead of being clipped.

**The star is baked into the animated WebP, not made in CSS.** The `_anim` sprites are drawn with the
disc smaller than their canvas so the star breaks into transparent margin. Base rules crop that off
with `overflow:hidden` + `object-fit:cover`. The fix unclips **only while a reaction plays**.

Source: `MTKGA02_L01_S01/app.js:256-269` + `style.css:2807-2808`

```css
/* ===== FLN ANIMATION KIT: mascot-react BEGIN ===== */
@keyframes mascotReact{
  0%{transform:scale(var(--mbase,1)) rotate(0);}
  35%{transform:scale(calc(var(--mbase,1)*1.16)) rotate(-5deg);}
  68%{transform:scale(calc(var(--mbase,1)*1.04)) rotate(3deg);}
  100%{transform:scale(var(--mbase,1)) rotate(0);}
}
.mascot-wrap.react .mascot-img{animation:mascotReact .62s cubic-bezier(.34,1.5,.6,1);}

/* THE UNCLIP - scoped to .anim so static poses are untouched */
.mascot-wrap.anim .mascot-circle{
  overflow:visible !important;background:transparent !important;
  border:none !important;box-shadow:none !important;}
.mascot-wrap.anim .mascot-circle .mascot-img{
  position:static !important;inset:auto !important;
  width:100% !important;height:auto !important;
  object-fit:contain !important;transform:none !important;}

.mascot-wrap[data-expr="celebrate"]{--mbase:1.22;}
.mascot-wrap[data-expr="hint"]{--mbase:1.12;}
/* ===== FLN ANIMATION KIT: mascot-react END ===== */
```

```js
/* ===== FLN ANIMATION KIT: mascot-react BEGIN ===== */
(function(){ "use strict";
  var M = window.FLNMotion;
  M.mascot = {
    defaults:{
      wrap:"swBuddy", img:"swBuddyImg", dir:"assets/UI/", prefix:"sw_head_",
      still:"talking", fallback:"assets/UI/mascot.webp", bust:["celebrate"],
      pose:{ talk:"talking", point:"talking", idle:"talking", happy:"celebrate",
             celebrate:"celebrate", tryagain:"tryagain", hint:"hint",
             idea:"hint", teach:"hint" }
    },
    set: function(mood, opts){
      var o = Object.assign({}, this.defaults, opts || {});
      M.guard(function(){
        var img = document.getElementById(o.img); if(!img) return;
        var expr = o.pose[mood] || o.still;
        var animated = expr !== o.still;
        if(M.still()) animated = false;          // animated WebPs can't be frozen by CSS
        var bust = (animated && o.bust.indexOf(expr) >= 0) ? ("?r=" + Date.now()) : "";
        img.onerror = function(){ img.onerror = null; img.src = o.fallback; };
        img.src = o.dir + o.prefix + expr + (animated ? "_anim.webp" : ".webp") + bust;
        img.style.display = "";
        var w = document.getElementById(o.wrap); if(!w) return;
        w.dataset.expr = expr;
        w.classList.toggle("anim", animated);    // <- the half usually missed
        w.classList.remove("react");
        void w.offsetWidth;                      // force reflow so it restarts
        w.classList.add("react");
      });
    }
  };
})();
/* ===== FLN ANIMATION KIT: mascot-react END ===== */
```

**Gotchas - this is where it silently breaks**
- **Both halves required:** the CSS unclip **and** the JS toggling `.anim` on the *wrapper*. It has
  shipped with correct CSS whose class was never toggled. Trace the class from JS to CSS before
  calling it done.
- `void w.offsetWidth` is load-bearing - without the reflow the animation does not restart.
- `?r=` cache-bust is what makes the burst replay; without it it plays once per page load.
- If markup is not `.mascot-wrap > .mascot-circle > .mascot-img`, restructure it rather than faking
  the effect, and check every stylesheet the page loads.

---

## 7. Correct answer confetti

**▶ Preview:** `index.html#confetti` · **Rebuilt** - the shipped version is replaced, not tuned

Source of the original: `MTKGA02_L01_S01/app.js:272-290`.

### Why the original reads as fake

| Shipped | Real paper |
|---|---|
| `ease-out` fall | Paper hits **terminal velocity** almost instantly - descent is constant speed. `ease-out` reads as decelerating, which nothing falling does. |
| 2D `rotate()` | A falling flat plate **tumbles** about its horizontal axes, so its projected area changes and it winks edge-on. An in-plane spin looks like a pinwheel. |
| Straight down | The tumble generates alternating lift, so pieces **zig-zag** like a pendulum. |
| One flat colour | Lit from one side, the **back face reads darker**. That shimmer is most of the effect. |
| Uniform 10×16px | Mixed shapes and sizes at different depths. |

### Structure

One element cannot run three transform animations, so each gets its own layer:

```
.p  path    translateY   constant-speed fall
 └ .w wobble translateX  pendulum sway
    └ .f face rotateX/Y  tumble + the two ::before/::after faces
```

```css
/* ===== FLN ANIMATION KIT: confetti BEGIN ===== */
.fx-confetti{position:absolute;inset:0;pointer-events:none;overflow:hidden;z-index:60;}
.fx-confetti .p{position:absolute;top:0;left:var(--x);
  animation:cfFall var(--fall) linear var(--delay) both;}
/* Sway shares the rock's PERIOD and lags it by a quarter cycle. A fluttering plate
   slides in the direction it is tilted - the swing and the rock are one motion, not
   two independent ones. The negative delay is what creates the quarter-cycle lag. */
.fx-confetti .w{display:block;perspective:600px;
  animation:cfGlide var(--rockT) linear var(--delay) infinite both;}
.fx-confetti .f{display:block;position:relative;transform-style:preserve-3d;
  width:calc(var(--w) * var(--z));height:calc(var(--h) * var(--z));
  opacity:var(--dim,1);
  animation:cfRock var(--rockT) linear var(--delay) infinite both;}
/* the minority that actually goes end-over-end */
.fx-confetti .f.tum{animation:cfTumble var(--rockT) linear var(--delay) infinite both;}
/* two real faces: front bright, back the same hue darkened */
.fx-confetti .f::before,.fx-confetti .f::after{content:"";position:absolute;inset:0;
  border-radius:inherit;backface-visibility:hidden;-webkit-backface-visibility:hidden;}
.fx-confetti .f::before{background:var(--c);}
.fx-confetti .f::after{background:var(--c2);transform:rotateY(180deg);}
/* Shape mix. Sizes are deliberately far apart - at 7-11px a rectangle and a square are
   indistinguishable while tumbling, which makes the whole field read as "all squares". */
.fx-confetti .sq{--w:8px;  --h:8px;  border-radius:1px;}   /* square    1:1   */
.fx-confetti .rc{--w:6px;  --h:13px; border-radius:1px;}   /* rectangle 1:2.2 */
.fx-confetti .ln{--w:2.5px;--h:16px; border-radius:2px;}   /* line      1:6.4 */
.fx-confetti .st{--w:11px; --h:11px;}                      /* star - needs a few
                                 more px than the rest for its points to read */
/* clip-path goes on the FACES, not on .f - clip-path on .f would force
   transform-style to flat and kill the two-sided tumble */
.fx-confetti .st::before,.fx-confetti .st::after{
  clip-path:polygon(50% 0%,61% 35%,98% 35%,68% 57%,79% 91%,
                    50% 70%,21% 91%,32% 57%,2% 35%,39% 35%);}

/* LINEAR - terminal velocity. `both` is load-bearing: without it delayed pieces
   sit in a visible row on the top edge until their delay elapses.
   --drift gives each piece a gentle lean, as if in a faint air current. */
@keyframes cfFall{
  0%{transform:translate(0,-40px);opacity:0;}
  5%{opacity:1;}
  86%{opacity:1;}
  100%{transform:translate(var(--drift,0px),var(--dist,820px));opacity:0;}
}
/* GLIDE + BOB. Real flutter is NOT sinusoidal: the plate glides at near-constant
   attitude, then turns sharply. Long glide, quick reversal, linear timing - the
   keyframe percentages do the shaping.
   The Y term is vertical speed modulation: the plate falls SLOWER broadside during
   the glide (max drag) and quicker through the flip (edge-on, min drag). That
   hesitate-then-drop is what the eye reads as paper. */
@keyframes cfGlide{
  0%  {transform:translate(calc(var(--sway) * -1), 0);}
  45% {transform:translate(var(--sway), calc(var(--bob) * -1));}
  50% {transform:translate(var(--sway), 0);}
  95% {transform:translate(calc(var(--sway) * -1), calc(var(--bob) * -1));}
  100%{transform:translate(calc(var(--sway) * -1), 0);}
}
/* FLUTTER - the default, ~78% of pieces. Rocks about ONE axis, capped well short of
   edge-on, so the face stays toward the viewer. ease-in-out because a turning point
   is a turning point: it decelerates at max tilt, like any pendulum. */
/* FLIP. Holds attitude through the glide, then snaps over in 5% of the cycle.
   Phase-locked to cfGlide by construction - both start at the beginning of a glide,
   so no offset delay: the flip lands exactly on the direction reversal. */
@keyframes cfRock{
  0%  {transform:rotateZ(var(--tilt)) rotateY(var(--yaw)) rotateX(var(--amp));}
  45% {transform:rotateZ(var(--tilt)) rotateY(var(--yaw)) rotateX(calc(var(--amp) * 0.86));}
  50% {transform:rotateZ(var(--tilt)) rotateY(var(--yaw)) rotateX(calc(var(--amp) * -1));}
  95% {transform:rotateZ(var(--tilt)) rotateY(var(--yaw)) rotateX(calc(var(--amp) * -0.86));}
  100%{transform:rotateZ(var(--tilt)) rotateY(var(--yaw)) rotateX(var(--amp));}
}
/* TUMBLE - the other ~22%. One half revolution, face to face. The keyframes dwell
   near the faces and sweep through edge-on in 16% of the cycle, because a real plate
   hangs broadside where drag is highest and flips fast through the low-drag edge. */
@keyframes cfTumble{
  0%  {transform:rotateZ(var(--tilt)) rotateY(var(--yaw)) rotateX(0deg);}
  42% {transform:rotateZ(var(--tilt)) rotateY(var(--yaw)) rotateX(72deg);}
  58% {transform:rotateZ(var(--tilt)) rotateY(var(--yaw)) rotateX(108deg);}
  100%{transform:rotateZ(var(--tilt)) rotateY(var(--yaw)) rotateX(180deg);}
}
/* ===== FLN ANIMATION KIT: confetti END ===== */
```

```js
/* ===== FLN ANIMATION KIT: confetti BEGIN ===== */
(function(){ "use strict";
  var M = window.FLNMotion;
  function rnd(a, b){ return a + Math.random() * (b - a); }

  M.confetti = {
    defaults: {
      host:".stage-inner", count:80, stagger:0.35,
      fall:[1.1,1.8], drift:45, sway:[10,34], bob:[3,7],
      rockT:[0.6,1.2], tumbleT:[0.75,1.5], tumbleShare:0.22,
      amp:[28,52], yaw:30, depth:[0.75,1.15], tilt:25,
      /* weighted: star 40%, rectangle 20%, line 20%, square 20%.
         Repeat an entry to weight it - the array is sampled uniformly. */
      shapes:["st","st","st","st","rc","rc","ln","ln","sq","sq"],
      /* VIBGYOR. Front/back pairs - the back is the SAME hue darkened, never a
         different hue, or it reads as two pieces flickering instead of one turning. */
      colors:[["#8B2FC9","#5E1C8C"],   /* violet */
              ["#3F51B5","#27358A"],   /* indigo */
              ["#1E88E5","#135FA6"],   /* blue   */
              ["#22B24C","#157A34"],   /* green  */
              ["#FFD21E","#D9A800"],   /* yellow */
              ["#FF8A1E","#C75F00"],   /* orange */
              ["#E5322D","#A81F1B"]],  /* red    */
      phases:["guided","practice","mastery"]   /* [] disables phase gating */
    },
    burst: function(opts){
      var o = Object.assign({}, this.defaults, opts || {});
      M.guard(function(){
        if(M.still()) return;
        /* confetti ONLY on activity phases - never tutorials, demos, landing, transitions */
        if(o.phases.length && o.phase && o.phases.indexOf(o.phase) < 0) return;
        var host = document.querySelector(o.host); if(!host) return;

        var dist = host.clientHeight + 60, maxLife = 0;
        var wrap = document.createElement("div");
        wrap.className = "fx-confetti";

        for(var i = 0; i < o.count; i++){
          var z     = rnd(o.depth[0], o.depth[1]);        /* depth */
          var fall  = rnd(o.fall[0], o.fall[1]) / z;      /* nearer = bigger = faster */
          var delay = rnd(0, o.stagger);
          if(fall + delay > maxLife) maxLife = fall + delay;
          var pair = o.colors[i % o.colors.length];
          /* most pieces flutter (face stays visible); a minority go end-over-end */
          /* Two regimes, and a real plate moves DIFFERENTLY in each:
             flutter = zigzags hard, almost no net sideways drift;
             tumble  = autorotation gives a steady lateral force, so it barely
                       zigzags but drifts consistently to one side. */
          var flutter = Math.random() > o.tumbleShare;
          var rockT   = flutter ? rnd(o.rockT[0], o.rockT[1])
                                : rnd(o.tumbleT[0], o.tumbleT[1]);
          var sway    = flutter ? rnd(o.sway[0], o.sway[1]) : rnd(2, 8);
          var drift   = flutter ? rnd(-o.drift/2.5, o.drift/2.5) : rnd(-o.drift, o.drift);
          var bob     = flutter ? rnd(o.bob[0], o.bob[1]) : rnd(2, 4);

          /* set every property once - they inherit down to .w and .f */
          var p = document.createElement("i"); p.className = "p";
          p.style.cssText =
            "--x:"     + rnd(-2, 98).toFixed(1) + "%;" +
            "--dist:"  + dist + "px;" +
            "--fall:"  + fall.toFixed(2) + "s;" +
            "--delay:" + delay.toFixed(2) + "s;" +
            "--drift:" + drift.toFixed(0) + "px;" +
            "--sway:"  + sway.toFixed(0) + "px;" +
            "--bob:"   + bob.toFixed(1) + "px;" +
            "--rockT:" + rockT.toFixed(2) + "s;" +
            /* capped short of 90deg: even at max tilt the face still reads */
            "--amp:"   + Math.round(rnd(o.amp[0], o.amp[1])) + "deg;" +
            "--yaw:"   + Math.round(rnd(-o.yaw, o.yaw)) + "deg;" +
            "--tilt:"  + Math.round(rnd(-o.tilt, o.tilt)) + "deg;" +
            "--z:"     + z.toFixed(2) + ";" +
            "--dim:"   + (0.72 + (z - o.depth[0]) /
                          (o.depth[1] - o.depth[0]) * 0.28).toFixed(2) + ";" +
            /* shapes stay legible by ASPECT RATIO, not size - see the shape table */
            "--c:"     + pair[0] + ";--c2:" + pair[1] + ";";

          var w = document.createElement("i"); w.className = "w";
          var f = document.createElement("i");
          f.className = "f " + o.shapes[Math.floor(Math.random() * o.shapes.length)] +
                        (flutter ? "" : " tum");
          w.appendChild(f); p.appendChild(w); wrap.appendChild(p);
        }
        host.appendChild(wrap);
        /* lifetime is computed, not hard-coded - a longer fall cannot be cut off */
        setTimeout(function(){ wrap.remove(); }, (maxLife + 0.3) * 1000);
      });
    },
    /* stops a slide advancing mid-celebration. 8s safety cap. */
    after: function(fn){
      var started = Date.now();
      (function check(){
        if(!document.querySelector(".fx-confetti") || Date.now() - started > 8000){ fn(); return; }
        setTimeout(check, 200);
      })();
    }
  };
})();
/* ===== FLN ANIMATION KIT: confetti END ===== */
```

### Options

| Key | Default | Effect |
|---|---|---|
| `host` | `".stage-inner"` | Container. Fall distance is measured from its height. |
| `count` | `80` | Pieces. Each is 3 elements + 2 pseudo-elements - see Performance. |
| `stagger` | `0.35` | Launch spread in seconds. |
| `fall` | `[1.1, 1.8]` | Seconds to cross, before the depth divisor. A correct-answer beat should clear in ~2s. |
| `drift` | `45` | Net sideways travel over the whole fall, px. Tumblers get the full range, flutterers 1/2.5 of it. |
| `sway` | `[10, 34]` | Glide amplitude, px - flutterers only. Tumblers are forced to 2-8px. |
| `bob` | `[3, 7]` | Vertical speed modulation, px. The hesitate-then-drop. Set to 0 and the fall goes dead. |
| `rockT` | `[0.6, 1.2]` | Glide/flip period, seconds. Drives the sway and bob too - one motion. |
| `tumbleT` | `[0.75, 1.5]` | Period for the end-over-end minority. |
| `tumbleShare` | `0.22` | Fraction that tumbles instead of fluttering. **Raise it and the face hides more.** |
| `amp` | `[28, 52]` | Flutter tilt, degrees. **Keep well under 90** or pieces go edge-on. |
| `yaw` | `30` | Max static second-axis lean, degrees. Variety without hiding the face. |
| `depth` | `[0.75, 1.15]` | Size scale. Also drives fall speed and dimming (parallax). |
| `tilt` | `25` | Max in-plane lean, degrees. |
| `shapes` | weighted | `r` strip, `s` square, `c` round, `t` streamer. Repeat entries to weight. |
| `colors` | 7 pairs | `[front, back]`. The back should be the front darkened, not a different hue. |
| `phases` + `phase` | activity phases | Gating, as before. |

### Tuning notes

- **Depth is one number driving three things** - size, fall speed, and dimming. Changing `depth`
  alone re-grades the whole field's sense of space.
- **The glide and the flip are one motion.** They share `rockT` and are phase-locked by their
  keyframes: the plate glides at near-constant attitude, then the flip lands exactly on the
  direction reversal. Decoupling them into independent periods makes confetti look shaken.
- **Nothing here is sinusoidal, on purpose.** `ease-in-out` on the glide gives a smooth pendulum,
  which is the wrong shape - real flutter is a long glide punctuated by a quick snap. The timing is
  `linear` and the keyframe percentages carry the shape (45%/50% and 95%/100% are the snaps).
- **Face visibility is a budget.** Projected area is `cos(rx)·cos(ry)`, so rotating two axes at once
  hides the face most of the time - the first version did this and was face-on only ~31% of the
  cycle. Rocking one axis at `amp ≤ 52°` is face-on ~100% of it. If you want more edge flashes,
  raise `tumbleShare`, not `amp`.
- **Back face = front darkened**, not a second hue. A contrasting back reads as two different
  confetti pieces flickering, not one piece turning over.
- **Lifetime is computed** from the slowest piece, not a fixed timeout - so raising `fall` or
  `depth` can't silently cut pieces off mid-air.

### Performance

Each piece is 3 elements plus 2 pseudo-elements, so `count:80` is ~400 nodes. Everything animates
`transform` and `opacity` only - both composited - so it is cheaper per pixel than the old version's
`ease-out` repaints, but the node count is higher. On low-end Android drop `count` to 45-55 before
touching anything else; the effect survives it because the depth spread still reads.

### Gotchas

- `perspective` sits on `.w`, not the wrapper - it must be on the **parent of the rotating element**
  or the tumble flattens into a 2D squash.
- `transform-style:preserve-3d` on `.f` is required, or the two faces collapse onto each other.
- Don't add a transform to `.p`, `.w` or `.f` from outside; each already owns its one transform.
- Use `FLNMotion.confetti.after()` before advancing, not a bare timeout.

### Deviation

This replaces the shipped effect rather than tuning it - different keyframes (`cfFall`/`cfGlide`/`cfRock`/
`cfTumble` vs `fxConfettiFall`), different markup (3 nested elements vs 1). Installing it means
removing the old `.fx-confetti i` rule and `fxConfettiFall`, or the two will both match and the old
flat rule will fight the new one.

## 8. Celebration star burst (end screen)

**▶ Preview:** `index.html#star-burst` · **Retuned** - fewer stars, slower drift

The only real canvas particle system in the repo. Source: `HI01H05_L02_S01/app.js:547-600`.

```js
/* ===== FLN ANIMATION KIT: star-burst BEGIN ===== */
(function(){ "use strict";
  var M = window.FLNMotion;
  M.starBurst = {
    defaults:{ host:"#confetti", w:1333, h:750,
      colors:["#FFE400","#FFBD00","#E89400","#FFCA6C","#FDFFB8"],
      /* retuned: fewer, slower, longer. Travel distance is held at ~547px so the
         burst still fills the same area - only the density and pace changed. */
      ticks:150, decay:0.975, startV:14, shots:[0,220,440], spin:0.18,
      stars:32, starScale:1.8, circles:8, circleScale:1.0 },
    fire: function(opts){
      var o = Object.assign({}, this.defaults, opts || {});
      M.guard(function(){
        if(M.still()) return;
        var host = document.querySelector(o.host); if(!host) return;
        var cv = document.createElement("canvas");
        cv.width = o.w; cv.height = o.h;                 // design grid, scaled by CSS
        cv.style.cssText = "position:absolute;inset:0;width:100%;height:100%;";
        host.appendChild(cv);
        var ctx = cv.getContext("2d"), parts = [];

        function starPath(r){
          ctx.beginPath();
          for(var i = 0; i < 10; i++){
            var rad = (i % 2 === 0) ? r : r/2, a = Math.PI/5*i - Math.PI/2;
            ctx[i === 0 ? "moveTo" : "lineTo"](Math.cos(a)*rad, Math.sin(a)*rad);
          }
          ctx.closePath();
        }
        function add(n, scalar, shape){
          for(var i = 0; i < n; i++){
            var a = Math.random()*Math.PI*2;
            parts.push({ x:cv.width/2, y:cv.height/2, ax:Math.cos(a), ay:Math.sin(a),
              vel:o.startV*(0.5 + Math.random()), tick:0, scalar:scalar, shape:shape,
              color:o.colors[Math.floor(Math.random()*o.colors.length)],
              rot:Math.random()*Math.PI*2, spin:(Math.random()-.5)*o.spin });
          }
        }
        function shoot(){ add(o.stars, o.starScale, "star"); add(o.circles, o.circleScale, "circle"); }
        o.shots.forEach(function(ms){ ms ? setTimeout(shoot, ms) : shoot(); });

        /* derived from the LAST shot, so retiming the shots cannot end the loop
           before they have all fired. A hard-coded 30 breaks if shots move later. */
        var minFrames = Math.max.apply(null, o.shots) / 16 + 20;
        var frames = 0;
        (function frame(){
          ctx.clearRect(0, 0, cv.width, cv.height);
          var alive = false;
          for(var i = 0; i < parts.length; i++){
            var p = parts[i];
            if(p.tick >= o.ticks) continue;
            alive = true;
            p.x += p.ax*p.vel; p.y += p.ay*p.vel; p.vel *= o.decay;
            p.rot += p.spin; p.tick++;
            ctx.globalAlpha = 1 - p.tick/o.ticks;
            ctx.fillStyle = p.color;
            ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot);
            if(p.shape === "star"){ starPath(8*p.scalar); ctx.fill(); }
            else { ctx.beginPath(); ctx.arc(0, 0, 6*p.scalar, 0, Math.PI*2); ctx.fill(); }
            ctx.restore();
          }
          frames++;
          if(alive || frames < minFrames) requestAnimationFrame(frame);  // survive delayed shots
          else setTimeout(function(){ cv.remove(); }, 300);
        })();
      });
    }
  };
})();
/* ===== FLN ANIMATION KIT: star-burst END ===== */
```

**Gotchas** - gravity is 0 by design (they float and fade). `minFrames` keeps the loop alive
through delayed shots. Canvas is the design grid stretched by CSS, so it scales for free.

---

## 9. Correct answer tile outline

**Superseded by recipe 19**, which keeps this rule and builds the confirm beat around it.
Kept here because the rule below - outline, no fill, no tick - is the house rule itself, and
recipe 19 is one way of animating it.

House rule: **no tick, no checkmark, no fill.** The green outline *is* the correct-mark.

```css
/* ===== FLN ANIMATION KIT: correct-outline BEGIN ===== */
.opt-cell.correct{
  background:#fff !important;                               /* NO green fill */
  border:3px solid var(--correct, #00B132) !important;
  box-shadow:0 6px 16px rgba(0,177,50,.14) !important;
}
.opt-cell.correct::after{content:none !important;display:none !important;}
@keyframes correctPop{0%{transform:scale(1);}45%{transform:scale(1.08);}100%{transform:scale(1);}}
.opt-cell.correct{animation:correctPop .4s cubic-bezier(.34,1.5,.6,1);}
/* ===== FLN ANIMATION KIT: correct-outline END ===== */
```

**Applying it** - the tile class varies (`.opt-cell`, `.m-card`, `.tile`, `.sort-item`). Find the
real "correct" class, then remove (a) any background fill and (b) any checkmark - pseudo-element,
inline SVG tick, or badge element. **Do not touch `.wrong`.**

---

## 10. Scene object outline (look-and-find)

**Generalised by recipe 21**, which turns this into a two-engine system any activity
can use. Kept because the reasoning below - why the ring is a baked alpha painted
through a mask, and why it must never be transformed - is what recipe 21's engine B
is built on.

Traces the exact silhouette of an object in a raster scene. Only in `HI01H01_L02_S04_dist`.

Each object ships a baked ring alpha as a base64 WebP in a CSS variable. The element paints a flat
colour *through* that alpha as a mask - so one asset serves idle, correct, wrong, guide and muted.

```css
/* ===== FLN ANIMATION KIT: contour-ring BEGIN ===== */
.tis-object-outline{
  position:absolute;inset:0;pointer-events:none;z-index:2;
  background:var(--tis-ring-c,#FFFFFF);
  -webkit-mask:var(--ring) center/cover no-repeat;
          mask:var(--ring) center/cover no-repeat;
  /* white core needs a hard coloured edge on pale art: 2 crisp shadows + 1 soft glow */
  filter:drop-shadow(0 0 1.2px var(--tis-ring-g,#2F6FE0))
         drop-shadow(0 0 1.2px var(--tis-ring-g,#2F6FE0))
         drop-shadow(0 0 7px var(--tis-ring-gs,rgba(47,111,224,.5)));
  animation:tisContourBreathe 2.8s ease-in-out infinite;
  transition:filter .18s ease,background .18s ease,opacity .25s ease;
}
.tis-object-outline:nth-of-type(2){animation-delay:-.93s;}   /* de-phase neighbours */
.tis-object-outline:nth-of-type(3){animation-delay:-1.86s;}

.tis-object-outline.is-hover{animation:none;opacity:1;
  filter:drop-shadow(0 0 1.3px var(--tis-ring-g,#2F6FE0))
         drop-shadow(0 0 1.3px var(--tis-ring-g,#2F6FE0))
         drop-shadow(0 0 11px rgba(47,111,224,.72));}
.tis-object-outline.is-wrong{opacity:1;--tis-ring-c:#F93544;
  animation:tisRingNo .62s cubic-bezier(.22,.8,.3,1) both;}
.tis-object-outline.is-correct{opacity:1;--tis-ring-c:#00B132;
  animation:tisRingPop .62s cubic-bezier(.16,1,.3,1) both;}
.tis-object-outline.is-guide{opacity:1;--tis-ring-c:#00B132;
  animation:tisContourGuide 1.15s ease-in-out infinite;}
.tis-object-outline.is-muted{animation:none;opacity:.16;filter:none;--tis-ring-c:#9AA7B4;}

@keyframes tisContourBreathe{0%,100%{opacity:.86;}50%{opacity:1;}}
@keyframes tisContourGuide{0%,100%{opacity:.62;}50%{opacity:1;}}
@keyframes tisRingPop{
  0%{opacity:.5;  filter:drop-shadow(0 0 1.3px #fff) drop-shadow(0 0 1.3px #fff) drop-shadow(0 0 0px rgba(0,177,50,.95));}
  38%{opacity:1;  filter:drop-shadow(0 0 1.3px #fff) drop-shadow(0 0 1.3px #fff) drop-shadow(0 0 24px rgba(0,177,50,.95));}
  100%{opacity:1; filter:drop-shadow(0 0 1.3px #fff) drop-shadow(0 0 1.3px #fff) drop-shadow(0 0 12px rgba(0,177,50,.75));}
}
@keyframes tisRingNo{
  0%,100%{opacity:1;filter:drop-shadow(0 0 1.3px #fff) drop-shadow(0 0 1.3px #fff) drop-shadow(0 0 10px rgba(249,53,68,.65));}
  22%{opacity:1;  filter:drop-shadow(0 0 1.3px #fff) drop-shadow(0 0 1.3px #fff) drop-shadow(0 0 22px rgba(249,53,68,.95));}
  48%{opacity:.7; filter:drop-shadow(0 0 1.3px #fff) drop-shadow(0 0 1.3px #fff) drop-shadow(0 0 3px rgba(249,53,68,.5));}
  74%{opacity:1;  filter:drop-shadow(0 0 1.3px #fff) drop-shadow(0 0 1.3px #fff) drop-shadow(0 0 22px rgba(249,53,68,.95));}
}
/* ===== FLN ANIMATION KIT: contour-ring END ===== */
```

**Two rules that make this work**
1. **Never animate `transform` on it.** It is a full-frame mask - scaling slides the ring off the
   art, the exact defect it exists to fix. Both effects are built from the glow instead.
2. **Never hand-edit the ring alphas - regenerate them** from the scene raster. Hand-tracing is why
   the untidy outline kept returning.

State is set from JS: the outline layers are appended *before* the hotspots, so no sibling selector
reaches backwards, and `:has()` was judged unsafe for the target Android tablets.

---

## 11. Wrong answer shake

**Superseded by recipe 20.** Kept as the inventory of what is actually in the fleet today -
six keyframes doing one job. Recipe 20 keeps this lateral idiom and its `.4s` tempo.

```css
/* ===== FLN ANIMATION KIT: shake BEGIN ===== */
@keyframes buzzShake{0%,100%{transform:translateX(0);}
  20%{transform:translateX(-9px);}40%{transform:translateX(9px);}
  60%{transform:translateX(-6px);}80%{transform:translateX(6px);}}
@keyframes msShake{0%,100%{transform:translateX(0);}
  20%,60%{transform:translateX(-7px);}40%,80%{transform:translateX(7px);}}
/* ===== FLN ANIMATION KIT: shake END ===== */
```

| Variant | Amplitude | Shape | Used on |
|---|---|---|---|
| `buzzShake` | ±9 → ±6 | 4-beat decaying | `.opt-cell.crossed` |
| `msShake` | ±7 | 2-beat constant | `.sort-item.shake-wrong`, `.opt-cell.wrong` |
| `tisShake` | ±6 | single | `.tis-hot.shake` |
| `shake` | ±8 | 2-beat | pattern slots - generic name (R7) |
| `matchShake` | ±7 | single | `.m-card.wrong` |
| `roadShake` | ±11 → ±5 | 4-beat decaying | wrong sticker drop |

Decaying 4-beat for a real error, constant 2-beat for a soft correction. Remove the class on
`animationend` so it can re-fire.

---

## 12. Hint glow (scaffold ladder)

**Reference only** - not installed, not in the preview.

```css
/* ===== FLN ANIMATION KIT: reveal-glow BEGIN ===== */
/* 1 soft nudge (2 iterations) */
@keyframes revealPulse{0%,100%{box-shadow:0 5px 12px rgba(0,177,50,.15);}
  50%{box-shadow:0 0 0 6px rgba(0,177,50,.28),0 10px 24px rgba(0,177,50,.30);}}
/* 2 sustained - holds until the child acts */
@keyframes revealHold{0%,100%{box-shadow:0 0 0 4px rgba(0,177,50,.20),0 5px 12px rgba(11,61,140,.10);}
  50%{box-shadow:0 0 0 12px rgba(0,177,50,.34),0 8px 20px rgba(0,177,50,.28);}}
/* 3 loudest - adds scale */
@keyframes answerGlow{0%,100%{box-shadow:0 0 0 4px rgba(0,177,50,.18),0 5px 12px rgba(11,61,140,.10);transform:scale(1);}
  50%{box-shadow:0 0 0 12px rgba(0,177,50,.32),0 8px 20px rgba(0,177,50,.28);transform:scale(1.04);}}
/* 4 expanding ring, tile stays put */
@keyframes optPulseRing{0%,100%{box-shadow:0 0 0 0 rgba(0,177,50,.50);opacity:1;}
  50%{box-shadow:0 0 0 13px rgba(0,177,50,0);opacity:.45;}}
/* drop zones */
@keyframes binGlow{0%,100%{box-shadow:0 0 0 4px rgba(0,177,50,.18);}
  50%{box-shadow:0 0 0 11px rgba(0,177,50,.34);}}
/* ===== FLN ANIMATION KIT: reveal-glow END ===== */
```

`headGlowPulse` lands on the bin's **header chip**, never the whole box - point at the label, don't
flood the container.

---

## 13. Phase gate (tutorial to guided to practice)

**Reference only** - not installed, not in the preview.

Stage blurs, headline appears, mascot rises from the bottom. Held ≥2s (3.5s before practice).

Source: `MTKGA02_L01_S01/app.js:3879-3905`

```css
/* ===== FLN ANIMATION KIT: phase-gate BEGIN ===== */
.phase-gate{position:fixed;inset:0;z-index:90;display:none;
  background:rgba(57,55,55,.35);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);}
.phase-gate.show{display:block;}
.phase-gate-title{position:absolute;left:50%;top:26%;transform:translateX(-50%);
  font-family:var(--font-hi);font-size:64px;font-weight:800;color:#E9268F;
  -webkit-text-stroke:9px #fff;paint-order:stroke fill;white-space:nowrap;
  animation:hintPop .4s cubic-bezier(.34,1.5,.6,1) both;}
.phase-gate img{position:absolute;left:50%;bottom:0;transform:translateX(-50%);
  animation:pgPeek .55s ease-out both;}
.stage.blurred{filter:blur(6px);transition:filter .3s ease;}
@keyframes pgPeek{from{transform:translateY(100%);}to{transform:translateY(0);}}
/* ===== FLN ANIMATION KIT: phase-gate END ===== */
```

```js
/* ===== FLN ANIMATION KIT: phase-gate BEGIN ===== */
(function(){ "use strict";
  var M = window.FLNMotion, _token = 0;
  M.phaseGate = {
    defaults:{ gate:"phaseGate", img:"phaseGateImg", titleEl:"phaseGateTitle", stage:"stage",
      art:"assets/UI/peeking_pal.webp", hold:2000, holdByPhase:{practice:3500},
      minHold:200, titles:{}, onVo:null },
    show: function(toPhase, done, opts){
      var o = Object.assign({}, this.defaults, opts || {});
      var tok = ++_token;                                   // guards against re-entry
      M.guard(function(){
        var gate = document.getElementById(o.gate), stage = document.getElementById(o.stage);
        if(!gate){ if(done) done(); return; }
        var img = document.getElementById(o.img);
        if(img) img.src = o.art + "?r=" + Date.now();        // restart the peek loop
        var t = document.getElementById(o.titleEl);
        if(t) t.textContent = o.titles[toPhase] || "";
        if(stage) stage.classList.add("blurred","gating");
        document.body.classList.add("gating");
        gate.classList.add("show");

        var openedAt = Date.now();
        var close = function(){
          gate.classList.remove("show");
          if(stage) stage.classList.remove("blurred","gating");
          document.body.classList.remove("gating");
        };
        var finish = function(){
          if(tok !== _token){ close(); return; }
          var want = o.holdByPhase[toPhase] || o.hold;
          var wait = Math.max(o.minHold, want - (Date.now() - openedAt));
          setTimeout(function(){
            if(tok !== _token){ close(); return; }
            gate.classList.remove("show");
            if(stage) stage.classList.remove("blurred");
            if(done) done();                                 // mount the next slide
            if(stage) stage.classList.remove("gating");       // header returns after
            document.body.classList.remove("gating");
          }, wait);
        };
        o.onVo ? o.onVo(toPhase, finish) : finish();
      });
    }
  };
})();
/* ===== FLN ANIMATION KIT: phase-gate END ===== */
```

**Gotchas** - the token guard is essential; without it two overlapping transitions both fire and two
slides mount. Minimum hold stops the gate flashing past when the VO is short or missing.

---

## 14. Boot loader (asset preload)

**Reference only** - not installed, not in the preview. **Asset-coupled** - the spinner is a pre-animated raster.
There is no CSS spin anywhere in the repo.

```css
/* ===== FLN ANIMATION KIT: boot-loader BEGIN ===== */
.boot-loader{position:fixed;inset:0;z-index:999;background:#fff;
  display:flex;align-items:center;justify-content:center;flex-direction:column;gap:18px;}
.boot-loader img{width:118px;height:118px;object-fit:contain;}   /* house standard */
.boot-loader.done{opacity:0;pointer-events:none;transition:opacity .4s ease;}
.boot-tap{opacity:.55;animation:bootTapPulse 1.4s ease-in-out infinite;}
@keyframes bootTapPulse{0%,100%{opacity:.55;}50%{opacity:1;}}
/* ===== FLN ANIMATION KIT: boot-loader END ===== */
```

- **118x118 is the standard.** Three conflicting `.boot-loader` rules were found in one file - append
  a final override so the size is unambiguous (R11).
- The preloader is byte-tracked streaming: `weightOf(u)` orders smallest-first, and **a failed asset
  counts its weight as done**, so a 404 can never strand the loader.
- Copy `HIKGH03_.../preloader.js` rather than reimplementing it.
- If an activity has a bespoke preloader UI, **ask before replacing it** - resize its logo in place.

---

## 15. Scene ambient sway (wind)

**Reference only** - not installed, not in the preview.

**The rule:** *a gust leaning one way and easing back reads as wind; an even left-right rock reads as
a metronome.* So: asymmetric 3-stop keyframes, `rotate` + `skewX`, never symmetric 2-stop.

```css
/* ===== FLN ANIMATION KIT: ambient-sway BEGIN ===== */
@keyframes decoPlantSway{
  0%,100%{transform:rotate(-1deg)  skewX(0.3deg);}
  35%    {transform:rotate(1.5deg) skewX(-0.7deg);}
  70%    {transform:rotate(0.2deg) skewX(-0.1deg);}
}
@keyframes decoCurtainBlow{            /* skewX not rotate - only the hem swings */
  0%,100%{transform:skewX(0.9deg)  scaleY(1);}
  42%    {transform:skewX(-2.4deg) scaleY(0.994);}   /* fabric shortens as it lifts */
  72%    {transform:skewX(-0.5deg) scaleY(1);}
}
@keyframes scCanopySway{
  0%,100%{transform:rotate(-0.7deg) skewX(0.4deg);}
  38%    {transform:rotate(1.05deg) skewX(-0.7deg);}
  70%    {transform:rotate(0.15deg) skewX(-0.1deg);}
}
.deco-plant{transform-origin:50% 94%;animation:decoPlantSway 5.6s ease-in-out infinite;}
.deco-curtain{animation:decoCurtainBlow 4.4s ease-in-out infinite;}
.sc-canopy{transform-origin:74px 159px;animation:scCanopySway 6.4s ease-in-out infinite;}
/* ===== FLN ANIMATION KIT: ambient-sway END ===== */
```

- **`transform-origin` is measured, not `center`** - the plant pivots at its pot base, the canopy at
  the trunk join. Wrong origin = the object detaches from its base.
- **Give neighbours coprime durations** (5.6s vs 4.4s) so they never pulse together.

---

## 16. Gleam sweep (voice-over highlight)

**Reference only** - not installed, not in the preview.

```css
/* ===== FLN ANIMATION KIT: shine BEGIN ===== */
@keyframes msShine{0%{top:-130%;left:-130%;}100%{top:110%;left:110%;}}
@keyframes trayShine{0%,15%{background-position:120% 120%;}55%,100%{background-position:-40% -40%;}}
@keyframes narratedShine{0%{background-position:83% 0;}55%,100%{background-position:17% 0;}}
@keyframes placeNameShine{0%,55%{left:-42%}85%,100%{left:120%}}
@keyframes narratedPolish{
  0%,100%{filter:saturate(1.16) brightness(1.04) contrast(1.03);}
  48%{filter:saturate(1.12) brightness(1.13) contrast(1.05) drop-shadow(0 0 4px rgba(225,234,244,.72));}
}
/* ===== FLN ANIMATION KIT: shine END ===== */
```

`narratedShine`'s range was retuned from 140%→−60% to 83%→17% - the wider sweep spent most of its
duration off-element.

---

## 17. Start screen entry (mascot, button, concepts)

**Reference only** - not installed, not in the preview.

```css
/* ===== FLN ANIMATION KIT: landing-entry BEGIN ===== */
@keyframes sgFloat{0%,100%{transform:translateY(0);}50%{transform:translateY(-8px);}}
@keyframes sgBtnPulse{0%,100%{transform:translateX(-50%) scale(1);}
  50%{transform:translateX(-50%) scale(1.03);}}
@keyframes sgBtnIn{0%{transform:translateX(-50%) scale(1);}
  45%{transform:translateX(-50%) scale(1.10);}100%{transform:translateX(-50%) scale(1);}}
@keyframes sgVoPulse{0%,100%{transform:scale(1);}50%{transform:scale(1.09);}}
@keyframes fingerPop{0%{opacity:0;transform:scale(.2);}
  70%{opacity:1;transform:scale(1.18);}100%{opacity:1;transform:scale(1);}}

.sg-mascot{animation:sgFloat 2.6s ease-in-out infinite;}
.sg-btn{animation:sgBtnPulse 1.4s ease-in-out infinite;}
.sg-btn.vo-ready{animation:sgBtnIn .5s cubic-bezier(.34,1.5,.6,1),
                           sgBtnPulse 1.4s ease-in-out .5s infinite;}
.sg-vo{animation:sgVoPulse 1.5s ease-in-out infinite;}
.sg-fcell{opacity:0;animation:fingerPop .5s cubic-bezier(.34,1.5,.6,1) both;
  animation-play-state:paused;}                  /* paused until preload finishes */
body.loaded .sg-fcell{animation-play-state:running;}
body.loaded .sg-fcell:nth-child(1){animation-delay:.15s;}
body.loaded .sg-fcell:nth-child(2){animation-delay:.60s;}
body.loaded .sg-fcell:nth-child(3){animation-delay:1.05s;}
/* ===== FLN ANIMATION KIT: landing-entry END ===== */
```

> **Several of these are DEAD in shipped games.** A blanket rule at
> `MTKGA01_L01_S01/style.css:2378-2382` kills `animation` on `.sg-mascot`, `.sg-btn`, `.audio-chip`
> and others in MTKGA01/MTKGA02. They work in the `_dist` files. The chip throb was separately
> disabled on purpose: *"the button must not move while a clip plays."* Decide which behaviour you
> want - a rule being present does not mean it runs.

---

## 18. Block Town block drop (counting)

**Reference only** - not installed, not in the preview.

```css
@keyframes blkDrop{0%{transform:translateY(-72px) scaleY(.82);opacity:.35;}
  70%{transform:translateY(0) scaleY(1.12);}          /* squash/stretch on landing */
  100%{transform:translateY(0) scaleY(1);opacity:1;}}
@keyframes btDust{0%{opacity:.85;transform:translate(-50%,0) scale(.6);}
  100%{opacity:0;transform:translate(-50%,-20px) scale(1.35);}}
@keyframes rocketGo{0%{transform:translate(-50%,0);}
  100%{transform:translate(-50%,-420px) scale(.65);opacity:0;}}
```

```js
/* pitch climbs one step per block - the child HEARS the count go up */
function btThunk(n){ tone([360 + n*46], "sine", 0.12, 0.10); }
```

The idea worth stealing: **the audio encodes the quantity.** The slide prompt plays first, then the
count sequence, so the counting VO never cuts the prompt off.

---

## 19. Correct answer select (tile confirm)

**▶ Preview:** `index.html#correct-select` · **Built** - supersedes recipe 9

The beat that fires the instant a child taps the right tile. Recipe 7 (confetti) is the
room-level celebration; this is the tile-level *confirmation*, and the two are meant to run
together. Source of the original: `MTKGA01_L01_S01/style.css:541,659`.

### Why the shipped confirm reads as arbitrary

| Shipped | Why it fails |
|---|---|
| `correctPop` - `scale(1)` → `1.08` → `1` | Symmetric, no anticipation, no settle. Nothing *causes* it, so it reads as a hiccup rather than as the tile locking in. |
| Green flood, `background:var(--correct-bg)` | Floods the tile the child is reading. The house rule already says the outline **is** the mark (recipe 9) - 5 of 7 activities still fill. |
| 64px ✓ badge (`.opt-cell.correct::after`) | House rule: no tick. Still live in MTKGA01. |
| `sparkFly` | Present in MTK01 and **dead** - killed by a blanket `animation:none`. |
| Everything at once | Pop, colour and confetti all start on the same frame, so nothing appears to cause anything else. |

### The idea: one causal chain, not three effects

```
0ms      tap  → the border turns green (70ms) and the tile presses IN
216ms    a crown of sparks lifts off the TOP edge
272ms    the pop peaks
544ms    the tile stops moving
792ms    the last spark clears
∞        the green outline stays - it is the correct-mark
```

**No rings, in either direction.** Earlier passes had one converging inward and two
pulsing outward; all three were cut after looking at them on a real tile. At tile
scale an extra ring reads as a flicker at the edge of the thing you are trying to
look at, not as part of it - and the confetti (recipe 7) already owns the
celebratory register. What is left is the tile itself: colour, a press, a pop, and
a few sparks.

Every duration derives from `--ckT`, and `--ckT` derives from the shared `--fx-beat`
tempo above - so the whole pair retimes from one number. The pop peak lands on the
converge by construction: `50%` of `.68 × --ckT` is the same instant as `34%` of
`--ckT`, whatever `--fx-beat` is set to.

```
.ck-correct        the tile      border-color + ckPop
  <i class=ck-fx>                inset:0, pointer-events:none
     <i class=ck-crown> <i> x5   sparks
```

```css
/* ===== FLN ANIMATION KIT: answer-tempo BEGIN ===== */
/* ONE tempo for all answer feedback. Both effects derive every duration from these
   two numbers, so they cannot drift apart - change --fx-beat and the whole pair
   retimes together; change --fx-reward and only the correct beat moves.
   --fx-beat is the shipped buzzShake tempo (.4s) and is the anchor: the wrong
   answer runs exactly one beat, the correct answer runs --fx-reward of them. */
:root{
  --fx-beat:.4s;
  --fx-reward:2;
}
/* ===== FLN ANIMATION KIT: answer-tempo END ===== */

/* ===== FLN ANIMATION KIT: correct-select BEGIN ===== */
/* NO RINGS. The confirm is the tile's own border turning green, the tile pressing
   in and popping back, and a few sparks lifting off its top edge - nothing else.
   Earlier passes had a ring converging inward and two halos pulsing outward; both
   were cut. On a small tile any extra ring reads as a flicker rather than as part
   of the tile, and the confetti (recipe 7) already covers the celebratory register.
   Every duration derives from --ckT, so retiming the beat is one number. */
.ck-correct{
  --ckT:calc(var(--fx-beat) * var(--fx-reward));   /* 2 beats = 800ms */
  overflow:visible !important;                  /* the halo leaves the box - see Gotchas */
  z-index:6;                                    /* ...and must not slide under a neighbour */
  /* HOUSE RULE: the green outline IS the correct-mark. No fill, no tick.
     Put on the tile's OWN border, as recipe 9 does - a separate ring layer would
     sit inside the existing border and leave a grey rim around it. It also means
     the mark survives `transition:none!important`: a killed transition still lands
     on its end value, where a killed `animation ... both` never applies one (R5). */
  background:var(--ck-face,#fff) !important;
  border-color:var(--correct,#00B132) !important;
  box-shadow:0 6px 16px rgba(0,177,50,.16) !important;
  /* 70ms, matched with .wg-wrong: the verdict colour is the most important thing
     on screen and must land inside the ~100ms "instantaneous" window. The softness
     comes from the motion, not from ramping the colour. */
  transition:border-color .07s linear, box-shadow .2s ease !important;
  /* NOT the house cubic-bezier(.34,1.5,.6,1): a timing function runs between
     EVERY pair of keyframes, so an overshooting spring applied to a four-stop
     pop overshoots four times and the anticipation dip never reads. The spring
     is already shaped by the percentages below - the easing just joins them. */
  animation:ckPop calc(var(--ckT) * .68) ease-in-out both;
}
.ck-correct::after{content:none !important;display:none !important;}   /* no tick */

.ck-fx{position:absolute;inset:0;border-radius:inherit;pointer-events:none;z-index:2;}
.ck-fx > i{position:absolute;inset:0;border-radius:inherit;}

/* THE CROWN - sparks over the TOP ARC only. A full 360 ring competes with the
   screen-wide confetti; a crown stays local and reads as lift. */
.ck-crown{overflow:visible;}
.ck-crown i{position:absolute;left:50%;top:50%;width:var(--ss);height:var(--ss);
  margin:calc(var(--ss) / -2) 0 0 calc(var(--ss) / -2);
  background:var(--ck-spark,#FFC93C);
  clip-path:polygon(50% 0%,61% 35%,98% 35%,68% 57%,79% 91%,
                    50% 70%,21% 91%,32% 57%,2% 35%,39% 35%);
  animation:ckSpark calc(var(--ckT) * .72) cubic-bezier(.15,.7,.35,1)
            calc(var(--ckT) * .27) both;}

@keyframes ckPop{
  0%  {transform:scale(1);}
  11% {transform:scale(.966);}    /* ANTICIPATION - the tap presses the tile in  */
  50% {transform:scale(1.055);}   /* peak, 272ms at the default tempo            */
  72% {transform:scale(.992);}    /* one counter-bounce: a spring decays         */
  100%{transform:scale(1);}
}
/* --x0/--y0 put each spark ON the tile's edge to begin with. Launching from the
   centre (the obvious version) sends every spark straight across the digit the
   child is reading - the sparks are decoration and must never cross the content. */
@keyframes ckSpark{
  0%  {transform:translate(var(--x0),var(--y0)) scale(.3) rotate(0deg);opacity:0;}
  25% {opacity:1;}
  100%{transform:translate(var(--sx),var(--sy)) scale(1) rotate(var(--sr));opacity:0;}
}
/* R5 - the decoration goes, the MARK stays. The border-color above already
   survives the kill-switch; these just stop the dead layers rendering as
   stationary green hoops parked at their `both` start state. */
html.no-anim .ck-crown{display:none;}
@media (prefers-reduced-motion: reduce){
  .ck-crown{display:none;}
}
/* ===== FLN ANIMATION KIT: correct-select END ===== */
```

```js
/* ===== FLN ANIMATION KIT: correct-select BEGIN ===== */
(function(){ "use strict";
  var M = window.FLNMotion;
  function rnd(a, b){ return a + Math.random() * (b - a); }
  function mk(cls){ var i = document.createElement("i"); i.className = cls; return i; }

  /* Every deferred step is parked ON THE TILE so clear() can cancel it. Without this
     a second play inherits the FIRST play's pending timers and they strip the state
     off the new beat part-way through. Owning the timers is what makes these safely
     re-fireable, which the 2-attempt ladder needs. */
  function later(el, fn, ms){ (el._selT = el._selT || []).push(setTimeout(fn, ms)); }

  /* Tempo lives in CSS (--fx-beat / --fx-reward) so the two effects cannot drift
     apart. JS reads it rather than keeping a second copy, and only writes --ckT or
     --wgT when a caller explicitly passes `dur`. Custom properties do not resolve
     calc(), so the two numbers are read and multiplied here rather than reading
     the composed value. */
  function tempo(el){
    var cs = getComputedStyle(el);
    function num(p, d){
      var v = parseFloat(cs.getPropertyValue(p));
      if(!v && v !== 0) return d;
      return v > 20 ? v / 1000 : v;              /* tolerate ms as well as s */
    }
    var beat = num("--fx-beat", 0.4);
    return { beat: beat, reward: beat * (parseFloat(cs.getPropertyValue("--fx-reward")) || 2) };
  }

  M.answer = {
    clear: function(el){
      if(!el) return;
      if(el._selT){ for(var j = 0; j < el._selT.length; j++) clearTimeout(el._selT[j]); }
      el._selT = [];
      el.classList.remove("ck-correct", "wg-wrong", "wg-out", "wg-rel");
      var fx = el.querySelectorAll(".ck-fx,.wg-fx");
      for(var i = 0; i < fx.length; i++) fx[i].remove();
    }
  };

  M.correctSelect = {
    defaults:{ crown:5 },      /* dur comes from CSS unless you pass one */
    play: function(el, opts){
      var o = Object.assign({}, this.defaults, opts || {});
      M.guard(function(){
        if(!el) return;
        M.answer.clear(el);
        void el.offsetWidth;                 /* forced reflow - restarts the pop */
        var dur = o.dur || tempo(el).reward;            /* CSS owns the tempo */
        if(o.dur) el.style.setProperty("--ckT", dur + "s");

        var fx = mk("ck-fx");

        if(o.crown && !M.still()){
          var cr = mk("ck-crown");
          /* clientWidth is layout px INSIDE the scaled stage - design px already.
             getBoundingClientRect() would come back multiplied by --scale (R1). */
          var w = el.clientWidth || 96, h = el.clientHeight || 96;
          var rx = w * 0.46, ry = h * 0.46;               /* the tile's own edge */
          for(var i = 0; i < o.crown; i++){
            var t  = (o.crown === 1) ? 0.5 : i / (o.crown - 1);
            var a  = (-158 + t * 136 + rnd(-7, 7)) * Math.PI / 180;   /* TOP arc */
            var x0 = Math.cos(a) * rx, y0 = Math.sin(a) * ry;
            var out = rnd(.20, .34);
            var s = mk("");
            s.style.cssText =
              "--ss:" + rnd(7, 12).toFixed(1) + "px;" +
              "--x0:" + x0.toFixed(1) + "px;" +
              "--y0:" + y0.toFixed(1) + "px;" +
              "--sx:" + (x0 + Math.cos(a) * w * out).toFixed(1) + "px;" +
              "--sy:" + (y0 + Math.sin(a) * h * out).toFixed(1) + "px;" +
              "--sr:" + Math.round(rnd(-140, 140)) + "deg;";
            cr.appendChild(s);
          }
          fx.appendChild(cr);
        }

        /* class FIRST: the border and the pop are the feedback, and they must not
           wait on ~9 nodes of decoration being built. Measured 45ms of dead time
           before any pixel moved when this ran the other way round. */
        el.classList.add("ck-correct");
        el.appendChild(fx);
        /* Only the TRANSIENT layers are swept. .ck-correct stays: the green outline
           is the correct-mark and it belongs to the tile until the slide advances. */
        later(el, function(){
          var t = fx.querySelectorAll(".ck-crown");
          for(var i = 0; i < t.length; i++) t[i].remove();
        }, dur * 1050);
      });
    }
  };
})();
/* ===== FLN ANIMATION KIT: correct-select END ===== */
```

### Tempo - both effects, one number

`--fx-beat` is the shared tempo and `--fx-reward` is how many beats the reward gets.
Nothing else carries a duration, so the pair cannot drift apart:

| | derives from | at the default `.4s` |
|---|---|---|
| wrong: shake | `1 × --fx-beat` | 400ms |
| wrong: hold, then release | `×1.5` then 220ms | red gone by ~900ms |
| correct: tile pop | `.68 × --ckT` | 544ms |
| correct: pop peak | `.34 × --ckT` | 272ms |
| correct: last spark clears | `.99 × --ckT` | 792ms |

`--fx-beat` is anchored to the shipped `buzzShake` tempo and should not move without a
reason - the fleet's other feedback is built on it. `--fx-reward` is the dial for "the
correct answer feels too fast / too slow": raise it and only the reward stretches.
**The JS reads these from CSS** rather than keeping its own copy, so there is exactly
one place to change them.

### Options

| Key | Default | Effect |
|---|---|---|
| `dur` | from CSS | The whole beat, seconds. Defaults to `--fx-beat × --fx-reward` (800ms) read from the stylesheet - pass it only to override one call. Every layer is a fraction of it. |
| `crown` | `5` | Sparks on the top arc. `0` turns them off. Above ~8 it stops reading as a crown and starts competing with the confetti. |
| `--ck-face` | `#fff` | Tile face. Set it if the activity's tiles are not white. |
| `--ck-spark` | `#FFC93C` | Spark colour. |
| `--correct` | `#00B132` | Existing token (R8). |

### Tuning notes

- **The press is what makes it feel caused.** With the rings gone, the only thing tying the pop
  to the child's finger is the anticipation dip - the tile compresses first, then rebounds. Cut
  the dip and you get a tile that inflates for no reason.
- **The anticipation dip is 3.4%, and it is not optional.** `scale(.966)` at 11% is what makes
  the tile feel *pressed* rather than spontaneously inflated. It is below conscious threshold
  and it carries most of the "caused by my finger" reading.
- **Don't use the house spring here.** `cubic-bezier(.34,1.5,.6,1)` is for a two-stop pop. A
  timing function runs between *every* pair of keyframes, so an overshooting curve on a
  four-stop pop overshoots four times and the dip never reads. The spring is already shaped
  by the percentages; the easing just joins them.
- **Sparks launch from the border, never the centre.** `--x0/--y0` put each spark on the tile
  edge first. Launching from the middle - the obvious version - sends every spark straight
  across the digit or word the child is reading.
- **Runs with recipe 7, not instead of it.** The confetti is gated to guided/practice/mastery;
  in tutorial this tile beat is the only feedback there is, which is why `crown` defaults on.

### Gotchas

- **`overflow:visible !important` is on `.ck-correct`.** The sparks leave the box. If the tile
  clips art at its border-radius by design, that art will bleed for the ~800ms the class is on
  - set `crown:0` and drop the overflow rule together, never the rule on its own.
- **A delayed layer must not use `both`.** Backwards-fill paints its 0% state throughout the
  delay, so a delayed ring sits on the tile as a static hoop from frame zero. This is why the
  sparks' 0% keyframe is `opacity:0`. An earlier version had two delayed outward halos and
  they showed exactly this defect before being cut for other reasons.
- **Re-firing needs the reflow.** Removing and re-adding the class in the same frame does not
  restart a CSS animation; `void el.offsetWidth` between them does.
- **The mark rides `border-color`, deliberately.** A separate ring layer at `inset:0` sits
  *inside* the tile's own border and leaves a grey rim around it. Putting the green on the
  border also means it survives `transition:none!important` - a killed transition still lands
  on its end value, where a killed `animation … both` never applies one (R5).
- **Call `FLNMotion.answer.clear(el)` when the slide advances**, or the outline persists into
  the next question.

---

## 20. Wrong answer select (tile correction)

**▶ Preview:** `index.html#wrong-select` · **Built** - supersedes recipe 11

Two states, because the fleet has two: a **transient** correction that releases the tile back
to tappable, and **elimination**, which stays. They map onto `.opt-cell.wrong` and
`.opt-cell.crossed`.

### What this keeps, and what it changes

| | Shipped | Here |
|---|---|---|
| Motion | lateral `translateX` buzz, `.4s` | **kept** - same idiom, same tempo |
| Amplitude | `msShake` holds a flat ±7 for 4 beats | decays −9 → +8 → −5.5 → +3 → 0 |
| Consistency | 6 keyframes doing one job (`buzzShake`, `msShake`, `tisShake`, `shake`, `matchShake`, `roadShake`), different amplitudes inside the same activity | one |
| Colour | red flood, `background:var(--wrong-bg)` | outline only |
| Cross | 110px ✕ overlay, then `content:none !important` two thousand lines later | none |
| Eliminated | `opacity:.5`, then `opacity:1 !important` overriding it | desaturate to `.3`, opacity `.72` |
| Ending | red persists | **releases** - the child has another attempt |

**The release is the point.** A wrong tile that stays red teaches "that one is gone"; the
2-attempt ladder needs it to look tappable again. Red arrives in ~100ms, holds through the
shake and ~240ms past it, then fades out by ~900ms - which is where the correct
beat also finishes, so the two resolve together.

**Elimination recedes by desaturating, not dimming.** `opacity:.5` makes the tile's own word
or digit unreadable on a low-brightness tablet in a bright classroom - which is exactly why a
later rule already forces it back to `opacity:1 !important` in MTKGA01 and MTKGA01_S03.

```css
/* ===== FLN ANIMATION KIT: wrong-select BEGIN ===== */
/* Two states, because the fleet has two: `.wg-wrong` is a TRANSIENT correction that
   RELEASES the tile back to tappable, `.wg-out` is elimination and stays. */
.wg-wrong,.wg-out{
  --wgT:var(--fx-beat);                         /* exactly one beat */
  overflow:visible !important;
  z-index:5;
  background:var(--wg-face,#fff) !important;    /* no red flood */
  border-color:var(--wrong,#F93544) !important;
  transition:border-color .07s linear !important;   /* matched with .ck-correct */
}
.wg-wrong::after,.wg-out::after{content:none !important;display:none !important;}  /* no cross */
.wg-wrong{box-shadow:0 6px 16px rgba(249,53,68,.16) !important;
  animation:wgNo var(--wgT) ease-in-out both;}
.wg-out{pointer-events:none;box-shadow:none !important;
  animation:wgNoOut calc(var(--wgT) * 1.6) ease-in-out both,
            wgFade  calc(var(--wgT) * 1.6) ease-out both;}

.wg-fx{position:absolute;inset:0;border-radius:inherit;pointer-events:none;z-index:2;}
.wg-fx > i{position:absolute;inset:0;border-radius:inherit;}
/* one soft outward pulse, so the "no" has a source instead of just a wobble */
.wg-pulse{border:3px solid var(--wrong,#F93544);
  animation:wgPulse calc(var(--wgT) * .62) ease-out both;}
.wg-out .wg-pulse{animation-duration:calc(var(--wgT) * .5);}

/* Lateral buzz at the shipped tempo - buzzShake .4s, +-9 then +-6
   (MTKGA01/style.css:662). Keeping that character matters more than being clever:
   an earlier pass here pivoted the tile about its base like a head shaking "no",
   which is truer to the gesture but reads slow and soft beside the rest of the
   fleet.
   What this DOES change is the decay. -9 -> +8 -> -5.5 -> +3 -> 0, where msShake
   holds a flat +-7 for four beats: real oscillation loses energy, and a constant
   amplitude reads as a machine buzzing rather than as a correction.
   ease-in-out, because a turning point is a turning point - velocity is zero at
   each reversal. */
@keyframes wgNo{
  0%  {transform:translateX(0);}
  18% {transform:translateX(-9px);}
  38% {transform:translateX(8px);}
  60% {transform:translateX(-5.5px);}
  80% {transform:translateX(3px);}
  100%{transform:translateX(0);}
}
/* Same shake, then it settles SMALLER and stays there. One element owns exactly
   ONE transform animation - a second `animation` also touching transform would
   silently win outright and drop the shake. That is why the fade below is
   filter + opacity only. */
@keyframes wgNoOut{
  0%  {transform:translateX(0)     scale(1);}
  11% {transform:translateX(-9px)  scale(1);}
  24% {transform:translateX(8px)   scale(1);}
  37% {transform:translateX(-5.5px)scale(1);}
  50% {transform:translateX(3px)   scale(1);}
  62% {transform:translateX(0)     scale(1);}
  100%{transform:translateX(0)     scale(.965);}
}
/* Recede by DESATURATING, not by dimming. The shipped opacity:.5 makes the tile's
   own word or digit unreadable on a low-brightness tablet in a bright classroom -
   which is exactly why a later rule already forces it back to opacity:1 !important
   in MTKGA01 and MTKGA01_S03. This keeps the content legible and still recedes. */
@keyframes wgFade{
  0%,52%{filter:saturate(1);opacity:1;}
  100%  {filter:saturate(.3);opacity:.72;}
}
@keyframes wgPulse{
  0%  {transform:scale(1.02);opacity:.65;}
  100%{transform:scale(1.16);opacity:0;}
}
/* THE RELEASE needs a class of its own. Dropping .wg-wrong also drops the
   transition declared on it, so the red would snap off in one frame; .wg-rel is
   added just before .wg-wrong comes off and outlives it by one transition, which
   is what turns the release into a fade. It also needs no knowledge of whatever
   neutral border colour the host activity uses. */
.wg-rel{transition:border-color .22s ease, box-shadow .22s ease !important;}

/* R5 - the red mark rides border-color, so it survives the kill-switch. What has
   to survive in JS is the RELEASE: animationend never fires under no-anim, so the
   class comes off on a timeout instead, or the tile stays red forever. */
html.no-anim .wg-pulse{display:none;}
html.no-anim .wg-out{opacity:.72;filter:saturate(.3);}
@media (prefers-reduced-motion: reduce){
  .wg-pulse{display:none;}
  .wg-out{opacity:.72;filter:saturate(.3);}
}
/* ===== FLN ANIMATION KIT: wrong-select END ===== */
```

```js
/* ===== FLN ANIMATION KIT: wrong-select BEGIN ===== */
/* needs the `later`, `tempo` and `M.answer.clear` helpers from recipe 19 */
(function(){ "use strict";
  var M = window.FLNMotion;
  function mk(cls){ var i = document.createElement("i"); i.className = cls; return i; }
  function later(el, fn, ms){ (el._selT = el._selT || []).push(setTimeout(fn, ms)); }

  M.wrongSelect = {
    defaults:{},               /* dur comes from CSS unless you pass one */

    /* transient: shakes, holds red, then RELEASES */
    play: function(el, opts){
      var o = Object.assign({}, this.defaults, opts || {});
      M.guard(function(){
        if(!el) return;
        M.answer.clear(el);
        void el.offsetWidth;
        var dur = o.dur || tempo(el).beat;              /* CSS owns the tempo */
        if(o.dur) el.style.setProperty("--wgT", dur + "s");
        el.classList.add("wg-wrong");          /* class first - see recipe 19 */
        var fx = mk("wg-fx"); fx.appendChild(mk("wg-pulse"));
        el.appendChild(fx);
        /* RELEASE on a timeout, never on animationend: under the reduced-motion kill
           switch animationend never fires and the tile would stay red forever - on
           exactly the devices least able to recover from it. (R5, second half.)
           .wg-rel goes on BEFORE .wg-wrong comes off so the border has something to
           transition with. */
        later(el, function(){
          el.classList.add("wg-rel");
          el.classList.remove("wg-wrong");
          var f = el.querySelector(".wg-fx"); if(f) f.remove();
          later(el, function(){
            el.classList.remove("wg-rel");
            if(o.then) o.then();
          }, 260);
        }, dur * 1500 + 40);
      });
    },

    /* elimination: shakes once, recedes, and STAYS recessed. No auto-clear. */
    out: function(el, opts){
      var o = Object.assign({}, this.defaults, opts || {});
      M.guard(function(){
        if(!el) return;
        M.answer.clear(el);
        void el.offsetWidth;
        var dur = o.dur || tempo(el).beat;
        if(o.dur) el.style.setProperty("--wgT", dur + "s");
        el.classList.add("wg-out");
        var fx = mk("wg-fx"); fx.appendChild(mk("wg-pulse"));
        el.appendChild(fx);
      });
    }
  };
})();
/* ===== FLN ANIMATION KIT: wrong-select END ===== */
```

### Options

| Key | Default | Effect |
|---|---|---|
| `dur` | `0.4` | The shake, seconds - the shipped `buzzShake` tempo. The hold and release derive from it (`×1.5` then a 220ms fade). |
| `then` | – | Called after the release completes. Use it to re-enable the tap gate. |
| `--wg-face` | `#fff` | Tile face. |
| `--wrong` | `#F93544` | Existing token (R8). |

### Gotchas

- **One element, one transform animation.** `.wg-out` runs `wgNoOut` *and* `wgFade`; the fade
  is `filter`+`opacity` only for exactly this reason. A second `animation` also touching
  `transform` silently wins outright and the shake disappears - it does not blend.
- **The release needs `.wg-rel`.** Dropping `.wg-wrong` also drops the transition declared on
  it, so the red snaps off in one frame. `.wg-rel` is added just before and outlives it by one
  transition. It also needs no knowledge of the host's neutral border colour.
- **Cancel the timers on re-fire.** Tap a wrong tile twice and, without `M.answer.clear`
  cancelling the pending release, the first play's timer strips the state off the second beat
  part-way through and the shake dies half way. This is a real defect, found in the preview.
- **Don't stack this on an existing `.wrong` rule.** Several activities already set
  `border-color … !important` on `.opt-cell.wrong` (e.g. `HI01H05/style.css:1164`); an
  `!important` author declaration beats a keyframe, so leave the old class off the element or
  remove its rule. Grep every rule for the selector first (R11).
- **`transform-origin` is not set.** An earlier pass pivoted the tile about its base like a
  head shaking "no" - truer to the gesture, but it reads slow and soft beside the rest of the
  fleet. If you revive it, retime the whole beat with it.

---

## 21. Tap the object - outline on any shape

**▶ Preview:** `index.html#object-outline` (engine A only - the engine B tile was
removed) · **Built** · generalises recipe 10, which did this for one activity only

"Tap the right thing in the picture", where every target is a different shape - a girl,
a parrot, a banana, a cupboard. **White** outline at rest so the child can see what is
tappable, **red + wiggle** when wrong, **green** when correct.

The whole problem is that the objects have nothing in common. This ships one set of
state classes over **two engines**, so a game can mix both in one scene and the states
still behave identically.

| | engine A `.ol-alpha` | engine B `.ol-band` |
|---|---|---|
| the object is | its own element, with real transparency | a **region of a baked scene raster** |
| outline comes from | the browser, off the element's own alpha | a pre-baked full-frame ring, painted through a mask |
| per-object asset | **none** | one ~1KB ring band |
| thickness | live, `--ol-w` | baked into the asset |
| art gets replaced | outline follows automatically | regenerate the band |
| wrong answer | **wiggles** | **flashes** - see Gotchas |

Prefer A. Use B only when the object genuinely cannot be separated from the scene -
which, in this fleet, is most of the time.

### What engine B replaces

`HIKGH01_L02_S03` today ships a **second copy of the whole scene** with the white
outlines painted into it, and swaps the `<img>`:

| | bytes |
|---|---|
| `scene_1_aangan.webp` + `scene_1_aangan_tap.webp` | 119,772 + 113,792 |
| `scene_2_hurt.webp` + `scene_2_hurt_tap.webp` | 143,488 + 140,176 |
| **the `_tap` duplicates alone** | **253,968** |
| the 5 ring bands doing the same job | **5,108** |

**50x**, and the duplicates buy less: the outline colour is baked, so a `_tap` scene
can only ever be white. Red for wrong and green for correct would need two more full
scenes each, and objects cannot be outlined **individually** at all - the whole scene
is outlined or none of it is. A band is per-object and the colour is live.

(Diffing `scene_1_aangan.webp` against its `_tap` twin shows the changed region is the
entire frame - it was re-encoded, not patched - so there is no cheap way to ship the
pair as a delta either.)

**When you would not need engine B:** if the art pipeline delivered a character-free
background plate plus cut-out sprites, engine A would cover everything and no bands
would exist. It does not today - every scene in the folder has its cast painted in,
and there is no clean plate to composite onto. That is an art decision, not a code
one, and it is the thing to change if you want this to get simpler.

### Why the outline is computed, never traced

Hand-tracing paths is why the untidy outline kept coming back in `HI01H01_L02_S04`.
Engine A never has a path at all; engine B derives one from the silhouette by
morphology (`tools/make-ring.py`). Neither can drift out of register with the art.

### Engine A - four passes, and not eight

Chained `drop-shadow`s **dilate**: each pass also shadows the previous passes' output.
Four axis-aligned zero-blur passes give a clean square-kernel dilation of exactly
`--ol-w`. Adding the four diagonals looks like the obvious improvement and is not -
the diagonals compound, the stroke blooms to roughly twice the requested thickness,
and it welds shut the gap between a character's arm and body. Rendered side by side on
five real sprites before choosing; the fifth pass is a soft glow, which is what keeps a
white outline readable against a pale wall.

```css
/* ===== FLN ANIMATION KIT: object-outline BEGIN ===== */
/* "Tap the right thing", where every target is a DIFFERENT shape.

   TWO ENGINES, one set of state classes. `.is-correct` / `.is-wrong` / `.is-muted`
   mean the same thing and are driven the same way whichever engine a target uses,
   so a game can mix them in one scene:

     .ol-alpha  the object is its OWN element with real transparency. The outline is
                computed from its alpha by the browser - no traced path, no exported
                ring, any silhouette, and it stays correct if the art is replaced.
                It CAN wiggle: the outline is the element's own filter, so it travels
                with the art.

     .ol-band   the object is a REGION of a baked scene raster. It cannot be moved or
                filtered on its own, so the outline is a pre-baked full-frame ring
                painted through a mask, and the wrong-answer beat is a FLASH, not a
                wiggle. Transforming it would slide the ring off the art it traces -
                see Gotchas, this is the defect the whole approach exists to avoid.

   Colour is the only thing a state changes: everything reads --ol-c. */
.ol{
  --ol-w:4px;                       /* stroke thickness, design px */
  --ol-soft:5px;                    /* separation glow; set 0 on low-end devices */
  --ol-idle:#FFFFFF;                /* "this is tappable" */
  --ol-c:var(--ol-idle);            /* the ONE property a state changes */
  --ol-amp:8px;                     /* wiggle travel */
  --olT:var(--fx-beat,.4s);         /* SAME tempo token as recipes 19 + 20 */
  cursor:pointer;
  -webkit-tap-highlight-color:transparent;
}
.ol.is-correct{--ol-c:var(--correct,#00B132);}
.ol.is-wrong  {--ol-c:var(--wrong,#F93544);}
.ol.is-muted  {--ol-c:rgba(255,255,255,.30);--ol-soft:0px;}

/* ---------- ENGINE A - outline from the object's own alpha ---------- */
/* FOUR axis-aligned zero-blur passes. Chained drop-shadows dilate, so four axis
   passes give a clean square-kernel dilation of exactly --ol-w. Do NOT "improve"
   this by adding the four diagonals: each pass also shadows the previous passes'
   output, so diagonals compound and the stroke blooms to ~2x thickness and welds
   shut the gaps between a character's arm and body. Measured, not guessed.
   The fifth pass is a soft glow - it is what separates a white outline from a
   pale background in a busy scene. Set --ol-soft:0 to drop it (4 passes). */
.ol-alpha{
  filter:
    drop-shadow( var(--ol-w) 0 0 var(--ol-c))
    drop-shadow(calc(var(--ol-w) * -1) 0 0 var(--ol-c))
    drop-shadow(0  var(--ol-w) 0 var(--ol-c))
    drop-shadow(0 calc(var(--ol-w) * -1) 0 var(--ol-c))
    drop-shadow(0 0 var(--ol-soft) var(--ol-c));
  /* 70ms at the default beat - matched with the tile marks in recipes 19/20.
     This is a ONE-OFF transition on a single element, not a running animation:
     the kit's standing objection to animating `filter` is about the landing sky
     doing it forever on ~87 elements, which is a different thing. */
  transition:filter calc(var(--olT) * .175) linear;
  transform-origin:var(--ol-origin,50% 100%);   /* scene objects rest on something */
}
.ol-alpha.is-wrong  {animation:olNo  var(--olT) ease-in-out both;}
.ol-alpha.is-correct{animation:olYes calc(var(--olT) * 1.35) ease-in-out both;}

/* Same decaying lateral buzz as the tile wrong-answer (recipe 20), to the same
   ratios, so the two mechanics speak one language. Amplitude is a variable
   because a 60px object and a 300px character cannot share a pixel figure. */
@keyframes olNo{
  0%  {transform:translateX(0);}
  18% {transform:translateX(calc(var(--ol-amp) * -1));}
  38% {transform:translateX(calc(var(--ol-amp) * .89));}
  60% {transform:translateX(calc(var(--ol-amp) * -.61));}
  80% {transform:translateX(calc(var(--ol-amp) * .33));}
  100%{transform:translateX(0);}
}
/* Same shape as ckPop (recipe 19): anticipation dip, peak, one counter-bounce. */
@keyframes olYes{
  0%  {transform:scale(1);}
  11% {transform:scale(.97);}
  50% {transform:scale(1.06);}
  72% {transform:scale(.995);}
  100%{transform:scale(1);}
}

/* ---------- ENGINE B - pre-baked ring band over a scene raster ---------- */
/* No preview tile: the band demo was removed from index.html. These rules are
   kept so the block stays one pasteable unit and matches recipe 21 verbatim. */
/* One full-frame alpha per object, painted through as a mask, so a single asset
   serves idle, correct, wrong and muted just by changing the colour under it. */
.ol-band{
  position:absolute; inset:0; pointer-events:none;
  background:var(--ol-c);
  -webkit-mask:var(--ol-band) center/100% 100% no-repeat;
          mask:var(--ol-band) center/100% 100% no-repeat;
  transition:background-color calc(var(--olT) * .175) linear, opacity .2s ease;
  filter:drop-shadow(0 0 var(--ol-soft) var(--ol-c));
}
/* NEVER put a transform on this. It is a full-frame mask over the scene, so any
   scale or translate slides the ring off the art it is tracing - which is exactly
   the "untidy outline" defect. The wrong-answer beat is a flash on OPACITY, which
   is composited and cannot move the ring. */
.ol-band.is-wrong  {animation:olBandNo var(--olT) linear both;}
.ol-band.is-correct{animation:olBandYes calc(var(--olT) * 1.35) ease-out both;}
@keyframes olBandNo{
  0%,100%{opacity:1;} 20%,60%{opacity:.28;} 40%,80%{opacity:1;}
}
@keyframes olBandYes{
  0%{opacity:.55;} 30%{opacity:1;} 100%{opacity:1;}
}

/* R5 - the outline is INFORMATION. Colour rides a custom property and a
   transition, both of which survive the kill-switch (a killed transition still
   lands on its end value). Only the motion is dropped. */
html.no-anim .ol-alpha,html.no-anim .ol-band{animation:none !important;}
@media (prefers-reduced-motion: reduce){
  .ol-alpha,.ol-band{animation:none !important;}
}
/* ===== FLN ANIMATION KIT: object-outline END ===== */
```

```js
/* ===== FLN ANIMATION KIT: object-outline BEGIN ===== */
(function(){ "use strict";
  var M = window.FLNMotion;
  var ST = ["is-correct", "is-wrong", "is-muted"];

  M.objectOutline = {
    /* state is just a class - both engines read the same ones */
    set: function(el, state){
      M.guard(function(){
        if(!el) return;
        for(var i = 0; i < ST.length; i++) el.classList.remove(ST[i]);
        void el.offsetWidth;                  /* restart - as in recipe 19 */
        if(state) el.classList.add("is-" + state);
      });
    },
    correct: function(el){ this.set(el, "correct"); },
    muted:   function(el){ this.set(el, "muted"); },
    reset:   function(el){ if(el && el._olT) clearTimeout(el._olT); this.set(el, ""); },

    /* wrong RELEASES back to idle white - the child has another attempt, exactly
       as the tile does in recipe 20. Timeout, never animationend: under the
       reduced-motion kill-switch animationend never fires. */
    wrong: function(el, opts){
      var o = opts || {}, self = this;
      M.guard(function(){
        if(!el) return;
        self.set(el, "wrong");
        var v = parseFloat(getComputedStyle(el).getPropertyValue("--olT")) || 0.4;
        if(v > 20) v = v / 1000;
        if(el._olT) clearTimeout(el._olT);
        el._olT = setTimeout(function(){
          el.classList.remove("is-wrong");
          if(o.then) o.then();
        }, v * 1500 + 40);
      });
    },

    /* OPTIONAL, and read the caveat. A rectangular hit box over an irregular sprite
       steals taps meant for whatever is behind it - two overlapping characters and
       the child taps the wrong one. This tests the tap against the sprite's ALPHA.
       It FAILS OPEN: reading pixels back taints the canvas on file://, which is how
       the activities ship, so there it always returns true and you are back to the
       bounding box. Treat it as a dev-server nicety, not a guarantee - the reliable
       fix is z-order and not overlapping the tappable parts in the first place. */
    alphaHit: function(img, clientX, clientY){
      var r = img.getBoundingClientRect();
      if(clientX < r.left || clientX > r.right || clientY < r.top || clientY > r.bottom)
        return false;
      if(img._olA === undefined){
        try{
          var w = Math.min(img.naturalWidth, 256);
          var h = Math.round(img.naturalHeight * w / img.naturalWidth);
          var c = document.createElement("canvas"); c.width = w; c.height = h;
          var x = c.getContext("2d"); x.drawImage(img, 0, 0, w, h);
          img._olA = x.getImageData(0, 0, w, h);
        }catch(e){ img._olA = null; }         /* tainted - fail OPEN */
      }
      if(!img._olA) return true;
      var d = img._olA;
      var px = Math.floor((clientX - r.left) / r.width  * d.width);
      var py = Math.floor((clientY - r.top)  / r.height * d.height);
      return d.data[(py * d.width + px) * 4 + 3] > 24;
    }
  };
})();
/* ===== FLN ANIMATION KIT: object-outline END ===== */
```

### Markup

```html
<!-- ENGINE A. Placement lives on a WRAPPER, never on the outlined element: the
     wiggle and pop are transforms, and they would overwrite a placement transform. -->
<div class="obj-slot" style="left:40%;bottom:9%">
  <img class="ol ol-alpha" src="char_tota.webp" alt="tota">
</div>

<!-- ENGINE B. Full-frame, sits over the scene at inset:0, base64 not a path. -->
<i class="ol ol-band" style="--ol-band:url('data:image/webp;base64,UklGRl...')"></i>
```

### Making a ring band (engine B only)

`tools/make-ring.py` in this folder. It computes the ring from a silhouette by morphology -
dilate minus erode - rather than an edge filter, because an edge filter's line thins
out wherever the art is soft, so the outline breaks along fur, hair and foliage,
exactly where it is needed most.

```bash
# from a cut-out sprite - its alpha IS the silhouette
python tools/make-ring.py --from-sprite tota.webp --w 1280 --h 724 --at 300,200 \
                    --scale .42 --width 6 -o ring_tota_band.webp --css
# from a painted mask, when the object was never a separate file
python tools/make-ring.py --from-mask tota_mask.png -o ring_tota_band.webp --css
```

`--css` prints the paste-ready `data:` URI. A band is ~99% transparent, so a real one
is **0.6-5KB**; if yours is much larger the input was a filled silhouette, not an
outline. `--inset 1` keeps 1px of the ring inside the shape - a ring entirely outside
reads as detached on a busy scene.

### Will it work on my objects?

Tested against 18 unrelated pieces of art from four activities - five people, a
parrot, three buildings, a football, a glass of milk, a microphone, a sun with rays,
a teacup, a road map - all with **the same two classes and no per-object work**.
Every one outlined to its own silhouette.

The one thing that decides it is the alpha channel:

| your object is | what to do |
|---|---|
| a cut-out with real transparency (**153 of 175** files in this fleet) | nothing - add `class="ol ol-alpha"` |
| an opaque card with a flat background (**22 of 175**) | `tools/make-cutout.py` once, then as above |
| welded into a scene raster | engine B and a ring band from `tools/make-ring.py` |
| an inline `<svg>` | works as-is; the filter reads its rendered alpha |

Thin protrusions survive - a walking stick, a microphone stem, a parrot's tail. What
does not is a **concave gap narrower than twice `--ol-w`**: dilation closes it, so at
`--ol-w:4px` a 6px gap between an arm and a body fills in. Drop to 2-3px for spindly
art, or use a generated band.

### Options

| Key | Default | Effect |
|---|---|---|
| `--ol-w` | `4px` | Stroke thickness. Engine A only; engine B bakes it in. |
| `--ol-soft` | `5px` | Separation glow. `0` drops a filter pass on low-end devices. |
| `--ol-idle` | `#FFFFFF` | The "this is tappable" colour. |
| `--ol-amp` | `8px` | Wiggle travel. A 60px object and a 300px character cannot share one figure. |
| `--ol-origin` | `50% 100%` | Pop origin. Objects that rest on the ground should scale from their base. |
| `--olT` | `var(--fx-beat)` | Tempo - the same token as recipes 19 and 20. |
| `--ol-band` | – | Engine B: the ring as a `data:` URI. |

### Gotchas

- **A CSS mask cannot load from a file path on `file://`.** `mask:url(...)` is fetched
  under CORS rules and a `file://` page is origin `null`, so it is **blocked in the
  WebView the activities ship in** - silently, as a missing mask. `<img src>` is not
  affected, which is what makes this so easy to miss. Inline the band as base64;
  that is why the shipped look-and-find carries nine of them.
- **Never transform an `.ol-band`.** It is a full-frame mask over the scene, so any
  scale or translate slides the ring off the art it traces. That is why wrong is a
  flash on `opacity` there and a wiggle only in engine A. This is the single defect
  the two-engine split exists to prevent.
- **Placement goes on a wrapper.** `olNo` and `olYes` are transforms and will overwrite
  a placement transform on the same element.
- **Fully-opaque "sprites" are a trap - but a fixable one.** Some object art is a
  1024x1024 **opaque** card with a flat cream background rather than a cut-out, and
  engine A will faithfully outline the *square*. Surveyed across five activities:
  **153 of 175 object files already have a real alpha channel**, and the 22 that do
  not are all in `HIKGH01_L02_S03`. Run `make-cutout.py --check` over a folder to
  see which are which, then convert those:

  ```bash
  python tools/make-cutout.py --check assets/Images/*.webp    # report only
  python tools/make-cutout.py obj_*.webp --trim               # convert in place
  ```

  It takes the background colour from the corners and floods inward **from the
  border**, so background connected to the edge is removed while a white glass or a
  cream wall *inside* the object keeps its pixels - a plain colour-key would punch
  holes through them. `make-ring.py --from-sprite` still refuses an opaque file
  rather than silently emit a rectangle.
- **Dilation fills concave gaps.** Between an arm and a body, or a parrot's toes, the
  outline closes up. That is inherent to any dilation-based outline; keeping `--ol-w`
  at 3-5px keeps it unobtrusive. It is a real reason to prefer a generated band for
  spindly art.
- **`filter` here is a one-off transition on one element**, not the running-forever
  repaint the kit objects to on the landing sky. Do not "fix" it into an animation.
- **The idle white outline is deliberately static.** With engine A the outline is part
  of the element's own filter, so it cannot be faded independently of the art - a
  breathing idle would pulse the object itself.

---

## 22. Sound

**▶ Preview:** every card plays its own cues, and each card header carries a speaker
button that mutes **only that card** · **Built**

Five cues, shared by every effect in the kit. Four of them are real recordings, so unlike
the rest of the kit they **do** need adding to `ASSET_BYTES` - about 21 KB for the three
in `sfx/`, and the fleet's own cheer is already on disk in every activity.

### These are real recordings, and the synth is switched off

Three rounds of synthesised cues were rejected as machine-made, and that judgement
was right - Web Audio synthesis has a ceiling for warm, kid-friendly sound.

Measuring a reel the team picked out themselves against Kenney's **interface** pack shows
the two are different material on three axes at once:

| | the reel the team picked | Kenney interface pack |
|---|---|---|
| length | 1.0 - 1.15s | 0.45s |
| warmth (spectral centroid) | 1500 - 1770 Hz | 2558 Hz |
| attack | 99 - 178ms | 65ms |

Half the length, an octave brighter, and twice as sharp on the attack. That is the
difference between a played instrument and a beep. When picking a *reward* tone,
**filter on attack time before anything else** - a sound that reaches full level in under
~60ms reads as a machine however nice its pitch is. Of 144 CC0 files searched, the 11 that
cleared that bar all came from an **instrument** pack; not one came from the interface pack.

**The shipped `correct` cue deliberately does not follow that rule.** A `jingles_SAX03`
pick that did match the reel (1.05s, 100ms attack) was tried and then **reverted on
request** - the shorter, brighter interface-pack tone was preferred. The table above is
kept because measuring is still the right way to *shortlist* a candidate; it is not the
thing that decides. If this cue is revisited, that is the comparison to redo.

What ships is four real recordings, three of them supplied by the team:

| cue | file | fires on |
|---|---|---|
| `correct` | `sfx/correct.ogg` | tiles and objects, recipes 19 + 21 |
| `wrong` | `sfx/wrong.ogg` | tiles and objects, recipes 20 + 21 |
| `burst` | `sfx/burst.ogg` | **every** elements-burst moment: landing stars, the end-screen burst, and the correct-answer confetti |
| `celebrate` | the fleet's own `sfx_celebrate.ogg` | registered, not currently fired |

`S.allowSynth` is **false**: a cue with no recording is silent. Silence beats a sound
nobody wants, and it stops a rejected fallback creeping back in.

### Supplied audio is never drop-in

Every one of the three needed work before it could be used, and each fault would have
shipped unnoticed:

- **`burst`** carried **512ms of leading silence**. Played raw, every star pop lands
  half a second after the finger. Trimmed to the onset.
- **`wrong`** ran **3.29s**, but the wrong-answer beat resolves by ~900ms, so it would
  still be sounding during the next question. Its useful energy ends at 0.95s; trimmed
  to 1.05s.
- **`correct`** was going to come from a **16.8s preview reel of eight takes**, and two
  separate things stopped it. Most of the takes FALL, so the obvious first one would have
  put a descending "wrong" shape on a correct answer. And the reel carries a **spoken
  stock watermark** - a watermarked preview is by definition not the licensed asset, so
  it cannot ship however good it sounds. Stripping the watermark is not the way round
  that: it is the marker saying the file has not been paid for.

  What ships instead is Kenney's CC0 `question_003` from the **interface** pack,
  transposed **down to 0.65x** so it sits in a warmer register than its native 4440 Hz
  brightness. A `jingles_SAX03` pick at native pitch was measured against the reel and
  briefly shipped in its place, then reverted - see the note above.

**Check pitch direction before using anything.** It is the one property that decides
whether a sound means yes or no, and nothing in a filename tells you. Measure it as a
**contour across the whole sound**, by spectral peak - a two-point autocorrelation
octave-errors on percussive material, and an octave error flips the apparent direction,
which is precisely the thing being tested. That bit me: the same file measured +11 and
then -8 semitones on two different runs of the naive test.

**Normalise by measuring, not with a dynamics filter.** `dynaudnorm` and single-pass
`loudnorm` both overshot here and produced a **1.18 peak** - clipped. What works is
measuring the peak and applying a plain gain.

### Swapping in your own audio

Every cue still has a synthesised version, used only when no file is registered for
it. Registering one is a single line, which is also how you swap in your own audio:

```js
FLNMotion.sfx.files.correct = "assets/Audio/my_correct.ogg";
```

Samples play through an `<audio>` element, not the Web Audio graph:
`decodeAudioData` needs `fetch()`, and fetch from a `file://` page is CORS-blocked to
origin `null` - the same trap that stops a CSS mask loading from a path. The cost is
that samples bypass the bus, so the limiter and the analyser do not see them; per-card
muting still works because it is enforced a level up, in `cue()`.

### The cues, measured

Rendered offline and measured, not estimated:

| cue | fires on | length | pitch | warmth | attack |
|---|---|---|---|---|---|
| `correct` | recipes 19, 21 | 0.50s | **+10.7 st, rising** | 5601 Hz | 65ms |
| `wrong` | recipes 20, 21 | 1.05s | **-5.1 st, falling** | 1524 Hz | 335ms |
| `burst` | recipe 2 stars, end-screen burst, confetti | 0.42s | flat | 3131 Hz | 14ms |
| `celebrate` | registered, not currently fired | 1.50s | +12.3 st, rising | 3234 Hz | 125ms |

All four are measured the same way: length is the decoded file duration, warmth a
broadband spectral centroid, attack the time to 90% of peak, and pitch a spectral-peak
contour from the first voiced frame to the last. An earlier version of this table mixed
methods - useful-energy length, a narrower centroid band - so its numbers do not compare
with these.

**`correct` and `wrong` are no longer a matched pair.** They still carry opposite pitch
directions, which is the property a child reads first - a rise means yes, a fall means no.
But `correct` is now under half the length of `wrong` and about four times brighter, so
"the only obvious difference is up versus down" no longer holds. That asymmetry is the
accepted cost of the revert noted above; if the two ever read as mismatched in a
classroom, length is the first thing to bring back together.

**`burst` breaks the 60ms attack rule, and should.** It is a pop, not a reward tone -
percussive is the whole point, and the rule above is about the two tonal cues. Do not
"fix" it.

**Level is matched on mean, not peak.** All four peak at about **-1 dBFS** because each
was peak-normalised to 0.89, but peak is not loudness: their mean levels still run from
**-10 dB** (`correct`) to **-24 dB** (`burst`), and that spread is correct - a 0.14s pop
with a long decay has a low mean by construction and would sound violent if pushed to
match a sustained tone. Per-cue trims live in `FLNMotion.sfx.vol`, and `S.master` (0.75)
scales the lot. If a room needs them quieter, move `S.master` rather than the individual
cues, which are balanced against each other.

**Normalise with a measured gain, never a dynamics filter** - see the note above. The
peak-normalise happens before encoding; Vorbis can overshoot a little on the way out, so
check the encoded file, not the WAV.

**`correct` and `wrong` are the same two sounds in every mechanic** - tiles, objects in a
scene, anything added later. A child should not have to learn a second vocabulary because the
mechanic changed.

**The nudge hand has no sound**, and its card carries no speaker either. It is a looping hint
that can run for many seconds while a child hesitates; a tick on every lap would be the most
irritating thing in the activity, and a mute button on something that never makes a noise is
a dead control.

**Everything that replays an effect cues, including the `Compare: old` buttons** - the old
version is still the effect happening, so it should sound. What stays silent is anything that
only clears or reconfigures (`Reset`, `Stroke`, and the sky's baked-raster compare, where
nothing is tappable and a star sound would be claiming otherwise).

```js
/* ===== FLN ANIMATION KIT: sfx BEGIN ===== */
/* Soft, warm, roomy. Rewritten after the first pass was rejected as sounding
   machine-made, which it did. Four things caused that, and none of them were the
   tune:
     1. BONE DRY. Nothing real is heard without a room around it. Everything now
        goes through a short generated reverb, and that single change does more for
        "not a machine" than any amount of partial-tuning.
     2. HARD ATTACKS. A 6ms attack is a click, and a click is a computer. The
        feedback cues now open over 18-30ms - struck felt, not struck glass.
     3. TOO BELL-HEAVY. Bright inharmonic partials read as "digital chime". The
        voice is now mostly fundamental with a quiet, slightly sharp second mode,
        which is what a music box or a soft mallet actually gives you.
     4. ONE OSCILLATOR PER PARTIAL. A single sine is sterile. Each mode is two
        oscillators a few cents apart, so they beat slowly against each other the
        way any real resonator does.
   No square or sawtooth anywhere, nothing sustains, and every hit is randomised a
   little so no two are identical.

   ONE REAL RECORDING EXISTS in the fleet - sfx_celebrate.ogg, the end-screen cheer.
   Any cue with a file registered in S.files uses it and skips synthesis entirely.

   All cues are trimmed to land at the SAME peak level, so nothing jumps out. */
(function(){ "use strict";
  var M = window.FLNMotion = window.FLNMotion || {};
  var ctx = null, bus = null, wet = null, noiseBuf = null;
  var unlocked = false, an = null, fired = 0, sampleAt = 0;

  var S = M.sfx = {
    enabled: true,
    volume: 1.5,
    files: {},         /* cue name -> url. This is the ONLY thing that makes sound. */
    /* The synthesised voices below are kept as reference, but they are OFF. Three
       rounds of them were rejected as machine-like and that judgement was right -
       Web Audio synthesis has a ceiling for warm, human, kid-friendly cues. A cue
       with no recording registered is SILENT, because silence beats a sound nobody
       wants. Turn this on only to hear what the fallback would be. */
    allowSynth: false
  };

  /* A generated room. Exponentially decaying noise is a crude impulse response and
     completely convincing at this length - it only has to suggest that the sound
     happened somewhere. */
  function impulse(c, secs, decay){
    var n = Math.floor(c.sampleRate * secs);
    var b = c.createBuffer(2, n, c.sampleRate);
    for(var ch = 0; ch < 2; ch++){
      var d = b.getChannelData(ch);
      for(var i = 0; i < n; i++)
        d[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / n, decay);
    }
    return b;
  }

  function ac(){
    if(!S.enabled) return null;
    try{
      /* `.length` only exists on an OfflineAudioContext - never resume one. */
      if(ctx){ if(ctx.state === "suspended" && !ctx.length) ctx.resume(); return ctx; }
      var AC = window.AudioContext || window.webkitAudioContext;
      if(!AC) return null;
      ctx = new AC();
      build(ctx);
      if(ctx.state === "suspended") ctx.resume();
      return ctx;
    }catch(_){ return null; }
  }

  function build(c){
    bus = c.createGain(); bus.gain.value = S.volume;

    var lp = c.createBiquadFilter();
    lp.type = "lowpass"; lp.frequency.value = 5200; lp.Q.value = 0.4;

    var rev = c.createConvolver(); rev.buffer = impulse(c, 1.1, 2.6);
    wet = c.createGain(); wet.gain.value = 0.34;      /* send level */
    var revOut = c.createGain(); revOut.gain.value = 1;

    var lim = c.createDynamicsCompressor();
    lim.threshold.value = -8; lim.knee.value = 8; lim.ratio.value = 12;
    lim.attack.value = 0.004; lim.release.value = 0.2;

    an = c.createAnalyser(); an.fftSize = 2048;

    bus.connect(lp);
    lp.connect(lim);                 /* dry */
    wet.connect(rev); rev.connect(revOut); revOut.connect(lim);   /* wet */
    lim.connect(an); an.connect(c.destination);
  }

  function noise(c){
    if(noiseBuf) return noiseBuf;
    var n = Math.floor(c.sampleRate * 0.4);
    noiseBuf = c.createBuffer(1, n, c.sampleRate);
    var d = noiseBuf.getChannelData(0);
    for(var i = 0; i < n; i++) d[i] = Math.random() * 2 - 1;
    return noiseBuf;
  }

  function rnd(a, b){ return a + Math.random() * (b - a); }

  /* Per-cue loudness trim. The cues are written for their own internal balance -
     how loud the second note is against the first - and this makes every cue as a
     WHOLE land at the same peak, so none of them jumps out against the others.
     Calibrated by rendering each one and measuring, not by ear or by guess. */
  var TRIM = { correct:1.006, wrong:1.171, pick:3.570, sprinkle:1.696,
               celebrate:0.910, burst:1.811, tick:9.155 };
  var trim = 1;

  /* One soft note. `atk` is what separates warm from clicky. Modes are quiet and
     only slightly inharmonic - enough to not be a pure tone, not so much that it
     rings like a bell. */
  var MODE = [[1, 1, 1], [2.02, 0.16, 0.62], [3.01, 0.05, 0.34]];

  function note(c, f, at, gain, dur, atk){
    atk = atk || 0.02; gain *= trim;
    f *= rnd(0.9975, 1.0025);
    for(var i = 0; i < MODE.length; i++){
      var m = MODE[i];
      for(var k = 0; k < 2; k++){                  /* two, a few cents apart */
        var o = c.createOscillator();
        o.type = "sine";
        o.frequency.value = f * m[0] * (k ? 1.0018 : 0.9982);
        var g = c.createGain();
        g.gain.setValueAtTime(0.0001, at);
        g.gain.exponentialRampToValueAtTime(gain * m[1] * 0.5, at + atk);
        g.gain.exponentialRampToValueAtTime(0.0001, at + dur * m[2]);
        o.connect(g); g.connect(bus); g.connect(wet);
        o.start(at); o.stop(at + dur * m[2] + 0.02);
      }
    }
  }

  /* Air, not pitch - for things coming apart. */
  function puff(c, at, gain, dur, f0, f1){
    gain *= trim;
    var src = c.createBufferSource(); src.buffer = noise(c);
    var bp = c.createBiquadFilter();
    bp.type = "bandpass"; bp.Q.value = 0.7;
    bp.frequency.setValueAtTime(f0, at);
    bp.frequency.exponentialRampToValueAtTime(f1, at + dur);
    var g = c.createGain();
    g.gain.setValueAtTime(0.0001, at);
    g.gain.exponentialRampToValueAtTime(gain, at + 0.01);
    g.gain.exponentialRampToValueAtTime(0.0001, at + dur);
    src.connect(bp); bp.connect(g); g.connect(bus); g.connect(wet);
    src.start(at); src.stop(at + dur + 0.02);
  }

  /* D major pentatonic - a run of these can never sound wrong together. */
  var PENT = [293.66, 329.63, 369.99, 440.00, 493.88,
              587.33, 659.25, 739.99, 880.00, 987.77];
  function pent(lo, hi){ return PENT[Math.floor(rnd(lo, hi))]; }

  function play(name, fn){
    try{
      /* NOTHING before the first gesture - recordings included. This gate used to
         sit after the S.files check, so a cue with a real file attached skipped it
         entirely: the star-burst tile auto-demos on load, and that fired the
         end-screen cheer the instant the page opened. The synth cues were gated and
         silent, which is exactly why it took a real recording to expose the hole. */
      if(!unlocked) return;
      if(S.files[name] && sample(S.files[name], S.vol[name], S.rate[name])){ fired++; return; }
      if(!S.allowSynth) return;               /* no recording -> no sound */
      var c = ac(); if(!c) return;
      if(!c.length && c.state === "suspended") c.resume();
      fired++;
      trim = TRIM[name] || 1;
      fn(c, c.currentTime + 0.005);
    }catch(_){}
  }

  /* Real recordings, played through <audio>: decodeAudioData needs fetch(), and
     fetch from a file:// page is CORS-blocked to origin "null" - the same trap
     that stops a CSS mask loading from a path. <audio src> is not affected. */
  /* Per-file playback volume. The recordings come from different sources and match
     on PEAK but not on perceived loudness, so these were solved from each file's
     RMS - measured, not guessed. */
  S.vol = {};
  /* Playback rate per cue. `preservesPitch` is switched OFF so this genuinely
     transposes the recording rather than time-stretching it - which is the point:
     it lets one recorded instrument cover two registers, so the correct and wrong
     cues can be the SAME sound rising and falling instead of two unrelated ones. */
  S.rate = {};
  var els = {};
  function sample(url, vol, rate){
    try{
      var a = els[url];
      if(!a){ a = els[url] = new Audio(url); a.preload = "auto"; }
      a.volume = Math.max(0, Math.min(1, vol == null ? 0.85 : vol));
      if(rate && rate !== 1){
        try{ a.preservesPitch = false; a.mozPreservesPitch = false;
             a.webkitPreservesPitch = false; }catch(_){}
        a.playbackRate = rate;
      }
      a.currentTime = 0;
      var pr = a.play(); if(pr && pr.catch) pr.catch(function(){});
      sampleAt = Date.now();
      return true;
    }catch(_){ return false; }
  }
  S.sample = sample;

  /* --- the cues. Gains are trimmed so every one peaks at the same level. ---- */

  /* CORRECT - two soft notes rising a fourth, opening slowly. Warm, not bright:
     this fires many times a session and anything brighter becomes nagging. */
  S.correct = function(){
    play("correct", function(c, t){
      note(c, 440.00, t,         0.115, 1.05, 0.022);
      note(c, 587.33, t + 0.105, 0.105, 1.30, 0.026);
    });
  };

  /* WRONG - two notes stepping gently DOWN, low and soft, opening slower still.
     No knock, no buzz, nothing percussive: it has to read as "not that one", and
     a child hears it far more often than the correct cue. */
  S.wrong = function(){
    play("wrong", function(c, t){
      note(c, 349.23, t,         0.100, 0.80, 0.030);
      note(c, 277.18, t + 0.115, 0.095, 1.05, 0.034);
    });
  };

  /* PICK - one quiet note, an object chosen but not yet judged. */
  S.pick = function(){
    play("pick", function(c, t){ note(c, pent(2, 6), t, 0.085, 0.55, 0.020); });
  };

  /* SPRINKLE - confetti. Distant, sparse, high. The confetti is already carrying
     the celebration; this is only meant to give it some air. */
  S.sprinkle = function(){
    play("sprinkle", function(c, t){
      for(var i = 0; i < 5; i++)
        note(c, pent(6, 10), t + rnd(0, 0.55), rnd(0.030, 0.050), rnd(0.7, 1.1), 0.018);
    });
  };

  /* CELEBRATE - the end screen. Uses the shipped recording when one is registered
     (S.files.celebrate); the synth below is only a stand-in. */
  S.celebrate = function(){
    play("celebrate", function(c, t){
      var n = [440.00, 587.33, 659.25, 880.00], i;
      for(i = 0; i < n.length; i++)
        note(c, n[i], t + i * 0.115, 0.100 - i * 0.008, 1.2 + i * 0.15, 0.022);
      note(c, 293.66, t, 0.070, 1.6, 0.030);
    });
  };

  /* BURST - a drifting star popped. A short downward breath of air for the pop,
     then a few tiny sparks. Was a single sustained bell, which read as a chime
     being played rather than as something coming apart. */
  S.burst = function(){
    play("burst", function(c, t){
      puff(c, t, 0.090, 0.15, 2400, 650);
      for(var i = 0; i < 4; i++)
        note(c, pent(6, 10), t + 0.015 + Math.random() * 0.16,
             rnd(0.030, 0.048), rnd(0.30, 0.50), 0.012);
    });
  };
  S.pling = S.burst;

  /* TICK - a fingertip landing. The quietest thing here on purpose. */
  S.tick = function(){
    play("tick", function(c, t){ note(c, 220, t, 0.045, 0.22, 0.014); });
  };

  S.resume = function(){
    unlocked = true;
    var c = ac();
    if(c && !c.length && c.state === "suspended") c.resume();
  };

  /* What is actually going on, for when nothing can be heard. Reports the level
     leaving the graph, which separates "never ran" from "ran but suspended" from
     "playing fine, the problem is downstream". */
  S.diagnose = function(){
    var peak = 0;
    if(an){
      var d = new Float32Array(an.fftSize);
      an.getFloatTimeDomainData(d);
      for(var i = 0; i < d.length; i++){ var v = Math.abs(d[i]); if(v > peak) peak = v; }
    }
    return {
      trims: TRIM,
      enabled: S.enabled, gestureSeen: unlocked,
      context: ctx ? ctx.state : "not created",
      sampleRate: ctx ? ctx.sampleRate : 0,
      clockRunning: ctx ? ctx.currentTime > 0 : false,
      cuesFired: fired, outputPeak: +peak.toFixed(4), volume: S.volume,
      /* A sample plays through an <audio> element, which is outside the graph the
         analyser sits in - so outputPeak reads 0 for it. Without this flag the
         readout would call a perfectly good recording "silent". */
      samplePlaying: Date.now() - sampleAt < 1500
    };
  };

  /* Render one cue offline, to measure it or export a file someone can listen to. */
  S.render = function(name, seconds, cb){
    try{
      var OAC = window.OfflineAudioContext || window.webkitOfflineAudioContext;
      if(!OAC || typeof S[name] !== "function"){ cb(null); return; }
      var sr = 44100, oc = new OAC(2, Math.ceil(sr * seconds), sr);
      var lc = ctx, lb = bus, lw = wet, ln = noiseBuf, la = an, lu = unlocked, lf = S.files;
      ctx = oc; noiseBuf = null; unlocked = true; S.files = {};
      build(oc);
      S[name]();
      oc.startRendering().then(function(buf){
        ctx = lc; bus = lb; wet = lw; noiseBuf = ln; an = la; unlocked = lu; S.files = lf;
        cb(Array.prototype.slice.call(buf.getChannelData(0)));
      });
    }catch(e){ cb(null); }
  };
})();
/* ===== FLN ANIMATION KIT: sfx END ===== */
```

### Options

| Key | Default | Effect |
|---|---|---|
| `FLNMotion.sfx.enabled` | `true` | Master switch. Setting it false silences everything and creates no context. |
| `FLNMotion.sfx.master` | `0.75` | **The loudness knob.** Scales every sampled cue, on top of the per-cue balance. |
| `FLNMotion.sfx.vol` | per cue | Balance *between* cues (`{correct:0.85, burst:0.8, …}`). Touch this to rebalance, not to change overall level. |
| `FLNMotion.sfx.volume` | `1.5` | Gain on the **synth** bus only. With `allowSynth` false it does nothing — `master` is the one you want. |
| `FLNMotion.sfx.resume()` | – | Call from a real gesture handler. |
| `FLNMotion.sfx.render(cue, secs, cb)` | – | Offline render of one cue, for measuring or exporting. |
| `FLNMotion.sfx.diagnose()` | – | Why you cannot hear anything. See below. |

### When you cannot hear it

`FLNMotion.sfx.diagnose()` reports the whole chain, including the level **actually
leaving the graph** - there is an AnalyserNode in the output path for exactly this.
The preview shows it live in a strip above the cards. It separates three failures
that are indistinguishable from the outside:

| reading | what it means |
|---|---|
| `cuesFired: 0` | the effect never called a cue - wiring, or that card is muted |
| `context: "suspended"`, `clockRunning: false` | the browser has not started audio; no gesture reached it |
| cues firing but `outputPeak: 0` | the graph ran and produced nothing - a gain or a broken connection |
| `outputPeak` around 0.3-0.5 and still silence | **the page is fine.** It is downstream: a muted tab, system volume, or an embedded webview that does not pass audio. Open the file in a normal browser window. |

That last row is the common one, and it is why the readout exists - without a number
there is no way to tell a broken cue from a muted speaker.

### Gotchas

- **Nothing sounds before the first gesture, by design.** A browser will not start an
  AudioContext until the user has interacted. Cues called before that return silently rather
  than queueing - otherwise everything the page auto-demos on load fires in one clump the
  moment the child first touches the screen. That defect was real and is guarded in `play()`.
- **Sound is for what the USER did.** Anything a page auto-demos on load must be silent.
  Do not lean on the gesture gate for this: it works by accident and fails the moment a cue
  has a real recording attached, because `<audio>` needs no AudioContext and so never reaches
  that gate. The preview holds an explicit `booting` flag and `cue()` returns early while it
  is set. The bug this prevents - the end-screen cheer firing the instant the page opened -
  was invisible while every cue was synthesised.
- **A registered file must be checked AFTER the gesture gate, not before.** Putting the
  `S.files` lookup first lets recordings bypass every guard above it.
- **Gate that on the GESTURE, never on `ctx.state`.** A context is born suspended and
  `resume()` is asynchronous, so it is still `"suspended"` inside the very tap that created
  it. An earlier version tested `state !== "running"` and so **swallowed the first cue of
  every session** - the sound only started working from the second tap. Creating the context
  must also call `resume()` immediately; returning a fresh one unresumed is silent.
  This was found only after testing in a browser launched **without**
  `--autoplay-policy=no-user-gesture-required`. That flag starts contexts already running and
  hides this entire class of bug - do not use it when checking whether audio actually works.
- **A mute control that is silent in both directions is untestable.** Unmuting plays a short
  cue back, so "sound is on" is distinguishable from "sound is broken" - and a click from
  someone expecting a preview does not just silently mute the card.
- **Never call `resume()` on an `OfflineAudioContext`** - it starts the render early. The two
  are told apart by `.length`, which only the offline one has.
- **Volume is per-cue, not global.** Raising `volume` to fix one quiet cue makes the
  celebration too loud. Tune the `gain` argument in the cue itself.
- **Keep the low-pass.** The 6kHz roll-off is what stops these sounding brittle on a tablet
  speaker; without it the mallet transients fizz.
- **A cue is fire-and-forget.** There is no voice limit, so if you call one on every frame of
  an animation you will stack hundreds of oscillators. Call them on state changes only.
- **Route cues through one helper, not from inside the effects.** In the preview every cue
  goes through `cue(el, name)`, which walks up to the owning card and drops the sound if that
  card is muted. The effects never reference audio directly, so muting is a property of the
  thing making the noise rather than a global switch - which matters as soon as you want to
  silence one noisy effect while judging another.

---

# Catalogue - all 147 keyframes

Grouped by family. Each block is pasteable whole. "n" = copies across the fleet.

## A. Landing / start gate (`sg*`)

`sgFly` 7 · `sgGlow` 7 · `sgBreathe` 7 · `sgFlash` 7 · `sgSpark` 7 · `sgFloat` 9 (DEAD in MTK) ·
`sgBtnPulse` 9 (DEAD in MTK) · `sgBtnIn` 2 · `sgVoPulse` 8 (DEAD in MTK) · `sgHandReveal` 2 ·
`fingerPop` 10 · `landingTownIn` 1 · `landingObjectGlow` 2 · `landingObjectPop` 2 ·
`bookPurpleGlow` 2 · `bookPurpleSparkle` 2 · `audioPulse` 14 · `tapPulse` 3 · `bootTapPulse` 5

```css
@keyframes sgFly{ 0%{transform:translate(var(--x1),var(--y1));opacity:0;} 10%{opacity:var(--o);} 84%{opacity:var(--o);} 100%{transform:translate(var(--x2),var(--y2));opacity:0;} }
@keyframes sgGlow{ from{filter:drop-shadow(0 0 0 rgba(255,255,255,0));} to{filter:drop-shadow(0 0 7px rgba(255,255,255,.95));} }
@keyframes sgBreathe{0%,100%{opacity:.55;}50%{opacity:1;}}
@keyframes sgFlash{0%{transform:scale(.15);opacity:1;}100%{transform:scale(1.6);opacity:0;}}
@keyframes sgSpark{ 0%{transform:translate(0,0) scale(.35);opacity:0;} 14%{opacity:1;transform:translate(calc(var(--dx) * .3),calc(var(--dy) * .3)) scale(1.12);} 100%{transform:translate(var(--dx),calc(var(--dy) + var(--g))) scale(.3);opacity:0;} }
@keyframes sgFloat{0%,100%{transform:translateY(0);}50%{transform:translateY(-8px);}}
@keyframes sgBtnPulse{0%,100%{transform:translateX(-50%) scale(1);}50%{transform:translateX(-50%) scale(1.03);}}
@keyframes sgBtnIn{ 0%{transform:translateX(-50%) scale(1);} 45%{transform:translateX(-50%) scale(1.10);} 100%{transform:translateX(-50%) scale(1);} }
@keyframes sgVoPulse{0%,100%{transform:scale(1);}50%{transform:scale(1.09);}}
@keyframes sgHandReveal{0%{opacity:0;transform:translateY(16px) scale(.55)}100%{opacity:1;transform:none}}
@keyframes fingerPop{0%{opacity:0;transform:scale(.2);}70%{opacity:1;transform:scale(1.18);}100%{opacity:1;transform:scale(1);}}
@keyframes landingTownIn{from{opacity:0;transform:translateY(20px) scale(.88)}to{opacity:1;transform:none}}
@keyframes landingObjectGlow{ from{transform:scale(1);filter:drop-shadow(0 4px 8px rgba(0,47,118,.14)) drop-shadow(0 0 10px rgba(244,250,255,1)) drop-shadow(0 0 20px rgba(96,165,250,.92));} to{transform:scale(1.08);filter:drop-shadow(0 5px 9px rgba(0,47,118,.16)) drop-shadow(0 0 17px rgba(244,250,255,1)) drop-shadow(0 0 36px rgba(30,58,138,1));} }
@keyframes landingObjectPop{ from{transform:scale(1);} to{transform:scale(1.08);} }
@keyframes bookPurpleGlow{ from{opacity:.86;} to{opacity:1;} }
@keyframes bookPurpleSparkle{ from{opacity:.56;} to{opacity:1;} }
@keyframes audioPulse{0%,100%{transform:scale(1);}50%{transform:scale(1.12);}}
@keyframes tapPulse{0%,100%{transform:scale(1);}50%{transform:scale(1.06);}}
@keyframes bootTapPulse{0%,100%{opacity:.55;}50%{opacity:1;}}
```

## B. Nudge hand

`nhPress` 5 · `nhFx` 5 · `nhTapHand`/`nhTapFx` 3 · `nhTapNew` 3 · `nhTapP` 1 · `nhSimple` 3 ·
`demoTapNew` 3 · `demoTapP` 1 · `nhRippleInner`/`Outer`/`nhSparkPop` 2 · `nhDemoRipple*` 1 ·
`nhBallRipple*` 1 · `nhRippleW1`/`W2` 1 · `nudgeMove` 5 (DEAD)

```css
@keyframes nhPress{ 0%,100%{transform:scale(1);} 40%,58%{transform:scale(.9);} }
@keyframes nhFx{ 0%,34%{opacity:0;transform:scale(.55);} 46%{opacity:1;transform:scale(1);} 58%{opacity:1;transform:scale(1.02);} 78%,100%{opacity:0;transform:scale(1.12);} }
@keyframes nhTapHand{0%,100%{transform:translateY(0) scale(1);}45%{transform:translateY(7px) scale(.95);}62%{transform:translateY(7px) scale(.95);}}
@keyframes nhTapFx{0%,45%{opacity:0;transform:scale(.35);}62%{opacity:1;transform:scale(1);}82%{opacity:1;transform:scale(1.18);}100%{opacity:0;transform:scale(1.18);}}
@keyframes nhTapNew{0%,100%{transform:translateY(0) scale(1);}45%{transform:translateY(6px) scale(.93);}62%{transform:translateY(6px) scale(.93);}}
@keyframes nhTapP{0%,100%{transform:translateY(0) scale(1);}45%{transform:translateY(6px) scale(.93);}62%{transform:translateY(6px) scale(.93);}}
@keyframes nhSimple{0%,100%{transform:scale(1);}50%{transform:scale(.88);}}
@keyframes demoTapNew{0%,100%{transform:scale(1);}48%{transform:scale(.9);}64%{transform:scale(.9);}}
@keyframes demoTapP{0%,100%{transform:scale(1);}48%{transform:scale(.9);}64%{transform:scale(.9);}}
@keyframes nhRippleInner{0%,38%{opacity:0;transform:scale(.30);}47%{opacity:1;transform:scale(.74);} 70%{opacity:.5;transform:scale(1.10);}90%,100%{opacity:0;transform:scale(1.34);}}
@keyframes nhRippleOuter{0%,45%{opacity:0;transform:scale(.55);}56%{opacity:.95;transform:scale(.88);} 78%{opacity:.4;transform:scale(1.20);}96%,100%{opacity:0;transform:scale(1.46);}}
@keyframes nhSparkPop{0%,42%{opacity:0;transform:scale(.55);}52%{opacity:1;transform:scale(1);} 68%{opacity:1;transform:scale(1.06);}86%,100%{opacity:0;transform:scale(1.18);}}
@keyframes nhDemoRippleInner{0%,41%{opacity:0;transform:scale(.30);}50%{opacity:1;transform:scale(.74);} 72%{opacity:.5;transform:scale(1.10);}91%,100%{opacity:0;transform:scale(1.34);}}
@keyframes nhDemoRippleOuter{0%,48%{opacity:0;transform:scale(.55);}58%{opacity:.95;transform:scale(.88);} 79%{opacity:.4;transform:scale(1.20);}96%,100%{opacity:0;transform:scale(1.46);}}
@keyframes nhDemoSparkPop{0%,45%{opacity:0;transform:scale(.55);}54%{opacity:1;transform:scale(1);} 70%{opacity:1;transform:scale(1.06);}87%,100%{opacity:0;transform:scale(1.18);}}
@keyframes nhBallRippleInner{0%,38%{opacity:0;transform:scale(.30);}47%{opacity:1;transform:scale(.74);} 70%{opacity:.5;transform:scale(1.10);}89%,100%{opacity:0;transform:scale(1.34);}}
@keyframes nhBallRippleOuter{0%,45%{opacity:0;transform:scale(.55);}55%{opacity:.95;transform:scale(.88);} 77%{opacity:.4;transform:scale(1.20);}95%,100%{opacity:0;transform:scale(1.46);}}
@keyframes nhBallSparkPop{0%,42%{opacity:0;transform:scale(.55);}51%{opacity:1;transform:scale(1);} 68%{opacity:1;transform:scale(1.06);}86%,100%{opacity:0;transform:scale(1.18);}}
@keyframes nhRippleW1{0%,42%{opacity:0;transform:scale(1);}50%{opacity:1;transform:scale(1.15);} 74%{opacity:.55;transform:scale(1.50);}92%,100%{opacity:0;transform:scale(1.78);}}
@keyframes nhRippleW2{0%,52%{opacity:0;transform:scale(1);}60%{opacity:.8;transform:scale(1.12);} 82%{opacity:.38;transform:scale(1.55);}98%,100%{opacity:0;transform:scale(1.90);}}
@keyframes nudgeMove{0%,100%{transform:translateY(2px);}50%{transform:translateY(-14px);}}
```

## C. Correct / incorrect

`correctPop` 6 · `sparkFly` 6 (DEAD in MTK01) · `buzzShake` 6 · `msShake` 6 · `tisShake` 5 ·
`shake` 2 · `matchShake` 1 · `roadShake` 1

Kit-only, from recipes 19 and 20 - not in any activity yet:
`ckPop` · `ckSpark` · `wgNo` · `wgNoOut` · `wgFade` · `wgPulse` ·
`olNo` · `olYes` · `olBandNo` · `olBandYes`

```css
@keyframes ckPop{0%{transform:scale(1);}11%{transform:scale(.966);}50%{transform:scale(1.055);}72%{transform:scale(.992);}100%{transform:scale(1);}}
@keyframes ckSpark{0%{transform:translate(var(--x0),var(--y0)) scale(.3) rotate(0deg);opacity:0;}25%{opacity:1;}100%{transform:translate(var(--sx),var(--sy)) scale(1) rotate(var(--sr));opacity:0;}}
@keyframes wgNo{0%{transform:translateX(0);}18%{transform:translateX(-9px);}38%{transform:translateX(8px);}60%{transform:translateX(-5.5px);}80%{transform:translateX(3px);}100%{transform:translateX(0);}}
@keyframes wgNoOut{0%{transform:translateX(0) scale(1);}11%{transform:translateX(-9px) scale(1);}24%{transform:translateX(8px) scale(1);}37%{transform:translateX(-5.5px) scale(1);}50%{transform:translateX(3px) scale(1);}62%{transform:translateX(0) scale(1);}100%{transform:translateX(0) scale(.965);}}
@keyframes wgFade{0%,52%{filter:saturate(1);opacity:1;}100%{filter:saturate(.3);opacity:.72;}}
@keyframes wgPulse{0%{transform:scale(1.02);opacity:.65;}100%{transform:scale(1.16);opacity:0;}}
@keyframes olNo{0%{transform:translateX(0);}18%{transform:translateX(calc(var(--ol-amp) * -1));}38%{transform:translateX(calc(var(--ol-amp) * .89));}60%{transform:translateX(calc(var(--ol-amp) * -.61));}80%{transform:translateX(calc(var(--ol-amp) * .33));}100%{transform:translateX(0);}}
@keyframes olYes{0%{transform:scale(1);}11%{transform:scale(.97);}50%{transform:scale(1.06);}72%{transform:scale(.995);}100%{transform:scale(1);}}
@keyframes olBandNo{0%,100%{opacity:1;}20%,60%{opacity:.28;}40%,80%{opacity:1;}}
@keyframes olBandYes{0%{opacity:.55;}30%{opacity:1;}100%{opacity:1;}}
```

```css
@keyframes correctPop{0%{transform:scale(1);}45%{transform:scale(1.08);}100%{transform:scale(1);}}
@keyframes sparkFly{0%{transform:translate(-50%,-50%) scale(.3);opacity:0;}18%{opacity:1;}100%{transform:translate(calc(-50% + var(--dx)),calc(-50% + var(--dy))) scale(1.15) rotate(22deg);opacity:0;}}
@keyframes buzzShake{0%,100%{transform:translateX(0);}20%{transform:translateX(-9px);}40%{transform:translateX(9px);}60%{transform:translateX(-6px);}80%{transform:translateX(6px);}}
@keyframes msShake{0%,100%{transform:translateX(0);}20%,60%{transform:translateX(-7px);}40%,80%{transform:translateX(7px);}}
@keyframes tisShake{0%,100%{transform:translateX(0);}25%{transform:translateX(-6px);}75%{transform:translateX(6px);}}
@keyframes shake{0%,100%{transform:translateX(0)}20%,60%{transform:translateX(-8px)}40%,80%{transform:translateX(8px)}}
@keyframes matchShake{0%,100%{transform:translateX(0)}25%{transform:translateX(-7px)}75%{transform:translateX(7px)}}
@keyframes roadShake{0%,100%{transform:translateX(0)}20%{transform:translateX(-11px)}40%{transform:translateX(10px)}60%{transform:translateX(-7px)}80%{transform:translateX(5px)}}
```

## D. Reveal / glow ladder

`revealPulse` 5 · `revealGlow` 2 · `revealHold` 1 · `answerGlow` 1 · `optPulseRing` 2 · `binGlow` 1 ·
`cardGlowPulse` 3 · `s03RevealPulse` 3 · `matchZoneGlow` 1 · `headGlowPulse` 3 · `mrChipGlow` 3 ·
`tisPulse` 5 · `meetGlow`/`meetBounce` 5 · `csTotalGlow`/`csBlankPop` 2 · `pulseSlot` 5 ·
`cmpTapPulse` 5

```css
@keyframes revealPulse{0%,100%{box-shadow:0 5px 12px rgba(0,177,50,.15);}50%{box-shadow:0 0 0 6px rgba(0,177,50,.28),0 10px 24px rgba(0,177,50,.30);}}
@keyframes revealGlow{0%,100%{box-shadow:0 0 0 5px rgba(0,177,50,.30)}50%{box-shadow:0 0 0 11px rgba(0,177,50,.16)}}
@keyframes revealHold{0%,100%{box-shadow:0 0 0 4px rgba(0,177,50,.20),0 5px 12px rgba(11,61,140,.10);}50%{box-shadow:0 0 0 12px rgba(0,177,50,.34),0 8px 20px rgba(0,177,50,.28);}}
@keyframes answerGlow{0%,100%{box-shadow:0 0 0 4px rgba(0,177,50,.18),0 5px 12px rgba(11,61,140,.10);transform:scale(1);}50%{box-shadow:0 0 0 12px rgba(0,177,50,.32),0 8px 20px rgba(0,177,50,.28);transform:scale(1.04);}}
@keyframes optPulseRing{ 0%,100%{ box-shadow:0 0 0 0 rgba(0,177,50,.50); opacity:1; } 50% { box-shadow:0 0 0 13px rgba(0,177,50,0); opacity:.45; } }
@keyframes binGlow{0%,100%{box-shadow:0 0 0 4px rgba(0,177,50,.18);}50%{box-shadow:0 0 0 11px rgba(0,177,50,.34);}}
@keyframes cardGlowPulse{0%,100%{box-shadow:0 0 0 3px rgba(33,167,74,.35),0 0 14px rgba(33,167,74,.45);}50%{box-shadow:0 0 0 5px rgba(33,167,74,.55),0 0 22px rgba(33,167,74,.7);}}
@keyframes s03RevealPulse{0%,100%{box-shadow:0 0 0 0 rgba(0,177,50,0);}50%{box-shadow:0 0 0 14px rgba(0,177,50,.35);}}
@keyframes matchZoneGlow{0%{box-shadow:0 0 0 0 rgba(0,177,50,.45);}100%{box-shadow:0 0 0 18px rgba(0,177,50,0);}}
@keyframes headGlowPulse{0%,100%{transform:translate(-50%,-52%) scale(1);}50%{transform:translate(-50%,-52%) scale(1.12);}}
@keyframes mrChipGlow{0%,100%{box-shadow:0 4px 0 rgba(11,61,140,.10);transform:scale(1);} 50%{box-shadow:0 0 0 8px rgba(96,165,250,.78),0 0 20px rgba(30,58,138,.72),0 4px 0 rgba(11,61,140,.10);transform:scale(1.05);}}
@keyframes tisPulse{0%,100%{box-shadow:0 0 0 4px rgba(0,177,50,.32);}50%{box-shadow:0 0 0 9px rgba(0,177,50,.6),0 0 28px rgba(0,177,50,.55);}}
@keyframes meetGlow{0%,100%{box-shadow:0 6px 16px rgba(11,61,140,.08);}50%{box-shadow:0 0 0 6px rgba(56,106,246,.22),0 10px 24px rgba(56,106,246,.30);}}
@keyframes meetBounce{0%,100%{transform:translateY(0) scale(1);}30%{transform:translateY(-15px) scale(1.09);}55%{transform:translateY(0) scale(1);}}
@keyframes csTotalGlow{ 0%,100%{ box-shadow:0 0 0 8px rgba(0,177,50,.16), 0 8px 18px rgba(11,61,140,.12); } 50% { box-shadow:0 0 0 15px rgba(0,177,50,.30), 0 8px 22px rgba(11,61,140,.16); } }
@keyframes csBlankPop{0%{transform:scale(.6);opacity:0}60%{transform:scale(1.12)}100%{transform:scale(1);opacity:1}}
@keyframes pulseSlot{0%,100%{transform:scale(1);}50%{transform:scale(1.07);}}
@keyframes cmpTapPulse{0%,100%{transform:scale(1);}50%{transform:scale(1.07);}}
```

## E. Celebration

`confettiFall` 7 · `fxConfettiFall` 3 · `endConfettiFall` 1 · `confShot` 5 · `endPop` 7 · `swPop` 3 ·
`mascotReact` 4 · `matchSparkFly` 1 · `roadStar` 1 · `pbPop` 3

```css
@keyframes confettiFall{0%{transform:translateY(-760px) rotate(0);opacity:1;}100%{transform:translateY(760px) rotate(720deg);opacity:0;}}
@keyframes fxConfettiFall{0%{transform:translateY(-40px) rotate(0);opacity:1;}100%{transform:translateY(780px) rotate(720deg);opacity:0;}}
@keyframes endConfettiFall{0%{transform:translateY(-24px) rotate(0);}100%{transform:translateY(820px) rotate(720deg);}}
@keyframes confShot{0%{transform:translate(0,0) rotate(0);opacity:1;}80%{opacity:1;}100%{transform:translate(var(--tx),var(--ty)) rotate(560deg);opacity:0;}}
@keyframes endPop{from{transform:scale(.4);opacity:0;}to{transform:scale(1);opacity:1;}}
@keyframes swPop{0%{transform:scale(1);}40%{transform:scale(1.13) rotate(-3deg);}100%{transform:scale(1);}}
@keyframes mascotReact{0%{transform:scale(var(--mbase,1)) rotate(0);}35%{transform:scale(calc(var(--mbase,1)*1.16)) rotate(-5deg);}68%{transform:scale(calc(var(--mbase,1)*1.04)) rotate(3deg);}100%{transform:scale(var(--mbase,1)) rotate(0);}}
@keyframes matchSparkFly{ 0% {opacity:0;transform:translate(0,0) scale(.2) rotate(0deg);} 35% {opacity:1;transform:translate(calc(var(--sx) * .55),calc(var(--sy) * .55)) scale(1.15) rotate(45deg);} 100%{opacity:0;transform:translate(var(--sx),var(--sy)) scale(.45) rotate(110deg);} }
@keyframes roadStar{0%{opacity:0;transform:translate(-50%,-50%) scale(.2)}22%{opacity:1}100%{opacity:0;transform:translate(calc(-50% + var(--sx)),calc(-50% + var(--sy))) scale(1.25) rotate(var(--sr))}}
@keyframes pbPop{from{transform:scale(.3);opacity:0;}to{transform:scale(1);opacity:1;}}
```

## F. Transitions

`fadeIn` 7 · `popUp` 7 · `hintPop` 7 · `slideIn` 6 · `pgPeek` 3 · `gateRise` 1 · `compArrive` 1 ·
`matchArtReveal` 1 · `actGo`/`popGo` 4 · `roadLand` 1 · `place*` 1 · `storyKenBurns` 5 ·
`calloutPop` 5 · `laughTears` 1

```css
@keyframes fadeIn{from{opacity:0;}to{opacity:1;}}
@keyframes popUp{from{transform:translateY(-160%);opacity:0;}to{transform:translateY(0);opacity:1;}}
@keyframes hintPop{from{transform:scale(.4);opacity:0;}to{transform:scale(1);opacity:1;}}
@keyframes slideIn{from{opacity:0;transform:translateY(16px) scale(.985);}to{opacity:1;transform:none;}}
@keyframes pgPeek{from{transform:translateY(100%);}to{transform:translateY(0);}}
@keyframes gateRise{from{transform:translateY(70%);}to{transform:translateY(0);}}
@keyframes compArrive{ 0% {opacity:0;transform:translate(-50%,-50%) var(--pos) translateY(-38px) scale(.86);} 30% {opacity:1;} 70% {transform:translate(-50%,-50%) var(--pos) translateY(4px) scale(1.03);} 84% {transform:translate(-50%,-50%) var(--pos) translateY(-2px);} 100%{opacity:1;transform:translate(-50%,-50%) var(--pos);} }
@keyframes matchArtReveal{0%{transform:scale(.78);}58%{transform:scale(1.09);}100%{transform:scale(1);}}
@keyframes actGo{0%{transform:scale(1);opacity:1;}55%{transform:translateY(-120px) scale(.5);opacity:.8;}100%{transform:translateY(-220px) scale(.1);opacity:0;}}
@keyframes popGo{0%{transform:scale(1);opacity:1;}45%{transform:scale(1.3);opacity:1;}100%{transform:scale(.2);opacity:0;}}
@keyframes roadLand{0%{transform:scale(.45) rotate(-8deg)}70%{transform:scale(1.12) rotate(3deg)}100%{transform:none}}
@keyframes placeArtArrive{from{opacity:0;transform:translateY(28px) scale(.72) rotate(-4deg)}to{opacity:1;transform:none}}
@keyframes placeArtFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@keyframes placeArrow{from{opacity:0;transform:translateX(-22px) scale(.7)}to{opacity:1;transform:none}}
@keyframes placeNameReveal{from{opacity:0;transform:translateX(34px) scale(.78)}to{opacity:1;transform:none}}
@keyframes storyKenBurns{0%{transform:scale(1.02) translate(0,0);}50%{transform:scale(1.08) translate(-1.5%,-1%);}100%{transform:scale(1.05) translate(1.5%,1%);}}
@keyframes calloutPop{from{opacity:0;transform:translateX(-50%) scale(.4);}to{opacity:1;transform:translateX(-50%) scale(1);}}
@keyframes laughTears{ from{opacity:0;transform:translateY(-3px) scale(.72);} to{opacity:1;transform:translateY(0) scale(1);} }
```

## G. Ambient

`decoPlantSway` 1 · `decoCurtainBlow` 1 · `bgTreeSway` 1 · `scCanopySway` 1 · `scWindFly` 1 ·
`scGust` 1 · `btSway` 5

```css
@keyframes decoPlantSway{ 0%,100%{transform:rotate(-1deg) skewX(0.3deg);} 35% {transform:rotate(1.5deg) skewX(-0.7deg);} 70% {transform:rotate(0.2deg) skewX(-0.1deg);} }
@keyframes decoCurtainBlow{ 0%,100%{transform:skewX(0.9deg) scaleY(1);} 42% {transform:skewX(-2.4deg) scaleY(0.994);} 72% {transform:skewX(-0.5deg) scaleY(1);} }
@keyframes bgTreeSway{ 0%,100%{transform:rotate(-0.7deg) skewX(0.4deg);} 38% {transform:rotate(1.1deg) skewX(-0.7deg);} 70% {transform:rotate(0.15deg) skewX(-0.1deg);} }
@keyframes scCanopySway{ 0%,100%{ transform:rotate(-0.7deg) skewX(0.4deg); } 38% { transform:rotate(1.05deg) skewX(-0.7deg); } 70% { transform:rotate(0.15deg) skewX(-0.1deg); } }
@keyframes scWindFly{ 0% { transform:translate(0,0) rotate(0deg); opacity:0; } 7% { opacity:var(--o); } 25% { transform:translate(345px,var(--w)) rotate(96deg); opacity:var(--o); } 50% { transform:translate(690px,calc(var(--w) * -1)) rotate(190deg); opacity:var(--o); } 75% { transform:translate(1035px,var(--w)) rotate(286deg); opacity:var(--o); } 93% { opacity:var(--o); } 100%{ transform:translate(1425px,0) rotate(380deg); opacity:0; } }
@keyframes scGust{ 0% { transform:translateX(0) scaleX(.55) rotate(-3deg); opacity:0; } 18% { opacity:.42; } 60% { opacity:.26; } 100%{ transform:translateX(1720px) scaleX(1.2) rotate(2deg); opacity:0; } }
@keyframes btSway{0%,100%{transform:translateX(-172px) rotate(-1.4deg);}50%{transform:translateX(-172px) rotate(1.4deg);}}
```

## H. Block Town

`blkDrop` 5 · `blkWobble` 5 · `btDust` 5 · `btHop` 5 · `btPeer` 5 · `rocketGo` 5

```css
@keyframes blkDrop{0%{transform:translateY(-72px) scaleY(.82);opacity:.35;}70%{transform:translateY(0) scaleY(1.12);}100%{transform:translateY(0) scaleY(1);opacity:1;}}
@keyframes blkWobble{0%,100%{transform:rotate(0);}25%{transform:rotate(5deg);}75%{transform:rotate(-5deg);}}
@keyframes btDust{0%{opacity:.85;transform:translate(-50%,0) scale(.6);}100%{opacity:0;transform:translate(-50%,-20px) scale(1.35);}}
@keyframes btHop{0%,100%{transform:translateY(0);}40%{transform:translateY(-34px);}}
@keyframes btPeer{0%,100%{transform:translateY(0) rotate(0);}50%{transform:translateY(-10px) rotate(-4deg);}}
@keyframes rocketGo{0%{transform:translate(-50%,0);}100%{transform:translate(-50%,-420px) scale(.65);opacity:0;}}
```

## I. Gleam

```css
@keyframes msShine{0%{top:-130%;left:-130%;}100%{top:110%;left:110%;}}
@keyframes trayShine{ 0%,15%{background-position:120% 120%;} 55%,100%{background-position:-40% -40%;} }
@keyframes narratedShine{ 0%{background-position:83% 0;} 55%,100%{background-position:17% 0;} }
@keyframes narratedPolish{ 0%,100%{ filter:saturate(1.16) brightness(1.04) contrast(1.03); } 48%{ filter:saturate(1.12) brightness(1.13) contrast(1.05) drop-shadow(0 0 4px rgba(225,234,244,.72)); } }
@keyframes narratedLift{from{filter:none;}to{filter:brightness(1.07) saturate(1.10);}}
@keyframes placeNameShine{0%,55%{left:-42%}85%,100%{left:120%}}
```

## J. Chrome / HUD

`wv1`/`wv2` 7 · `speakerWaveSmall`/`Large` 3 · `bulbRays` 7 · `roSpin` 3 · `sortDragWobble` 3 ·
`actCountBump` 2 · `silBounce` 1 · `wordPop`/`wordHover` 1 · `mwPulse` 2

```css
@keyframes wv1{0%{opacity:0;}33%{opacity:1;}100%{opacity:1;}}
@keyframes wv2{0%{opacity:0;}66%{opacity:1;}100%{opacity:1;}}
@keyframes speakerWaveSmall{0%,17%{visibility:hidden;}18%,72%{visibility:visible;}73%,100%{visibility:hidden;}}
@keyframes speakerWaveLarge{0%,42%{visibility:hidden;}43%,72%{visibility:visible;}73%,100%{visibility:hidden;}}
@keyframes bulbRays{0%,100%{opacity:.5;}50%{opacity:1;}}
@keyframes roSpin{0%,100%{transform:rotate(0deg);}50%{transform:rotate(-90deg);}}
@keyframes sortDragWobble{0%,100%{filter:brightness(1.03);}50%{filter:brightness(1.12);}}
@keyframes actCountBump{0%,100%{transform:scale(1)}45%{transform:scale(1.22)}}
@keyframes silBounce{0%,100%{transform:scale(1);}50%{transform:scale(1.08);}}
@keyframes wordPop{0%{transform:scale(1);}50%{transform:scale(1.18);}100%{transform:scale(1);}}
@keyframes wordHover{0%{transform:translateY(0);}45%{transform:translateY(-12px);}100%{transform:translateY(0);}}
@keyframes mwPulse{0%,100%{opacity:1}50%{opacity:.12}}
```

## K. Birthday board (MTKGA02 only)

```css
@keyframes birthdayOptionContentIn{ 0%{opacity:0;transform:perspective(600px) rotateY(0deg) scale(.35);} 55%{opacity:1;} 100%{opacity:1;transform:perspective(600px) rotateY(720deg) scale(1);} }
@keyframes birthdayPlacedDissolve{ 0%,18%{opacity:1;transform:scale(1);filter:blur(0) saturate(1);} 100%{opacity:0;transform:scale(.9);filter:blur(7px) saturate(1.08);} }
@keyframes birthdayCorrectGlowIn{ 0%{ filter:none; } 25%{ filter: drop-shadow(0 0 2px oklch(0.9 0.08 151 / .95)) drop-shadow(0 0 14px oklch(0.7 0.16 151 / .65)); } 65%{ filter: drop-shadow(0 0 2px oklch(0.9 0.08 151 / .9)) drop-shadow(0 0 12px oklch(0.7 0.16 151 / .55)); } 100%{ filter:none; } }
@keyframes birthdayVacantPulse{ 0%,100%{opacity:1;} 50%{opacity:.5;} }
@keyframes birthdayBalloonBreeze{ 0%,25%,72%,100%{ transform:perspective(760px) translate3d(0,0,0) rotateZ(0) rotateY(0) rotateX(0); } 36%{ transform:perspective(760px) translate3d(-1px,-1px,2px) rotateZ(-.7deg) rotateY(2deg) rotateX(.4deg); } 47%{ transform:perspective(760px) translate3d(3px,-3px,6px) rotateZ(1.25deg) rotateY(-4deg) rotateX(-.8deg); } 59%{ transform:perspective(760px) translate3d(-1px,-1px,2px) rotateZ(-.5deg) rotateY(1.8deg) rotateX(.35deg); } }
@keyframes birthdayFlameLive{ 0%{transform:rotate(-1.5deg) scale(.96,1.025);filter:drop-shadow(0 0 1px rgba(255,179,26,.48)) brightness(.98);} 52%{transform:rotate(1.7deg) scale(1.015,.965);filter:drop-shadow(0 0 2px rgba(255,190,35,.72)) brightness(1.06);} 100%{transform:rotate(-.6deg) scale(.985,1.015);filter:drop-shadow(0 0 1.4px rgba(255,169,20,.58)) brightness(1.01);} }
@keyframes birthdaySprinkleDrift{ 0%,100%{transform:translate3d(0,0,0) rotate(var(--rot));} 50%{transform:translate3d(var(--dx),-3px,0) rotate(calc(var(--rot) + 3deg));} }
```

`birthdayOptionContentIn` spins 720° - two full turns, so it can never stop edge-on like a coin flip.

## L. Look-and-find (`tis*`, `_dist` only)

```css
@keyframes tisBreathe{ 0%,100%{transform:scale(1);opacity:.94;} 50%{transform:scale(1.022);opacity:1;} }
@keyframes tisRipple{ 0%{transform:scale(1);opacity:0;} 18%{opacity:.75;} 100%{transform:scale(1.10);opacity:0;} }
@keyframes tisPop{0%{transform:scale(.94);}60%{transform:scale(1.04);}100%{transform:scale(1);}}
@keyframes tisBloom{0%{transform:scale(1);opacity:.9;}100%{transform:scale(1.4);opacity:0;}}
@keyframes tisContourBreathe{0%,100%{opacity:.86;}50%{opacity:1;}}
@keyframes tisContourGuide{0%,100%{opacity:.62;}50%{opacity:1;}}
@keyframes tisNaturalCorrect{0%{transform:scale(.9);opacity:0;}100%{transform:scale(1);opacity:1;}}
@keyframes tisNaturalBadge{0%{transform:scale(.55);opacity:0;}100%{transform:scale(1);opacity:1;}}
```

## M. Mechanic-specific

```css
@keyframes popBurstOut{ 0%{transform:scale(1);opacity:1;} 45%{transform:scale(1.22);opacity:.85;} 100%{transform:scale(.3);opacity:0;} }
@keyframes popFlash{ 0%{opacity:0;transform:scale(.4);} 30%{opacity:1;transform:scale(1);} 100%{opacity:0;transform:scale(1.5);} }
@keyframes popNumUp{ 0%{ opacity:0; transform:translate(-50%,10px) scale(.5); } 35%{ opacity:1; transform:translate(-50%,-16px) scale(1.12); } 75%{ opacity:1; transform:translate(-50%,-30px) scale(1); } 100%{ opacity:1; transform:translate(-50%,-34px) scale(1); } }
@keyframes demoPop{0%{transform:scale(.5);}70%{transform:scale(1.25);}100%{transform:scale(1);}}
@keyframes demoHit{0%{transform:scale(1);}40%{transform:scale(1.14);}100%{transform:scale(1);}}
```

---

# House style for new animations

- **Wind = asymmetric 3-stop keyframes** with `rotate` + `skewX`. Symmetric = metronome.
- **Springy pops are `cubic-bezier(.34,1.5,.6,1)`.**
- **Time effects to read as *caused*** - the 6-star burst peaks exactly as the object lands.
- **Sync by duration, not `animation-delay`.** Animations start at page load, not on `.show`.
- **Stagger via a custom property, not `nth-child` delay** - the `animation` shorthand resets delay.
- **`fill-mode: both` on staggered pieces**, or they sit visible on the top edge during their delay.
- **Animate `filter` only when a transform would fight something else**; otherwise prefer
  `transform`/`opacity` (composited).
- **Build overlays as throwaway DOM** - create, append N `<i>`, self-remove on a timeout longer than
  the animation.
- **One keyframe, N instances** - read per-element custom properties. Never generate N keyframe rules.
- **Claim a 2-3 letter prefix.** Don't add another `popUp`.
- **A timing function runs between EVERY pair of keyframes.** An overshooting spring on a
  multi-stop animation overshoots at every stop. Shape a spring with percentages and join
  them with `ease-in-out`; save `cubic-bezier(.34,1.5,.6,1)` for two-stop pops.
- **`both` on a DELAYED layer paints its 0% state throughout the delay.** Wanted for staggered
  confetti, wrong for anything that should be invisible until it starts - use base
  `opacity:0` + `forwards` there.
- **State that a child can trigger twice must own its timers.** Park them on the element and
  cancel them on replay, or the previous play's cleanup fires into the new one.
- **Decoration must never cross the content.** Launch particles from the element's edge, not
  its centre - the word or digit on the tile is the thing being read.
- **Chained `drop-shadow`s compound.** Each pass shadows the previous passes' output too, so
  "more directions" thickens the stroke instead of rounding it. Four axis passes = a clean
  dilation of exactly the radius asked for.
- **A CSS `mask`/`background` url is CORS-checked; `<img src>` is not.** On `file://` - which
  is how these ship - a path in a mask is blocked silently. Inline it as base64.
- **Outlines are computed from the art, never traced.** A traced path drifts out of register
  the first time the art is re-exported.

---

# Deviations from shipped code

| # | Defect | Fix |
|---|---|---|
| 1 | `sgGlow` animates `filter` on ~87 elements - uncomposited, repaints every frame | Static shadow on `::after`, animate opacity |
| 2 | `--g` = glow duration on sky, gravity on burst | Burst renamed `--gy` |
| 3 | Reduced-motion kill-switch in only 1 of 7 activities | Shipped with every effect |
| 4 | 3 activities never preload `bgdeco_*.svg`; 1 preloads the wrong background | Each recipe lists its manifest entries |
| 5 | `classList.forEach` - only ES6 call in ES5 code | Index loop |

**Deliberate - do not "fix":**
- Hard-edged mask hole on landing (the card is visible; it's a real occlusion boundary).
- Soft radial hole on the end screen (a hard edge there reads as a sliced crescent).
- Audio chip not throbbing in `_dist`: *"the button must not move while a clip plays."*

---

# Verification

1. Serve via Live Server (port 5503 is already configured): `http://localhost:5503/<folder>/`.
2. Paste-test into a **copy**, not an activity in place.
3. **Sky effects: full-screen only.** `vmax` stays viewport-relative - a small pane proves nothing.
4. Don't trust headless Chrome. `--virtual-time-budget` doesn't reliably advance compositor
   animations; sample by overriding `animation-delay`.
5. Test hit boxes on touch, not mouse. Confirm a star over a button doesn't also fire the button.
6. Load `?still=1` - everything freezes, nothing throws, loader still dismisses.
7. Rotate to portrait - fixed overlays stay attached.
8. For the mascot, trace `.anim` from JS to CSS. That's the failure it has actually shipped with.

---

*Line numbers drift. The comments around them in the source are the durable landmark - and they are
the only design record this codebase has.*

---

# Installing an effect

Copy the block below into Claude Code (or any coding agent) with the animation kit folder in the
workspace. Fill in the two blanks at the top. It installs one animation at a time, safely.

**Install one effect per run.** Batching is how you get conflicts you cannot attribute.

---

## The prompt

```text
You are installing an animation from the FLN Animation Kit into a learning activity.

TARGET ACTIVITY: <folder name, e.g. MTKGA02_L01_S01>
EFFECT TO INSTALL: <recipe number and name, e.g. "1. Start screen stars (drift)">

Read fln-animation-kit/ANIMATIONS.md first. Follow its rules R1-R11 exactly.
Work through the phases below in order. Do not skip a phase. Do not batch multiple effects.

────────────────────────────────────────
PHASE 1 - AUDIT (read-only, change nothing)

1. Identify the target's generation:
   - Does it have index.html + style.css + app.js  -> split-file. CSS goes at the end of
     style.css, JS at the end of app.js, markup in index.html.
   - Is it a single <NAME>.html  -> _dist build. CSS goes inside the one <style> block, JS inside
     the one <script> block. Say so in your report: _dist files are build outputs and editing
     them is a patch, not a fix.

2. Is the effect ALREADY there? Grep the target for every @keyframes name the recipe uses.
   - Found and working  -> STOP. Report "already installed" and do nothing else.
   - Found but different -> STOP. Show me the diff and ask before replacing.
   - Not found           -> continue.

3. Is it already there but DEAD? Grep for rules that would kill it:
   - `animation:\s*none` / `animation:none !important` on any selector the recipe uses
   - `display:\s*none` on the recipe's elements
   - a blanket rule listing several selectors at once (this pattern exists at
     MTKGA01_L01_S01/style.css:2378-2382 and silently kills sgFloat / sgBtnPulse / sgVoPulse)
   If found, report it and ask whether to remove the killer or skip the effect.

4. R11 CHECK - the one that causes most bugs.
   For EVERY selector the recipe touches, grep ALL rules for it, not just the first.
   This codebase appends later overrides instead of editing in place: #nudgeHand is declared 3x,
   .phase-gate 7x, .boot-loader 3x in one file, audioPulse 14x across the fleet.
   If a LATER rule changes a size, position or display that the recipe's pixel offsets assume,
   report it. Do not paste offsets computed against a different box size.

5. ASSETS - verify each asset the recipe lists exists in THIS folder's assets/UI/.
   Never assume it exists because a sibling activity has the same filename.
   List any that are missing. Small SVGs have full source in ANIMATIONS.md; rasters must be
   copied from another activity.

6. Report findings and WAIT for my go-ahead before editing.

────────────────────────────────────────
PHASE 2 - INSTALL

7. If the core block is not present, paste "FLN ANIMATION KIT: core" and the reduced-motion CSS
   from ANIMATIONS.md first. It is required by every recipe. Never paste it twice.

8. Paste the recipe's blocks verbatim, keeping the BEGIN/END marker comments. They are how the
   next person finds and removes this cleanly.

9. Add any required markup at the insertion point the recipe names.

10. Copy missing assets, then add each one to the preload manifest (ASSET_BYTES, or
    asset-manifest.js on the newest generation). Use the real byte size.

11. HARD CONSTRAINTS - violating any of these is a failed install:
    - Do NOT edit ENGINE_VERSION. verify_bundle.py hard-fails on divergence.
    - Do NOT convert anything to an ES module or add type="module".
    - Do NOT rename the recipe's keyframes unless the target is a brand-new game with a name
      collision (popUp, fadeIn, slideIn, shake, confettiFall are taken everywhere).
    - Do NOT remove or reorder existing rules to make yours win. Append.
    - Do NOT reformat, re-indent or "clean up" surrounding code. Touch only what you add.
    - Do NOT add a build step, bundler, package.json, or dependency.
    - Every JS entry point must be wrapped in try/catch (use FLNMotion.guard) so it can never
      strand #bootLoader.
    - Any touch listener must be registered {passive:false}.

────────────────────────────────────────
PHASE 3 - VERIFY

12. Syntax check what you changed. For a _dist single-file target, extract the inline <script>
    blocks and parse them separately (node --check will not lint the .html).

13. Serve the activity and open it. Live Server port 5503 is already configured.
    Confirm, and tell me the result of each:
    a. The effect renders and animates.
    b. Browser console is clean - no errors, no 404s for the new assets.
    c. `?still=1` freezes it, nothing throws, and the boot loader still dismisses.
    d. Portrait / rotated: the effect stays attached to the stage and does not detach.
    e. Nothing that worked before is broken - buttons still respond, slides still advance.
    f. For anything tappable: test with touch emulation, not just a mouse. Confirm a tap on the
       new element does not ALSO fire the control underneath it.

14. Effect-specific checks, if applicable:
    - Start screen stars: verify FULL-SCREEN only. It is vmax-based; a small window proves nothing.
      Confirm .start-bg uses startnew_bg_plain.webp, and that there is exactly ONE set of
      decorations (two sets = you skipped the background swap).
    - Mascot: trace the .anim class from the JS call site through to the CSS selector. The CSS
      being present is not enough - this has shipped with the class never toggled.
    - Answer feedback (19/20): install BOTH or neither - half the pair leaves correct and wrong
      looking like they came from different games. Then, on the real tile class (.opt-cell,
      .m-card, .tile, .sort-item - find the actual one):
        a. remove any background FILL and any tick/cross on the correct and wrong states,
           including pseudo-elements and badge nodes;
        b. grep every rule for that selector - an existing `border-color ... !important` on
           .correct/.wrong BEATS a keyframe, so the old rule has to go or the new mark loses;
        c. tap the same wrong tile twice and confirm the second shake runs its full length -
           if it dies half way, the pending release from the first tap was not cancelled;
        d. confirm the tile's own word/digit stays readable in every state, eliminated included;
        e. load ?still=1: the green/red border must still be there, the halo and sparks must not.
    - Anything with pixel offsets: confirm against the ACTUAL rendered box size, per step 4.

────────────────────────────────────────
PHASE 4 - REPORT

15. Tell me:
    - Files changed and where each block was inserted.
    - Assets copied and manifest entries added.
    - Anything from Phase 1 you found but did not fix.
    - Each Phase 3 check and whether it passed. If you could not verify something, say so
      plainly - do not report it as passing.

If any phase fails, stop and report. Do not work around a failure by changing the recipe.
```

---

## Removing an effect

Every block is fenced with `BEGIN` / `END` markers, so removal is:

```bash
# find what a kit install added
grep -rn "FLN ANIMATION KIT" <activity-folder>/
```

Delete between the markers, drop the assets from the manifest, and remove any markup the recipe
added. Leave the `core` block if another effect still uses it.

---

## If you are installing by hand instead

The short version of the same checks:

1. Which generation - split files or `_dist`?
2. Grep the keyframe names. Already there? Stop.
3. Grep for `animation:none` killers on those selectors.
4. Grep **every** rule for each selector, not the first - later overrides win here.
5. Confirm assets exist in *this* folder.
6. Paste with the BEGIN/END markers intact.
7. Add assets to the manifest.
8. Test: renders, console clean, `?still=1`, portrait, touch, nothing else broken.
