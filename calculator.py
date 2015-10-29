# calculator.py
#
# All this fun about developing calculator in Python started with one stupid sentence.
# While my yunger son and I waiting for doctor I said that stupid sentence. We were
# waiting in the room crowded by siriusly injured or ill people. After a while
# you realise that waiting can take hours. We start talk about what he currently learning in
# school. After geografy, and some other things we start talk about programming class.
# I have start to explain posible beatuty things that can be don by programming. And,
# enthusisatic, said tha I am also now start to learning python as he. And we start
# to discus what can be easili made ba it. And, in one moment, I said: You can easy build
# calculator! He said: Real one? Me: Off course!! And it started :-)
#
from tkinter import *
from tkinter import ttk

BUTTON_CONTENT_TYPE_COMMAND = 0
BUTTON_CONTENT_TYPE_NUMBER = 1
BUTTON_CONTENT_TYPE_OPERATOR = 2
BUTTON_CONTENT_TYPE_DECIMAL_POINT = 3
BUTTON_CONTENT_TYPE_PARENTHESIS = 4
BUTTON_CONTENT_TYPE_DECIMAL_POINT = 5

class Stack():

    def __init__(self):
        self.stack = []

    def clear(self):
        self.stack.clear()
        
    def addItem(self, item):
        self.stack.append(item)

    def getItem(self):
        if not self.stack:
            return None
        return self.stack.pop()

    def print(self):
        for item in self.stack:
            print('stack -->', item)
        
class NumberStack(Stack):

    def add(self, str_number):
        if '.' in str_number:
            number = float(str_number)
        else:
            number = int(str_number)
        self.addItem(number)

    def get(self):
        return self.getItem()


class OperatorStack(Stack):

    def add(self, operator_type, operator):
        o = []
        o.append(operator_type)
        o.append(operator)
        self.addItem(o)

    def get(self):
        return self.getItem()


class Buffer():

    def __init__(self):
        self.clear()

    def clear(self):    
        self.value = ''
        
    def addChar(self, char):
        self.value += char

    def setValue(self, text):
        self.value = text
            

class CalculatorButton():

    def __init__(self, frame, controller, display_text, content_type, content):
        self.frame = frame
        self.controller = controller
        self.display_text = display_text
        self.content_type = content_type
        self.content = content
        self.button = None

    def iAmPressed(self):
        self.controller.buttonPressed(self)
        
    def makeButton(self):
        self.button = ttk.Button(self.frame,
                                 text=self.display_text,
                                 command=self.iAmPressed)
    
class CalculatorController():

    def __init__(self, display_text):
        # set initial state
        self.state = 'int'
        self.display_text = display_text
        self.setDisplayText()
        self.number_stack = NumberStack()
        self.operator_stack = OperatorStack()
        self.buffer = Buffer()

    def setDisplayText(self, text=''):

        if text == '':
            self.display_text.set('0')
        else:
            self.display_text.set(text)
            
    def calculate(self):
        o = self.operator_stack.get()
        print(o)
        if o:
            b = self.number_stack.get()
            a = self.number_stack.get()
            op = o[1] # OMG!!!
            if op == '+':
                r = a + b
            elif op == '-':
                r = a - b
            elif op == '*':
                r = a * b
            elif op == '/':
                r = a / b
            else:
                r = None
            self.number_stack.add(str(r))
            self.buffer.setValue(str(r))
    
    def buttonPressed(self, cb):
        print(cb.content)

        #
        # finite state machine starts here :-)
        #
        if cb.content_type == BUTTON_CONTENT_TYPE_COMMAND and cb.content == 'CLEAR_ALL':
            self.buffer.clear()
            self.number_stack.clear()
            self.operator_stack.clear()
                
        elif self.state == 'int' and cb.content_type == BUTTON_CONTENT_TYPE_DECIMAL_POINT:
            self.buffer.addChar(cb.content)
            
        elif self.state == 'float' and cb.content_type == BUTTON_CONTENT_TYPE_DECIMAL_POINT:
            print('--- only one decimal point allowed ---')
            
        elif (self.state == 'int' or self.state == 'float') and cb.content_type == BUTTON_CONTENT_TYPE_NUMBER:
            self.buffer.addChar(cb.content)
            
        elif (self.state == 'int' or self.state == 'float') and cb.content_type == BUTTON_CONTENT_TYPE_OPERATOR:
            self.number_stack.add(self.buffer.value)
            self.calculate()
            self.operator_stack.add('operator', cb.content)
            #self.buffer.clear()
            #self.buffer.addChar(cb.content)
            self.state = 'operator'

        elif self.state == 'operator' and cb.content_type == BUTTON_CONTENT_TYPE_NUMBER:
            self.buffer.clear() # shoud be clear or calc -- or cleared allready!!!
            self.buffer.addChar(cb.content)
            self.state = 'number'

        elif cb.content_type == BUTTON_CONTENT_TYPE_COMMAND and cb.content == '=':
            if self.state == 'number':
                self.number_stack.add(self.buffer.value)
                self.calculate()
            elif self.state == 'operator':
                print('what is here?')
            else:
                print('--- funny state ---')
                
        else:
            print('---- Error state ----')

        self.setDisplayText(self.buffer.value)

        self.number_stack.print()
        self.operator_stack.print()
