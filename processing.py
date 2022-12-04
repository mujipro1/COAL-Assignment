
class Data:
    priority = 0
    opcode = '          '
    PCReg = ''
    IRReg = ''
    regList = ['01', "02", '03', '04', '05', '06', '07', '08']
    memorylist = ['01', '02', '03', '04', '05', '06', '07', '08',
                  '09', '10', '11', '12', '13', '14', '15', '16']
    highlighter = ['x','x','x','x','x','x']
  
  
    hexList = [str(i) for i in range(10)]
    for i in range(65,71):
        hexList.append(chr(i))

    def HextoDec(self, data):
        return int(data, base=16)

    def DectoHex(self, data, bit):
        #bit 0 : 8 bit
        #bit 1 : 16 bit
        data = self.HextoDec(data)
        data = hex(data)
        x=''
  
        for i in range(2,len(data)):
            x+=data[i]
        data = x.upper()
        
        if(bit == 0 and len(data)<2):
            return '0'+ data
        elif (bit == 1 and len(data)<4):
            for i in range(4-len(data)):
                data = '0'+data
            return data
        
       

    def XRegs(self, xreg, data='xxxx'):
        hdata = data[0]+data[1]
        ldata = data[2]+data[3]
        
        if(xreg == 'AX'):
            return [hdata,ldata, 0,4]
        if(xreg == 'BX'):
            return [hdata,ldata, 1,5]
        if(xreg == 'CX'):
            return [hdata,ldata, 2,6]
        if(xreg == 'DX'):
            return [hdata,ldata, 3,7]

    def swork(self, s):
        if(s[0] != '[' or s[-1] != ']'):
            return "Syntax Error"
        s = s.replace('[','')
        s = s.replace(']','')
        return s

