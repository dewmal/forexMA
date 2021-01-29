import React, { useState } from 'react'
import { connect } from 'react-redux'
import Chart from "react-google-charts";



const MarketPriceViewCompoennt = ({ prices }) => {
	const [showTable, setShowTable] = useState(false);

	return (<div className="p-4">

		<h1 className="text-3xl">Market Status</h1>
		<button onClick={() => setShowTable(true)} className=" text-sm text-black bg-green-400 rounded-sm m-2 p-2">Table</button>
		<button onClick={() => setShowTable(false)} className="text-sm  text-black bg-purple-400 rounded-sm m-2 p-2">Chart</button>

		{showTable ? <ul>
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
			:
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
					backgroundColor:"#e5e5e5",
					candlestick: {
						fallingColor: { strokeWidth: 0, fill: '#a52714' }, // red
						risingColor: { strokeWidth: 0, fill: '#0f9d58' }, // green
					},
				}}
				rootProps={{ 'data-testid': '1' }}
			/>}
	</div>);
}

export default connect((state) => {
	const { marketStatus } = state;
	return { ...marketStatus };
})(MarketPriceViewCompoennt);