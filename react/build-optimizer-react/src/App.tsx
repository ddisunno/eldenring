import React, {useState} from 'react';
import './App.css';
import BuildDisplay from './components/BuildDisplay';
import InputForm from './components/InputForm';



/** All user-inputted values are sent to the server as string types in JSON format. */
function App() {

  const [build, setBuild] = useState<string>('');
  const [optimizedBuild, setOptimizedBuild] = useState<string>('');
  return (
    <div className="App" style = {{position:'relative', margin: 'auto', padding: 20}}>

      <div id = 'header'>
        <h1>Boc's BRILLIANT Build Optimizer</h1>
      </div>

      <div id = "body" style = {{position:'relative', margin: 'auto', padding: 20, flex:'left', display:'flex'}}>
        <div id = 'form'>
          <InputForm build = {build} setBuild = {setBuild} setOptimizedBuild = {setOptimizedBuild}></InputForm> {/** Have to update talismans.json to include all upgraded versions of talismans, and update their images. */}
        </div>
        <div id = 'build-results'>
          <BuildDisplay build = {build} setBuild = {setBuild}></BuildDisplay>
        </div>
      </div>

    </div>
  );
}

export default App;
