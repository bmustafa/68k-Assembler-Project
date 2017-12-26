import sys
import random

smallLetter = ['a','b','c','d','e']
largeLetter = ['A','B','C','D','E']

ListOfInstruction = []

Instructions = ['move', 'add', 'swap', 'cmp', 'dump', 'stop', 'beq', 'bgt', \
                'blt', 'bra', 'sub', 'mulu', 'divu']

InstructionCode = ['0011', '1101', '0100100001000', '1011', '010011100111', \
                   '010011100111', '01100111', '01101110', '01101101', \
                   '01100000', '1001', '1100', '1000']

Directives = ['dc', 'ds', 'org', 'end']

DecChar = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

HexChar = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D',
           'E', 'F']
BinaryEquivalent = ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', \
                    '1000', '1001', '1010', '1011','1100', '1101', '1110', '1111']

FirstLabelList = []
LabelTable = []
ListOfContents = []
ListOfTokens = []
memory = []
Location = "$0000"

def TwoDigit(IntStr):
    '''takes an int str of 1 or 2 length and returns an int string with a length of two
    e.g. from 8 to 08'''
    if len(IntStr) == 1:
        IntStr = '0' + IntStr
    return IntStr


def ConvertSignedHexToInt(inpt):
    if len(inpt) > 4:
        inpt = inpt[0:4]
    while len(inpt) < 4:
        inpt = '0' + inpt
    # convert to unsigned
    x = int(inpt, 16) # example (-65)
    # check sign bit
    if (x & 0x8000) == 0x8000:
        # if set, invert and add one to get the negative value, then add the negative sign
        x = -( (x ^ 0xffff) + 1)
    return x

def RandomHex():
    '''Generates a random hex byte'''
    i = HexChar[random.randrange(0, 16)]
    i += HexChar[random.randrange(0, 16)]
    return i



def BinaryToHex(InptStr):
    '''Convert a binary string into hex string'''
    return '$' + hex(int(InptStr, 2))[2:]


def HexStr(InptStr):
    '''Take in a string of numbers and return a hex string'''
    if InptStr[0] != "$":
        i = int(InptStr)
        return hex((i) & 0xFFFF)[2:]
    else:
        return InptStr


def BraHexStrings(String1, String2):
    '''Calculates the different between two hex strings'''
    Number1 = int(String1[1:], 16)
    Number2 = int(String2[1:], 16)
    Result = Number1 - Number2
    if Result > 128 or Result < -128:
        print('Too large a difference to branch')
        sys.exit()
    else:
        return hex((Result) & 0xFF)[2:]


def IntNmber(Inpt):
    '''Take input deci or hex string and return int number'''
    if Inpt[0] != '$':
        return int(Inpt)
    else:
        return int(Inpt[1:], 16)


def intTo16Bit(intgr):
    '''represents an signed int as a 16 bit string'''
    Bool = True
    WorkingString = ''
    if intgr < 0:
        TempVariable = hex((intgr) & 0xFFFF)[2:]
        for j in TempVariable:
            for i in range(len(HexChar)):
                if j.upper() == HexChar[i]:
                    WorkingString += BinaryEquivalent[i]
        return WorkingString

    bitString = bin(intgr)
    bitString = bitString[2:]
    if (len(bitString[2:])) > 15:
        print('move displacement int too large')
        sys.exit()
    else:
        WorkingString = bitString
        while len(bitString) < 15:
            bitString = '0' + bitString
        if Bool:
            bitString = '0' + bitString
        else:
            bitString = '1' + bitString
        return bitString


def IsItValidInstruction(InputList):
    '''Check to see in opcode is an instruction'''
    for k in Instructions:
        if InputList[1].lower() == k:
            return True
    return False


def CheckAddress(InptString):
    '''check to see in address is of a valid form -  (a0) or 10(a0)
    and return (True/False, The displacement, the int in (aX))'''
    if InptString.lower() == 'd1' or InptString.lower() == 'd3' or InptString.lower() == 'd2' \
            or InptString.lower() == 'd0':
        return False
    if len(InptString) == 4 and InptString[0] == '(' and InptString[1].lower() == 'a' and (InptString[2] == '0' or \
                                                                                                       InptString[
                                                                                                           2] == '1' or
                                                                                                   InptString[
                                                                                                       2] == '2' or
                                                                                                   InptString[
                                                                                                       2] == '3') and \
                    InptString[3] \
                    == ')':
        return (True, 0, InptString[2])
    else:
        TempString = ''
        if InptString[0] == '-':
            TempString += '-'
            InptString = InptString[1:]
        for k in InptString:
            if k != '(':
                if k != '0' and k != '1' and k != '2' and k != '3' and k != '4' and k != '5' and \
                                k != '6' and k != '7' and k != '8' and k != '9':
                    print('error invalid address')
                    sys.exit()
                else:
                    TempString += k
                    InptString = InptString[1:]
            else:
                return (True, int(TempString), InptString[2])

def AmmendedCheckAddress(InptString, InptNo):
    '''check to see in address is of a valid form -  (a0) or 10(a0)
    and return (True/False, The displacement, the int in (aX))'''
    '''InptNo 1 is being use for PassOne and 2 for PassTwo'''
    Bool = True
    Bool2 = True
    Bool3 = False
    Location = ''
    OutputVariable = 0
    if InptString.lower() == 'd1' or InptString.lower() == 'd3' or InptString.lower() == 'd2' \
            or InptString.lower() == 'd0':
        #return False if of format d0
        return False
    if len(InptString) == 4 and InptString[0] == '(' and InptString[1].lower() == 'a' and (InptString[2] == '0' or \
                                                                                                       InptString[
                                                                                                           2] == '1' or
                                                                                                   InptString[
                                                                                                       2] == '2' or
                                                                                                   InptString[
                                                                                                       2] == '3') and \
                    InptString[3] == ')':
        #return (True, Displacement, Register no.) if of format (aX)
        return (True, 0, InptString[2])
    else:
        TempString2 = ''
        TempString = ''
        if InptString[0] == '-':
            TempString += '-'
            InptString = InptString[1:]
            #incase there is a negative displacement
        for k in InptString:
            if k != '(' and Bool:
                TempString += k
                InptString = InptString[1:]
            else:
                Bool = False
        if not CheckAddress(InptString)[0]:
            #check to see if (a0) part of 10(a0) is of the right format
            print('error format mem')
            sys.exit()
        Counter4 = 0
        for i in TempString:
            if Counter4 == 0:
                Counter4 += 1
                if i == '0' or i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or \
                                i == '8' or i == '9' or i == '-':
                    pass
                else:
                    Bool2 = False
            elif i == '0' or i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or \
                        i == '8' or i == '9':
                pass
            else:
                Bool2 = False
            #Bool2 is False if there is a potential label before (a0)
        if Bool2:
            return (True, int(TempString), InptString[2])
            #return (True, Displacement, Register no.) in 10(a0)
        else:
            if InptNo == 1:
                return (False, 0, 0)
            for k in LabelTable:
                if k[0] == TempString:
                    Bool3 = True
                    Location = k[1]
                else:
                    pass
            #If Label matches X in X(a0) Bool3 is True
            if not Bool3:
                print(TempString)
                print('Label in memory address not recognized')
                sys.exit()
            else:
                OutputVariable = ConvertSignedHexToInt(Location[1:])
                return (True, OutputVariable, InptString[2])



