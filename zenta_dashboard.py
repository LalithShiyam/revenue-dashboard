import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Function to calculate projections
def calculate_projections(
    years, units_sold, hardware_price, hardware_cost, subscription_fee, subscription_cost, initial_investment
):
    total_units_in_market = [sum(units_sold[:i + 1]) for i in range(len(units_sold))]
    hardware_revenue = [units * hardware_price for units in units_sold]
    recurring_revenue = [total_units_in_market[i] * subscription_fee for i in range(len(years))]
    total_revenue = [hardware_revenue[i] + recurring_revenue[i] for i in range(len(years))]
    cumulative_revenue = [sum(total_revenue[:i + 1]) for i in range(len(total_revenue))]
    hardware_costs = [units * hardware_cost for units in units_sold]
    recurring_costs = [total_units_in_market[i] * subscription_cost for i in range(len(years))]
    total_costs = [hardware_costs[i] + recurring_costs[i] for i in range(len(years))]
    profit = [total_revenue[i] - total_costs[i] for i in range(len(years))]
    profit_margin = [profit[i] / total_revenue[i] * 100 if total_revenue[i] > 0 else 0 for i in range(len(years))]
    roi = [(cumulative_revenue[i] - initial_investment) / initial_investment * 100 for i in range(len(years))]
    return pd.DataFrame({
        "Year": years,
        "Units Sold": units_sold,
        "Hardware Revenue (€)": hardware_revenue,
        "Recurring Revenue (€)": recurring_revenue,
        "Total Revenue (€)": total_revenue,
        "Total Costs (€)": total_costs,
        "Profit (€)": profit,
        "Profit Margin (%)": profit_margin,
        "Cumulative Revenue (€)": cumulative_revenue,
        "ROI (%)": roi
    })

# Streamlit UI
st.title("Dynamic Business Projections: Ark by Zenta")
st.markdown("Adjust the inputs below to see real-time business projections.")

# Inputs: Grouping for better organization
st.sidebar.header("Input Parameters")
col1, col2 = st.columns(2)

with col1:
    years = st.sidebar.number_input("Number of Years", min_value=1, max_value=10, value=5, step=1)
    st.markdown("""
    **Number of Years**:
    - Specifies the duration (in years) for which projections are calculated.
    - Adjust this value to see the impact over a short or extended time frame.
    """)
    
    initial_investment = st.sidebar.number_input("Initial Investment (€)", min_value=0, value=6000000, step=100000)
    st.markdown("""
    **Initial Investment (€)**:
    - The upfront capital you inject into the business.
    - Typically sourced from investors or savings.
    - This will help gauge how quickly the investment pays off over time.
    """)
    
    hardware_price = st.sidebar.number_input("Hardware Price Per Unit (€)", min_value=0, value=15000, step=1000)
    st.markdown("""
    **Hardware Price Per Unit (€)**:
    - The selling price for each unit of hardware.
    - This influences your revenue from hardware sales.
    - Setting this too low may affect profit margins.
    """)
    
    subscription_fee = st.sidebar.number_input("Subscription Fee Per Year (€)", min_value=0, value=2000, step=100)
    st.markdown("""
    **Subscription Fee Per Year (€)**:
    - The annual subscription cost charged to customers for access to the service.
    - Recurring revenue from subscriptions is critical for long-term profitability.
    """)

with col2:
    hardware_cost = st.sidebar.number_input("Hardware Cost Per Unit (€)", min_value=0, value=11000, step=1000)
    st.markdown("""
    **Hardware Cost Per Unit (€)**:
    - The cost associated with manufacturing or acquiring each hardware unit.
    - This affects your gross margin for each unit sold.
    - Lower hardware costs improve profitability.
    """)
    
    subscription_cost = st.sidebar.number_input("Subscription Cost Per Unit Per Year (€)", min_value=0, value=500, step=50)
    st.markdown("""
    **Subscription Cost Per Unit Per Year (€)**:
    - The cost to maintain the subscription services annually (e.g., server hosting, support, updates).
    - It directly affects the profitability of your recurring revenue streams.
    - Lowering this cost increases net profit from subscriptions.
    """)

# Units Sold Inputs
st.sidebar.subheader("Units Sold Per Year")
st.markdown("""
**Units Sold Per Year**:
- The number of units you expect to sell each year.
- Adjust based on sales projections and market demand.
- The more units you sell, the higher your revenue.
""")
units_sold = [st.sidebar.number_input(f"Units Sold in Year {i + 1}", min_value=0, value=100, step=10) for i in range(years)]


