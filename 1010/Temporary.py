import random
resolution=0#saving resolution
TableCenter=0#center of table 
newChoise=1#flag of refilling choise table
LOSS=[]#list of size settings
for l in range (6,10):#fills LOSS
    LOSS.append("{} {}".format(l,l))
LOCS=[]#list of choise settings
for l in range (3,9):#fills LOCS
    LOCS.append("{}".format(l))
flag=0#flag of existing game if exist:->1 else:->0 
StringCurSetting="5 5"#chosen Size setting(string to represent in OptionMenu)
CurSetting=5#chosen Size setting(int)
StringChoiseSetting="5"#chosen Choises setting(string to represent in OptionMenu)
ChoiseSetting=5#chosen Choise setting(int)
ChoiseLeft=5#Choise available
curFigures=[]#list of current figures available
AllFigures=[]#list of all figures
FigureColor=[
    "magenta",
    "yellow",
    "blue",
    "green",
    "orange",
    "grey",
    "#04f7b4",
    "#ff0000",
    "#b600ff",
    "#849400",
    "#00f7ff",
    "#f5ceb2",
    "#482d16",
    "black",
    "#b3584d",
    "#00414d",
    "#5fa091"
]#list of figures color
def windowsize(Choise,table):#Counts resolution according current settings
    a=max(Choise,table)
    result=2*[a*150]
    return result 
def Centrate(Table,resolution):#Counts center of window according current settings
    a=resolution[0]/2-Table*25
    return a 
FiguresImage=["Images/{}.png".format(i) for i in range(17)]#list of figures images
Structure=[
        [[1,1]],
        [[1,1],[1,1]],
        [[1,1],[1,0],[1,0]],
        [[1],[1],[1],[1]],
        [[1,1],[1,0]],
        [[1]],
        [[1,1],[0,1]],
        [[1,0],[1,1]],
        [[0,1],[1,1]],
        [[1,1],[0,1],[0,1]],
        [[1,0],[1,0],[1,1]],
        [[0,1],[0,1],[1,1]],
        [[1,1,1],[0,0,1]],
        [[1,0,0],[1,1,1]],
        [[1,1,1],[1,0,0]],
        [[0,0,1],[1,1,1]],
        [[1],[1]]
]#list of figures structure(where 0 is "empty" tile and 1 is filled one)
FigureSize=[
    (1,2),
    (2,2),
    (3,2),
    (4,1),
    (2,2),
    (1,1),
    (2,2),
    (2,2),
    (2,2),
    (3,2),
    (3,2),
    (3,2),
    (2,3),
    (2,3),
    (2,3),
    (2,3),
    (2,1)
]#list of figures size 
class Figure():
    """Creates figure with its characteristics"""
    def __init__(self,Color,Ident,Structure,Image,Size,Allowence):
        self.Ident=Ident
        self.Structure=Structure
        self.Image=Image
        self.Size=Size
        self.Allowedx,self.Allowedy=Allowence[0],Allowence[1]
        self.color=Color
def Build_Figures(CurSetting):
    """Counts Allowence and creates all figures(and adding it to AllFigures"""
    Allowence=[
        [
            [i for i in range(CurSetting)],[i for i in range(CurSetting-1)]
        ],
        [
            [i for i in range(CurSetting-1)],[i for i in range(CurSetting-1)]
        ],
        [
            [i for i in range(CurSetting-2)],[i for i in range(CurSetting-1)]
        ],
        [
            [i for i in range(CurSetting-3)],[i for i in range(CurSetting)]
        ],
        [
            [i for i in range(CurSetting-1)],[i for i in range(CurSetting-1)]
        ],
        [
            [i for i in range(CurSetting)],[i for i in range(CurSetting)]
        ],
        [
            [i for i in range(CurSetting-1)],[i for i in range(CurSetting-1)]
        ],
        [
            [i for i in range(CurSetting-1)],[i for i in range(CurSetting-1)]
        ],
        [
            [i for i in range(CurSetting-1)],[i for i in range(CurSetting-1)]
        ],
        [
            [i for i in range(CurSetting-2)],[i for i in range(CurSetting-1)]
        ],
        [
            [i for i in range(CurSetting-2)],[i for i in range(CurSetting-1)]
        ],
        [
            [i for i in range(CurSetting-2)],[i for i in range(CurSetting-1)]
        ],
        [
            [i for i in range(CurSetting-1)],[i for i in range(CurSetting-2)]
        ],
        [
            [i for i in range(CurSetting-1)],[i for i in range(CurSetting-2)]
        ],
        [
            [i for i in range(CurSetting-1)],[i for i in range(CurSetting-2)]
        ],
        [
            [i for i in range(CurSetting-1)],[i for i in range(CurSetting-2)]
        ],
        [
            [i for i in range(CurSetting-1)],[i for i in range(CurSetting)]
        ]
    ]#list of figures allowed placements
    for i in range(17):
        NewFigure=Figure(FigureColor[i],i,Structure[i],FiguresImage[i],FigureSize[i],Allowence[i])
        AllFigures.append(NewFigure)
