import { useEffect, useState } from "react";

const API_URL =
  "https://expert-chainsaw-gx76j44jv9jqfvvp9-8000.app.github.dev";

function Dashboard() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);
  const [role, setRole] = useState("");

  const [engagement, setEngagement] = useState(null);
  const [audience, setAudience] = useState(null);
  const [trends, setTrends] = useState(null);
  const [socialMedia, setSocialMedia] = useState(null);

  const [revenue, setRevenue] = useState(null);
  const [revenueTrends, setRevenueTrends] = useState(null);
  const [sponsorships, setSponsorships] = useState(null);
  const [notifications, setNotifications] = useState(null);

  const [loading, setLoading] = useState(false);

  async function handleLogin(e) {
    e.preventDefault();

    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.detail || "Login failed");
        return;
      }

      setMessage(data.message);
      setRole(data.role);
      setLoggedIn(true);
    } catch (error) {
      setMessage("Could not connect to backend");
    }
  }

  useEffect(() => {
    if (!loggedIn) return;

    async function loadDashboard() {
      setLoading(true);

      try {
        const [
          engagementResponse,
          audienceResponse,
          trendsResponse,
          socialResponse,
          revenueResponse,
          revenueTrendsResponse,
          sponsorshipResponse,
          notificationResponse,
        ] = await Promise.all([
          fetch(
            `${API_URL}/analytics/engagement?likes=250&comments=50&shares=25&views=5000`
          ),
          fetch(
            `${API_URL}/analytics/audience?followers=1000&new_followers=100&returning_followers=50`
          ),
          fetch(
            `${API_URL}/analytics/trends?data=100,120,150,180,200`
          ),
          fetch(`${API_URL}/analytics/social-media`),
          fetch(`${API_URL}/revenue/summary`),
          fetch(`${API_URL}/revenue/trends`),
          fetch(`${API_URL}/revenue/sponsorships`),
          fetch(`${API_URL}/revenue/notifications`),
        ]);

        setEngagement(await engagementResponse.json());
        setAudience(await audienceResponse.json());
        setTrends(await trendsResponse.json());
        setSocialMedia(await socialResponse.json());
        setRevenue(await revenueResponse.json());
        setRevenueTrends(await revenueTrendsResponse.json());
        setSponsorships(await sponsorshipResponse.json());
        setNotifications(await notificationResponse.json());
      } catch (error) {
        setMessage("Could not load dashboard data");
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, [loggedIn]);

  function downloadReport(type) {
    window.open(`${API_URL}/revenue/export/${type}`, "_blank");
  }

  if (loggedIn) {
    return (
      <div style={styles.page}>
        <header style={styles.header}>
          <div>
            <h1 style={styles.title}>CreatorIQ Analytics Dashboard</h1>
            <p>
              Welcome, <strong>{username}</strong> | Role: {role}
            </p>
          </div>

          <button
            style={styles.logoutButton}
            onClick={() => {
              setLoggedIn(false);
              setUsername("");
              setPassword("");
            }}
          >
            Logout
          </button>
        </header>

        {loading && <p>Loading dashboard data...</p>}

        <section>
          <h2>Content Analytics</h2>

          <div style={styles.cardGrid}>
            <div style={styles.card}>
              <h3>Total Engagement</h3>
              <p style={styles.metric}>
                {engagement?.total_engagement ?? 0}
              </p>
            </div>

            <div style={styles.card}>
              <h3>Engagement Rate</h3>
              <p style={styles.metric}>
                {engagement?.engagement_rate ?? 0}%
              </p>
            </div>

            <div style={styles.card}>
              <h3>Followers</h3>
              <p style={styles.metric}>
                {audience?.followers ?? 0}
              </p>
            </div>

            <div style={styles.card}>
              <h3>Follower Growth</h3>
              <p style={styles.metric}>
                {audience?.growth_rate ?? 0}%
              </p>
            </div>
          </div>
        </section>

        <section style={styles.section}>
          <h2>Growth Trends</h2>

          <div style={styles.card}>
            <p>
              Data: {trends?.data?.join(" → ") || "No data"}
            </p>
            <p>
              Growth: <strong>{trends?.growth ?? 0}</strong>
            </p>
            <p>
              Growth Rate: <strong>{trends?.growth_rate ?? 0}%</strong>
            </p>
          </div>
        </section>

        <section style={styles.section}>
          <h2>Social Media</h2>

          <div style={styles.cardGrid}>
            {socialMedia?.platforms?.map((platform) => (
              <div style={styles.card} key={platform.platform}>
                <h3>{platform.platform}</h3>
                <p>Followers: {platform.followers}</p>
                <p>Likes: {platform.likes}</p>
                <p>Comments: {platform.comments}</p>
                <p>Shares: {platform.shares}</p>
                <p>Views: {platform.views}</p>
              </div>
            ))}
          </div>
        </section>

        <section style={styles.section}>
          <h2>Revenue Analytics</h2>

          <div style={styles.cardGrid}>
            <div style={styles.card}>
              <h3>Total Revenue</h3>
              <p style={styles.metric}>
                ${revenue?.total_revenue ?? 0}
              </p>
            </div>

            <div style={styles.card}>
              <h3>Sponsorship</h3>
              <p style={styles.metric}>
                ${revenue?.sponsorship_revenue ?? 0}
              </p>
            </div>

            <div style={styles.card}>
              <h3>Ad Revenue</h3>
              <p style={styles.metric}>
                ${revenue?.ad_revenue ?? 0}
              </p>
            </div>

            <div style={styles.card}>
              <h3>Affiliate Revenue</h3>
              <p style={styles.metric}>
                ${revenue?.affiliate_revenue ?? 0}
              </p>
            </div>

            <div style={styles.card}>
              <h3>Subscription Revenue</h3>
              <p style={styles.metric}>
                ${revenue?.subscription_revenue ?? 0}
              </p>
            </div>
          </div>
        </section>

        <section style={styles.section}>
          <h2>Revenue Trends</h2>

          <div style={styles.card}>
            {revenueTrends?.labels?.map((label, index) => (
              <p key={label}>
                <strong>{label}:</strong>{" "}
                ${revenueTrends.values[index]}
              </p>
            ))}
          </div>
        </section>

        <section style={styles.section}>
          <h2>Sponsorship Tracking</h2>

          <div style={styles.cardGrid}>
            {sponsorships?.sponsorships?.map((item) => (
              <div style={styles.card} key={item.id}>
                <h3>{item.brand}</h3>
                <p>{item.campaign}</p>
                <p>Amount: ${item.amount}</p>
                <p>Status: {item.status}</p>
                <p>Due: {item.due_date}</p>
              </div>
            ))}
          </div>
        </section>

        <section style={styles.section}>
          <h2>Notifications & Alerts</h2>

          <div style={styles.card}>
            {notifications?.notifications?.map((item, index) => (
              <p key={index}>
                <strong>{item.type}:</strong> {item.message}
              </p>
            ))}
          </div>
        </section>

        <section style={styles.section}>
          <h2>Reports & Exports</h2>

          <div style={styles.buttonGroup}>
            <button onClick={() => downloadReport("csv")}>
              Export CSV
            </button>

            <button onClick={() => downloadReport("excel")}>
              Export Excel
            </button>

            <button onClick={() => downloadReport("pdf")}>
              Export PDF
            </button>
          </div>
        </section>
      </div>
    );
  }

  return (
    <div style={styles.loginPage}>
      <div style={styles.loginCard}>
        <h1>CreatorIQ Login</h1>

        <form onSubmit={handleLogin}>
          <div>
            <label>Username</label>
            <br />
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              required
            />
          </div>

          <br />

          <div>
            <label>Password</label>
            <br />
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
            />
          </div>

          <br />

          <button type="submit">Login</button>
        </form>

        <p>{message}</p>
      </div>
    </div>
  );
}

const styles = {
  page: {
    padding: "30px",
    fontFamily: "Arial, sans-serif",
    background: "#f5f7fb",
    minHeight: "100vh",
  },

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "30px",
  },

  title: {
    marginBottom: "5px",
  },

  cardGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
    gap: "20px",
  },

  card: {
    background: "white",
    padding: "20px",
    borderRadius: "10px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
  },

  metric: {
    fontSize: "28px",
    fontWeight: "bold",
  },

  section: {
    marginTop: "35px",
  },

  buttonGroup: {
    display: "flex",
    gap: "15px",
    flexWrap: "wrap",
  },

  logoutButton: {
    padding: "10px 18px",
    cursor: "pointer",
  },

  loginPage: {
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    fontFamily: "Arial, sans-serif",
  },

  loginCard: {
    padding: "30px",
    borderRadius: "10px",
    boxShadow: "0 2px 10px rgba(0,0,0,0.15)",
    minWidth: "300px",
  },
};

export default Dashboard;