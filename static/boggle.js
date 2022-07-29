"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;


/** Start */

async function start() {
  let response = await axios.post("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
}

/** Display board */

function displayBoard(board) {
  $table.empty();

  tableBody = $("<tbody>")
  for(let i = 0; i <=5; i++){
    newRow = $("<tr>")
    for(let j = 0; j<=5; j++){
      newCell = $("<td>").innerText(board[i][j])
      newRow.append(newCell)
    }
    tableBody.append(newRow)
  }
}


start();