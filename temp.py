import requests
import re
import csv
from bs4 import BeautifulSoup
from itertools import zip_longest
    
def getNombreclan ():
    url = 'https://statsroyale.com/es/top/clans'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    clan = soup.findAll('div',class_='ui__blueLink')
    enlaces = []
    for link in clan:
        enlaces.append(link.get('href'))
    return enlaces

def getURL (enlace):
    url = 'https://statsroyale.com/es/clan/' + enlace
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    clan = soup.find('div',class_='clan__table')
    return clan

def getTitulo (enlace):
    url = 'https://statsroyale.com/es/clan/' + enlace
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    titulo = soup.find('div',class_='clan__name')
    return titulo

def getClannombre(nombres, clan):    
    clanname = clan.find_all('div', class_='ui__headerMedium clan__clanName')
    for pertenece in clanname:
        nombres.append(pertenece.get_text(strip=True))
    return nombres
 
def getNombre(jugadores, clan):    
    nombre = clan.find_all('a')
    for mote in nombre:
        jugadores.append(mote.findAll(text=True))
    return jugadores

def getNivel (niveles, clan):
    nivel = clan.find_all('span', class_='clan__playerLevel')
    for level in nivel:
        niveles.append(level.findAll(text=True))
    return niveles

def getPuesto (puestos, clan):
    puesto = clan.find_all('div', class_='clan__row')
    for posicion in puesto:
        puestos.append(posicion.get_text(strip=True))
    return puestos                                                      
                                                  
def getTrofeo (trofeos, clan):
    trofeo = clan.find_all('div', class_='clan__cup')
    for coronas in trofeo:
        trofeos.append(coronas.findAll(text=True))  
    return trofeos

def getDonacion (donaciones, clan):
    donacion = clan.find_all('div', class_='clan__donation')
    for carta in donacion:
        donaciones.append(carta.findAll(text=True))           
    return donaciones

def getRol (roles, clan):
    rol = clan.find_all('div', class_='clan__memberRoleInner')
    for miembro in rol:
        roles.append(miembro.findAll(text=True)) 
    return roles

jugadores = []
niveles = []
puestos = []
trofeos = []
donaciones = []
roles = []
nombres = []

codigo = input("Introduce el código de clan, o en blanco para los 200 mejores: ")
if codigo == '':
    nombreclan = []
else:
    nombreclan = [codigo]

if not nombreclan:
    listaclanes = getNombreclan ()
else:
    listaclanes = ['https://statsroyale.com/es/clan/' + nombreclan[0]]
    
for clanes in listaclanes:
    enlace = clanes.rsplit('/', 1)[-1]  
    clan = getURL (enlace)
    if clan == None:
        continue
    else:
        titulo = getTitulo (enlace)
#        clannombre = getClannombre (nombres,titulo)
        puestos = getPuesto (puestos,clan)
        jugadores = getNombre (jugadores,clan)
        niveles = getNivel (niveles,clan)
        trofeos = getTrofeo (trofeos,clan)
        donaciones = getDonacion (donaciones,clan)
        roles = getRol (roles,clan)
    
puestos = [x for x in puestos if re.match('^#[1-9]|#[1-4][0-9]|#50$',x)]

if not clan:
    print ("Error al introducir código del clan. Inténtalo de nuevo")
else:
    tabla = (puestos,jugadores,trofeos,donaciones,roles)
    export_data = zip_longest(*tabla,fillvalue = '')
    with open('stats.csv', 'w', encoding='utf-8',newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("Puesto", "Nombre", "Trofeos", "Donaciones", "Rol"))
        wr.writerows(export_data)
    myfile.close()  
