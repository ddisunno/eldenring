/**
 * Max out the AR of any weapon, given the weapon's level, infusions, starting class, and # of levels to contribute to damage scaling.
 * Boc's Brilliant Build Optimizer
 */
function main() {

//First, get the contants from the spreadsheet for the weapon AR formula. This takes the longest amount of time.
var constants = getWeaponFormulaConstants()
console.log('Done constants');

//On Button press, get user entered information
var numOfLevels = SpreadsheetApp.getActiveSheet().getRange(4, 8).getValue();
var startingClass = SpreadsheetApp.getActiveSheet().getRange(6,8).getValue().toLowerCase();

//Get the wepon requirement levels & scaling of the chosen weapon.
var weaponReq = {'strength':SpreadsheetApp.getActiveSheet().getRange(3,2).getValue(),'dexterity':SpreadsheetApp.getActiveSheet().getRange(3,3).getValue(),'intelligence':SpreadsheetApp.getActiveSheet().getRange(3,4).getValue(),'faith':SpreadsheetApp.getActiveSheet().getRange(3,5).getValue(),'arcane':SpreadsheetApp.getActiveSheet().getRange(3,6).getValue()};

var scaling = [SpreadsheetApp.getActiveSheet().getRange(4,2).getValue(),SpreadsheetApp.getActiveSheet().getRange(4,3).getValue(),SpreadsheetApp.getActiveSheet().getRange(4,4).getValue(),SpreadsheetApp.getActiveSheet().getRange(4,5).getValue(),SpreadsheetApp.getActiveSheet().getRange(4,6).getValue()];
var scalingStats = getScalingStats(scaling);

//Get classes from eldenring.fanapis.com
var classes = JSON.parse(UrlFetchApp.fetch("https://eldenring.fanapis.com/api/classes").getContentText());

//Call optimizeBuildStats() based off of which class the user chose.
for(var i = 0; i < classes['data'].length; i++){
    if(startingClass == classes['data'][i]['name'].toLowerCase()){
    startingStats = classes['data'][i]['stats'];
    optimizeBuildStats(numOfLevels, startingStats, weaponReq, scalingStats, constants);
    }
}
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//Works for weapons that scale off of 0,1, or 2 stats. 3 stats takes too long due to using calculator. 4 or 5 is not supported. (I'm not sure if 4 or 5 is even possible).
function optimizeBuildStats(numOfLevels, startingStats, weaponReq, scalingStats, constants){

//If too many levels are enterted, and all scaling stats can be maxed to 99, return every value being 99.
if(isNumOfLevelsOver(numOfLevels, startingStats, scalingStats)){
    setStats({'strength': 99, 'dexterity': 99, 'intelligence': 99, 'faith': 99, 'arcane': 99, 'ar': null});
    return 1;
}

//Get min stats, then get the number of levels to be initially added to the stats that scale.
var minStats = getMinStats(startingStats, weaponReq);
numOfLevels = getLevelsAfterStatReq(numOfLevels, scalingStats, startingStats, weaponReq)
numOfLevelsStack = getInitialAddedLevelsPerStat(minStats, scalingStats, numOfLevels); 

//Create the starting state
var startState = {'strength': minStats['strength'], 'dexterity': minStats['dexterity'], 'intelligence': minStats['intelligence'], 'faith': minStats['faith'], 'arcane': minStats['arcane'], 'ar': null};

//Add initial levels to stats that scale.
for(var i = 0; i < scalingStats.length; i++){
    startState[scalingStats[i]] += numOfLevelsStack[i];
}

//Get AR of this state
startState['ar'] = getWeaponAR(startState['strength'], startState['dexterity'], startState['intelligence'], startState['faith'], startState['arcane'], constants); 

//If no stats scale or only one stat scales, return startState
if(scalingStats.length == 0 || scalingStats.length == 1)
    return 1;

//Min-max for state with the highest AR (Valid state cannot have a stat under the stat minimum defined in minStats, or total # of levels != starting # of levels)
/** Brute Force approach (although other methods won't be much better) */
var optimialBuild = {...startState}; //Initially the start state
var stateStack = [startState];

//With 2 scalinf stats- branching factor of 1. With 3, branching factor of 2.
//Feel like im thinking of this the wrong way...
var statesVisited = {};
statesVisited[JSON.stringify(startState)] = true;
while(stateStack.length > 0){
    var state = {...stateStack.shift()}
    
    //console.log(state['strength'], state['dexterity'], state['faith']);

    if(state[scalingStats[0]] - 1 >= minStats[scalingStats[0]]){

    state[scalingStats[0]] -= 1;
    for(var i = 1; i < scalingStats.length; i++){
        var newState = {...state};
        if(newState[scalingStats[i]]+1 <= 99){
        newState[scalingStats[i]] += 1;
        newState['ar'] = getWeaponAR(newState['strength'], newState['dexterity'], newState['intelligence'], newState['faith'], newState['arcane'], constants); 

        if(newState['ar'] > optimialBuild['ar']){
            optimialBuild = {...newState};
        }
        
        if(statesVisited[JSON.stringify(newState)] == undefined){
            stateStack.push({...newState});
            statesVisited[JSON.stringify(newState)] = true;
        }
        }
    }
    }
}

setStats(optimialBuild);
console.log("Done Optimization: " + optimialBuild['ar']);
return 1;
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/** Helper functions */
//Get the attack rating from the spreadsheet (Not used anymore)
function getTotalAR(state){
setStats(state)
return SpreadsheetApp.getActiveSheet().getRange(10, 7).getValue();
}

//Set the stats on the spreadsheet to the given stats. {str: ...}
function setStats(stats){
SpreadsheetApp.getActiveSheet().getRange(2, 2).setValue(stats['strength']);
SpreadsheetApp.getActiveSheet().getRange(2, 3).setValue(stats['dexterity']);
SpreadsheetApp.getActiveSheet().getRange(2, 4).setValue(stats['intelligence']);
SpreadsheetApp.getActiveSheet().getRange(2, 5).setValue(stats['faith']);
SpreadsheetApp.getActiveSheet().getRange(2, 6).setValue(stats['arcane']);
}

//Return an array with the names of the stats that scale with the given weapon.
function getScalingStats(scaling){
var scalingStats = []
for(var i = 0; i < scaling.length; i++){
    if(scaling[i]!='-'){
    switch(i){
        case 0:
        scalingStats.push('strength');
        break;
        case 1:
        scalingStats.push('dexterity');
        break;
        case 2:
        scalingStats.push('intelligence');
        break;
        case 3:
        scalingStats.push('faith');
        break;
        case 4:
        scalingStats.push('arcane');
        break;
    }
    }
}
return scalingStats;
}

//Get the minimum stats for each stat line. For each stat this is either the default stat of the starting class, or the weapon required stat, whichever is larger.
function getMinStats(startingStats, weaponReq){


//Minimum stats based off of starting class
var minStr = Math.max(parseInt(startingStats['strength']),weaponReq['strength']);
var minDex = Math.max(parseInt(startingStats['dexterity']),weaponReq['dexterity']);
var minInt = Math.max(parseInt(startingStats['intelligence']),weaponReq['intelligence']);
var minFai = Math.max(parseInt(startingStats['faith']),weaponReq['faith']);
var minArc = Math.max(parseInt(startingStats['arcane']),weaponReq['arcane']);
return {'strength':minStr, 'dexterity':minDex, 'intelligence':minInt, 'faith':minFai, 'arcane':minArc};
}

//Get the amount of levels taken from weapon requirments, that cannot be used in optimizing.
function getLevelsAfterStatReq(numOfLevels, scalingStats, startingStats, weaponReq){
var levelsFromStatReq = 0;

for(var i = 0; i < scalingStats.length; i++){
    if(parseInt(startingStats[scalingStats[i]]) < weaponReq[scalingStats[i]]){
    levelsFromStatReq += weaponReq[scalingStats[i]] - parseInt(startingStats[scalingStats[i]]);
    }
}

return numOfLevels - levelsFromStatReq;
}

//If the user entered enough stats to max out each statline that scales, return true.
function isNumOfLevelsOver(numOfLevels, startingStats, scalingStats){
//Get total number of levels already in scaled stats
var startScalingTotal = 0;
for(var i = 0; i < scalingStats.length; i++){
    startScalingTotal += startingStats[scalingStats[i]]
}

//If the user entered too many levels, then true
if(numOfLevels >= (scalingStats.length * 99)-startScalingTotal){
    return false;
}
else{
    return true;
}
}

//Get the amount of levels to be initally added to each scaling stat line based of the number of levels given, and the min stats of the character. Returns an array of length = # of scaling stats, with each entry being between minStat and 99.
function getInitialAddedLevelsPerStat(minStats, scalingStats, numOfLevels){
var numOfLevelsStack = Array(scalingStats.length).fill(0);
for(var i = 0; i < scalingStats.length; i++){
    if(minStats[scalingStats[i]] + numOfLevels > 99){
    numOfLevelsStack[i] = 99-minStats[scalingStats[i]];
    numOfLevels -= numOfLevelsStack[i];
    }
    else{
    numOfLevelsStack[i] += numOfLevels
    break;
    }
}

return numOfLevelsStack;
}
