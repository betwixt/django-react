import React, { Component } from 'react';
import PropTypes from 'prop-types'


// Expected props: setChosenDate, showTodayColor, showChosenDayColor
// all functions that manipulate state
class TargetChooser extends Component {

    render() {

	const now = new Date()
	const today = now.toDateString();
	let initDateStr = new Date(+now - now.getTimezoneOffset() * 60 * 1000).toISOString().slice(0,10);
	this.props.setChosenDate(initDateStr);
    console.log("Init target is " + initDateStr);
    let holder;
	
    return(
        <div>
            <div id="today-section">
                <h3 id="today"> Today is: </h3>
                <p> {today}  </p>
                <button  onClick={this.props.showTodayColor} >
                     SHOW MY COLOR!
                </button>
            </div>
            <div id="choosing">
                <p>  Choose a Day:  </p>
                <input type="date" 
                       defaultValue={initDateStr}
                       ref={input => holder = input}
                       onChange={() => this.props.setChosenDate(holder.value)} />
                <button className="pickDay"  onClick={this.props.showChosenDayColor} >
                    MY COLOR for this Day
                </button>
            </div>
            <div id="barbutton">
                <button  onClick={this.props.showTargetWeek}>
                   SHOW Week of Colors
                </button>
            </div>
        </div>
    )}
}

TargetChooser.propTypes = {
	setChosenDate: PropTypes.func,
    showTodayColor: PropTypes.func,
    showChosenDayColor: PropTypes.func,
    showTargetWeek: PropTypes.func
}
export default TargetChooser;
