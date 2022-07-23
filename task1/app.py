import os
from random import choice

symb1 = "💛"
symb2 = "💔"
number = choice([i for i in range(10,50) if i not in [10,25,50]])

hints = f"""
Number is {'Even' if number%2==0 else 'Odd'}
Number xy where x*y : {int(str(number)[:1])*int(str(number)[1:])}
0 < 10 {'< x <' if 10<number<26<50 else '<'} 25 {'< x <' if 10<26<number<50 else '<'} 50
Divisible by 2 : {'Yes' if number%2==0 else 'No'}
Divisible by 3 : {'Yes' if number%3==0 else 'No'}
"""

hints = [s for s in hints.splitlines() if s]
points = len(hints)*10
idntf = len(hints)
correct = False

os.system("clear")
print("\t\t\t\tWelcome to the game of guessing.")
print("\t\t\t\tGuess the number in {} chances to win the game!\n".format(idntf))
while points>0:
    remaining_chances = int(points/10)
    print(f"\t\t Hint : {hints[idntf-remaining_chances]}")
    inp=input(f"{symb1*remaining_chances}{symb2*(idntf-remaining_chances)}\tInput : ")
    try:
        if not int(inp)==number:
            points-=10
            if points>0:
                print(f"Upps, wrong guess!\n")
            if points==0:
                print(f"\n{symb2*idntf} No lives left hence you lost the game :(\n\nThe number was : {number}")  
        else:
            correct=True
            print("Right guess!\n")
            break
    except ValueError: print("Please enter numericals only!")

if correct:
    print(f"You won with {points}/{idntf*10} points!")
