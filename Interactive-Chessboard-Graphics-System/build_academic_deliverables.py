from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pptx import Presentation
from pptx.util import Inches as PInches, Pt as PPt
from pptx.dml.color import RGBColor as PRGB
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
import os, sys

ROOT=os.path.dirname(__file__); ASSET='/mnt/data/template_assets'
OUT_DOC=os.path.join(ROOT,'Interactive_Chessboard_Graphics_PBL_Report.docx')
OUT_PPT=os.path.join(ROOT,'Interactive_Chessboard_Graphics_PBL_Presentation.pptx')
TEAM=[('Shivam','1/24/SET/BCS/159'),('Deepak','1/24/SET/BCS/165'),('Sameer','1/24/SET/BCS/154'),('Abhay','1/24/SET/BCS/157')]

# ---------- DOCX ----------
d=Document(); sec=d.sections[0]; sec.top_margin=Inches(.72); sec.bottom_margin=Inches(.72); sec.left_margin=Inches(.85); sec.right_margin=Inches(.85)
styles=d.styles
styles['Normal'].font.name='Times New Roman'; styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'),'Times New Roman'); styles['Normal'].font.size=Pt(11)
styles['Normal'].paragraph_format.space_after=Pt(6)
for nm,size in [('Title',25),('Heading 1',18),('Heading 2',14),('Heading 3',12)]:
    st=styles[nm]; st.font.name='Times New Roman'; st.font.size=Pt(size); st.font.bold=True; st.font.color.rgb=RGBColor(31,57,105)
    st._element.rPr.rFonts.set(qn('w:eastAsia'),'Times New Roman')
# header/footer inspired by uploaded PBL report template
header=sec.header.paragraphs[0]; header.alignment=WD_ALIGN_PARAGRAPH.RIGHT
r=header.add_run('PBL  |  PROJECT BASED LEARNING'); r.bold=True; r.font.name='Times New Roman'; r.font.size=Pt(9); r.font.color.rgb=RGBColor(90,105,130)
footer=sec.footer.paragraphs[0]; footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
rr=footer.add_run('Computer Graphics  |  Interactive Chessboard Graphics System  |  '); rr.font.size=Pt(8); rr.font.color.rgb=RGBColor(100,110,125)
fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); footer._p.append(fld)

def p(text='',bold=False,align=None,italic=False,size=None):
    para=d.add_paragraph();
    if align is not None: para.alignment=align
    run=para.add_run(text); run.bold=bold; run.italic=italic; run.font.name='Times New Roman'
    if size: run.font.size=Pt(size)
    return para

def heading(text,level=1): d.add_heading(text,level=level)
def bullet(text): d.add_paragraph(text,style='List Bullet')
def numbered(text): d.add_paragraph(text,style='List Number')
def page(): d.add_page_break()
def table(headers, rows, widths=None):
    t=d.add_table(rows=1, cols=len(headers)); t.style='Light Shading Accent 1'
    for i,h in enumerate(headers): t.rows[0].cells[i].text=h
    for row in rows:
        cells=t.add_row().cells
        for i,val in enumerate(row): cells[i].text=str(val)
    return t

# cover
p('MANAV RACHNA INTERNATIONAL INSTITUTE OF RESEARCH AND STUDIES',True,WD_ALIGN_PARAGRAPH.CENTER, size=14)
p('Deemed to be University',False,WD_ALIGN_PARAGRAPH.CENTER,size=10)
if os.path.exists(os.path.join(ASSET,'image1.png')):
    pp=d.add_paragraph(); pp.alignment=WD_ALIGN_PARAGRAPH.CENTER; pp.add_run().add_picture(os.path.join(ASSET,'image1.png'),width=Inches(6.4))
