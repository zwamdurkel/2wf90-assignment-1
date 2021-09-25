import asn1tools as asn
import json

### AfS software assignment 1 ###

# set file names
base_location = './'
ops_loc = base_location + 'operations.asn'
exs_loc = base_location + 'input.ops'
ans_loc = base_location + 'output.ops'

# ###### Creating an exercise list file ######

# # How to create an exercise JSON file containing one addition exercise
# exercises = {'exercises' : []}                                     # initialize empty exercise list
# ex = {'add' : {'radix' : 10, 'x' : '3', 'y' : '4', 'answer' : ''}} # create add exercise
# exercises['exercises'].append(ex)                                  # add exercise to list

# # Encode exercise list and print to file
# my_file = open(exs_loc, 'wb+')                                     # write to binary file
# my_file.write(json.dumps(exercises).encode())                      # add encoded exercise list
# my_file.close()

###### Using an exercise list file ######

# Compile specification
spec = asn.compile_files(ops_loc, codec="jer")

# Read exercise list
# open binary file
exercise_file = open(exs_loc, 'rb')
# read byte array
file_data = exercise_file.read()
# decode after specification
my_exercises = spec.decode('Exercises', file_data)
exercise_file.close()

# Create answer JSON
my_answers = {'exercises': []}


def numberToArray(number, base):
    # Will convert a number to an array of digits. first element = radix^0, 2nd = radix^1, etc

    array = []

    for i in range(len(number)):
        if number[-i - 1] == '-':
            array.append('-')
        else:
            array.append(int(number[-i - 1], base=base))

    return array


def arrayToNumber(array):
    # Will convert array to number as string with 0-9a-f as digits

    number = ''

    # Convert digit to proper string representation
    for digit in array:
        if digit == '-':
            number = '-' + number
            break
        if digit < 10:
            number = str(digit) + number
        if digit >= 10:
            number = chr(ord('a')+digit-10) + number

    return number


def arrayAdd(x, y, base):
    # Adds numbers in array representation with variable base

    negativeX = False
    negativeY = False

    if x[-1] == '-':
        x.pop()
        negativeX = True
    if y[-1] == '-':
        y.pop()
        negativeY = True

    # Get max size to fill rest with zeros
    size = max(len(x), len(y))
    # Extend numbers with trailing 0 (doesn't change value)
    x += [0] * (size - len(x))
    y += [0] * (size - len(y))

    # If both numbers are negative
    if negativeX and negativeY:
        answer = arrayAdd(x, y, base)
        answer.append('-')
        return answer

    # If x is negative
    if negativeX:
        if x[-1] > y[-1]:
            answer = arraySub(x, y, base)
            answer.append('-')
            return answer
        else:
            answer = arraySub(y, x, base)
            return answer

    # If y is negative
    if negativeY:
        if x[-1] < y[-1]:
            answer = arraySub(y, x, base)
            answer.append('-')
            return answer
        else:
            answer = arraySub(x, y, base)
            return answer

    # Else...

    # Prepare empty carry and answer array
    answer = []
    carry = 0

    # Do digit wise addition (and carry)
    for i in range(size):
        answer.append(x[i] + y[i] + carry)
        carry = 0

        if answer[i] >= base:
            answer[i] -= base
            carry = 1

    if carry == 1:
        answer.append(1)

    # Remove trailing 0
    while answer[-1] == 0 and answer != [0]:
        answer.pop()

    return answer


def arraySub(x, y, base):
    # Subtracts numbers in array representation with variable base

    negativeX = False
    negativeY = False

    if x[-1] == '-':
        x.pop()
        negativeX = True
    if y[-1] == '-':
        y.pop()
        negativeY = True

    # Get max size to fill rest with zeros
    size = max(len(x), len(y))
    # Extend numbers with trailing 0 (doesn't change value)
    y += [0] * (size - len(y))
    x += [0] * (size - len(x))

    # If both numbers are negative
    if negativeX and negativeY:
        if x[-1] > y[-1]:
            answer = arraySub(x, y, base)
            answer.append('-')
            return answer
        else:
            answer = arraySub(y, x, base)
            return answer

    # If x is negative
    if negativeX:
        answer = arrayAdd(x, y, base)
        answer.append('-')
        return answer

    # If y is negative
    if negativeY:
        answer = arrayAdd(x, y, base)
        return answer

    # If x is smaller than y
    if x[-1] < y[-1]:
        answer = arraySub(y, x, base)
        answer.append('-')
        return answer

    # Else...

    # Prepare empty carry and answer array
    answer = []
    carry = 0

    for i in range(size):
        answer.append(x[i] - y[i] - carry)
        carry = 0

        if answer[i] < 0:
            answer[i] += base
            carry = 1

    # Remove trailing 0
    while answer[-1] == 0 and answer != [0]:
        answer.pop()

    return answer


# Loop over exercises and solve
for exercise in my_exercises['exercises']:
    # get operation type
    operation = exercise[0]
    # get parameters
    params = exercise[1]

    print(f'Running exercise:\n{exercise}')

    if operation == 'add':
        ### Do addition ###

        # Convert to array to handle more easily
        x = numberToArray(params['x'], params['radix'])
        y = numberToArray(params['y'], params['radix'])

        params['answer'] = arrayToNumber(arrayAdd(x, y, params['radix']))
        print(f"Answer: {params['answer']}")

    if operation == 'subtract':
        ### Do subtraction ###

        # Convert to array to handle more easily
        x = numberToArray(params['x'], params['radix'])
        y = numberToArray(params['y'], params['radix'])

        params['answer'] = arrayToNumber(arraySub(x, y, params['radix']))
        print(f"Answer: {params['answer']}")

    if operation == 'multiply':
        ### Do multiplication ###
        params['answer'] = '66'
        params['count-mul'] = '1'
        params['count-add'] = '2'

    if operation == 'mod-add':
        ### Do modular addition ###
        params['answer'] = '1234'

    if operation == 'euclid':
        ### Do euclidean algorithm ###
        params['answ-d'] = '1'
        params['answ-a'] = '0'
        params['answ-b'] = '0'

    # etc.

    # Save answer
    my_answers['exercises'].append({operation: params})

###### Creating an answers list file ######

# Save exercises with answers to file
# write to binary file
my_file = open(ans_loc, 'wb+')
# add encoded exercise list
my_file.write(json.dumps(my_answers).encode())
my_file.close()
