import React from 'react';

interface Props{
    targetRoll:string,
    setTargetRoll:React.Dispatch<React.SetStateAction<string>>
}

const  RollTypeForm:React.FC<Props> = ({targetRoll, setTargetRoll}) => {

    function handleRollChange(e:any){
        setTargetRoll(e.target.value)
    }

    return (  
        <div>
            <label>Desired Roll Type: </label>
            <select defaultValue="med" onChange = {handleRollChange}>
                <option value = "light">Light</option>
                <option value = "med">Medium</option>
                <option value = "fat">Heavy/Fat</option>
                <option value = 'overencumbered'>Overencumbered</option>
            </select>
        </div>
    );
}
 
export default RollTypeForm;