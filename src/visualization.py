import plotly.express as px
import plotly.graph_objects as go
from src.ml_forecasting import sales_forecasting
from src.customer_segmentation import customer_segmentation

# ── Dark Theme Palette ────────────────────────────────────────
BG_SURFACE  = "#111827"
BG_ELEVATED = "#1a2236"
GRID_COLOR  = "rgba(255,255,255,0.06)"
TEXT_COLOR  = "#e8edf5"
TEXT_MUTED  = "#7a8ba8"
FONT_FAMILY = "Syne, Arial, sans-serif"

COLORS = [
    "#00d2ff", "#7c5af3", "#00e5a0",
    "#ffb347", "#ff4f7b", "#38bdf8",
    "#a78bfa", "#34d399", "#f472b6"
]

# ── Country name fixes ────────────────────────────────────────
# Plotly's locationmode="country names" uses ISO 3166 display names.
# These dataset names differ from what Plotly expects — map them here.
COUNTRY_NAME_FIXES = {
    "Cote d'Ivoire"                    : "Ivory Coast",
    "Myanmar (Burma)"                  : "Myanmar",
    "Democratic Republic of the Congo" : "Democratic Republic of Congo",
    "Republic of the Congo"            : "Republic of Congo",
    "Macedonia"                        : "North Macedonia",
    "Swaziland"                        : "Eswatini",
    "Czech Republic"                   : "Czechia",
}


def _dark_layout(fig, title=""):
    """Apply unified dark theme to any Plotly figure."""
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(family=FONT_FAMILY, size=15, color=TEXT_COLOR),
            x=0.02,
            pad=dict(l=10, t=10)
        ),
        paper_bgcolor=BG_SURFACE,
        plot_bgcolor=BG_SURFACE,
        font=dict(family=FONT_FAMILY, color=TEXT_MUTED, size=12),
        margin=dict(l=20, r=20, t=52, b=20),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            bordercolor=GRID_COLOR,
            borderwidth=1,
            font=dict(color=TEXT_MUTED, size=11),
        ),
        xaxis=dict(
            gridcolor=GRID_COLOR,
            linecolor=GRID_COLOR,
            tickcolor=GRID_COLOR,
            tickfont=dict(color=TEXT_MUTED),
            title_font=dict(color=TEXT_MUTED),
            zeroline=False,
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR,
            linecolor=GRID_COLOR,
            tickcolor=GRID_COLOR,
            tickfont=dict(color=TEXT_MUTED),
            title_font=dict(color=TEXT_MUTED),
            zeroline=False,
        ),
        hoverlabel=dict(
            bgcolor=BG_ELEVATED,
            bordercolor=GRID_COLOR,
            font=dict(family=FONT_FAMILY, color=TEXT_COLOR, size=11),
            namelength=-1,
        ),
        colorway=COLORS,
    )
    return fig


def _dark_axes(fig):
    """Extra pass for subplots / multi-axis figures."""
    fig.update_xaxes(gridcolor=GRID_COLOR, linecolor=GRID_COLOR,
                     tickfont=dict(color=TEXT_MUTED), zeroline=False)
    fig.update_yaxes(gridcolor=GRID_COLOR, linecolor=GRID_COLOR,
                     tickfont=dict(color=TEXT_MUTED), zeroline=False)
    return fig


# ── Chart Functions ───────────────────────────────────────────

def sales_by_region(df):
    fig = px.bar(
        df.groupby("Region")["Sales"].sum().reset_index(),
        x="Region", y="Sales",
        color_discrete_sequence=COLORS,
    )
    fig.update_traces(marker_line_width=0)
    return _dark_layout(fig, "Sales by Region")


def monthly_sales(df):
    monthly = df.groupby("Month Name")["Sales"].sum().reset_index()
    fig = px.line(monthly, x="Month Name", y="Sales",
                  color_discrete_sequence=[COLORS[0]])
    fig.update_traces(line_width=2.5)
    return _dark_layout(fig, "Monthly Sales Trend")


def profit_category(df):
    data = df.groupby("Category")["Profit"].sum().reset_index()
    fig = px.bar(data, x="Category", y="Profit",
                 color="Category",
                 color_discrete_sequence=COLORS)
    fig.update_traces(marker_line_width=0)
    fig.update_layout(showlegend=False)
    return _dark_layout(fig, "Profit by Category")


def discount_profit(df):
    fig = px.scatter(df, x="Discount", y="Profit", color="Category",
                     color_discrete_sequence=COLORS)
    fig.update_traces(marker=dict(size=6, opacity=0.7, line=dict(width=0)))
    return _dark_layout(fig, "Discount vs Profit by Category")


