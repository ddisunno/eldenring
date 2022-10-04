import React, { useState } from 'react';

interface Props{
    build:string[],
    setBuild:React.Dispatch<React.SetStateAction<string[]>>
}

const BuildDisplay: React.FC<Props> = ({build, setBuild}) => {
    
    //Display Level, Starting Class, Stats, Weapon AR, Armor (weight, poise, neg/resistances)
    return(
        <div>

        </div>
    )
}

export default BuildDisplay;