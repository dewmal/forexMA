import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'



const MarketQuantitativeFactViewCompoennt = ({ qunatitativeFacts }) => {
	return (<> 
	<h2>Price Quntitative Facts	</h2>
		<ul>
			<li>Time, Asset, Accuracy, Excpected Change, Direction</li>
			{qunatitativeFacts.map((qf) => <li>
				{qf.time_stamp},{qf.asset_name}, {qf.accuracy}, {qf.expected_change},{qf.direction}
			</li>)}
		</ul>
	</>);
}

export default connect((state) => {
	const { makretFacts } = state;
	return { ...makretFacts };
})(MarketQuantitativeFactViewCompoennt);