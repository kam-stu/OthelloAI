import React, { useEffect, useState } from 'react'
import Board from "../../BoardGen/Board"
import './PvAI.css'

function PvAI() {
    const [board, setBoard] = useState(null)
    const [currPlayer, setCurrPlayer] = useState(null)
    const [validMoves, setValidMoves] = useState([])
    const [score, setScore] = useState({ 1:0, 2:0 })
    const [prune, setPrune] = useState(false)
    const [maxDepth, setMaxDepth] = useState(1)
    const [suggestedMove, setSuggestedMove] = useState(null)
    const [debug, setDebug] = useState(false)

    useEffect(() => {
            fetch("http://127.0.0.1:5000/othello/start")
            .then(res => res.json())
            .then(data => {
                setBoard(data.board)
                setCurrPlayer(data.curr_player)
                setScore(data.score)
                setValidMoves(data.valid_moves)
            })
        }, [])
    
    function handleMove(row, col) {
        fetch("http://127.0.0.1:5000/othello/update", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                board,
                curr_player: currPlayer,
                curr_move: [row, col],
                ai: true,
                prune: prune,
                depth: maxDepth,
                debug: debug
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                alert(data.message)
                return
            }
            setBoard(data.board)
            setCurrPlayer(data.curr_player)
            setScore(data.score)
            setValidMoves(data.valid_moves)
            setSuggestedMove(null)
        })
    }
    function aiMove() {
        fetch("http://127.0.0.1:5000/othello/ai_move", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                board,
                curr_player: currPlayer,
                prune: prune,
                max_depth: maxDepth,
                debug: debug
            })
        })
        .then(res => res.json())
        .then(data => {setSuggestedMove(data.suggested_move)})
    }
    if (!board) return <div>Loading Game...</div>
    
        return (
        <>
        <button onClick={aiMove}>AI Helper</button>
        <div className="pruning">
            <label className="switch">
            <input 
            type="checkbox" 
            checked={prune}
            onChange={() => setPrune(!prune)}
            />
            <span className="slider"></span>
            </label>
            <span className="pruneText">Alpha Beta Pruning</span>
        </div>
        
        <div className="debug">
            <label className="switch">
                <input 
                type="checkbox"
                checked={debug}
                onChange={() => setDebug(!debug)}
                />
                <span className="slider"></span>
            </label>
            <span className="debugText">Debug</span>
        </div>
            
        <div className="depth">
            <label>
                Search Depth:&nbsp;
                <input
                type="number"
                min={1}
                max={10}
                value={maxDepth}
                onChange={(e) => setMaxDepth(Number(e.target.value))}
                className="depthInput"
                />
            </label>
        </div>
    
    
        {suggestedMove && (
            <div className="suggested">
                Suggested Move: ({suggestedMove[1]}, {suggestedMove[0]})
            </div>
        )}
        
        <Board 
        board={board}
        validMoves={validMoves}
        onCellClick={handleMove}
        currPlayer={currPlayer}
        currScore={score}/>
        </>
        )
}

export default PvAI