class Table():
    """
    Creates all needed to check if figure fits placement, put figures, 
    coloring placement, check fullness of row or col and check end of game
    """
    def __init__(self):
        pass
    def Build_New_Table(self,CurSetting,resolution):
        """
        Creates Canvas and CoordsTable
        Canvas stores colors of every tile 
        CoordsTalbe stores coordinates of coorners of every tile
        """
        self.CurSetting=CurSetting
        self.TileCoords=[]
        self.Canvas=[]
        for i in range (CurSetting):
            self.TileCoords.append([])
            self.Canvas.append([])
            for j in range(CurSetting):
                self.Canvas[i].append("white")
                self.TileCoords[i].append((resolution+j*50,55+i*50))
    def AddFigure(self,Figure,x,y):
        """
            Approximates row and col of closest tile 
            to figures coorner, if figure is not close 
            enough to any or figure can`t be placed there(Borders conflict)
            returns false
            else returns true
        """
        self.NewFigure=Figure
        self.coords=(x,y)
        mini=36
        for row, i in enumerate(self.TileCoords):
            for col, j in enumerate(i):
                cur=pow((pow(self.coords[0]-j[0],2)+pow(self.coords[1]-j[1],2)),0.5)
                if cur<mini:
                    mini=cur
                    self.closestx,self.closesty=(row,col)
        if mini!=36:
            if (self.closestx in self.NewFigure.Allowedx) and(self.closesty in self.NewFigure.Allowedy) :
                flag=self.Check(self.closestx,self.closesty)
                return flag
            else:
                return False
        else: 
            return False
    def Color(self):
        """Colors placement of figure"""
        for i in self.save:
            self.Canvas[self.closestx+i[0]][self.closesty+i[1]]=self.NewFigure.color
    def Check(self,row,col):
        """
        Checks if figure fits placemnt
        if fits colors it
        returns if figure can be placed
        """
        self.size=self.NewFigure.Size
        self.save=[]
        flag=True
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.NewFigure.Structure[i][j]==0 or flag==False:
                    pass
                else:
                    if self.Canvas[row+i][col+j]=="white":
                        self.save.append((i,j))
                        flag=True
                    else:
                        flag=False
        return flag
    def Update(self,row,col):
        """
        returns color of Tile(for BoardTile color)
        """
        color=self.Canvas[row][col]
        return color
    def Full(self):
        """
        Checks if row or col is full 
        if full calls self.Clear
        """
        counterx,countery=0,0
        for i in range (self.CurSetting):
            if counterx==self.CurSetting:
                self.Clear(0,i-1)
            if countery==self.CurSetting:
                self.Clear(1,i-1)
            counterx,countery=0,0
            for j in range(self.CurSetting):
                if self.Canvas[i][j]!="white":
                    counterx+=1
                if self.Canvas[j][i]!="white":
                    countery+=1
        if counterx==self.CurSetting:
            self.Clear(0,self.CurSetting-1)
        if countery==self.CurSetting:
            self.Clear(1,self.CurSetting-1)
    def Clear(self,ort,line):
        """
        Clears row or col
        """
        if ort==0:
            for j in range (self.CurSetting):
                self.Canvas[line][j]="white"
        else:
            for j in range (self.CurSetting):
                self.Canvas[j][line]="white"
    def CheckEndGame(self,figure):
        """
        Checks if figure can fit any of places on the board
        returns sum of all available placements
        """
        flag=1
        for row in figure.Allowedx:
            for col in figure.Allowedy:
                if(flag<2):
                    flag=1
                    for i in range(figure.Size[0]):
                        for j in range(figure.Size[1]):
                            if figure.Structure[i][j]==0 or flag==0:
                                pass
                            else:
                                if self.Canvas[row+i][col+j]=="white":
                                    flag+=1
                                else:
                                    flag=0
                else:
                    pass
        return flag
newtable=Table()
