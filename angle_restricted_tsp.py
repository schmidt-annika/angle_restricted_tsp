from math import sqrt, degrees, acos
from sys import maxsize
from turtle import screensize, speed, setup, up, down, goto, dot, write, pencolor, hideturtle, clear

# Einlesen der Koordinaten aus der .txt-Datei in eine geschachtelte Liste
def koordinatenEinlesen(datei):
    global knoten_liste
    koordinaten = open(datei, mode="r", encoding="utf-8")
    # Die Koordinaten in eine einfache Liste einlesen [x1 y1, x2 y2, ...]
    knoten_liste = koordinaten.read().splitlines()
    # Die Koordinaten in einer geschachtelten Liste in x und y trennen [[x1, y1], [x2, y2], ...]
    for i in range(len(knoten_liste)):
        knoten_liste[i] = knoten_liste[i].split(" ")
        for j in range(2):
            knoten_liste[i][j] = float(knoten_liste[i][j])
    return

# Berechnen der Kantenlänge nach Pythagoras
def kantenBerechnen():
    global kanten_liste
    for i in range(len(knoten_liste)):
        # Erstellen einer leeren Liste für die Streckenlängen von dem Knoten i zu den anderen Knoten
        kanten_i = []
        for j in range(len(knoten_liste)):
            # Berechnen der Kantenlänge zwischen den Koordinaten i und j nach Pythagoras
            strecke = sqrt((knoten_liste[j][0] - knoten_liste[i][0])**2 + (knoten_liste[j][1] - knoten_liste[i][1])**2)
            strecke = round(strecke, 6)
            # Keine Knoten sollten doppelt vorkommen
            if strecke == 0.0 and j != i:
                del knoten_liste[i]
                del kanten_liste[i]
            # Hinzufügen der Kantenlänge zur Liste der Kantenlängen von i zu jedem anderen Koordinaten
            kanten_i.append(strecke)
        # Hinzufügen der Liste der Kantenlängen von i zu den anderen Knoten zur Liste der Kantenlänge
        kanten_liste.append(kanten_i)
    return

# Bei bestimmten Algorithmen ist es wichtig, dass in der Adjazenzliste beim Abstand zu sich selbst nicht 0 sondern ein besonders hoher Wert angegeben wird
def kantenMitMaxsizeZuSichSelbst(kanten, knoten):
    for i in range(len(knoten)):
        for j in range(len(knoten)):
            if j == i:
                kanten[i][j] = maxsize
    return kanten

# Bei anderen Algorithmen ist es wichtig, dass in der Adjazenzliste beim Abstand zu sich selbst nicht maxsize sondern 0 angegeben wird
def kantenMitNullZuSichSelbst(kanten, knoten):
    for i in range(len(knoten)):
        for j in range(len(knoten)):
            if j == i:
                kanten[i][j] = 0
    return kanten

# Gibt zurück, ob der Winkel zwischen pc und pj im Gegenuhrzeigersinn oder im Uhrzeigersinn oder kollinear ist, das wird manchmal zum Berechnen der Winkel benötigt
def orientierung(p, c, j):
    wert = (c[1] - p[1]) * (j[0] - c[0]) - (c[0] - p[0]) * (j[1] - c[1])
    if wert == 0:
        return "kollinear"
    elif wert > 0:
        return "mit"  
    else:
        return "gegen"
    
# Diese Funktion berechnet den Winkel zwischen den Kanten ab und bc, wobei a, b und c Indexe der Koordinatenpunkte sind
def winkelBerechnen(punkt_a, punkt_b, punkt_c):
    if orientierung(knoten_liste[punkt_a], knoten_liste[punkt_b], knoten_liste[punkt_c]) != "kollinear":
        a = kanten_liste[punkt_c][punkt_b]
        b = kanten_liste[punkt_a][punkt_c]
        c = kanten_liste[punkt_b][punkt_a]
        beta = degrees(acos(round((b**2 - (a**2 + c**2)) / (-2*a*c), 6)))
        return beta
    else:
        if punkt_a == punkt_b or punkt_a == punkt_c or punkt_b == punkt_c or (kanten_liste[punkt_a][punkt_b] + kanten_liste[punkt_b][punkt_c]) != kanten_liste[punkt_a][punkt_c]:
            return 0
        else:
            return 180

