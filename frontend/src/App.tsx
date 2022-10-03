import { Routes, Route } from 'react-router-dom';
import Home from './components/Main';
import Status from './components/Status';
import NoPageError from './components/NoPageError';

function App() {
return (  
  <>    
    <Routes>
    <Route path='/' element={<Home/>} />
    <Route path='/status' element={<Status/>} />
    <Route path='/*' element={<NoPageError/>} />
  </Routes>
  <link
  rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css"
  integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor"
  crossOrigin="anonymous"/>
</>

);
}

export default App;