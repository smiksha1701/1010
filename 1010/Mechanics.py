import tkinter as tk
import random
import os
import Temporary as T
class MenuWin():
    """Creates menu with all needed widgets"""
    def __init__(self,parent):
        self.parent=parent
        self.parent.protocol("WM_DELETE_WINDOW",self.Nothing)
        self.Clear()
        self.flag=T.flag
        self.parent.geometry('300x300')
        self.size=tk.StringVar(parent)
        self.size.set(T.StringCurSetting)
        self.choises=tk.StringVar(parent)
        self.choises.set(T.StringChoiseSetting)
        Explanation1=tk.Label(parent,bg="white",fg="black",text="Size of Table",font=('Arial',14))
        SizeOption=tk.OptionMenu(parent,self.size,"5 5", *T.LOSS)
        SizeOption.config(width=10,height=1,font=('Arial',14))
        Explanation2=tk.Label(parent,bg="white",fg="black",text="How many figures you get",font=('Arial',14))
        ChoiseOption=tk.OptionMenu(parent,self.choises,"2", *T.LOCS)
        ChoiseOption.config(width=10,height=1,font=('Arial',14))
        StartB=tk.Button(parent,width=20,height=2,fg="black",bg="white",state=tk.ACTIVE,font=('Arial',14,"bold"),text="START NEW GAME",command=self.Start)
        Continue=tk.Button(parent,width=20,height=2,fg="black",bg="white",state=tk.ACTIVE,text="CONTINUE",command=self.Continue)
        Quit=tk.Button(parent,width=20,height=2,fg="black",bg="white",state=tk.ACTIVE,text="QUIT",command=self.parent.destroy)
        Explanation1.pack()
        SizeOption.pack()
        Explanation2.pack()
        ChoiseOption.pack()
        StartB.pack()
        Continue.pack()
        Quit.pack()
    def Continue(self):#continues game if any running already
        if T.flag:
            self.ContinuePrevious()
        else:
            pass
    def Start(self):#starts new game if any running already
        if T.flag:
            self.QuestionMark()
        else:
            self.CreateNewGameWin()
    def ContinuePrevious(self):#continues previous game
        self.Clear()
        GamingWin(self.parent)
    def CreateNewGameWin(self):#creates NEW gaming win (changes all essential temporaries)
        self.Clear()
        T.curFigures=[]
        T.CurSetting=int((self.size.get()).split()[0])
        T.StringCurSetting=self.size.get()
        T.StringChoiseSetting=self.choises.get()
        T.ChoiseSetting=int(self.choises.get())
        T.ChoiseLeft=T.ChoiseSetting
        T.Build_Figures(T.CurSetting)
        T.resolution=T.windowsize(T.ChoiseSetting,T.CurSetting)
        T.TableCenter=T.Centrate(T.CurSetting,T.resolution)
        T.newtable.Build_New_Table(T.CurSetting,T.TableCenter)
        T.newChoise=1
        GamingWin(self.parent)
        T.flag=1
    def Nothing(self):#to do nothing if "x" button pressed
            pass
    def QuestionMark(self):#creates question win about risk of starting new game
        def Back():#returning to menu and activates it 
            Question.destroy()
            self.Activate()
        def Startnew():#starts new game
            T.flag=0
            self.CreateNewGameWin()
            Question.destroy()
        Question=tk.Tk()
        self.Disable()
        Question.geometry("300x200")
        Question.focus_force()
        Text=tk.Label(Question,font=('Arial',14),text="YOU HAVE EXISTING\n START NEW?")
        ButtonYEAH=tk.Button(Question,width=10,height=2,text="Hell YEAHHH")
        ButtonNOPE=tk.Button(Question,width=10,height=2,text="No")
        Question.protocol("WM_DELETE_WINDOW",self.Nothing)
        Text.place(x=50,y=10)
        ButtonYEAH.config(command=Startnew)
        ButtonNOPE.config(command=Back)
        ButtonYEAH.place(x=20,y=54)
        ButtonNOPE.place(x=180,y=54)
    def Clear(self):
        #Cleares all widgets
        for widget in self.parent.winfo_children():
            widget.destroy()
    def Activate(self):
        #Activates all widgets
        for widget in self.parent.winfo_children():
            widget.config(state=tk.ACTIVE)
    def Disable(self):
        #disables all widgets
        for widget in self.parent.winfo_children():
            widget.config(state=tk.DISABLED)
class GamingWin():
    """changing start window to gaming window and filling it """
    def __init__(self,parent):
        self.parent=parent
        resolution=T.resolution
        self.parent.geometry("{}x{}".format(*resolution))
        Settings=tk.Button(self.parent,width=10,height=2,fg="black",bg="white",text="Back to Settings",command=self.Build_BackToMenu)
        Settings.place(x=resolution[0]/2,y=20,anchor=tk.CENTER) 
        GamingTable(self.parent)
        ChoiceTable(self.parent)
        parent.protocol("WM_DELETE_WINDOW",self.Nothing)
    def Nothing(self):#to do nothing if "x" button pressed
        pass
    def Build_BackToMenu(self):
        #returns to menu
        MenuWin(self.parent)
