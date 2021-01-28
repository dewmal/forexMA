import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'



const MarketPriceViewCompoennt = ({ prices }) => {

	return (<> Price Variations
	
		<ul>
			<li>Name, Time, Open, High, Low, Close, Volume</li>
			{prices.map((p) => <li>

				{p.asset_name},
				{p.time_stamp},
				{p.open},
				{p.high},
				{p.low},
				{p.close},
				{p.volume},

			</li>)}
		</ul>

	</>);
}

export default connect((state) => {
	const { marketStatus } = state;
	return { ...marketStatus };
})(MarketPriceViewCompoennt);