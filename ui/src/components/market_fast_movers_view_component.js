import React from 'react';
import { connect } from 'react-redux';
import * as numeral from 'numeral'


const FastMoverTableView = ({ equilibriums }) => {
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
				{equilibriums.map((eq) =>
					<tr className="space-y-2">
						<td><a target={eq.name} href={"https://www.binance.com/en/trade/" + eq.name + "?layout=pro"}>{eq.name}</a></td>
						<td>{numeral(eq.peak_average).format("00.00%")}</td>
						<td>{eq.peaks_count}</td>
					</tr>

				)}
			</tbody>
		</table>
	</>);
}

const MarketFastMoverViewComponent = ({ equilibriums }) => {
	return (
		<div className="p-2">
			<h3 className="text-sm">Market FastMovers</h3>
			<ul>
				<FastMoverTableView equilibriums={(equilibriums.sort((a, b) => b.peaks_count - a.peaks_count))} />
			</ul>
		</div>
	);
}



export default connect((state) => {
	const { marketStatus } = state;
	return { ...marketStatus };
})(MarketFastMoverViewComponent);