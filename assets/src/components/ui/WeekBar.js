import React, { Component } from 'react';
import PropTypes from 'prop-types'
import './App.css';

// WeekBar - Expected props:  
//   *startDay - Date for first day in the bar
//   *colorNums - array of color numbers for successive days
//   *colorInfo - map of number to display information
//   *active - whether or not to display
//   *items - array representing item selection
//   *setWeekday - closure from parent to update which Day (square) is selected
//   *setResult  - closure from parent to change contents of ColorPane
//
class WeekBar extends Component {

  render() {

    let obj = this.props.barInfo[0];
    if (obj)
    console.log(`What's in props? barInfo[1]: ${obj.weekday}, ${obj.calnum}, ${obj.color}; active: ${this.props.active}`);

    if (! this.props.active) 
       return(
           <div className="barhide">  </div>
    );
    

    // Each item holds info: date num, day-of-week, colorNum
    let info, element, dayNodes = [];

    for (let n=0; n<7; n++) { 

       info = this.props.barInfo[n];

       element = <BarSquare
                    setColor={this.props.setResult}
                    setChoice={() => this.props.setWeekday(n)}
                    highlight={this.props.weekdayVals[n]}
                    dayName={info.weekday}
                    dayNum={info.calnum}
                    colorName={info.color}
                    colorNum={info.colorNum}   />
       dayNodes.push(element);
    }

    return ( 
        <div className="baractive"> 
            {dayNodes}
        </div> 
    );

  }
}

WeekBar.propTypes = {
    barInfo: PropTypes.array,
    weekdayVals: PropTypes.array,
    setResult: PropTypes.func,
    setWeekday: PropTypes.func,
    active: PropTypes.bool.isRequired
}
export default WeekBar;


// BarSquare - Expected props:  
//   *setColor - closure from App to set contents of ColorPane
//   *setChoice - closure from WeekBar to set item selection
//   *highlight - boolean of whether to highlight square
//   *dayName - day of week
//   *dayNum - calendar day
//   *colorNum - number to set contents of ColorPane
//
class BarSquare extends React.Component {

  constructor(){
      super();
  }

  doClickAct() {
    this.props.setColor(this.props.colorNum);
    this.props.setChoice();
  }

  render() {
    var c;
    if (this.props.highlight)  
       c = "barselect";
    else
       c = "barsq"

    return (
        <div onClick={() => this.doClickAct()} className={c}>
            <p className="weekday"> {this.props.dayName} </p>
            <p className="calnum"> {this.props.dayNum} </p>
            <p className="sqtext"> {this.props.colorName} </p>
        </div>
    );

  }
}
