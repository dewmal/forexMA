import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'



const MarketQuantitativeFactViewCompoennt = ({ qunatitativeFacts }) => {
	return (<div className="p-4">
	<h2>Price Quntitative Facts	</h2>
		<ul>
			<li>Time, Asset, Accuracy, Excpected Change, Direction</li>
			{qunatitativeFacts.map((qf) => <li>
				{new Date(qf.time_stamp*1000).toLocaleTimeString()},{qf.asset_name}, {qf.accuracy}, {qf.expected_change},{qf.direction}
			</li>)}
		</ul>
	</div>);
}

export default connect((state) => {
	const { makretFacts } = state;
	return { ...makretFacts };
})(MarketQuantitativeFactViewCompoennt);