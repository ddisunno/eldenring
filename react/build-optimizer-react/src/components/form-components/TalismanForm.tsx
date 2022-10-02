import { url } from 'inspector';
import React, { useEffect, useState } from 'react';

interface Talisman{
    name:string,
    pngUrl: string
}
interface Props{
    slot:number,
    talismans: Talisman[],
    setTalismans: React.Dispatch<React.SetStateAction<Talisman[]>>,
    talismanArray:Talisman[]
}

const TalismanForm: React.FC<Props> = ({slot, talismans, setTalismans, talismanArray}) => {

    
    const [talismanOptions, setTalismanOptions] = useState<JSX.Element[]>()
    
   
    useEffect(() => {
        setTalismanOptions(talismanArray.map((key:Talisman) => {
            return <option key = {key['name']} value = {JSON.stringify(key)}>{key['name']}</option>
        }));
    }, [talismanArray]);

    //Handle change in weapon selection
    function handleChangeWeapon(e:any){
        console.log(e.target.value)
        var value = JSON.parse(e.target.value)
        
        var talismanTemp = [...talismans];
        talismanTemp[slot] = {name:value['name'], pngUrl:value['pngUrl']}
        setTalismans(talismanTemp);
    }

    //Everytime talisman array is changed, update the options s.t. all now-incompatable talismans are not options.
    useEffect(() => {
        //The same talisman cannot be used twice. Different levels of the same talisman cannot be used together.

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