# Zur Visualisierung der Pfade reicht eine simple Bibliothek wie turtle vollkommen aus
def turtle(liste, boolesche, farbe):
    clear()
    hideturtle()
    up()
    win_width, win_height, bg_color = 2000, 2000, 'white'

    pencolor(farbe)
    setup()
    screensize(win_width, win_height, bg_color)
    speed(10)
    
    for i in range(len(liste)):
        if boolesche == False:
            up()
        else:
            down
        goto(liste[i][0], liste[i][1])
        down()
        dot(3)
    return

# Die Vorarbeit besteht darin, die Koordinaten aus den .txt-Datein in eine geschachtelte Liste einzulesen und die Kantenlänge zwischen diesen Koordinaten zu berechnen
def vorarbeit(datei):
    koordinatenEinlesen(datei)
    kantenBerechnen()
    #turtle(knoten_liste, False, "black")
    return

# Diese Funktionen werden bei Farthes und Nearest Insertion benötigt
def abstand(pfad, kanten, knoten_aus_uebrig):
    abstand = 0
    for i in pfad:
        abstand += kanten[i][knoten_aus_uebrig]
    return abstand

def minAbstandLokal(pfad, kanten, knoten_aus_uebrig):
    abstand = 0
    for i in pfad:
        if kanten[i][knoten_aus_uebrig] < abstand:
            abstand = kanten[i][knoten_aus_uebrig] > abstand
    return abstand

def maxAbstandLokal(pfad, kanten, knoten_aus_uebrig):
    abstand = 0
    for i in pfad:
        if kanten[i][knoten_aus_uebrig] > abstand:
            abstand = kanten[i][knoten_aus_uebrig] > abstand
    return abstand

# Diese Funktion wird beim Nearest Neighbour Algorithmus benötigt
def naechsterKnoten(kanten_an_parent, parent, pfad_indexe, besucht, verboten):
    naechster_punkt = None
    kuerzeste_kante = maxsize
    for j in range(len(kanten_an_parent)):
        if besucht[j] != True and j not in verboten and kanten_an_parent[j] < kuerzeste_kante and (len(pfad_indexe) == 1 or winkelBerechnen(pfad_indexe[parent-1], pfad_indexe[parent], j) >= 90):
            kuerzeste_kante = kanten_an_parent[j]
            naechster_punkt = j
    return naechster_punkt

# Diese Funktion wird für alle Insertion-Algorithmen benötigt
def moeglichstGuenstigEinfuegen(knoten, kanten, gewaehlte_kante_index, pfad_indexe, pfad_koordinaten, uebrig):
    aenderung = False
    kuerzestes_einfuegen = maxsize
    an = None
            
    if winkelBerechnen(gewaehlte_kante_index, pfad_indexe[0], pfad_indexe[1]) >= 90 and kanten[pfad_indexe[0]][gewaehlte_kante_index] < kuerzestes_einfuegen:
        kuerzestes_einfuegen = kanten[pfad_indexe[0]][gewaehlte_kante_index]
        an = "anfang"
        aenderung = True
                    
    if winkelBerechnen(pfad_indexe[len(pfad_indexe)-2], pfad_indexe[len(pfad_indexe)-1], gewaehlte_kante_index) >= 90 and kanten[pfad_indexe[len(pfad_indexe)-1]][gewaehlte_kante_index] < kuerzestes_einfuegen:
        kuerzestes_einfuegen = kanten[pfad_indexe[len(pfad_indexe)-1]][gewaehlte_kante_index]
        an = "len(pfad_indexe)-1"
        aenderung = True
                    
    for l in range(len(pfad_indexe)-1):
        if (kanten[l][gewaehlte_kante_index] + kanten[l+1][gewaehlte_kante_index]) - kanten[pfad_indexe[l]][l+1] < kuerzestes_einfuegen and winkelBerechnen(pfad_indexe[l], gewaehlte_kante_index, pfad_indexe[l+1]) >= 90 and ((l == 0 and (len(pfad_indexe) == 2 or winkelBerechnen(gewaehlte_kante_index, pfad_indexe[1], pfad_indexe[2]) >= 90)) or (l != 0 and ((l == len(pfad_indexe)-2 and winkelBerechnen(pfad_indexe[l-1], pfad_indexe[l], gewaehlte_kante_index) >= 90) or (winkelBerechnen(pfad_indexe[l-1], pfad_indexe[l], gewaehlte_kante_index) >= 90 and winkelBerechnen(gewaehlte_kante_index, pfad_indexe[l+1], pfad_indexe[l+2]) >= 90)))):
            kuerzestes_einfuegen = (kanten[l][gewaehlte_kante_index] + kanten[l+1][gewaehlte_kante_index]) - kanten[pfad_indexe[l]][l+1]
            an = l
            aenderung = True
                            
    if aenderung != False:
        if an == "anfang":
            pfad_indexe.insert(0, gewaehlte_kante_index)
            pfad_koordinaten.insert(0, knoten[gewaehlte_kante_index])
            uebrig[gewaehlte_kante_index] = False
            return(True, pfad_indexe, pfad_koordinaten, uebrig)
        elif an == "len(pfad_indexe)-1":
            pfad_indexe.append(gewaehlte_kante_index)
            pfad_koordinaten.append(knoten[gewaehlte_kante_index])
            uebrig[gewaehlte_kante_index] = False
            return(True, pfad_indexe, pfad_koordinaten, uebrig)
        else:
            pfad_indexe.insert(an+1, gewaehlte_kante_index)
            pfad_koordinaten.insert(an+1, knoten[gewaehlte_kante_index])
            uebrig[gewaehlte_kante_index] = False
            return(True, pfad_indexe, pfad_koordinaten, uebrig)
    else:
        return(False, pfad_indexe, pfad_koordinaten, uebrig)

