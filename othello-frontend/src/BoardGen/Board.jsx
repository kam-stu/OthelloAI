import React from "react";
import "./Board.css";

export default function Board({ board, validMoves, onCellClick, currPlayer, currScore }) {
  return (
    <>
    <h1>Current Player: {currPlayer}</h1>
    <h2>Score: Player 1 = {currScore[1]} | Player 2 = {currScore[2]}</h2>
    <div className="board">
      {board.map((row, rowIndex) => (
        <div key={rowIndex} className="row">
          {row.map((cell, colIndex) => {
            const isValidMove = validMoves.some(
              ([validRow, validCol]) => validRow === rowIndex && validCol === colIndex
            );
            return (
              <div
                key={colIndex}
                className={`cell ${isValidMove ? "valid-move" : ""}`}
                onClick={() => isValidMove && onCellClick(rowIndex, colIndex)}
              >
                {cell === 1 ? "⚫" : cell === 2 ? "⚪" : ""}
              </div>
            );
          })}
        </div>
      ))}
    </div>
    </>
  );
}
