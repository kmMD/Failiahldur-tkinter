#Probleemid:
#1. Skrollimine, kaustad ja kausta leidmine.
#2. Nupp saada
#3. Saadud failide aken
#4. Teatised
#5. Kaustad
#6. Rekursiooniga kausta leidmine
#7. Faili nime muutmine
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
from os.path import isdir


valitud_failid1=[]
    
def impordi_faile():   #impordib failid sisestatud kausta nimest
    def info():
        global kausta_nimi
        global path
        kausta_nimi=nimi.get()
        raam2.destroy()

        failid = []
        path = os.getcwd() + "\\"+str(kausta_nimi)

        for fail in os.listdir(path):
            failid.append(fail)


        tekst = ""
        i = 1
        for fail in failid[0:]:
            tekst = fail + "\n"
            rada=path+"\\"+fail
            if not isdir(rada):
                tahvel1.create_text(5,5+15*(i-1),text=tekst,anchor=NW,fill='black', activefill='grey')
                i += 1
        

    raam2=Tk()
    raam2.title('Kaust')
    raam2.geometry('200x100')
    
    nimi=ttk.Entry(raam2)
    nimi.place(x=20,y=30, width=100)
    silt=ttk.Label(raam2,text='Sisesta kausta nimi:')
    silt.place(x=20,y=10)
    nupp5=ttk.Button(raam2, text='Sisesta',command=info)
    nupp5.place(x=20,y=60)
    raam2.mainloop()

def vali(event):                    #vasakul tahvlis peale klõpsates vasaku hiire klahviga lisab faili järjendisse valitud_failid1, teist korda klikates eemaldab järjendist
    global valitud_failid1          #lisaks muudab värvi
    tahvel1.addtag_closest('valik',event.x,event.y)
    valik=tahvel1.itemcget('valik','text')
    valik=valik.strip('\n')
    if valik !=None:
        if valik not in valitud_failid1:
            tahvel1.itemconfigure('valik',fill='grey')
        else:
            tahvel1.itemconfigure('valik',fill='black')
    tahvel1.dtag('valik','valik')
    if valik !=None:
        if valik not in valitud_failid1:
            valitud_failid1+=[valik]
        else:
            valitud_failid1.remove(valik)

def ava(event):                                      #muudab käsurea käsu korrektseks ja avab valitud faili 
    tahvel1.addtag_closest('ava',event.x,event.y)
    faili_nimi=tahvel1.itemcget('ava','text')
    faili_nimi=faili_nimi.strip('\n')
    käsk=path+"\\"+faili_nimi
    käsk=käsk.split('\\')
    õige_käsk='C:'
    for i in range(1,len(käsk)):
        õige_käsk+=('\\'+'\"'+käsk[i]+'\"')
    os.system(õige_käsk)
    
    

    



raam=Tk()
raam.title('Projekt')
raam.geometry('1000x700')

silt=ttk.Label(raam, text='Imporditud failid:')
silt.place(x=20,y=10)

silt=ttk.Label(raam, text='Kätte saadud failid:')
silt.place(x=520,y=10)

tahvel1=Canvas(raam, width=350, height=640, background='white',yscrollincrement=0, yscrollcommand=10000)
tahvel1.grid()
tahvel1.place(x=20, y=30)
scrollbar1=Scrollbar(raam,orient=VERTICAL)
scrollbar1.place(x=370, y=30)
#scrollbar1.set(0,10000)

tahvel2=Canvas(raam, width=350, height=640, background='white')
tahvel2.grid()
tahvel2.place(x=520, y=30)

nupp1=ttk.Button(raam ,text='Impordi faile', command=impordi_faile)
nupp1.place(x=400, y=30)

tahvel1.bind('<3>',vali)
tahvel1.bind('<Double-Button-1>',ava)






raam.mainloop()


