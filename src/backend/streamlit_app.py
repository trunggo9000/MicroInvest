import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Micro Invest Wise - Streamlit", page_icon="📈", layout="wide")

st.title("Micro Invest Wise (Streamlit)")
st.caption("Python • Pandas • scikit-learn • Streamlit")

with st.sidebar:
	st.header("Navigation")
	page = st.radio("Go to", ["DCA Simulator", "Simple ML Demo"]) 

@st.cache_data
def simulate_dca(prices: pd.Series, contribution: float) -> pd.DataFrame:
	shares = 0.0
	total_contributed = 0.0
	records = []
	for date, price in prices.items():
		buy_shares = contribution / price if price > 0 else 0
		shares += buy_shares
		total_contributed += contribution
		nav = shares * price
		gain = nav - total_contributed
		records.append({
			"date": date,
			"price": price,
			"shares": shares,
			"total_contributed": total_contributed,
			"nav": nav,
			"gain": gain,
			"gain_pct": (gain / total_contributed * 100) if total_contributed > 0 else 0,
		})
	return pd.DataFrame(records)

if page == "DCA Simulator":
	st.subheader("Dollar-Cost Averaging (DCA) Simulator")
	st.write("Upload a CSV with columns: date, price — or generate synthetic data.")

	col_a, col_b = st.columns(2)
	with col_a:
		contribution = st.number_input("Contribution per period ($)", min_value=0.0, value=100.0, step=10.0)
		periods = st.number_input("Number of periods", min_value=1, value=60, step=1)
	with col_b:
		use_synthetic = st.checkbox("Generate synthetic price series", value=True)
		uploaded = st.file_uploader("Or upload CSV", type=["csv"]) if not use_synthetic else None

	if use_synthetic:
		np.random.seed(42)
		trend = np.linspace(50, 120, int(periods))
		noise = np.random.normal(0, 5, int(periods))
		series = trend + noise
		dates = pd.date_range(end=pd.Timestamp.today(), periods=int(periods), freq="ME")
		prices = pd.Series(series.clip(min=1.0), index=dates)
	else:
		if uploaded is None:
			st.info("Upload a CSV to run the simulation.")
			st.stop()
		df = pd.read_csv(uploaded)
		df["date"] = pd.to_datetime(df["date"]) 
		df = df.sort_values("date")
		prices = pd.Series(df["price"].values, index=df["date"].values)

	results = simulate_dca(prices, contribution)
	st.dataframe(results.tail(10), width="stretch")

	st.metric("Total Contributed", f"${results["total_contributed"].iloc[-1]:,.2f}")
	st.metric("Portfolio Value (NAV)", f"${results["nav"].iloc[-1]:,.2f}")
	st.metric("Gain", f"${results["gain"].iloc[-1]:,.2f}")
	st.metric("Gain %", f"{results["gain_pct"].iloc[-1]:.2f}%")

	st.line_chart(results.set_index("date")["nav"], width="stretch")

else:
	st.subheader("Simple ML Demo: Price trend fit")
	st.write("Fit a linear regression to a synthetic price trend and display coefficients.")

	n = st.slider("Data points", 20, 200, 100, step=10)
	np.random.seed(0)
	x = np.arange(n)
	y = 0.5 * x + 10 + np.random.normal(scale=5, size=n)
	model = LinearRegression()
	model.fit(x.reshape(-1, 1), y)
	coef = float(model.coef_[0])
	intercept = float(model.intercept_)

	st.code(f"y = {coef:.3f} * x + {intercept:.3f}")
	st.line_chart(pd.DataFrame({"x": x, "y": y}), width="stretch")
