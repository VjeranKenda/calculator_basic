#
# calculator.py -- on standby
#
# Vjeran Kenda
# ------------------------------------------------------------------------------
# 2015     : initial version
# 20151029 : upload to Git
#
from tkinter import *
from tkinter import ttk

BUTTON_CONTENT_TYPE_COMMAND = 0
BUTTON_CONTENT_TYPE_NUMBER = 1
BUTTON_CONTENT_TYPE_OPERATOR_1 = 2
BUTTON_CONTENT_TYPE_OPERATOR_2 = 3
BUTTON_CONTENT_TYPE_DECIMAL_POINT = 4
BUTTON_CONTENT_TYPE_PARENTHESIS = 5
BUTTON_CONTENT_TYPE_DECIMAL_POINT = 6

def string_number_type_is_float(s):
    if '.' in s:
        return True
    return False
    
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

        
class NumberStack(Stack):

    def add(self, str_number):
        if string_number_type_is_float(str_number):
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
        # connection : GUI --> controller
        self.controller.buttonPressed(self)
        
    def makeButton(self):
        self.button = ttk.Button(self.frame,
                                 text=self.display_text,
                                 # setup of conection : GUI --> controller
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

    def clearAll(self):
            self.buffer.clear()
            self.number_stack.clear()
            self.operator_stack.clear()
            self.state = 'int'
        
    def calculate(self):
        o = self.operator_stack.get()
        # -- print for debug
        #print(o)
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
        #
        # finite state machine should start here :-)
        #
        # state : int : float : operator
        #--------------------------------
        # num   : int : float : int
        # dot   : float: err : float (add 0 on display)
        # oper  : calc : calc : ?  <--- nacrtaj
        # 
        if cb.content_type == BUTTON_CONTENT_TYPE_COMMAND and cb.content == 'CLEAR_ALL':
            self.clearAll()
                
        elif self.state == 'int' and \
             cb.content_type == BUTTON_CONTENT_TYPE_DECIMAL_POINT:
            self.buffer.addChar(cb.content)
            
        elif self.state == 'float' and \
             cb.content_type == BUTTON_CONTENT_TYPE_DECIMAL_POINT:
            # here must go to error state
            print('--- only one decimal point allowed ---')
            
        elif (self.state == 'int' or self.state == 'float') and \
             cb.content_type == BUTTON_CONTENT_TYPE_NUMBER:
            self.buffer.addChar(cb.content)
            
        elif (self.state == 'int' or self.state == 'float') and \
             (cb.content_type == BUTTON_CONTENT_TYPE_OPERATOR_1 or \
              cb.content_type == BUTTON_CONTENT_TYPE_OPERATOR_2):
            self.number_stack.add(self.buffer.value)
            self.calculate()
            self.operator_stack.add(cb.content_type, cb.content)
            #self.buffer.clear()
            #self.buffer.addChar(cb.content)
            self.state = 'operator'

        elif self.state == 'operator' and \
             cb.content_type == BUTTON_CONTENT_TYPE_NUMBER:
            self.buffer.clear() # shoud be clear or calc -- or cleared allready!!!
            self.buffer.addChar(cb.content)
            self.state = 'int'

        elif cb.content_type == BUTTON_CONTENT_TYPE_COMMAND and cb.content == '=':
            if (self.state == 'int' or self.state == 'float'):
                self.number_stack.add(self.buffer.value)
                self.calculate()
                b = self.buffer.value
                self.clearAll()
                # set back calculated number
                self.number_stack.add(b)
                self.buffer.setValue(b)
                if string_number_type_is_float(b):
                    self.state = 'float'
                else:
                    self.state = 'int'                
                
            elif self.state == 'operator':
                #-- to be implemented
                print('what is here? fancy functionality of common calc!')
            else:
                print('--- funny state ---')
                
        else:
            # oprator after operator
            print('---- Error state ----')

        self.setDisplayText(self.buffer.value)

# --- definition of display ---
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
        ['/', BUTTON_CONTENT_TYPE_OPERATOR_2, '/']
    ], [
        ['4', BUTTON_CONTENT_TYPE_NUMBER, '4'],
        ['5', BUTTON_CONTENT_TYPE_NUMBER, '5'],
        ['6', BUTTON_CONTENT_TYPE_NUMBER, '6'],
        ['*', BUTTON_CONTENT_TYPE_OPERATOR_2, '*']
    ], [
        ['7', BUTTON_CONTENT_TYPE_NUMBER, '7'],
        ['8', BUTTON_CONTENT_TYPE_NUMBER, '8'],
        ['9', BUTTON_CONTENT_TYPE_NUMBER, '9'],
        ['-', BUTTON_CONTENT_TYPE_OPERATOR_1, '-']
    ], [
        [None],
        ['0', BUTTON_CONTENT_TYPE_NUMBER, '0'],
        ['.', BUTTON_CONTENT_TYPE_DECIMAL_POINT, '.'],
        ['+', BUTTON_CONTENT_TYPE_OPERATOR_1, '+']
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
        #--- print for debug only
        # print(i, j, len(cb)-1,  one_button[0])
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

