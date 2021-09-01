from tkinter.filedialog import *
from tkinter import *
from random import randint
from tkinter.messagebox import * #Gestion des boites de dialogue
import threading
import sys
import encodings
import base64
version= "0.4 Beta"
liste=[]
cles=[]
nbdelignes=0
mode="basic"
#------Partie graphique -------


root2=Tk()
root2.title('Dumb encryption, 2015')
fen=Canvas(root2,width="400",height="140")

photo = PhotoImage(file= "cadena.gif")
fen.create_image(200,50,image=photo)
fen.pack()

#---------------------------

##def comptelignes():
##    global nbdelignes,nbdelignestot
##    fichier=open(file,'r',encoding="utf8")
##    for nb in fichier.readlines():
##        nbdelignes+=1
##    nbdelignestot=nbdelignes
##    return nbdelignes

def op():
    global file2,liste,nbdelignes,file
    try:
        dec.delete(0, END)
        file = askopenfilename(title="Cryptage")
        if mode=="unicode":
            fichier=open(file,'r',encoding="utf8")
        else:
            fichier=open(file,'r',encoding="utf8")
        file2 = asksaveasfilename(title="Enregistrer sous",filetypes=[('fichier','.txt')])
        #nbdelignes=comptelignes()
        for line in fichier.readlines():
            #threading.Thread(target=crypte,args=(line,)).start()
            crypte(line)
        fichier.close()
        
    except FileNotFoundError:
        dec.delete(0, END)
        dec.insert(0, "Opération annulée par l'utilisateur.")
    except:
        dec.delete(0, END)
        dec.insert(0, "Opération annulée : erreur "+str(sys.exc_info()[0])+" : "+ str(sys.exc_info()[1]))

##def op():
##    global file2,liste,nbdelignes,file
##    try:
##        dec.delete(0, END)
##        file = askopenfilename(title="Cryptage")
##        fichier=open(file,'r',encoding="ISO-Latin1")
##        file2 = asksaveasfilename(title="Enregistrer sous",filetypes=[('fichier','.txt')])
##        #nbdelignes=comptelignes()
##        for line in fichier.readlines():
##            #threading.Thread(target=crypte,args=(line,)).start()
##            crypte(line)
##        fichier.close()
##        root2.after(1000,avancement)
##
##    except FileNotFoundError:
##        dec.delete(0, END)
##        dec.insert(0, "Opération annulée par l'utilisateur.")
##    except:
##        dec.delete(0, END)
##        dec.insert(0, "Opération annulée : erreur "+str(sys.exc_info()[0]))

def avancement():
    dec.delete(0, END)
    dec.insert(0, "100% Terminé !")

def keygen(l):
    global cles
    cles=[]
    l2=list(l)
    for i in range(len(l2)):
        cle1=randint(1,3) #clé pour multiplier
        cle2=randint(0,99)  #clé pour additionner
        cles.append((cle1,cle2))
    return cles

def encrypte(l,keys):  #Crypter grâce à une clé
    l2=list(l)
    for i in range(len(l2)):
        cle1=keys[i][0]
        cle2= keys[i][1]
        l2[i]=ord(l2[i])
        l2[i]*=cle1
        l2[i]+=cle2
        if mode=="unicode":
            l2[i]=chr(l2[i])
    return l2

def crypte(l):
    global res,cles,dec,file2
    cles=keygen(l)
    res=encrypte(l,cles)
    if mode=="unicode":
        fichier=open(file2,'a',encoding="utf8") #~fichier de sortie
    else:
        fichier=open(file2,'a',encoding="utf8") #~fichier de sortie
    for x in res:
        if mode=="unicode":
            fichier.writelines(str(x))
        else:
            fichier.writelines(str(x)+" ")
    fichier.writelines("\n")
    fichier.close()
    fichier=open(str(file2)+"Key.ini",'a',encoding="utf8")
    for k in cles:
        fichier.writelines(str(k)+";")
    fichier.writelines("\n")
    fichier.close()
    root2.after(1000,avancement)
    


def decrypte(l,keys):
    global sv
    filesave=open(sv,'a',encoding="utf8")
    l2=l
    if type(l2[0]) is int:
        
        for i in range(len(l2)):
            cle1=keys[i][0]
            cle2= keys[i][1]
            l2[i]-=cle2
            l2[i]=int(l2[i]/cle1)
            l2[i]=chr(l2[i])
    else:

        for i in range(len(l2)):
            cle1=keys[i][0]
            cle2= keys[i][1]
            l2[i]=ord(l2[i])
            l2[i]-=cle2
            l2[i]=int(l2[i]/cle1)
            l2[i]=chr(l2[i])
            
            
    filesave.writelines(l2)
    filesave.close()