# Calculate projections
years_list = list(range(1, years + 1))
data = calculate_projections(years_list, units_sold, hardware_price, hardware_cost, subscription_fee, subscription_cost, initial_investment)

# Display DataFrame
st.subheader("Projections Table")
st.dataframe(data)

# Plot: Revenue Breakdown
fig1 = go.Figure()
fig1.add_trace(go.Bar(x=data["Year"], y=data["Hardware Revenue (€)"], name="Hardware Revenue (€)", marker_color='#3498db'))
fig1.add_trace(go.Bar(x=data["Year"], y=data["Recurring Revenue (€)"], name="Recurring Revenue (€)", marker_color='#ff69b4'))
fig1.update_layout(
    title=dict(
        text="Revenue Breakdown",
        font=dict(size=30)  # Adjust the title size
    ),
   
    barmode="stack",
    xaxis=dict(
        title="Year",
        titlefont=dict(size=20),
        tickfont=dict(size=20),
        showgrid=False  # Disable x-axis gridlines
    ),
    yaxis=dict(
        title="Revenue (€)",
        titlefont=dict(size=20),
        tickfont=dict(size=20),
        showgrid=False  # Disable y-axis gridlines
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig1)
st.markdown("**Formula:**")
st.latex(r"Total\ Revenue = Hardware\ Revenue + Recurring\ Revenue")
st.markdown("**Explanation:** This chart shows the annual contribution of hardware sales and recurring revenue to the total revenue.")




# Plot: Profit vs Costs
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=data["Year"], y=data["Total Costs (€)"], mode='lines+markers', name="Total Costs (€)", line=dict(color='#e74c3c')))
fig2.add_trace(go.Scatter(x=data["Year"], y=data["Profit (€)"], mode='lines+markers', name="Profit (€)", line=dict(color='#2ecc71')))
fig2.update_layout(
    title=dict(
        text="Profit vs Total costs",
        font=dict(size=30)  # Adjust the title size
    ),
    xaxis=dict(
        title="Year",
        titlefont=dict(size=20),
        tickfont=dict(size=20),
        showgrid=False  # Disable x-axis gridlines
    ),
    yaxis=dict(
        title="Amount (€)",
        titlefont=dict(size=20),
        tickfont=dict(size=20),
        showgrid=False  # Disable y-axis gridlines
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig2)
st.markdown("**Formula:**")
st.latex(r"Profit = Total\ Revenue - Total\ Costs")
st.latex(r"Total\ Costs = Hardware\ Costs + Recurring\ Costs")
st.markdown("**Explanation:** This plot compares annual profits with costs, showing how profitability evolves over time.")



# Simplified Cumulative Revenue Plot
fig_revenue = go.Figure()
fig_revenue.add_trace(go.Bar(
    x=data["Year"],
    y=[value / 1_000_000 for value in data["Cumulative Revenue (€)"]],  # Convert to millions
    name="Cumulative Revenue (€M)",
    marker_color='#3498db',
    opacity=0.8
))
fig_revenue.update_layout(
    title=dict(
        text="Cumulative Revenue (€M)",
        font=dict(size=30)  # Adjust the title size
    ),
    xaxis=dict(
        title="Year",
        titlefont=dict(size=20),
        tickfont=dict(size=20),
        showgrid=False  # Disable x-axis gridlines
    ),
    yaxis=dict(
        title="Revenue (€M)",
        titlefont=dict(size=20),
        tickfont=dict(size=20),
        showgrid=False  # Disable y-axis gridlines
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig_revenue)
st.markdown("**Formula:**")
st.latex(r"Cumulative\ Revenue_t = \sum_{i=1}^t Total\ Revenue_i")
st.markdown("**Explanation:** This chart highlights the total revenue generated year-over-year, offering a snapshot of the business's long-term growth.")


# ROI (%) over time

fig_roi = go.Figure()
fig_roi.add_trace(go.Scatter(
    x=data["Year"],
    y=data["ROI (%)"],
    mode='lines+markers',
    name="ROI (%)",
    line=dict(color='#f39c12', width=3),
    marker=dict(size=10)
))
fig_roi.update_layout(
    title=dict(
        text="ROI (%) Over Time",
        font=dict(size=30)
    ),
    xaxis=dict(
        title="Year",
        titlefont=dict(size=20),
        tickfont=dict(size=20),
        showgrid=False
    ),
    yaxis=dict(
        title="ROI (%)",
        titlefont=dict(size=20),
        tickfont=dict(size=20),
        showgrid=False
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig_roi)
st.markdown("**Formula:**")
st.latex(r"ROI(\%) = \frac{Cumulative\ Revenue - Initial\ Investment}{Initial\ Investment} \times 100")
st.markdown("**Explanation:** This plot demonstrates how return on investment evolves annually. It helps track when the initial investment breaks even and how profitable the business becomes.")


# Profit Margin (%)

fig_margin = go.Figure()
fig_margin.add_trace(go.Scatter(
    x=data["Year"],
    y=data["Profit Margin (%)"],
    mode='lines+markers',
    name="Profit Margin (%)",
    line=dict(color='#2ecc71', width=3),
    marker=dict(size=10)
))
fig_margin.update_layout(
    title=dict(
        text="Profit Margin (%) Over Time",
        font=dict(size=30)
    ),
    xaxis=dict(
        title="Year",
        titlefont=dict(size=20),
        tickfont=dict(size=20),
        showgrid=False
    ),
    yaxis=dict(
        title="Profit Margin (%)",
        titlefont=dict(size=20),
        tickfont=dict(size=20),
        showgrid=False
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig_margin)
st.markdown("**Formula:**")
st.latex(r"Profit\ Margin(\%) = \frac{Profit}{Total\ Revenue} \times 100")
st.markdown("**Explanation:** This chart shows the percentage of revenue retained as profit, highlighting operational efficiency and cost management.")


# Revenue vs Costs Breakdown

fig_rev_costs = go.Figure()
fig_rev_costs.add_trace(go.Bar(
    x=data["Year"],
    y=[value / 1_000_000 for value in data["Total Revenue (€)"]],
    name="Total Revenue (€M)",
    marker_color='#3498db'
))
fig_rev_costs.add_trace(go.Bar(
    x=data["Year"],
    y=[value / 1_000_000 for value in data["Total Costs (€)"]],
    name="Total Costs (€M)",
    marker_color='#e74c3c'
))
fig_rev_costs.update_layout(
    title=dict(
        text="Revenue vs Costs Breakdown",
        font=dict(size=30)
    ),
    xaxis=dict(
        title="Year",
        titlefont=dict(size=20),
        tickfont=dict(size=20),
        showgrid=False
    ),
    yaxis=dict(
        title="Amount (€M)",
        titlefont=dict(size=20),
        tickfont=dict(size=20),
        showgrid=False
    ),
    barmode="group",  # Bars side by side
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig_rev_costs)
st.markdown("**Formula:**")
st.latex(r"Revenue\ vs\ Costs:\ Compare\ Total\ Revenue\ and\ Total\ Costs\ for\ each\ year.")
st.markdown("**Explanation:** This visualization compares annual revenue and costs side by side, showing the financial balance and identifying cost-heavy or revenue-dominant periods.")



fig_cum = go.Figure()
fig_cum.add_trace(go.Scatter(
    x=data["Year"],
    y=[value / 1_000_000 for value in data["Cumulative Revenue (€)"]],
    mode='lines+markers',
    name="Cumulative Revenue (€M)",
    line=dict(color='#3498db', width=3),
    marker=dict(size=10)
))
fig_cum.add_trace(go.Scatter(
    x=data["Year"],
    y=[sum(data["Total Costs (€)"][:i+1]) / 1_000_000 for i in range(len(data))],
    mode='lines+markers',
    name="Cumulative Costs (€M)",
    line=dict(color='#e74c3c', width=3),
    marker=dict(size=10)
))
fig_cum.update_layout(
    title=dict(
        text="Cumulative Revenue vs Costs",
        font=dict(size=30)
    ),
    xaxis=dict(
        title="Year",
        titlefont=dict(size=20),
        tickfont=dict(size=20),
        showgrid=False
    ),
    yaxis=dict(
        title="Amount (€M)",
        titlefont=dict(size=20),
        tickfont=dict(size=20),
        showgrid=False
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig_cum)
st.markdown("**Formula:**")
st.latex(r"Cumulative\ Costs_t = \sum_{i=1}^t Total\ Costs_i")
st.latex(r"Cumulative\ Revenue_t = \sum_{i=1}^t Total\ Revenue_i")
st.markdown("**Explanation:** This chart displays the cumulative revenue and costs year-over-year, providing insight into when the business reaches break-even and begins to generate net gains.")



