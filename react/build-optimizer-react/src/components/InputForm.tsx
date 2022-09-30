import React from 'react';
import TargetLevelForm from './form-components/TargetLevelForm';
import TargetHealthForm from './form-components/TargetHealthForm';
import TargetPoiseForm from './form-components/TargetPoiseForm';
import WeaponsForm from './form-components/WeaponsForm';

interface Props{
    targetLevel: string,
    setTargetLevel: React.Dispatch<React.SetStateAction<string>>, 

    targetHealth: string,
    setTargetHealth: React.Dispatch<React.SetStateAction<string>>, 

    targetPoise: string,
    setTargetPoise: React.Dispatch<React.SetStateAction<string>>,

    weapons: string[],
    setWeapons: React.Dispatch<React.SetStateAction<string[]>>
}

const InputForm: React.FC<Props> = ({targetLevel, setTargetLevel, targetHealth, setTargetHealth, targetPoise, setTargetPoise, weapons, setWeapons}) => {

    return (
      <div>
        <form>
            <TargetLevelForm targetLevel = {targetLevel} setTargetLevel = {setTargetLevel}></TargetLevelForm>

            <TargetHealthForm targetHealth = {targetHealth} setTargetHealth = {setTargetHealth}></TargetHealthForm>
            
            <TargetPoiseForm targetPoise = {targetPoise} setTargetPoise = {setTargetPoise}></TargetPoiseForm>

            <WeaponsForm weapons={weapons} setWeapons ={setWeapons}></WeaponsForm>
        </form>
      </div>
    );
};

export default InputForm;