def decrypte2():
    dec.delete(0, END)
    try:
        global sv
        l1=[]
        l2=[]
        file = askopenfilename(title="Textfile to decrypt")
        fichier=open(file,'r',encoding="utf8")
        try:
            file2=file+"Key.ini"
            fichier2=open(file2,'r',encoding="utf8")
        except IOError:
            file2 = askopenfilename(title="Encryption key",filetypes=[('key','.ini')])
            fichier2=open(file2,'r',encoding="utf8")
        for line in fichier.readlines():
            l1.append(list(map(int, line.split())))
        for line2 in fichier2.readlines():
            a=line2.split(";")
            a.remove("\n")
            for i in range(len(a)):
                a[i]=eval(a[i]) #transformer en tuple
            l2.append(a)
        sv=file+".DEC"
        #sv = asksaveasfilename(title="Sortie du fichier")
        for i in range(len(l2)):
            decrypte(l1[i],l2[i])
        dec.delete(0, END)
        fichier.close()
        fichier2.close()
        dec.insert(0,"Decryption done.")
        
    except ValueError:
        fichier.close()
        fichier2.close()
        fichier=open(file,'r',encoding="utf-8")
        fichier2=open(file2,'r',encoding="utf8")
        for line in fichier.readlines():
            l1.append(list(map(str, line.split())))
        for line2 in fichier2.readlines():
            a=line2.split(";")
            a.remove("\n")
            for i in range(len(a)):
                a[i]=eval(a[i]) #transformer en tuple
            l2.append(a)
        sv=file+".DEC"
        #sv = asksaveasfilename(title="Sortie du fichier")
        for i in range(len(l2)):
            l1[i]=list(l1[i][0])
            decrypte(l1[i],l2[i])
        dec.delete(0, END)
        dec.insert(0,"Decryption done.")
    except FileNotFoundError:
        dec.delete(0, END)
        dec.insert(0, "Operation stopped by the user.")

    except:
        dec.delete(0, END)
        dec.insert(0, "Error : "+str(sys.exc_info()[0])+" : "+ str(sys.exc_info()[1]))


def copyRight():
    showinfo("Credit","Copyright : Bensitel Younes. \n 2015")

def unicode():
    global mode
    if mode=="unicode":
        mode="basic"
        dec.delete(0, END)
        dec.insert(0, "Mode compressé désactivé : le mode normal est par conséquent réactivé.")
    else:
        mode="unicode"
        dec.delete(0, END)
        dec.insert(0, "Mode compressé activé : le fichier de sorti sera en unicode.")





special=["à","ç","ê","é","è","î","û","œ","ô","ï","â","û"]
ponctuation=[" ","-",",",";",":","=","!","/"]
divers=["&","@","*"]

def chiffrer(texte,clef):
    return coderTexte(texte,clef)

def dechiffrer(texte,clef):
    clef=-clef
    return coderTexte(texte,clef)

def coderMin(lettre,clef):
    clef=clef%26
    newl=ord(lettre)+clef
    if newl>ord("z"):
        return chr((newl-26))
    elif newl<ord("a"):
        return chr((newl+26))
    else: return chr((newl))

def coderMaj(lettre,clef):
    clef=clef%26
    newl=ord(lettre)+clef
    if newl>ord("Z"):
        return chr((newl-26))
    elif newl<ord("A"):
        return chr((newl+26))
    else: return chr((newl))
    
def coderCaractereSpecial(caractere,clef,liste):
    clef=clef%len(liste)
    newc=liste.index(caractere)+clef
    if newc>=len(liste):
        return liste[newc-len(liste)]
    elif newc<=0:
        return liste[newc+len(liste)]
    else: return liste[newc]
    
def coderCaractereInconnu(caractere,clef):
    return caractere

def coderTexte(texte,clef):
    newt=""
    for x in texte:
        newt+=coderCaractere(x,clef)
    return newt

def coderCaractere(caractere,clef):
    if caractere in special:
        return coderCaractereSpecial(caractere,clef,special)
    elif caractere in ponctuation:
        return coderCaractereSpecial(caractere,clef,ponctuation)
    elif caractere in divers:
        return coderCaractereSpecial(caractere,clef,divers)
    elif ord("a")<=ord(caractere)<=ord("z"):
        return coderMin(caractere,clef)
    elif ord("A")<=ord(caractere)<=ord("Z"):
        return coderMaj(caractere,clef)
    else: return coderCaractereInconnu(caractere,clef)
    
c = Checkbutton(root2, text="Activate compressed encryption", command=unicode)
c.pack()

barre = Menu(root2)
option=Menu(barre,tearoff=0)
edit=Menu(barre,tearoff=0)
affichage=Menu(barre,tearoff=0)
aide=Menu(barre,tearoff=0)
log=Menu(aide,tearoff=0)
barre.add_cascade(label="Fichier",menu=option)
option.add_command(label="Ouvrir un fichier")
option.add_command(label="Enregistrer Sous")
option.add_separator()
option.add_command(label="Quitter",command=fen.destroy)
barre.add_cascade(label="Edition",menu=edit)
barre.add_cascade(label="Affichage",menu=affichage)
barre.add_cascade(label="Aide",menu=aide)
aide.add_cascade(label="Version du logiciel",menu=log)
aide.add_command(label="Copyright",command=copyRight)
edit.add_command(label="Unicode encryption",command=unicode)
log.add_cascade(label=version)
root2.config(menu=barre)

Button(root2,text="Encrypt a text file",command=op,font=("Helvetica", 16)).pack()
Button(root2,text="Decrypt a text file",command=decrypte2,font=("Helvetica", 16)).pack()
#Button(root2,text="Clé de décryptage (en fichier)",command=op,font=("Helvetica", 16)).pack()
w = Label(root2, text="Avancement :",height=2,font=("Helvetica", 11))
w.pack(side='top')
dec = Entry(root2, width=80) #affiche ce qui se passe
dec.pack()



root2.mainloop()
