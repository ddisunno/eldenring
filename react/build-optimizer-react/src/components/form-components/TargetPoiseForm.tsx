import React from 'react';

interface Props{
    targetPoise: string,
    setTargetPoise: React.Dispatch<React.SetStateAction<string>>
}

const TargetPoiseForm: React.FC<Props> = ({targetPoise, setTargetPoise}) => {

    return (
        <div>
            <label>Target Poise (0-133): </label>
            <input type="number" id="tPoise" min = "0" max = "133" value={targetPoise} onChange = {(e) => setTargetPoise(e.target.value)}></input><br></br>
        </div>
    );
};

export default TargetPoiseForm;