def CheckNumberAddress(InptString, TrueOrFalse):
    '''Check if of the form $700 if true or #$700 if false'''
    if TrueOrFalse:
        if InptString[0] == '$':
            for k in InptString[1:]:
                if k != '0' and k != '1' and k != '2' and k != '3' and k != '4' and k != '5' and \
                                k != '6' and k != '7' and k != '8' and k != '9' and k != 'A' and k != 'B' \
                        and k != 'C' and k != 'D' and k != 'E':
                    return False
        else:
            return False
    else:
        if InptString[0] == '#':
            if InptString[1] == '$':
                for k in InptString[1:]:
                    if k != '0' and k != '1' and k != '2' and k != '3' and k != '4' and k != '5' and \
                                    k != '6' and k != '7' and k != '8' and k != '9' and k != 'A' and k != 'B' \
                            and k != 'C' and k != 'D' and k != 'E':
                        return False
            else:
                return False
        else:
            return False


def OperandSplit(InptString):
    '''Parses operands to give a tuple with (a1,d1) or (10(a0),d3) or the like'''
    WorkingString = InptString
    String1 = ''
    String2 = ''
    Output1 = 0
    Output2 = 0
    Bool = True
    for k in WorkingString:
        if Bool:
            if k != ',':
                String1 += k
            else:
                Bool = False
        if not Bool:
            if k != ',':
                String2 += k
    return (String1, String2)


def ParseOperand(InptList):
    '''Parses operands to give a tuple that identifies the source and destination
    and checks for errors     1=DATA 2=Address 10=Memory without disp  20 = memory with displacement'''
    WorkingString = InptList[2]
    String1 = ''
    String2 = ''
    Output1 = 0
    Output2 = 0
    Bool = True
    Bool2 = True
    for k in WorkingString:
        if Bool:
            if k != ',':
                String1 += k
            else:
                Bool = False
        if not Bool:
            if k != ',':
                String2 += k
    if String1[0].lower() == 'd' and (String1[1] == '1' or String1[1] == '2' \
                                              or String1[1] == '3' or String1[1] == '0'):
        Output1 = 1
    elif String1[0].lower() == 'a' and (String1[1] == '1' or String1[1] == '2' \
                                                or String1[1] == '3' or String1[1] == '0'):
        Output1 = 2
    else:
        if InptList[1].lower() != 'move':
            if AmmendedCheckAddress(String1, 1)[0]:
                Output1 = 10
                # if it is an address of form (a10) for any instruction other than move
        else:
            if AmmendedCheckAddress(String1, 1)[0] and AmmendedCheckAddress(String1, 1)[1] == 0:
                Output1 = 10
                # output 2 to signal there is no displacement needed for this one
                # as it is of the form 0(a0)
            elif AmmendedCheckAddress(String1, 1)[0] and AmmendedCheckAddress(String1, 1)[1] != 0:
                Output1 = 20
                # if of the form 10(a0) output 3
            else:
                for k in LabelTable:
                    if k[0] == String1:
                        if int(k[1][1:], 16) != 0:
                            Output1 = 10
                            Bool2 = False
                        else:
                            Output1 = 20
                            Bool2 = False

                            # to signal no displacement needed
                if Bool2:
                    Output1 = 20
                    # label table not formed yet check at a later date

    #    else:
    #       Output1 = String1
    #      #checks to see if the source is either a DR, AR, Memory slot or label
    Bool2 = True
    if String2[0].lower() == 'd' and (String2[1] == '1' or String2[1] == '2' \
                                              or String2[1] == '3' or String2[1] == '0'):
        Output2 = 1
    elif String2[0].lower() == 'a' and (String2[1] == '1' or String2[1] == '2' \
                                                or String2[1] == '3' or String2[1] == '0'):
        Output2 = 2
    else:
        if InptList[1].lower() != 'move':
            if AmmendedCheckAddress(String2,1)[0]:
                Output2 = 10
                #if it is an address of form (a10) for any instruction other than move
        else:
            if AmmendedCheckAddress(String2,1)[0] and AmmendedCheckAddress(String2,1)[1] == 0:
                Output2 = 10

                #output 2 to signal there is no displacement needed for this one
                #as it is of the form 0(a0)
            elif AmmendedCheckAddress(String2, 1)[0] and AmmendedCheckAddress(String2,1)[1] != 0:
                Output2 = 20
                # if of the form 10(a0) output 3
            else:
                for k in LabelTable:
                    if k[0] == String2:
                        if int(k[1][1:], 16) != 0:
                            Output2 = 10
                            Bool2 = False
                        else:
                            Output2 = 20
                            Bool2 = False

                            #to signal no displacement needed
                if Bool2:
                    Output2 = 20
            #label table not formed yet check at a later date
        # else:
        #    Output2 = String2
        # checks to see if the destination is either a DR, AR, Memory slot or label

    return (Output1, Output2)


def IsItValidMemory(InptHexString):
    '''To make sure memory is not going out of bounds'''
    if int(InptHexString[1:], 16) > 16000 or int(InptHexString[1:], 16) < 0:
        return False
        print('memory out of bounds')
        sys.exit()
    else:
        return True


