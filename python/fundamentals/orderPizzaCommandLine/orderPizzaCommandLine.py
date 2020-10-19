from __future__ import print_function, unicode_literals

from pathlib import Path
pathToThisPythonFile = Path(__file__).resolve()
import sys

from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint as p
import time

def mainFunction(arrayOfArguments):

    styleObj = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',  # default
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })

    # p(type(p))

    def validateAnswer(answer):
        if len(answer) == 0:
            p(1)
            return 'You must choose at least one topping.'
        else:
            p(2)
            return True

    arrayOfQuestions = [
        {
            'type': 'checkbox',
            'message': 'Select toppings',
            'name': 'toppings',
            'choices': [
                Separator('= The Meats ='),
                {
                    'name': 'Ham'
                },
                {
                    'name': 'Ground Meat'
                },
                {
                    'name': 'Bacon'
                },
                Separator('= The Cheeses ='),
                {
                    'name': 'Mozzarella',
                    'checked': True
                },
                {
                    'name': 'Cheddar'
                },
                {
                    'name': 'Parmesan'
                },
                Separator('= The usual ='),
                {
                    'name': 'Mushroom'
                },
                {
                    'name': 'Tomato'
                },
                {
                    'name': 'Pepperoni'
                },
                Separator('= The extras ='),
                {
                    'name': 'Pineapple'
                },
                {
                    'name': 'Olives',
                    'disabled': 'out of stock'
                },
                {
                    'name': 'Extra cheese'
                }
            ],
            'validate': validateAnswer
        }
    ]

    for i in range(0, 1):

        selectedOptionsObj = prompt(arrayOfQuestions, style=styleObj)
        # time.sleep(2)
    # p(selectedOptionsObj)



if __name__ == '__main__':
    p(str(pathToThisPythonFile.name) + ' is not being imported. It is being run directly...')
    mainFunction(sys.argv)
else:
	p(str(pathToThisPythonFile.name) + ' is being imported. It is not being run directly...')


