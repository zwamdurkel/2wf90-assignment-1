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

# Checks for two number arrays if one is smaller than the other


def arraySmaller(x, y, base):
    return int(arrayToNumber(x), base=base) < int(arrayToNumber(y), base=base)

# Checks for two number arrays if one is greater than the other


def arrayGreater(x, y, base):
    return int(arrayToNumber(x), base=base) > int(arrayToNumber(y), base=base)

# Euclidean extended algorithm


def euclid(x, y, base):

    xNew = x.copy()
    yNew = y.copy()

    if xNew[-1] == '-':
        xNew.pop()
    if yNew[-1] == '-':
        yNew.pop()

    x1 = [1]
    x2 = [0]
    y1 = [0]
    y2 = [1]

    while arrayGreater(yNew, [0], base):
        q = arrayDivide(xNew, yNew, base)
        r = arraySub(xNew, arrayMultiply(q, yNew, base)[0], base)
        xNew = yNew
        yNew = r
        x3 = arraySub(x1, arrayMultiply(q, x2, base)[0], base)
        y3 = arraySub(y1, arrayMultiply(q, y2, base)[0], base)
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

# Modular inverse algorithm


def inverse(x, m, base):
    xNew = x.copy()
    mNew = m.copy()
    x1 = [1]
    x2 = [0]

    # while arrayGreater(mNew, [0], base):
    while mNew[-1] > 0:
        q = arrayDivide(xNew, mNew, base)
        r = arraySub(xNew, arrayMultiply(q, mNew, base)[0], base)
        xNew = mNew
        mNew = r
        x3 = arraySub(x1, arrayMultiply(q, x2, base)[0], base)
        x1 = x2
        x2 = x3

    answer = 'ERROR - inverse does not exist'

    # check if it was succesfull
    if xNew == [1]:
        answer = x1

    return answer

# Modular multiplication algorithm


def modMult(x, y, m, base):
    if len(m) % 2 == [0]:
        n = len(m)
    else:
        n = len(m) + 1

    bo = [0, 1]
    b = [0, 1]
    h = n/2
    while h > 0:
        b = arrayMultiply(b, bo, base)[0]
        h = h - 1

    xlo = arrayReduce(x, b, base)
    xhi = arrayMultiply(arraySub(x, xlo, base), b, base)[0]

    ylo = arrayReduce(y, b, base)
    yhi = arrayMultiply(arraySub(y, ylo, base), b, base)[0]

    z0 = arrayMultiply(xlo, ylo, base)[0]
    z1 = arrayReduce(arrayAdd(arrayMultiply(xhi, ylo, base)[
                     0], arrayMultiply(xlo, yhi, base)[0], base), m, base)
    z2 = arrayReduce(arrayMultiply(xhi, yhi, base)[0], m, base)

    z = z2

    for i in range(1, int(n/2)):
        z = arrayMultiply(bo, z, base)

    z = arrayReduce(arrayAdd(z, z1, base), m, base)

    for i in range(1, int(n/2)):
        z = arrayMultiply(bo, z, base)

    z = arrayReduce(arrayAdd(z, z0, base), m, base)

    return z


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

    xNew = x.copy()
    yNew = y.copy()

    negativeX = False
    negativeY = False

    if xNew[-1] == '-':
        xNew.pop()
        negativeX = True
    if yNew[-1] == '-':
        yNew.pop()
        negativeY = True

    # Get max size to fill rest with zeros
    size = max(len(xNew), len(yNew))
    # Extend numbers with trailing 0 (doesn't change value)
    xNew += [0] * (size - len(xNew))
    yNew += [0] * (size - len(yNew))

    # If both numbers are negative
    if negativeX and negativeY:
        answer = arrayAdd(xNew, yNew, base)
        answer.append('-')
        return answer

    # If x is negative
    if negativeX:
        if arrayGreater(xNew, yNew, base):
            answer = arraySub(xNew, yNew, base)
            answer.append('-')
            return answer
        else:
            answer = arraySub(yNew, xNew, base)
            return answer

    # If y is negative
    if negativeY:
        if arraySmaller(xNew, yNew, base):
            answer = arraySub(yNew, xNew, base)
            answer.append('-')
            return answer
        else:
            answer = arraySub(xNew, yNew, base)
            return answer

    # Else...

    # Prepare empty carry and answer array
    answer = []
    carry = 0

    # Do digit wise addition (and carry)
    for i in range(size):
        answer.append(xNew[i] + yNew[i] + carry)
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

    xNew = x.copy()
    yNew = y.copy()

    negativeX = False
    negativeY = False

    if xNew[-1] == '-':
        xNew.pop()
        negativeX = True
    if yNew[-1] == '-':
        yNew.pop()
        negativeY = True

    # Get max size to fill rest with zeros
    size = max(len(xNew), len(yNew))
    # Extend numbers with trailing 0 (doesn't change value)
    yNew += [0] * (size - len(yNew))
    xNew += [0] * (size - len(xNew))

    # If both numbers are negative
    if negativeX and negativeY:
        if arrayGreater(xNew, yNew, base):
            answer = arraySub(xNew, yNew, base)
            answer.append('-')
            return answer
        else:
            answer = arraySub(yNew, xNew, base)
            return answer

    # If x is negative
    if negativeX:
        answer = arrayAdd(xNew, yNew, base)
        answer.append('-')
        return answer

    # If y is negative
    if negativeY:
        answer = arrayAdd(xNew, yNew, base)
        return answer

    # If x is smaller than y
    if arraySmaller(xNew, yNew, base):
        answer = arraySub(yNew, xNew, base)
        answer.append('-')
        return answer

    # Else...

    # Prepare empty carry and answer array
    answer = []
    carry = 0

    for i in range(size):
        answer.append(xNew[i] - yNew[i] - carry)
        carry = 0

        if answer[i] < 0:
            answer[i] += base
            carry = 1

    # Remove trailing 0
    while answer[-1] == 0 and answer != [0]:
        answer.pop()

    return answer


