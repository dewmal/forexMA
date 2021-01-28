import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'



const MarketNewsViewCompoennt = ({ texts }) => {
	return (<> News Variations
	
		<ul>
			<li>Time, Text</li>
			{texts.map((text) => <li>
				{text.time_stamp}, {text.text}
			</li>)}
		</ul>
	</>);
}

export default connect((state) => {
	const { marketStatus } = state;
	return { ...marketStatus };
})(MarketNewsViewCompoennt);