# Diese Funktion wird am Ende zum Berechnen der Pfadlänge benötigt
def laenge(kanten, pfad):
    laenge = 0
    for i in range(len(pfad)-1):
        laenge += kanten[pfad[i]][pfad[i+1]]
    return laenge

# Hinzufügen des nähesten Knotens, gemessen am letzten Pfadglied
def nearestNeighbour(kanten, knoten):
    zaehler = 0
    while True:
        zaehler += 1
        if zaehler == len(knoten):
            return (False, [], [])
        start = knoten[zaehler]
        index = zaehler
        besucht = len(knoten) * [False]  
        besucht[index] = True
        pfad_koordinaten = [start]
        pfad_indexe = [index]
        stelle = 0
        while True:
            naechster_knoten = naechsterKnoten(kanten[index], stelle, pfad_indexe, besucht, [])
            if naechster_knoten == None:
                break
            else:
                besucht[naechster_knoten] = True
                pfad_koordinaten.append(knoten[naechster_knoten])
                pfad_indexe.append(naechster_knoten)
                stelle += 1
                index = naechster_knoten
                if len(pfad_koordinaten) == len(knoten):
                    #turtle(pfad_koordinaten, True, "red")
                    return (True, pfad_koordinaten, pfad_indexe)

# Suchen nach dem nähesten Punkt im Vergleich zu allen Punkten des Pfades und anschließend möglichst günstiges Einfügen in den Pfad 
def nearestInsertionHeuristik(kanten, knoten):
    kanten = kantenMitMaxsizeZuSichSelbst(kanten, knoten)
    zaehler = 0
    while True:
        zaehler += 1
        if zaehler == len(knoten):
            return (False, [], [])
        links_unten = knoten[zaehler]
        index_links_unten = zaehler
                
        kuerzste_strecke = min(kanten[index_links_unten])
        index_rechts_oben = kanten[index_links_unten].index(kuerzste_strecke)
        rechts_oben = knoten[index_rechts_oben]
        
        uebrig = len(knoten) * [True]
        uebrig[index_rechts_oben] = False
        uebrig[index_links_unten] = False
        
        pfad_koordinaten = [links_unten, rechts_oben]
        pfad_indexe = [index_links_unten, index_rechts_oben]
        abbruch = False
        while True:
            if abbruch == True:
                break
            if len(pfad_koordinaten) == len(knoten):
                #turtle(pfad_koordinaten, True, "red")
                return (True, pfad_koordinaten, pfad_indexe)
                    
            zu_pruefen = uebrig.copy()            
            while True:
            
                kuerzeste_kante = maxsize
                kuerzeste_kante_index = None
            
                for k in range(len(uebrig)):
                    if zu_pruefen[k] != False and abstand(pfad_indexe, kanten, k) < kuerzeste_kante:
                        kuerzeste_kante = abstand(pfad_indexe, kanten, k)
                        kuerzeste_kante_index = k
                
                if kuerzeste_kante_index == None:
                    abbruch = True
                    break
                else:
                    zu_pruefen[kuerzeste_kante_index] = False
                 
                aenderung, pfad_indexe, pfad_koordinaten, uebrig = moeglichstGuenstigEinfuegen(knoten, kanten, kuerzeste_kante_index, pfad_indexe, pfad_koordinaten, uebrig)
                if aenderung == True:
                    break

