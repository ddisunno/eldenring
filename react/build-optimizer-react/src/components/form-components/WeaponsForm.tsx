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
    
    useEffect(() => {
        console.log(chosenWeapons)
        console.log(chosenWeaponsSomber)
    }, [chosenWeapons, chosenWeaponsSomber]);
        
    //Get all weapons from server, use them in dropdown menu
    return (
      <div style ={{position:'relative', margin:'0 auto', padding:20, alignItems:'flex-start', flexDirection:'row', flex:'left', display:'flex'}}>

        <div style ={{position:'relative', alignItems:'center', flexDirection:'column', flex:'center', display:'flex', backgroundColor:'pink'}}>
          <label>Non-Somber Weapons: </label>
          <WeaponOptions weaponArray = {weaponArray} chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons} index = {0}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArray} chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons} index = {1}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArray} chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons} index = {2}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArray} chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons} index = {3}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArray} chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons} index = {4}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArray} chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons} index = {5}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArray} chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons} index = {6}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArray} chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons} index = {7}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArray} chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons} index = {8}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArray} chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons} index = {9}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArray} chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons} index = {10}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArray} chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons} index = {11}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArray} chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons} index = {12}></WeaponOptions>
        </div>

        <div style ={{position:'relative', margin:'0 auto', alignItems:'center', flexDirection:'column', flex:'left', display:'flex'}}>
          <label>Somber Weapons: </label>
          <WeaponOptions weaponArray = {weaponArraySomber} chosenWeapons = {chosenWeaponsSomber} setChosenWeapons = {setChosenWeaponsSomber} index = {0}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArraySomber} chosenWeapons = {chosenWeaponsSomber} setChosenWeapons = {setChosenWeaponsSomber} index = {1}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArraySomber} chosenWeapons = {chosenWeaponsSomber} setChosenWeapons = {setChosenWeaponsSomber} index = {2}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArraySomber} chosenWeapons = {chosenWeaponsSomber} setChosenWeapons = {setChosenWeaponsSomber} index = {3}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArraySomber} chosenWeapons = {chosenWeaponsSomber} setChosenWeapons = {setChosenWeaponsSomber} index = {4}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArraySomber} chosenWeapons = {chosenWeaponsSomber} setChosenWeapons = {setChosenWeaponsSomber} index = {5}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArraySomber} chosenWeapons = {chosenWeaponsSomber} setChosenWeapons = {setChosenWeaponsSomber} index = {6}></WeaponOptions>

          <WeaponOptions weaponArray = {weaponArraySomber} chosenWeapons = {chosenWeaponsSomber} setChosenWeapons = {setChosenWeaponsSomber} index = {7}></WeaponOptions>
        </div>
        
      </div>
    );
};

export default WeaponsForm;