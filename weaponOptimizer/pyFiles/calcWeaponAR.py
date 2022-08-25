import pygsheets
import simplejson as JSON
import math

gc = pygsheets.authorize(service_file='eldenring/weaponOptimizer/elden-ring-build-optimizer-c393835be6d1.json')
sh = gc.open('Elden Ring Weapon Calculator 2')
calculator = sh[0]
calculations = sh[3]
extra_sheet = sh[10]
scaling_sheet = sh[7]

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////
def getWeaponFormulaConstants():
    physical = getPhyDamageFormulaConstants()
    magic = getMagicDamageFormulaConstants()
    fire = getFireDamageFormulaConstants()
    lightning = getLightningDamageFormulaConstants()
    holy = getHolyDamageFormulaConstants()

    strength = getStrFormula()
    constants= {'physical':physical, 'magic':magic, "fire":fire, "lightning":lightning, 'holy':holy, 'strength':strength}
    return constants
    
def getStrFormula():
    #J2, F10, rowNum, extraData are constants
    J2 = bool(calculator.get_value("J2"))
    F10 = (calculations.get_value("F10"))

    rowNum = int(calculations.get_value("H2"))
    extraData = extra_sheet.get_value((rowNum,14)) #15 might be 14 here

    return {"J2":J2, "F10":F10, "extraData":extraData}
    
def getPhyDamageFormulaConstants():
    #Get scaling info
    G10 = int(calculations.get_value("G10"))
    H10 = int(calculations.get_value("H10"))
    I10 = int(calculations.get_value("I10"))
    J10 = int(calculations.get_value("J10"))
    K10 = int(calculations.get_value("K10"))

    #Physical damage group ID
    A8 = int(calculations.get_value("A8"))

    #Phy base attack  
    A4 = float(calculations.get_value("A4"))

    #Str Scaling
    rowNum = int(calculations.get_value("H2"))
    scalingCol = int(calculations.get_value("H4"))
    result = scaling_sheet.get_values((rowNum,scalingCol), (rowNum,scalingCol+4))
    X6 = [[]]
    X6[0] = [float(item) for item in result[0]]
    #print(X6[0])
    return {"A8": A8, "A4":A4, "A6":X6[0][0], "B6":X6[0][1], "C6":X6[0][2], "D6":X6[0][3], "E6":X6[0][4], "G10":G10, "H10":H10, 'I10':I10, "J10":J10, 'K10':K10}
    
def getMagicDamageFormulaConstants():
    #Get scaling info
    G12 = int(calculations.get_value("G12"))
    H12 = int(calculations.get_value("H12"))
    I12 = int(calculations.get_value("I12"))
    J12 = int(calculations.get_value("J12"))
    K12 = int(calculations.get_value("K12"))

    #Physical damage group ID
    B8 = int(calculations.get_value("B8"))

    #Phy base attack  
    B4 = float(calculations.get_value("B4"))

    #Str Scaling
    rowNum = int(calculations.get_value("H2"))
    scalingCol = int(calculations.get_value("H4"))
    result = scaling_sheet.get_values((rowNum,scalingCol), (rowNum,scalingCol+4))
    X6 = [[]]
    X6[0] = [float(item) for item in result[0]]
    return {"A8": B8, "A4":B4, "A6":X6[0][0], "B6":X6[0][1], "C6":X6[0][2], "D6":X6[0][3], "E6":X6[0][4], "G10":G12, "H10":H12, 'I10':I12, "J10":J12, 'K10':K12}
    
def getFireDamageFormulaConstants():
    #Get scaling info
    G14 = int(calculations.get_value("G14"))
    H14 = int(calculations.get_value("H14"))
    I14 = int(calculations.get_value("I14"))
    J14 = int(calculations.get_value("J14"))
    K14 = int(calculations.get_value("K14"))

    #Physical damage group ID
    C8 = int(calculations.get_value("C8"))

    #Phy base attack  
    C4 = float(calculations.get_value("C4"))

    #Str Scaling
    rowNum = int(calculations.get_value("H2"))
    scalingCol = int(calculations.get_value("H4"))
    result = scaling_sheet.get_values((rowNum,scalingCol), (rowNum,scalingCol+4))
    X6 = [[]]
    X6[0] = [float(item) for item in result[0]]
    return {"A8": C8, "A4":C4, "A6":X6[0][0], "B6":X6[0][1], "C6":X6[0][2], "D6":X6[0][3], "E6":X6[0][4], "G10":G14, "H10":H14, 'I10':I14, "J10":J14, 'K10':K14}
    
