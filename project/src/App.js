import logo from './logo.svg';
import './App.css';
import ChatSection from './components/ChatSection';
import Login from './components/Login';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Signup from './components/Signup';
function App() {
  return (
    <BrowserRouter>
    <Routes>
      <Route exact path="/" element={<Login />}>
      </Route>
        <Route exact path="/signup" element={<Signup />} />
        <Route exact path="/Chat" element={<ChatSection />} />
       </Routes>
  </BrowserRouter>
  );
}

export default App;
