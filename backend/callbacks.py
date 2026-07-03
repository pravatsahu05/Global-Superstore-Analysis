from dash import Input, Output, State, html, dcc, callback_context
import plotly.graph_objects as go
import plotly.express as px
from src.visualization import (
    profit_category, top_products, discount_profit,
    geo_sales, profit_heatmap, product_demand,
    customer_clusters, forecast_chart, sales_trend,
)

FONT = "Syne, Arial, sans-serif"
MONO = "'JetBrains Mono', 'Courier New', monospace"

COLORS = [
    "#00d2ff", "#7c5af3", "#00e5a0",
    "#ffb347", "#ff4f7b", "#38bdf8",
]

BG_SURFACE  = "#111827"
BG_ELEVATED = "#1a2236"
GRID_COLOR  = "rgba(255,255,255,0.06)"
TEXT_COLOR  = "#e8edf5"
TEXT_MUTED  = "#7a8ba8"


# ── Number formatter ─────────────────────────────────────────
def _fmt(n):
    """Format large numbers compactly: $12.64M, $1.47M, 25,035, 11.6%"""
    if abs(n) >= 1_000_000:
        return f"${n/1_000_000:.2f}M"
    if abs(n) >= 1_000:
        return f"${n/1_000:.1f}K"
    return f"${n:,.2f}"

# ── KPI card builder ──────────────────────────────────────────
def _kpi_card(icon, label, value, subtitle, accent):
    return html.Div([
        html.Div([
            # Icon bubble
            html.Div(icon, style={
                "fontSize": "1.2rem",
                "background": f"rgba({_hex_to_rgb(accent)},0.15)",
                "borderRadius": "10px",
                "width": "40px", "height": "40px",
                "minWidth": "40px",
                "display": "flex", "alignItems": "center",
                "justifyContent": "center",
            }),
            # Text block
            html.Div([
                html.Div(label, style={
                    "fontSize": "0.58rem", "fontWeight": "700",
                    "letterSpacing": "0.12em", "textTransform": "uppercase",
                    "color": TEXT_MUTED, "fontFamily": FONT,
                    "whiteSpace": "nowrap",
                }),
                html.Div(value, style={
                    "fontSize": "1.25rem", "fontWeight": "800",
                    "color": accent, "fontFamily": MONO,
                    "lineHeight": "1.2",
                    "whiteSpace": "nowrap",
                    "overflow": "hidden",
                    "textOverflow": "ellipsis",
                }),
                html.Div(subtitle, style={
                    "fontSize": "0.56rem", "color": TEXT_MUTED,
                    "fontFamily": FONT, "marginTop": "2px",
                    "whiteSpace": "nowrap",
                }),
            ], style={
                "flex": "1",
                "minWidth": "0",       # allows text-overflow to work in flex
                "overflow": "hidden",
            }),
        ], style={
            "display": "flex", "alignItems": "center", "gap": "10px",
            "overflow": "hidden",
        }),
    ], style={
        "background": "#111827",
        "border": "1px solid rgba(255,255,255,0.07)",
        "borderTop": f"3px solid {accent}",
        "borderRadius": "14px",
        "padding": "14px 12px",
        "boxShadow": f"0 4px 24px rgba({_hex_to_rgb(accent)},0.1)",
        "overflow": "hidden",
        "minWidth": "0",
    })


def _hex_to_rgb(hex_color):
    """Convert #rrggbb to 'r,g,b' string for rgba() use."""
    h = hex_color.lstrip("#")
    return ",".join(str(int(h[i:i+2], 16)) for i in (0, 2, 4))


def _empty_figure(message="No data for selected filters"):
    fig = go.Figure()
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[{
            "text": message,
            "xref": "paper", "yref": "paper",
            "x": 0.5, "y": 0.5,
            "showarrow": False,
            "font": {"size": 14, "color": TEXT_MUTED, "family": FONT},
        }],
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig


