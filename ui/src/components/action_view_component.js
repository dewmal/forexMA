import React, { useEffect } from 'react'
import { connect } from 'react-redux';
import { ArrowUpSolid, ArrowDownSolid, DotsHorizontalOutline } from '@graywolfai/react-heroicons'

const ActionViewComponent = ({ allActions }) => {
	return (
		<div className="p-4">
			<h1 className="text-3xl">Predicted Actions</h1>
			<ul>
				{allActions.map((v) => <li>

					<div className="flex m-3">

						<span className={"flex-none w-4 h-4 text-center inline-block align-middle"}>
							{v.predicted_action === "UP" ? <ArrowUpSolid className="bg-green-500" /> : 
							v.predicted_action === "NULL" ? <DotsHorizontalOutline className="bg-gray-500" /> :
							 <ArrowDownSolid  className="bg-red-500" />}
						</span >

						<div className="flex-auto p-3">
							<h4 className="text-xl">{v.predicted_price_variation}</h4>
							<h6 className="text-sm">{v.accuracy}</h6>


							<div className="text-sm">
								{new Date(v.time_stamp * 1000).toLocaleString()}, {new Date(v.action_end_time * 1000).toLocaleString()}
							</div>

						</div>


					</div>

				</li>)}
			</ul>
		</div>
	);
}

export default connect((state) => {
	const { marketAction } = state;
	return { ...marketAction };
})(ActionViewComponent);
