import React, { useState } from 'react';
import ImageWithInfo from './ImageWithInfo';
import {Weapon} from './interfaces';

interface Props{
    keyName:Weapon,
    chosenWeapons:Weapon[],
    setChosenWeapons:React.Dispatch<React.SetStateAction<Weapon[]>>,
    setWeaponName:React.Dispatch<React.SetStateAction<string>>
}

const AffinitySelection:React.FC<Props> = ({keyName, chosenWeapons, setChosenWeapons, setWeaponName}) => {
    
    //const [weaponName, setWeaponName] = useState<string>(keyName['name']);
   
    //Handle change in affinity selection
    function handleChangeWeapon(e:any){
        var tempList:Weapon[] = [...chosenWeapons]
        tempList.forEach(weapon => {
            if(weapon['name'] == keyName['name']){
                weapon['affinity'] = e.target.value;
            }
        });

        setChosenWeapons(tempList);
        
        //setWeaponName(e.target.value + " " + keyName['name']);
    }

    return(
        <div style= {{ }}>
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
        </div>
    );
}

export default AffinitySelection;