def arrayMultiply(x, y, base):

    xNew = x.copy()
    yNew = y.copy()

    negativeX = False
    negativeY = False

    if xNew[-1] == '-':
        xNew.pop()
        negativeX = True

    if yNew[-1] == '-':
        yNew.pop()
        negativeY = True

    lengthX = len(xNew)
    lengthY = len(yNew)
    mul = 0
    add = 0

    answer = [0] * (lengthX + lengthY)

    for i in range(lengthX):
        carry = 0
        for j in range(lengthY):
            t = answer[i + j] + xNew[i] * yNew[j]
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

    xNew = x.copy()
    mNew = m.copy()

    negativeX = False

    if xNew[-1] == '-':
        xNew.pop()
        negativeX = True

    xp = xNew

    i = len(xNew)-len(mNew)

    for j in range(i, -1, -1):
        m2 = [0]*j + mNew
        while not arraySmaller(xp, m2, base):
            xp = arraySub(xp, m2, base)

    if not negativeX or xp == 0:
        answer = xp
    else:
        answer = arraySub(mNew, xp, base)
    return answer


def arrayDivide(x, m, base):
    i = len(x)-len(m)
    q = [0] * len(x)

    for j in range(i, -1, -1):
        m2 = [0]*j + m
        while not arraySmaller(x, m2, base):
            q[j] += 1
            x = arraySub(x, m2, base)

    while q[-1] == 0 and q != [0]:
        q.pop()

    return q


def modAdd(x, y, m, base):
    return arrayReduce(arrayAdd(x, y), m, base)


def modSub(x, y, m, base):
    return arrayReduce(arraySub(x, y), m, base)


### !!!EMRES AREA TO MAKE COOL KARATSUBA ALGORITHM!!! ###