# Suchen nach dem weitesten Punkt im Vergleich zu allen Punkten des Pfades und anschließend möglichst günstiges Einfügen in den Pfad 
def farthestInsertionHeuristik(kanten, knoten):
    kanten = kantenMitNullZuSichSelbst(kanten, knoten) 
    zaehler = 0
    while True:
        zaehler += 1
        if zaehler == len(knoten):
            return (False, [], [])
        links_unten = knoten[zaehler]
        index_links_unten = zaehler
                
        laengste_strecke = max(kanten[index_links_unten])
        index_rechts_oben = kanten[index_links_unten].index(laengste_strecke)
        rechts_oben = knoten[index_rechts_oben]
        
        uebrig = len(knoten) * [True]
        uebrig[index_rechts_oben] = False
        uebrig[index_links_unten] = False
        
        pfad_koordinaten = [links_unten, rechts_oben]
        pfad_indexe = [index_links_unten, index_rechts_oben]
        abbruch = False
        while True:
            if abbruch == True:
                break
            if len(pfad_koordinaten) == len(knoten):
                #turtle(pfad_koordinaten, True, "red")
                return (True, pfad_koordinaten, pfad_indexe)
            zu_pruefen = uebrig.copy()            
            while True:
                laengste_kante = 0
                laengste_kante_index = None
            
                for k in range(len(zu_pruefen)):
                    if zu_pruefen[k] != False and abstand(pfad_indexe, kanten, k) > laengste_kante:
                        laengste_kante = abstand(pfad_indexe, kanten, k)
                        laengste_kante_index = k
                
                if laengste_kante_index == None:
                    abbruch = True
                    break
                else:
                    zu_pruefen[laengste_kante_index] = False
                    
                aenderung, pfad_indexe, pfad_koordinaten, uebrig = moeglichstGuenstigEinfuegen(knoten, kanten, laengste_kante_index, pfad_indexe, pfad_koordinaten, uebrig)
                if aenderung == True:
                    break        
                
# Suchen nach dem nähesten Punkt im Vergleich zu einem bestimmten Punkt des Pfades und anschließend möglichst günstiges Einfügen in den Pfad 
def nearestInsertionHeuristikMitLokalemMinimum(kanten, knoten):
    kanten = kantenMitMaxsizeZuSichSelbst(kanten, knoten)
    zaehler = 0
    while True:
        zaehler += 1
        if zaehler == len(knoten):
            return (False, [], [])
        links_unten = knoten[zaehler]
        index_links_unten = zaehler
                
        kuerzste_strecke = min(kanten[index_links_unten])
        index_rechts_oben = kanten[index_links_unten].index(kuerzste_strecke)
        rechts_oben = knoten[index_rechts_oben]
        
        uebrig = len(knoten) * [True]
        uebrig[index_rechts_oben] = False
        uebrig[index_links_unten] = False
        
        pfad_koordinaten = [links_unten, rechts_oben]
        pfad_indexe = [index_links_unten, index_rechts_oben]
        abbruch = False
        while True:
            if abbruch == True:
                break
            if len(pfad_koordinaten) == len(knoten):
                #turtle(pfad_koordinaten, True, "red")
                return (True, pfad_koordinaten, pfad_indexe)
            zu_pruefen = uebrig.copy()            
            while True:
                kuerzeste_kante = maxsize
                kuerzeste_kante_index = None
            
                for k in range(len(uebrig)):
                    if zu_pruefen[k] != False and minAbstandLokal(pfad_indexe, kanten, k) < kuerzeste_kante:
                        kuerzeste_kante = abstand(pfad_indexe, kanten, k)
                        kuerzeste_kante_index = k
                
                if kuerzeste_kante_index == None:
                    abbruch = True
                    break
                else:
                    zu_pruefen[kuerzeste_kante_index] = False
                        
                aenderung, pfad_indexe, pfad_koordinaten, uebrig = moeglichstGuenstigEinfuegen(knoten, kanten, kuerzeste_kante_index, pfad_indexe, pfad_koordinaten, uebrig)
                if aenderung == True:
                    break

