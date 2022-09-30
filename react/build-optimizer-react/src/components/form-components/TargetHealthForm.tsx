import React from 'react';

interface Props{
    targetHealth: string,
    setTargetHealth: React.Dispatch<React.SetStateAction<string>>
}

const TargetHealthForm: React.FC<Props> = ({targetHealth, setTargetHealth}) => {

    return (
        <div>
            <label>Target Health (345-2415): </label>
            <input type="number" id="tHealth" min = "396" max = "2415" value={targetHealth} onChange = {(e) => setTargetHealth(e.target.value)}></input><br></br>
        </div>
    );
};

export default TargetHealthForm;