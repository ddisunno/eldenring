import React, { useEffect, useState } from 'react';
import {Spell} from './interfaces';

interface Props{
    spellList:Spell[],
    setSpellList:React.Dispatch<React.SetStateAction<Spell[]>>
}

//SpellList is the list of chosen spells
const  SpellListForm:React.FC<Props> = ({spellList, setSpellList}) => {

    const [selectedSpell, setSelectedSpell] = useState<Spell>({name:"",pngUrl:""});

    const [spellOptions, setSpellOptions] = useState<Spell[]>([]);
    const [spellOptionsJSX, setSpellOptionsJSX] = useState<JSX.Element[]>();

    const [spellListJSX, setSpellListJSX] = useState<JSX.Element[]>();

    //Get spells from server
    useEffect(() => {
        const spellOpts = async() => {
            try{
                await fetch("http://localhost:5000", {method: 'post', body: JSON.stringify({type: 'getSpells'})}).then(body => body.json().then(res => setSpellOptions(res))); //returns array of strings
            } catch(err) {
                console.error(`Error: ${err}`);
            }        
        }
        spellOpts()
    }, []);
    
    useEffect(() => {
       
        setSpellOptionsJSX(spellOptions.map((key:Spell) => {
            return <option key = {key['name']} value = {JSON.stringify(key)}>{key['name']}</option>
        }));
           
    }, [spellOptions]);

    useEffect(() => {

        setSpellListJSX(spellList.map((key:Spell) => {
            return(
                <div style= {{ width: '100%', display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems:'center'}}>
                    <img src = {key['pngUrl']} width = {50} height = {50}></img>
                    <li key = {key['name']} value = {key['name']} style = {{listStyle:'none'}}>{key['name']}</li>
                    <input type="button" value="Remove" onClick ={() => removeSpell(key)}></input>
                </div>
            )}))
        
    }, [spellList]);

    function handleSpellChange(e:any){
        var value = JSON.parse(e.target.value)
        setSelectedSpell({name:value['name'], pngUrl:value['pngUrl']})
    }

    function addSpell(){
        if(selectedSpell['name'] != "" ){
            var temp: Array<Spell> = [...spellList];
            temp.push(selectedSpell);
            setSpellList(temp);
        }
    }

    function removeSpell(spell:Spell){
        var temp: Array<Spell> = [...spellList];
        const index = temp.indexOf(spell);
        if (index > -1) { // only splice array when item is found
        temp.splice(index, 1); // 2nd parameter means remove one item only
        }
        setSpellList(temp);
    }
    return (  
        <div>
            <label>Spells: </label>
            <select defaultValue="med" onChange = {handleSpellChange}>
                <option value = ""></option>
                {spellOptionsJSX}
            </select>
            <input type="button" value="Add Spell" onClick={addSpell}></input>
            <ul>
                {spellListJSX}
            </ul>
        </div>
    );
}
 
export default SpellListForm;