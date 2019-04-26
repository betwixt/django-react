
import React, { Component } from 'react';


// Square - Expected props:
//   * value - my label
//   * clickAction - closure, sent from above, to record the user's choice
//   * highlight - boolean, do I render the highlight effect?
//   * disabled - boolean, do I gray out
class Square extends Component {

  render() {

    if (this.props.highlight) {
      return (
          <button 
                style={{backgroundColor : "lightsteelblue"}}
                className="square" 
                onClick={() => this.props.clickAction()}  > 
             {this.props.value}
          </button>
      );
    }

    if (this.props.disabled) {
      return (
          <button 
                style={{color: "gray"}}
                disabled={true}
                className="square" 
                onClick={() => this.props.clickAction()}  > 
             {this.props.value}
          </button>
      );
    }

    return (
          <button  
                className="square" 
                onClick={() => this.props.clickAction()} >
             {this.props.value}
          </button>
    );
  }
}

export default Square;