def getLightningDamageFormulaConstants():
    #Get scaling info
    G16 = int(calculations.get_value("G16"))
    H16 = int(calculations.get_value("H16"))
    I16 = int(calculations.get_value("I16"))
    J16 = int(calculations.get_value("J16"))
    K16 = int(calculations.get_value("K16"))

    #Physical damage group ID
    D8 = int(calculations.get_value("D8"))

    #Phy base attack  
    D4 = float(calculations.get_value("D4"))

    #Str Scaling
    rowNum = int(calculations.get_value("H2"))
    scalingCol = int(calculations.get_value("H4"))
    result = scaling_sheet.get_values((rowNum,scalingCol), (rowNum,scalingCol+4))
    X6 = [[]]
    X6[0] = [float(item) for item in result[0]]

    return {"A8": D8, "A4":D4, "A6":X6[0][0], "B6":X6[0][1], "C6":X6[0][2], "D6":X6[0][3], "E6":X6[0][4], "G10":G16, "H10":H16, 'I10':I16, "J10":J16, 'K10':K16}
    
def getHolyDamageFormulaConstants():
    #Get scaling info
    G18 = int(calculations.get_value("G18"))
    H18 = int(calculations.get_value("H18"))
    I18 = int(calculations.get_value("I18"))
    J18 = int(calculations.get_value("J18"))
    K18 = int(calculations.get_value("K18"))

    #Physical damage group ID
    E8 = int(calculations.get_value("E8"))

    #Phy base attack  
    E4 = float(calculations.get_value("E4"))

    #Str Scaling
    rowNum = int(calculations.get_value("H2"))
    scalingCol = int(calculations.get_value("H4"))
    result = scaling_sheet.get_values((rowNum,scalingCol), (rowNum,scalingCol+4))
    X6 = [[]]
    X6[0] = [float(item) for item in result[0]]
    return {"A8": E8, "A4":E4, "A6":X6[0][0], "B6":X6[0][1], "C6":X6[0][2], "D6":X6[0][3], "E6":X6[0][4], "G10":G18, "H10":H18, 'I10':I18, "J10":J18, 'K10':K18}
    
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////
#/*** Calculate damage given the constants*/
def getWeaponAR(str,dex,int,fai,arc,constants):
    #Get the damage for each damage type 
    phyDmg = calcDamage(str,dex,int,fai,arc,constants['physical'],constants['strength'])
    magDmg = calcDamage(str,dex,int,fai,arc,constants['magic'],constants['strength'])
    fireDmg = calcDamage(str,dex,int,fai,arc,constants['fire'],constants['strength'])
    lightDmg = calcDamage(str,dex,int,fai,arc,constants['lightning'],constants['strength'])
    holyDmg = calcDamage(str,dex,int,fai,arc,constants['holy'],constants['strength'])

    #Return the trunicated sum of all damage types
    return math.trunc(phyDmg+magDmg+fireDmg+lightDmg+holyDmg)
    
def calcDamage(str,dex,int,fai,arc,constants, strength):

    A2 = calcStr(str, strength['J2'], strength['extraData'], strength["F10"])

    #Calc variables that change based off stats
    A10 = switchX8(constants['G10'],constants['A8'],A2)
    B10 = switchX8(constants['H10'], constants['A8'], dex)
    C10 = switchX8(constants['I10'], constants['A8'], int)
    D10 = switchX8(constants['J10'], constants['A8'], fai)
    E10 = switchX8(constants['K10'], constants['A8'], arc)

    #Calc physical damage
    return constants['A4']+(constants['A4']*(constants['A6']*(A10 /100))+constants['A4']*(constants['B6']*(B10/100))+(constants['A4']*(constants['C6']*(C10/100)))+(constants['A4']*(constants['D6']*(D10/100)))+constants['A4']*(constants['E6']*(E10/100)))
    
