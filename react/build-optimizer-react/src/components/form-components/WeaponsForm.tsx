import React, { useEffect, useState } from 'react';
import AffinitySelection from './AffinitySelection';

interface Props{
    weapons: string[],
    setWeapons: React.Dispatch<React.SetStateAction<string[]>>
}

const WeaponsForm: React.FC<Props> = ({weapons, setWeapons}) => {
    
    //All weapons in options 
    const [weaponArray, setWeaponArray] = useState<Array<{'name':string, "somber":boolean}>>([]);
    const [getWeaponOptions, setWeaponOptions] = useState<JSX.Element[]>()

    //Weapons the user adds to their build.
    //const [chosenWeapons, setChosenWeapons] = useState<string[]>([]);
    const [chosenWeapons, setChosenWeapons] = useState<Array<{'name':string, "somber":boolean}>>([]);
    const [chosenWeaponsJSX, setChosenWeaponsJSX] = useState<JSX.Element[]>()
    
    //The current weapon in the selection bar
    //This was type string
    const [selectedWeapon, setSelectedWeapon] = useState<{'name':string, "somber":boolean}>({name:'',somber:false});

    useEffect(() => {
        const weaponList = async() => {
            try{
                await fetch("http://localhost:5000", {method: 'post', body: JSON.stringify({type: 'getWeaponNames'})}).then(body => body.json().then(res => setWeaponArray(res))); //returns array of strings
            } catch(err) {
                console.error(`Error: ${err}`);
            }        
        }
        weaponList()
    }, []);
    
    useEffect(() => {
       
        setWeaponOptions(weaponArray.map((key:{name:string, somber:boolean}) => {
            return <option key = {key['name']} value = {JSON.stringify(key)}>{key['name']}</option>
        }));
           
    }, [weaponArray]);

    useEffect(() => {
       
        setChosenWeaponsJSX(chosenWeapons.map((key:{name:string, somber:boolean}) => {
            //If key is not somber weapon, the add affinity
            if(key['somber'] == false){
                return <AffinitySelection keyName = {key['name']}></AffinitySelection>;
            }
            else{
                return <li key = {key['name']} value = {key['name']}>{key['name']}</li>
            }
        }));
           
    }, [chosenWeapons]);

    //Press the add weapon button.
    function addWeapon(){
        if(selectedWeapon['name'] != "" ){
            var temp: Array<{name:string, somber:boolean}> = [...chosenWeapons];
            temp.push(selectedWeapon);
            setChosenWeapons(temp);
        }
    }

    //Handle change in weapon selection
    function handleChangeWeapon(e:any){
        console.log(e.target.value)
        var value = JSON.parse(e.target.value)
        
        setSelectedWeapon({name:value['name'], somber: value['somber']});
    }

    //Get all weapons from server, use them in dropdown menu
    return (
      <div>
          <label>Weapons: </label>
          <select id = 'select-weapon' defaultValue = "" onChange={handleChangeWeapon}>
                <option value = {JSON.stringify({name:"",somber:false})}></option>
                {getWeaponOptions}
          </select> 
          <input type="button" value="Add Weapon" onClick={addWeapon}></input>
          <ul>
            {chosenWeaponsJSX}
          </ul>
      </div>
    );
};

export default WeaponsForm;