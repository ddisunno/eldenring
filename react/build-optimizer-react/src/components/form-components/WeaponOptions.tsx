import React, { useEffect, useState } from 'react';
import AffinitySelection from './AffinitySelection';
import ChosenWeapon from './ChosenWeapon';
import ImageWithInfo from './ImageWithInfo';
import {Weapon} from './interfaces';

interface Props{
   weaponArray:Weapon[],
   chosenWeapons: Weapon[],
   setChosenWeapons: React.Dispatch<React.SetStateAction<Weapon[]>>,
   index:number
}

const WeaponOptions:React.FC<Props> = ({weaponArray, chosenWeapons, setChosenWeapons, index}) => {
    const [getWeaponOptions, setWeaponOptions] = useState<JSX.Element[]>()
    
    const [selectedWeapon, setSelectedWeapon] = useState<Weapon>({name:'',somber:true, affinity:"", pngUrl:"", isPow:false});

    const [chosenWeaponsJSX, setChosenWeaponsJSX] = useState<JSX.Element>(<ChosenWeapon weapon = {selectedWeapon} somber = {selectedWeapon['somber']} chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons}></ChosenWeapon>)

    useEffect(() => {
       
        setWeaponOptions(weaponArray.map((key:Weapon) => {
            return <option key = {key['name']} value = {JSON.stringify(key)}>{key['name']}</option>
        }));
           
    }, [weaponArray]);

    //Update chosen weapon JSX
    useEffect(() => {
       
        setChosenWeaponsJSX(<ChosenWeapon weapon = {selectedWeapon} somber = {selectedWeapon['somber']} chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons}></ChosenWeapon>)

    }, [selectedWeapon]);

    //Press the add weapon button.
    /*
    function addWeapon(){
        if(selectedWeapon['name'] != "" ){
            var temp: Array<Weapon> = [...chosenWeapons];
            temp.push(selectedWeapon);
            setChosenWeapons(temp);
        }
    }
    */

    //Handle change in weapon selection
    function handleChangeWeapon(e:any){
        var weapon = JSON.parse(e.target.value);
        setSelectedWeapon(weapon);

        var temp: Array<Weapon> = [...chosenWeapons];
        temp[index] = weapon;
        setChosenWeapons(temp);
    }

    return(
        <div style= {{position:'relative', width: '100%', padding:'18px', display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems:'center', backgroundColor:'firebrick', borderColor:'white'}}>
            <label style = {{}}>{index+1}: </label>
            <ImageWithInfo pngUrl={selectedWeapon['pngUrl']} info={selectedWeapon} name = {selectedWeapon['name']}></ImageWithInfo>
            <select id = 'select-weapon' defaultValue = "" onChange={handleChangeWeapon}>
                <option value = {JSON.stringify({name:"",somber:false})}></option>
                {getWeaponOptions}
            </select> 
            {chosenWeaponsJSX}
        </div>
    );
}

export default WeaponOptions;