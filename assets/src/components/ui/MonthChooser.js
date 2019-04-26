import React, { Component } from 'react';
import PropTypes from 'prop-types'
import { months } from '../colorData';
import Square from './Square'


// MonthChooser - Expected props from container:  
//	 *squares - array of bool representing which box is selected/highlighted
//   *setSelection - function for Square to call when clicked, updating squares?
class MonthChooser extends Component {


  /* Updating selection has to include removing the old selection */
  // setSelection(i) {
    // const squares = Array(12).fill(false);
    // squares[i] = true;

    // this.setState({squares: squares});
    // this.props.setResult(i+1);  // Number value for month
  // }

  renderSquare(i) {
      return <Square value={months[i]} 
                     clickAction={() => this.props.setSelection(i)} 
                     disabled={false}
                     highlight={this.props.squares[i]}  />;
  }

  render() {  
      return (
           <div className="months">
             <div className="board-row">
                {this.renderSquare(0)}
                {this.renderSquare(1)}
                {this.renderSquare(2)}
                {this.renderSquare(3)}
              </div>
              <div className="board-row">
                {this.renderSquare(4)}
                {this.renderSquare(5)}
                {this.renderSquare(6)}
                {this.renderSquare(7)}
              </div>
              <div className="board-row">
                {this.renderSquare(8)}
                {this.renderSquare(9)}
                {this.renderSquare(10)}
                {this.renderSquare(11)}
              </div>
           </div>
      );
  }
}

MonthChooser.propTypes = {
    squares: PropTypes.array,
    setSelection: PropTypes.func
}
export default MonthChooser;

