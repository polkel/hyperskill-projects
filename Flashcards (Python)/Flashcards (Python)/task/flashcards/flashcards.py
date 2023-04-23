import random
import re
import os
import argparse
from io import StringIO


class Flashcards:  # I didn't handle errors in export and import, there's one rogue import error line
    file_names = []
    cli_message = "Input the action (add, remove, import, export, ask, exit," \
                  " log, hardest card, reset stats):\n"
    exit_message = "Bye bye!\n"

    def __init__(self, arguments):
        self.cards = dict()
        self.errors = dict()
        self.logs = StringIO()
        self.args = arguments
        if self.args.import_from:
            self.import_first(self.args.import_from)
        self.start_program()

    def start_program(self):
        user_response = ""
        while user_response != "exit":
            user_response = self.log_input(self.cli_message)
            match user_response:
                case "add":
                    self.add_card()
                case "remove":
                    self.remove_card()
                case "import":
                    self.import_cards()
                case "export":
                    self.export_cards()
                case "ask":
                    self.ask_cards()
                case "hardest card":
                    self.find_hardest()
                case "reset stats":
                    self.erase_errors()
                case "log":
                    self.record_log()
                case "exit":
                    self.log_print(self.exit_message)
                    if self.args.export_to:
                        self.export_last(self.args.export_to)
                    self.logs.close()
                    break

    def add_card(self):
        term = self.log_input("The card:\n")
        while term in self.cards.keys():
            term = self.log_input(f'The card "{term}" already exists. Try again:\n')
        definition = self.log_input("The definition of the card:\n")
        while definition in self.cards.values():
            definition = self.log_input(f'The definition "{definition}" already exists. Try again:\n')
        self.cards[term] = definition
        self.errors[term] = 0
        self.log_print(f'The pair ("{term}":"{definition}") has been added.\n')

    def remove_card(self):
        term = self.log_input("Which card?\n")
        if term in self.cards.keys():
            self.cards.pop(term)
            self.log_print("The card has been removed.\n")
        else:
            self.log_print(f'Can\'t remove "{term}": there is no such card.\n')

    def import_cards(self):
        file_name = self.log_input("File name:\n")
        if file_name not in os.listdir():
            self.log_print("File not found.\n")
        else:
            re_term = "(?<=term: ).*(?=, definition: )"
            re_definition = "(?<=definition: ).*"
            counter = 0
            with open(file_name, "r") as file:
                for line in file.readlines():
                    start, end = re.search(re_term, line).span()
                    term = line[start:end]
                    start, end = re.search(re_definition, line).span()
                    definition = line[start:end]
                    self.cards[term] = definition
                    counter += 1
            self.log_print(f"{str(counter)} cards have been loaded.\n")

    def export_cards(self):
        file_name = self.log_input("File name:\n")
        with open(file_name, "w") as file:
            for term, definition in self.cards.items():
                file.write(f"term: {term}, definition: {definition}\n")
        self.log_print(f"{str(len(self.cards))} cards have been saved.\n")  # does not account for 0 or 1

    def ask_cards(self):  # does not account for an empty list
        n = int(self.log_input("How many times to ask?\n"))
        list_of_cards = list(self.cards.items())
        for _ in range(n):
            card_index = random.randint(0, len(list_of_cards) - 1)
            term, definition = list_of_cards[card_index]
            answer = self.log_input(f'Print the definition of "{term}":\n')
            if answer == definition:
                self.log_print("Correct!")
            elif answer not in self.cards.values():
                self.log_print(f'Wrong. The right answer is "{definition}".')
                self.errors[term] += 1
            else:
                key_index = list(self.cards.values()).index(answer)
                key = list_of_cards[key_index][0]
                self.log_print(f'Wrong. The right answer is "{definition}", '
                               f'but your definition is correct for "{key}".\n')
                self.errors[term] += 1

    def log_print(self, message):
        self.logs.write(message)
        print(message)

    def log_input(self, message):
        self.logs.write(message)
        user_input = input(message)
        self.logs.write("".join([user_input, "\n"]))
        return user_input

    def find_hardest(self):  # does not check if there are no terms
        error_values = list(self.errors.values())
        if not error_values:
            self.log_print("There are no cards with errors.\n")
            return
        max_errors = max(error_values)
        if not max_errors:
            self.log_print("There are no cards with errors.\n")
        else:
            max_count = error_values.count(max_errors)
            errors_list = []
            start_index = 0
            terms = list(self.errors.keys())
            while max_count:
                term_index = error_values.index(max_errors, start_index)
                errors_list.append(terms[term_index])
                start_index = term_index + 1
                max_count -= 1
            if len(errors_list) > 1:
                first_verb = "cards are"
                last_pronoun = "them"
            else:
                first_verb = "card is"
                last_pronoun = "it"
            terms_string = ""
            for term in errors_list[:-1]:
                terms_string = "".join([terms_string, f'"{term}", '])
            terms_string = "".join([terms_string, f'"{errors_list[-1]}"'])
            self.log_print(f"The hardest {first_verb} {terms_string}. You have"
                           f" {str(max_errors)} errors answering {last_pronoun}.\n")

    def erase_errors(self):
        for key in self.errors.keys():
            self.errors[key] = 0
        self.log_print("Card statistics have been reset.\n")

    def record_log(self):
        file_name = self.log_input("File name:\n")
        with open(file_name, "w") as file:
            file.write(self.logs.getvalue())
        self.log_print("The log has been saved.\n")

    def import_first(self, file_name):
        if file_name in os.listdir():
            re_term = "(?<=term: ).*(?=, definition: )"
            re_definition = "(?<=definition: ).*"
            counter = 0
            with open(file_name, "r") as file:
                for line in file.readlines():
                    start, end = re.search(re_term, line).span()
                    term = line[start:end]
                    start, end = re.search(re_definition, line).span()
                    definition = line[start:end]
                    self.cards[term] = definition
                    self.errors[term] = 0  # i'm sick of this
                    counter += 1
            self.log_print(f"{str(counter)} cards have been loaded.\n")

    def export_last(self, file_name):
        with open(file_name, "w") as file:
            for term, definition in self.cards.items():
                file.write(f"term: {term}, definition: {definition}\n")
        self.log_print(f"{str(len(self.cards))} cards have been saved.\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flashcards CLI app")
    parser.add_argument("--import_from")
    parser.add_argument("--export_to")
    args = parser.parse_args()
    my_flashcards = Flashcards(args)
