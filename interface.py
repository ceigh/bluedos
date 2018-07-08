# coding=utf-8
"""Simple interface module.

Simple functions are placed in a separate module
so as not to contaminate the main program.

bye()               Exit from the program.
confirm(question)   Receives an answer to the question.

"""


def bye():
    """Friendly exit from the program."""
    from time import sleep
    print("\nBye!")
    sleep(0.8)
    print('\033c')  # Clear screen


def confirm(question: str) -> bool:
    """Gets the user's response and interprets it in a boolean value.

    :param question: string with '?' at the end (for readability).
    :return: True/False

    """
    try:
        reply = input(f"{question}: ").lower()[:1]
        while True:
            if reply in 'yjsd':  # (yes, ja, si, da); <Enter> also here
                return True
            elif reply == 'n':
                return False
            else:
                reply = input(f"{question} (yjsd/n): ").lower()[:1]
    except (KeyboardInterrupt, EOFError):  # <Ctrl+C>; <Ctrl+D>
        bye()
