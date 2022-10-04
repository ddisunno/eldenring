import React, { useEffect, useState } from 'react';
import {Talisman} from './interfaces';

interface Props{
    slot:number,
    talismans: Talisman[],
    setTalismans: React.Dispatch<React.SetStateAction<Talisman[]>>,
    talismanArray:Talisman[],
    setTalismanArray:React.Dispatch<React.SetStateAction<Talisman[]>>
}

const TalismanForm: React.FC<Props> = ({slot, talismans, setTalismans, talismanArray, setTalismanArray}) => {

    
    const [talismanOptions, setTalismanOptions] = useState<JSX.Element[]>()
    
   
    useEffect(() => {
        setTalismanOptions(talismanArray.map((key:Talisman) => {
            return <option key = {key['name']} value = {JSON.stringify(key)}>{key['name']}</option>
        }));
    }, [talismanArray]);

    //Handle change in talismanselection
    function handleChangeWeapon(e:any){
        console.log(e.target.value)
        var value = JSON.parse(e.target.value)
        
        var talismanTemp = [...talismans];
        talismanTemp[slot] = {name:value['name'], pngUrl:value['pngUrl']}
        setTalismans(talismanTemp);

        //Remove talisman from talisman list
    }

    //Everytime talisman array is changed, update the options s.t. all now-incompatable talismans are not options.
    useEffect(() => {
        /*
        var temp = [...talismanArray]

        //The same talisman cannot be used twice. Different levels of the same talisman cannot be used together.
        talismans.map((key:Talisman) => {
            if(key['name'] === "Arsenal Charm"){

                var index = temp.map(function(e) { return e.name; }).indexOf('Arsenal Charm +1');
                if (index > -1) { 
                    temp.splice(index, 1); 
                }
            }
        })

        setTalismanArray(temp);
        */
    }, [talismans]);

    return(
        <div style= {{ width: '100%', display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems:'center'}}>
            <label>Talisman {slot+1}: </label>
            <img src = {talismans[slot]['pngUrl']} width = {50} height = {50}></img>
            <select defaultValue="" onChange = {handleChangeWeapon}>
                <option value={JSON.stringify({name:"", pngUrl:""})}></option>
                {talismanOptions}
            </select>
        </div>
    )
}

export default TalismanForm;