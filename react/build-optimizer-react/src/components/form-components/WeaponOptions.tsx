import React, { useEffect, useState } from 'react';
import AffinitySelection from './AffinitySelection';
import ChosenWeapon from './ChosenWeapon';
import ImageWithInfo from './ImageWithInfo';
import {Weapon} from './interfaces';

interface Props{
   weaponArray:Weapon[],
   chosenWeapons: Weapon[],
   setChosenWeapons: React.Dispatch<React.SetStateAction<Weapon[]>>
}

const WeaponOptions:React.FC<Props> = ({weaponArray, chosenWeapons, setChosenWeapons}) => {
    const [getWeaponOptions, setWeaponOptions] = useState<JSX.Element[]>()
    const [chosenWeaponsJSX, setChosenWeaponsJSX] = useState<JSX.Element[]>()
    const [selectedWeapon, setSelectedWeapon] = useState<Weapon>({name:'',somber:false, affinity:"", pngUrl:"", isPow:false});

    useEffect(() => {
       
        setWeaponOptions(weaponArray.map((key:Weapon) => {
            return <option key = {key['name']} value = {JSON.stringify(key)}>{key['name']}</option>
        }));
           
    }, [weaponArray]);

    //Update chosen weapon JSX
    useEffect(() => {
        setChosenWeaponsJSX(chosenWeapons.map((key:Weapon) => {
        
            return(<ChosenWeapon weapon = {key} somber = {key['somber']} chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons}></ChosenWeapon>)
        
        }))

    }, [chosenWeapons]);

    //Press the add weapon button.
    function addWeapon(){
        if(selectedWeapon['name'] != "" ){
            var temp: Array<Weapon> = [...chosenWeapons];
            temp.push(selectedWeapon);
            setChosenWeapons(temp);
        }
    }


    //Handle change in weapon selection
    function handleChangeWeapon(e:any){
        setSelectedWeapon(JSON.parse(e.target.value));
    }

    return(
        <div>
            <select id = 'select-weapon' defaultValue = "" onChange={handleChangeWeapon}>
                <option value = {JSON.stringify({name:"",somber:false})}></option>
                {getWeaponOptions}
          </select> 
          <input type="button" value="Add Weapon" onClick={addWeapon}></input>
          <div style= {{ width: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'flex-start', alignItems:'left'}}>
                <ul>
                    {chosenWeaponsJSX}
                </ul>
            </div>
        </div>
    );
}

export default WeaponOptions;