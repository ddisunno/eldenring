import React, { useEffect, useState } from 'react';
import TalismanForm from './TalismanForm';
import {Talisman} from './interfaces';

interface Props{
    talismans: Talisman[],
    setTalismans: React.Dispatch<React.SetStateAction<Talisman[]>>
}

const TalismansForm: React.FC<Props> = ({talismans, setTalismans}) => {

    const [talismanArray, setTalismanArray] = useState<Array<Talisman>>([]);
    
    //Get talismans from server
    useEffect(() => {
        const talismanList = async() => {
            try{
                await fetch("http://localhost:5000", {method: 'post', body: JSON.stringify({type: 'getTalismans'})}).then(body => body.json().then(res => setTalismanArray(res))); //returns array of strings
            } catch(err) {
                console.error(`Error: ${err}`);
            }        
        }
        talismanList()
    }, []);

    return(
        <div style = {{position:'relative', margin:'0 auto', padding:40, alignItems:'flex-start', flexDirection:'column', flex:'left', display:'center'}}>
            <label>Talismans: </label>
            <TalismanForm slot = {0} talismans = {talismans} setTalismans = {setTalismans} talismanArray = {talismanArray} setTalismanArray = {setTalismanArray}></TalismanForm>
            <TalismanForm slot = {1} talismans = {talismans} setTalismans = {setTalismans} talismanArray = {talismanArray} setTalismanArray = {setTalismanArray}></TalismanForm>
            <TalismanForm slot = {2} talismans = {talismans} setTalismans = {setTalismans} talismanArray = {talismanArray} setTalismanArray = {setTalismanArray}></TalismanForm>
            <TalismanForm slot = {3} talismans = {talismans} setTalismans = {setTalismans} talismanArray = {talismanArray} setTalismanArray = {setTalismanArray}></TalismanForm>
        </div>
    )
}

export default TalismansForm;