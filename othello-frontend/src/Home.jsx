import './Home.css'
import { Link } from "react-router-dom"


function Home() {

  return (
    <>
      <div className="logo">
        <h1>Othello AI</h1>
      </div>
      <div className="modeList">
          <Link to="/pvp"><button>Player vs Player</button></Link>
          <Link to="/pvai"><button>Player vs AI</button></Link>
      </div>
    </>
  )
}

export default Home
