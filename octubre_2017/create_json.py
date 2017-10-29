#!/usr/bin/python3
# coding=utf-8

import re
import os

from tesserocr import PyTessBaseAPI

# '1001-LV-SJO-HER-ALA.jpg'
images = ['1001-LV-SJO-HER-ALA_tabla.png', '1002-LV-ALA-HER-SJO_tabla.png']


def main():
    print("iniciando el programa")

    for image_path in images:
        textual_trips = get_lines(image_path)

        schedule = parse_times(textual_trips)

        schedule = fix_schedule(schedule, image_path)

        # debug
        print("time table: ", image_path)
        for trip in schedule:
            print(trip)


def fix_schedule(trips_schedules, route):
    '''
    custom method
    '''

    schedule = []

    if "SJO-HER-ALA" in route:
        # debug
        #print("ruta SJO - Heredia - Alajuela")

        fixed_trip = []
        for trip in trips_schedules:
            # based on time table adds empty times at begining and/or end.
            if len(trip) == 9:
                fixed_trip = ["-", "-"] + trip
            elif len(trip) == 5:
                fixed_trip = ["-", "-"] + trip + ["-", "-", "-", "-"]
            elif len(trip) == 7:
                fixed_trip = trip + ["-", "-", "-", "-"]
            else:
                fixed_trip = trip

            schedule += [fixed_trip]

    elif "ALA-HER-SJO" in route:
            # debug
            # print("ruta ALA-HER-SJO")

            fixed_trip = []
            for trip in trips_schedules:
                # based on time table adds empty times at begining and/or end.
                if len(trip) == 5:
                    fixed_trip = ["-", "-", "-", "-"] + trip + ["-", "-"]
                elif len(trip) == 9:
                    fixed_trip = trip + ["-", "-"]
                elif len(trip) == 7:
                    fixed_trip = ["-", "-", "-", "-"] + trip
                else:
                    fixed_trip = trip

                schedule += [fixed_trip]

    return schedule


def get_lines(filename):
    '''
    Args
    ::filename (str): Image file relative or absolute path.

    Return:
    ::list: List of lines as text from the image. Every line contain the stop
      times for a certain trip.
    '''
    api = PyTessBaseAPI()
    api.SetImageFile(filename)
    text = api.GetUTF8Text()

    textual_lines = []
    line = ''
    line_num = 0
    for char in text:
        line += char
        if char == "\n":
            # ignore lines with less than 5 chars (H:MM)
            if len(line) < 5:
                line = ''
                continue
            else:
                line_num += 1
                # debug
                # print('linea: "', line, '" numero: ', line_num,
                # q      'largo de linea: ', len(line))
                textual_lines.append(line)
                line = ''

    return textual_lines


def parse_times(textual_trips):
    '''
    Arguments:
    ::textual_trips is a str representing a trip recognized from the image.

    ::return a list of trips schedules lists. A schedule list contains stop
      times of type str.
    '''

    pattern = "(?P<hours>[0-9]|0[0-9]|1[0-9]|2[0-3])(:| )(?P<minutes>[0-5][0-9])"
    trips_schedules = []

    for line in textual_trips:
        result = re.compile(pattern)
        stop_times = []

        for match in result.finditer(line):
            # debug
            # print(match.groupdict())
            hours = match.groupdict()['hours']
            minutes = match.groupdict()['minutes']
            stop_times += [hours + ":" + minutes]

        # debug
        # print("\nagregando stop times: ")
        # print(stop_times)
        trips_schedules += [stop_times]

    return trips_schedules


if __name__ == "__main__":
    main()
