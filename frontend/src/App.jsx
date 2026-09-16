import { useEffect, useState } from "react";

function App() {
  const [engagement, setEngagement] = useState(null);
  const [audience, setAudience] = useState(null);
  const [trends, setTrends] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadAnalytics = async () => {
      try {
        const engagementResponse = await fetch(
          "http://localhost:8000/analytics/engagement?likes=100&comments=20&shares=10&views=1000"
        );

        const audienceResponse = await fetch(
          "http://localhost:8000/analytics/audience?followers=1000&new_followers=100&returning_followers=500"
        );

        const trendsResponse = await fetch(
          "http://localhost:8000/analytics/trends?data=100,120,150,180,200"
        );

        if (!engagementResponse.ok || !audienceResponse.ok || !trendsResponse.ok) {
          throw new Error("API request failed");
        }

        setEngagement(await engagementResponse.json());
        setAudience(await audienceResponse.json());
        setTrends(await trendsResponse.json());
      } catch (err) {
        setError(err.message);
      }
    };

    loadAnalytics();
  }, []);

  return (
    <div>
      <h1>CreatorIQ Analytics Dashboard</h1>

      {error && <p>Error: {error}</p>}

      <h2>Engagement</h2>
      {engagement && (
        <p>
          Total Engagement: {engagement.total_engagement} | Rate:{" "}
          {engagement.engagement_rate}%
        </p>
      )}

      <h2>Audience</h2>
      {audience && (
        <p>
          Followers: {audience.followers} | New Followers:{" "}
          {audience.new_followers} | Returning Followers:{" "}
          {audience.returning_followers}
        </p>
      )}

      <h2>Trends</h2>
      {trends && <pre>{JSON.stringify(trends, null, 2)}</pre>}
    </div>
  );
}

export default App;