def geo_sales(df):
    # ── Aggregate ──────────────────────────────────────────────
    country_sales = df.groupby("Country")["Sales"].sum().reset_index()

    # ── Fix country names to match Plotly's ISO 3166 display names ──
    # No pycountry needed — locationmode="country names" handles
    # geocoding internally. We only need to fix the 7 names that
    # differ between this dataset and Plotly's expected format.
    country_sales["Country"] = country_sales["Country"].replace(COUNTRY_NAME_FIXES)

    # ── Build choropleth ───────────────────────────────────────
    fig = px.choropleth(
        country_sales,
        locations="Country",
        locationmode="country names",   # ← Plotly handles geocoding directly
        color="Sales",
        hover_name="Country",
        color_continuous_scale=[
            [0.0, "#1e2535"],
            [0.3, "#7c5af3"],
            [0.6, "#00d2ff"],
            [1.0, "#e0f9ff"],
        ],
    )

    fig.update_traces(
        marker_line_color="rgba(255,255,255,0.12)",
        marker_line_width=0.5,
    )

    fig.update_layout(
        paper_bgcolor=BG_SURFACE,
        geo=dict(
            bgcolor="#0a0f1a",
            showframe=False,
            showcoastlines=True,
            coastlinecolor="rgba(255,255,255,0.15)",
            projection_type="natural earth",
        ),
        coloraxis_colorbar=dict(
            tickfont=dict(color=TEXT_MUTED),
            title=dict(font=dict(color=TEXT_MUTED)),
        ),
        margin=dict(l=0, r=0, t=52, b=0),
        title=dict(
            text="Global Sales Distribution",
            font=dict(family=FONT_FAMILY, size=15, color=TEXT_COLOR),
            x=0.02,
        ),
    )

    return fig


def sales_trend(df):
    unique_years = df["Year"].nunique()

    # ── Single year selected → show monthly breakdown instead ──
    # A yearly line chart with 1 data point is meaningless.
    # Monthly view is more useful and always has 12 points to plot.
    if unique_years == 1:
        monthly = (
            df.groupby(["Month", "Month Name"])["Sales"]
            .sum()
            .reset_index()
            .sort_values("Month")
        )
        fig = px.line(monthly, x="Month Name", y="Sales",
                      color_discrete_sequence=[COLORS[0]])
        fig.update_traces(
            line=dict(width=3, color=COLORS[0]),
            fill="tozeroy",
            fillcolor="rgba(0,210,255,0.07)",
            mode="lines+markers",
            marker=dict(size=7, color=COLORS[0]),
        )
        year_label = df["Year"].iloc[0]
        return _dark_layout(fig, f"Monthly Sales Trend — {year_label}")

    # ── Multiple years → show yearly trend as normal ───────────
    sales = df.groupby("Year")["Sales"].sum().reset_index()
    fig = px.line(sales, x="Year", y="Sales",
                  color_discrete_sequence=[COLORS[0]])
    fig.update_traces(
        line=dict(width=3, color=COLORS[0]),
        fill="tozeroy",
        fillcolor="rgba(0,210,255,0.07)",
        mode="lines+markers",
        marker=dict(size=8, color=COLORS[0]),
        hovertemplate="<b>Year %{x}</b><br>Sales: $%{y:,.0f}<extra></extra>",
    )
    fig.update_layout(
        yaxis=dict(tickformat="$,.0s"),   # $2.5M, $3M, $4.5M
    )
    return _dark_layout(fig, "Yearly Sales Trend")


def top_products(df):
    data = df.groupby("Product Name")["Sales"].sum().nlargest(10).reset_index()

    # Readable label for hover
    data["Revenue"] = data["Sales"].apply(lambda s: f"${s:,.0f}")

    fig = px.bar(
        data, x="Sales", y="Product Name", orientation="h",
        color="Sales",
        color_continuous_scale=[[0, "#1a2236"], [1, "#00d2ff"]],
        custom_data=["Revenue"],
    )
    fig.update_traces(
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>Revenue: %{customdata[0]}<extra></extra>",
    )
    fig.update_layout(
        xaxis=dict(
            tickformat="$,.0s",       # $80k, $90k etc.
            tickfont=dict(size=10, color=TEXT_MUTED),
        ),
        yaxis=dict(tickfont=dict(size=10, color=TEXT_MUTED)),
        coloraxis_showscale=False,
    )
    return _dark_layout(fig, "Top 10 Products by Sales")


def segment_sales(df):
    segment = df.groupby("Segment")["Sales"].sum().reset_index()
    fig = px.pie(segment, names="Segment", values="Sales",
                 color_discrete_sequence=COLORS,
                 hole=0.45)
    fig.update_traces(
        textfont=dict(color=TEXT_COLOR),
        marker=dict(line=dict(color=BG_SURFACE, width=2))
    )
    return _dark_layout(fig, "Sales by Customer Segment")


