import React from 'react';
import { connect } from 'react-redux';

const MarketTrendViewComponent = ({ trends }) => {
	return (
		<>
			Market Trend
			<ul>
				{(trends.map((t) => {
					return {
						...t,
						change: Math.round(t.change * 10000)/100
					}
				}).sort((a,b)=>b.change-a.change)).map((trend) => <li>
					<a target="blank" href={"https://www.binance.com/en/trade/"+trend.name+"?layout=pro"}>{trend.name}</a>,
					
					{trend.change},{trend.length}</li>)}
			</ul>
		</>
	);
}



export default connect((state) => {
	const { marketStatus } = state;
	return { ...marketStatus };
})(MarketTrendViewComponent);