def InstructionLength(InptList):
    '''Take Parsed Data and return instruction length'''
    if IsItValidInstruction(InptList):
        if InptList[1].lower() == 'stop':
            if InptList[2] != '#$2700':
                print('error wrong operand following stop')
                sys.exit()
            else:
                return 2

        if InptList[1].lower() == 'swap' and (InptList[2][0].lower() != 'd' \
                                              or (InptList[2][1] != '1' and InptList[2][1] != '0' \
                                                          and InptList[2][1] != '2' and InptList[2][1] != '3')):
            print('error with swap')
            sys.exit()
            # if InptList[1].lower() == ('bra' or 'blt' or 'bgt' or 'beq') and not CheckAddress(InptList[2])[0]:
            #    print('branch error')
            #   sys.exit()
        if InptList[1].lower() != 'bra' and InptList[1].lower() != 'blt' and InptList[1].lower() != 'bgt' \
                and InptList[1].lower() != 'beq' and InptList[1].lower() != 'swap':
            TempVariable = ParseOperand(InptList)
            if InptList[1].lower() == 'add' and (TempVariable[1] != 1 or TempVariable[0] == 10):
                print('error with add')
                sys.exit()
            if InptList[1].lower() == 'sub' and (TempVariable[1] != 1 or TempVariable[0] != 1):
                print('error with sub')
                sys.exit()
            if InptList[1].lower() == 'mulu' and (TempVariable[1] != 1 or TempVariable[0] != 1):
                print('error with mulu')
                sys.exit()
            if InptList[1].lower() == 'divu' and (TempVariable[1] != 1 or TempVariable[0] != 1):
                print('error with divu')
                sys.exit()
            if InptList[1].lower() == 'cmp' and (TempVariable[1] != 1 and TempVariable[0] != 1):
                print('error with cmp')
                sys.exit()
        if InptList[1].lower() == 'add' or InptList[1].lower() == 'sub' \
                or InptList[1].lower() == 'mulu' or InptList[1].lower() == 'divu' \
                or InptList[1].lower() == 'cmp' or InptList[1].lower() == 'bra' \
                or InptList[1].lower() == 'beq' or InptList[1].lower() == 'bgt' \
                or InptList[1].lower() == 'blt' \
                or InptList[1].lower() == 'dump' or InptList[1].lower() == 'swap':
            return 2
        else:
            if InptList[1].lower() == 'move':
                if (TempVariable[0] + TempVariable[1]) == 40:
                    return 6

                if (TempVariable[0] + TempVariable[1]) > 20:
                    return 4
                if (TempVariable[1] + TempVariable[0]) <= 20:
                    return 2
                else:
                    print('error operand is not valid label, memory or register')
                    sys.exit()
                    # check to see if either operand is a label
                    # if none of the above are a label then error


def hexAdd(HexString, Dec):
    '''take a hex string and a deci number. Add and return a hex string'''
    HexString = HexString[1:]
    HexString = '0x' + HexString
    i = int(HexString, 16)
    i = i + Dec
    s = hex(i)
    s = s[2:]
    s = '$' + s
    return s


def hexSub(HexString, Dec):
    '''take a hex string and a deci number. Sub and return a hex string'''
    i = int(HexString, 16)
    i = i - Dec
    s = hex(i)
    return s[2:]


def CheckComment(InputString):
    '''check to see if the line is a comment'''
    TempList = InputString.split()
    if len(TempList) != 0:
        if TempList[0][0] == '*':
            return True
        else:
            return False
    return True


def Binary3Bit(InptString):
    '''Takes a0-3 or d0-3 and returns the bit equivalent of the number'''
    if InptString[0].lower() == 'a':
        if InptString[1] == '0':
            return '000'
        elif InptString[1] == '1':
            return '001'
        elif InptString[1] == '2':
            return '010'
        elif InptString[1] == '3':
            return '011'
    if InptString[0].lower() == 'd':
        if InptString[1] == '0':
            return '000'
        elif InptString[1] == '1':
            return '001'
        elif InptString[1] == '2':
            return '010'
        elif InptString[1] == '3':
            return '011'
    sys.exit()


def EmptyLine(InputString):
    '''Return false if the line has any characters other than the space char and the new line char
    else true'''
    for k in InputString:
        if k != ' ' or k != '\n':
            return False
    return True


def CheckString(InputString):
    '''Take a string and return parsed data'''
    Bool = True
    OutPutLabel = ""
    OutPutOpcode = ""
    OutPutOperand = ""
    TempList = InputString.split()
    if InputString[0] == " " or InputString[0] == '	':
        OutPutLabel = ""
        OutPutOpcode = TempList[0]
        OutPutOperand = TempList[1]
    else:
        for i in Instructions:
            if i == TempList[0]:
                OutPutLabel = ""
                OutPutOpcode = TempList[0]
                OutPutOperand = TempList[1]
                Bool = False

        for i in Directives:
            if i == TempList[0]:
                OutPutLabel = ""
                OutPutOpcode = TempList[0]
                OutPutOperand = TempList[1]
                Bool = False

        if Bool:
            OutPutLabel = TempList[0]
            OutPutOpcode = TempList[1]
            OutPutOperand = TempList[2]

    return [OutPutLabel, OutPutOpcode, OutPutOperand]


def CheckLocation(InputString):
    '''Check to see if location is of valid form'''
    if InputString[0] == "$":
        for i in InputString[1:]:
            Bool = False
            for j in HexChar:
                if i == j:
                    Bool = True
            if Bool == False:
                return False
        return True

    else:
        for i in InputString:
            Bool = False
            for j in HexChar:
                if i == j:
                    Bool = True
            if Bool == False:
                return False
        return True


