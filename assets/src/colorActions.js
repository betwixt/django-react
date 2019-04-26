import C from './colorConstants'
import {daysInMonth} from './components/colorData'
import {computeForDate, computeWeekStartingOn, dateObjFromString } from './components'

// SET_BMONTH: "SET_BMONTH",
// SET_BCALDAY: "SET_BCALDAY",
// SET_MAXDAYS: "SET_MAXDAYS",
// SET_CURRENTDATE: "SET_CURRENTDATE",
// SET_CHOSENDATE: "SET_CHOSENDATE",
// SET_TARGETDATE: "SET_TARGETDATE",
// SET_COLORPANE: "SET_COLORPANE

// Leave out for now, just show every time, default start date is today
// SHOW_WEEKBAR: "SHOW_WEEKBAR",
// HIDE_WEEKBAR: "HIDE_WEEKBAR",

// maybe not needed, same as setTargetDate
// SHOW_TODAY: "SHOW_TODAY",
// SHOW_CHOSENDAY: "SHOW_CHOSENDAY",
// SHOW_BARDAY: "SHOW_BARDAY",

// SET_BARINFO: "SET_BARINFO",
// SET_WEEKSELECT: "SET_WEEKSELECT"

// Action Creators: will return an action object with type (constant) and payload (some type of argument value)
// With Thunk package, can also return a function - (dispatch,getState)=>{stuff}

// Setting of month value causes a constraint on possible values for calendar day
// Is action creator the right place to implement this?
export function setBirthMonth(monthInt) {
	return (dispatch, getState) => {
	  let max = daysInMonth.get(monthInt); 
	  dispatch({
		type: C.SET_MONTHVALS,  payload: monthInt-1
	  });
      dispatch({
        type: C.SET_BMONTH,   payload: monthInt
      });
	  dispatch({
		type: C.SET_MAXDAYS,  payload: max
	  });
	  if (max < getState().birthval.bcalday) {
		   dispatch({ type: C.SET_BCALDAY,   payload: max });
           dispatch({ type: C.SET_DAYVALS,   payload: max-1 })
      }
	}
}
export const setBirthCalDay = num => dispatch => {
    dispatch ({
        type: C.SET_DAYVALS,
        payload: num - 1
    });
	dispatch ({
        type: C.SET_BCALDAY,
        payload: num
    })
}

export const setChosenDate = dateStr =>
	({
		type: C.SET_CHOSENDATE,
		payload: dateStr
	})

export const setColorPane = num =>
	({
		type: C.SET_COLORPANE,
		payload: num
	})
	
export const setBarInfo = arr =>
	({
		type: C.SET_BARINFO,
		payload: arr
	})

export const setWeekActive = bool =>
	({
		type: C.SET_WEEKACTIVE,
		payload: bool
	})

export const setWeekSelect = num =>
	({
		type: C.SET_WEEKSELECT,
		payload: num
	})

	
export function showTodayColor(){ 
	return (dispatch, getState) => {
		const {birthval, chosenDate, colorPane, weekbar} = getState();
		const now = new Date();
		const todayStr = new Date(+now - now.getTimezoneOffset() * 60 * 1000).toISOString().slice(0,10);
		dispatch( setColorPane(computeForDate(todayStr, birthval.bmonth, birthval.bcalday)) );
	}
}

export function showChosenDayColor() {
	return (dispatch, getState) => {
		const {birthval, chosenDate, colorPane, weekbar} = getState();
		dispatch( setColorPane(computeForDate(chosenDate, birthval.bmonth, birthval.bcalday) ) );
	}
}

export function showTargetWeek() {
	return (dispatch, getState) => {
		const {birthval, chosenDate, colorPane, weekbar} = getState();
		
		// Parse string to get tmonth, tdate and tyear, then set state
			console.log("converting date string: " + chosenDate);
		let y = chosenDate.slice(0,4);
		let m = chosenDate.slice(5,7);
		let d = chosenDate.slice(8);
		let dateObj = new Date(y, m-1, d);
		let bar = computeWeekStartingOn(dateObj, birthval.bmonth, birthval.bcalday);
		
        dispatch( setBarInfo(bar) );
        dispatch( setWeekActive(true) );
        dispatch( setWeekSelect(0) );
		dispatch( setColorPane(bar[0].colorNum) );
	}
}
