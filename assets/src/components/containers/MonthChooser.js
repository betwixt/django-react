import MonthChooser from '../ui/MonthChooser'
import { connect } from 'react-redux'
import { setBirthMonth } from '../../colorActions'


const mapStateToMonthProps = state =>
    ({
        squares: state.birthval.monthSelectVals
    })


const mapDispatchToMonthProps = dispatch =>
    ({
        setSelection(i){
            dispatch( setBirthMonth(i+1) )
        } 
    })


export default connect(mapStateToMonthProps, mapDispatchToMonthProps)(MonthChooser)
