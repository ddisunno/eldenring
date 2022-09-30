import React, {useState} from 'react';
import './App.css';
import InputForm from './components/InputForm';

/** All user-inputted values are sent to the server as string types in JSON format. */
function App() {

  const [targetLevel, setTargetLevel] = useState<string>("");
  const [targetHealth, setTargetHealth] = useState<string>("");
  const [targetPoise, setTargetPoise] = useState<string>("");
  const [weapons, setWeapons] = useState<string[]>([])

  console.log("Level: " + targetLevel);
  console.log("Health: " + targetHealth);
  console.log("Poise: " + targetPoise);

  return (
    <div className="App">
      <InputForm targetLevel = {targetLevel} setTargetLevel = {setTargetLevel} targetHealth = {targetHealth} setTargetHealth = {setTargetHealth} targetPoise = {targetPoise} setTargetPoise = {setTargetPoise} weapons = {weapons}setWeapons = {setWeapons}></InputForm>
    </div>
  );
}

export default App;
