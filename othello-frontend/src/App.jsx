import {Routes, Route} from "react-router-dom"
import Home from './Home'
import PvP from './gameModes/PvP/PvP'
import PvAI from './gameModes/PvAI/PvAI'

function App() {
    return (
        <Routes>
            <Route path="/" element={<Home />}/>
            <Route path="/pvp" element={<PvP />} />
            <Route path="/pvai" element={<PvAI />} />
        </Routes>
    )
}

export default App