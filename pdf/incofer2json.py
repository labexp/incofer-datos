#!/usr/bin/env python3
# coding=utf-8

import re
import json


# to create the txt file using the incofer pdf use the command:
# $pdftotext -layout $filename.pdf
def main(filename="HORARIO-CARTAGO-AGOSTO-2016.txt",stops=8, dialog=False):
    '''
    stops : cantidad de paradas que tiene el archivo de entrada
    dialog: si quiere preguntarse al usuario por el nombre de cada parada.
    '''
    #approximate minimum length of line with stations data
    STATIONS_MIN_LINE_LEN = 20

    #column number of each stops in input file
    stops_cols = get_stops_span(filename, stops)

    #metadada
    sentido = None
    estaciones = []
    horarios = []
    num_linea = 0

    #run command $pdftotext -layout $filename
    incofer_data = open(filename, "r")
    for linea in incofer_data:

        if "-" in linea:
            #posiblemente sea el "sentido"
            #print(num_linea, "sentido")

            if sentido == None:
                sentido = linea.strip()

            else:
                #salvar los datos hasta ahora.
                save_data(sentido, estaciones, horarios)
                #reset variables
                sentido = linea.strip()
                estaciones = []
                horarios = []

        elif ":" in linea:
            #print(num_linea, "hay horarios")
            trip =list(["-"] * stops )

            pattern = re.compile("([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]")
            for hora in pattern.finditer(linea):
                column = hora.start(0)
                i = get_stop_index(stops_cols, column)
                trip[i] = hora.group(0)

            horarios.append(trip)


        elif len(linea) > STATIONS_MIN_LINE_LEN:
            if estaciones != []:
                continue
            else:
                for n in range(stops):
                    if dialog:
                        estacion = input("["+sentido+"] nombre de la estación " + str(n) + ": ")
                    else:
                        estacion = str(n)
                    estaciones.append(estacion)

        else:
            #print(num_linea, "nada")
            #esta línea no contiene nada útil.
            pass
        num_linea += 1

    #end of file
    save_data(sentido, estaciones, horarios)
    incofer_data.close()



def get_stop_index(stops, colum_number):
    '''
    stops is returned from get_stops_span
'''

    for stop_col in stops:

        if abs(int(stop_col) - int(colum_number)) <= 1:
            return stops.index(stop_col)
    else:
        return -1


def get_stops_span(filename, stops_num):
    '''
    incofer_filename: nombre del archivo con la info de las paradas.

    retorna un arreglo de N elementos. Cada uno tendrá la posición inicial de
    cada una de las paradas.
'''
    stops_span = []

    incofer_data = open(filename, "r")
    for linea in incofer_data:

        if linea.count(":") == stops_num:
            pattern = re.compile("([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]")
            for hora in pattern.finditer(linea):
                stops_span.append(hora.start(0))
            break

    incofer_data.close()

    return stops_span

def save_data(sentido, estaciones, horarios):

    internal_data = { "from":estaciones[0], "to":estaciones[-1], "estaciones":estaciones, "horarios":horarios}

    with open(sentido+".json", "w") as archivo:
        json.dump({sentido : internal_data}, archivo, ensure_ascii=False)

    archivo.close()

    #debug
    '''
    print("sentido:", sentido)
    print("estaciones:",estaciones)
    print("horarios:")
    for h in horarios:
        print("\t", h)
    '''


if __name__ == "__main__":

    pavas = "HORARIO-PAVAS-AGOSTO-2016.txt"
    pavas_stops = 16
    #main(pavas,pavas_stops, False)

    #fix me
    heredia = "HORARIO-HEREDIA-AGOSTO-2016.txt"
    heredia_stops=10
    #main(heredia,heredia_stops, False)

    belén = "HORARIO-BELEN-AGOSTO-2016.txt"
    belén_stops = 5
    #main(belén,belén_stops, False)

    cartago = "HORARIO-CARTAGO-AGOSTO-2016.txt"
    CARTAGO_STOPS = 8
    #main(cartago,CARTAGO_STOPS, False)

    alajuela = "Horarios-Rio-Segundo.txt"
    alajuela_stops = 10
    #main(alajuela,alajuela_stops, False)
