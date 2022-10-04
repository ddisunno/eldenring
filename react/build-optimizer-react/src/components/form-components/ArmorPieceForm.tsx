import React, { useEffect, useState } from 'react';
import {Armor} from './interfaces';
import './ImageWithInfo';
import ImageWithInfo from './ImageWithInfo';
interface Props{
    type:string
    target:Armor,
    setTarget:React.Dispatch<React.SetStateAction<Armor>>
}

const ArmorPieceForm: React.FC<Props> = ({type, target, setTarget}) => {

    const [armorArray, setArmorArray] = useState<Array<Armor>>([]);
    const [getArmorOptions, setArmorOptions] = useState<JSX.Element[]>()
  
    useEffect(() => {
        const armorList = async() => {
            try{
                await fetch("http://localhost:5000", {method: 'post', body: JSON.stringify({type: 'getArmor', category: type})}).then(body => body.json().then(res => setArmorArray(res))); //returns array of strings
            } catch(err) {
                console.error(`Error: ${err}`);
            }        
        }
        armorList()
    }, []);

    useEffect(() => {
        setArmorOptions(armorArray.map((key:Armor) => {
            return <option key = {key['name']} value = {JSON.stringify(key)}>{key['name']}</option>
        }));
    }, [armorArray]);

    //Handle change in weapon selection
    function handleChangeArmor(e:any){
        console.log(e.target.value)
        var value = JSON.parse(e.target.value)
        
        setTarget({name:value['name'], weight:value['weight'], poise:value['poise'], pngUrl:value['pngUrl']});
    }

    return(
    <div style= {{ width: '100%', display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems:'center'}}>
        <label>{type}: </label>
        {/*<img src = {target['pngUrl']} width = {50} height = {50} ></img>*/}
        <ImageWithInfo pngUrl={target['pngUrl']} info={target}></ImageWithInfo>
       
        <select defaultValue={JSON.stringify({name:"", weight: 0, poise:0, pngUrl:""})} onChange={handleChangeArmor}>
            <option value = {JSON.stringify({name:"", weight: 0, poise:0, pngUrl:""})}>Choose For Me</option>
            <option value = {JSON.stringify({name:"None", weight: 0, poise:0, pngUrl:""})}>Leave Empty</option>
            {getArmorOptions}
        </select>
        
    </div>);
}

export default ArmorPieceForm;