def passOne():
    '''function for the passone algorithm. Covers the spacing of instructions within memory'''
    inPutString = input('Enter File Name (i.e.C:/users/bilbum/desktop/My Test Files/Testfile.asm) ')
    with open(inPutString, 'r') as inputFile:
    #with open('C:/users/bilbum/desktop/My Test Files/Testfile6.txt', 'r') as inputFile:
        Contents = inputFile.read()
        WorkingString = ''
        for lines in Contents:
            if (lines != '\n'):
                WorkingString = WorkingString + lines
            else:
                ListOfContents.append(WorkingString)
                WorkingString = ''
        # create a list of strings for each line

        for i in ListOfContents:
            ListOfTokens.append(i.split())
            # create a list of lists - each inner list containing tokens for it
            # respective line


        #############################################################################################
        for i in ListOfContents:
            if not EmptyLine(i):
                # go through the lines in the program
                #stop if they are empty
                if not CheckComment(i):
                    # check to see if its a comment

                    ParsedData = CheckString(i)
                    # parse each one into an label, opcode and operand
                    if ParsedData[1].lower() == 'end':
                        return
                    #quit program if you have reached end



                    for j in LabelTable:
                        if (ParsedData[0] == j[0]):
                            print("error duplicate label")
                            sys.exit()
                    if ParsedData[0] != "":
                        IsItValidMemory(Location)
                        LabelTable.append((ParsedData[0], Location))
                    # Check label to see if its been used before, if so flag error
                    # if not then add it to the list of labels

                    HelpingBool = False
                    for k in Instructions:
                        if ParsedData[1].lower() == k:
                            HelpingBool = True
                            IsItValidMemory(Location)
                            memory.append(Location)
                            if InstructionLength(ParsedData) == 6:
                                Location = hexAdd(Location, 4)
                                IsItValidMemory(Location)
                                memory.append(Location)
                                Location = hexAdd(Location, 2)
                                IsItValidMemory(Location)

                            else:
                                Location = hexAdd(Location, InstructionLength(ParsedData))
                                IsItValidMemory(Location)
                    # check to see if the opcode is an intruction

                    if not HelpingBool:
                        if ParsedData[1].upper() == "ORG":
                            if CheckLocation(ParsedData[2]):
                                Location = HexStr(ParsedData[2])
                            else:
                                print("error - address")
                                sys.exit()
                        # check to see if opcode is ORG

                        elif ParsedData[1].upper() == "DC":
                            internalCounter = 0
                            TempString = ''
                            if ParsedData[2][0] == ',':
                                print('DC - invalid operand strucutre')
                                sys.exit()
                            for n in range(len(ParsedData[2])):
                                if ParsedData[2][n] != ',':
                                    if len(TempString) == 0 or (n+1) != len(ParsedData[2]):
                                        #so check that last character of chain is not '-' but first char of each
                                        #number can be -
                                        if ParsedData[2][n] != '0' and ParsedData[2][n] != '1' and ParsedData[2][
                                            n] != '2' \
                                                and ParsedData[2][n] != '3' and ParsedData[2][n] != '4' and \
                                                        ParsedData[2][n] != '5' \
                                                and ParsedData[2][n] != '6' and ParsedData[2][n] != '7' and \
                                                        ParsedData[2][n] != '8' and ParsedData[2][n] != '9' \
                                                and ParsedData[2][n] != '-':
                                            print('error with DC - invalid char 1')
                                            sys.exit()
                                        TempString += ParsedData[2][n]
                                        if (n+1) == len(ParsedData[2]):
                                            #exception for if there is only one number
                                            if (int(TempString) < -32786 or int(TempString) > 32786):
                                                print('error with DC - int too large or small')
                                                sys.exit()
                                            if internalCounter == 1:
                                                Location = hexAdd(Location, 2)
                                                IsItValidMemory(Location)
                                                TempString = ''
                                                internalCounter = 0
                                            elif internalCounter == 0:
                                                IsItValidMemory(Location)
                                                memory.append(Location)
                                                Location = hexAdd(Location, 2)
                                                IsItValidMemory(Location)
                                                TempString = ''
                                                internalCounter = 1
                                    else:
                                        #for other cases where char not allowed to be -
                                        if ParsedData[2][n] != '0' and ParsedData[2][n] != '1' and ParsedData[2][n] != '2'\
                                                and ParsedData[2][n] != '3' and ParsedData[2][n] != '4' and ParsedData[2][n] != '5' \
                                                and ParsedData[2][n] != '6' and ParsedData[2][n] != '7' and \
                                                        ParsedData[2][n] != '8' and ParsedData[2][n] != '9':
                                            print('error with DC - invalid char 2')
                                            sys.exit()
                                        TempString += ParsedData[2][n]
                                        if (n+1) == len(ParsedData[2]):
                                            if (int(TempString) < -32786 or int(TempString) > 32786):
                                                print('error with DC - int too large or small')
                                                sys.exit()
                                            if internalCounter == 1:
                                                Location = hexAdd(Location, 2)
                                                IsItValidMemory(Location)
                                                TempString = ''
                                                internalCounter = 0
                                            elif internalCounter == 0:
                                                IsItValidMemory(Location)
                                                memory.append(Location)
                                                Location = hexAdd(Location, 2)
                                                IsItValidMemory(Location)
                                                TempString = ''
                                                internalCounter = 1
                                else:
                                    #for if there is a , char
                                    if (n+1) == len(ParsedData[2]):
                                        print('error last char is comma')
                                    if ParsedData[2][n+1] == ',':
                                        print('Error - Invalid DC Structure - two consecutive commas)')
                                    if(int(TempString) < -32786 or int(TempString) > 32786):
                                        print('error with DC - int too large or small')
                                        sys.exit()
                                    if internalCounter == 1:
                                        Location = hexAdd(Location, 2)
                                        IsItValidMemory(Location)
                                        TempString = ''
                                        internalCounter = 0
                                    elif internalCounter == 0:
                                        IsItValidMemory(Location)
                                        memory.append(Location)
                                        Location = hexAdd(Location, 2)
                                        IsItValidMemory(Location)
                                        TempString = ''
                                        internalCounter = 1
                        #assumption that it is not greater than a world long
                        # check to see if opcode is DC
                        # If so add to memory and make appropriate change to Location

                        elif ParsedData[1].upper() == "DS":
                            IsItValidMemory(Location)
                            memory.append(Location)
                            Location = hexAdd(Location, 2 * IntNmber(ParsedData[2]))
                            IsItValidMemory(Location)
                        # check to see if opcode is DS
                        # If so add to memory and make appropriate change to Location

                        else:
                            print("illegal opcode 2")
                            sys.exit()
                            # flag if illegal opcode
        passTwo()


