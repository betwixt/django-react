import React, { Component } from 'react';
import PropTypes from 'prop-types'
import Square from './Square'


// NumChooser - Expected props:  
//	 *squares - array of bool representing which box is selected/highlighted
//   *maxDays - number of days for the currently selected month
//   *setSelection - function for Square to call when clicked, to update state
class NumChooser extends Component {


  // Updating selection has to include removing the old selection 
  // Before actual selection occurs, validate argument 'i' against the
  // month that's currently selected. **TODO**
  // setSelection(i) {
    // const squares = Array(31).fill(false);
    // squares[i] = true;

    // this.setState({squares: squares});
    // this.props.setResult(i+1);
  // }



  renderSquare(i) {
    var isDisabled = i > (this.props.maxDays - 1)

    return <Square value={i + 1} 
                   clickAction={() => this.props.setSelection(i)} 
                   highlight={isDisabled ? false : this.props.squares[i]}  
                   disabled={isDisabled}
           />;
  }

  renderNumberRow(start, end){
    var row = [];
    for (var i=start; i<=end; i++) {

       row.push(this.renderSquare(i)); 
    }
    return row;
  }

  render() {

    return (
           <div className="nums">
              <div className="board-row">
                {this.renderNumberRow(0,6)}
              </div>
              <div className="board-row">
                {this.renderNumberRow(7,13)}
              </div>
              <div className="board-row">
                {this.renderNumberRow(14,20)}
              </div>
              <div className="board-row">
                {this.renderNumberRow(21,27)}
              </div>
              <div className="board-row">
                {this.renderNumberRow(28,30)}
              </div>
            </div>
      );
  }
}

NumChooser.propTypes = {
	squares: PropTypes.array,
    maxDays: PropTypes.number,
    setSelection: PropTypes.func
}
export default NumChooser;

