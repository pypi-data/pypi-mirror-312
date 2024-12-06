def padBinaryFloats(bin1, bin2):
    if '.' in bin1:
        int_part1, frac_part1 = bin1.split('.')
    else:
        int_part1, frac_part1 = bin1, '0'
    if '.' in bin2:
        int_part2, frac_part2 = bin2.split('.')
    else:
        int_part2, frac_part2 = bin2, '0'

    # Pad integer parts (left-padding with '0')
    max_int_len = max(len(int_part1), len(int_part2))
    int_part1 = int_part1.zfill(max_int_len)
    int_part2 = int_part2.zfill(max_int_len)

    # Pad fractional parts (right-padding with '0')
    max_frac_len = max(len(frac_part1), len(frac_part2))
    frac_part1 = frac_part1.ljust(max_frac_len, '0')
    frac_part2 = frac_part2.ljust(max_frac_len, '0')

    return int_part1 + '.' + frac_part1, int_part2 + '.' + frac_part2

class binVal:
    def __init__(self, val='0'):
        if str(type(val)) == '<class \'exactBin.binVal\'>':
            self.val = val.val
        else:
            self.val=val
        self.isCorrect()

    def isCorrect(self): #Raises corresponding error when something's incorrect.
        if type(self.val)!=str:raise TypeError('Value is not a string.')
        if len(self.val.split('.'))>2:raise ValueError('Value must have 1 or less dots. Not '+str(len(self.val.split('.'))-1))
        for digit in self.val:
            if digit!='0' and digit!='1' and digit!='.':
                raise ValueError(f'Value can only contain: "0", "1", ".". Not {digit}')

    def getFloat(self): #Turns binary value into decimal float
        self.isCorrect()
        try:
            precision=len(self.val.split('.')[1])
        except IndexError:
            precision=-1
        out=0
        for idx, digit in enumerate(self.val.replace('.', '')): #Go through every digit and add it onto the result.
            out+=int(digit)*2**(len(self.val)-idx-precision-2)
        return out
    
    def setDecValue(self, number, precision=50, clip=True): #Gets a decimal value and turns that into a binary float.
        # Split the number into integer and fractional parts
        integer_part = int(number)
        fractional_part = number - integer_part
        # Convert the integer part to binary
        integer_binary = ""
        if integer_part == 0:
            integer_binary = "0"
        else:
            while integer_part > 0:
                integer_binary = str(integer_part % 2) + integer_binary
                integer_part //= 2
        # Convert the fractional part to binary
        fractional_binary = ""
        while len(fractional_binary) < precision and (fractional_part > 0 or not(clip)):
            fractional_part *= 2
            bit = int(fractional_part)
            fractional_binary += str(bit)
            fractional_part -= bit
        # Combine integer and fractional parts
        if fractional_binary:
            self.val=f"{integer_binary}.{fractional_binary}"
        else:
            self.val=integer_binary
    
    def __iadd__(self, other):
        self.isCorrect()
        other.isCorrect()
        # Pad strings to make them the same length
        bin1, bin2 = padBinaryFloats(self.val, other.val)
        int_part1, frac_part1 = bin1.split('.')
        int_part2, frac_part2 = bin2.split('.')

        # Initialize result and carry
        result_frac = ''
        carry = 0

        # Add fractional part from right to left
        for i in range(len(frac_part1) - 1, -1, -1):
            sum_bit = int(frac_part1[i]) + int(frac_part2[i]) + carry
            result_frac = str(sum_bit % 2) + result_frac
            carry = sum_bit // 2

        # Add integer part from right to left
        result_int = ''
        for i in range(len(int_part1) - 1, -1, -1):
            sum_bit = int(int_part1[i]) + int(int_part2[i]) + carry
            result_int = str(sum_bit % 2) + result_int
            carry = sum_bit // 2

        # If there's a carry left for the integer part, add it
        if carry:
            result_int = '1' + result_int

        # Combine integer and fractional results
        self.val=result_int + '.' + result_frac
        return self

    def __add__(self, other):
        result = binVal(self) # Set the value of result to the value of self
        result += other
        return result
    