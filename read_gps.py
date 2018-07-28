from argparse import ArgumentParser
from contextlib import contextmanager
import os
import pynmea2
import serial


# Serial
GPS_TTY = '/dev/tty.usbserial'
BAUD = 4800
TIMEOUT = 5


# NMEA
GPS_TALKER_ID = 'GP'
GPS_SENTENCE_IDS = [
    'BOD', # Bearing, origin to destination
    'BWC', # Bearing and distance to waypoint, great circle
    'GGA', # Global Positioning System Fix Data
    'GLL', # Geographic position, latitude / longitude
    'GSA', # GPS DOP and active satellites 
    'GSV', # GPS Satellites in view
    'HDT', # Heading, True
    'R00', # List of waypoints in currently active route
    'RMA', # Recommended minimum specific Loran-C data
    'RMB', # Recommended minimum navigation info
    'RMC', # Recommended minimum specific GPS/Transit data
    'RTE', # Routes
    'TRF', # Transit Fix Data
    'STN', # Multiple Data ID
    'VBW', # Dual Ground / Water Speed
    'VTG', # Track made good and ground speed
    'WPL', # Waypoint location
    'XTE', # Cross-track error, Measured
    'ZDA', # Date & Time
]


# Other
UTF8 = 'utf-8'


def is_nmea_sentence(decoded_serial_line):
    if '$' == decoded_serial_line[0]:
        return True
    return False


@contextmanager
def get_serial(port=GPS_TTY, baud=BAUD, timeout=TIMEOUT):
    with serial.Serial(port, baud, timeout=timeout) as ser:
        yield ser


def filter_format_output(sentence, sentence_id_filter):
    if is_nmea_sentence(sentence):
        if not sentence_id_filter:
            print(sentence)
        else:
            talker_sentence_id = f'${GPS_TALKER_ID}{sentence_id_filter}'
            if talker_sentence_id == sentence.split(',')[0]:
                print(sentence)


def read_output(sentence_id_filter):
    with get_serial() as ser:
        i = 0
        while True:
            try:
                gps_line = ser.readline().decode(UTF8).strip('\n')
                filter_format_output(gps_line, sentence_id_filter)
            except UnicodeDecodeError as e:
                print('Could not read serial port. Retrying...')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--sentence_id', dest='sentence_id_filter', choices=GPS_SENTENCE_IDS, help='The NMEA sentence id to parse. If not specified, defaults to all sentences')
    args = parser.parse_args()
    read_output(args.sentence_id_filter)
