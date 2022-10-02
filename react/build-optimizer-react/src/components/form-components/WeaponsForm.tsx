import React, { useEffect, useState } from 'react';
import AffinitySelection from './AffinitySelection';

interface Weapon{
    name: string,
    somber: boolean,
    affinity: string,
    pngUrl: string
}
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
    const [selectedWeapon, setSelectedWeapon] = useState<Weapon>({name:'',somber:false, affinity:"", pngUrl:""});

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
       
        setWeaponOptions(weaponArray.map((key:Weapon) => {
            return <option key = {key['name']} value = {JSON.stringify(key)}>{key['name']}</option>
        }));
           
    }, [weaponArray]);

    useEffect(() => {
       
        setChosenWeaponsJSX(chosenWeapons.map((key:Weapon) => {
            //If key is not somber weapon, the add affinity
            if(key['somber'] == false){
                return <AffinitySelection chosenWeapons = {chosenWeapons} setChosenWeapons = {setChosenWeapons} keyName = {key}></AffinitySelection>;
            }
            else{
                return(
                    <div style= {{ width: '100%', display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems:'center'}}>
                        <img src = {key['pngUrl']} width = {50} height = {50}></img>
                        <li key = {key['name']} value = {key['name']} style = {{listStyle:'none'}}>{key['name']}</li>
                    </div>
            )}
        }));
        console.log(chosenWeapons);
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
        console.log(e.target.value)
        var value = JSON.parse(e.target.value)
        
        setSelectedWeapon({name:value['name'], somber: value['somber'], affinity:value['affinity'], pngUrl:value['pngUrl']});
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