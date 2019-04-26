

//    barInfo: PropTypes.arr,
//    weekdayVals: PropTypes.arr,
//    setResult: PropTypes.func,
//    setWeekday: PropTypes.func,
//    active: PropTypes.bool


import WeekBar  from '../ui/WeekBar'
import { connect } from 'react-redux'
import { setWeekSelect, setColorPane } from '../../colorActions'


const mapStateToProps = state =>
    ({
        barInfo: state.weekbar.barInfo,
        weekdayVals: state.weekbar.weekSelectVals,
        active: state.weekbar.weekActive
    })


const mapDispatchToProps = dispatch =>
    ({
        setWeekday(i){
            dispatch( setWeekSelect(i) )
        }, 
        setResult(i){
            dispatch( setColorPane(i) )
        } 
    })


export default connect(mapStateToProps, mapDispatchToProps)(WeekBar)



