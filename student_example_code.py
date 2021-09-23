import asn1tools as asn
import json

### AfS software assignment 1 - example code ###

# set file names
base_location = './'
ops_loc = base_location + 'operations.asn'
exs_loc = base_location + 'my_exercises'
ans_loc = base_location + 'my_answers'

###### Creating an exercise list file ######

# How to create an exercise JSON file containing one addition exercise
exercises = {'exercises' : []}                                     # initialize empty exercise list
ex = {'add' : {'radix' : 10, 'x' : '3', 'y' : '4', 'answer' : ''}} # create add exercise
exercises['exercises'].append(ex)                                  # add exercise to list

# Encode exercise list and print to file
my_file = open(exs_loc, 'wb+')                                     # write to binary file
my_file.write(json.dumps(exercises).encode())                      # add encoded exercise list
my_file.close()

###### Using an exercise list file ######

# Compile specification
spec = asn.compile_files(ops_loc, codec = "jer")

# Read exercise list 
exercise_file = open(exs_loc, 'rb')                                # open binary file
file_data = exercise_file.read()                                   # read byte array
my_exercises = spec.decode('Exercises', file_data)                 # decode after specification
exercise_file.close()                                              

# Create answer JSON
my_answers = {'exercises': []}

# Will convert a number to an array of digits. first element = radix^0, 2nd = radix^1, etc
def numberToArray(number, base):
    array = []

    for i in range(len(number)):
        array.append(int(number[-i - 1], base=base))

    return array


# Will convert array to number as string with 0-9a-f as digits
def arrayToNumber(array):
    number = ''

    # Convert digit to proper string representation
    for digit in array:
        if digit < 10:
            number = str(digit) + number
        if digit >= 10:
            number = chr(ord('a')+digit-10) + number

    return number

# Adds numbers in array representation with variable base
def arrayAdd(x, y, base):

    # Get max size to fill rest with zeros + 1 for carry
    size = len(max(x, y)) + 1
       
    # Extend numbers with trailing 0 for addition (doesn't change value)
    x += [0] * (size - len(x))
    y += [0] * (size - len(y))

    # Prepare empty carry and answer array (I don't wanna do .append())
    carry = [0] * size
    answer = [0] * size

    # Do digit wise addition (and carry)
    for i in range(size):
        digit = x[i] + y[i] + carry[i]

        while digit >= base:
            digit -= base
            carry[i + 1] += 1

        answer[i] = digit

    # Remove trailing 0
    while answer[-1] == 0:
        answer.pop()
        if answer == [0]: break

    return answer

# Loop over exercises and solve
for exercise in my_exercises['exercises']:
    operation = exercise[0]                                        # get operation type
    params = exercise[1]                                           # get parameters

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
        params['answer'] = '-0'

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
my_file = open(ans_loc, 'wb+')                                       # write to binary file
my_file.write(json.dumps(my_answers).encode())                       # add encoded exercise list
my_file.close()
