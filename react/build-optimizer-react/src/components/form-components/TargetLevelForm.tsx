import React from 'react';

interface Props{
    targetLevel: string,
    setTargetLevel: React.Dispatch<React.SetStateAction<string>>
}

const TargetLevelForm: React.FC<Props> = ({targetLevel, setTargetLevel}) => {

    return (
      <div>
          <label>Target Level (1-713): </label>
          <input type="number" id="tLevel" name = "tLevel" min = "1" max = "713" value={targetLevel} onChange = {(e) => setTargetLevel(e.target.value)}></input><br></br>
      </div>
    );
};

export default TargetLevelForm;