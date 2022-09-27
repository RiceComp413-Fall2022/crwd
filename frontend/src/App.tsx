import { Routes, Route } from 'react-router-dom';
import Home from './components/Main';
import Status from './components/Status';
import NoPageError from './components/NoPageError';

function App() {
return (        
    <Routes>
    <Route path='/' element={<Home/>} />
    <Route path='/status' element={<Status/>} />
    <Route path='/*' element={<NoPageError/>} />
  </Routes>
);
}

export default App;