def passTwo():
    '''algorithm that creates the instruction code'''
    Location = '$0000'
    WorkingString = ''
    Location = memory[0]
    Counter = 0
    for i in ListOfContents:
        Bool2 = True
        Bool = True
        HelpingBool = False
        if not EmptyLine(i):
            WorkingString = ''
            # go through the lines in the program
            #check to see if it is an empty line
            if not CheckComment(i):
                # check to see if its a comment

                ParsedData = CheckString(i)
                if ParsedData[1].lower() == 'end':
                    sys.exit()
                    # parse each one into an label, opcode and operand



                if ParsedData[1].lower() != 'swap' and ParsedData[1].lower() != 'bra' and \
                                ParsedData[1].lower() != 'blt' and ParsedData[1].lower() != 'bgt' and \
                                ParsedData[1].lower() != 'beq' and ParsedData[1].lower() != 'stop':
                    ParsedOp = OperandSplit(ParsedData[2])
                else:
                    ParsedOp = ParsedData[2]
                    Bool = False
                #check to see if it is one of the instructions mentioned above to avoid error

                for k in range(len(Instructions)):
                    if ParsedData[1] == Instructions[k]:
                        WorkingString = WorkingString + InstructionCode[k]
                        # create first part of the string for code
                        HelpingBool = True

                if Bool and HelpingBool:
                    if WorkingString == '1101' and ParsedOp[0][0].lower() == 'd' and \
                                    ParsedOp[1][0].lower() == 'd':
                        WorkingString = WorkingString + Binary3Bit(ParsedOp[1]) + '001000' + \
                                        Binary3Bit(ParsedOp[0])
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                        Counter += 1
                        # add dr dr
                        #generate the instruction

                    elif WorkingString == '1101' and ParsedOp[0][0].lower() == 'd' and \
                                    ParsedOp[1][0].lower() == 'a':
                        WorkingString = WorkingString + Binary3Bit(ParsedOp[1]) + '011000' + \
                                        Binary3Bit(ParsedOp[0])
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                        Counter += 1
                        # add dr ar
                        #generate the instruction

                    elif WorkingString == '1001' and ParsedOp[0][0].lower() == 'd' and \
                                    ParsedOp[1][0].lower() == 'd':
                        WorkingString = WorkingString + Binary3Bit(ParsedOp[1]) + '001000' + \
                                        Binary3Bit(ParsedOp[0])
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                        Counter += 1
                        # sub dr dr
                        #generate the instruction

                    elif WorkingString == '1100' and ParsedOp[0][0].lower() == 'd' and \
                                    ParsedOp[1][0].lower() == 'd':
                        WorkingString = WorkingString + Binary3Bit(ParsedOp[1]) + '011000' + \
                                        Binary3Bit(ParsedOp[0])
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                        Counter += 1
                        # mult dr dr
                        #generate the instruction

                    elif WorkingString == '1000' and ParsedOp[0][0].lower() == 'd' and \
                                    ParsedOp[1][0].lower() == 'd':
                        WorkingString = WorkingString + Binary3Bit(ParsedOp[1]) + '011000' + \
                                        Binary3Bit(ParsedOp[0])
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                        Counter += 1
                        # div dr dr
                        #generate the instruction

                    elif WorkingString == '1011' and ParsedOp[0][0].lower() == 'd' and \
                                    ParsedOp[1][0].lower() == 'd':
                        WorkingString = WorkingString + Binary3Bit(ParsedOp[1]) + '001000' + \
                                        Binary3Bit(ParsedOp[0])
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                        Counter += 1
                        # cmp dr dr
                        #generate the instruction


                    elif WorkingString == '0011' and ParsedOp[0][0].lower() == 'd' and \
                                    ParsedOp[1][0].lower() == 'd':
                        WorkingString = WorkingString + Binary3Bit(ParsedOp[1]) + '000000' + \
                                        Binary3Bit(ParsedOp[0])
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                        Counter += 1
                        # move dr dr
                        #generate the instruction

                    elif WorkingString == '0011' and ParsedOp[0][0].lower() == 'd' and \
                                    ParsedOp[1][0].lower() == 'a':
                        WorkingString = WorkingString + Binary3Bit(ParsedOp[1]) + '001000' + \
                                        Binary3Bit(ParsedOp[0])
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                        Counter += 1
                        # move dr ar
                        #generate the instruction

                    elif WorkingString == '0011' and ParsedOp[0][0].lower() == 'a' and \
                                    ParsedOp[1][0].lower() == 'd':
                        WorkingString = WorkingString + Binary3Bit(ParsedOp[1]) + '000001' + \
                                        Binary3Bit(ParsedOp[0])
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                        Counter += 1
                        # move ar dr
                        #generate the instruction

                    elif WorkingString == '0011' and ParsedOp[0][0].lower() == 'a' and \
                                    ParsedOp[1][0].lower() == 'a':
                        WorkingString = WorkingString + Binary3Bit(ParsedOp[1]) + '001001' + \
                                        Binary3Bit(ParsedOp[0])
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                        Counter += 1
                        # move ar ar
                        #generate the instruction

                    elif WorkingString == '0011' and ParsedOp[0][0].lower() == 'a' and \
                            AmmendedCheckAddress(ParsedOp[1], 2)[0]:
                        if AmmendedCheckAddress(ParsedOp[1],2)[1] != 0:
                            WorkingString = WorkingString + Binary3Bit('a' + AmmendedCheckAddress(ParsedOp[1],2)[2]) \
                                            + '101001' + Binary3Bit(ParsedOp[0]) + \
                                            intTo16Bit(AmmendedCheckAddress(ParsedOp[1],2)[1])
                        else:
                            WorkingString = WorkingString + Binary3Bit('a' + AmmendedCheckAddress(ParsedOp[1],2)[2]) \
                                            + '010001' + Binary3Bit(ParsedOp[0])
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                        Counter += 1
                        # move ar mem
                        #generate the instruction

                    elif WorkingString == '0011' and ParsedOp[0][0].lower() == 'd' and \
                            AmmendedCheckAddress(ParsedOp[1],2)[0]:
                        if AmmendedCheckAddress(ParsedOp[1],2)[1] != 0:
                            WorkingString = WorkingString + Binary3Bit('a' + AmmendedCheckAddress(ParsedOp[1],2)[2]) \
                                            + '101000' + Binary3Bit(ParsedOp[0]) + \
                                            intTo16Bit(AmmendedCheckAddress(ParsedOp[1],2)[1])
                        else:
                            WorkingString = WorkingString + Binary3Bit('a' + AmmendedCheckAddress(ParsedOp[1],2)[2]) \
                                            + '010000' + Binary3Bit(ParsedOp[0])
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                        Counter += 1
                        # move dr mem
                        #generate the instruction

                    elif WorkingString == '0011' and ParsedOp[1][0].lower() == 'a' and \
                            AmmendedCheckAddress(ParsedOp[0],2)[0]:
                        if AmmendedCheckAddress(ParsedOp[0],2)[1] != 0:
                            WorkingString = WorkingString + Binary3Bit(ParsedOp[1]) \
                                            + '001101' + Binary3Bit('a' + AmmendedCheckAddress(ParsedOp[0],2)[2]) + \
                                            intTo16Bit(AmmendedCheckAddress(ParsedOp[0],2)[1])
                            #001101
                        else:
                            WorkingString = WorkingString + Binary3Bit(ParsedOp[1]) \
                                            + '001010' + Binary3Bit('a' + AmmendedCheckAddress(ParsedOp[0],2)[2])

                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                        Counter += 1
                        # move mem ar
                        #generate the instruction

                    elif WorkingString == '0011' and ParsedOp[1][0].lower() == 'd' and \
                            AmmendedCheckAddress(ParsedOp[0],2)[0]:
                        if AmmendedCheckAddress(ParsedOp[0], 2)[1] != 0:
                            WorkingString = WorkingString + Binary3Bit(ParsedOp[1]) \
                                            + '000101' + Binary3Bit('a' + AmmendedCheckAddress(ParsedOp[0], 2)[2]) + \
                                            intTo16Bit(AmmendedCheckAddress(ParsedOp[0], 2)[1])
                        else:
                            WorkingString = WorkingString + Binary3Bit(ParsedOp[1]) \
                                            + '000010' + Binary3Bit('a' + AmmendedCheckAddress(ParsedOp[0], 2)[2])
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                        Counter += 1
                        # move mem dr
                        #generate the instruction


                    elif WorkingString == '0011' and AmmendedCheckAddress(ParsedOp[1],2)[0] and \
                            AmmendedCheckAddress(ParsedOp[0],2)[0]:
                        if AmmendedCheckAddress(ParsedOp[1],2)[1] == 0 and AmmendedCheckAddress(ParsedOp[0],2)[1] == 0:
                            WorkingString = WorkingString + Binary3Bit('a' + AmmendedCheckAddress(ParsedOp[1],2)[2]) \
                                            + '010010' + Binary3Bit('a' + AmmendedCheckAddress(ParsedOp[0],2)[2])
                            ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                            Counter += 1

                        elif AmmendedCheckAddress(ParsedOp[1],2)[1] != 0 and AmmendedCheckAddress(ParsedOp[0],2)[1] != 0:
                            WorkingString = WorkingString + Binary3Bit('a' + AmmendedCheckAddress(ParsedOp[1], 2)[2]) \
                                            + '101101' + Binary3Bit('a' + AmmendedCheckAddress(ParsedOp[0], 2)[2]) + \
                                            intTo16Bit(AmmendedCheckAddress(ParsedOp[0], 2)[1]) + \
                                            intTo16Bit(AmmendedCheckAddress(ParsedOp[1], 2)[1])
                            Counter += 2
                            ListOfInstruction.append(BinaryToHex(WorkingString[:-16])[1:])
                            TempVariable2 = BinaryToHex(WorkingString[-16:])[1:]
                            while len(TempVariable2) < 4:
                                TempVariable2 = '0' + TempVariable2
                            ListOfInstruction.append(TempVariable2)

                        elif AmmendedCheckAddress(ParsedOp[1],2)[1] != 0:
                            WorkingString = WorkingString + Binary3Bit('a' + AmmendedCheckAddress(ParsedOp[1], 2)[2]) \
                                            + '101010' + Binary3Bit('a' + AmmendedCheckAddress(ParsedOp[0], 2)[2]) + \
                                            intTo16Bit(AmmendedCheckAddress(ParsedOp[1], 2)[1])
                            ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                            Counter += 1

                        else:
                            WorkingString = WorkingString + Binary3Bit('a' + AmmendedCheckAddress(ParsedOp[1], 2)[2]) \
                                            + '010101' + Binary3Bit('a' + AmmendedCheckAddress(ParsedOp[0], 2)[2]) + \
                                            intTo16Bit(AmmendedCheckAddress(ParsedOp[0], 2)[1])
                            ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                            Counter +=1
                        # move mem mem
                        #generate the instruction

                elif HelpingBool:
                    if WorkingString == '0100100001000':
                        WorkingString = WorkingString + Binary3Bit(ParsedOp)
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                        Counter += 1
                        # swap
                        #generate the instruction

                    elif WorkingString == '010011100111':
                        WorkingString += '00100010011100000000'
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:])
                        Counter += 1
                        # stop or dump
                        #generate the instruction

                    elif WorkingString == '01100000':
                        TempVariable = ''
                        for k in LabelTable:
                            if k[0] == ParsedData[2]:
                                TempVariable = k[1]
                                Bool2 = False
                        if Bool2:
                            print('error bra - no LABEL')
                            sys.exit()
                        TempVariable = BraHexStrings(TempVariable, hexAdd(memory[Counter], 2))
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:] + TempVariable)
                        Counter += 1
                        # bra
                        #generate the instruction

                    elif WorkingString == '01100111':
                        TempVariable = ''
                        for k in LabelTable:
                            if k[0] == ParsedData[2]:
                                TempVariable = k[1]
                                Bool2 = False
                        if Bool2:
                            print('error beq - no LABEL')
                            sys.exit()
                        TempVariable = BraHexStrings(TempVariable, hexAdd(memory[Counter], 2))
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:] + TempVariable)
                        Counter += 1
                        # beq
                        #generate the instruction

                    elif WorkingString == '01101110':
                        TempVariable = ''
                        for k in LabelTable:
                            if k[0] == ParsedData[2]:
                                TempVariable = k[1]
                                Bool2 = False
                        if Bool2:
                            print('error bgt - no LABEL')
                            sys.exit()
                        TempVariable = BraHexStrings(TempVariable, hexAdd(memory[Counter], 2))
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:] + TempVariable)
                        Counter += 1
                        # bgt
                        #generate the instruction

                    elif WorkingString == '01101101':
                        TempVariable = ''
                        for k in LabelTable:
                            if k[0] == ParsedData[2]:
                                TempVariable = k[1]
                                Bool2 = False
                        if Bool2:
                            print('error blt - no LABEL')
                            sys.exit()
                        TempVariable = BraHexStrings(TempVariable, hexAdd(memory[Counter], 2))
                        ListOfInstruction.append(BinaryToHex(WorkingString)[1:] + TempVariable)
                        Counter += 1
                        # blt
                        #generate the instruction



                else:
                    if ParsedData[1].upper() == 'DC':
                       DcCounter = 0
                       SignedHex = ''
                       SignedHex2 = ''
                       TempString = ''
                       if ParsedData[2][0] == ',':
                           print('DC - invalid operand strucutre')
                           sys.exit()
                       for n in range(len(ParsedData[2])):
                           if ParsedData[2][n] != ',':
                               if len(TempString) == 0 or (n+1) != len(ParsedData[2]):
                                   if ParsedData[2][n] != '0' and ParsedData[2][n] != '1' and ParsedData[2][
                                       n] != '2' \
                                           and ParsedData[2][n] != '3' and ParsedData[2][n] != '4' and \
                                                   ParsedData[2][n] != '5' \
                                           and ParsedData[2][n] != '6' and ParsedData[2][n] != '7' and \
                                                   ParsedData[2][n] != '8' and ParsedData[2][n] != '9' \
                                           and ParsedData[2][n] != '-':
                                       print('error with DC - invalid char 4')
                                       sys.exit()
                                   TempString += ParsedData[2][n]
                                   if (n + 1) == len(ParsedData[2]):
                                       if int(TempString) > -32768 or int(TempString) < 32768:
                                           if DcCounter == 1:
                                               SignedHex2 = HexStr(TempString)
                                               AddOnString = ''
                                               if len(SignedHex2) < 4:
                                                   for j in range(4 - len(SignedHex2)):
                                                       AddOnString += '0'
                                               SignedHex2 = AddOnString + SignedHex2
                                               SignedHex = SignedHex + SignedHex2
                                               ListOfInstruction.append(SignedHex)
                                               Counter += 1
                                               TempString = ''
                                               DcCounter = 0

                                           elif DcCounter == 0:
                                               SignedHex = HexStr(TempString)
                                               AddOnString = ''
                                               if len(SignedHex) < 4:
                                                   for j in range(4 - len(SignedHex)):
                                                       AddOnString += '0'
                                               SignedHex = AddOnString + SignedHex
                                               ListOfInstruction.append(SignedHex)
                                               Counter += 1
                                               DcCounter = 1
                                               TempString = ''


                               else:
                                   if ParsedData[2][n] != '0' and ParsedData[2][n] != '1' and ParsedData[2][n] != '2' \
                                           and ParsedData[2][n] != '3' and ParsedData[2][n] != '4' and ParsedData[2][
                                       n] != '5' \
                                           and ParsedData[2][n] != '6' and ParsedData[2][n] != '7' and \
                                                   ParsedData[2][n] != '8' and ParsedData[2][n] != '9':
                                       print('error with DC - invalid char 3')
                                       sys.exit()
                                   TempString += ParsedData[2][n]
                                   if (n+1) == len(ParsedData[2]):
                                       if int(TempString) > -32768 or int(TempString) < 32768:
                                           if DcCounter == 1:
                                               SignedHex2 = HexStr(TempString)
                                               AddOnString = ''
                                               if len(SignedHex2) < 4:
                                                   for j in range(4 - len(SignedHex2)):
                                                       AddOnString += '0'
                                               SignedHex2 = AddOnString + SignedHex2
                                               SignedHex = SignedHex + SignedHex2
                                               ListOfInstruction.append(SignedHex)
                                               Counter += 1
                                               TempString = ''
                                               DcCounter = 0

                                           elif DcCounter == 0:
                                               SignedHex = HexStr(TempString)
                                               AddOnString = ''
                                               if len(SignedHex) < 4:
                                                   for j in range(4 - len(SignedHex)):
                                                       AddOnString += '0'
                                               SignedHex = AddOnString + SignedHex
                                               ListOfInstruction.append(SignedHex)
                                               Counter += 1
                                               DcCounter = 1
                                               TempString = ''
                                       else:
                                           print('error 2 - Value too small or large DC')
                                           sys.exit()
                           else:
                               if (n + 1) == len(ParsedData[2]):
                                   print('error last char is comma')
                               if ParsedData[2][n + 1] == ',':
                                   print('Error - Invalid DC Structure - two consecutive commas)')

                               if int(TempString) > -32768 or int(TempString) < 32768:
                                   if DcCounter == 1:
                                       SignedHex2 = HexStr(TempString)
                                       AddOnString = ''
                                       if len(SignedHex2) < 4:
                                           for j in range(4 - len(SignedHex2)):
                                               AddOnString += '0'
                                       SignedHex2 = AddOnString + SignedHex2
                                       SignedHex = SignedHex + SignedHex2
                                       ListOfInstruction.append(SignedHex)
                                       Counter += 1
                                       TempString = ''
                                       DcCounter = 0
                                       SignedHex = ''

                                   elif DcCounter == 0:
                                       SignedHex = HexStr(TempString)
                                       AddOnString = ''
                                       if len(SignedHex) < 4:
                                           for j in range(4-len(SignedHex)):
                                               AddOnString += '0'
                                       SignedHex = AddOnString + SignedHex
                                       #ListOfInstruction.append(SignedHex)
                                       #Counter += 1
                                       DcCounter = 1
                                       TempString = ''
                                   else:
                                       print('error - DC int too large or small')
                                       sys.exit()
                                     #if dc has a signed int within range then store it as a hex

                    elif ParsedData[1].upper() == 'DS':
                        ListOfInstruction.append('@')
                        Counter += 1
                        #if DS then simply append an empty string

    for k in range(len(memory)):
        if len(memory[k]) < 9:
            TempString = ''
            for l in range(9 - len(memory[k])):
                TempString += '0'
            memory[k] = '$' + TempString + memory[k][1:]
        #add 0s before locations e.g. $8 to $00000008

        for j in range(len(memory[k])):
            if memory[k][j] == 'a':
                memory[k] = memory[k][:j] + 'A' + memory[k][j+1:]
            elif memory[k][j] == 'b':
                memory[k] = memory[k][:j] + 'B' + memory[k][j + 1:]
            elif memory[k][j] == 'c':
                memory[k] = memory[k][:j] + 'C' + memory[k][j+1:]
            elif memory[k][j] == 'd':
                memory[k] = memory[k][:j] + 'D' + memory[k][j + 1:]
            elif memory[k][j] == 'e':
                memory[k] = memory[k][:j] + 'E' + memory[k][j + 1:]
            elif memory[k][j] == 'f':
                memory[k] = memory[k][:j] + 'F' + memory[k][j + 1:]
        #cap the hex letters in memory e.g.  $1c to $1C

    for k in range(len(ListOfInstruction)):
        for j in range(len(ListOfInstruction[k])):
            if ListOfInstruction[k][j] == 'a':
                ListOfInstruction[k] = ListOfInstruction[k][:j] + 'A' + ListOfInstruction[k][j+1:]
            elif ListOfInstruction[k][j] == 'b':
                ListOfInstruction[k] = ListOfInstruction[k][:j] + 'B' + ListOfInstruction[k][j + 1:]
            elif ListOfInstruction[k][j] == 'c':
                ListOfInstruction[k] = ListOfInstruction[k][:j] + 'C' + ListOfInstruction[k][j+1:]
            elif ListOfInstruction[k][j] == 'd':
                ListOfInstruction[k] = ListOfInstruction[k][:j] + 'D' + ListOfInstruction[k][j + 1:]
            elif ListOfInstruction[k][j] == 'e':
                ListOfInstruction[k] = ListOfInstruction[k][:j] + 'E' + ListOfInstruction[k][j + 1:]
            elif ListOfInstruction[k][j] == 'f':
                ListOfInstruction[k] = ListOfInstruction[k][:j] + 'F' + ListOfInstruction[k][j + 1:]
    #similarly cap the letters in list of instructions
    print(LastCall())
    OutputFile = open('OutputFile.hex', 'w')
    OutputFile.write(LastCall())


