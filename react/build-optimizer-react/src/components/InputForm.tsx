import React, { useEffect, useState } from 'react';
import TargetLevelForm from './form-components/TargetLevelForm';
import TargetHealthForm from './form-components/TargetHealthForm';
import TargetPoiseForm from './form-components/TargetPoiseForm';
import WeaponsForm from './form-components/WeaponsForm';
import ArmorForm from './form-components/ArmorForm';
import TalismansForm from './form-components/TalismansForm';
import RollTypeForm from './form-components/RollTypeForm';
import SpellListForm from './form-components/SpellListForm';
import {Weapon, Armor, Talisman, Spell} from './form-components/interfaces';


interface Props{
    build:string,
    setBuild:React.Dispatch<React.SetStateAction<string>>,
    setOptimizedBuild:React.Dispatch<React.SetStateAction<string>>,
}

//Todo: {Add weapon grouping, two-handing, shields}, search in select fields, add Spell grouping, talismans of same type cant be added, add default pic, target mind?, CSS, hover over show item info?, weapon Level: right click on weapon -> open color box (unchecked = alone, rainbow = universal, colors of same color in same group) left click -> isTwoHanding isPowerStancing, affinities, two weapon additions: somber / non somber, somber max at 8, non-somber maxed at 13
const InputForm: React.FC<Props> = ({build, setBuild, setOptimizedBuild}) => {

    const [targetLevel, setTargetLevel] = useState<string>("150");
    const [targetHealth, setTargetHealth] = useState<string>("1900");
    const [targetPoise, setTargetPoise] = useState<string>("61");
    const [targetRoll, setTargetRoll] = useState<string>("med")

    const [chosenWeapons, setChosenWeapons] = useState<Array<Weapon>>([]);
    const [chosenWeaponsSomber, setChosenWeaponsSomber] = useState<Array<Weapon>>([]);

    const [targetHelm, setTargetHelm] = useState<Armor>({name:"",weight:0,poise:0,pngUrl:""});
    const [targetChest, setTargetChest] = useState<Armor>({name:"",weight:0,poise:0,pngUrl:""});
    const [targetGauntlets, setTargetGauntlets] = useState<Armor>({name:"",weight:0,poise:0,pngUrl:""});
    const [targetLegs, setTargetLegs] = useState<Armor>({name:"",weight:0,poise:0,pngUrl:""});

    const [talismans, setTalismans] = useState<Talisman[]>([{name:"",pngUrl:"",effect:''},{name:"",pngUrl:"",effect:''},{name:"",pngUrl:"",effect:''},{name:"",pngUrl:"",effect:''}]);

    const [spellList, setSpellList] = useState<Spell[]>([]);

    useEffect(() => {
        const optimizeBuild = async() => {
            try{
                await fetch("http://localhost:5000", {method: 'post', body: JSON.stringify({type: 'getBuild', build:build})}).then(body => body.json().then(res => setOptimizedBuild(res))); //returns array of strings
            } catch(err) {
                console.error(`Error: ${err}`);
            }        
        }
        optimizeBuild()
    }, [build]);

    function sendBuild(){
        var jsonBuild = JSON.stringify({"targetLevel":targetLevel, "targetHealth":targetHealth, "targetPoise":targetPoise, "targetRoll":targetRoll, "weapons":{"chosenWeapons":chosenWeapons, "chosenWeaponsSomber":chosenWeaponsSomber}, "targetArmor":{'helm':targetHelm, 'chest':targetChest, 'gauntlets':targetGauntlets,'legs':targetLegs}, 'talismans':talismans, 'spellList':spellList})
        setBuild(jsonBuild)
    }

    return (
      <div style = {{backgroundColor:'lightseagreen'}}>
        <h3>Enter Build Info: </h3>
        <form>
            <div id = 'basic-info' style = {{position:'relative', margin:'0 auto', padding:20, alignItems:'flex-start', flexDirection:'column', flex:'left', display:'flex', backgroundColor:'blue'}}>
                <TargetLevelForm targetLevel = {targetLevel} setTargetLevel = {setTargetLevel}></TargetLevelForm>

                <TargetHealthForm targetHealth = {targetHealth} setTargetHealth = {setTargetHealth}></TargetHealthForm>
                
                <TargetPoiseForm targetPoise = {targetPoise} setTargetPoise = {setTargetPoise}></TargetPoiseForm>

                <RollTypeForm targetRoll = {targetRoll} setTargetRoll = {setTargetRoll}></RollTypeForm>
            </div>
            <div style = {{position:'relative', margin:'0 auto', padding:20, alignItems:'flex-start', flex:'left', display:'flex', backgroundColor:'red'}}>
                <WeaponsForm chosenWeapons={chosenWeapons} setChosenWeapons ={setChosenWeapons} chosenWeaponsSomber={chosenWeaponsSomber} setChosenWeaponsSomber ={setChosenWeaponsSomber}></WeaponsForm>
            </div>
            <div style = {{position:'relative', margin:'0 auto', padding:20, alignItems:'flex-start', flexDirection:'row', flex:'left', display:'flex', backgroundColor:'yellow'}}>
                <ArmorForm targetHelm = {targetHelm} setTargetHelm = {setTargetHelm} targetChest = {targetChest} setTargetChest = {setTargetChest} targetGauntlets = {targetGauntlets} setTargetGauntlets = {setTargetGauntlets} targetLegs = {targetLegs} setTargetLegs = {setTargetLegs}></ArmorForm>

                <TalismansForm talismans = {talismans} setTalismans = {setTalismans}></TalismansForm>
            </div>
            <div style = {{position:'relative', margin:'0 auto', padding:20, alignItems:'flex-start', flexDirection:'row', flex:'left', display:'flex', backgroundColor:'chocolate'}}>
                <SpellListForm spellList = {spellList} setSpellList = {setSpellList}></SpellListForm>
                <input type="button" value="Optimize Build" style = {{marginLeft: 200}} onClick = {sendBuild}></input>
            </div>
        </form>
      </div>
    );
};

export default InputForm;