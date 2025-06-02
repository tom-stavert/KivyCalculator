import kivy
import re
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('calculator.kv')

class MyLayout(Widget):
    
    display = ObjectProperty()

    nums = ['1','2','3','4','5','6','7','8','9','0']
    symbols = ['+','-','*','/','.']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display.text = ''

    def press(self, button):
        if button in self.nums:
            self.display.text = self.display.text + button
        elif button in self.symbols:
            # if the last entry was a symbol replace instead of adding on
            if self.display.text[-1] in self.symbols:
                self.display.text = self.display.text[0:-1] + button
            else:
                self.display.text = self.display.text + button

    def calculate(self):
        numbers = re.split(r'\+|\-|\*|\/', self.display.text)
        operations = re.findall(r'\+|\-|\*|\/', self.display.text)
        numbers = [float(i) for i in numbers]
        print(numbers, operations) 

        # Brute force approach for order of operations
        while operations.count('/') + operations.count('*') > 0:
            for n, o in enumerate(operations):
                if o == '/':
                    x = numbers[n]/numbers[n+1]
                    numbers[n] = x
                    numbers.pop(n+1)
                    operations.pop(n)
                elif o == '*':
                    x = numbers[n]*numbers[n+1]
                    numbers[n] = x
                    numbers.pop(n+1)
                    operations.pop(n)

        while len(operations) > 0:
            for n, o in enumerate(operations):
                if o == '+':
                    print(numbers, operations)
                    x = numbers[n]+numbers[n+1]
                    numbers[n] = x
                    numbers.pop(n+1)
                    operations.pop(n)
                elif o == '-':
                    x = numbers[n]+numbers[n+1]
                    numbers[n] = x
                    numbers.pop(n+1)
                    operations.pop(n)

        result = round(numbers[0],10)
        if result.is_integer():
            result = int(result)
        self.display.text = str(result)

    def clear_everything(self):
        if self.display.text == '':
            pass
        else:
            self.display.text = ''

    def clear_entry(self):
        if self.display.text == '':
            pass
        elif self.display.text[-1] in (['+','-','*','/',]):
            pass
        else:
            self.display.text = self.display.text[:-len(re.search(r'[0-9]+',self.display.text[::-1]).group())]
        

    def backspace(self):
        if self.display.text == '':
            pass
        else:
            self.display.text = self.display.text[:-1]

class Calculator(App):
    def build(self):
        return MyLayout()
    

    
if __name__ == '__main__':
    Calculator().run()