import React, { useEffect, useState } from 'react';
import ImageWithInfo from './ImageWithInfo';
import {Spell} from './interfaces';

interface Props{
    spellList:Spell[],
    setSpellList:React.Dispatch<React.SetStateAction<Spell[]>>
}

//SpellList is the list of chosen spells
const  SpellListForm:React.FC<Props> = ({spellList, setSpellList}) => {

    const [selectedSpell, setSelectedSpell] = useState<Spell>({name:"",pngUrl:"", type:'',effect:"",cost:0, slots:0});

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
                    <ImageWithInfo pngUrl={key['pngUrl']} info={key} name = {key['name']}></ImageWithInfo>
                    <input type="button" value="Remove" onClick ={() => removeSpell(key)}></input>
                </div>
            )}))
        
    }, [spellList]);

    function handleSpellChange(e:any){
        var value = JSON.parse(e.target.value)
        setSelectedSpell(value)
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