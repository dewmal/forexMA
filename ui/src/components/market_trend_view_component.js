import React from 'react';
import { connect } from 'react-redux';
import * as numeral from 'numeral'


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
					<tr className="space-y-2">
						<td><a target="blank" href={"https://www.binance.com/en/trade/" + trend.name + "?layout=pro"}>{trend.name}</a></td>
						<td>{numeral(trend.change).format("00.00%")}</td>
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
			<h3 className="text-sm">Market Trends</h3>
			<ul>
				<TrendTableView trends={(trends.sort((a, b) => b.change - a.change))} />
			</ul>
		</div>
	);
}



export default connect((state) => {
	const { marketStatus } = state;
	return { ...marketStatus };
})(MarketTrendViewComponent);