import React, { useEffect, useState } from 'react';
import ArmorPieceForm from './ArmorPieceForm';
import {Armor} from './interfaces';

interface Props{
    targetHelm: Armor,
    setTargetHelm: React.Dispatch<React.SetStateAction<Armor>>,

    targetChest: Armor,
    setTargetChest: React.Dispatch<React.SetStateAction<Armor>>,

    targetGauntlets: Armor,
    setTargetGauntlets: React.Dispatch<React.SetStateAction<Armor>>,

    targetLegs: Armor,
    setTargetLegs: React.Dispatch<React.SetStateAction<Armor>>
}

const ArmorForm: React.FC<Props> = ({targetHelm, setTargetHelm, targetChest, setTargetChest, targetGauntlets, setTargetGauntlets, targetLegs, setTargetLegs}) => {
    return(
    <div style = {{position:'relative', margin:'0 auto', padding:40, alignItems:'flex-start', flexDirection:'column', flex:'left', display:'flex', backgroundColor:'white', border:'5,solid,black'}}>
        <label>Armor: </label>
        <div style = {{justifyContent:'flex-start', flex:''}}>
            <ArmorPieceForm type = "Helm" target = {targetHelm} setTarget = {setTargetHelm}></ArmorPieceForm>
            <ArmorPieceForm type = "Chest Armor" target = {targetChest} setTarget = {setTargetChest}></ArmorPieceForm>
            <ArmorPieceForm type = "Gauntlets" target = {targetGauntlets} setTarget = {setTargetGauntlets}></ArmorPieceForm>
            <ArmorPieceForm type = "Leg Armor" target = {targetLegs} setTarget = {setTargetLegs}></ArmorPieceForm>
        </div>
    </div>);
}

export default ArmorForm;