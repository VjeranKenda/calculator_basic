#
# calculator_basic_simple.py
#
# Vjeran Kenda
# ------------------------------------------------------------------------------
# 2015     : initial version - very simple calculator
# 20151029 : upload to Git
# 20151109 : working model
#
from tkinter import *
from tkinter import ttk

BUTTON_CONTENT_TYPE_COMMAND = 0
BUTTON_CONTENT_TYPE_NUMBER = 1
BUTTON_CONTENT_TYPE_OPERATOR = 2
BUTTON_CONTENT_TYPE_DECIMAL_POINT = 4
BUTTON_CONTENT_TYPE_PARENTHESIS = 5
BUTTON_CONTENT_TYPE_DECIMAL_POINT = 6

def string_number_type_is_float(s):
    if '.' in s:
        return True
    return False
    
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
        self.state = 'int'
        self.display_text = display_text
        self.setDisplayText()
        self.buffer = Buffer()

        self.number_register = []
        self.operator_register = []
        
    def setDisplayText(self, text=''):

        if text == '':
            self.display_text.set('0')
        else:
            self.display_text.set(text)

    def clearAll(self):
            self.buffer.clear()
            self.state = 'int'
            self.number_register = []
            self.operator_register = []

    def append_number_to_number_register(self):

        if self.buffer.value == '':
            # Nothing to do? Is this lefover of some old design?
            return
        
        if string_number_type_is_float(self.buffer.value):
            self.number_register.append(float(self.buffer.value))
        else:
            self.number_register.append(int(self.buffer.value))
        #
        # clear buffer here?
        #

    def calculate(self, finish_calculation):

        if finish_calculation:
            # get last operator
            i = -1
        else:
            # get second last operator
            i = -2
        operator = self.operator_register.pop(i)[1] # OMG!!! Discusting!

        b = self.number_register.pop()
        a = self.number_register.pop()

        # operation error exceptions should be here
        if operator == '+':
            r = a + b
        elif operator == '-':
            r = a - b
        elif operator == '*':
            r = a * b
        elif operator == '/':
            # here shold be error checking for division by 0
            r = a / b
        else:
            # maybe here inform that something is wrong ?
            r = None

        return r

    def calculate_loop(self, finish_calculation=False):

        # multiple equal command pressed test (when there is no operators left)
        if len(self.operator_register) > 0:
            #
            # push number to number_register
            #
            self.append_number_to_number_register()

        #
        # calculate if needed
        #
        while len(self.number_register) > 1 :
            # Two or more numbers on stack. Try to do calculation.
            if not finish_calculation and len(self.operator_register) > 1:
                # At least two operators on stack.
                # Compare last and second last for greater precedence.
                go_with_calculation = self.operator_register[-1][0] \
                                      <= self.operator_register[-2][0]
            elif len(self.operator_register) == 0 :
                # no more operators
                go_with_calculation = False
            else:
                # Only one operator or equal command. Go with calculation.
                go_with_calculation = True
                
            if go_with_calculation:
                # calculate <-- num[n-1] (op) num[n]
                # and
                # set result in buffer
                self.buffer.setValue(str(self.calculate(finish_calculation)))
                if len(self.operator_register) > 0:
                    # Store result because more operators waiting.
                    self.append_number_to_number_register()
            else:
                # higher operator precedence --> do not calculate
                break
            
    def buttonPressed(self, cb):

        #
        # command processing
        #
        if cb.content_type == BUTTON_CONTENT_TYPE_COMMAND and cb.content == 'CLEAR_ALL':
            self.clearAll()

        elif cb.content_type == BUTTON_CONTENT_TYPE_COMMAND and cb.content == '=':
            if (self.state == 'int' or self.state == 'float'):

                self.calculate_loop(True)

                # set back calculated number state
                if string_number_type_is_float(self.buffer.value):
                    self.state = 'float'
                else:
                    self.state = 'int'

            elif self.state == 'operator':
                #-- to be implemented
                print('what here should be? fancy functionality of common calc!')
            else:
                print('--- funny state ---')
                
        # number processing        
        elif (self.state == 'int' or self.state == 'float') and \
             cb.content_type == BUTTON_CONTENT_TYPE_NUMBER:
            self.buffer.addChar(cb.content)
            
        elif self.state == 'int' and \
             cb.content_type == BUTTON_CONTENT_TYPE_DECIMAL_POINT:
            self.buffer.addChar(cb.content)
            self.state = 'float'
            
        elif self.state == 'float' and \
             cb.content_type == BUTTON_CONTENT_TYPE_DECIMAL_POINT:
            self.state = 'error'
            print('--- only one decimal point allowed ---')

        # operator processing
        elif self.state == 'operator' and \
             cb.content_type == BUTTON_CONTENT_TYPE_OPERATOR:
            self.state = 'error'
            print('--- only one operator in line ---')

        elif self.state == 'operator' and \
             cb.content_type == BUTTON_CONTENT_TYPE_NUMBER:
            self.state = 'int'
            self.buffer.setValue(cb.content)

        elif self.state == 'operator' and \
             cb.content_type == BUTTON_CONTENT_TYPE_DECIMAL_POINT:
            self.state = 'float'
            self.buffer.setValue('0' + cb.content)

        elif (self.state == 'int' or self.state == 'float') and \
             cb.content_type == BUTTON_CONTENT_TYPE_OPERATOR:
            #
            # push operator to operator_register
            #
            if cb.content in ('+', '-'):
                self.operator_register.append([1, cb.content])
            else:
                self.operator_register.append([2, cb.content])

            #
            # calculate if needed
            #
            self.calculate_loop()

            self.state = 'operator'

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
        ['.', BUTTON_CONTENT_TYPE_DECIMAL_POINT, '.'],
        ['0', BUTTON_CONTENT_TYPE_NUMBER, '0'],
        ['=', BUTTON_CONTENT_TYPE_COMMAND, '='],
        ['+', BUTTON_CONTENT_TYPE_OPERATOR, '+']
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

