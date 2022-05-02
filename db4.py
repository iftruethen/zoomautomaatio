import sqlite3
import subprocess
from time import time
import datetime
#import koodinhakija
conn = sqlite3.connect('tiedot.db') #(ID INTEGER PRIMARY KEY, course TEXT, meetingID TEXT, passcode TEXT)
conn.isolation_level = None

#koodin_hakija = Hakija()

def bashcom(cmd):
    subprocess.Popen(cmd, shell=True, executable='/bin/bash')

c=conn.cursor()
# c.execute("CREATE TABLE Tiedot (ID INTEGER PRIMARY KEY, course TEXT, meetingID TEXT, passcode TEXT)")
bashcom("xrandr -s 1360x768")

def print_choices():
    print("""
        Valitse toiminto:
        1 - ajasta nauhoitus (valitse Zoom-koodi listalta)
        2 - ajasta nauhoitus (suoraan Zoom-koodin perusteella)
        3 - ajasta nauhoitus (hae Zoom-koodin verkosta)
        4 - näytä oletukset
        5 - lisää uusi oletus
        6 - poista oletus
        7 - muokkaa oletusta
        8 - poistu
        """)

def tulosta_lista():
    c.execute("SELECT * FROM Tiedot")
    table=c.fetchall()
    otsakkeet=[('ID','Kurssin nimi','Zoom-koodi','Passcode')]
    col_width = [max(len(str(x)) for x in col) for col in zip(*table)]
    for otsake in otsakkeet:
        print ("\n        " + " \t".join("{0:{1}}".format(x, col_width[i]) for i, x in enumerate(otsake)) + "")
    for line in table:
        print ("        " + " \t".join("{0:{1}}".format(x, col_width[i]) for i, x in enumerate(line)) + "")

# def tulosta_lista():
#     c.execute("SELECT * FROM Tiedot")
#     print(c.fetchall())

# käyttöliittymä:
while True:
    print_choices()
    response=input()

    if response=="1": #ajasta nauhoitus (oletuksesta)
        print("Valitse kurssi:")
        tulosta_lista()
        valinta=input("\nAnna ID: ")

        v=" "  #alustaa kyselyn vastausmuuttujan, kysyy onko aloitusaika oikein
        while v.upper() != "K":
            aloitusaika=input("Anna nauhoituksen aloitusaika muodossa [HHMM]: ")
            aloitusaika=aloitusaika[0:2]+":"+aloitusaika[2:4]
            v=input("Aloitetaanko nauhoitus " + aloitusaika + " ? (K/E): ")
            while v.upper() not in "KE":
                v=input("Aloitetaanko nauhoitus " + aloitusaika + "? (K/E): ")

        luentokoodi=c.execute("SELECT meetingID FROM Tiedot WHERE ID=?",[valinta]).fetchall()[0][0]  # hakee Zoom-koodin
        pc=c.execute("SELECT passcode FROM Tiedot WHERE ID=?",[valinta]).fetchall()[0][0]  # hakee salasanan

        bashcom("""        
            pkill -f zoom
            zoom &
            sleep 5
            ikkunaId=$(wmctrl -l | grep -i "zoom")
            ikkunaId=${ikkunaId:0:10}
            xdotool windowactivate $ikkunaId
            xdotool key Tab
            xdotool key Return
            sleep 1
            """

            #syötetään meetinkikoodi
            """
            ikkunaId=$(wmctrl -l | grep -i "zoom" | grep -iv "cloud")
            ikkunaId=${ikkunaId:0:10}
            ikkunaDec=${ikkunaId:2:10}
            ikkunaDec=$((16#$ikkunaDec))
            xdotool windowactivate $ikkunaDec;
            """ # aktivoi ikkunan
            """
            xdotool key Tab
            xdotool key Tab
            xdotool type --window $ikkunaDec --delay 5 $kokousID;
            """ # syöttää kokoustunnuksen
            """
            xdotool key Return;
            sleep 3;
            iserror=$(wmctrl -l | grep -i "leave mee")
            if [ ${#iserror} != 0 ] # cathcaa mahdollisen "invalid meeting ID":n
            then
                xdotool windowactivate ${iserror:0:10}
                xdotool key Tab
                xdotool key Tab
                xdotool key Tab
                xdotool key Return
            fi
            sleep 3;
            if [ ${#kokousPW} != 0 ]
            then
                xdotool type --window $ikkunaDec --delay 5 $kokousPW
                xdotool key --window $ikkunaDec Return
                sleep 2;
            fi
            xdotool key --window $ikkunaDec Return

            nohup obs --startrecording &>/dev/null &
            sleep 5
            ikkunaId2=$(wmctrl -l | grep -i "obs")
            ikkunaId2=${ikkunaId:0:10}
            xdotool windowminimize $ikkunaId2
            sleep 5
            ikkunaId=$(wmctrl -l | grep -i "zoom meeting")
            ikkunaId=${ikkunaId:0:10}
            xdotool windowactivate $ikkunaId
            xdotool windowsize $ikkunaId 95% 95%
            xdotool windowmove $ikkunaId 0 0
        """
        )

    elif response=="2": #ajasta nauhoitus (koodin perusteella)
        name=input("Anna kurssin nimi: ")
        koodi=input("Anna Zoom-koodi: ")
        pc=input("Anna salasana (paina enter jos ei salasanaa): ")
    elif response=="3": #zoom-koodi verkosta
        name=input("Anna kurssin nimi: ")
        zoominfo = koodin_hakija.hae()
        koodi=zoominfo[0]
        pc=zoominfo[1]
    elif response=="4": #näytä oletukset
        tulosta_lista()
    elif response=="5": #lisää uusi oletus
        name=input("Kurssin nimi: ")
        koodi=input("Zoom-kokoustunnus: ")
        pc=input("Kokoussalasana: ")
        c.execute("INSERT INTO Tiedot(course,meetingID,passcode) VALUES (?,?,?)",
            [(name),(koodi),(pc)])
    elif response=="6": #poista oletus
        poistettava=input("Anna ID mikä poistetaan: ")
        c.execute("DELETE FROM Tiedot WHERE ID=(?)",[(poistettava)])
    elif response=="7": #muokkaa oletusta
        muokattava=input("Anna ID mitä muokataan: ")
        name=input("Anna kurssin nimi: ")
        koodi=input("Anna Zoom-koodi: ")
        pc=input("Anna salasana (paina enter jos ei salasanaa): ")
        c.execute("UPDATE Tiedot SET course=(?),meetingID=(?),passcode=(?) WHERE ID=(?)",
            [(name),(koodi),(pc),(muokattava)])
    elif response=="8": #poistu
        conn.commit()
        c.close()
        exit()
    else:
        print("\nTarkista syöte\n")