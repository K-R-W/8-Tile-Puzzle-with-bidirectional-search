import React, { useState} from "react";
import Tile from "./Tile";
import useForceUpdate from 'use-force-update';
import { TILE_COUNT, GRID_SIZE, BOARD_SIZE, BACKEND_URL } from "./constants"
import { canSwap, shuffle, swap, isSolved, board_to_array, direction_to_index } from "./helpers"

//workaround to our usestate render issues:
var indexes = []

function Board({ imgUrl }) {
  const [tiles, setTiles] = useState([...Array(TILE_COUNT).keys()]);
  const [isStarted, setIsStarted] = useState(false);


  console.log('is started:', isStarted)

  const shuffleTiles = () => {
    const shuffledTiles = shuffle(tiles)
    setTiles(shuffledTiles);
  }

  function swapTiles(tileIndex){
    // return new Promise((resolve,reject) => {
      if (canSwap(tileIndex, tiles.indexOf(tiles.length - 1))) {
        const swappedTiles = swap(tiles, tileIndex, tiles.indexOf(tiles.length - 1))
        setTiles(swappedTiles)
        // forceupdate(swappedTiles);
        // resolve('done')
      }
    //   else{
    //     reject(tileIndex)
    //   }
    // });
  }

  const handleTileClick = (index) => {
    // console.log(tiles)
    swapTiles(index)
    
  }

  const handleShuffleClick = () => {
    shuffleTiles()
  }

  const handleStartClick = () => {
    shuffleTiles()
    setIsStarted(true)
  }

  //our code
  function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
  }
  async function handleSolving (){
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json'},
      body: JSON.stringify({ size:8,board:board_to_array(tiles)})
    };
    if(indexes.length!=0){
      console.log('Saved Time with global array!!');
      var curr = indexes[0];
      indexes=indexes.slice(1);
      swapTiles(curr);
      
    }
    else{
      console.log(requestOptions)
      const response = await fetch(BACKEND_URL, requestOptions); //should be await
      const result = await response.json();
      console.log(result);
      const idx_of_zero = tiles.indexOf(TILE_COUNT-1);
      const newindexes = direction_to_index(result,idx_of_zero);
      console.log(indexes,newindexes);
      indexes=newindexes;
      if(indexes){
        swapTiles(indexes[0]);
      }
    }
  }

  const pieceWidth = Math.round(BOARD_SIZE / GRID_SIZE);
  const pieceHeight = Math.round(BOARD_SIZE / GRID_SIZE);
  const style = {
    width: BOARD_SIZE,
    height: BOARD_SIZE,
  };
  const hasWon = isSolved(tiles)

  return (
    <>
      <ul style={style} className="board">
        {tiles.map((tile, index) => (
          <Tile
            key={tile}
            index={index}
            imgUrl={imgUrl}
            tile={tile}
            width={pieceWidth}
            height={pieceHeight}
            handleTileClick={handleTileClick}
          />
        ))}
      </ul>
      {hasWon && isStarted && <div>Puzzle solved 🧠 🎉</div>}
      {!isStarted ?
        (<button onClick={() => handleStartClick()}>Start game</button>) :
        (<>
        <button onClick={() => handleShuffleClick()}>Restart game</button>
        <button onClick={() => handleSolving()}>get and implement Solution</button>
        </>)}
    </>
  );
}

export default Board;