p('PROJECT BASED LEARNING',True,WD_ALIGN_PARAGRAPH.CENTER,size=18)
p('COMPUTER GRAPHICS — PBL REPORT',True,WD_ALIGN_PARAGRAPH.CENTER,size=14)
p('INTERACTIVE CHESSBOARD GRAPHICS SYSTEM',True,WD_ALIGN_PARAGRAPH.CENTER,size=22)
p('An interactive chess visualization system demonstrating polygon filling, geometric transformations, object modelling and coordinate systems',False,WD_ALIGN_PARAGRAPH.CENTER,italic=True,size=12)
p('Submitted by',True,WD_ALIGN_PARAGRAPH.CENTER)
for name,reg in TEAM: p(f'{name} ({reg})',False,WD_ALIGN_PARAGRAPH.CENTER)
p('Submitted to',True,WD_ALIGN_PARAGRAPH.CENTER)
p('Faculty Name: To be confirmed',False,WD_ALIGN_PARAGRAPH.CENTER)
p('Department of Computer Science and Engineering',False,WD_ALIGN_PARAGRAPH.CENTER)
p('Manav Rachna International Institute of Research and Studies',False,WD_ALIGN_PARAGRAPH.CENTER)
p('Academic Year: 2026–2027  |  Semester: To be confirmed',True,WD_ALIGN_PARAGRAPH.CENTER)
page()

heading('INDEX',1)
index_rows=[('1','Abstract','3'),('2','Introduction','4'),('3','Objectives','5'),('4','System Analysis','6'),('5','CG Concepts and Methodology','7'),('6','Implementation','8'),('7','Output','9'),('8','Results and Discussion','10'),('9','Conclusion and Future Work','11'),('10','References','12')]
table(['S. No.','Section','Page'],index_rows)
p('The section sequence follows the supplied PBL report template. The content has been adapted to the Computer Graphics topic and faculty requirements.',italic=True)
page()

heading('ABSTRACT',1)
p('The Interactive Chessboard Graphics System is a Python desktop application designed to demonstrate fundamental Computer Graphics concepts through an interactive chess visualization environment. The project combines an 8×8 chessboard interface with independent implementations of Scan-Line Polygon Filling, homogeneous 2D transformations, coordinate mapping, DDA line drawing, Bresenham line drawing, Midpoint Circle Drawing and Cohen–Sutherland line clipping. Chess piece shapes are represented through geometric modelling ideas using polygons and other primitives. Users can select chess pieces, view legal destinations, inspect move history, undo moves, restart the game and flip the board. A separate Graphics Algorithms Lab visualizes intermediate algorithm operations rather than showing only final output. The chess-rule layer uses the python-chess package, while the core graphics algorithms are implemented manually in the project source. The design keeps gameplay and Computer Graphics implementation separate so that the application remains useful as both a chess interface and an academic algorithm demonstrator.')
p('Keywords: Computer Graphics, Chessboard, Polygon Filling, Homogeneous Coordinates, 2D Transformations, Object Modelling, Coordinate Mapping.',italic=True)
page()

heading('CHAPTER 1 — INTRODUCTION',1)
heading('1.1 Background',2)
p('Computer Graphics deals with the creation, representation, manipulation and display of visual objects. A chessboard provides a clear geometric environment: it contains repeated square regions, coordinate-labelled positions, and distinct objects that move between discrete locations. This makes it suitable for demonstrating rasterization, polygon filling, transformations and coordinate conversion.')
heading('1.2 Problem Statement',2)
p('A basic chess application may display pieces and allow moves, but it often hides the graphics operations that create the board and objects. The project addresses this learning gap by combining a playable chess interface with a separate laboratory that exposes the mathematical and algorithmic steps used to generate and transform graphics.')
heading('1.3 Motivation',2)
p('The motivation is to connect classroom Computer Graphics topics with a familiar interactive application. Students can observe how geometric primitives form chess-piece silhouettes, how coordinate systems map a selected square to a screen location, and how scan-line filling and transformation matrices affect rendered shapes.')
heading('1.4 Scope',2)
bullet('Interactive 8×8 chessboard with legal-move selection, turn indication, move history, undo, restart and board orientation control.')
bullet('Manual implementations of core rasterization and geometric algorithms in Python.')
bullet('A visual lab for polygon filling, line drawing, circle drawing, clipping, transformations and coordinate conversion.')
bullet('Academic documentation, testing and demonstration material.')
heading('1.5 System Boundary',2)
p('The chess rules engine and the Computer Graphics algorithms are separate modules. python-chess is used only for rule correctness; it is not used to perform polygon filling, transformations, rasterization or coordinate mapping.')
page()

