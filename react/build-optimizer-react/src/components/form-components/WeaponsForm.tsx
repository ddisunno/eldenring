import React, { useEffect, useState } from 'react';
import AffinitySelection from './AffinitySelection';
import ImageWithInfo from './ImageWithInfo';
import {Weapon} from './interfaces';

interface Props{
    chosenWeapons: Weapon[],
    setChosenWeapons: React.Dispatch<React.SetStateAction<Weapon[]>>
}

const WeaponsForm: React.FC<Props> = ({chosenWeapons, setChosenWeapons}) => {
    
    //All weapons in options 
    const [weaponArray, setWeaponArray] = useState<Array<Weapon>>([]);
    const [getWeaponOptions, setWeaponOptions] = useState<JSX.Element[]>()

    //Weapons the user adds to their build.
    const [chosenWeaponsJSX, setChosenWeaponsJSX] = useState<JSX.Element[]>()
    
    //The current weapon in the selection bar
    //This was type string
    const [selectedWeapon, setSelectedWeapon] = useState<Weapon>({name:'',somber:false, affinity:"", pngUrl:"", isPow:false});

    //On load, get weapon array from server. *Happens only once*
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
    
    //Update option JSX on weaponArray
    useEffect(() => {
       
        setWeaponOptions(weaponArray.map((key:Weapon) => {
            return <option key = {key['name']} value = {JSON.stringify(key)}>{key['name']}</option>
        }));
           
    }, [weaponArray]);

    //Update chosen weapon JSX
    useEffect(() => {
       
        setChosenWeaponsJSX(chosenWeapons.map((key:Weapon) => {
            //If key is not somber weapon, the add affinity
            if(key['somber'] == false){
                return <AffinitySelection chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons} keyName = {key} removeWeapon = {removeWeapon}></AffinitySelection>;
            }
            //Not somber- no affinity selection
            else{
                return(
                    <div style= {{ width: '100%', display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems:'center'}}>
                        <ImageWithInfo pngUrl={key['pngUrl']} info={key}></ImageWithInfo>
                        <li key = {key['name']} value = {key['name']} style = {{listStyle:'none'}}>{key['name']}</li>
                        <label> Dual Wielding? </label>
                        <input type = 'checkbox' id = 'is-power-stancing' onChange={() => handleIsPowerStancing(key)} hidden = {false}></input>
                        <input type="button" value="Remove" onClick ={() => removeWeapon(key)}></input>
                    </div>
            )}
        }));
        
    }, [chosenWeapons]);

    //Press the add weapon button.
    function addWeapon(){
        if(selectedWeapon['name'] != "" ){
            var temp: Array<Weapon> = [...chosenWeapons];
            temp.push(selectedWeapon);
            setChosenWeapons(temp);
        }
    }

    const removeWeapon = (weapon:Weapon) =>{
        var temp: Array<Weapon> = [...chosenWeapons];
        const index = temp.indexOf(weapon);
        if (index > -1) { // only splice array when item is found
        temp.splice(index, 1); // 2nd parameter means remove one item only
        }
        setChosenWeapons(temp);
    }

    //Handle change in weapon selection
    function handleChangeWeapon(e:any){
        setSelectedWeapon(JSON.parse(e.target.value));
    }

    function handleIsPowerStancing(key:Weapon){
        var tempList:Weapon[] = [...chosenWeapons]
        tempList.forEach(weapon => {
            if(weapon['name'] == key['name']){
                //setIsPowerStancing(!isPowerStancing)
                weapon['isPow'] = !weapon['isPow']
            }
        });

        setChosenWeapons(tempList);
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