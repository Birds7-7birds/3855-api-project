import React, { useEffect, useState } from 'react'
import '../App.css';


export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)
    const [index, setIndex] = useState(null);
	const getStats = () => {
	// localhost tester
        fetch(`http://${process.env.REACT_APP_API_URL}:8100/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
                // setIndex(rand_val);
                setIndex(stats['traceID']);

            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>id</th>
							<th>traceID</th>
						</tr>
						<tr>
							<td># id: {stats['id']}</td>
							<td># traceID: {stats['traceID']}</td>
						</tr>
						<tr>
							<td colspan="2">total bids: {stats['num_bids']}</td>
						</tr>
                        <tr>
							<td colspan="2">total items: {stats['num_items_listed']}</td>
						</tr>
						<tr>
							<td colspan="2">Max instabuy price: {stats['max_instabuy_price']}</td>
						</tr>
						<tr>
							<td colspan="2">Max bid: {stats['max_bid']}</td>
						</tr>
					</tbody>
                </table>
                <h3>Last Updated: {stats['last_updated']}</h3>

            </div>
        )
    }
}