heading('CHAPTER 2 — OBJECTIVES',1)
for x in ['To develop an interactive 8×8 chessboard with clear graphical representation of all chess pieces.','To implement Scan-Line Polygon Filling manually and visualize scanline intersections and filled spans.','To apply translation, scaling, rotation, reflection and composite transformations using homogeneous coordinate matrices.','To model chess-piece silhouettes using geometric primitives such as polygons, circles and curves.','To implement coordinate conversion between chessboard, Cartesian and screen coordinate systems.','To demonstrate additional algorithms including DDA, Bresenham, Midpoint Circle and Cohen–Sutherland clipping.','To provide user-controlled inputs, intermediate visualizations, test cases and technical documentation.']:
    numbered(x)
heading('2.1 Expected Learning Outcomes',2)
p('On completion, students should be able to explain the difference between game rules and graphics rendering, derive 2D transformation matrices, calculate scanline-edge intersections, describe rasterization decisions, and test coordinate conversion with known inputs.')
page()

heading('CHAPTER 3 — SYSTEM ANALYSIS',1)
heading('3.1 Existing Approach',2)
p('A conventional chess interface primarily focuses on game state and piece movement. A graphics algorithm is often hidden inside a rendering library. Such an approach is convenient for gameplay but does not expose the intermediate steps required for a Computer Graphics laboratory demonstration.')
heading('3.2 Proposed System',2)
p('The proposed application provides two connected areas: (1) a chessboard for interactive play and (2) a Graphics Algorithms Lab for independently running and observing manual algorithms. The system separates game legality, algorithm computation and graphical presentation.')
heading('3.3 System Architecture',2)
p('User Interaction → Tkinter Interface → Chess State Module → Board Renderer → Matplotlib Canvas. For the algorithm laboratory: User Parameters → Manual CG Algorithm Module → Intermediate Data → Matplotlib Visualization → Explanation and Result.')
heading('3.4 Functional Requirements',2)
for x in ['Render an 8×8 alternating-colour board and distinguish white and black pieces.','Select a piece and highlight legal destination squares.','Maintain turn state, move history, undo and restart operations.','Run graphics algorithms with visible intermediate and final results.','Accept transformation parameters and update the transformed polygon.','Convert board coordinates to screen positions and convert screen positions back to board cells.']:
    bullet(x)
heading('3.5 Non-Functional Requirements',2)
p('The application should be modular, readable, responsive on a standard Windows desktop, reproducible using requirements.txt, and sufficiently clear for a live faculty demonstration. Errors in numeric input should be reported without terminating the application.')
page()

heading('CHAPTER 4 — CG CONCEPTS AND METHODOLOGY',1)
heading('4.1 Scan-Line Polygon Filling',2)
p('For each scanline y, the algorithm finds intersections with polygon edges. Horizontal edges are ignored. A half-open vertical edge rule avoids double-counting shared vertices. The x-intersections are sorted and filled in pairs according to the even-odd rule. For an edge from (x1,y1) to (x2,y2), the intersection is x = x1 + (y−y1)(x2−x1)/(y2−y1).')
p('The implementation returns both filled integer pixel coordinates and a trace of scanline intersections. This supports a step-oriented visualization and allows a user-supplied polygon to be tested.')
heading('4.2 Homogeneous 2D Transformations',2)
p('A 2D point is represented as P = [x, y, 1]ᵀ. Translation uses T = [[1,0,tx],[0,1,ty],[0,0,1]]. Scaling uses S = [[sx,0,0],[0,sy,0],[0,0,1]]. Rotation uses R = [[cosθ,−sinθ,0],[sinθ,cosθ,0],[0,0,1]]. Reflection is represented by sign changes in the x or y diagonal entries. The code composes T·R·F·S; therefore scaling and reflection are applied before rotation and translation.')
heading('4.3 Object Modelling',2)
p('Chess pieces are treated as composite geometric objects. A model can combine polygonal outlines, circles or ellipses, line segments and curves. The project includes normalized silhouette vertex definitions for King, Queen, Rook, Bishop, Knight and Pawn in src/piece_models.py. The model can be scaled and positioned in a local coordinate frame before mapping to a board square.')
heading('4.4 Coordinate Systems',2)
p('For square size s and top-left screen origin (ox,oy), the board-to-screen mapping is px = ox + file·s and py = oy + (7−rank)·s, where file and rank are zero-based from a1. The inverse mapping uses integer division and reverses the screen row. Out-of-board clicks return no square.')
heading('4.5 Additional Algorithms',2)
table(['Algorithm','Purpose in the project','Key idea'],[
('DDA Line Drawing','Rasterize a segment','Increment x and y by fixed fractional steps'),
('Bresenham Line Drawing','Integer line rasterization','Use an integer decision/error accumulator'),
('Midpoint Circle','Rasterize circular details','Calculate one octant and use eight-way symmetry'),
('Cohen–Sutherland','Clip a line to a window','Use 4-bit endpoint region codes and boundary intersections')])
page()