class Instruction:
    string = ""
    PrevObj = Data()
    Obj = Data()

    XRegsList = ['AX','BX','CX','DX']
    InstructionList = ["MOV", "ADD", "SUB", "INC", "DEC","MUL", "DIV", "OR"]
    RegList = ["AH", "BH", "CH", "DH", "AL",
               "BL", "CL", "DL"]
    MemList = ["00000","00001", "00002", "00003", "00004", "00005", "00006", "00007",
               "00008", "00009", "0000A", "0000B", "0000C", "0000D", "0000E", "0000F"]

    def __init__(self, string, prev_Obj):
        self.string = string
        if (prev_Obj.priority >= 3):
            prev_Obj.priority = 0
        self.PrevObj = prev_Obj
        self.Obj = self.PrevObj
        pass

    def split_string(self):

        error = "invalid"
        string = self.string
        Strlist = string.split(" ", 1)
        if (len(Strlist) != 2):
            return error

        regList = Strlist[1].split(",")
        inst = Strlist[0]
        opr1 = regList[0].replace(' ', '')
        opr2 = 0

        if ("" in regList and string.find(",") != -1):
            return error

        if (len(regList) > 1):
            if (string.find(",") == -1):
                return error
            else:
                opr2 = regList[1].replace(' ', '')

        if (opr2 != 0):
            return ([inst, opr1, opr2])
        else:
            return ([inst, opr1])

    def working(self, insList):
        errorType1 = "Invalid Instruction"
        errorType2 = "Invalid Operand"
        inst = ''
        opr1 = ''
        opr2 = ''
        if (len(insList) == 3):
            inst = insList[0].upper()
            opr1 = insList[1].upper()
            opr2 = insList[2].upper()
        elif (len(insList) == 2):
            inst = insList[0].upper()
            opr1 = insList[1].upper()

        if (inst.upper() not in self.InstructionList):
            return errorType1
   
    #Instruction Set

        if (inst.upper() == "MOV"):
            a = self.mov(opr1, opr2)
            if (type(a) == str):
                return a

        if (inst.upper() == "INC" or inst.upper() == "DEC"):
            a = self.incDec(opr1, inst)
            if (type(a) == str):
                return a

        if (inst.upper() == "ADD" or inst.upper()=="SUB"):
            a = self.addSub(inst, opr1, opr2)
            if (type(a) == str):
               return a

        if (inst.upper() == "MUL"):
            self.mul(opr1)
       
        if (inst.upper() == "DIV"):
            self.div(opr1)
       
        if (inst.upper() == "OR"):
            self.orF(opr1, opr2)
        return self.Obj


    def mov(self, opr1, opr2):
        des_index = ''
        source_index = ''
        source_indexh = ''
        source_indexl = ''
        des_indexh = ''
        des_indexl= ''

        # Case'1' : MOV REG REG

        if(opr1 in self.XRegsList and opr2 in self.XRegsList):
            sourcelist = self.Obj.XRegs(opr2)

            sourceDatah = self.PrevObj.regList[sourcelist[2]]
            sourceDatal = self.PrevObj.regList[sourcelist[3]]
            
            deslist = self.Obj.XRegs(opr1)

            self.Obj.regList[deslist[2]] = sourceDatah
            self.Obj.regList[deslist[3]] = sourceDatal
            self.Obj.opcode = '1000101111'
            self.Obj.highlighter = [sourcelist[2],deslist[2],'x','x',sourcelist[3],deslist[3]]

        elif (opr1 in self.RegList and opr2 in self.RegList):
            source_index = self.RegList.index(opr2)
            des_index = self.RegList.index(opr1)
            
            sourceData = self.PrevObj.regList[source_index]

            if(source_index<=7 and des_index>7):
                sourceData = self.Obj.DectoHex(sourceData,1)

            self.Obj.regList[des_index] = sourceData
            self.Obj.opcode = '1000101011'
            self.Obj.highlighter = [source_index,des_index,'x','x','x','x']
            

        elif (opr1 not in self.RegList and opr2 not in self.RegList and opr1 not in self.XRegsList and opr2 not in self.XRegsList):
            return "Error 400 : Invalid X Operands"

        elif ((opr1 in self.RegList and opr2 in self.XRegsList) or (opr2 in self.RegList and opr1 in self.XRegsList)):
            return "Operands size doesn't match"

        elif(opr1 in self.RegList or opr2 in self.RegList):
            s = ''
                              
            if(opr1 in self.RegList and opr2[0] == '['):
                des_index = self.RegList.index(opr1)                  
                s = self.Obj.swork(opr2)
                if(s == "Syntax Error"):
                    return s
        
        # Case 2: Mov Reg [Mem]
                #check s == hex
                if(s in self.MemList):
                    memLoc = s
                    
            # Case 3: MOV Reg [Reg]

                elif(s in self.RegList):
                    idx = self.RegList.index(s)
                    memLoc = self.PrevObj.regList[int(idx)] 
                    memLoc = '000'+memLoc
                
                elif(s in self.XRegsList):
                    temp = self.Obj.XRegs(s)
                    memLoc = self.PrevObj.regList[temp[3]]
                    des_index = temp[3]
                    memLoc = '000'+memLoc

                elif(s not in self.RegList and s not in self.MemList and s not in self.XRegsList):
                    return "401: Invalid Memory Location"

                if(memLoc not in self.MemList):
                    return "401: Invalid Memory Location"
                else:
                    source_index = self.MemList.index(memLoc)
                    sourceData = self.PrevObj.memorylist[source_index]
                    self.Obj.regList[des_index] = sourceData
                    self.Obj.opcode = '1000101000'
                    self.Obj.highlighter = ['x',des_index,source_index,'x','x','x']
            
            elif(opr2 in self.RegList and opr1[0] == '['):
                source_index = self.RegList.index(opr2)
                s = opr1
                if(s[0] != '[' or s[-1] != ']'):
                    return "Syntax Error"
                s = s.replace('[','')
                s = s.replace(']','')

                #check hex here 
        
        #Case 4: MOV [Mem] Reg
        
                if(s in self.MemList):
                    memLoc = s
                  
        #Case 5: MOV [Reg] Reg

                elif(s in self.RegList):
                    idx = self.RegList.index(s)
                    memLoc = self.PrevObj.regList[int(idx)] 
                  

                elif(s in self.XRegsList):
                    temp = self.Obj.XRegs(s)
                    memLoc = self.PrevObj.regList[temp[3]]
                    memLoc = '000'+memLoc
                

                elif(s not in self.RegList and s not in self.MemList and s not in self.XRegsList):
                    return "401: Invalid Memory Location"

                if(memLoc not in self.MemList):
                    return "401 : Invalid Memory Location"
                else:
                    des_index = self.MemList.index(memLoc)

                sourceData = self.PrevObj.regList[source_index]
                self.Obj.memorylist[des_index] = sourceData
                self.Obj.opcode = '1000100000'
                self.Obj.highlighter = [source_index,'x','x',des_index,'x','x']
    
    

        elif(opr1 in self.XRegsList or opr2 in self.XRegsList):           
            if(opr1 in self.XRegsList and opr2[0] == '['):
                deslist = self.Obj.XRegs(opr1)
                des_indexh = deslist[2]
                des_indexl = deslist[3] 

                s = self.Obj.swork(opr2)
                if(s == "Syntax Error"):
                    return s
        
        # Case 2: Mov Reg [Mem]
                #check s == hex
                if(s in self.MemList):
                    memLoc = s

        # Case 3: MOV Reg [Reg]

                elif(s in self.RegList):
                    idx = self.RegList.index(s)
                    memLoc = self.PrevObj.regList[int(idx)] 
                    memLoc = '000'+memLoc

                elif (s in self.XRegsList):
                    temp = self.Obj.XRegs(s)
                    memLoc = self.PrevObj.regList[temp[3]]
                    memLoc = '000'+memLoc

                elif(s not in self.RegList and s not in self.MemList and s not in self.XRegsList):
                    return "401: Invalid Memory Location"

                if(memLoc not in self.MemList):
                    return "401: Invalid Memory Location"
                else:
                    
                    source_index = self.MemList.index(memLoc)
                    sourceDatah = self.PrevObj.memorylist[source_index]
                    if(source_index==15):
                        sourceDatal = '00' 
                    else:
                        sourceDatal = self.PrevObj.memorylist[source_index+1]
                    self.Obj.regList[des_indexl] = sourceDatal
                    self.Obj.regList[des_indexh] = sourceDatah
                    self.Obj.opcode = '1000101100'
                    self.Obj.highlighter = [des_indexl,des_indexh,source_index,source_index+1,'x','x']


            elif(opr2 in self.XRegsList and opr1[0] == '['):
                temp = self.Obj.XRegs(opr2)
                source_indexh = temp[2]
                source_indexl = temp[3]
                s = opr1
                if(s[0] != '[' or s[-1] != ']'):
                    return "Syntax Error"
                s = s.replace('[','')
                s = s.replace(']','')

                #check hex here 
        
        #Case 4: MOV [Mem] Reg
        
                if(s in self.MemList):
                    memLoc = s
                
        #Case 5: MOV [Reg] Reg

                elif(s in self.RegList):
                    idx = self.RegList.index(s)
                    memLoc = self.PrevObj.regList[int(idx)] 

                elif(s in self.XRegsList):
                    temp = self.Obj.XRegs(s)
                    memLoc = self.PrevObj.regList[temp[3]]
                    memLoc = '000'+memLoc

                elif(s not in self.RegList and s not in self.MemList and s not in self.XRegsList):
                    return "401: Invalid Memory Location"

                if(memLoc not in self.MemList):
                    return "401 : Invalid Memory Location"
                else:
                    des_index = self.MemList.index(memLoc)

                sourceDatah = self.PrevObj.regList[source_indexh]
                sourceDatal = self.PrevObj.regList[source_indexl]

                    
                self.Obj.memorylist[des_index] = sourceDatah
                self.Obj.memorylist[des_index+1] = sourceDatal
                self.Obj.opcode = '1000100100'
                self.Obj.highlighter = [source_indexh,source_indexl,des_index,des_index+1,'x','x']

            
        #Case 6 : Mov Reg Imm

        if((opr1 in self.RegList or opr1 in self.XRegsList) and (opr2 not in self.RegList and opr2 not in self.XRegsList and opr2[0] != '[')):
            if(opr1 in self.XRegsList):
                temp = self.Obj.XRegs(opr1)
                des_indexh = temp[2]
                des_indexl = temp[3]
                
                self.Obj.regList[des_indexh] = opr2[0]+opr2[1]
                self.Obj.regList[des_indexl] = opr2[2]+opr2[3]
                self.Obj.highlighter = [des_indexh,des_indexl,'x','x','x','x']                
                self.Obj.opcode = '1100011100'
            
            if(opr1 in self.RegList):
                source_index = self.RegList.index(opr1)
                
                self.Obj.opcode = '1100011000'
                self.Obj.regList[source_index] = opr2
                self.Obj.highlighter = [source_index,'x','x','x','x','x']                


    #Case 7: INC [Reg]
    #Case 8: DEC [Reg]

    def incDec(self, opr1, inst):
        source_index = ''
        idx = ''
        if (opr1[0] == '[' and opr1[-1]==']'):
            s = opr1
            s = s.replace('[','')
            s = s.replace(']','')
            if (s not in self.RegList and s not in self.XRegsList):
                return "Invalid Register"
            else:
                if(s in self.XRegsList):
                   temp = self.Obj.XRegs(s)
                   memLoc = self.PrevObj.regList[int(temp[3])] 
                   idx = temp[3]
                   memLoc = '000'+memLoc
                   w =  '1'
                elif(s in self.RegList):
                    idx = self.RegList.index(s)
                    memLoc = self.PrevObj.regList[int(idx)] 
                    memLoc = '000'+memLoc
                    w = '0'

                if(memLoc not in self.MemList):
                    return "401: Invalid Memory Location"
                else:
                    source_index = self.MemList.index(memLoc)
                data = int(self.Obj.memorylist[source_index], base=16)
                if (inst == 'INC'):
                    data += 1
                if (inst == 'DEC'):
                    data -= 1
                data = self.Obj.DectoHex(str(data),0)
                self.Obj.opcode = '1111111'+w+'00'
                self.Obj.memorylist[source_index] = str(data)
                self.Obj.highlighter = ['x',idx, source_index,'x','x','x']
            

        elif(opr1 not in self.RegList and opr1 not in self.XRegsList):
            return "Invalid Operand"

    #Case 9: INC Reg
    #Case 10: DEC Reg

        else:
            if(opr1 in self.XRegsList):
                temp = self.Obj.XRegs(opr1)
                source_index = temp[3]
            else:
                source_index = self.RegList.index(opr1)
            data = int(self.PrevObj.regList[source_index], base=16)
            if (inst == 'INC'):
                    data += 1
            if (inst == 'DEC'):
                    data -= 1
            data = self.Obj.DectoHex(str(data),0)
            self.Obj.regList[source_index] = str(data)
            self.Obj.opcode = '001000----'
            self.Obj.highlighter = [source_index,'x','x','x','x','x']

    def addData(self, first, second, start, end):
        data = int(first+second, base =16)
        data2 = int(start+end, base =16)
        return hex(data+data2)

    def subData(self, first, second, start, end):
        data = int(first+second, base =16)
        data2 = int(start+end, base =16)
        return hex(data-data2)


    def addSub(self, inst, opr1, opr2):     
        desData = ''
        source_index = 0
        des_index = 0
        sourceData = ''
    
    #Case 11: ADD Reg Reg
    #Case 12: SUB Reg Reg

        if(opr1 not in self.RegList and opr2 not in self.RegList and opr1 not in self.XRegsList and opr2 not in self.XRegsList):
                return "403 : Invalid Operands"

        elif(opr1 in self.RegList and opr2 in self.RegList):
            source_index = self.RegList.index(opr2)
            des_index = self.RegList.index(opr1)
            
            sourceData = (self.PrevObj.regList[source_index])
            sourceData = self.Obj.HextoDec(sourceData)
            desData = (self.PrevObj.regList[des_index])
            desData = self.Obj.HextoDec(desData)

            if(inst == 'ADD'):
                data = self.Obj.DectoHex(str(sourceData+desData),0)
                self.Obj.regList[des_index] = str(data)
            if(inst == 'SUB'):
                data = self.Obj.DectoHex(str(desData - sourceData),0)
                self.Obj.regList[des_index] = str(data)

            self.Obj.opcode = '0000001011'
            self.Obj.highlighter = [source_index,des_index,'x','x','x','x']
          
        elif(opr1 in self.XRegsList and opr2 in self.XRegsList):            
            desList = self.Obj.XRegs(opr1)
            des_indexh = desList[2]
            des_indexl = desList[3]

            sourceList = self.Obj.XRegs(opr2)
            source_indexh = sourceList[2]
            source_indexl = sourceList[3]

            sourceDatah = int(self.PrevObj.regList[source_indexh])
            sourceDatal = int(self.PrevObj.regList[source_indexl])
            desDatah = int(self.PrevObj.regList[des_indexh])
            desDatal = int(self.PrevObj.regList[des_indexl])

            if(inst == 'ADD'):
                data = self.addData(sourceDatah,sourceDatal,desDatah,desDatal)

            if(inst == 'SUB'):
                data = self.subData(sourceDatah,sourceDatal,desDatah,desDatal)
            
            self.Obj.regList[des_indexh] = data[0]+data[1]
            self.Obj.regList[des_indexl] = data[2]+data[3]
            self.Obj.opcode = '0000001111'
            self.Obj.highlighter = [source_indexh,des_indexh,'x','x',source_indexl,des_indexl]
          

    #Case 13: Add Reg [Reg]
    #Case 14: Sub Reg [Reg]  
        
        elif((opr1 in self.RegList or opr2 in self.RegList) and(opr1[0] == '[' or opr2[0] == '[')):

            if (opr1 in self.RegList and opr2[0] == '['):
                des_index = self.RegList.index(opr1)
                s = opr2
                if(s[0] != '[' or s[-1] != ']'):
                    return "Syntax Error"
                s = s.replace('[','')
                s = s.replace(']','')

    # Case 15: Add Reg [Mem]
    # Case 16: Sub Reg [Mem]

                if(s in self.MemList):
                    memLoc = s

                elif(s in self.RegList):
                    idx = self.RegList.index(s)
                    memLoc = self.PrevObj.regList[int(idx)] 

                elif(s not in self.MemList and s not in self.RegList):
                    return "Error 401 : Invalid Memory Location"
                else:
                    source_index = self.MemList.index(memLoc)

                sourceData = int(self.PrevObj.memorylist[source_index])
                desData = int(self.PrevObj.regList[des_index])

                if(inst == "ADD"):
                    self.Obj.regList[des_index] = str(sourceData+desData)
                if(inst == "SUB"):
                    self.Obj.regList[des_index] = str(desData - sourceData)
                
                self.Obj.opcode = '0000000000'           
                self.Obj.highlighter = ['x',des_index,source_index,'x','x','x']
        
    #Case 17: Add [Reg] Reg
    #Case 18: Sub [Reg] Reg

            if(opr2 in self.RegList and opr1[0] == '['):
                source_index = self.RegList.index(opr2)

                s = opr1
                if(s[0] != '[' or s[-1] != ']'):
                    return "Syntax Error"
                s = s.replace('[','')
                s = s.replace(']','')


    # Case 19: Add [Mem] Reg
    # Case 20: Sub [Mem] Reg

                memLoc = ''
                if(s in self.MemList):
                    memLoc = s

                if(s in self.RegList):
                    idx = self.RegList.index(s)
                    memLoc = self.PrevObj.regList[int(idx)]
                    memLoc = '000'+memLoc

                if(memLoc not in self.MemList):
                    return "Error 401 : Invalid Memory Location"
                else:
                    des_index = self.MemList.index(memLoc)

                sourceData = int(self.PrevObj.regList[source_index])
                desData = int(self.PrevObj.memorylist[des_index])

                if(inst == "ADD"):
                    self.Obj.memorylist[des_index] = str(sourceData + desData)
                if(inst == "SUB"):
                    self.Obj.memorylist[des_index] = str(desData - sourceData)
                
                self.Obj.opcode = '0000000100'           
                self.Obj.highlighter = [source_index,'x','x',des_index,'x','x']
    

    #Case 21: Add Reg Imm
    #Case 22: Sub Reg Imm
    

        elif(opr1 in self.RegList and opr2[0] != '['):
    
            source_index = self.RegList.index(opr1)
            if(len(opr2) > 2):
                return "Invalid Data"
            else:
                if(inst == 'ADD'):
                    data = int(self.Obj.regList[source_index])
                    data += self.Obj.HextoDec(opr2)
                    self.Obj.regList[source_index] = data
                if(inst == 'SUB'):
                    data = int(self.Obj.regList[source_index])
                    data -= int(opr2)
                    self.Obj.regList[source_index] = data

                self.Obj.opcode = '100000 00 00'           
                self.Obj.highlighter = [source_index,'x','x','x','x','x']