import React, { useEffect } from 'react'
import { connect } from 'react-redux';

const ActionViewComponent = ({ allActions }) => {
	// useEffect(()=>{
	// 	console.log(allActions)
	// },[])
	return (
		<>
			Action View
			<ul>
				<li>Time, End Time, Action, Price Variation, Accuracy</li>
				{allActions.map((v) => <li>{v.time_stamp}, {v.action_end_time}, {v.predicted_action}, {v.predicted_price_variation}, {v.accuracy}</li>)}
			</ul>
		</>
	);
}

export default connect((state) => {
	const { marketAction } = state;
	return { ...marketAction };
})(ActionViewComponent);
