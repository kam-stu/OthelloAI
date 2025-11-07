import React from "react";
import "./Board.css";

function Board({ board, validMoves, onCellClick }) {
  return (
    <div className="board">
      {board.map((row, rowIndex) => (
        <div key={rowIndex} className="row">
          {row.map((cell, colIndex) => (
            <div key={colIndex} className="cell">
              {cell === 1 && "⚫"}
              {cell === 2 && "⚪"}
            </div>
          ))}
        </div>
      ))}
    </div>
  );
}

export default Board;
