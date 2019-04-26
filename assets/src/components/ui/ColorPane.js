import React, { Component } from 'react';
import PropTypes from 'prop-types'
import {colorInfo} from '../colorData'



// ColorPane - Expected props:
//   *colorNum
class ColorPane extends Component {

  render() {
    let c = colorInfo.get(this.props.colorNum);
    let title = c.title;
    let desc = c.desc;
    let bg = c.bg;

    let paneStyle = { backgroundColor: bg };
    return(

        <div id="colorPane" style={paneStyle} >
            <h2> {title} </h2>
            <p> 
                This is where we will say interesting things about what the color stands for!!!!
            </p>
            <p> And have a nice background image :-D </p>
            <p> {desc} </p>
        </div>
    );
  }

}
ColorPane.propTypes = {
    colorNum: PropTypes.number
}
export default ColorPane;
