import React, { useEffect, useState } from 'react';
import TalismanForm from './TalismanForm';

interface Talisman{
    name:string,
    pngUrl:string
}
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
        <div>
            <label>Talismans: </label>
            <TalismanForm slot = {0} talismans = {talismans} setTalismans = {setTalismans} talismanArray = {talismanArray}></TalismanForm>
            <TalismanForm slot = {1} talismans = {talismans} setTalismans = {setTalismans} talismanArray = {talismanArray}></TalismanForm>
            <TalismanForm slot = {2} talismans = {talismans} setTalismans = {setTalismans} talismanArray = {talismanArray}></TalismanForm>
            <TalismanForm slot = {3} talismans = {talismans} setTalismans = {setTalismans} talismanArray = {talismanArray}></TalismanForm>
        </div>
    )
}

export default TalismansForm;