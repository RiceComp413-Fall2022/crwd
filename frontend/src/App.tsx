import { Routes, Route } from 'react-router-dom';
import Home from './pages/Main';
import Status from './pages/Status';
import NoPageError from './pages/NoPageError';

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