def LastCall():
    '''final algorithm. generates output from instruction code and memory'''
    newCombinedList = []
    Outputstring = 'S004000000' + RandomHex()
    WorkingString = ''
    Counter = 0
    Counter2 = -1
    for i in range(len(memory)):
        newCombinedList.append((memory[i], ListOfInstruction[i]))
    #create list of tuple of memory and list of instruction to make it easier for me

    if(len(newCombinedList)) > 0:
        Outputstring = Outputstring + '\n' + 'S1'
        Location = newCombinedList[0][0][-4:]
    else:
        Outputstring = Outputstring + '\n' + 'S9030000' + RandomHex()
    #check to see if there is nothing

    for k in newCombinedList:
        Counter2 += 1
        Counter4 = 0
        TempList = newCombinedList[Counter2 + 1:]
        TempBool = True
        if (Counter2+1) < len(newCombinedList) and Counter2 > 2:
            if (int(memory[Counter2-1][1:],16) - int(memory[Counter2][1:],16)) > 100 or \
                            (int(memory[Counter2-1][1:], 16) - int(memory[Counter2][1:], 16)) < -100:
                Outputstring = Outputstring + TwoDigit(str(int((len(WorkingString) / 2) + 3))) \
                               + Location + WorkingString + RandomHex() + '\n' + 'S1'
                WorkingString = ''
                Counter = 0
                Location = newCombinedList[Counter2][0][-4:]

        if k[1][0] == '@':
            if Counter != 0:
                for m in range(len(TempList)):
                    if TempList[m][1][0] == '@' and TempBool:
                       Counter4 += 1
                    else:
                        TempBool = False
                #Location = newCombinedList[Counter2 - 1][0][-4:]
                Outputstring = Outputstring + TwoDigit(str(int((len(WorkingString)/2) + 3))) \
                               + Location + WorkingString + RandomHex() + '\n'
                WorkingString = ''
                Counter = 0
            #used to check for ds

            if (len(newCombinedList)) == (Counter2 + 1):
                Outputstring = Outputstring + 'S9030000' + RandomHex()
                return Outputstring
            else:
                if not TempBool:
                    Outputstring = Outputstring + 'S1'
                    Location = newCombinedList[(Counter2 + Counter4 + 1)][0][-4:]
            #Used to check if we have finished running through list
            #if nor then update location and outputstring

        else:
            counter3 = 0
            for l in range(len(k[1])):
                WorkingString += k[1][l]
                Counter += 1
                counter3 += 1
                if Counter == 20:
                    Outputstring = Outputstring + '13' + Location + \
                                   WorkingString + RandomHex() + '\n' + 'S1'
                    if counter3 == len(k[1]):
                        #if the 13th character is the last character of an intstruction
                        #set location to the address next instruction
                        if (Counter2 + 1) != len(newCombinedList):
                        #to prevent error if we are on the last possible instruction
                            Location = newCombinedList[Counter2 + 1][0][-4:]
                    else:
                        Location = newCombinedList[Counter2][0][-4:]
                        #else set location to the address of current instruction
                    Counter = 0
                    WorkingString = ''
                    #if we have added 13 char to string then add to outputstring and rest
                    #workingstring and counter

                    if(len(k[1])) == (l+1):
                        if(Counter2 + 1) == len(newCombinedList):
                            if (len(newCombinedList)) == (Counter2 + 1):
                                Outputstring = Outputstring[:-2] + 'S9030000' + RandomHex()
                                return Outputstring
                    #check to see if we have finished running through list

    if len(WorkingString) != 0:
        Location = newCombinedList[Counter2][0][-4:]
        Outputstring = Outputstring + TwoDigit(str(int((len(WorkingString)/2) + 3))) + Location + WorkingString +\
            RandomHex() + '\n' + 'S1'
    Outputstring = Outputstring[:-2] + 'S9030000' + RandomHex()
    return Outputstring
    #last call to finish the process if process hasn't ended with dc or at exact intervals of 13 bits
    print(Outputstring)

passOne()
