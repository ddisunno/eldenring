'''
'''

#Import needed functions
import math
import pandas as pd

#Declare global variables, this being dataframes build from CSV files holding weapon information.
#CHANGE: Make these paths non-local to single machine.
df_attack = pd.read_csv(r'C:\Users\Rudyd\Desktop\Coding Projects\EldenRingBuildOptimizer\eldenring\.csv\Attack.csv')
df_scaling = pd.read_csv(r'C:\Users\Rudyd\Desktop\Coding Projects\EldenRingBuildOptimizer\eldenring\.csv\Scaling.csv')
df_extraData = pd.read_csv(r'C:\Users\Rudyd\Desktop\Coding Projects\EldenRingBuildOptimizer\eldenring\.csv\Extra_Data.csv')
df_elementParam = pd.read_csv(r'C:\Users\Rudyd\Desktop\Coding Projects\EldenRingBuildOptimizer\eldenring\.csv\AttackElementCorrectParam.csv')
df_calcCorrect = pd.read_csv(r'C:\Users\Rudyd\Desktop\Coding Projects\EldenRingBuildOptimizer\eldenring\.csv\CalcCorrectGraph_ID.csv')

################################################################################################################
def getWeaponFormulaConstants(weaponName, weaponLevel, isTwoHanding):

    #Start by getting h2 and h4
    #Needs weapon name from user entered weapon
    H2 = int(df_attack.loc[df_attack['Name'] == weaponName].index[0])
    H4 = int(df_scaling.columns.get_loc("Str +" + str(weaponLevel)))
    F4 = int(df_calcCorrect.iloc[H2,6])
    F6 = int(df_elementParam.loc[df_elementParam['ID']==F4].index[0])
    G4 = int(df_attack.columns.get_loc("Phys +" + str(weaponLevel)))

    #Get the constants for each of the five damage types. (Work is repeated here, A6-E6 is calculated 5 times)
    physical = getPhyDamageFormulaConstants(H2,H4,F6,G4)
    magic = getMagicDamageFormulaConstants(H2,H4,F6,G4)
    fire = getFireDamageFormulaConstants(H2,H4,F6,G4)
    lightning = getLightningDamageFormulaConstants(H2,H4,F6,G4)
    holy = getHolyDamageFormulaConstants(H2,H4,F6,G4)

    #Get the constants needed for the strength formula
    strength = getStrFormula(H2, isTwoHanding)

    #Return as dict, with one key-value pair for each damage type.
    constants= {'physical':physical, 'magic':magic, "fire":fire, "lightning":lightning, 'holy':holy, 'strength':strength}
    return constants
    
def getStrFormula(H2, isTwoHanding):
    #Get data on whether weapon gives str bonus based off two-handing or not. Return answer as dict.
    extraData = df_extraData.iloc[H2,13]
    return {"J2":isTwoHanding,"F10":extraData,"extraData":extraData}

################################################################################################################
#Get the contants for the five different damage types. These five functions are all functionally the same, they just return slightly different data. (A6-E6 is calculated 5 times, work is re-done for simplicity)
def getPhyDamageFormulaConstants(rowNum,scalingCol, F6, G4):
    
    #Get scaling info
    G10 = int(df_elementParam.iloc[F6,1])
    H10 = int(df_elementParam.iloc[F6,2])
    I10 = int(df_elementParam.iloc[F6,3])
    J10 = int(df_elementParam.iloc[F6,4])
    K10 = int(df_elementParam.iloc[F6,5])

    #Physical damage group ID
    A8 = int(df_calcCorrect.iloc[rowNum,1])
    
    #Phy base attack  
    A4 = float(df_attack.iloc[rowNum,G4])
    
    #Get whether or not the weapon scales physical damage with each stat. This can be cleaned up.
    result = df_scaling.iloc[rowNum,scalingCol:scalingCol+5]
    X6 = [[]]
    X6[0] = [float(item) for item in result]
    
    #Return answer as a dict of all constants.
    return {"A8":A8,"A4":A4,"A6":X6[0][0],"B6":X6[0][1],"C6":X6[0][2],"D6":X6[0][3],"E6":X6[0][4],"G10":G10,"H10":H10,'I10':I10,"J10":J10,'K10':K10}
    
def getMagicDamageFormulaConstants(rowNum,scalingCol,F6,G4):
    #Get scaling info
    G12 = int(df_elementParam.iloc[F6,6])
    H12 = int(df_elementParam.iloc[F6,7])
    I12 = int(df_elementParam.iloc[F6,8])
    J12 = int(df_elementParam.iloc[F6,9])
    K12 = int(df_elementParam.iloc[F6,10])

    #Physical damage group ID
    B8 = int(df_calcCorrect.iloc[rowNum,2])

    #Phy base attack  
    B4 = float(df_attack.iloc[rowNum,G4+1])

    #Str Scaling
    result = df_scaling.iloc[rowNum,scalingCol:scalingCol+5]
    X6 = [[]]
    X6[0] = [float(item) for item in result]
    return {"A8": B8, "A4":B4, "A6":X6[0][0], "B6":X6[0][1], "C6":X6[0][2], "D6":X6[0][3], "E6":X6[0][4], "G10":G12, "H10":H12, 'I10':I12, "J10":J12, 'K10':K12}
    
