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

  let tableBody = $("<tbody>");
  for (let i = 0; i < 5; i++) {
    let newRow = $("<tr>");
    for (let j = 0; j < 5; j++) {
      let newCell = $("<td>").text(board[i][j]);
      newRow.append(newCell);
    }
    tableBody.append(newRow);
  }
  $table.append(tableBody);
}

/**Takes word submission and sends to back end and returns results*/
async function handleSubmit(e) {
  e.preventDefault();

  let word = $wordInput.val();

  let response = await axios.post("/api/score-word", {
    "word": word, "gameId": gameId }  );
  let result = response.data.result;


  if (result !== "ok") {
    invalidWordMessage();
  } else {
    addValidWord(word);
  }
}

/**Displays message indicating invalid word submission on DOM */
function invalidWordMessage() {
  $message.text("This word is invalid! Try again!");
}

/**Adds a valid word submission to bulleted list of valid words */
function addValidWord(word) {

  let newWord = $("<li>").text(word);
  $playedWords.append(newWord);
}

$form.on("submit", handleSubmit);

start();