import os,sys
sys.path.insert(0,os.path.dirname(__file__))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Rectangle
from src.cg_algorithms import scanline_polygon_fill,transform_points,dda_line,bresenham_line,midpoint_circle,cohen_sutherland_clip
OUT=os.path.join(os.path.dirname(__file__),'screenshots')
# Scanline
poly=[(1,1),(6,1),(7,4),(4,7),(2,5)]; pix,steps=scanline_polygon_fill(poly)
fig,ax=plt.subplots(figsize=(7,5)); ax.add_patch(Polygon(poly,closed=True,fill=False,edgecolor='black',lw=2));
if pix: ax.scatter(*zip(*pix),s=18,c='royalblue',marker='s')
for st in steps[::2]: ax.axhline(st['y'],color='seagreen',alpha=.35,lw=.8)
ax.set_title('Scan-Line Polygon Filling — manual output'); ax.set_aspect('equal'); ax.grid(alpha=.2); fig.tight_layout(); fig.savefig(os.path.join(OUT,'scanline_polygon_fill.png'),dpi=160); plt.close(fig)
# transforms
pts=[(0,0),(2,0),(2,1),(1,1.7),(0,1)]; out,M=transform_points(pts,tx=1,ty=.5,sx=1.2,sy=.8,angle_deg=30)
fig,ax=plt.subplots(figsize=(7,5)); ax.add_patch(Polygon(pts,closed=True,fill=False,edgecolor='darkorange',lw=2,label='Original')); ax.add_patch(Polygon(out,closed=True,alpha=.3,edgecolor='royalblue',facecolor='royalblue',lw=2,label='Transformed')); ax.legend(); ax.set_title('Homogeneous 2D Transformations'); ax.grid(alpha=.2); ax.set_aspect('equal'); fig.tight_layout(); fig.savefig(os.path.join(OUT,'transformations.png'),dpi=160); plt.close(fig)
# rasterization
p1=dda_line(1,2,12,8); p2=bresenham_line(1,2,12,8)
fig,axs=plt.subplots(1,2,figsize=(10,4));
for ax,pts,title in [(axs[0],p1,'DDA'),(axs[1],p2,'Bresenham')]: ax.scatter(*zip(*pts),s=65,marker='s'); ax.set_title(title+' Line Drawing'); ax.grid(alpha=.3); ax.set_aspect('equal')
fig.tight_layout(); fig.savefig(os.path.join(OUT,'line_drawing_algorithms.png'),dpi=160); plt.close(fig)
# circle and clipping
cpts,_=midpoint_circle(0,0,7); seg=(-3,2,10,9); clip=cohen_sutherland_clip(*seg,0,0,8,6)
fig,axs=plt.subplots(1,2,figsize=(10,4)); axs[0].scatter(*zip(*cpts),s=20); axs[0].set_title('Midpoint Circle Drawing'); axs[0].set_aspect('equal'); axs[0].grid(alpha=.3)
axs[1].add_patch(Rectangle((0,0),8,6,fill=False,edgecolor='green',lw=2)); axs[1].plot([seg[0],seg[2]],[seg[1],seg[3]],'--',label='Original'); axs[1].plot([clip[0],clip[2]],[clip[1],clip[3]],lw=3,label='Clipped'); axs[1].set_title('Cohen–Sutherland Clipping'); axs[1].legend(); axs[1].grid(alpha=.3); fig.tight_layout(); fig.savefig(os.path.join(OUT,'circle_and_clipping.png'),dpi=160); plt.close(fig)
