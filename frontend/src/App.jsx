import Nav from "./Components/Nav.jsx";
import Home from './Components/Home.jsx';
import Researchers from './Components/Researchers.jsx';
import Statistics from './Components/Statistics.jsx';
import Users from './Components/Users.jsx';
import Products from "./Components/Products.jsx";
import { Route, Routes } from "react-router-dom";

function App() {
  return (
    <Nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/home" element={<Home />} />
        <Route path="/products" element={<Products/>} />
        <Route path="/researchers" element={<Researchers/>} />
        <Route path="/statistics" element={<Statistics/>} />
        <Route path="/users" element={<Users/>} />
      </Routes>
    </Nav>
  );
}

export default App;
