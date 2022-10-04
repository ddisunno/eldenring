import React, { useEffect, useState } from 'react';
import {Armor, Weapon, Spell, Talisman} from './interfaces';

interface Props{
    pngUrl:string,
    info: Armor | Weapon | Spell | Talisman
}

const ImageWithInfo: React.FC<Props> = ({pngUrl, info}) => {

    const [isHidden, setIsHidden] = useState<boolean>(true);
    const [infoJSX, setInfoJSX] = useState<JSX.Element[]>();

    useEffect(() => {
        var temp:JSX.Element[] = []
        for (const [key, value] of Object.entries(info)) {
            console.log(key + " " + value)
            if(key != 'pngUrl' && key != 'name' && key != 'affinity' && key != 'isPow'){
                var upperKey = key.charAt(0).toUpperCase() + key.slice(1);
                upperKey = (upperKey === 'Somber' ? 'Infusable':upperKey)
                temp.push(<li>{upperKey}: {value.toString()}</li>);
            }
          }
        
        setInfoJSX(temp);
    }, [info]);
    
    return(
        <div id = 'image'>
            <img src = {pngUrl} width = {50} height = {50} onMouseOver = {()=>setIsHidden(false)} onMouseOut = {()=>setIsHidden(true)}></img>
            <div id = 'hidden-info-box' hidden = {isHidden} style = {{position: 'fixed', backgroundColor:'darkslategrey', color:'lightgray', textAlign:'center'}}>
                <ul style = {{display:'inline', margin: 200, listStyle:'none'}}>
                    {infoJSX}
                </ul>
            </div>
        </div>
    )
}

export default ImageWithInfo;