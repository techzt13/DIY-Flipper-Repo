# case_step.py - DIY Flipper case -> STEP export
# Run in Google Colab (free):  https://colab.research.google.com
#   Cell 1:  !pip install cadquery
#   Cell 2:  paste this file's code, run, then download the .step files it writes.
# Dimensions match the STL shells (bottom_shell.stl / lid.stl) exactly.

import cadquery as cq

# ---------- shared dimensions (mm) ----------
L, W = 130.0, 105.0      # outer footprint (matches PCB edge cuts + clearance)
WALL = 2.0               # wall thickness
BASE = 2.0               # bottom plate thickness
H    = 14.0              # shell height (walls)
USB_W, USB_H = 14.0, 7.0 # USB-C cutout (back wall, y=W side), centred at x=65
SMA_D = 9.0              # SMA antenna hole (right wall, x=L side), centred y=49, z=10
POST  = 6.0              # corner post size
POST_H = 10.0

# ---------- bottom shell ----------
outer = cq.Workplane("XY").box(L, W, BASE + H, centered=(False, False, False))
inner = (cq.Workplane("XY")
         .transformed(offset=(WALL, WALL, BASE))
         .box(L - 2*WALL, W - 2*WALL, H + 1, centered=(False, False, False)))
shell = outer.cut(inner)

# USB-C cutout in back wall (y = W), z from BASE to BASE+USB_H
usb = (cq.Workplane("XY")
       .transformed(offset=(65 - USB_W/2, W - WALL - 0.1, BASE))
       .box(USB_W, WALL + 0.2, USB_H, centered=(False, False, False)))
shell = shell.cut(usb)

# SMA hole through right wall (x = L), centred y=49, z=10
sma = (cq.Workplane("YZ")
       .transformed(offset=cq.Vector(L - WALL - 0.1, 0, 0))
       .center(49, 10)          # (y, z) in YZ plane
       .circle(SMA_D/2).extrude(WALL + 0.2))
shell = shell.cut(sma)

# 4 corner posts
for px, py in [(WALL, WALL), (L-WALL-POST, WALL), (WALL, W-WALL-POST), (L-WALL-POST, W-WALL-POST)]:
    post = (cq.Workplane("XY").transformed(offset=(px, py, BASE))
            .box(POST, POST, POST_H, centered=(False, False, False)))
    shell = shell.union(post)

cq.exporters.export(shell, "bottom_shell.step")

# ---------- lid (2 mm plate + screen window + button window) ----------
lid = cq.Workplane("XY").box(L, W, 2.0, centered=(False, False, False))
screen = (cq.Workplane("XY").transformed(offset=(38, 16, -0.1))
          .box(64, 30, 2.2, centered=(False, False, False)))
buttons = (cq.Workplane("XY").transformed(offset=(33, 53, -0.1))
           .box(74, 44, 2.2, centered=(False, False, False)))
lid = lid.cut(screen).cut(buttons)
cq.exporters.export(lid, "lid.step")

print("Wrote bottom_shell.step and lid.step - download from the Files pane (folder icon, left).")