# ── Toggle button style helpers ──────────────────────────────
CYAN = "#00d2ff"

def _btn_active():
    """Style for the currently active toggle button."""
    return {
        "padding": "4px 12px",
        "fontSize": "0.62rem", "fontWeight": "700",
        "letterSpacing": "0.1em",
        "border": f"1px solid {CYAN}",
        "borderRadius": "999px",
        "background": "rgba(0,210,255,0.15)",
        "color": CYAN,
        "cursor": "pointer",
        "fontFamily": "Syne, Arial, sans-serif",
        "transition": "all 0.15s",
    }

def _btn_inactive():
    """Style for inactive toggle buttons."""
    return {
        "padding": "4px 12px",
        "fontSize": "0.62rem", "fontWeight": "700",
        "letterSpacing": "0.1em",
        "border": "1px solid rgba(255,255,255,0.12)",
        "borderRadius": "999px",
        "background": "transparent",
        "color": "#4a5f80",
        "cursor": "pointer",
        "fontFamily": "Syne, Arial, sans-serif",
        "transition": "all 0.15s",
    }

def _btn_styles(active_id, *btn_ids):
    """Return a style tuple — active for the matching id, inactive for the rest."""
    return tuple(_btn_active() if bid == active_id else _btn_inactive() for bid in btn_ids)


def _dark_bar(data, x, y, title, color=COLORS[0], orientation="v"):
    fig = px.bar(data, x=x, y=y, orientation=orientation,
                 color_discrete_sequence=[color])
    fig.update_traces(marker_line_width=0)
    fig.update_layout(
        paper_bgcolor=BG_SURFACE, plot_bgcolor=BG_SURFACE,
        font=dict(family=FONT, color=TEXT_MUTED, size=12),
        title=dict(text=title, font=dict(size=14, color=TEXT_COLOR), x=0.02),
        margin=dict(l=20, r=20, t=48, b=20),
        xaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color=TEXT_MUTED), zeroline=False),
        yaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color=TEXT_MUTED), zeroline=False),
        hoverlabel=dict(bgcolor=BG_ELEVATED, font=dict(family=FONT, color=TEXT_COLOR)),
    )
    return fig


