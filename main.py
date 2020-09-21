import requests
import json
import random

# response = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/hello')

FILE_PATH = 'definitions.json'

# test = response.status_code
# print(test)

# for word in test:
#     for meaning in word['meanings']:
#         for definition in meaning['definitions']:
#             print(definition['definition'])


# response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
# saved = json.loads(file_path)


class Word:

    @classmethod
    def get_definition(cls, word):
        # check file for word 
        saved_data = File.load_data(FILE_PATH)
        definitions = saved_data.get(word, Word.get_word_from_api(word))
        if definitions:
            for definition in definitions:
                print(f' - {definition}')

    @classmethod
    def get_word_from_api(cls, word):
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        status = Word.check_request(response)
        if status:
            api_vals = json.loads(response.text)
            saved_data = File.load_data(FILE_PATH)
            new_definition = []
            for word_dict in api_vals:
                for meaning in word_dict['meanings']:
                    for definition in meaning['definitions']:
                        new_definition.append(definition['definition'])

            saved_data[word] = new_definition
            File.save_to_file(FILE_PATH, saved_data)
            return new_definition
        else:
            return None

    @classmethod
    def check_request(cls, response):
        status = response.status_code
        if status in range(400, 500):
            print("Word not found.")
            return False
        return True

class File:
    @classmethod
    def save_to_file(cls, file_path, data):
        with open(file_path, 'w') as save_file:
            json_data = json.dumps(data)
            save_file.write(json_data)

    @classmethod
    def load_data(cls, file_path):
        try:
            with open(file_path, 'r') as save_file:
                json_data = json.loads(save_file.read())
                return json_data
        except:
            return {}

class Quiz:
    length = 10

    def __init__(self):
        self.questions = Quiz.generate_questions()
        self.score = 0
        self.current_question = 0

    @classmethod
    def generate_questions(self):
        definitions_dict = File.load_data(FILE_PATH)
        questions = {}
        while len(questions) < self.length:
            answer = random.choice(list(definitions_dict.keys()))
            question = random.choice(definitions_dict[answer])
            if question not in questions:
                questions[question] = answer
        return questions

    def ask_questions(self):
        for question, answer in self.questions.items():
            self.current_question += 1
            user_answer = input(f'Question {self.current_question}: {question}\n')
            if user_answer.lower().strip() == answer.lower():
                self.score += 1
                print(f'Correct!')
            else:
                print(f'The word was {answer}')
        return f'Your score was {self.score}/{self.length}!'
        
    



print("Welcome to an extraordinary world of words!")
while True:
    option = input("Choose an option: \n [1] Word Lookup \n [2] Quiz \n [3] Quit\n")
    if option not in ['1', '2', '3']:
        print("Invalid option.")
    else:
        if option == '1':
            word = input("Input Word: ").lower()
            Word.get_definition(word)
        elif option == '2':
            questions = Quiz()
            print(questions.ask_questions())
        else:
            print("Goodbye.")
            exit()