def karatsuba(x, y, m, base):
    if len(m) % 2 == [0]:  # Checking if the length of the number is even or odd
        n = len(m)  # If it's even
    else:
        n = len(m) + 1  # If it's odd

    bo = [0, 1]
    b = [0, 1]
    h = n/2
    while h > 0:
        b = arrayMultiply(b, bo, base)[0]
        h = h-1

    xlo = arrayReduce(x, b, base)  # Computing xlo, xhi, ylo, yhi
    xhi = arrayMultiply(arraySub(x, xlo, base), b, base)[0]

    ylo = arrayReduce(y, b, base)
    yhi = arrayMultiply(arraySub(y, ylo, base), b, base)[0]

    # z0 = xlo*ylo         #Computing z0 and z2
    z0 = arrayMultiply(xlo, ylo, base)[0]
    z2 = arrayMultiply(xhi, yhi, base)[0]  # z2 = xhi*yhi
    z = arraySub(arrayMultiply(arrayAdd(xhi, xlo, base), arrayAdd(yhi, ylo, base), base)[
                 0], arrayAdd(z2, z0, base), base)  # z is the end product xy

    return z
### !!!END OF EMRES AREA TO MAKE COOL KARATSUBA ALGORITHM!!! ###


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
        ### Do modular reduction ###
        x = numberToArray(params['x'], params['radix'])
        m = numberToArray(params['m'], params['radix'])

        params['answer'] = arrayToNumber(arrayReduce(x, m, params['radix']))
        print(f"Answer: {params['answer']}")

    if operation == 'mod-add':
        ### Do modular addition ###

        # Convert to array to handle more easily
        x = numberToArray(params['x'], params['radix'])
        y = numberToArray(params['y'], params['radix'])
        m = numberToArray(params['m'], params['radix'])

        params['answer'] = arrayToNumber(modAdd(x, y, m, params['radix']))
        print(f"Answer: {params['answer']}")

    if operation == 'mod-subtract':
        ### Do modular subtraction ###

        # Convert to array to handle more easily
        x = numberToArray(params['x'], params['radix'])
        y = numberToArray(params['y'], params['radix'])
        m = numberToArray(params['m'], params['radix'])

        params['answer'] = arrayToNumber(modAdd(x, y, m, params['radix']))
        print(f"Answer: {params['answer']}")

    if operation == 'euclid':
        ### Do euclidean algorithm ###

        # Convert to array to handle more easily
        x = numberToArray(params['x'], params['radix'])
        y = numberToArray(params['y'], params['radix'])

        d, a, b = euclid(x, y, params['radix'])

        params['answ-d'] = arrayToNumber(d)
        params['answ-a'] = arrayToNumber(a)
        params['answ-b'] = arrayToNumber(b)

        print(
            f"Answer: {params['answ-d']}, {params['answ-a']}, {params['answ-b']}")

    if operation == 'inverse':
        ### Do inverse ###

        ### Do inverse algorithm ###
        x = numberToArray(params['x'], params['radix'])
        m = numberToArray(params['m'], params['radix'])

        answer = inverse(x, m, params['radix'])

        if answer == 'ERROR - inverse does not exist':
            params['answer'] = 'ERROR - inverse does not exist'
        else:
            params['answer'] = arrayToNumber(answer)

        print(f"Answer: {params['answer']}")

    if operation == 'mod-multiply':
        ### Do modular multiplication algorithm ###

        # Convert to array to handle more easily
        x = numberToArray(params['x'], params['radix'])
        y = numberToArray(params['y'], params['radix'])
        m = numberToArray(params['m'], params['radix'])

        params['answer'] = arrayToNumber(modMult(x, y, m, params['radix']))

        print(f"Answer: {params['answer']}")

# MORE OF EMRES AREA TO MAKE COOL KARATSUBA STUFF (I ALREADY MADE THIS STUFF FOR YOU <3 - Finnean)
    if operation == 'karatsuba':
        ### Do karatsuba algorithm ###

        # Convert to array to handle more easily
        x = numberToArray(params['x'], params['radix'])
        y = numberToArray(params['y'], params['radix'])

        answer, mul, add = arrayMultiply(x, y, params['radix'])

        params['answer'] = arrayToNumber(answer)
        params['count-mul'] = mul
        params['count-add'] = add

        print(
            f"Answer: {params['answer']}, {params['count-mul']}, {params['count-add']}")
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
