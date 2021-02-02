import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'



const MarketNewsViewCompoennt = ({ texts }) => {
	return (<div className="p-4 bg-gray-900"> News Variations
	
		<ul>
			{texts.length > 0 ? [texts[0]].map((text) => <li>
				<span className="text-sm">{new Date(text.time_stamp*1000).toLocaleTimeString()}</span>
				<p className="text-indigo-200">
					{text.text}
				</p>
			</li>) : <span></span>}
		</ul>
	</div>
	);
}

export default connect((state) => {
	const { marketStatus } = state;
	return { ...marketStatus };
})(MarketNewsViewCompoennt);