# Suchen nach dem weitesten Punkt im Vergleich zu einem bestimmten Punkt des Pfades und anschließend möglichst günstiges Einfügen in den Pfad 
def farthestInsertionHeuristikMitLokalemMaximum(kanten, knoten):
    kanten = kantenMitNullZuSichSelbst(kanten, knoten) 
    zaehler = 0
    while True:
        zaehler += 1
        if zaehler == len(knoten):
            return (False, [], [])
        links_unten = knoten[zaehler]
        index_links_unten = zaehler
                
        laengste_strecke = max(kanten[index_links_unten])
        index_rechts_oben = kanten[index_links_unten].index(laengste_strecke)
        rechts_oben = knoten[index_rechts_oben]
        
        uebrig = len(knoten) * [True]
        uebrig[index_rechts_oben] = False
        uebrig[index_links_unten] = False
        
        pfad_koordinaten = [links_unten, rechts_oben]
        pfad_indexe = [index_links_unten, index_rechts_oben]
        abbruch = False
        while True:
            if abbruch == True:
                break
            if len(pfad_koordinaten) == len(knoten):
                #turtle(pfad_koordinaten, True, "red")
                return (True, pfad_koordinaten, pfad_indexe)
            zu_pruefen = uebrig.copy()            
            while True:
                laengste_kante = 0
                laengste_kante_index = None
            
                for k in range(len(uebrig)):
                    if zu_pruefen[k] != False and maxAbstandLokal(pfad_indexe, kanten, k) > laengste_kante:
                        laengste_kante = abstand(pfad_indexe, kanten, k)
                        laengste_kante_index = k
                
                if laengste_kante_index == None:
                    abbruch = True
                    break
                else:
                    zu_pruefen[laengste_kante_index] = False
                        
                aenderung, pfad_indexe, pfad_koordinaten, uebrig = moeglichstGuenstigEinfuegen(knoten, kanten, laengste_kante_index, pfad_indexe, pfad_koordinaten, uebrig)
                if aenderung == True:
                    break
                
# Suchen nach dem weitesten Punkt im Vergleich zu einem bestimmten Punkt des Pfades und anschließend möglichst günstiges Einfügen in den Pfad  
def randomInsertionHeuristik(kanten, knoten):
    zaehler = 0
    while True:
        zaehler += 1
        if zaehler == len(knoten)-1:
            return (False, [], [])
        links_unten = knoten[zaehler]
        index_links_unten = zaehler
                
        index_rechts_oben = zaehler+1
        rechts_oben = knoten[index_rechts_oben]
        
        uebrig = len(knoten) * [True]
        uebrig[index_rechts_oben] = False
        uebrig[index_links_unten] = False
        
        pfad_koordinaten = [links_unten, rechts_oben]
        pfad_indexe = [index_links_unten, index_rechts_oben]
        abbruch = False
        while True:
            if abbruch == True:
                break
            if len(pfad_koordinaten) == len(knoten):
                #turtle(pfad_koordinaten, True, "red")
                return (True, pfad_koordinaten, pfad_indexe) 
            zu_pruefen = uebrig.copy()            
            while True:
                zufaellige_kante_index = None
            
                for k in range(len(uebrig)):
                    if zu_pruefen[k] != False:
                        zufaellige_kante_index = k
                        break
                
                if zufaellige_kante_index == None:
                    abbruch = True
                    break
                else:
                    zu_pruefen[zufaellige_kante_index] = False
                        
                aenderung, pfad_indexe, pfad_koordinaten, uebrig = moeglichstGuenstigEinfuegen(knoten, kanten, zufaellige_kante_index, pfad_indexe, pfad_koordinaten, uebrig)
                if aenderung == True:
                    break

