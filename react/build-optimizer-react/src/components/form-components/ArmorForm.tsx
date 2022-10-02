import React, { useEffect, useState } from 'react';
import ArmorPieceForm from './ArmorPieceForm';

interface Armor{
    name:string,
    weight:number,
    poise:number,
    pngUrl:string
}

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
    <div>
        <label>Enter Armor (Leave pieces you wanted calculated blank): </label>
        <ArmorPieceForm type = "Helm" target = {targetHelm} setTarget = {setTargetHelm}></ArmorPieceForm>
        <ArmorPieceForm type = "Chest Armor" target = {targetChest} setTarget = {setTargetChest}></ArmorPieceForm>
        <ArmorPieceForm type = "Gauntlets" target = {targetGauntlets} setTarget = {setTargetGauntlets}></ArmorPieceForm>
        <ArmorPieceForm type = "Leg Armor" target = {targetLegs} setTarget = {setTargetLegs}></ArmorPieceForm>
    </div>);
}

export default ArmorForm;