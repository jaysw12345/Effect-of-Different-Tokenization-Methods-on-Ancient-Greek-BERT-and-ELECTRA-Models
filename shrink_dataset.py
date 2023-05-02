import random

def main():

    # Open the input file
    with open('50k-Wordpiece/50k_wordpiece.txt', 'r') as f:
        # Read the entire file and store it as a string
        text = f.read()

    # Split the string into a list of units, with each unit being a string between newline characters
    units = text.split('\n')

    # Shuffle the list of units randomly
    random.shuffle(units)

    # Calculate the number of units to keep, which is 1/3 of the total number of units
    num_units_to_keep = len(units) // 1000

    # Take the first num_units_to_keep units and store them in a new list
    units_to_keep = units[:num_units_to_keep]

    # Join the list of units back into a string, with newline characters separating each unit
    output_text = '\n'.join(units_to_keep)

    # Open the output file and write the output text to it
    with open('super_mini_wordpiece.txt', 'w') as f:
        f.write(output_text)

if __name__ == '__main__':
    main()