def switchX8(scaling,A8,A2):
    A10 = None

    #Based off scaling, A8, A2, calc and return A10
    if(scaling == 1):
        if(A8 == 0):
            if(A2>80):
                #ADD(90,MULTIPLY(20,DIVIDE(A2-80,70))),
                A10 = 90+(20*((A2-80)/70))
            else:
                if(A2>60):
                    #ADD(75,MULTIPLY(15,DIVIDE(A2-60,20))),
                    A10 = 75+(15*((A2-60)/20))
                else:
                    if(A2>18):
                        # ADD(25,MULTIPLY(50,MINUS(1,POW(MINUS(1,DIVIDE(A2-18,42)),1.2)))),MULTIPLY(25,POW(DIVIDE(A2-1,17),1.2)) ))),
                        A10 = 25+(50*(1-(math.pow(1-((A2-18)/42),1.2))))  
                    else:
                        A10 = (25*math.pow((A2-1)/17,1.2))         
        elif(A8 == 1):
            if(A2>80):
                #ADD(90,MULTIPLY(20,DIVIDE(A2-80,70))),
                A10 = 90+(20*((A2-80)/70))
            else:
                if(A2>60):
                    #ADD(75,MULTIPLY(15,DIVIDE(A2-60,20))),
                    A10 = 75+(15*((A2-60)/20))
                else:
                    if(A2>20):
                        A10 = 35+(40*(1-(math.pow(1-((A2-20)/40),1.2))))  
                    else:
                        A10 = (35*math.pow((A2-1)/19,1.2))    
        elif(A8 == 2):
            if(A2>80):
                #ADD(90,MULTIPLY(20,DIVIDE(A2-80,70))),
                A10 = 90+(20*((A2-80)/70))
            else:
                if(A2>60):
                    #ADD(75,MULTIPLY(15,DIVIDE(A2-60,20))),
                    A10 = 75+(15*((A2-60)/20))
                else:
                    if(A2>18):
                        # ADD(25,MULTIPLY(50,MINUS(1,POW(MINUS(1,DIVIDE(A2-18,42)),1.2)))),MULTIPLY(25,POW(DIVIDE(A2-1,17),1.2)) ))),
                        A10 = 25+(50*(1-(math.pow(1-((A2-18)/42),1.2))))  
                    else:
                        A10 = (25*math.pow((A2-1)/17,1.2))    
        elif(A8 == 4):
            if(A2>80):
                A10 = 95+(5*((A2-80)/19))
            else:
                if(A2>50):
                    A10 = 80+(15*((A2-50)/30))
                else:
                    if(A2>20):
                        A10 = 40+(40*((A2-20)/30))
                    else:
                        A10 = 40*((A2-1)/19)
        elif(A8 == 7):
            if(A2>80):
                A10 = 90+(20*((A2-80)/70))
            else:
                if(A2>60):
                    A10 = 75+(15*((A2-60)/20))
                else:
                    if(A2>20):
                        A10 = 35+(40*(1-(math.pow(1-((A2-20)/40),1.2))))  
                    else:
                        A10 = (35*math.pow((A2-1)/19,1.2))
        elif(A8 == 8):
            if(A2>80):
                A10 = 90+(20*((A2-80)/70))
            else:
                if(A2>60):
                    A10 = 75+(15*((A2-60)/20))
                else:
                    if(A2>16):
                        A10 = 25+(50*(1-(math.pow(1-((A2-16)/44),1.2))))  
                    else:
                        A10 = (25*math.pow((A2-1)/15,1.2))
        elif(A8 == 12):
            if(A2>45):
                A10 = 75+(25*((A2-45)/54))
            else:
                if(A2>30):
                    A10 = 55+(20*((A2-30)/15))
                else:
                    if(A2>15):
                        A10 = 10+(45*((A2-15)/15))  
                    else:
                        A10 = 10*((A2-1)/14)
        elif(A8 == 14):
            if(A2>80):
                A10 = 85+(15*((A2-80)/19))
            else:
                if(A2>40):
                    A10 = 60+(25*((A2-40)/40))
                
                else:
                    if(A2>20):
                        A10 = 40+(20*((A2-20)/20))  
                    else:
                        A10 = 40*((A2-1)/19)
        elif(A8 == 15):
            if(A2>80):
                A10 = 95+(5*((A2-80)/19))
            else:
                if(A2>60):
                    A10 = 65+(30*((A2-60)/20))
                
                else:
                    if(A2>25):
                        A10 = 25+(40*((A2-25)/35))  
                    else:
                        A10 = 25*((A2-1)/24)
        elif(A8 == 16):
            if(A2>80):
                A10 = 90+(10*((A2-80)/19))
            else:
                if(A2>60):
                    A10 = 75+(15*((A2-60)/20))
                
                else:
                    if(A2>18):
                        A10 = 20+(55*((A2-18)/42)) 
                    else:
                        A10 = 20*((A2-1)/17)          
    else:
        return 0
    
    return A10
    
def calcStr(B2,J2, extraData, F10):
    #B2 is str stat
    if((J2 == False or extraData == "No") and not(F10=="Bow" or F10=="Light Bow" or F10=="Greatbow")):
        return B2
    else:
        if(B2*1.5>150):
            return 150
        else:
            return math.trunc(B2*1.5)
        
    