# Dieser Algorithmus verbindet Nearest Neighbour und Nearest Insertion miteinander, indem die günstigste Kante (direkt mit Berücksichtigung der Winkelbedingung) gesucht und in den Pfad eingefügt wird
def mischungNearestInsertionHeuristikUndNearestNeighbour(kanten, knoten):
    kanten = kantenMitMaxsizeZuSichSelbst(kanten, knoten)
    zaehler = 0
    while True:
        zaehler += 1
        if zaehler == len(knoten):
            return (False, [], [])
        links_unten = knoten[zaehler]
        index_links_unten = zaehler
                
        kuerzste_strecke = min(kanten[index_links_unten])
        index_rechts_oben = kanten[index_links_unten].index(kuerzste_strecke)
        rechts_oben = knoten[index_rechts_oben]
        
        uebrig = len(knoten) * [True]
        uebrig[index_rechts_oben] = False
        uebrig[index_links_unten] = False
        
        pfad_koordinaten = [links_unten, rechts_oben]
        pfad_indexe = [index_links_unten, index_rechts_oben]
        while True:
            aenderung = False
            kuerzeste_kante = maxsize
            kuerzeste_kante_index = None
            an = None
            
            for k in range(len(uebrig)):
                if uebrig[k] != False and winkelBerechnen(k, pfad_indexe[0], pfad_indexe[1]) >= 90 and kanten[pfad_indexe[0]][k] < kuerzeste_kante:
                    kuerzeste_kante = kanten[pfad_indexe[0]][k]
                    kuerzeste_kante_index = k
                    an = "anfang"
                    aenderung = True
                    
                if uebrig[k] != False and winkelBerechnen(pfad_indexe[len(pfad_indexe)-2], pfad_indexe[len(pfad_indexe)-1], k) >= 90 and kanten[pfad_indexe[len(pfad_indexe)-1]][k] < kuerzeste_kante:
                    kuerzeste_kante = kanten[pfad_indexe[len(pfad_indexe)-1]][k]
                    kuerzeste_kante_index = k
                    an = len(pfad_indexe)-1
                    aenderung = True
                    
            for l in range(len(pfad_indexe)-1):
                max_abstand = kanten[pfad_indexe[l]][pfad_indexe[l+1]]
                        
                zu_pruefen = uebrig.copy()
                while True:
                        
                    if len(pfad_koordinaten) == len(knoten):
                        #turtle(pfad_koordinaten, True, "red")
                        return (True, pfad_koordinaten, pfad_indexe)
                            
                    naehester_punkt_index = None
                    for n in range(len(zu_pruefen)):
                        if zu_pruefen[n] != False and (kanten[l][n] + kanten[l+1][n]) - kanten[pfad_indexe[l]][l+1] < kuerzeste_kante and (naehester_punkt_index == None or (kanten[pfad_indexe[l]][n] + kanten[pfad_indexe[l+1]][n]) < (kanten[pfad_indexe[l]][naehester_punkt_index] + kanten[pfad_indexe[l+1]][naehester_punkt_index])) and kanten[pfad_indexe[l]][n] < max_abstand:
                            naehester_punkt_index = n
                        
                    if naehester_punkt_index != None:
                        zu_pruefen[naehester_punkt_index] = False

                        if winkelBerechnen(pfad_indexe[l], naehester_punkt_index, pfad_indexe[l+1]) >= 90 and ((l == 0 and (len(pfad_indexe) == 2 or winkelBerechnen(naehester_punkt_index, pfad_indexe[1], pfad_indexe[2]) >= 90)) or (l != 0 and ((l == len(pfad_indexe)-2 and winkelBerechnen(pfad_indexe[l-1], pfad_indexe[l], naehester_punkt_index) >= 90) or (winkelBerechnen(pfad_indexe[l-1], pfad_indexe[l], naehester_punkt_index) >= 90 and winkelBerechnen(naehester_punkt_index, pfad_indexe[l+1], pfad_indexe[l+2]) >= 90)))):
                            kuerzeste_kante = (kanten[l][naehester_punkt_index] + kanten[l+1][naehester_punkt_index]) - kanten[pfad_indexe[l]][l+1]
                            kuerzeste_kante_index = naehester_punkt_index
                            an = l
                            aenderung = True
                    else:
                        break
                            
            if aenderung != False:
                if an == "anfang":
                    pfad_indexe.insert(0, kuerzeste_kante_index)
                    pfad_koordinaten.insert(0, knoten[kuerzeste_kante_index])
                    uebrig[kuerzeste_kante_index] = False
                elif an == len(pfad_indexe)-1:
                    pfad_indexe.append(kuerzeste_kante_index)
                    pfad_koordinaten.append(knoten[kuerzeste_kante_index])
                    uebrig[kuerzeste_kante_index] = False
                else:
                    pfad_indexe.insert(an+1, kuerzeste_kante_index)
                    pfad_koordinaten.insert(an+1, knoten[kuerzeste_kante_index])
                    uebrig[kuerzeste_kante_index] = False
                
            if aenderung == False:
                break
            
