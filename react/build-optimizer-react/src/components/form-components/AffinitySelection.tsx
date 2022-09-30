import React from 'react';

interface Props{
    keyName:string
}

const AffinitySelection:React.FC<Props> = ({keyName}) => {
    
    return(
        <div>
            <li key = {keyName} value = {keyName}>{keyName}</li>
            <label>Affinity: </label>
            <select defaultValue="standard"> 
                <option value = "standard">Standard</option>
                <option value = "heavy">Heavy</option>
                <option value = "keen">Keen</option>
                <option value = "quality">Quality</option>
                <option value = "magic">Magic</option>
                <option value = "cold">Cold</option>
                <option value = "fire">Fire</option>
                <option value = "flame art">Flame Art</option>
                <option value = "lightning">Lightning</option>
                <option value = "sacred">Sacred</option>
                <option value = "poison">Poison</option>
                <option value = "blood">Blood</option>
                <option value = "occult">Occult</option>
            </select>
        </div>
    );
}

export default AffinitySelection;