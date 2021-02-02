import React, { useState, useEffect, useRef } from 'react'
import { connect } from 'react-redux'
import Chart from "react-google-charts";

import * as echarts from 'echarts';


const ChartView = ({ prices }) => {
	const refChart = useRef()
	const [chart, setChart] = useState()

	useEffect(() => {
		if (refChart) {
			console.log(refChart);
			var myChart = echarts.init(refChart.current);
			setChart(myChart)
		}
	}, [refChart]);

	useEffect(() => {
		if (chart && prices) {
			let option = {
				xAxis: {
					data: prices.map((p) => new Date(p.time_stamp * 1000).toLocaleTimeString())
				},
				yAxis: {
					scale: true,
					splitArea: {
						show: true
					}
				},
				series: [{
					type: 'k',
					data: prices.map((p) => [p.open, p.close, p.low, p.high])
				}]
			};
			chart.setOption(option);
		}

	}, [chart, prices]);




	return (
		<>
			Chart
			<div className="w-auto h-48" style={{ height: "300px" }} ref={refChart}></div>
		</>
	);
}


const MarketPriceViewCompoennt = ({ prices }) => {
	const [showTable, setShowTable] = useState(false);

	return (<div className="p-4">

		<h1 className="text-3xl">Market Status</h1>
		<button onClick={() => setShowTable(true)} className=" text-sm text-black bg-green-400 rounded-sm m-2 p-2">Table</button>
		<button onClick={() => setShowTable(false)} className="text-sm  text-black bg-purple-400 rounded-sm m-2 p-2">Chart</button>

		{prices.length > 0 ?
			showTable ? <ul>
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
				<ChartView prices={prices} />
			: <span>Please wait</span>}
	</div>);
}

export default connect((state) => {
	const { marketStatus } = state;
	return { ...marketStatus };
})(MarketPriceViewCompoennt);