def primsAlgorithmus(kanten, knoten):
    mst_laenge =  0
    uebrig = len(knoten) * [True]
    uebrig[0] = False
    mst_enthalten = [0]
    
    while True:

        if len(mst_enthalten) == len(knoten):
            return mst_laenge

        naechster_knoten = None
        kuerzeste_entfernung = maxsize
        
        for j in range(len(uebrig)):
            if uebrig[j] == False:
                continue
            for k in mst_enthalten:
                if kanten[j][k] < kuerzeste_entfernung:
                    naechster_knoten = j
                    kuerzeste_entfernung = kanten[naechster_knoten][k]
        mst_laenge += kuerzeste_entfernung
        uebrig[naechster_knoten] = False
        mst_enthalten.append(naechster_knoten)
            
 
def winkelPruefen(pfad, i, j):   
    if (i == 1 or winkelBerechnen(pfad[i-2], pfad[i-1], pfad[i]) >= 90) and winkelBerechnen(pfad[i-1], pfad[i], pfad[i+1]) >= 90 and winkelBerechnen(pfad[j-2], pfad[j-1], pfad[j]) >= 90 and (j == len(pfad)-1 or winkelBerechnen(pfad[j-1], pfad[j], pfad[j+1]) >= 90):
        return True
    else:
        return False
    
def twoOpt(pfad_indexe, pfad_koordinaten, kanten, boolsche):
    while True:
        verbessert = False
        for i in range(1, len(pfad_indexe)-2):
            if verbessert == True:
                break
            for j in range(i+1, len(pfad_indexe)):
                if j-i == 1:
                    continue
                else:
                    neuer_pfad_indexe = pfad_indexe[:]
                    neuer_pfad_koordinaten = pfad_koordinaten[:]
                    neuer_pfad_indexe[i:j] = pfad_indexe[j-1:i-1:-1]
                    neuer_pfad_koordinaten[i:j] = pfad_koordinaten[j-1:i-1:-1]
                    if winkelPruefen(neuer_pfad_indexe, i, j) == True and ((kanten[pfad_indexe[i]][pfad_indexe[i-1]] + kanten[pfad_indexe[j]][pfad_indexe[j-1]]) > (kanten[neuer_pfad_indexe[i]][neuer_pfad_indexe[i-1]] + kanten[neuer_pfad_indexe[j]][neuer_pfad_indexe[j-1]])):
                        pfad_indexe = neuer_pfad_indexe
                        pfad_koordinaten = neuer_pfad_koordinaten
                        verbessert = True
                        break
        if verbessert == False:
            break
    if boolsche == "ja":
        turtle(pfad_koordinaten, True, "green")
    return (pfad_koordinaten, pfad_indexe)
                    
knoten_liste = []
kanten_liste = []



welches_verfahren = input("Mit welchem Verfahren (Auswahl: nn, ni, fi, nilm, film, ri, nni, mst): ")
welche_datei = input("Welche Datei soll ausgelesen werden (z.B. wenigerkrumm1.txt): ")
if welches_verfahren != "mst":
    mit_oder_ohne_turtle = input("Soll die Route durch Australien visualisiert werden? (ja/nein) ")
vorarbeit(welche_datei)

