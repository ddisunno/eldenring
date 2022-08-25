/////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/**
 * Functions for getting the constants from the spreadsheet
 */
function getWeaponFormulaConstants(){
var physical = getPhyDamageFormulaConstants();
var magic = getMagicDamageFormulaConstants();
var fire = getFireDamageFormulaConstants();
var lightning = getLightningDamageFormulaConstants();
var holy = getHolyDamageFormulaConstants();

var strength = getStrFormula();
var constants= {'physical':physical, 'magic':magic, "fire":fire, "lightning":lightning, 'holy':holy, 'strength':strength}
return constants;
}

function getStrFormula(){
//J2, F10, rowNum, extraData are constants
var J2 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculator!J2").getValue();
var F10 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!F10").getValue();

var rowNum = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!H2").getValue();
var extraData = SpreadsheetApp.getActiveSpreadsheet().getSheets()[10].getRange(rowNum,14).getValue(); //15 might be 14 here

return {"J2":J2, "F10":F10, "extraData":extraData};
}

function getPhyDamageFormulaConstants(){

//Get scaling info
var G10 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!G10").getValue();
var H10 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!H10").getValue();
var I10 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!I10").getValue();
var J10 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!J10").getValue();
var K10 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!K10").getValue();

//Physical damage group ID
var A8 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!A8").getValue()

//Phy base attack  
var A4 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!A4").getValue();

//Str Scaling
var rowNum = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!H2").getValue();
var scalingCol = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!H4").getValue();
var X6 = SpreadsheetApp.getActiveSpreadsheet().getSheets()[7].getRange(rowNum,scalingCol,1,5).getValues();

return {"A8": A8, "A4":A4, "A6":X6[0][0], "B6":X6[0][1], "C6":X6[0][2], "D6":X6[0][3], "E6":X6[0][4], "G10":G10, "H10":H10, 'I10':I10, "J10":J10, 'K10':K10};
}

function getMagicDamageFormulaConstants(){

//Get scaling
var G12 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!G12").getValue();
var H12 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!H12").getValue();
var I12 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!I12").getValue();
var J12 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!J12").getValue();
var K12 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!K12").getValue();

//Magic Group ID
var B8 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!B8").getValue();

//Base magic dmg
var B4 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!B4").getValue();

//Scaling
var rowNum = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!H2").getValue();
var scalingCol = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!H4").getValue();
var X6 = SpreadsheetApp.getActiveSpreadsheet().getSheets()[7].getRange(rowNum,scalingCol,1,5).getValues();

return {"A8": B8, "A4":B4, "A6":X6[0][0], "B6":X6[0][1], "C6":X6[0][2], "D6":X6[0][3], "E6":X6[0][4], "G10":G12, "H10":H12, 'I10':I12, "J10":J12, 'K10':K12};
}

function getFireDamageFormulaConstants(){

//Scaling info
var G14 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!G14").getValue();
var H14 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!H14").getValue();
var I14 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!I14").getValue();
var J14 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!J14").getValue();
var K14 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!K14").getValue();

//Fire group ID
var C8 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!C8").getValue();

//Base Fire damage
var C4 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!C4").getValue();

//Scaling
var rowNum = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!H2").getValue();
var scalingCol = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!H4").getValue();
var X6 = SpreadsheetApp.getActiveSpreadsheet().getSheets()[7].getRange(rowNum,scalingCol,1,5).getValues(); 

return {"A8": C8, "A4":C4, "A6":X6[0][0], "B6":X6[0][1], "C6":X6[0][2], "D6":X6[0][3], "E6":X6[0][4], "G10":G14, "H10":H14, 'I10':I14, "J10":J14, 'K10':K14};
}

function getLightningDamageFormulaConstants(){

//Saling info
var G16 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!G16").getValue();
var H16 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!H16").getValue();
var I16 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!I16").getValue();
var J16 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!J16").getValue();
var K16 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!K16").getValue();

//Lightning group ID
var D8 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!D8").getValue();

//Base lightning dmg
var D4 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!D4").getValue();

//Scaling
var rowNum = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!H2").getValue();
var scalingCol = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!H4").getValue();
var X6 = SpreadsheetApp.getActiveSpreadsheet().getSheets()[7].getRange(rowNum,scalingCol,1,5).getValues(); 

return {"A8": D8, "A4":D4, "A6":X6[0][0], "B6":X6[0][1], "C6":X6[0][2], "D6":X6[0][3], "E6":X6[0][4], "G10":G16, "H10":H16, 'I10':I16, "J10":J16, 'K10':K16};
}

