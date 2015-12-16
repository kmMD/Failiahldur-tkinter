from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
from os.path import isdir
import socket
import sys


valitud_failid1=[]
    
def impordi_faile():   #impordib failid sisestatud kausta nimest
    def info():                  #antud funktsioon kirjeldab kuidas trükitakse failide nimed esimesele teksti väljundi alale
        global kausta_nimi
        global path
        kausta_nimi=nimi.get()  #kausta nimi saadkase aknast kuhu kasutaja selle ise sisaldab
        raam2.destroy()         #sisestuse aken suletakse

        failid = []            #loodakse uus tühi järjend
        path = os.getcwd() + "/"+str(kausta_nimi)  #salvestame kausta aadressi(raja)

        for fail in os.listdir(path):   #võttes järjest faile antud kaustast lisatakse need järjendisse failid
            failid.append(fail)


        i = 1
        for fail in failid[0:]:  #iga fail järjendist failid 
            tekst = fail + "\n"  #puhul salvestatakse nii tema rada kui ka faili nimi
            rada=path+"\\"+fail
            if not isdir(rada): #kui tegemist on kaustaga siis teda ei kuvata kui mitte siis
                tahvel1.create_text(5,5+15*(i-1),text=tekst,anchor=NW,fill='black', activefill='grey') #trüiktakse antud faili nimi teksti väljundi alale
                i += 1
        

    raam2=Tk()   #loome sisestamise akna, nimeks Kaust
    raam2.title('Kaust')
    raam2.geometry('200x100')
    
    nimi=ttk.Entry(raam2)   #loome sisestuse ala
    nimi.place(x=20,y=30, width=100)
    silt=ttk.Label(raam2,text='Sisesta kausta nimi:')
    silt.place(x=20,y=10)
    nupp5=ttk.Button(raam2, text='Sisesta',command=info) #lisame nupu, mis käivitab funktsiooni info
    nupp5.place(x=20,y=60)
    raam2.mainloop()

def vali(event):                    #vasakul tahvlis peale klõpsates vasaku hiire klahviga lisab faili järjendisse valitud_failid1, teist korda klikates eemaldab järjendist
    global valitud_failid1          #lisaks muudab värvi
    tahvel1.addtag_closest('valik',event.x,event.y) #lisame hiire klõpsule lähimale failile sildi 'valik'
    valik=tahvel1.itemcget('valik','text')  #toome välja valiku teksti osa
    valik=valik.strip('\n')          
    if valik !=None:        #kui valik ei ole tühi ja fail ei ole juba järednis valitud_failid siis muudame tema värvi halliks 
        if valik not in valitud_failid1:
            tahvel1.itemconfigure('valik',fill='grey')
        else:                                           #vastasel juhul muudame valitud faili värvi tagasi mustaks
            tahvel1.itemconfigure('valik',fill='black')
    tahvel1.dtag('valik','valik')       #kustutame antud sildi
    if valik !=None:                       #kui vailk ei ole tühi ja ei ole järjendis valitud_failid1 diid lisame ta sinna, kui ta seal juba on siis eemaldame ta
        if valik not in valitud_failid1:
            valitud_failid1+=[valik]
        else:
            valitud_failid1.remove(valik)

def ava(event):                                      #muudab käsurea käsu korrektseks ja avab valitud faili 
    tahvel1.addtag_closest('ava',event.x,event.y)   #lisame hiire klõpsuel lähimale failie silid 'ava'
    faili_nimi=tahvel1.itemcget('ava','text')       #saame antud sildile vastava valiku teksti osa
    faili_nimi=faili_nimi.strip('\n')
    käsk=path+"\\"+faili_nimi                    #loome käsu mille sisestame pärast vastavaid korrektuure käsureale
    käsk=käsk.split('\\')
    õige_käsk='C:'
    for i in range(1,len(käsk)):
        õige_käsk+=('\\'+'\"'+käsk[i]+'\"')
    os.system(õige_käsk)

def saada():                                #funktsioon, mis tegelb failide saatmisega
    s = socket.socket()             
    host = socket.gethostname()
    port = 10110
    s.bind((host, port))
    pakk1=''                                #saadetav pakk on alguses tühi                                
    for i in range(len(valitud_failid1)):   #lisame pakki iga faili nime ja tema sisu, eraldatud kahe #
        nimi=valitud_failid1[i]
        fail=open(path+'\\'+nimi)
        pakk=fail.read()
        pakk1+=nimi+'##'+pakk
        if i<len(valitud_failid1)-1:
            pakk1+='&&'                     #failid eraldame omavahel &&
    s.listen(1)                             #pakk kajastatakse
    while True:                             #kui ühendus käes saadetakse pakk teele
        c, addr = s.accept()
        c.send(pakk1.encode())
        c.close()
        break


