import React, { useState } from 'react';

interface Props{
    keyName:string,
    chosenWeapons:{name: string;somber: boolean;}[],
    setChosenWeapons:React.Dispatch<React.SetStateAction<{name: string; somber: boolean;}[]>>
}

const AffinitySelection:React.FC<Props> = ({keyName, chosenWeapons, setChosenWeapons}) => {

    const [weaponName, setWeaponName] = useState<string>(keyName);

    //Handle change in affinity selection
    function handleChangeWeapon(e:any){
        var tempList:{name: string;somber: boolean;}[] = [...chosenWeapons]
        tempList.forEach(weapon => {
            if(weapon['name'] == keyName ){
                weapon['name'] = e.target.value + " " + keyName;
            }
        });

        setChosenWeapons(tempList);
        
        setWeaponName(e.target.value + " " + keyName);
    }

    return(
        <div>
            <li key = {keyName} value = {weaponName}>{weaponName}</li>
            <label>Affinity: </label>
            <select defaultValue="" onChange={handleChangeWeapon}> 
                <option value = "">Standard</option>
                <option value = "Heavy">Heavy</option>
                <option value = "Keen">Keen</option>
                <option value = "Quality">Quality</option>
                <option value = "Magic">Magic</option>
                <option value = "Cold">Cold</option>
                <option value = "Fire">Fire</option>
                <option value = "Flame art">Flame Art</option>
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