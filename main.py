import json
import requests


instructions = "Welcome to the CowBull game. The objective of this game is to guess " \
               "a set of four digits (numbers between 0 and 9) by entering a sequence " \
               "of numbers. Each time you try to guess, you will see an analysis of " \
               "your guesses: * is a bull (the right number in the right place), - (" \
               "the right number in the wrong place), x is a miss, and any of the other " \
               "symbols followed with + means that the number occurs more than once."

print()
print(instructions)
print()
while True:
    answer = input("Do you want to play? (Yes/No) ")
    if answer.lower() in ['yes', 'y', 'no', 'n']:
        break

print()
print('Requesting a new game.')
r = requests.get("http://localhost:5000/v0_1/game")
try:
    game_data = r.json()
except ValueError as ve:
    print()
    print('Well! This is embarrasing. But for some reason there was no response: {}'.format(str(ve)))

game_key = game_data["key"]

print("Starting a new game. You have {} goes to guess {} digits".format(game_data["guesses"], game_data["digits"]))

headers = {
    "content-type": "application/json"
}
while True:
    guesses = []
    number = 0
    while number < game_data["digits"]:
        temp_number = input("Enter number {}: ".format(number+1))
        try:
            temp_number = int(temp_number)
            if temp_number < 0 or temp_number > 9:
                raise ValueError()
            guesses.append(temp_number)
            number += 1
        except ValueError:
            print("You need to enter a number between 0 and 9")
    payload = {
        "key": game_key,
        "digits": guesses
    }
    r = requests.post(url="http://localhost:5000/v0_1/game", json=payload, headers=headers)
    try:
        response_data = r.json()
    except ValueError as ve:
        print("Something isn't working! {}".format(str(ve)))
        break

    game_info = response_data.get("game", {})
    status = game_info.get("status", None)

    if status.lower() in ["lost", "won"]:
        print()
        analysis = response_data.get("outcome", {})
        print("{}".format(analysis["message"]))
        break

    game_analysis = response_data.get("outcome", {})

    header_string = "{} {} {} {}".format(*guesses)
    uline_string = "--------"
    output_string = ""

    for analysis_record in game_analysis["analysis"]:
        if analysis_record["match"]:
            output_string += "*"
        elif analysis_record["in_word"]:
            output_string += "-"
        else:
            output_string += "x"

        if analysis_record["multiple"]:
            output_string += "+"
        else:
            output_string += " "
    print()
    print("You have {} bulls and {} cows.".format(game_analysis["bulls"], game_analysis["cows"]))
    print()
    print("{}".format(header_string))
    print("{}".format(uline_string))
    print("{}".format(output_string))
    print()
print()
