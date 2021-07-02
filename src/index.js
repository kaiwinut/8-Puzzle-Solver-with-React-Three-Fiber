import ReactDOM from 'react-dom';
import React from 'react';
import Axios from 'axios';

import App from './App';
import './index.css';

// If shuffle button is clicked
let generate = false;

const switchGenerate = () => {
  console.log('Switch generate to true!');
  generate = true

  const puzzle = Promise.resolve(makePuzzle(generate))
  puzzle.then((puzzle) => {
    const problem = puzzle[0];
    const solution = puzzle[1];

    const rootElement = document.getElementById("root");
    ReactDOM.render(
      // <React.StrictMode>
        <App problem={problem} solution={solution} generate={switchGenerate} />
      // </React.StrictMode>,
      , rootElement
    );
  });
}

const makePuzzle = (generate=false) => {
  let puzzle;
  let solution;
  let result;
  if (generate) {
    // console.log('Generate Puzzle!');
    result = Axios.post('http://127.0.0.1:5000/generatePuzzle', {
      post_text: 'ready!'
    }).then( (res) => {
      puzzle = res.data.puzzle;
      solution = res.data.solution;
      return [puzzle, solution]
    })
  } else {
    // console.log('Get Puzzle!');
    result = Axios.post('http://127.0.0.1:5000/getPuzzle', {
      post_text: 'ready!'
    }).then( (res) => {
      puzzle = res.data.puzzle;
      solution = res.data.solution;
      return [puzzle, solution]
    })
  }
  return result;
}

const puzzle = Promise.resolve(makePuzzle(generate))
puzzle.then((puzzle) => {
  const problem = puzzle[0];
  const solution = puzzle[1];

  const rootElement = document.getElementById("root");
  ReactDOM.render(
    // <React.StrictMode>
      <App problem={problem} solution={solution} generate={switchGenerate} />
    // </React.StrictMode>,
    , rootElement
  );
});
