import asn1tools as asn
import json
import math

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
spec = asn.compile_files(ops_loc, codec = "jer")

# Read exercise list 
exercise_file = open(exs_loc, 'rb')                                # open binary file
file_data = exercise_file.read()                                   # read byte array
my_exercises = spec.decode('Exercises', file_data)                 # decode after specification
exercise_file.close()                                              

# Create answer JSON
my_answers = {'exercises': []}

# Checks for two number arrays if one is smaller than the other
def arraySmaller(x, y, base):
    return int(arrayToNumber(x), base=base) < int(arrayToNumber(y), base=base)

# Checks for two number arrays if one is greater than the other
def arrayGreater(x, y, base):
    return int(arrayToNumber(x), base=base) > int(arrayToNumber(y), base=base)

# FINNEANS GEBIED!!!

def euclid(x, y, base):

    xNew = x
    yNew = y

    if xNew[-1] == '-':
        xNew.pop()
    if yNew[-1] == '-':
        yNew.pop()

    x1 = [1]
    x2 = [0]
    y1 = [0]
    y2 = [1]

    while arrayGreater(yNew, [0], base):
        q = arrayReduce(xNew, yNew, base).floor()
        r = arraySub(xNew, arrayMultiply(q, yNew, base), base)
        xNew = yNew
        yNew = r
        x3 = arraySub(x1, arrayMultiply(q, x2, base), base)
        y3 = arraySub(y1, arrayMultiply(q, y2, base), base)
        x1 = x2
        y1 = y2
        x2 = x3
        y2 = y3

    d = xNew
    if arrayGreater(x, [0], base) or x == [0]:
        a = x1
    else:
        a = x1.append('-')

    if arrayGreater(y, [0], base) or y == [0]:
        b = y1
    else:
        b = y1.append('-')

    return(d, a, b)

def inverse(x, y, base):
    print('')

# FINNEANS GEBIED!

# Will convert a number to an array of digits. first element = radix^0, 2nd = radix^1, etc
def numberToArray(number, base):
    array = []

    for i in range(len(number)):
        if number[-i - 1] == '-':
            array.append('-')
        else:
            array.append(int(number[-i - 1], base=base))

    return array

# Will convert array to number as string with 0-9a-f as digits
def arrayToNumber(array):
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

# Adds numbers in array representation with variable base
def arrayAdd(x, y, base):

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
        if arrayGreater(x, y, base):
            answer = arraySub(x, y, base)
            answer.append('-')
            return answer
        else: 
            answer = arraySub(y, x, base)
            return answer

    # If y is negative
    if negativeY:
        if arraySmaller(x, y, base):
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
        answer.append( x[i] + y[i] + carry )
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
        if arrayGreater(x, y, base):
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
    if arraySmaller(x, y, base):
        answer = arraySub(y, x, base)
        answer.append('-')
        return answer

    # Else...
    
    # Prepare empty carry and answer array
    answer = []
    carry = 0
       
    for i in range(size):
        answer.append( x[i] - y[i] - carry )
        carry = 0

        if answer[i] < 0:
            answer[i] += base
            carry = 1
    
    # Remove trailing 0
    while answer[-1] == 0 and answer != [0]:
        answer.pop()
    
    return answer

def arrayMultiply(x, y, base):

    negativeX = False
    negativeY = False

    if x[-1] == '-':
        x.pop()
        negativeX = True

    if y[-1] == '-':
        y.pop()
        negativeY = True

    lengthX = len(x)
    lengthY = len(y)
    mul = 0
    add = 0

    answer = [0] * (lengthX + lengthY)

    for i in range(lengthX):
        carry = 0
        for j in range(lengthY):
            t = answer[i + j] + x[i] * y[j]
            carry = t // base
            answer[i + j] = t - carry * base
            answer[i + j + 1] += carry
            add += 3
            mul += 2

    if answer[-1] == 0:
        answer.pop()

    if negativeX ^ negativeY:
        answer.append('-')

    return answer, mul, add

def arrayReduce(x, m, base):
    
    negativeX = False

    if x[-1] == '-':
        x.pop()
        negativeX = True

    xp = x

    i = len(x)-len(m)

    for j in range(i,-1,-1):
        m2 = [0]*j + m
        while not arraySmaller(xp, m2, base):
            xp = arraySub(xp, m2, base)
    
    if not negativeX or xp == 0:
        answer = xp
    else:
        answer = arraySub(m, xp, base)
    return answer
    
def modAdd(x,y,m,base):
    return arrayReduce(arrayAdd(x,y),m, base)

def modSub(x,y,m,base):
    return arrayReduce(arraySub(x,y),m, base)

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

        # Convert to array to handle more easily
        x = numberToArray(params['x'], params['radix'])
        y = numberToArray(params['y'], params['radix'])

        params['answer'] = arrayToNumber(arraySub(x, y, params['radix']))
        print(f"Answer: {params['answer']}")

    if operation == 'multiply':
        ### Do multiplication ###
        # Convert to array to handle more easily
        x = numberToArray(params['x'], params['radix'])
        y = numberToArray(params['y'], params['radix'])

        answer, mul, add = arrayMultiply(x, y, params['radix'])

        params['answer'] = arrayToNumber(answer)
        params['count-mul'] = mul
        params['count-add'] = add

        print(
            f"Answer: {params['answer']}, {params['count-mul']}, {params['count-add']}")
    if operation == 'reduce':
        x = numberToArray(params['x'], params['radix'])
        m = numberToArray(params['m'], params['radix']) 

        params['answer'] = arrayToNumber(arrayReduce(x, m, params['radix'])) 
        print(f"Answer: {params['answer']}")
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