function getHolyDamageFormulaConstants(){

//Sclaing info
var G18 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!G18").getValue();
var H18 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!H18").getValue();
var I18 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!I18").getValue();
var J18 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!J18").getValue();
var K18 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!K18").getValue();

//Holy group ID
var E8 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!E8").getValue();

//Base Holy Dmg
var E4 = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!E4").getValue();

//Scaling
var rowNum = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!H2").getValue();
var scalingCol = SpreadsheetApp.getActiveSpreadsheet().getRange("Calculations!H4").getValue();
var X6 = SpreadsheetApp.getActiveSpreadsheet().getSheets()[7].getRange(rowNum,scalingCol,1,5).getValues(); 

return {"A8": E8, "A4":E4, "A6":X6[0][0], "B6":X6[0][1], "C6":X6[0][2], "D6":X6[0][3], "E6":X6[0][4], "G10":G18, "H10":H18, 'I10':I18, "J10":J18, 'K10':K18};
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*** Calculate damage given the constants*/
function getWeaponAR(str,dex,int,fai,arc,constants){

//Get the damage for each damage type 
var phyDmg = calcDamage(str,dex,int,fai,arc,constants['physical'],constants['strength']);
var magDmg = calcDamage(str,dex,int,fai,arc,constants['magic'],constants['strength'])
var fireDmg = calcDamage(str,dex,int,fai,arc,constants['fire'],constants['strength'])
var lightDmg = calcDamage(str,dex,int,fai,arc,constants['lightning'],constants['strength'])
var holyDmg = calcDamage(str,dex,int,fai,arc,constants['holy'],constants['strength'])

//Return the trunicated sum of all damage types
return Math.trunc(phyDmg+magDmg+fireDmg+lightDmg+holyDmg);
}

function calcDamage(str,dex,int,fai,arc,constants, strength){

var A2 = calcStr(str, strength['J2'], strength['extraData'], strength["F10"]);

//Calc variables that change based off stats
var A10 = switchX8(constants['G10'],constants['A8'],A2);
var B10 = switchX8(constants['H10'], constants['A8'], dex)
var C10 = switchX8(constants['I10'], constants['A8'], int);
var D10 = switchX8(constants['J10'], constants['A8'], fai);
var E10 = switchX8(constants['K10'], constants['A8'], arc);

//Calc physical damage
return constants['A4']+ (constants['A4']*(constants['A6']*(A10 /100)) + constants['A4']*(constants['B6']*(B10/100)) + (constants['A4']*(constants['C6']*(C10/100))) +(constants['A4']*(constants['D6']*(D10/100))) + constants['A4']*(constants['E6']*(E10/100)));
}

function switchX8(scaling,A8,A2){
var A10 = null;

//Based off scaling, A8, A2, calc and return A10
if(scaling == 1){
    switch(A8){
    case 0:
        if(A2>80){
            //ADD(90,MULTIPLY(20,DIVIDE(A2-80,70))),
            A10 = 90+(20*((A2-80)/70))
        }
        else{
            if(A2>60){
            //ADD(75,MULTIPLY(15,DIVIDE(A2-60,20))),
            A10 = 75+(15*((A2-60)/20))
            }
            else{
            if(A2>18){
                //ADD(25,MULTIPLY(50,MINUS(1,POW(MINUS(1,DIVIDE(A2-18,42)),1.2)))),MULTIPLY(25,POW(DIVIDE(A2-1,17),1.2)) ))),
                A10 = 25+(50*(1-(Math.pow(1-((A2-18)/42),1.2))))  
            }
            else{
                A10 = (25*Math.pow((A2-1)/17,1.2))
            }
            }
        }
        break;
        
    case 1:
        if(A2>80){
            //ADD(90,MULTIPLY(20,DIVIDE(A2-80,70))),
            A10 = 90+(20*((A2-80)/70))
        }
        else{
            if(A2>60){
            //ADD(75,MULTIPLY(15,DIVIDE(A2-60,20))),
            A10 = 75+(15*((A2-60)/20))
            }
            else{
            if(A2>20){
                A10 = 35+(40*(1-(Math.pow(1-((A2-20)/40),1.2))))  
            }
            else{
                A10 = (35*Math.pow((A2-1)/19,1.2))
            }
            }
        }
        break;
    case 2:
        //Same as case 1
        if(A2>80){
            A10 = 90+(20*((A2-80)/70))
        }
        else{
            if(A2>60){
            A10 = 75+(15*((A2-60)/20))
            }
            else{
            if(A2>20){
                A10 = 35+(40*(1-(Math.pow(1-((A2-20)/40),1.2))))  
            }
            else{
                A10 = (35*Math.pow((A2-1)/19,1.2))
            }
            }
        }
        break;

    case 4:
        /*
        IF(A2>80,ADD(95,MULTIPLY(5,DIVIDE(A2-80,19))),
        IF(A2>50,ADD(80,MULTIPLY(15,DIVIDE(A2-50,30))),
        IF(A2>20,ADD(40,MULTIPLY(40,DIVIDE(A2-20,30))),
        MULTIPLY(40,DIVIDE(A2-1,19)) ))),
        */

        if(A2>80){
            A10 = 95+(5*((A2-80)/19))
        }
        else{
            if(A2>50){
            A10 = 80+(15*((A2-50)/30))
            }
            else{
            if(A2>20){
                A10 = 40+(40*((A2-20)/30)) 
            }
            else{
                A10 = 40*((A2-1)/19)
            }
            }
        }
        break;
    case 7:
        /*
        IF(A2>80,ADD(90,MULTIPLY(20,DIVIDE(A2-80,70))),
        IF(A2>60,ADD(75,MULTIPLY(15,DIVIDE(A2-60,20))),
        IF(A2>20,ADD(35,MULTIPLY(40,MINUS(1,POW(MINUS(1,DIVIDE(A2-20,40)),1.2)))),
        MULTIPLY(35,POW(DIVIDE(A2-1,19),1.2)) ))),
        */

        if(A2>80){
            A10 = 90+(20*((A2-80)/70))
        }
        else{
            if(A2>60){
            A10 = 75+(15*((A2-60)/20))
            }
            else{
            if(A2>20){
                A10 = 35+(40*(1-(Math.pow(1-((A2-20)/40),1.2))))  
            }
            else{
                A10 = (35*Math.pow((A2-1)/19,1.2))
            }
            }
        }
        break;
    case 8:
        /*
        IF(A2>80,ADD(90,MULTIPLY(20,DIVIDE(A2-80,70))),
        IF(A2>60,ADD(75,MULTIPLY(15,DIVIDE(A2-60,20))),
        IF(A2>16,ADD(25,MULTIPLY(50,MINUS(1,POW(MINUS(1,DIVIDE(A2-16,44)),1.2)))),
        MULTIPLY(25,POW(DIVIDE(A2-1,15),1.2)) ))),
        */
        if(A2>80){
            A10 = 90+(20*((A2-80)/70))
        }
        else{
            if(A2>60){
            A10 = 75+(15*((A2-60)/20))
            }
            else{
            if(A2>16){
                A10 = 25+(50*(1-(Math.pow(1-((A2-16)/44),1.2))))  
            }
            else{
                A10 = (25*Math.pow((A2-1)/15,1.2))
            }
            }
        }
        break;
    case 12:
        /*
        IF(A2>45,ADD(75,MULTIPLY(25,DIVIDE(A2-45,54))),
        IF(A2>30,ADD(55,MULTIPLY(20,DIVIDE(A2-30,15))),
        IF(A2>15,ADD(10,MULTIPLY(45,DIVIDE(A2-15,15))),
        MULTIPLY(10,DIVIDE(A2-1,14)) ))),
        */
        if(A2>45){
            A10 = 75+(25*((A2-45)/54))
        }
        else{
            if(A2>30){
            A10 = 55+(20*((A2-30)/15))
            }
            else{
            if(A2>15){
                A10 = 10+(45*((A2-15)/15))  
            }
            else{
                A10 = 10*((A2-1)/14)
            }
            }
        }
        break;
    case 14:
        /*
        IF(A2>80,ADD(85,MULTIPLY(15,DIVIDE(A2-80,19))),
        IF(A2>40,ADD(60,MULTIPLY(25,DIVIDE(A2-40,40))),
        IF(A2>20,ADD(40,MULTIPLY(20,DIVIDE(A2-20,20))),
        MULTIPLY(40,DIVIDE(A2-1,19)) ))),
        */

        if(A2>80){
            A10 = 85+(15*((A2-80)/19))
        }
        else{
            if(A2>40){
            A10 = 60+(25*((A2-40)/40))
            }
            else{
            if(A2>20){
                A10 = 40+(20*((A2-20)/20))  
            }
            else{
                A10 = 40*((A2-1)/19)
            }
            }
        }
        break;
    case 15:
        /*
        IF(A2>80,ADD(95,MULTIPLY(5,DIVIDE(A2-80,19))),
        IF(A2>60,ADD(65,MULTIPLY(30,DIVIDE(A2-60,20))),
        IF(A2>25,ADD(25,MULTIPLY(40,DIVIDE(A2-25,35))),
        MULTIPLY(25,DIVIDE(A2-1,24)) ))),
        */

        if(A2>80){
            A10 = 95+(5*((A2-80)/19))
        }
        else{
            if(A2>60){
            A10 = 65+(30*((A2-60)/20))
            }
            else{
            if(A2>25){
                A10 = 25+(40*((A2-25)/35))  
            }
            else{
                A10 = 25*((A2-1)/24)
            }
            }
        }
        break;
    case 16:
        /*
        IF(A2>80,ADD(90,MULTIPLY(10,DIVIDE(A2-80,19))),
        IF(A2>60,ADD(75,MULTIPLY(15,DIVIDE(A2-60,20))),
        IF(A2>18,ADD(20,MULTIPLY(55,DIVIDE(A2-18,42))),
        MULTIPLY(20,DIVIDE(A2-1,17)) )))))
        */

        if(A2>80){
            A10 = 90+(10*((A2-80)/19))
        }
        else{
            if(A2>60){
            A10 = 75+(15*((A2-60)/20))
            }
            else{
            if(A2>18){
                A10 = 20+(55*((A2-18)/42)) 
            }
            else{
                A10 = 20*((A2-1)/17)
            }
            }
        }
        break;
    }
}
else{
    return 0;
}

return A10;
}

function calcStr(B2,J2, extraData, F10){
//B2 is str stat
if((J2 == false || extraData == "No") && !(F10=="Bow"||F10=="Light Bow"||F10=="Greatbow")){
    return B2;
}
else{
    if(B2*1.5>150){
    return 150;
    }
    else{
    return Math.trunc(B2*1.5);
    }
}
}