heading('CHAPTER 5 — IMPLEMENTATION',1)
heading('5.1 Technology Stack',2)
table(['Technology','Role'],[('Python 3.x','Application and algorithm implementation'),('NumPy','Homogeneous matrix and numerical operations'),('Matplotlib','Board and algorithm visualization'),('Tkinter / ttk','Desktop controls and tabs'),('python-chess','Legal chess move and game-state validation')])
heading('5.2 Module Structure',2)
for x in ['main.py — desktop application, board rendering, mouse interaction and tab navigation.','src/cg_algorithms.py — Scan-Line Fill, transformations, DDA, Bresenham, Midpoint Circle, Boundary Fill, Cohen–Sutherland and coordinate mapping.','src/piece_models.py — normalized polygon silhouette definitions for chess pieces.','tests/test_algorithms.py — unit tests for numerical and geometric algorithms.']:
    bullet(x)
heading('5.3 Chess Interaction Workflow',2)
p('The user clicks a piece belonging to the active side. Legal destination squares are obtained from the chess rules module and highlighted. A second click on a legal destination creates a move; a pawn reaching the final rank is promoted to a queen by default in the current interface. The move is pushed to the game state and the board is redrawn. Undo pops the most recent move; New Game resets the position; Flip Board changes the viewing orientation.')
heading('5.4 Algorithm Execution Workflow',2)
p('The user selects an algorithm and requests visualization. The manual function calculates output points or intermediate data. Matplotlib then plots the result and the interface displays the input, number of generated points or scanlines, and a concise explanation. The visualization is intentionally separate from the chess legality engine.')
heading('5.5 Important Implementation Notes',2)
p('The scan-line implementation uses a half-open edge rule and excludes the maximum-y boundary scanline. The transformation function accepts an n×2 point array and returns both transformed points and the composite 3×3 matrix. Coordinate conversion validates board bounds. Cohen–Sutherland repeatedly clips the endpoint outside the window until the segment is accepted or trivially rejected.')
page()

heading('CHAPTER 6 — OUTPUT',1)
p('The application is designed to show the following outputs during demonstration. Screenshots should be captured from the running Windows application after installing the dependencies; this report does not substitute mock screenshots for the final application.')
for x in ['Live chessboard: initial position, selected piece and highlighted legal moves.','Move history and status: active player, check state, checkmate or draw status.','Transformation Playground: original polygon and transformed polygon shown together, with the composite matrix displayed.','Scan-Line Polygon Fill: polygon outline, scanline intersections and filled pixel locations.','DDA and Bresenham: rasterized integer pixels for a sample line segment.','Midpoint Circle: symmetric raster points generated from the first octant.','Cohen–Sutherland: original segment and accepted clipped segment inside a rectangular window.','Coordinate Mapping: board square converted to screen position and inverse conversion result.']:
    bullet(x)
