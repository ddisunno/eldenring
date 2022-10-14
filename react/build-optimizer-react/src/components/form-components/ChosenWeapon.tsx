import React, { useEffect, useState } from 'react';
import AffinitySelection from './AffinitySelection';
import ImageWithInfo from './ImageWithInfo';
import {Weapon} from './interfaces';

interface Props{
    weapon:Weapon
    chosenWeapons: Weapon[],
    setChosenWeapons: React.Dispatch<React.SetStateAction<Weapon[]>>,
    somber:boolean,
    
}

const ChosenWeapon:React.FC<Props> = ({weapon, somber, chosenWeapons, setChosenWeapons}) => {

    const [weaponName, setWeaponName] = useState<string>(weapon['name']);
    const [affinity, setAffinity] = useState<JSX.Element>(<div></div>);

    /*
    const removeWeapon = (weapon:Weapon) =>{
        var temp: Array<Weapon> = [...chosenWeapons];
        const index = temp.indexOf(weapon);
        if (index > -1) { // only splice array when item is found
        temp.splice(index, 1); // 2nd parameter means remove one item only
        }
        setChosenWeapons(temp);
    }
    */

    function handleIsPowerStancing(key:Weapon){
        var tempList:Weapon[] = [...chosenWeapons]
        tempList.forEach(weapon => {
            if(key['name'] == weapon['name']){
                //setIsPowerStancing(!isPowerStancing)
                weapon['isPow'] = !weapon['isPow']
            }
        });

        setChosenWeapons(tempList);
    }

    useEffect(() => {
        
        if(weapon['somber']){
            setAffinity(<div></div>)
        }
        else{
            console.log("Set Affinity")
            setAffinity(<AffinitySelection chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons} keyName = {weapon} setWeaponName = {setWeaponName}></AffinitySelection>);
        }

    }, [weapon]);

    return(
        <div style= {{display: 'inline-flex', flexDirection: 'row', justifyContent: 'center', alignItems:'center'}}>
            {affinity}
            <div hidden = {(weapon['name'] == "" ? true: false)} style= {{flexDirection: 'column', position:'relative'}}>
                <label style ={{fontSize:'.8em'}}> Pow. Stancing?</label>
                <input type = 'checkbox' id = 'is-power-stancing' onChange={() => handleIsPowerStancing(weapon)}></input>
            </div>
        </div>
    );
}

export default ChosenWeapon;