"""Manual Computer Graphics algorithms for the Interactive Chessboard PBL."""
from __future__ import annotations
import math
import numpy as np


def scanline_polygon_fill(vertices):
    """Return filled integer pixels and per-scanline intersections using even-odd rule."""
    pts = [(float(x), float(y)) for x, y in vertices]
    if len(pts) < 3:
        raise ValueError("A polygon needs at least three vertices")
    ymin = math.ceil(min(y for _, y in pts)); ymax = math.ceil(max(y for _, y in pts)) - 1
    pixels, steps = [], []
    for y in range(ymin, ymax + 1):
        xs = []
        for i, (x1, y1) in enumerate(pts):
            x2, y2 = pts[(i + 1) % len(pts)]
            # Half-open edge rule avoids counting shared vertices twice.
            if y1 == y2:
                continue
            if min(y1, y2) <= y < max(y1, y2):
                xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
        xs.sort(); spans = []
        for j in range(0, len(xs) - 1, 2):
            left, right = xs[j], xs[j + 1]
            spans.append((left, right))
            for x in range(math.ceil(left), math.floor(right) + 1):
                pixels.append((x, y))
        steps.append({"y": y, "intersections": xs, "spans": spans})
    return pixels, steps


def transform_points(points, tx=0, ty=0, sx=1, sy=1, angle_deg=0, reflect_x=False, reflect_y=False):
    """Apply homogeneous 2D transformations in the documented order: scale, reflect, rotate, translate."""
    p = np.asarray(points, dtype=float)
    if p.ndim != 2 or p.shape[1] != 2:
        raise ValueError("points must have shape (n, 2)")
    rad = math.radians(angle_deg); c, s = math.cos(rad), math.sin(rad)
    S = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]], float)
    F = np.diag([-1 if reflect_x else 1, -1 if reflect_y else 1, 1])
    R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], float)
    T = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]], float)
    homogeneous = np.column_stack([p, np.ones(len(p))])
    out = (T @ R @ F @ S @ homogeneous.T).T
    return out[:, :2], T @ R @ F @ S


def dda_line(x1, y1, x2, y2):
    dx, dy = x2-x1, y2-y1; steps = int(max(abs(dx), abs(dy)))
    if steps == 0: return [(round(x1), round(y1))]
    x_inc, y_inc = dx/steps, dy/steps; x, y = x1, y1; pts=[]
    for _ in range(steps+1):
        pts.append((round(x), round(y))); x += x_inc; y += y_inc
    return pts


def bresenham_line(x1, y1, x2, y2):
    x1,y1,x2,y2=map(int,(x1,y1,x2,y2)); pts=[]
    dx,dy=abs(x2-x1),abs(y2-y1); sx=1 if x1<x2 else -1; sy=1 if y1<y2 else -1
    err=dx-dy
    while True:
        pts.append((x1,y1))
        if x1==x2 and y1==y2: break
        e2=2*err
        if e2 > -dy: err-=dy; x1+=sx
        if e2 < dx: err+=dx; y1+=sy
    return pts


def midpoint_circle(xc, yc, radius):
    if radius < 0: raise ValueError("Radius must be non-negative")
    x, y, d = 0, int(radius), 1-int(radius); pts=set(); steps=[]
    while x <= y:
        octants=[(xc+x,yc+y),(xc-x,yc+y),(xc+x,yc-y),(xc-x,yc-y),(xc+y,yc+x),(xc-y,yc+x),(xc+y,yc-x),(xc-y,yc-x)]
        pts.update(octants); steps.append((x,y,d))
        if d < 0: d += 2*x+3
        else: d += 2*(x-y)+5; y -= 1
        x += 1
    return sorted(pts), steps


def boundary_fill(seed, boundary, fill, max_pixels=100000):
    """4-connected boundary fill over a 2D integer grid; returns changed cells."""
    grid=np.asarray(boundary).copy(); h,w=grid.shape; sx,sy=seed
    if not (0<=sx<w and 0<=sy<h): raise ValueError("Seed outside grid")
    if grid[sy,sx] != 0: return grid, []
    stack=[(sx,sy)]; changed=[]
    while stack and len(changed)<max_pixels:
        x,y=stack.pop()
        if not (0<=x<w and 0<=y<h) or grid[y,x] != 0: continue
        grid[y,x]=fill; changed.append((x,y))
        stack.extend([(x+1,y),(x-1,y),(x,y+1),(x,y-1)])
    return grid, changed


def cohen_sutherland_clip(x1,y1,x2,y2,xmin,ymin,xmax,ymax):
    INSIDE,LEFT,RIGHT,BOTTOM,TOP=0,1,2,4,8
    def code(x,y):
        c=INSIDE
        if x<xmin:c|=LEFT
        elif x>xmax:c|=RIGHT
        if y<ymin:c|=BOTTOM
        elif y>ymax:c|=TOP
        return c
    c1,c2=code(x1,y1),code(x2,y2)
    while True:
        if not (c1|c2): return (x1,y1,x2,y2)
        if c1&c2:return None
        out=c1 or c2
        if out&TOP:
            if y2==y1:return None
            x=x1+(x2-x1)*(ymax-y1)/(y2-y1); y=ymax
        elif out&BOTTOM:
            if y2==y1:return None
            x=x1+(x2-x1)*(ymin-y1)/(y2-y1); y=ymin
        elif out&RIGHT:
            if x2==x1:return None
            y=y1+(y2-y1)*(xmax-x1)/(x2-x1); x=xmax
        else:
            if x2==x1:return None
            y=y1+(y2-y1)*(xmin-x1)/(x2-x1); x=xmin
        if out==c1:x1,y1,c1=x,y,code(x,y)
        else:x2,y2,c2=x,y,code(x,y)


def board_to_screen(file_index, rank_index, origin=(0,0), square_size=64):
    """Map a-h (0..7), ranks 1-8 (0..7 from White's bottom) to top-left screen coordinates."""
    ox,oy=origin
    if not (0<=file_index<8 and 0<=rank_index<8): raise ValueError("Board coordinate out of range")
    return ox+file_index*square_size, oy+(7-rank_index)*square_size


def screen_to_board(px,py,origin=(0,0),square_size=64):
    ox,oy=origin; f=int((px-ox)//square_size); row=int((py-oy)//square_size)
    if not (0<=f<8 and 0<=row<8): return None
    return f,7-row
