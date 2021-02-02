import React from 'react';
import { connect } from 'react-redux';

const TrendTableView = ({ trends }) => {
	return (<>
		<table class="table-auto w-full text-sm text-left">
			<thead>
				<tr>
					<th>Asset</th>
					<th>Change</th>
					<th>Lot</th>
				</tr>
			</thead>
			<tbody>
				{trends.map((trend) =>

					<tr>
						<td><a target="blank" href={"https://www.binance.com/en/trade/" + trend.name + "?layout=pro"}>{trend.name}</a></td>
						<td>{trend.change}</td>
						<td>{trend.length}</td>
					</tr>

				)}

			</tbody>
		</table>





	</>);
}

const MarketTrendViewComponent = ({ trends }) => {
	return (
		<div className="p-2">
			Market Trend
			<ul>
				<TrendTableView trends={(trends.map((t) => {
					return {
						...t,
						change: Math.round(t.change * 10000) / 100
					}
				}).sort((a, b) => b.change - a.change))} />
			</ul>
		</div>
	);
}



export default connect((state) => {
	const { marketStatus } = state;
	return { ...marketStatus };
})(MarketTrendViewComponent);