def getFireDamageFormulaConstants(rowNum,scalingCol, F6, G4):
    #Get scaling info
    G14 = int(df_elementParam.iloc[F6,11])
    H14 = int(df_elementParam.iloc[F6,12])
    I14 = int(df_elementParam.iloc[F6,13])
    J14 = int(df_elementParam.iloc[F6,14])
    K14 = int(df_elementParam.iloc[F6,15])

    #Physical damage group ID
    C8 = int(df_calcCorrect.iloc[rowNum,3])

    #Phy base attack  
    C4 = float(df_attack.iloc[rowNum,G4+2])

    #Str Scaling
    #rowNum = int(calculations.get_value("H2"))
    #scalingCol = int(calculations.get_value("H4"))
    result = df_scaling.iloc[rowNum,scalingCol:scalingCol+5]
    X6 = [[]]
    X6[0] = [float(item) for item in result]
    return {"A8": C8, "A4":C4, "A6":X6[0][0], "B6":X6[0][1], "C6":X6[0][2], "D6":X6[0][3], "E6":X6[0][4], "G10":G14, "H10":H14, 'I10':I14, "J10":J14, 'K10':K14}
    
def getLightningDamageFormulaConstants(rowNum,scalingCol, F6, G4):
    #Get scaling info
    G16 = int(df_elementParam.iloc[F6,16])
    H16 = int(df_elementParam.iloc[F6,17])
    I16 = int(df_elementParam.iloc[F6,18])
    J16 = int(df_elementParam.iloc[F6,19])
    K16 = int(df_elementParam.iloc[F6,20])

    #Physical damage group ID
    D8 = int(df_calcCorrect.iloc[rowNum,4])

    #Phy base attack  
    D4 = float(df_attack.iloc[rowNum,G4+3])

    #Str Scaling
    #rowNum = int(calculations.get_value("H2"))
    #scalingCol = int(calculations.get_value("H4"))
    result = df_scaling.iloc[rowNum,scalingCol:scalingCol+5]
    X6 = [[]]
    X6[0] = [float(item) for item in result]

    return {"A8": D8, "A4":D4, "A6":X6[0][0], "B6":X6[0][1], "C6":X6[0][2], "D6":X6[0][3], "E6":X6[0][4], "G10":G16, "H10":H16, 'I10':I16, "J10":J16, 'K10':K16}
    
def getHolyDamageFormulaConstants(rowNum,scalingCol, F6, G4):
    #Get scaling info
    G18 = int(df_elementParam.iloc[F6,21])
    H18 = int(df_elementParam.iloc[F6,22])
    I18 = int(df_elementParam.iloc[F6,23])
    J18 = int(df_elementParam.iloc[F6,24])
    K18 = int(df_elementParam.iloc[F6,25])

    #Physical damage group ID
    E8 = int(df_calcCorrect.iloc[rowNum,5])

    #Phy base attack  
    E4 = float(df_attack.iloc[rowNum,G4+4])

    #Str Scaling
    #rowNum = int(calculations.get_value("H2"))
    #scalingCol = int(calculations.get_value("H4"))
    result = df_scaling.iloc[rowNum,scalingCol:scalingCol+5]
    X6 = [[]]
    X6[0] = [float(item) for item in result]
    return {"A8": E8, "A4":E4, "A6":X6[0][0], "B6":X6[0][1], "C6":X6[0][2], "D6":X6[0][3], "E6":X6[0][4], "G10":G18, "H10":H18, 'I10':I18, "J10":J18, 'K10':K18}
    
################################################################################################################
### Calculate damage given the constants ###
def getWeaponAR(str,dex,int,fai,arc,constants):

    #Get the damage for each damage type 
    phyDmg = calcDamage(str,dex,int,fai,arc,constants['physical'],constants['strength'])
    magDmg = calcDamage(str,dex,int,fai,arc,constants['magic'],constants['strength'])
    fireDmg = calcDamage(str,dex,int,fai,arc,constants['fire'],constants['strength'])
    lightDmg = calcDamage(str,dex,int,fai,arc,constants['lightning'],constants['strength'])
    holyDmg = calcDamage(str,dex,int,fai,arc,constants['holy'],constants['strength'])

    #Return the trunicated sum of all damage types to get the total weapon AR.
    return math.trunc(phyDmg+magDmg+fireDmg+lightDmg+holyDmg)
    
#Called to calculate the total damage from each different damage type (Physical, Fire, etc.). The total from all damage types is added in getWeaponAR()
def calcDamage(str,dex,int,fai,arc,constants, strength):

    #Calculate if the strength stat gets a bonus, and if so, the value of that bonus. 
    A2 = calcStr(str, strength['J2'], strength['extraData'], strength["F10"])

    #Calc variables that change based off stats
    A10 = switchX8(constants['G10'],constants['A8'],A2)
    B10 = switchX8(constants['H10'], constants['A8'], dex)
    C10 = switchX8(constants['I10'], constants['A8'], int)
    D10 = switchX8(constants['J10'], constants['A8'], fai)
    E10 = switchX8(constants['K10'], constants['A8'], arc)

    #Calculate damage
    return constants['A4']+(constants['A4']*(constants['A6']*(A10 /100))+constants['A4']*(constants['B6']*(B10/100))+(constants['A4']*(constants['C6']*(C10/100)))+(constants['A4']*(constants['D6']*(D10/100)))+constants['A4']*(constants['E6']*(E10/100)))

#Part of the formula- calculates how well a stat increases damage based off of how well the weapon scales. 
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

#Calculate if the strength stat gets a bonus or not, and what that bonus is.
def calcStr(B2,J2, extraData, F10):
    #B2 is str stat
    if((J2 == False or extraData == "No") and not(F10=="Bow" or F10=="Light Bow" or F10=="Greatbow")):
        return B2
    else:
        if(B2*1.5>150):
            return 150
        else:
            return math.trunc(B2*1.5)
        
    
