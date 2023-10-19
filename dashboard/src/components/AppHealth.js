import React, { useEffect, useState } from 'react'
import '../App.css';


export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)
    const [index, setIndex] = useState(null);
	const getStats = () => {
	// localhost tester
        fetch(`http://${process.env.REACT_APP_API_URL}/healthcheck/health`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
                // setIndex(rand_val);
                setIndex(stats['last_updated']);

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
                <h1>Latest health</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<td colspan="2">audit: {stats['audit']}</td>
						</tr>
                        <tr>
							<td colspan="2">storage: {stats['storage']}</td>
						</tr>
						<tr>
							<td colspan="2">receiver: {stats['receiver']}</td>
						</tr>
						<tr>
							<td colspan="2">processing: {stats['processing']}</td>
						</tr>
					</tbody>
                </table>
                <h3>Last Updated: {stats['last_updated']}</h3>

            </div>
        )
    }
}
