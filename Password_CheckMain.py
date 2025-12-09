## This project will be a simple password security checker 
## That will evaluate the strength of a password based on certain criteria.
import random
import string
import colorama
from colorama import Fore
colorama.init(autoreset=True)

## The following function serves as an introduction to the password checker tool.
def print_welcome_message():
    print("***************************************")
    print("*     Welcome to Password Checker     *")
    print("***************************************")
    print("This tool will help you evaluate the strength of your password.")
    print("Let's get started!")
    print("***************************************")

## The following function checks the strength of the password based on defined criteria.
def check_password_strength(password):
    strength_criteria = {
        'length': len(password) >= 8,
        'integers': sum(char.isdigit() for char in password) >= 2,
        'uppercase': sum(char.isupper() for char in password) >= 2,
        'special characters': any(char in '!@#$%^&*()-_=+,.' for char in password)
    }
    if all(strength_criteria.values()):
        return (Fore.GREEN + "Strong")
    if sum(strength_criteria.values()) >= 2:
        return (Fore.YELLOW + "Moderate")
    return (Fore.RED + "Weak")

## The following function provides suggestions to improve password strength.
def strength_suggestions(password):
    suggestions = []
    if len(password) < 8:
        suggestions.append("Use at least 8 characters.")
    if sum(char.isdigit() for char in password) < 2:
        suggestions.append("Include at least 2 integers.")
    if sum(char.isupper() for char in password) < 2:
        suggestions.append("Include at least 2 uppercase letters.")
    if not any(char in '!@#$%^&*()-_=+,.' for char in password):
        suggestions.append("Add at least 1 special character such as !@#$%^&*()-_=+,.")
    return suggestions

## The following function asks and provides random suggestions to improve password strength. WORK IN PROGRESS
def randomize_improvement(password):
    add_words = ["EMBER", "QUARTZ", "RAVEN", "BLAZING", "ORBIT", "FROST", "THORN", "NOVA", "TITAN", "BRIGHT", 
                 "VORTEX", "SCARY", "STRONG", "ASTRO", "LYRIC", "BRINK", "ONYX", "MIRAGE", "STRIKE", "PHANTOM", 
                 "ECHO", "FLARE", "SPARK", "QUILL", "HAVOC", "TEMPEST", "SOLAR", "SHINING", "SHADOW", "RELIC"]
## Sepperate the characters in to two categories, numbers and letters.
    letters = "".join([char for char in password if char.isalpha()])
    numbers = "".join([char for char in password if char.isdigit()])
## If no numbers exist, add two random numbers
    if numbers == "":
        numbers = "".join(random.choices(string.digits, k=2))
## if two numbers exist, flip them
    else:
        numbers = "".join(reversed(numbers))
## if the input only contains one word, add a random word from list
    word = random.choice(add_words)
## Build the final strengthened password
    stronger = f'{word}_{letters}{numbers}'
    return stronger

def main():
## Prints welcome message
    print_welcome_message()      
## Main execution flow (Displays the code in action)
    print("***************************************")
    input_password = input("Enter a password to check its strength:")
    result = check_password_strength(input_password)
    print (f"Password Strength: {result}")
## If the password provided was not strong, the following prompt will appear with reccomendations
    if result != (Fore.GREEN + "Strong"):
        print("Suggestions to improve your password:")
    for suggestion in strength_suggestions(input_password):
        print(f"- {suggestion}")
## The following code will ask the user if they would like a stronger password to be generated for them
    valid_responses = ['yes', 'YES', 'Yes', 'Y', 'y']
    print("                                                      ")
    print("******************************************************")
    password_question = input("Would you like me to generate a stronger password? Y/N ")
    if password_question in valid_responses:
        print("OK!")
        stronger_password = randomize_improvement(input_password)
        print(f"Suggested Stronger Password: {stronger_password}")
    else:
        print("No problem! Stay safe")
if __name__ == "__main__":
    main()