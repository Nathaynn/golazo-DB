import json
import os

def open_json(path, foo):
    file = open(path, foo)
    return file

def close_json(file):
    file.close()

def gen_player_insert(player_fname, player_lname, player_position, player_age, player_height, player_weight, player_nationality):
    statement = 'INSERT INTO PLAYER (PLAYER_FNAME, PLAYER_LNAME, PLAYER_POSITION, PLAYER_AGE, PLAYER_HEIGHT, PLAYER_WEIGHT, PLAYER_NATIONALITY) VALUES'
    statement += f'({player_fname}, {player_lname}, {player_position}, {int(player_age)}, {int(player_height)}, {int(player_weight)}, {player_nationality})'

def gen_match_insert()