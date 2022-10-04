import React, { useState } from 'react';
import ImageWithInfo from './ImageWithInfo';
import {Weapon} from './interfaces';

interface Props{
    keyName:Weapon,
    chosenWeapons:Weapon[],
    setChosenWeapons:React.Dispatch<React.SetStateAction<Weapon[]>>,
    removeWeapon:(weapon: Weapon) => void
}

const AffinitySelection:React.FC<Props> = ({keyName, chosenWeapons, setChosenWeapons, removeWeapon}) => {
    
    const [weaponName, setWeaponName] = useState<string>(keyName['name']);
   
    //Handle change in affinity selection
    function handleChangeWeapon(e:any){
        var tempList:Weapon[] = [...chosenWeapons]
        tempList.forEach(weapon => {
            if(weapon['name'] == keyName['name']){
                weapon['affinity'] = e.target.value;
            }
        });

        setChosenWeapons(tempList);
        
        setWeaponName(e.target.value + " " + keyName['name']);
    }

    function handleIsPowerStancing(e:any){
        var tempList:Weapon[] = [...chosenWeapons]
        tempList.forEach(weapon => {
            if(weapon['name'] == keyName['name']){
                //setIsPowerStancing(!isPowerStancing)
                weapon['isPow'] = !weapon['isPow']
            }
        });

        setChosenWeapons(tempList);
    }

    return(
        <div style= {{ width: '100%', display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems:'center'}}>
            <ImageWithInfo pngUrl={keyName['pngUrl']} info={keyName}></ImageWithInfo>
            <li key = {keyName['name']} value = {weaponName} style = {{listStyle:'none'}}>{weaponName}</li>
            <select defaultValue="" onChange={handleChangeWeapon}> 
                <option value = "">Standard</option>
                <option value = "Heavy">Heavy</option>
                <option value = "Keen">Keen</option>
                <option value = "Quality">Quality</option>
                <option value = "Magic">Magic</option>
                <option value = "Cold">Cold</option>
                <option value = "Fire">Fire</option>
                <option value = "Flame Art">Flame Art</option>
                <option value = "Lightning">Lightning</option>
                <option value = "Sacred">Sacred</option>
                <option value = "Poison">Poison</option>
                <option value = "Blood">Blood</option>
                <option value = "Occult">Occult</option>
            </select>
            <label> Dual Wielding? </label>
            <input type = 'checkbox' id = 'is-power-stancing' onChange={handleIsPowerStancing}></input>
            <input type="button" value="Remove" onClick ={() => removeWeapon(keyName)}></input>
        </div>
    );
}

export default AffinitySelection;