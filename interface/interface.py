# coding=utf-8
"""Here are the functions of the interface.

bye()               Exit from the program.
confirm(question)   Receives an answer to the question.

"""


def bye():
    """Friendly exit from the program."""
    from time import sleep
    print("\nBye!")
    sleep(1)
    print('\033c')  # Clear screen
    exit(0)


def confirm(question: str) -> bool:
    """Gets the user's response and interprets it in a boolean value.

    :param question: string with '?' at the end (for better readability).
    :return: True/False

    """
    try:
        reply = input(f"{question} ").lower()[:1]
        while True:
            if reply in 'yjsd':  # international (yes, ja, si, da); <Enter> also here
                return True
            elif reply == 'n':
                return False
            else:
                reply = input(f"{question} (yjsd/n): ").lower()[:1]
    except (KeyboardInterrupt, EOFError):  # <Ctrl+C>; <Ctrl+D>
        bye()
