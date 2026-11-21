import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import numpy as np
import chess
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Polygon, Circle, Rectangle
from src.cg_algorithms import (scanline_polygon_fill, transform_points, dda_line,
    bresenham_line, midpoint_circle, cohen_sutherland_clip, board_to_screen, screen_to_board)
from src.piece_models import PIECE_POLYGONS

BG='#101827'; PANEL='#172338'; ACCENT='#4f8cff'; TEXT='#e8eef8'; MUTED='#9aaac0'
LIGHT="#e1daec"; DARK='#7890a7'
UNICODE={'K':'♔','Q':'♕','R':'♖','B':'♗','N':'♘','P':'♙','k':'♚','q':'♛','r':'♜','b':'♝','n':'♞','p':'♟'}

class ChessGraphicsApp:
    def __init__(self, root):
        self.root=root; root.title('Interactive Chessboard Graphics System'); root.geometry('1400x900'); root.configure(bg=BG)
        self.board=chess.Board(); self.selected=None; self.flipped=False; self.last_move=None; self.history=[]; self.mode=tk.StringVar(value='Player vs Player')
        self._style(); self._layout(); self.draw_board()

    def _style(self):
        s=ttk.Style(); s.theme_use('clam'); s.configure('TNotebook',background=BG,borderwidth=0); s.configure('TNotebook.Tab',background=PANEL,foreground=TEXT,padding=(14,8)); s.map('TNotebook.Tab',background=[('selected',ACCENT)])
        s.configure('TButton',background=ACCENT,foreground='white',padding=7); s.map('TButton',background=[('active','#356ed0')])
        s.configure('TLabel',background=PANEL,foreground=TEXT)

    def _layout(self):
        header=tk.Frame(self.root,bg=BG); header.pack(fill='x',padx=22,pady=(16,8))
        tk.Label(header,text='♟  INTERACTIVE CHESSBOARD GRAPHICS SYSTEM',bg=BG,fg=TEXT,font=('Segoe UI',20,'bold')).pack(side='left')
        tk.Label(header,text='COMPUTER GRAPHICS  •  PBL TOPIC 17',bg=BG,fg=ACCENT,font=('Segoe UI',10,'bold')).pack(side='right')
        body=tk.Frame(self.root,bg=BG); body.pack(fill='both',expand=True,padx=18,pady=12)
        left=tk.Frame(body,bg=PANEL); left.pack(side='left',fill='y',padx=(0,14))
        tk.Label(left,text='LIVE CHESSBOARD',bg=PANEL,fg=TEXT,font=('Segoe UI',13,'bold')).pack(anchor='w',padx=14,pady=(14,4))
        self.fig=Figure(figsize=(7.2,7.2),dpi=90,facecolor=PANEL); self.ax=self.fig.add_subplot(111); self.ax.set_facecolor(PANEL)
        self.board_canvas=FigureCanvasTkAgg(self.fig,master=left); self.board_canvas.get_tk_widget().pack(padx=10,pady=6)
        self.board_canvas.mpl_connect('button_press_event',self.on_board_click)
        controls=tk.Frame(left,bg=PANEL); controls.pack(fill='x',padx=12,pady=8)
        for label,cmd in [('New Game',self.new_game),('Undo',self.undo),('Flip Board',self.flip_board)]: ttk.Button(controls,text=label,command=cmd).pack(side='left',expand=True,fill='x',padx=3)
        ttk.Combobox(left,textvariable=self.mode,state='readonly',values=['Player vs Player','Player vs Computer (random legal move)'],width=31).pack(padx=12,pady=(0,8))
        self.status=tk.Label(left,text='White to move',bg=PANEL,fg='#8fd6a5',font=('Segoe UI',11,'bold')); self.status.pack(anchor='w',padx=16,pady=(3,2))
        self.move_text=tk.Text(left,height=5,width=56,bg='#0c1422',fg=TEXT,insertbackground=TEXT,relief='flat',font=('Consolas',10)); self.move_text.pack(padx=12,pady=(3,12)); self.move_text.configure(state='disabled')
        right=tk.Frame(body,bg=BG); right.pack(side='left',fill='both',expand=True)
        self.tabs=ttk.Notebook(right); self.tabs.pack(fill='both',expand=True)
        self._build_graphics_tab(); self._build_algorithms_tab(); self._build_models_tab(); self._build_about_tab()

    def draw_board(self):
        self.ax.clear(); self.ax.set_xlim(0,8); self.ax.set_ylim(0,8); self.ax.set_aspect('equal'); self.ax.axis('off')
        for row in range(8):
            for col in range(8):
                x,y=(7-col,7-row) if self.flipped else (col,7-row)
                color=LIGHT if (row+col)%2==0 else DARK
                self.ax.add_patch(Rectangle((x,y),1,1,facecolor=color,edgecolor='#35465a',linewidth=.5))
                sq=chess.square(col,7-row)
                if self.last_move and sq in (self.last_move.from_square,self.last_move.to_square):
                    self.ax.add_patch(Rectangle((x,y),1,1,facecolor='#f6d365',alpha=.48))
                if self.selected==sq:
                    self.ax.add_patch(Rectangle((x,y),1,1,facecolor='#42d392',alpha=.48))
        if self.selected is not None:
            for mv in self.board.legal_moves:
                if mv.from_square==self.selected:
                    col=chess.square_file(mv.to_square); row=chess.square_rank(mv.to_square)
                    x,y=(7-col, row) if self.flipped else (col,7-row)
                    self.ax.add_patch(Circle((x+.5,y+.5),.12,facecolor='#153b2a',alpha=.8))
        for sq,piece in self.board.piece_map().items():
            col,row=chess.square_file(sq),chess.square_rank(sq)
            x,y=(7-col,row) if self.flipped else (col,7-row)
            glyph=UNICODE[piece.symbol()]
            self.ax.text(x+.5,y+.50,glyph,ha='center',va='center',fontsize=39,
                         color='#fffaf0' if piece.color else '#151b25',fontfamily='DejaVu Sans',
                         path_effects=[])
        # labels
        for i in range(8):
            self.ax.text(i+.5,-.18,'abcdefgh'[7-i if self.flipped else i],ha='center',va='center',fontsize=9,color=TEXT)
            self.ax.text(-.18,i+.5,str(i+1 if self.flipped else 8-i),ha='center',va='center',fontsize=9,color=TEXT)
        self.fig.tight_layout(pad=.3); self.board_canvas.draw_idle()
        if self.board.is_checkmate(): status='CHECKMATE — '+('Black' if self.board.turn else 'White')+' wins'
        elif self.board.is_stalemate(): status='DRAW — Stalemate'
        elif self.board.is_check(): status=('White' if self.board.turn else 'Black')+' to move — CHECK'
        elif self.board.is_game_over(): status='GAME OVER — '+self.board.result()
        else: status=('White' if self.board.turn else 'Black')+' to move'
        self.status.config(text=status)
        self.move_text.configure(state='normal'); self.move_text.delete('1.0','end')
        sans=[]
        for i,m in enumerate(self.board.move_stack):
            sans.append(f'{i//2+1}. ' if i%2==0 else '')
            sans.append(self.board.san(m)+'   ')
        self.move_text.insert('end',''.join(sans)); self.move_text.configure(state='disabled')

    def on_board_click(self,event):
        if event.xdata is None or event.ydata is None or self.board.is_game_over(): return
        x,y=int(event.xdata),int(event.ydata)
        if not (0<=x<8 and 0<=y<8): return
        col,row=(7-x,y) if self.flipped else (x,7-y); sq=chess.square(col,row)
        piece=self.board.piece_at(sq)
        if self.selected is None:
            if piece and piece.color==self.board.turn: self.selected=sq
        else:
            move=chess.Move(self.selected,sq)
            if self.board.piece_at(self.selected) and self.board.piece_at(self.selected).piece_type==chess.PAWN and chess.square_rank(sq) in (0,7):
                move.promotion=chess.QUEEN
            if move in self.board.legal_moves:
                self.history.append(self.board.fen()); self.last_move=move; self.board.push(move); self.selected=None
                if self.mode.get().startswith('Player vs Computer') and not self.board.is_game_over() and self.board.turn==chess.BLACK:
                    legal=list(self.board.legal_moves)
                    if legal:
                        computer_move=random.choice(legal); self.board.push(computer_move); self.last_move=computer_move
            elif piece and piece.color==self.board.turn: self.selected=sq
            else: self.selected=None
        self.draw_board()

    def new_game(self): self.board.reset(); self.selected=None; self.last_move=None; self.history.clear(); self.draw_board()
    def undo(self):
        if self.board.move_stack: self.board.pop(); self.selected=None; self.last_move=self.board.peek() if self.board.move_stack else None; self.draw_board()
    def flip_board(self): self.flipped=not self.flipped; self.draw_board()

    def _tab(self,title):
        frame=tk.Frame(self.tabs,bg=PANEL); self.tabs.add(frame,text=title); return frame
    def _build_graphics_tab(self):
        tab=self._tab('Transformations & Models')
        tk.Label(tab,text='2D TRANSFORMATION PLAYGROUND',bg=PANEL,fg=TEXT,font=('Segoe UI',15,'bold')).pack(anchor='w',padx=18,pady=(16,4))
        tk.Label(tab,text='Apply homogeneous-coordinate transformations to a model polygon. Original and transformed geometry are shown together.',bg=PANEL,fg=MUTED,wraplength=620).pack(anchor='w',padx=18)
        controls=tk.Frame(tab,bg=PANEL); controls.pack(fill='x',padx=18,pady=12)
        self.vars={}
        for name,default in [('tx','1.0'),('ty','0.5'),('sx','1.2'),('sy','0.8'),('angle','30')]:
            box=tk.Frame(controls,bg=PANEL); box.pack(side='left',padx=5)
            tk.Label(box,text=name.upper(),bg=PANEL,fg=MUTED).pack()
            v=tk.StringVar(value=default); self.vars[name]=v; tk.Entry(box,textvariable=v,width=7,bg='#0c1422',fg=TEXT,insertbackground=TEXT,relief='flat').pack()
        self.reflect_x=tk.BooleanVar(); self.reflect_y=tk.BooleanVar()
        tk.Checkbutton(controls,text='Reflect X',variable=self.reflect_x,bg=PANEL,fg=TEXT,selectcolor=BG).pack(side='left',padx=6)
        tk.Checkbutton(controls,text='Reflect Y',variable=self.reflect_y,bg=PANEL,fg=TEXT,selectcolor=BG).pack(side='left',padx=6)
        ttk.Button(controls,text='Apply Matrix',command=self.plot_transform).pack(side='left',padx=8)
        self.transform_fig=Figure(figsize=(7,4.7),dpi=95,facecolor=PANEL); self.transform_ax=self.transform_fig.add_subplot(111); self.transform_canvas=FigureCanvasTkAgg(self.transform_fig,master=tab); self.transform_canvas.get_tk_widget().pack(fill='both',expand=True,padx=14,pady=6)
        self.matrix_label=tk.Label(tab,text='Matrix: identity',bg=PANEL,fg='#a9c7ff',font=('Consolas',10)); self.matrix_label.pack(anchor='w',padx=18,pady=6)
        self.plot_transform()

    def plot_transform(self):
        try:
            vals={k:float(v.get()) for k,v in self.vars.items()}
            pts=np.array([[0,0],[2,0],[2,1],[1,1.7],[0,1]])
            out,M=transform_points(pts,tx=vals['tx'],ty=vals['ty'],sx=vals['sx'],sy=vals['sy'],angle_deg=vals['angle'],reflect_x=self.reflect_x.get(),reflect_y=self.reflect_y.get())
            ax=self.transform_ax; ax.clear(); ax.set_facecolor('#0c1422'); ax.grid(True,alpha=.2); ax.axhline(0,color='#66758a',lw=.7); ax.axvline(0,color='#66758a',lw=.7)
            ax.add_patch(Polygon(pts,closed=True,fill=False,edgecolor='#f6c85f',linewidth=2,label='Original'))
            ax.add_patch(Polygon(out,closed=True,fill=True,facecolor='#4f8cff',alpha=.28,edgecolor='#4f8cff',linewidth=2,label='Transformed'))
            ax.legend(facecolor=PANEL,labelcolor=TEXT); ax.set_aspect('equal'); ax.set_title('Homogeneous 2D Transformations',color=TEXT); ax.tick_params(colors=MUTED)
            self.transform_fig.tight_layout(); self.transform_canvas.draw_idle(); self.matrix_label.config(text='Composite matrix (T · R · F · S):\n'+np.array2string(M,precision=3,suppress_small=True))
        except Exception as e: messagebox.showerror('Invalid transformation input',str(e))

    def _build_algorithms_tab(self):
        tab=self._tab('Algorithms Lab')
        tk.Label(tab,text='MANUAL COMPUTER GRAPHICS ALGORITHMS',bg=PANEL,fg=TEXT,font=('Segoe UI',15,'bold')).pack(anchor='w',padx=18,pady=(16,4))
        bar=tk.Frame(tab,bg=PANEL); bar.pack(fill='x',padx=18,pady=8)
        self.alg=tk.StringVar(value='Scan-Line Polygon Fill'); ttk.Combobox(bar,textvariable=self.alg,state='readonly',values=['Scan-Line Polygon Fill','DDA Line','Bresenham Line','Midpoint Circle','Cohen-Sutherland Clipping','Coordinate Mapping'],width=28).pack(side='left')
        ttk.Button(bar,text='Run Visualization',command=self.run_algorithm).pack(side='left',padx=8)
        self.alg_fig=Figure(figsize=(7,4.8),dpi=95,facecolor=PANEL); self.alg_ax=self.alg_fig.add_subplot(111); self.alg_canvas=FigureCanvasTkAgg(self.alg_fig,master=tab); self.alg_canvas.get_tk_widget().pack(fill='both',expand=True,padx=14,pady=6)
        self.alg_info=tk.Label(tab,text='',bg=PANEL,fg='#a9c7ff',justify='left',anchor='w',font=('Consolas',10),wraplength=780); self.alg_info.pack(fill='x',padx=18,pady=8)
        self.run_algorithm()

    def run_algorithm(self):
        name=self.alg.get(); ax=self.alg_ax; ax.clear(); ax.set_facecolor('#0c1422'); ax.grid(True,alpha=.15)
        if name=='Scan-Line Polygon Fill':
            poly=[(1,1),(6,1),(7,4),(4,7),(2,5)]; pix,steps=scanline_polygon_fill(poly)
            ax.add_patch(Polygon(poly,closed=True,fill=False,edgecolor='#f6c85f',lw=2))
            if pix:
                xs,ys=zip(*pix); ax.scatter(xs,ys,s=18,c='#4f8cff',marker='s')
            for st in steps[::2]: ax.axhline(st['y'],color='#70d6b5',alpha=.25,lw=.6)
            self.alg_info.config(text=f'Scan-Line Polygon Filling\nVertices: {poly}\nScan lines processed: {len(steps)} | Filled pixel samples: {len(pix)}\nMethod: edge intersections → sort x values → fill alternate spans (even-odd rule).')
        elif name in ('DDA Line','Bresenham Line'):
            pts=dda_line(1,2,12,8) if name=='DDA Line' else bresenham_line(1,2,12,8)
            ax.plot([1,12],[2,8],color='#f6c85f',lw=1,alpha=.5); xs,ys=zip(*pts); ax.scatter(xs,ys,c='#4f8cff',s=45,marker='s')
            self.alg_info.config(text=f'{name}\nInput line: (1,2) to (12,8)\nGenerated pixels: {len(pts)}\nThe plotted squares are the integer raster positions calculated by the algorithm.')
        elif name=='Midpoint Circle':
            pts,steps=midpoint_circle(0,0,7); xs,ys=zip(*pts); ax.scatter(xs,ys,c='#4f8cff',s=30,marker='s'); ax.set_aspect('equal')
            self.alg_info.config(text=f'Midpoint Circle Drawing\nCentre: (0,0), radius: 7\nFirst-octant decision steps: {len(steps)}\nEight-way symmetry reflects each calculated point into the remaining octants.')
        elif name=='Cohen-Sutherland Clipping':
            seg=(-3,2,10,9); clip=cohen_sutherland_clip(*seg,0,0,8,6)
            ax.add_patch(Rectangle((0,0),8,6,fill=False,edgecolor='#70d6b5',lw=2)); ax.plot([seg[0],seg[2]],[seg[1],seg[3]],'--',color='#f6c85f',label='Original')
            if clip: ax.plot([clip[0],clip[2]],[clip[1],clip[3]],color='#4f8cff',lw=3,label='Clipped')
            ax.legend(facecolor=PANEL,labelcolor=TEXT)
            self.alg_info.config(text=f'Cohen-Sutherland Line Clipping\nWindow: [0,8] × [0,6]\nOriginal segment: {seg}\nClipped segment: {clip}')
        else:
            p=board_to_screen(4,3,origin=(20,20),square_size=64); back=screen_to_board(*p,origin=(20,20),square_size=64)
            ax.add_patch(Rectangle((0,0),8,8,fill=False,edgecolor='#70d6b5',lw=2)); ax.scatter([4.5],[4.5],s=120,c='#4f8cff'); ax.text(4.7,4.5,'e4 → screen',color=TEXT)
            self.alg_info.config(text=f'Coordinate Mapping\nChess square e4 (file=4, rank=3 from rank 1) → top-left pixel {p}\nInverse conversion → {back}\nMapping formula: px = ox + file·s; py = oy + (7−rank)·s.')
        ax.tick_params(colors=MUTED); ax.set_title(name,color=TEXT); self.alg_fig.tight_layout(); self.alg_canvas.draw_idle()


    def _build_models_tab(self):
        tab=self._tab('Object Modelling')
        tk.Label(tab,text='CHESS PIECES AS GEOMETRIC MODELS',bg=PANEL,fg=TEXT,font=('Segoe UI',15,'bold')).pack(anchor='w',padx=18,pady=(16,4))
        tk.Label(tab,text='Normalized polygon silhouettes are assembled from vertices in src/piece_models.py. This panel demonstrates the local geometric model data.',bg=PANEL,fg=MUTED,wraplength=700).pack(anchor='w',padx=18)
        fig=Figure(figsize=(7.3,4.7),dpi=95,facecolor=PANEL); ax=fig.add_subplot(111); ax.set_facecolor('#0c1422')
        from matplotlib.patches import Polygon as MPolygon, Circle as MCircle
        labels=['King','Queen','Rook','Bishop','Knight','Pawn']; codes=['K','Q','R','B','N','P']
        for i,(label,code) in enumerate(zip(labels,codes)):
            x=i*2.0
            pts=np.asarray(PIECE_POLYGONS[code][0],dtype=float)
            pts[:,0]=pts[:,0]*.85+x+.5; pts[:,1]=pts[:,1]*.85+1.1
            ax.add_patch(MPolygon(pts,closed=True,facecolor='#4f8cff',edgecolor='#dce8ff',linewidth=1.6,alpha=.85))
            ax.add_patch(MCircle((x+.5,.55),.32,facecolor='#f6c85f',edgecolor='#fff0c2',alpha=.9))
            ax.text(x+.5,.05,label,ha='center',color=TEXT,fontsize=10)
        ax.set_xlim(-.5,11.5); ax.set_ylim(-.3,2.2); ax.set_aspect('equal'); ax.axis('off'); fig.tight_layout()
        canvas=FigureCanvasTkAgg(fig,master=tab); canvas.get_tk_widget().pack(fill='both',expand=True,padx=14,pady=8); canvas.draw()

    def _build_about_tab(self):
        tab=self._tab('Project & Concepts')
        content=("PROJECT: Interactive Chessboard Graphics System\n\n"
        "Selected faculty topic: 17 — Interactive Chessboard Graphics System\n\n"
        "Core Computer Graphics concepts demonstrated:\n"
        "• Scan-Line Polygon Filling — edge intersections and even-odd filling\n"
        "• 2D Transformations — homogeneous matrices for translation, rotation, scaling and reflection\n"
        "• Object Modelling — chess piece silhouettes assembled from geometric primitives\n"
        "• Coordinate Systems — chess square ↔ Cartesian/screen coordinate mapping\n\n"
        "Additional manual algorithms:\n"
        "• DDA line drawing  • Bresenham line drawing  • Midpoint circle drawing\n"
        "• Cohen-Sutherland line clipping\n\n"
        "Chess rules are handled by python-chess; graphics algorithms are implemented separately in src/cg_algorithms.py.\n\n"
        "Team (as supplied):\nShivam — 1/24/SET/BCS/159\nDeepak — 1/24/SET/BCS/165\nSameer — 1/24/SET/BCS/154\nAbhay — 1/24/SET/BCS/157\n\n"
        "Faculty name and course code should be confirmed from the Computer Graphics course details before final submission.")
        tk.Label(tab,text=content,bg=PANEL,fg=TEXT,justify='left',anchor='nw',font=('Segoe UI',12),padx=24,pady=24).pack(fill='both',expand=True)

if __name__=='__main__':
    root=tk.Tk(); app=ChessGraphicsApp(root); root.mainloop()
