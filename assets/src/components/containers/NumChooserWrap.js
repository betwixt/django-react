import NumChooser from '../ui/NumChooser'
import { connect } from 'react-redux'
import { setBirthCalDay } from '../../colorActions'

const mapStateToNumProps = state =>   
    ({
        squares: state.birthval.daySelectVals,
        maxDays: parseInt(state.birthval.maxDays)
    })

const mapDispatchToNumProps = dispatch =>
    ({
        setSelection(i){
            dispatch( setBirthCalDay(i+1) )
        } 
    })

export default connect(mapStateToNumProps, mapDispatchToNumProps)(NumChooser)