def recive():                                                   #funktsioon, mis tegeleb failide saamisega seotud tkinter toiminkutega
    def kuula():                                                #funktsioon, mis tegeleb failide saamisega
        IP=nimi2.get()                                          #saatja IP aadressi saame sisestatud IP aadressist
        raam3.destroy()
        s = socket.socket()
        host = IP
        port = 10110


        s.connect((host, port))                                 #ühendame ennast saajaga ja dekodeerime paki sisu
        sisu=(s.recv(1024).decode())
        jupid=sisu.split('&&')                                  #vastavaid poolitusi kasutades kirjutame kausta Saadetised kõik saadetud failid
        for jupp in jupid:
            osad=jupp.split('##')
            save_path=os.getcwd()+"/Saadetised"
            complete_name=os.path.join(save_path,osad[0])
            uus_fail=open(complete_name,'w')
            uus_fail.write(osad[1])
            uus_fail.close()
        s.close()

        path = os.getcwd() + "/"+'Saadetised'  #salvestame saadetiste aadressi(raja)
        failid=[]

        for fail in os.listdir(path):   #võttes järjest faile antud kaustast lisatakse need järjendisse failid
            failid.append(fail)


        i = 1
        for fail in failid[0:]:  #iga fail järjendist failid 
            tekst = fail + "\n"  #puhul salvestatakse nii tema rada kui ka faili nimi
            rada=path+"\\"+fail
            if not isdir(rada): #kui tegemist on kaustaga siis teda ei kuvata kui mitte siis
                tahvel2.create_text(5,5+15*(i-1),text=tekst,anchor=NW,fill='black', activefill='grey') #trükitakse antud faili nimi teksti väljundi alale
                i += 1

    raam3=Tk()   #loome sisestamise akna, nimeks IP aadress
    raam3.title('IP aadress')
    raam3.geometry('200x100')
    
    nimi2=ttk.Entry(raam3)   #loome sisestuse ala
    nimi2.place(x=20,y=30, width=100)
    silt=ttk.Label(raam3,text='Sisesta IP-aadress:')
    silt.place(x=20,y=10)
    nupp5=ttk.Button(raam3, text='Sisesta',command=kuula) #lisame nupu, mis käivitab funktsiooni kuula
    nupp5.place(x=20,y=60)
    raam3.mainloop()
        

def ava2(event):                                      #muudab käsurea käsu korrektseks ja avab valitud faili 
    tahvel2.addtag_closest('ava2',event.x,event.y)   #lisame hiire klõpsuel lähimale failie silid 'ava2'
    faili_nimi=tahvel2.itemcget('ava2','text')       #saame antud sildile vastava valiku teksti osa
    faili_nimi=faili_nimi.strip('\n')
    path2=os.getcwd()+'\\'+'Saadetised'
    käsk=path2+"\\"+faili_nimi                    #loome käsu mille sisestame pärast vastavaid korrektuure käsureale
    käsk=käsk.split('\\')
    õige_käsk='C:'
    for i in range(1,len(käsk)):
        õige_käsk+=('\\'+'\"'+käsk[i]+'\"')
    os.system(õige_käsk)

def ip():                                                       #funktsioon, mis tagastab arvuti IP aadressi ja kuvab selle kasutajaliidesele
    ip=socket.gethostbyname(socket.gethostname())

    silt=ttk.Label(raam, text=('Minu IP aadress: '+ip))
    silt.place(x=350,y=10)
    
    

    
    
    

    



raam=Tk()                            #loome suure akna nimega Projekt
raam.title('Projekt')
raam.geometry('1000x700')

silt=ttk.Label(raam, text='Imporditud failid:')  #lisame kaks silti Importitud failid ja kätte saadud failid
silt.place(x=20,y=10)

silt=ttk.Label(raam, text='Kätte saadud failid:')
silt.place(x=520,y=10)

tahvel1=Canvas(raam, width=350, height=640, background='white',yscrollincrement=0, yscrollcommand=10000) #lisame esimese tekstiväljundi ala
tahvel1.grid()
tahvel1.place(x=20, y=30)

tahvel2=Canvas(raam, width=350, height=640, background='white') #loome teise teksti väljundi ala
tahvel2.grid()
tahvel2.place(x=520, y=30)

nupp1=ttk.Button(raam ,text='Impordi faile', command=impordi_faile) #lisame nupu Impordi faile, mis seostub funktsiooniga impordi_faile
nupp1.place(x=400, y=30)

tahvel1.bind('<3>',vali) #seome hiire vasaku topelt klõpsu ja parema klõpsu vastava teksti väljundi alaga ja ka funktsiooniga
tahvel1.bind('<Double-Button-1>',ava)

nupp2=ttk.Button(raam, text='Saada', command=saada)
nupp2.place(x=400, y=60)

nupp3=ttk.Button(raam, text='Kuula',command=recive)
nupp3.place(x=900, y=30)

tahvel2.bind('<Double-Button-1>',ava2)

nupp4=ttk.Button(raam, text='Minu IP', command=ip)
nupp4.place(x=400, y=90)








raam.mainloop()