def register_callbacks(app, df):

    # ── FILTER HELPER ─────────────────────────────────────────
    def apply_filters(region, country, category, year_range,
                      sales_range, discount_range, segment, shipmode):
        fdf = df.copy()
        if region:
            fdf = fdf[fdf["Region"].isin(region)]
        if country:
            fdf = fdf[fdf["Country"].isin(country)]
        if category:
            fdf = fdf[fdf["Category"].isin(category)]
        if segment:
            fdf = fdf[fdf["Segment"].isin(segment)]
        if shipmode:
            fdf = fdf[fdf["Ship Mode"].isin(shipmode)]
        if year_range:
            fdf = fdf[(fdf["Year"] >= year_range[0]) & (fdf["Year"] <= year_range[1])]
        if sales_range:
            fdf = fdf[(fdf["Sales"] >= sales_range[0]) & (fdf["Sales"] <= sales_range[1])]
        if discount_range:
            fdf = fdf[(fdf["Discount"] >= discount_range[0]) & (fdf["Discount"] <= discount_range[1])]
        return fdf

    # ── FILTER INPUTS (shared across all callbacks) ───────────
    FILTER_INPUTS = [
        Input("region-filter",    "value"),
        Input("country-filter",   "value"),
        Input("category-filter",  "value"),
        Input("year-slider",      "value"),
        Input("sales-slider",     "value"),
        Input("discount-slider",  "value"),
        Input("segment-filter",   "value"),
        Input("shipmode-filter",  "value"),
    ]

    # ── DROPDOWN OPTIONS ──────────────────────────────────────
    @app.callback(
        Output("region-filter",  "options"),
        Output("country-filter", "options"),
        Output("category-filter","options"),
        Output("year-filter",    "options"),
        Input("region-filter",   "value"),
    )
    def populate_dropdowns(selected_region):
        regions    = [{"label": r, "value": r} for r in sorted(df["Region"].unique())]
        categories = [{"label": c, "value": c} for c in sorted(df["Category"].unique())]
        years      = [{"label": y, "value": y} for y in sorted(df["Year"].unique())]
        if selected_region:
            filtered  = df[df["Region"].isin(selected_region)]
            countries = [{"label": c, "value": c} for c in sorted(filtered["Country"].unique())]
        else:
            countries = [{"label": c, "value": c} for c in sorted(df["Country"].unique())]
        return regions, countries, categories, years

    @app.callback(
        Output("country-filter", "value"),
        Input("region-filter",   "value"),
    )
    def reset_country(_):
        return None

    # ── HEADER BADGE + RECORD COUNT ───────────────────────────
    @app.callback(
        Output("filter-badge",  "children"),
        Output("record-count",  "children"),
        *FILTER_INPUTS,
    )
    def update_header(region, country, category, year_range,
                      sales_range, discount_range, segment, shipmode):
        fdf = apply_filters(region, country, category, year_range,
                            sales_range, discount_range, segment, shipmode)
        active = sum([
            bool(region), bool(country), bool(category),
            bool(segment), bool(shipmode),
            year_range != [2011, 2014] if year_range else False,
            sales_range != [0, 22638]  if sales_range else False,
            discount_range != [0, 0.85] if discount_range else False,
        ])
        badge = f"{active} FILTER{'S' if active != 1 else ''} ACTIVE  ·  {len(fdf):,} RECORDS"
        count = f"SHOWING {len(fdf):,} OF {len(df):,} RECORDS"
        return badge, count

    # ── KPI CARDS ─────────────────────────────────────────────
    @app.callback(
        Output("kpi-sales",    "children"),
        Output("kpi-profit",   "children"),
        Output("kpi-orders",   "children"),
        Output("kpi-margin",   "children"),
        Output("kpi-shipping", "children"),
        *FILTER_INPUTS,
    )
    def update_kpis(region, country, category, year_range,
                    sales_range, discount_range, segment, shipmode):
        fdf = apply_filters(region, country, category, year_range,
                            sales_range, discount_range, segment, shipmode)
        if fdf.empty:
            return (
                _kpi_card("💰", "Total Sales",    "$0",   "no data", "#00d2ff"),
                _kpi_card("📈", "Total Profit",   "$0",   "no data", "#00e5a0"),
                _kpi_card("🛒", "Orders",         "0",    "no data", "#7c5af3"),
                _kpi_card("🎯", "Profit Margin",  "0.0%", "no data", "#ffb347"),
                _kpi_card("🚚", "Avg Shipping",   "$0",   "no data", "#ff4f7b"),
            )
        total_sales    = fdf["Sales"].sum()
        total_profit   = fdf["Profit"].sum()
        total_orders   = fdf["Order ID"].nunique()
        margin         = (total_profit / total_sales * 100) if total_sales else 0
        avg_shipping   = fdf["Shipping Cost"].mean()
        yoy = ""
        return (
            _kpi_card("💰", "Total Sales",   _fmt(total_sales),
                      f"{total_orders:,} orders", "#00d2ff"),
            _kpi_card("📈", "Total Profit",  _fmt(total_profit),
                      "net earnings", "#00e5a0"),
            _kpi_card("🛒", "Orders",        f"{total_orders:,}",
                      "unique order IDs", "#7c5af3"),
            _kpi_card("🎯", "Profit Margin", f"{margin:.1f}%",
                      "profit / sales", "#ffb347"),
            _kpi_card("🚚", "Avg Shipping",  f"${avg_shipping:.2f}",
                      "per order", "#ff4f7b"),
        )

    # ── SALES TREND (with toggle) ──────────────────────────────
    @app.callback(
        Output("sales-trend",    "figure"),
        Output("trend-line-btn", "style"),
        Output("trend-bar-btn",  "style"),
        Input("trend-line-btn",  "n_clicks"),
        Input("trend-bar-btn",   "n_clicks"),
        *FILTER_INPUTS,
    )
    def update_sales_trend(n_line, n_bar,
                           region, country, category, year_range,
                           sales_range, discount_range, segment, shipmode):
        fdf = apply_filters(region, country, category, year_range,
                            sales_range, discount_range, segment, shipmode)
        ctx = callback_context
        tid = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else "trend-line-btn"
        active = tid if tid in ("trend-line-btn", "trend-bar-btn") else "trend-line-btn"
        styles = _btn_styles(active, "trend-line-btn", "trend-bar-btn")

        if fdf.empty:
            return (_empty_figure(), *styles)
        if active == "trend-line-btn":
            return (sales_trend(fdf), *styles)
        unique_years = fdf["Year"].nunique()
        if unique_years == 1:
            data = (fdf.groupby(["Month", "Month Name"])["Sales"]
                    .sum().reset_index().sort_values("Month"))
            return (_dark_bar(data, "Month Name", "Sales",
                              f"Monthly Sales — {fdf['Year'].iloc[0]}", COLORS[0]), *styles)
        data = fdf.groupby("Year")["Sales"].sum().reset_index()
        return (_dark_bar(data, "Year", "Sales", "Yearly Sales", COLORS[0]), *styles)

    # ── PROFIT BY CATEGORY (with toggle) ──────────────────────
    @app.callback(
        Output("profit-category", "figure"),
        Output("cat-bar-btn",     "style"),
        Output("cat-pie-btn",     "style"),
        Output("cat-line-btn",    "style"),
        Input("cat-bar-btn",  "n_clicks"),
        Input("cat-pie-btn",  "n_clicks"),
        Input("cat-line-btn", "n_clicks"),
        *FILTER_INPUTS,
    )
    def update_profit_category(n_bar, n_pie, n_line,
                               region, country, category, year_range,
                               sales_range, discount_range, segment, shipmode):
        fdf = apply_filters(region, country, category, year_range,
                            sales_range, discount_range, segment, shipmode)
        ctx = callback_context
        tid = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else "cat-bar-btn"
        active = tid if tid in ("cat-bar-btn","cat-pie-btn","cat-line-btn") else "cat-bar-btn"
        mode = {"cat-pie-btn": "pie", "cat-line-btn": "line"}.get(active, "bar")
        styles = _btn_styles(active, "cat-bar-btn", "cat-pie-btn", "cat-line-btn")
        if fdf.empty:
            return (_empty_figure(), *styles)

        data = fdf.groupby("Category")["Profit"].sum().reset_index()
        data = fdf.groupby("Category")["Profit"].sum().reset_index()
        if mode == "pie":
            fig = px.pie(data, names="Category", values="Profit",
                         color_discrete_sequence=COLORS, hole=0.4)
            fig.update_traces(
                textfont=dict(color=TEXT_COLOR),
                marker=dict(line=dict(color="#111827", width=2))
            )
            fig.update_layout(
                paper_bgcolor=BG_SURFACE,
                font=dict(family=FONT, color=TEXT_MUTED),
                title=dict(text="Profit by Category",
                           font=dict(size=14, color=TEXT_COLOR), x=0.02),
                margin=dict(l=20, r=20, t=48, b=20),
                legend=dict(font=dict(color=TEXT_MUTED)),
                hoverlabel=dict(bgcolor=BG_ELEVATED,
                                font=dict(family=FONT, color=TEXT_COLOR)),
            )
            return (fig, *styles)
        elif mode == "line":
            fig = px.line(data, x="Category", y="Profit",
                          color_discrete_sequence=[COLORS[1]])
            fig.update_traces(line=dict(width=3), mode="lines+markers",
                              marker=dict(size=8))
            fig.update_layout(
                paper_bgcolor=BG_SURFACE, plot_bgcolor=BG_SURFACE,
                font=dict(family=FONT, color=TEXT_MUTED),
                title=dict(text="Profit by Category",
                           font=dict(size=14, color=TEXT_COLOR), x=0.02),
                margin=dict(l=20, r=20, t=48, b=20),
                xaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color=TEXT_MUTED)),
                yaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color=TEXT_MUTED)),
            )
            return (fig, *styles)
        return (profit_category(fdf), *styles)

    # ── TOP PRODUCTS (with toggle) ─────────────────────────────
    @app.callback(
        Output("top-products",  "figure"),
        Output("prod-bar-btn",  "style"),
        Output("prod-line-btn", "style"),
        Input("prod-bar-btn",   "n_clicks"),
        Input("prod-line-btn",  "n_clicks"),
        *FILTER_INPUTS,
    )
    def update_top_products(n_bar, n_line,
                            region, country, category, year_range,
                            sales_range, discount_range, segment, shipmode):
        fdf = apply_filters(region, country, category, year_range,
                            sales_range, discount_range, segment, shipmode)
        ctx = callback_context
        tid = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else "prod-bar-btn"
        active = tid if tid in ("prod-bar-btn","prod-line-btn") else "prod-bar-btn"
        styles = _btn_styles(active, "prod-bar-btn", "prod-line-btn")
        if fdf.empty:
            return (_empty_figure(), *styles)
        if active == "prod-line-btn":
            data = fdf.groupby("Product Name")["Sales"].sum().nlargest(10).reset_index()
            fig = px.line(data, x="Sales", y="Product Name", orientation="h",
                          color_discrete_sequence=[COLORS[2]])
            fig.update_traces(mode="lines+markers", marker=dict(size=7))
            fig.update_layout(
                paper_bgcolor=BG_SURFACE, plot_bgcolor=BG_SURFACE,
                font=dict(family=FONT, color=TEXT_MUTED),
                title=dict(text="Top 10 Products",
                           font=dict(size=14, color=TEXT_COLOR), x=0.02),
                margin=dict(l=20, r=20, t=48, b=20),
                xaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color=TEXT_MUTED)),
                yaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(size=10, color=TEXT_MUTED)),
            )
            return (fig, *styles)
        return (top_products(fdf), *styles)

    # ── DISCOUNT vs PROFIT (with toggle) ──────────────────────
    @app.callback(
        Output("discount-profit",  "figure"),
        Output("disc-scatter-btn", "style"),
        Output("disc-bar-btn",     "style"),
        Input("disc-scatter-btn",  "n_clicks"),
        Input("disc-bar-btn",      "n_clicks"),
        *FILTER_INPUTS,
    )
    def update_discount_profit(n_scatter, n_bar,
                               region, country, category, year_range,
                               sales_range, discount_range, segment, shipmode):
        fdf = apply_filters(region, country, category, year_range,
                            sales_range, discount_range, segment, shipmode)
        ctx = callback_context
        tid = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else "disc-scatter-btn"
        active = tid if tid in ("disc-scatter-btn","disc-bar-btn") else "disc-scatter-btn"
        styles = _btn_styles(active, "disc-scatter-btn", "disc-bar-btn")
        if fdf.empty:
            return (_empty_figure(), *styles)
        if active == "disc-bar-btn":
            data = (fdf.groupby("Category")
                    .agg(Avg_Discount=("Discount","mean"), Avg_Profit=("Profit","mean"))
                    .reset_index())
            fig = px.bar(data, x="Category", y="Avg_Profit",
                         color="Category", color_discrete_sequence=COLORS)
            fig.update_traces(marker_line_width=0)
            fig.update_layout(
                paper_bgcolor=BG_SURFACE, plot_bgcolor=BG_SURFACE,
                font=dict(family=FONT, color=TEXT_MUTED),
                title=dict(text="Avg Profit by Category",
                           font=dict(size=14, color=TEXT_COLOR), x=0.02),
                margin=dict(l=20, r=20, t=48, b=20),
                xaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color=TEXT_MUTED)),
                yaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color=TEXT_MUTED)),
                showlegend=False,
            )
            return (fig, *styles)
        return (discount_profit(fdf), *styles)

    # ── PROFIT HEATMAP (with toggle) ───────────────────────────
    @app.callback(
        Output("profit-heatmap",  "figure"),
        Output("heat-heatmap-btn","style"),
        Output("heat-bar-btn",    "style"),
        Input("heat-heatmap-btn", "n_clicks"),
        Input("heat-bar-btn",     "n_clicks"),
        *FILTER_INPUTS,
    )
    def update_profit_heatmap(n_heat, n_bar,
                              region, country, category, year_range,
                              sales_range, discount_range, segment, shipmode):
        fdf = apply_filters(region, country, category, year_range,
                            sales_range, discount_range, segment, shipmode)
        ctx = callback_context
        tid = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else "heat-heatmap-btn"
        active = tid if tid in ("heat-heatmap-btn","heat-bar-btn") else "heat-heatmap-btn"
        styles = _btn_styles(active, "heat-heatmap-btn", "heat-bar-btn")
        if fdf.empty:
            return (_empty_figure(), *styles)
        if active == "heat-bar-btn":
            data = fdf.groupby("Region")["Profit"].sum().reset_index()
            return (_dark_bar(data, "Region", "Profit", "Profit by Region", COLORS[3]), *styles)
        return (profit_heatmap(fdf), *styles)

    # ── PRODUCT DEMAND (with toggle) ───────────────────────────
    @app.callback(
        Output("product-demand", "figure"),
        Output("dem-bar-btn",    "style"),
        Output("dem-line-btn",   "style"),
        Input("dem-bar-btn",     "n_clicks"),
        Input("dem-line-btn",    "n_clicks"),
        *FILTER_INPUTS,
    )
    def update_product_demand(n_bar, n_line,
                              region, country, category, year_range,
                              sales_range, discount_range, segment, shipmode):
        fdf = apply_filters(region, country, category, year_range,
                            sales_range, discount_range, segment, shipmode)
        ctx = callback_context
        tid = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else "dem-bar-btn"
        active = tid if tid in ("dem-bar-btn","dem-line-btn") else "dem-bar-btn"
        styles = _btn_styles(active, "dem-bar-btn", "dem-line-btn")
        if fdf.empty:
            return (_empty_figure(), *styles)
        if active == "dem-line-btn":
            data = (fdf.groupby("Product Name")["Quantity"]
                    .sum().nlargest(10).reset_index())
            fig = px.line(data, x="Quantity", y="Product Name",
                          color_discrete_sequence=[COLORS[5]])
            fig.update_traces(mode="lines+markers", marker=dict(size=7))
            fig.update_layout(
                paper_bgcolor=BG_SURFACE, plot_bgcolor=BG_SURFACE,
                font=dict(family=FONT, color=TEXT_MUTED),
                title=dict(text="Top 10 Products by Demand",
                           font=dict(size=14, color=TEXT_COLOR), x=0.02),
                margin=dict(l=20, r=20, t=48, b=20),
                xaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(color=TEXT_MUTED)),
                yaxis=dict(gridcolor=GRID_COLOR, tickfont=dict(size=10, color=TEXT_MUTED)),
            )
            return (fig, *styles)
        return (product_demand(fdf), *styles)

    # ── CUSTOMER SEGMENTATION (with toggle) ────────────────────
    @app.callback(
        Output("customer-segmentation", "figure"),
        Output("seg-scatter-btn",        "style"),
        Output("seg-bar-btn",            "style"),
        Input("seg-scatter-btn",         "n_clicks"),
        Input("seg-bar-btn",             "n_clicks"),
        *FILTER_INPUTS,
    )
    def update_customer_seg(n_scatter, n_bar,
                            region, country, category, year_range,
                            sales_range, discount_range, segment, shipmode):
        fdf = apply_filters(region, country, category, year_range,
                            sales_range, discount_range, segment, shipmode)
        ctx = callback_context
        tid = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else "seg-scatter-btn"
        active = tid if tid in ("seg-scatter-btn","seg-bar-btn") else "seg-scatter-btn"
        styles = _btn_styles(active, "seg-scatter-btn", "seg-bar-btn")
        if fdf.empty:
            return (_empty_figure(), *styles)
        if active == "seg-bar-btn":
            data = fdf.groupby("Segment")["Sales"].sum().reset_index()
            return (_dark_bar(data, "Segment", "Sales", "Sales by Segment", COLORS[1]), *styles)
        return (customer_clusters(fdf), *styles)

    # ── SALES FORECAST (with toggle) ───────────────────────────
    @app.callback(
        Output("sales-forecast", "figure"),
        Output("fore-line-btn",  "style"),
        Output("fore-bar-btn",   "style"),
        Input("fore-line-btn",   "n_clicks"),
        Input("fore-bar-btn",    "n_clicks"),
        *FILTER_INPUTS,
    )
    def update_forecast(n_line, n_bar,
                        region, country, category, year_range,
                        sales_range, discount_range, segment, shipmode):
        fdf = apply_filters(region, country, category, year_range,
                            sales_range, discount_range, segment, shipmode)
        ctx = callback_context
        tid = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else "fore-line-btn"
        active = tid if tid in ("fore-line-btn","fore-bar-btn") else "fore-line-btn"
        styles = _btn_styles(active, "fore-line-btn", "fore-bar-btn")
        if fdf.empty:
            return (_empty_figure(), *styles)
        if active == "fore-bar-btn":
            from src.ml_forecasting import sales_forecasting
            data = sales_forecasting(fdf)
            return (_dark_bar(data, "Year", "Predicted Sales", "Sales Forecast (ML)", COLORS[2]), *styles)
        return (forecast_chart(fdf), *styles)

    # ── GEO MAP (with toggle) ──────────────────────────────────
    @app.callback(
        Output("geo-sales",  "figure"),
        Output("geo-map-btn","style"),
        Output("geo-bar-btn","style"),
        Input("geo-map-btn", "n_clicks"),
        Input("geo-bar-btn", "n_clicks"),
        *FILTER_INPUTS,
    )
    def update_geo(n_map, n_bar,
                   region, country, category, year_range,
                   sales_range, discount_range, segment, shipmode):
        fdf = apply_filters(region, country, category, year_range,
                            sales_range, discount_range, segment, shipmode)
        ctx = callback_context
        tid = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else "geo-map-btn"
        active = tid if tid in ("geo-map-btn","geo-bar-btn") else "geo-map-btn"
        styles = _btn_styles(active, "geo-map-btn", "geo-bar-btn")
        if fdf.empty:
            return (_empty_figure(), *styles)
        if active == "geo-bar-btn":
            data = (fdf.groupby("Country")["Sales"].sum().nlargest(20).reset_index())
            return (_dark_bar(data, "Sales", "Country",
                              "Top 20 Countries by Sales", COLORS[4], orientation="h"), *styles)
        return (geo_sales(fdf), *styles)

    # ── EXPORT CSV ─────────────────────────────────────────────
    @app.callback(
        Output("download-data", "data"),
        Input("download-btn", "n_clicks"),
        State("region-filter",   "value"),
        State("country-filter",  "value"),
        State("category-filter", "value"),
        State("year-slider",     "value"),
        State("sales-slider",    "value"),
        State("discount-slider", "value"),
        State("segment-filter",  "value"),
        State("shipmode-filter", "value"),
        prevent_initial_call=True,
    )
    def export_csv(n_clicks, region, country, category, year_range,
                   sales_range, discount_range, segment, shipmode):
        fdf = apply_filters(region, country, category, year_range,
                            sales_range, discount_range, segment, shipmode)
        return dcc.send_data_frame(fdf.to_csv, "superstore_export.csv", index=False)