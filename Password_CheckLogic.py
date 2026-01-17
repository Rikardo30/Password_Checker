import random
import string

def display_welcome_message():
    return (
        "==============================================\n"
        "|      Welcome to Password Void Checker      |\n"
        "==============================================\n"
        "                                              \n"
        "    This tools purpose is to test, create,    \n"
        "           and store your password            \n"
        "                                              \n"
    )

# The following function checks the strength of the password based on defined criteria.
def check_password_strength(password):
    strength_criteria = {
        'length': len(password) >= 8,
        'integers': sum(char.isdigit() for char in password) >= 2,
        'uppercase': sum(char.isupper() for char in password) >= 2,
        'special characters': any(char in '!@#$%^&*()-_=+,.' for char in password),
    }

    if all(strength_criteria.values()):
        return "Strong"
    if sum(strength_criteria.values()) >= 2:
        return "Moderate"
    return "Weak"

# The following function provides suggestions to improve password strength.
def strength_suggestions(password):
    suggestions = []

    if len(password) < 8:
        suggestions.append("Use at least 8 characters")

    if sum(char.isdigit() for char in password) < 2:
        suggestions.append("Include at least 2 integers")

    if sum(char.isupper() for char in password) < 2:
        suggestions.append("Include at least 2 uppercase letters")

    if not any(char in '!@#$%^&*()-_=+,.' for char in password):
        suggestions.append("Add at least 1 special character such as !@#$%^&*()-_=+,")

    if check_password_strength(password) == "Strong":
        suggestions.append("Your password is strong. No suggestions needed.")
    return suggestions

# The following function provides a randomized stronger password.
def randomize_improvement(password):
    add_words = [
        "EMBER", "QUARTZ", "RAVEN", "BLAZING", "ORBIT", "FROST", "THORN", "NOVA",
        "TITAN", "BRIGHT", "VORTEX", "SCARY", "STRONG", "ASTRO", "LYRIC", "BRINK",
        "ONYX", "MIRAGE", "STRIKE", "PHANTOM", "ECHO", "FLARE", "SPARK", "QUILL",
        "HAVOC", "TEMPEST", "SOLAR", "SHINING", "SHADOW", "RELIC",
    ]

    # Separate letters and numbers
    letters = "".join(char for char in password if char.isalpha())
    numbers = "".join(char for char in password if char.isdigit())

    # If no numbers exist, add two random numbers
    if numbers == "":
        numbers = "".join(random.choices(string.digits, k=2))
    else:
        numbers = "".join(reversed(numbers))

    # Pick a random word and build the final strengthened password
    word = random.choice(add_words)
    stronger = f"{word}_{letters}{numbers}"
    return stronger