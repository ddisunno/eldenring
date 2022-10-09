import React, { useEffect, useState } from 'react';
import AffinitySelection from './AffinitySelection';
import ImageWithInfo from './ImageWithInfo';
import {Weapon} from './interfaces';
import WeaponOptions from './WeaponOptions';

interface Props{
    chosenWeapons: Weapon[],
    setChosenWeapons: React.Dispatch<React.SetStateAction<Weapon[]>>,

    chosenWeaponsSomber: Weapon[],
    setChosenWeaponsSomber: React.Dispatch<React.SetStateAction<Weapon[]>>
}


const WeaponsForm: React.FC<Props> = ({chosenWeapons, setChosenWeapons, chosenWeaponsSomber, setChosenWeaponsSomber}) => {
    
    //All weapons in options 
    const [weaponArray, setWeaponArray] = useState<Array<Weapon>>([]);
    const [weaponArraySomber, setWeaponArraySomber] = useState<Array<Weapon>>([]);
   
    function getWeaponsFromServer(res:any){
            setWeaponArray(res['standard'])    
            setWeaponArraySomber(res['somber'])
    }

    //On load, get weapon array from server. *Happens only once*
    useEffect(() => {
        const weaponList = async() => {
            try{
                await fetch("http://localhost:5000", {method: 'post', body: JSON.stringify({type: 'getWeaponNames'})}).then(body => body.json().then(res => getWeaponsFromServer(res))); //returns array of strings
            } catch(err) {
                console.error(`Error: ${err}`);
            }        
        }
        weaponList()
    }, []);
    
        
    //Get all weapons from server, use them in dropdown menu
    return (
      <div style ={{position:'relative', margin:'0 auto', padding:20, alignItems:'flex-start', flexDirection:'row', flex:'left', display:'flex'}}>

        <div style ={{position:'relative', margin:'0 auto', padding:20, alignItems:'center', flexDirection:'column', flex:'left', display:'flex'}}>
          <label>Non-Somber Weapons: </label>
          <WeaponOptions weaponArray = {weaponArray} chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons}></WeaponOptions>
        </div>

        <div style ={{position:'relative', margin:'0 auto', padding:20, alignItems:'center', flexDirection:'column', flex:'left', display:'flex'}}>
          <label>Somber Weapons: </label>
          <WeaponOptions weaponArray = {weaponArraySomber} chosenWeapons = {chosenWeaponsSomber} setChosenWeapons = {setChosenWeaponsSomber}></WeaponOptions>
        </div>
        
      </div>
    );
};

export default WeaponsForm;