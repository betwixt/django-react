import C from '../colorConstants'
import { combineReducers } from 'redux'

// For each entry in app state, how will state value change, based on a specified action?
export const bmonth = (state=1, action) =>
    (action.type === C.SET_BMONTH) ?
         parseInt(action.payload) :
         state
		 
export const bcalday = (state=1, action) =>
    (action.type === C.SET_BCALDAY) ?
         parseInt(action.payload) :
         state
		 
export function monthSelectVals(state=[], action) {
    if (action.type === C.SET_MONTHVALS){         
		const squares = Array(12).fill(false);
		squares[parseInt(action.payload)] = true;
		return squares;
	}
    return state;
}

export function daySelectVals(state=[], action) {
    if (action.type === C.SET_DAYVALS){         
		const squares = Array(31).fill(false);
		squares[parseInt(action.payload)] = true;
		return squares;
	}
    return state;
}
export const maxDays = (state=31, action) =>
    (action.type === C.SET_MAXDAYS) ?
         parseInt(action.payload) :
         state

/* Not really needed		 
export const currentDate = (state, action) =>
    (action.type === C.SET_CURRENTDATE) ?
         parseInt(action.payload) :
         state
*/

export const chosenDate = (state="", action) =>
    (action.type === C.SET_CHOSENDATE) ?
         action.payload :
         state
		 
export const colorPane = (state=0, action) =>
    (action.type === C.SET_COLORPANE) ?
         parseInt(action.payload) :
         state
		 
export const weekActive = (state=false, action) =>
    (action.type === C.SET_WEEKACTIVE) ?
         action.payload :
         state
		 
export const barInfo = (state=[], action) =>
    (action.type === C.SET_BARINFO) ?
         action.payload :
         state
		 
export function weekSelectVals(state = [true, false, false, false, false, false, false], action) {
    if (action.type === C.SET_WEEKSELECT){         
		const squares = Array(7).fill(false);
		squares[parseInt(action.payload)] = true;
		return squares;
	}
    return state;
}


export default combineReducers({
  birthval: combineReducers({
    bmonth,
    bcalday,
    monthSelectVals,
    daySelectVals,
    maxDays
  }),
  chosenDate,
  colorPane,
  weekbar: combineReducers({
	weekActive,
    barInfo,
    weekSelectVals
  })

})