heading('6.1 Screenshot Checklist',2)
table(['Screenshot ID','Capture after running','Evidence'],[
('SS-01','Initial chessboard','Board orientation, all pieces and coordinate labels'),('SS-02','Selected piece','Legal move destination markers'),('SS-03','Transformation tab','Original/transformed polygon and matrix'),('SS-04','Scan-line fill','Polygon and filled pixel output'),('SS-05','Rasterization','DDA/Bresenham pixel points'),('SS-06','Clipping','Original and clipped line')])
imgs=[('scanline_polygon_fill.png','Figure 6.1 — Scan-Line Polygon Filling'),('transformations.png','Figure 6.2 — Homogeneous Transformations'),('line_drawing_algorithms.png','Figure 6.3 — DDA and Bresenham'),('circle_and_clipping.png','Figure 6.4 — Circle and Line Clipping')]
grid=d.add_table(rows=2,cols=2); grid.autofit=False
for n,(img,caption) in enumerate(imgs):
    imgpath=os.path.join(ROOT,'screenshots',img); cell=grid.cell(n//2,n%2)
    if os.path.exists(imgpath):
        pp=cell.paragraphs[0]; pp.alignment=WD_ALIGN_PARAGRAPH.CENTER; pp.add_run().add_picture(imgpath,width=Inches(3.0))
        cp=cell.add_paragraph(caption); cp.alignment=WD_ALIGN_PARAGRAPH.CENTER; cp.runs[0].italic=True; cp.runs[0].font.size=Pt(8)

heading('CHAPTER 7 — RESULTS AND DISCUSSION',1)
p('The manual Computer Graphics algorithms were checked using unit tests. The test suite covers polygon filling, translation, 90-degree rotation, DDA and Bresenham endpoints, circle symmetry, line clipping and coordinate round-trip conversion. The current local test run completed with 7 tests passing.')
table(['Test ID','Input / operation','Expected result','Observed result'],[
('CG-01','Fill a 3×3 axis-aligned square','12 interior/boundary raster samples over 3 scanlines under half-open edge rule','Passed'),
('CG-02','Translate point (1,2) by (3,−1)','(4,1)','Passed'),
('CG-03','Rotate (1,0) by 90°','Approximately (0,1)','Passed'),
('CG-04','Rasterize (0,0) to (5,3)','Last pixel equals (5,3)','Passed'),
('CG-05','Circle radius 5','Eight-way symmetric points include (±5,0)','Passed'),
('CG-06','Clip segment through window [0,4]×[0,4]','Accepted segment endpoints on x=0 and x=4','Passed'),
('CG-07','Board/screen coordinate round trip','Inverse mapping returns original file/rank','Passed')])
p('The desktop chess interface requires the dependencies listed in requirements.txt. The chess UI was not executed in this build environment because python-chess was not installed in the runtime used for the algorithm test run. Install the dependencies and perform the end-to-end chess interaction checks on the target Windows machine before claiming final application validation.')
heading('7.1 Limitations',2)
bullet('Pawn promotion currently defaults to a queen rather than displaying a promotion-choice dialog.')
bullet('The current desktop board uses Unicode chess glyphs for compact rendering; the geometric piece silhouette definitions are supplied as modelling data and can be integrated into a custom vector renderer for a richer final version.')
bullet('Player-versus-computer search is not included in this initial build; the interactive chessboard supports human move input.')
bullet('Screenshots and final end-to-end test evidence must be captured after dependency installation on the presentation machine.')
page()

heading('CHAPTER 8 — CONCLUSION AND FUTURE WORK',1)
p('The project establishes an interactive environment for learning Computer Graphics through a chessboard application. It demonstrates polygon filling, homogeneous 2D transformations, object modelling concepts, coordinate conversion and additional rasterization and clipping algorithms. The manual algorithm module is independently testable and the seven included unit tests passed in the current local run.')
heading('8.1 Future Scope',2)
for x in ['Integrate custom vector piece silhouettes directly into the chessboard renderer.','Add a promotion chooser and richer draw-claim controls.','Add a computer opponent using Minimax with alpha-beta pruning as an optional game-logic extension.','Add editable polygon vertices and a step-by-step scanline animation control.','Add a 3D chessboard mode using a suitable 3D rendering approach if approved by the faculty.','Capture actual application screenshots and extend the test suite to cover all chess special moves and GUI interactions.']:
    bullet(x)
heading('8.2 Team Contribution Plan',2)
table(['Member','Proposed responsibility (confirm actual work before submission)'],[
('Shivam','Chessboard interface, board coordinate display and UI integration'),('Deepak','Scan-Line Polygon Filling, DDA and Bresenham algorithm modules'),('Sameer','Homogeneous transformations, coordinate mapping and object modelling'),('Abhay','Testing, chess interaction validation, screenshots, report and presentation integration')])
page()

heading('REFERENCES',1)
for x in ['Hearn, D., Baker, M. P., & Carithers, W. (2014). Computer Graphics with OpenGL (4th ed.). Pearson.','Foley, J. D., van Dam, A., Feiner, S. K., & Hughes, J. F. (1996). Computer Graphics: Principles and Practice (2nd ed.). Addison-Wesley.','Python Software Foundation. Python 3 Documentation. https://docs.python.org/3/','NumPy Developers. NumPy Documentation. https://numpy.org/doc/','Matplotlib Development Team. Matplotlib Documentation. https://matplotlib.org/stable/','python-chess Documentation. https://python-chess.readthedocs.io/','Cohen, D. (1985). A clipping algorithm for line segments and polygons. (Cohen–Sutherland line clipping method; consult standard Computer Graphics references for derivation).']:
    bullet(x)
p('Academic details to verify before submission: Computer Graphics faculty name, exact course code, semester, and academic year as required by the course coordinator.',italic=True)
d.save(OUT_DOC)

# ---------- PPTX: retain uploaded template and add slide content ----------
prs=Presentation('/mnt/data/PBL_presentation_template_v2.pptx')
NAVY=PRGB(31,57,105); BLUE=PRGB(79,140,255); WHITE=PRGB(245,248,252); MUTED=PRGB(180,194,214)

def set_shape_text(shape, text, size=22, color=WHITE, bold=False):
    tf=shape.text_frame; tf.clear(); tf.word_wrap=True
    for j,line in enumerate(text.split('\n')):
        para=tf.paragraphs[0] if j==0 else tf.add_paragraph(); para.text=line; para.font.name='Aptos'; para.font.size=PPt(size); para.font.bold=bold; para.font.color.rgb=color

def add_content(slide, title, bullets, subtitle=None):
    # Keep existing template title placeholder and add content in the open content area.
    title_shape=None
    for sh in slide.shapes:
        if getattr(sh,'has_text_frame',False) and sh.text.strip() and sh.top < PInches(1.5):
            title_shape=sh; break
    if title_shape:
        set_shape_text(title_shape,title,27,NAVY,True)
    top=PInches(1.55); left=PInches(.62); width=PInches(8.75); height=PInches(3.65)
    box=slide.shapes.add_textbox(left,top,width,height); tf=box.text_frame; tf.clear(); tf.word_wrap=True
    if subtitle:
        pa=tf.paragraphs[0]; pa.text=subtitle; pa.font.name='Aptos'; pa.font.size=PPt(16); pa.font.bold=True; pa.font.color.rgb=BLUE
    for item in bullets:
        pa=tf.add_paragraph(); pa.text='•  '+item; pa.level=0; pa.font.name='Aptos'; pa.font.size=PPt(16); pa.font.color.rgb=PRGB(42,54,73); pa.space_after=PPt(12)

# Slide 1 title page
s=prs.slides[0]
for sh in s.shapes:
    if getattr(sh,'has_text_frame',False):
        if '[Project Title]' in sh.text: set_shape_text(sh,'Interactive Chessboard\nGraphics System',30,WHITE,True)
        elif 'A one-line description' in sh.text: set_shape_text(sh,'An interactive chess visualization system demonstrating core Computer Graphics algorithms',17,WHITE)
        elif sh.text.strip()=='Lavanya (1/24/SET/BCS/559)\nAnuj Rawat (1/24/SET/BCS/536)\nSimran Singh (1/24/SET/BCS/537)\nMahi Tandon (1/24/SET/BCS/540)': set_shape_text(sh,'\n'.join(f'{n} ({r})' for n,r in TEAM),12,WHITE)
        elif 'Dr. Ali Abbas' in sh.text: set_shape_text(sh,'Faculty Name: To be confirmed\nDepartment of Computer Science and Engineering\nComputer Graphics\nAcademic Year 2026–2027 | Semester to be confirmed',12,WHITE)
# Slide 2 index update existing index page
s=prs.slides[1]
for sh in s.shapes:
    if getattr(sh,'has_text_frame',False) and sh.text.strip()=='Index': set_shape_text(sh,'Index',28,NAVY,True)
# Slides 3-12 content
content={
2:('Abstract',['Interactive 8×8 chessboard with legal-move highlighting and game status.','Manual Computer Graphics algorithms are separated from chess-rule handling.','Graphics Lab visualizes polygon filling, transformations, rasterization, clipping and coordinate mapping.'],'Project overview'),
3:('Introduction',['Chessboard geometry provides repeated square regions and discrete coordinates.','The project exposes graphics operations that are normally hidden inside a rendering library.','The goal is to connect theoretical Computer Graphics algorithms with a familiar interactive application.'],'Problem and motivation'),
4:('Objectives',['Implement Scan-Line Polygon Filling manually.','Apply translation, rotation, scaling, reflection and composite transformations.','Model chess-piece silhouettes from geometric primitives.','Convert chessboard coordinates to screen coordinates and back.','Show intermediate algorithm steps and validate with test cases.'],'Learning outcomes'),
5:('System Analysis',['Two layers: interactive chess gameplay and independent Graphics Algorithms Lab.','Tkinter provides desktop controls; Matplotlib renders the board and algorithm visualizations.','NumPy supports homogeneous transformation matrices.','python-chess validates chess rules only; graphics algorithms are implemented separately.'],'Architecture and modules'),
6:('CG Concepts & Algorithms',['Polygon Filling: Scan-Line intersections, sorting and even-odd spans.','Transformations: 3×3 homogeneous matrices; composite order T·R·F·S.','Object Modelling: polygons, circles, ellipses, lines and curves.','Coordinate Systems: board ↔ screen mapping.','Additional: DDA, Bresenham, Midpoint Circle and Cohen–Sutherland.'],'Core concepts'),
7:('Implementation',['Chessboard: select pieces, highlight legal destinations, view status and move history.','Transformation Playground: original and transformed polygons with matrix display.','Algorithms Lab: choose an algorithm and visualize calculated pixels or clipped segments.','Source modules separate UI, chess state, CG algorithms and piece model data.'],'Implementation workflow'),
8:('Output & Demonstration',['Live chessboard and legal move highlights.','Scan-Line polygon fill with scanline traces.','Original and transformed polygon with composite matrix.','DDA/Bresenham pixels, midpoint circle points and clipped line segment.','Capture actual screenshots after installing the requirements.'],'Demonstration evidence'),
9:('Results & Discussion',['Seven unit tests for the manual graphics algorithms passed in the current local test run.','Tests cover polygon filling, translation, rotation, line rasterization, circle symmetry, clipping and coordinate round trip.','The chess GUI still requires end-to-end execution after installing python-chess on the target machine.'],'Validation status'),
10:('Conclusion & Future Work',['The application connects an interactive chessboard with independent graphics algorithm demonstrations.','Future work: vector piece rendering, editable polygon input, step animation, promotion chooser and optional AI opponent.','Confirm faculty/course details and capture real GUI screenshots before submission.'],'Summary'),
11:('References',['Hearn, Baker & Carithers — Computer Graphics with OpenGL.','Foley et al. — Computer Graphics: Principles and Practice.','Python Documentation — docs.python.org/3/','NumPy Documentation — numpy.org/doc/','Matplotlib Documentation — matplotlib.org/stable/','python-chess Documentation — python-chess.readthedocs.io/'],'Technical sources')}
for idx,(title,bullets,sub) in content.items(): add_content(prs.slides[idx],title,bullets,sub)
# Replace inherited DAA footer with the correct subject label on every slide.
for slide in prs.slides:
    for sh in slide.shapes:
        if getattr(sh,'has_text_frame',False) and 'Design & Analysis of Algorithm (5.0CE100COIH)' in sh.text:
            sh.text_frame.text = sh.text.replace('Design & Analysis of Algorithm (5.0CE100COIH)','Computer Graphics')
# add slide note in last slide title if possible
prs.save(OUT_PPT)
print(OUT_DOC); print(OUT_PPT)