if welches_verfahren == "nn":        
    fertig, pfad_koordinaten, pfad_indexe = nearestNeighbour(kanten_liste, knoten_liste)
    if fertig == True:
        pfad_koordinaten, pfad_indexe = twoOpt(pfad_indexe, pfad_koordinaten, kanten_liste, mit_oder_ohne_turtle)
        print("Die Länge des Pfades bei Nearest Neighbour:", laenge(kanten_liste, pfad_indexe))
        print("Die Koordinaten werden dabei in folgenden Reihenfolge abgeflogen:", pfad_koordinaten)

elif welches_verfahren == "ni": 
    fertig, pfad_koordinaten, pfad_indexe = nearestInsertionHeuristik(kanten_liste, knoten_liste)
    if fertig == True:
        pfad_koordinaten, pfad_indexe = twoOpt(pfad_indexe, pfad_koordinaten, kanten_liste, mit_oder_ohne_turtle)
        print("Die Länge des Pfades bei Nearest Insertion:", laenge(kanten_liste, pfad_indexe))
        print("Die Koordinaten werden dabei in folgenden Reihenfolge abgeflogen:", pfad_koordinaten)
        
elif welches_verfahren == "fi":
    fertig, pfad_koordinaten, pfad_indexe = farthestInsertionHeuristik(kanten_liste, knoten_liste)
    if fertig == True:
        pfad_koordinaten, pfad_indexe = twoOpt(pfad_indexe, pfad_koordinaten, kanten_liste, mit_oder_ohne_turtle)
        print("Die Länge des Pfades bei Farthes Insertion:", laenge(kanten_liste, pfad_indexe))
        print("Die Koordinaten werden dabei in folgenden Reihenfolge abgeflogen:", pfad_koordinaten)

elif welches_verfahren == "nilm":
    fertig, pfad_koordinaten, pfad_indexe = nearestInsertionHeuristikMitLokalemMinimum(kanten_liste, knoten_liste)
    if fertig == True:
        pfad_koordinaten, pfad_indexe = twoOpt(pfad_indexe, pfad_koordinaten, kanten_liste, mit_oder_ohne_turtle)
        print("Die Länge des Pfades bei Nearest Insertion mit lokalem Minimum:", laenge(kanten_liste, pfad_indexe))
        print("Die Koordinaten werden dabei in folgenden Reihenfolge abgeflogen:", pfad_koordinaten)
        
elif welches_verfahren == "film":
    fertig, pfad_koordinaten, pfad_indexe = farthestInsertionHeuristikMitLokalemMaximum(kanten_liste, knoten_liste)
    if fertig == True:
        pfad_koordinaten, pfad_indexe = twoOpt(pfad_indexe, pfad_koordinaten, kanten_liste, mit_oder_ohne_turtle)
        print("Die Länge des Pfades bei Farthes Insertion mit lokalem Maximum:", laenge(kanten_liste, pfad_indexe))
        print("Die Koordinaten werden dabei in folgenden Reihenfolge abgeflogen:", pfad_koordinaten)
        
elif welches_verfahren == "ri":
    fertig, pfad_koordinaten, pfad_indexe = randomInsertionHeuristik(kanten_liste, knoten_liste)
    if fertig == True:
        pfad_koordinaten, pfad_indexe = twoOpt(pfad_indexe, pfad_koordinaten, kanten_liste, mit_oder_ohne_turtle)
        print("Die Länge des Pfades bei Random Insertion:", laenge(kanten_liste, pfad_indexe))
        print("Die Koordinaten werden dabei in folgenden Reihenfolge abgeflogen:", pfad_koordinaten)
        
elif welches_verfahren == "nni":
    fertig, pfad_koordinaten, pfad_indexe = mischungNearestInsertionHeuristikUndNearestNeighbour(kanten_liste, knoten_liste)
    if fertig == True:
        pfad_koordinaten, pfad_indexe = twoOpt(pfad_indexe, pfad_koordinaten, kanten_liste, mit_oder_ohne_turtle)
        print("Die Länge des Pfades bei der Mischung aus Nearest Insertion und Nearest Neighbour:", laenge(kanten_liste, pfad_indexe))
        print("Die Koordinaten werden dabei in folgenden Reihenfolge abgeflogen:", pfad_koordinaten)
        
elif welches_verfahren == "mst":
    print("Die Länge des minimum spanning tree:", primsAlgorithmus(kanten_liste, knoten_liste))