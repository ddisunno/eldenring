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
    const [affinity, setAffinity] = useState<JSX.Element>();

    const removeWeapon = (weapon:Weapon) =>{
        var temp: Array<Weapon> = [...chosenWeapons];
        const index = temp.indexOf(weapon);
        if (index > -1) { // only splice array when item is found
        temp.splice(index, 1); // 2nd parameter means remove one item only
        }
        setChosenWeapons(temp);
    }

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

        if(somber){
            setAffinity(<div></div>)
        }
        else{
            setAffinity(<AffinitySelection chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons} keyName = {weapon} removeWeapon = {removeWeapon} setWeaponName = {setWeaponName}></AffinitySelection>);
        }

    }, []);

    return(
        <div style= {{ width: '100%', display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems:'center'}}>
            <div id = 'weapon'>
                <ImageWithInfo pngUrl={weapon['pngUrl']} info={weapon} name = {weaponName}></ImageWithInfo>
            </div>
            {affinity}
            <label> Dual Wielding? </label>
            <input type = 'checkbox' id = 'is-power-stancing' onChange={() => handleIsPowerStancing(weapon)} hidden = {false}></input>
            <input type="button" value="Remove" onClick ={() => removeWeapon(weapon)}></input>
        </div>
    );
}

export default ChosenWeapon;