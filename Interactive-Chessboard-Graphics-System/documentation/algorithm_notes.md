# Computer Graphics Algorithm Notes

## Scan-Line Polygon Filling
For each integer scanline y, inspect every polygon edge using a half-open vertical interval. For a non-horizontal edge `(x1,y1)`–`(x2,y2)`, calculate `x = x1 + (y-y1)(x2-x1)/(y2-y1)`. Sort intersections and fill alternate pairs (even-odd rule). For V vertices and H scanlines, the straightforward implementation is O(H·V + H·I log I), where I is the number of intersections on a scanline.

## Homogeneous 2D Transformations
Represent a point as `[x,y,1]^T`. Translation, scaling, rotation and reflection are 3×3 matrices. This implementation composes `T·R·F·S`, so scaling and reflection occur first, followed by rotation and translation. Matrix multiplication order matters.

## DDA
Choose `steps=max(|dx|,|dy|)`, increment x and y by `dx/steps` and `dy/steps`, and round each generated location.

## Bresenham
Use an integer error accumulator to choose the next raster pixel while minimizing floating-point arithmetic.

## Midpoint Circle
Use the circle decision parameter and eight-way symmetry. Only one octant is calculated directly.

## Cohen–Sutherland
Assign a four-bit region code to each endpoint. Accept when both codes are zero; reject when their bitwise AND is nonzero; otherwise intersect the outside endpoint with the relevant clipping boundary and repeat.

## Coordinate Mapping
For a square size s and top-left origin (ox,oy), `px=ox+file·s`, `py=oy+(7-rank)·s`. The inverse uses integer division and reverses the screen row.
