# -*- coding: utf-8 -*-
# Importamos los paquetes que vamos a utilizar
import requests
import re
import csv
from bs4 import BeautifulSoup
from itertools import zip_longest
import time
import os
start_time = time.time()

# De la URL indicada, almacenamos en clan los div con esa clase, y luego extraemos 
# los href en enlaces
def getNombreclan ():
    url = 'https://statsroyale.com/es/top/clans'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    clan = soup.findAll('div',class_='ui__blueLink')
    enlaces = []
    for link in clan:
        enlaces.append(link.get('href'))
    return enlaces

# Creamos nuestra URL y almacenamos en clan el div de la clase table
def getURL (enlace):
    url = 'https://statsroyale.com/es/clan/' + enlace
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    clan = soup.find('div',class_='clan__table')
    return clan

# Creamos nuestra URL y almacenamos en título los div de la clase name
def getTitulo (enlace):
    url = 'https://statsroyale.com/es/clan/' + enlace
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    titulo = soup.find('div',class_='clan__name')
    return titulo

# Extraemos todos los nombres de los clanes
def getClannombre(nombres, titulo):
    clanname = titulo.find_all('div', class_='ui__headerMedium clan__clanName')
    for pertenece in clanname:
        nombres.append(pertenece.get_text(strip=True))
    return nombres

# Almacenamos todos los enlaces a las imágenes de escudos. Si el 
# usuario a seleccionado que quiere almacenar las imágenes, aquí
# se realizaría esa función
def getClanescudos(nombreimagen,escudos, titulo, descarga,imagen):
    clanescudo = titulo.find_all('img', class_='clan__clanWarBadge')
    if not clanescudo:
        clanescudo = titulo.find_all('img', class_='clan__clanBadge')
    for emblema in clanescudo:
        s = [x['src'] for x in clanescudo]
        emblema = "https://statsroyale.com%s"%(s[0])
        escudos.append(emblema)
# Aquí, si el ususario ha seleccionado que quiere decargar las imágenes,
# entramos sólo la primera vez que analizamos un clan, ya que sólo hay un escudo
# por clan. Y renombramos la descarga con el nombre del propio clan
    if (descarga in ('s','S') and (imagen == 0)):
        filename = "/Escudos/"
        local_filename = filename + nombreimagen + '.png'
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(local_filename, 'wb') as f:
            f.write(requests.get(emblema).content)
    return escudos

# Se obtienes todos los nombres de los jugadores de un clan
def getNombre(jugadores, clan):    
    nombre = clan.find_all('a')
    for mote in nombre:
        jugadores.append(mote.get_text(strip=True))
    return jugadores

# Se obtienes los niveles de cada jugador
def getNivel (niveles, clan):
    nivel = clan.find_all('span', class_='clan__playerLevel')
    for level in nivel:
        niveles.append(level.get_text(strip=True))
    return niveles

# Se obtienen las posiciones de cada jugador en su clan
def getPuesto (puestos, clan):
    puesto = clan.find_all('div', class_='clan__row')
    for posicion in puesto:
        puestos.append(posicion.get_text(strip=True))
    return puestos                                                      
                                
# Se obtienen los trofeos de cada jugador                  
def getTrofeo (trofeos, clan):
    trofeo = clan.find_all('div', class_='clan__cup')
    for coronas in trofeo:
        trofeos.append(coronas.get_text(strip=True))  
    return trofeos

# Se obtienen las donaciones de cada jugador
def getDonacion (donaciones, clan):
    donacion = clan.find_all('div', class_='clan__donation')
    for carta in donacion:
        donaciones.append(carta.get_text(strip=True))           
    return donaciones

# Se obtiene el rol de cada jugador en su clan
def getRol (roles, clan):
    rol = clan.find_all('div', class_='clan__memberRoleInner')
    for miembro in rol:
        roles.append(miembro.get_text(strip=True)) 
    return roles

# inicializamos las variables que vayamos a usar
jugadores = []
niveles = []
puestos = []
trofeos = []
donaciones = []
roles = []
nombres = []
clanesnombres = []
escudos = []
i=0
imagen = 0

# le preguntamos al usuario si quiere hacer la consulta de un clan 
# concreto o seleccionaremos los 200 mejores
# Además le preguntaremos si quieres almacenar las imágenes de escudos
codigo = input("Introduce el código de clan, o en blanco para los 200 mejores: ")
descarga = input("¿Quieres descargar las imágenes de los escudos? S/N : ")
if codigo == '':
    nombreclan = []
else:
    nombreclan = [codigo]

# En función de si el usuario quiere consultar un clan o los 200 mejores
if not nombreclan:
    listaclanes = getNombreclan ()
else:
    listaclanes = ['https://statsroyale.com/es/clan/' + nombreclan[0]]

# recorremos cada url de los clanes a consultar    
for clanes in listaclanes:
# generamos el ID de cada clan con el que generaremos la/s URLs
    enlace = clanes.rsplit('/', 1)[-1]  
    clan = getURL (enlace)
    if clan == None:
        continue
    else:
        titulo = getTitulo (enlace)
        puestos = getPuesto (puestos,clan)
        jugadores = getNombre (jugadores,clan)
        niveles = getNivel (niveles,clan)
        trofeos = getTrofeo (trofeos,clan)
        donaciones = getDonacion (donaciones,clan)
        roles = getRol (roles,clan)
        contador = len(jugadores)
# Ya que el nombre del clan y la imagen será una para cada jugador,
# generamos una entrada por cada jugador que haya en el clan        
        while i < contador:
            nombres = getClannombre (nombres,titulo)
            nombreimagen = nombres[i]
            escudos = getClanescudos (nombreimagen,escudos,titulo,descarga,imagen)
            imagen = 1
            i += 1
        imagen = 0

# seleccionamos, en todo lo almacenado de las posiciones, lo que 
# comience por # seguido de ciertos números        
puestos = [x for x in puestos if re.match('^#[1-9]|#[1-4][0-9]|#50$',x)]

# aviso de error si el ID del clan no existe                                          
if not clan:
    print ("Error al introducir código del clan. Inténtalo de nuevo")
else:
# generamos una tabla que exportaremos a formato csv
    tabla = (nombres,escudos,puestos,jugadores,trofeos,donaciones,roles)
    export_data = zip_longest(*tabla,fillvalue = '')
    filename = "/Estadisticas/clashroyale_stats_dataset.csv"
    local_filename = "/Estadisticas/"
    os.makedirs(os.path.dirname(local_filename), exist_ok=True)
# rellenamos nuestro archivo csv con el contenido de la tabla generada    
    with open(filename, 'w', encoding='utf-8',newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("Clan", "Escudo", "Puesto", "Nombre", "Trofeos", "Donaciones", "Rol"))
        wr.writerows(export_data)
    myfile.close()  

print("--- %s seconds ---" % (time.time() - start_time))