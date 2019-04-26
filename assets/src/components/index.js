import React, {Component} from 'react'
import { Provider } from 'react-redux'

import storeFactory from '../store'
import ColorCalc from './ui/ColorCalc'
import sampleData from '../initialState.json'
import { colorInfo } from './colorData'


const store = storeFactory(sampleData)  

window.store = store

class App extends Component {
  render() {
    return (
       <Provider store={store}>
         <ColorCalc />
       </Provider>
    )
  }
}
export default App;


  // Calculation methods
  //
  // Generalized method for calculating personal day
  // Inputs: bmonth, bdate, targMonth, targDate, targYear
  // Outputs: numbers for personal day, month and year
  //
  export function calculate( bmonth, bdate, targMonth, targDate, targYear) {

    let univYear = reduceDigits( targYear ) ;
    let personalYear = reduceDigits( reduceBirthNums(bmonth, bdate) + univYear );
    let personalMonth = reduceDigits ( personalYear + reduceDigits(targMonth) );
    let personalDay = reduceForPersonalDay(personalMonth, targDate)
    return [ personalDay, personalMonth, personalYear ]

  }

  export function reduceDigits(num) {
     var digitsum = 0;  
     var numstr = num.toString();
     for (var i = 0; i < numstr.length; i++) {
          digitsum +=  parseInt(numstr[i]);
     }
     if ( digitsum === 0 ) {
        // print error or throw exception?
        } else if ( digitsum > 9 ) {
          return reduceDigits (digitsum)
        } else {
          return digitsum;
        }
                                  
  }

  export function reduceBirthNums(m, d) {
     return reduceDigits(m) + reduceDigits(d)
  }


  // When calculating personal day, check for special cases, sum is 11 or 22
  // Note: pMon arg is already reduced
  export function reduceForPersonalDay(pMon, d){
     var dayValue = reduceDigits(d) + pMon;
     if (dayValue < 10 || dayValue === 11 || dayValue === 22) {
        return dayValue;
     } else {
        return reduceDigits(dayValue);
     }
  }
  //================================================================

  // Convert a string with format yyyy-mm-dd to corresponding Date object
  export function dateObjFromString(dateStr) {
    // Parse string to get month, day, year
	console.log("converting date string: " + dateStr);
    let y = dateStr.slice(0,4);
    let m = dateStr.slice(5,7);
    let d = dateStr.slice(8);
	
	return new Date(y, m-1, d)
  }
  
  export function computeForDate(aDate, bmonth, bcalday){
    // aDate arg is a string with format yyyy-mm-dd
    // Return value for color to be displayed   
   
    // Parse string to get month, day, year
    let y = aDate.slice(0,4)
    let m = aDate.slice(5,7)
    let d = aDate.slice(8)

    console.log("Calling calculate with " + aDate );
    let colorNum = (calculate( bmonth, bcalday, m, d, y ))[0];
    return colorNum;
  }


  export function computeWeekStartingOn(startDate, bmonth, bcalday){
    // startDate arg is a Date object
    // Return array of color info: {weekday, calendar #, color name & number}

    let d = new Date( startDate.getTime() );
    let barInfo = [];
    let colorNum, colorName, element;

    for (let i=0; i< 7; i++) {
       colorNum = ( calculate(bmonth, bcalday, d.getMonth()+1, d.getDate(), d.getFullYear()) )[0];
       colorName = colorInfo.get(colorNum).title;
       /* Check for the titles that are too long, abbreviate */
       if (colorNum === 8) { colorName = "Pink / Brown"; }

       element = {
           weekday: d.toDateString().slice(0,3).toUpperCase(),
           calnum: d.getDate(),
           color:  colorName,
           colorNum: colorNum
       }

       barInfo.push(element);

 		console.log("date is " + d.toDateString());
      /* increment to next day */
       d.setDate(d.getDate() + 1);
       // d.setTime(d.getTime() + 86400000); /* doesn't work for DST change */
    }

    return barInfo;

  }
