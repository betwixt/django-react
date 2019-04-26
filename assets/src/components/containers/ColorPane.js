import ColorPane from '../ui/ColorPane'
import { connect } from 'react-redux'


const mapStateToMonthProps = state =>
    ({
        colorNum: parseInt(state.colorPane)
    })


export default connect( mapStateToMonthProps )(ColorPane)
