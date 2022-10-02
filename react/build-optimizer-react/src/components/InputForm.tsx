import React, { useState } from 'react';
import TargetLevelForm from './form-components/TargetLevelForm';
import TargetHealthForm from './form-components/TargetHealthForm';
import TargetPoiseForm from './form-components/TargetPoiseForm';
import WeaponsForm from './form-components/WeaponsForm';
import ArmorForm from './form-components/ArmorForm';
import TalismansForm from './form-components/TalismansForm';

interface Weapon{
    name: string,
    somber: boolean,
    affinity: string,
    pngUrl: string
}
interface Armor{
    name:string,
    weight:number,
    poise:number,
    pngUrl: string
}
interface Talisman{
    name:string,
    pngUrl:string
}
interface Props{
    setBuild:React.Dispatch<React.SetStateAction<string[]>>
}
const InputForm: React.FC<Props> = ({setBuild}) => {

    const [targetLevel, setTargetLevel] = useState<string>("");
    const [targetHealth, setTargetHealth] = useState<string>("");
    const [targetPoise, setTargetPoise] = useState<string>("");
    const [chosenWeapons, setChosenWeapons] = useState<Array<Weapon>>([]);

    const [targetHelm, setTargetHelm] = useState<Armor>({name:"",weight:0,poise:0,pngUrl:""});
    const [targetChest, setTargetChest] = useState<Armor>({name:"",weight:0,poise:0,pngUrl:""});
    const [targetGauntlets, setTargetGauntlets] = useState<Armor>({name:"",weight:0,poise:0,pngUrl:""});
    const [targetLegs, setTargetLegs] = useState<Armor>({name:"",weight:0,poise:0,pngUrl:""});

    const [talismans, setTalismans] = useState<Talisman[]>([{name:"",pngUrl:""},{name:"",pngUrl:""},{name:"",pngUrl:""},{name:"",pngUrl:""}]);

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

            <WeaponsForm chosenWeapons={chosenWeapons} setChosenWeapons ={setChosenWeapons}></WeaponsForm>

            <ArmorForm targetHelm = {targetHelm} setTargetHelm = {setTargetHelm} targetChest = {targetChest} setTargetChest = {setTargetChest} targetGauntlets = {targetGauntlets} setTargetGauntlets = {setTargetGauntlets} targetLegs = {targetLegs} setTargetLegs = {setTargetLegs}></ArmorForm>

            <TalismansForm talismans = {talismans} setTalismans = {setTalismans}></TalismansForm>

            <input type="button" value="Optimize Build" onClick = {optimizeBuild}></input>
        </form>
      </div>
    );
};

export default InputForm;