#
calculator_keyboard = [
    [
        [None],
        [None],
        [None],
        ['C', BUTTON_CONTENT_TYPE_COMMAND, 'CLEAR_ALL']
    ], [
        ['1', BUTTON_CONTENT_TYPE_NUMBER, '1'],
        ['2', BUTTON_CONTENT_TYPE_NUMBER, '2'],
        ['3', BUTTON_CONTENT_TYPE_NUMBER, '3'],
        ['/', BUTTON_CONTENT_TYPE_OPERATOR, '/']
    ], [
        ['4', BUTTON_CONTENT_TYPE_NUMBER, '4'],
        ['5', BUTTON_CONTENT_TYPE_NUMBER, '5'],
        ['6', BUTTON_CONTENT_TYPE_NUMBER, '6'],
        ['*', BUTTON_CONTENT_TYPE_OPERATOR, '*']
    ], [
        ['7', BUTTON_CONTENT_TYPE_NUMBER, '7'],
        ['8', BUTTON_CONTENT_TYPE_NUMBER, '8'],
        ['9', BUTTON_CONTENT_TYPE_NUMBER, '9'],
        ['-', BUTTON_CONTENT_TYPE_OPERATOR, '-']
    ], [
        [None],
        ['0', BUTTON_CONTENT_TYPE_NUMBER, '0'],
        ['.', BUTTON_CONTENT_TYPE_DECIMAL_POINT, '.'],
        ['+', BUTTON_CONTENT_TYPE_OPERATOR, '+']
    ], [
        [None],
        [None],
        ['=', BUTTON_CONTENT_TYPE_COMMAND, '='],
        [None]
    ]]

# --- disply setup ---
root = Tk()

display_frame = ttk.Frame(root, borderwidth=5, relief="sunken")
display_frame.grid(row=0, column = 0)

display_text = StringVar()
display_label = ttk.Label(display_frame,
                          width=45,
                          textvariable=display_text)
display_label.grid(row=0, column=0)

calculator_keyboard_frame = ttk.Frame(root)
calculator_keyboard_frame.grid(row=1, column = 0)

# --- 
cc = CalculatorController(display_text)

cb = []
for i in range(len(calculator_keyboard)):
    for j in range(len(calculator_keyboard[i])):
        one_button=calculator_keyboard[i][j]
        print(i, j, len(cb)-1,  one_button[0])
        if one_button[0]:
            cb.append(CalculatorButton(
                calculator_keyboard_frame,
                cc,
                one_button[0],
                one_button[1],
                one_button[2]))
            cb[len(cb)-1].makeButton()
            cb[len(cb)-1].button.grid(row=i, column=j)
    
root.mainloop()

