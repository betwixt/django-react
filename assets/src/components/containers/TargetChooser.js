import TargetChooser from '../ui/TargetChooser'
import { connect } from 'react-redux'
import { setChosenDate, showTodayColor, showTargetWeek, showChosenDayColor } from '../../colorActions'



const mapStateToProps = state  => null

const mapDispatchToProps = dispatch =>
    ({
        setChosenDate(str){
            dispatch( setChosenDate(str) )
        }, 
        showTodayColor(){
            dispatch( showTodayColor() )
        }, 
        showTargetWeek(){
            dispatch( showTargetWeek() )
        }, 
        showChosenDayColor(){
            dispatch( showChosenDayColor() )
        } 
    })


export default connect( mapStateToProps, mapDispatchToProps )(TargetChooser)
