#!/usr/bin/env python3
# A program that guesses your name, given age and gender
# Meant as a conceptual introduction to data science, in
#  the mold of the binary tree animal-guessing-game
from datetime import date
import os
import pandas as pd

def get_age_input():
    while True:
        print('\nHow many years old are you?')
        line = input(" > ")
        result = parse_age(line)
        if result:
            return result
        print("I did not understand that. Type a number between 1 and 100 and press enter.")

def parse_age(line):
    for token in line.split():
        try:
            years = int(token)
            if years > 1:
                return years
        except ValueError:
            pass
    return None
assert parse_age('10') == 10
assert parse_age('i am 11 years old') == 11
assert parse_age('8 and 6 months') == 8

def get_gender_input():
    while True:
        print('\nAre you a girl or a boy?')
        line = input(" > ")
        result = parse_gender(line)
        if result:
            return result
        print("I did not understand that. Type GIRL or BOY and press enter.")

def parse_gender(line):
    MALE = ['boy', 'b', 'man', 'male', 'm']
    FEMALE = ['girl', 'g', 'woman', 'female', 'f']
    for token in line.lower().split():
        if token in FEMALE:
            return 'female'
        if token in MALE:
            return 'male'
    return None
assert parse_gender('f') == 'female'
assert parse_gender('boy') == 'male'
assert parse_gender('i am a girl') == 'female'
assert parse_gender('im male') == 'male'

def get_yes_no_prompt(msg):
    while True:
        print(msg)
        line = input(" > ")
        result = parse_boolean(line)
        if result is not None:
            return result
        print("I did not understand that. Type YES or NO and press enter.")

def parse_boolean(line):
    TRUE = ['yes', 'y', 'true', '1']
    FALSE = ['no', 'n', 'false', '0']
    for token in line.lower().split():
        if token in TRUE:
            return True
        if token in FALSE:
            return False
    return None
assert parse_boolean('false') == False
assert parse_boolean('  Yes ') == True
assert parse_boolean('NO NO PLEASE NO') == False


def get_birth_year(age, min_year=1880, max_year=2018):
    current_year = date.today().year
    # Adjust to range of applicable census data
    return max(min_year, min(current_year - age, max_year))

def get_names(age, gender, csv_directory='usa_names/'):
    birth_year = get_birth_year(age)
    csv_filenames = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]
    csv_file = os.path.join(csv_directory, '{}.csv'.format(birth_year))
    df = pd.read_csv(csv_file)
    return df['male_name'] if gender == 'male' else df['female_name']


def guess_name(name):
    if get_yes_no_prompt('Is your name {}?'.format(name)):
        print('Your name is {}! Hello {}'.format(name, name))
        exit()


def main():
    age = get_age_input()
    print('You are {} years old'.format(age))
    if age > 100:
        print('Wow, you are very old!')
    gender = get_gender_input()
    print('You are {} years old and your gender is {}'.format(age, gender))

    names = get_names(age, gender)
    does_not_start_with = set()
    for name in names:
        first_letter = name[0]
        if first_letter in does_not_start_with:
            continue
        msg = 'Does your name start with the letter {}?'.format(first_letter)
        if len(does_not_start_with) == 25:
            starts_with = True
        else:
            starts_with = get_yes_no_prompt(msg)
        if starts_with:
            for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                if letter != first_letter:
                    does_not_start_with.add(letter)
            guess_name(name)
        else:
            does_not_start_with.add(first_letter)
    print('I give up! I do not know what your name is.')

if __name__ == '__main__':
    main()