class ChoiceTable():
    """Build Choise Table with choise Tiles on it"""
    def __init__(self,parent):
        self.parent=parent
        for counter in range(T.ChoiseLeft):
            x=10+counter*150
            y=70*T.CurSetting
            Figure=ChoiceTile(parent,counter)
            Figure.place(x=x,y=y)
        T.newChoise=0
class ChoiceTile(tk.Button):
    """Build Choise Tile gets figure in temporary"""
    def __init__(self,parent,counter):
        self.parent=parent
        if T.newChoise:#checks if new figures are needed
            self.figure=random.choice(T.AllFigures)
            T.curFigures.append(self.figure)
        else:
            self.figure=T.curFigures[counter]
        self.image=tk.PhotoImage(file=os.path.abspath(self.figure.Image))
        self.height,self.width=self.figure.Size
        tk.Button.__init__(self,parent,borderwidth=0,bg="white",image=self.image,height=self.height*50,width=self.width*50)
        self.bind('<ButtonPress-1>',self.Press)
        self.bind('<ButtonRelease-1>',self.Drop)
        self.bind('<B1-Motion>',self.Pick)
    def Press(self,event):
        self.startingxcorner=self.winfo_rootx()-self.parent.winfo_rootx()#x coord of button corner
        self.startingycorner=self.winfo_rooty()-self.parent.winfo_rooty()#y coord of button corner
        self.apx=self.parent.winfo_pointerx()-self.parent.winfo_rootx()#x coord where clicked(relatively window)
        self.apy=self.parent.winfo_pointery()-self.parent.winfo_rooty()#y coord where clicked(relatively window)
        self.deltax=self.apx-self.startingxcorner#x coord where clicked(relatively button)
        self.deltay=self.apy-self.startingycorner#y coord where clicked(relatively button)
        self.lift()#lifts button on the top
    def Mouse(self):
        self.apx=self.parent.winfo_pointerx()-self.parent.winfo_rootx()
        self.apy=self.parent.winfo_pointery()-self.parent.winfo_rooty()
    def Pick(self,event):
        self.Mouse()
        self.x=self.apx-self.deltax
        self.y=self.apy-self.deltay
        self.place_configure(x=self.x,y=self.y)
        self["state"]=tk.DISABLED
    def Drop(self,event):
        fits=T.newtable.AddFigure(self.figure,self.x,self.y)#returns if figure fits 
        if fits:
            T.newtable.Color()#colors Table
            T.newtable.Full()#checks fullness of Gaming Table
            T.curFigures.remove(self.figure)#delets figure out of available
            T.ChoiseLeft-=1#decreases counter of available choise
            if (T.ChoiseLeft==0):#if out of figures
                T.newChoise=1
                T.ChoiseLeft=T.ChoiseSetting#refills it
                ChoiceTable(self.parent)#refills Choise Table
            GamingTable(self.parent)#updates GamingTable
            self.destroy()
        else:
            self.place_configure(x=self.startingxcorner,y=self.startingycorner)#places it back
class GamingTable():
    """Class which creates Gaming Table 
    and checks if Game is Over in this case
    informs player and asks about start new game"""
    def __init__(self,parent):
        self.parent=parent
        for row in range(T.CurSetting):
            for col in range(T.CurSetting):
                BoardTile(parent,row,col)
        if T.curFigures:#checks if there is any figures
            self.flag=0
            for i in T.curFigures:#check if any of figures fits any position
                self.flag+=T.newtable.CheckEndGame(i)
            if self.flag==0:
                self.TheEnd()
    def TheEnd(self):
        """Game Over asks about new game"""
        def Nothing():#to do nothing if "x" button pressed
            pass
        self.parent
        self.Disable()
        self.GameOver=tk.Tk()
        self.GameOver.config(bg="black")
        self.GameOver.geometry("300x200")
        GO=tk.Label(self.GameOver,font=('Arial',19),bg="black",fg="red",text="GAME OVER")
        BTS=tk.Button(self.GameOver,font=('Arial',14),bg="black",fg="white",text="START NEW")
        BTS.bind("<Button-1>",self.StartNew)
        self.GameOver.protocol("WM_DELETE_WINDOW",Nothing)
        GO.pack()
        BTS.pack()
        self.GameOver.focus_force()
    def StartNew(self,event):#Returns to menu
        self.GameOver.destroy()
        T.flag=0
        MenuWin(self.parent)
    def Disable(self):
         #disables all widgets
        for widget in self.parent.winfo_children():
            widget.config(state=tk.DISABLED)
class BoardTile(tk.Button):
    """Class which creates Tile of Gaming Table
    takes color of tile in temporaries"""
    def __init__(self,parent,row,col):
        self.Table=T.newtable
        color=self.Table.Update(row,col)
        tk.Button.__init__(self,parent,bg=color,state=tk.DISABLED)
        self.place(y=55+row*50,x=T.TableCenter+col*50,height=50,width=50)