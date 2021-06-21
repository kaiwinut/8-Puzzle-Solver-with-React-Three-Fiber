import ReactDOM from 'react-dom';
import React from 'react';
import Axios from 'axios';

import App from './App';
import './index.css';

// const problem = [[1, 1], [0, 1], [0, 2], [0, 0], [2, 2], [2, 1], [1, 0], [2, 0], [1, 2]];
// const solution = [[1, 1], [2, 1], [2, 2], [1, 2], [1, 1], [2, 1], [2, 0], [1, 0], [0, 0]];

const getPuzzle = () => {
  //console.log("input text >>"+text)
  const puzzle = Axios.post('http://127.0.0.1:5000/getPuzzle', {
    post_text: 'ready!'
  }).then( (res) => {
    const problem = res.data.puzzle;
    const solution = res.data.solution;
    return [problem, solution]
  })
  return puzzle;
};

const puzzle = Promise.resolve(getPuzzle())
puzzle.then((puzzle) => {
  const problem = puzzle[0];
  const solution = puzzle[1];

  const rootElement = document.getElementById("root");
  ReactDOM.render(
    <React.StrictMode>
      <App problem={problem} solution={solution} />
    </React.StrictMode>,
    rootElement
  );
});
