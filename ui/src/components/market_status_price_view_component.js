import React from 'react'
import { connect } from 'react-redux'
import Chart from "react-google-charts";



const MarketPriceViewCompoennt = ({ prices }) => {

	return (<div className="p-4">

		<h1 className="text-3xl">Market Status</h1>

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

		<Chart
			width={'100%'}
			height={350}
			chartType="CandlestickChart"
			loader={<div>Loading Chart</div>}
			data={[
				['time', 'open', 'high', 'low', 'close'],
				...prices.map((d) => ["" + new Date(d.time_stamp * 1000).toLocaleString(), d.low, d.open, d.close, d.high])
			]}
			options={{
				legend: 'none',
				candlestick: {
					fallingColor: { strokeWidth: 0, fill: '#a52714' }, // red
					risingColor: { strokeWidth: 0, fill: '#0f9d58' }, // green
				},
			}}
			rootProps={{ 'data-testid': '1' }}
		/>
	</div>);
}

export default connect((state) => {
	const { marketStatus } = state;
	return { ...marketStatus };
})(MarketPriceViewCompoennt);