
# Imports
from __future__ import print_function
# Main #


def main():
    # Main Code
    # Create Deck of Cards
    v_deck = f_CreateDeck()  # Create deck of cards.
    print("DEBUG", "Deck")  # DEBUG
    f_PrintDeck(v_deck)  # DEBUG


def f_CreateDeck():
    """Creates the card deck of 13 cards, 2 > A, of each of 4 suits
        None, Return(string list)"""
    v_deck = []  # Init deck variable
    for i in ["\u2663", "\u2660", "\u2666", "\u2665"]:  # Each suit: Clubs, Spades, Diamonds, Hearts
        for j in range(2, 11):  # Numbered cards
            v_deck.append('{:>2}'.format(j) + str(i))  # Append each number to a suit
        for j in ("J", "Q", "K", "A"):  # Face cards
            v_deck.append(i + str(j))  # Append each face card to a suit
    return v_deck
    # DEBUG PRINT DECK OF CARDS


def f_PrintDeck(v_deck):
    v_row_count, v_card_count = 0, 0  # Init row count, and card count
    v_len_line = 13  # Init typical line length
    v_num_lines, v_len_last_line = divmod(len(v_deck), v_len_line)  # Get this deck's computed num of lines, and the length of the last line
    for i in range(0, (v_num_lines + 1)):
        if v_row_count == v_num_lines:  # If at last line change length of line to computed value of last line
            v_len_line = v_len_last_line
        for j in range(v_len_line):  # Run through printing each value to max of line length
            if v_deck[v_card_count][-1:] in ["\u2666", "\u2665"]:
                print("\033[1;31;48m" + v_deck[v_card_count], end="\033[1;37;0m,")
            else:
                print("\033[1;30;48m" + v_deck[v_card_count], end="\033[1;37;0m,")
            v_card_count += 1  # Increment card count
        print()  # Advance to next line
        v_row_count += 1  # Increment row
    return


main()