def profit_heatmap(df):
    heatmap_data = df.pivot_table(
        values="Profit", index="Category",
        columns="Region", aggfunc="sum"
    )

    # Build custom hover text matrix: "$135k ✦ Technology / Central"
    hover_matrix = []
    for cat in heatmap_data.index:
        hover_row = []
        for reg in heatmap_data.columns:
            val = heatmap_data.loc[cat, reg]
            sign = "▲" if val >= 0 else "▼"
            formatted = f"${abs(val)/1000:.1f}k"
            hover_row.append(
                f"<b>{cat}</b> · {reg}<br>"
                f"Profit: {sign} {formatted}"
            )
        hover_matrix.append(hover_row)

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=list(heatmap_data.columns),
        y=list(heatmap_data.index),
        text=hover_matrix,
        hovertemplate="%{text}<extra></extra>",
        # NO in-cell text — cells are too narrow, hover is cleaner
        colorscale=[
            [0.0,  "#0d1117"],   # deep dark  (loss)
            [0.15, "#1e1040"],   # dark violet
            [0.4,  "#5b3fa0"],   # mid violet
            [0.65, "#7c5af3"],   # bright violet
            [0.85, "#00b8e6"],   # cyan-blue
            [1.0,  "#00e5ff"],   # bright cyan (top profit)
        ],
        colorbar=dict(
            title=dict(
                text="Profit",
                font=dict(family=FONT_FAMILY, color=TEXT_MUTED, size=11),
            ),
            tickformat="$,.0s",      # $100k, $50k etc.
            tickfont=dict(family=FONT_FAMILY, color=TEXT_MUTED, size=10),
            thickness=12,
            len=0.85,
            outlinewidth=0,
            bgcolor="rgba(0,0,0,0)",
        ),
    ))

    fig.update_layout(
        paper_bgcolor=BG_SURFACE,
        plot_bgcolor=BG_SURFACE,
        font=dict(family=FONT_FAMILY, color=TEXT_MUTED, size=11),
        margin=dict(l=20, r=60, t=52, b=80),
        xaxis=dict(
            tickangle=-40,
            tickfont=dict(size=10, color=TEXT_MUTED),
            gridcolor="rgba(0,0,0,0)",
            linecolor="rgba(0,0,0,0)",
            side="bottom",
        ),
        yaxis=dict(
            tickfont=dict(size=11, color=TEXT_MUTED),
            gridcolor="rgba(0,0,0,0)",
            linecolor="rgba(0,0,0,0)",
            autorange="reversed",     # Furniture at top, Technology at bottom
        ),
        hoverlabel=dict(
            bgcolor=BG_ELEVATED,
            bordercolor=GRID_COLOR,
            font=dict(family=FONT_FAMILY, color=TEXT_COLOR, size=12),
            namelength=-1,
        ),
        title=dict(
            text="Profit Heatmap — Category × Region",
            font=dict(family=FONT_FAMILY, size=15, color=TEXT_COLOR),
            x=0.02, pad=dict(l=10, t=10),
        ),
        height=260,     # taller rows = easier to read
    )

    return fig


def product_demand(df):
    demand = df.groupby("Product Name")["Quantity"].sum().nlargest(10).reset_index()

    # Add readable label column for hover
    demand["Units Sold"] = demand["Quantity"].apply(lambda q: f"{q:,} units")

    fig = px.bar(
        demand, x="Quantity", y="Product Name", orientation="h",
        color="Quantity",
        color_continuous_scale=[[0, "#1a2236"], [1, "#00e5a0"]],
        hover_data={"Quantity": False, "Units Sold": True},
        custom_data=["Units Sold"],
    )
    fig.update_traces(
        marker_line_width=0,
        hovertemplate="<b>%{y}</b><br>%{customdata[0]}<extra></extra>",
    )
    fig.update_layout(
        xaxis=dict(
            tickformat=",d",          # e.g. 800 not 800.0
            ticksuffix=" units",
            tickfont=dict(size=10, color=TEXT_MUTED),
        ),
        yaxis=dict(tickfont=dict(size=10, color=TEXT_MUTED)),
        coloraxis_showscale=False,
    )
    return _dark_layout(fig, "Top 10 Products by Demand")


def forecast_chart(df):
    forecast = sales_forecasting(df)
    fig = px.line(forecast, x="Year", y="Predicted Sales",
                  color_discrete_sequence=[COLORS[2]])
    fig.update_traces(line=dict(width=3, dash="dot"))
    return _dark_layout(fig, "Sales Forecast (ML)")


def customer_clusters(df):
    cluster_data = customer_segmentation(df)
    fig = px.scatter(cluster_data, x="Sales", y="Profit",
                     color="Cluster",
                     color_discrete_sequence=COLORS)
    fig.update_traces(marker=dict(size=7, opacity=0.75, line=dict(width=0)))
    return _dark_layout(fig, "Customer Segmentation")