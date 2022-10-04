import React, { useState } from 'react';
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
    setBuild:React.Dispatch<React.SetStateAction<string[]>>
}

//Todo: {Add weapon grouping, shields}, search in select fields, add Spell grouping, talismans of same type cant be added, add default pic, target mind?, CSS, hover over show item info?
const InputForm: React.FC<Props> = ({setBuild}) => {

    const [targetLevel, setTargetLevel] = useState<string>("150");
    const [targetHealth, setTargetHealth] = useState<string>("1900");
    const [targetPoise, setTargetPoise] = useState<string>("61");
    const [targetRoll, setTargetRoll] = useState<string>("med")

    const [chosenWeapons, setChosenWeapons] = useState<Array<Weapon>>([]);
    console.log(chosenWeapons)
    const [targetHelm, setTargetHelm] = useState<Armor>({name:"",weight:0,poise:0,pngUrl:""});
    const [targetChest, setTargetChest] = useState<Armor>({name:"",weight:0,poise:0,pngUrl:""});
    const [targetGauntlets, setTargetGauntlets] = useState<Armor>({name:"",weight:0,poise:0,pngUrl:""});
    const [targetLegs, setTargetLegs] = useState<Armor>({name:"",weight:0,poise:0,pngUrl:""});

    const [talismans, setTalismans] = useState<Talisman[]>([{name:"",pngUrl:"",effect:''},{name:"",pngUrl:"",effect:''},{name:"",pngUrl:"",effect:''},{name:"",pngUrl:"",effect:''}]);

    const [spellList, setSpellList] = useState<Spell[]>([]);

    async function optimizeBuild(){
        try{
            await fetch("http://localhost:5000", {method: 'post', body: JSON.stringify({type: 'getBuild'})}).then(body => body.json().then(res => setBuild(res))); //returns array of strings
        } catch(err) {
            console.error(`Error: ${err}`);
        }        
    }

    return (
      <div>
        <form>
            <TargetLevelForm targetLevel = {targetLevel} setTargetLevel = {setTargetLevel}></TargetLevelForm>

            <TargetHealthForm targetHealth = {targetHealth} setTargetHealth = {setTargetHealth}></TargetHealthForm>
            
            <TargetPoiseForm targetPoise = {targetPoise} setTargetPoise = {setTargetPoise}></TargetPoiseForm>

            <RollTypeForm targetRoll = {targetRoll} setTargetRoll = {setTargetRoll}></RollTypeForm>

            <WeaponsForm chosenWeapons={chosenWeapons} setChosenWeapons ={setChosenWeapons}></WeaponsForm>

            <ArmorForm targetHelm = {targetHelm} setTargetHelm = {setTargetHelm} targetChest = {targetChest} setTargetChest = {setTargetChest} targetGauntlets = {targetGauntlets} setTargetGauntlets = {setTargetGauntlets} targetLegs = {targetLegs} setTargetLegs = {setTargetLegs}></ArmorForm>

            <TalismansForm talismans = {talismans} setTalismans = {setTalismans}></TalismansForm>

            <SpellListForm spellList = {spellList} setSpellList = {setSpellList}></SpellListForm>

            <input type="button" value="Optimize Build" onClick = {optimizeBuild}></input>
        </form>
      </div>
    );
};

export default InputForm;