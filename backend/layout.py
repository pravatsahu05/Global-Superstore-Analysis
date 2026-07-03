from dash import html, dcc

# ── Design tokens ─────────────────────────────────────────────
BG_VOID    = "#080b12"
BG_SIDEBAR = "#0d1424"
BG_CARD    = "#111827"
BG_PANEL   = "#0f1829"
BORDER     = "rgba(255,255,255,0.07)"
FONT       = "Syne, Arial, sans-serif"
TEXT       = "#e8edf5"
MUTED      = "#7a8fa8"

CYAN    = "#00d2ff"
VIOLET  = "#7c5af3"
EMERALD = "#00e5a0"
AMBER   = "#ffb347"
PINK    = "#ff4f7b"
BLUE    = "#38bdf8"

# ── Helpers ───────────────────────────────────────────────────
def _label(text):
    return html.Div(text, style={
        "color": "#8faabf",          # brighter than MUTED for readability
        "fontSize": "0.62rem",
        "fontWeight": "700",
        "letterSpacing": "0.12em",
        "textTransform": "uppercase",
        "marginBottom": "5px",
        "marginTop": "14px",
    })

def _section_dot(color, label):
    return html.Div([
        html.Span(style={
            "display": "inline-block",
            "width": "8px", "height": "8px",
            "borderRadius": "50%",
            "background": color,
            "marginRight": "8px",
            "boxShadow": f"0 0 6px {color}",
        }),
        html.Span(label, style={
            "fontSize": "0.65rem",
            "fontWeight": "700",
            "letterSpacing": "0.12em",
            "textTransform": "uppercase",
            "color": MUTED,
        }),
    ], style={"display": "flex", "alignItems": "center",
              "marginBottom": "8px", "marginTop": "4px"})

def _toggle_btn(label, btn_id, active=False):
    return html.Button(label, id=btn_id, n_clicks=0, style={
        "padding": "4px 12px",
        "fontSize": "0.62rem",
        "fontWeight": "700",
        "letterSpacing": "0.1em",
        "border": f"1px solid {CYAN if active else 'rgba(255,255,255,0.12)'}",
        "borderRadius": "999px",
        "background": "rgba(0,210,255,0.15)" if active else "transparent",
        "color": CYAN if active else MUTED,
        "cursor": "pointer",
        "fontFamily": FONT,
        "transition": "all 0.15s",
    })

def _chart_panel(dot_color, section_label, toggles, graph_id, full_width=False):
    return html.Div([
        html.Div([
            _section_dot(dot_color, section_label),
            html.Div(toggles, style={"display": "flex", "gap": "6px"}),
        ], style={
            "display": "flex", "alignItems": "center",
            "justifyContent": "space-between",
            "padding": "12px 14px 4px",
        }),
        dcc.Loading(
            dcc.Graph(id=graph_id, config={"displayModeBar": False}),
            color=CYAN,
        ),
    ], style={
        "background": BG_CARD,
        "border": f"1px solid {BORDER}",
        "borderRadius": "16px",
        "boxShadow": "0 4px 28px rgba(0,0,0,0.55)",
        "flex": "1" if not full_width else None,
        "width": "100%" if full_width else None,
        "minWidth": "0",
    })

# ── Layout ────────────────────────────────────────────────────
layout = html.Div([

    # ═══════════════════════════════
    # SIDEBAR
    # ═══════════════════════════════
    html.Div([

        # ── LOGO BLOCK ──────────────────────────
        html.Div([

            # Icon with layered glow rings
            html.Div([
                html.Div("📦", style={
                    "fontSize": "1.7rem", "lineHeight": "1",
                    "filter": "drop-shadow(0 0 8px rgba(0,210,255,0.5))",
                }),
            ], style={
                "background": "linear-gradient(135deg, #1a1040 0%, #0d1a30 100%)",
                "border": "1px solid rgba(124,90,243,0.5)",
                "borderRadius": "14px",
                "width": "52px", "height": "52px",
                "display": "flex", "alignItems": "center", "justifyContent": "center",
                "flexShrink": "0",
                "boxShadow": "0 0 0 3px rgba(124,90,243,0.1), 0 0 20px rgba(124,90,243,0.2)",
            }),

            # Text
            html.Div([
                html.Div([
                    html.Span("Global ", style={"color": TEXT}),
                    html.Span("Superstore", style={
                        "background": "linear-gradient(90deg, #00d2ff, #7c5af3)",
                        "WebkitBackgroundClip": "text",
                        "WebkitTextFillColor": "transparent",
                        "backgroundClip": "text",
                    }),
                ], style={
                    "fontSize": "1rem", "fontWeight": "800",
                    "letterSpacing": "0.01em", "lineHeight": "1.2",
                    "fontFamily": FONT,
                }),
                # Animated tag line
                html.Div([
                    html.Span(style={
                        "display": "inline-block",
                        "width": "5px", "height": "5px",
                        "borderRadius": "50%",
                        "background": EMERALD,
                        "marginRight": "5px",
                        "verticalAlign": "middle",
                        "boxShadow": f"0 0 6px {EMERALD}",
                    }),
                    html.Span("BI INTELLIGENCE", style={
                        "color": "#5ab4cc",
                        "fontSize": "0.52rem",
                        "letterSpacing": "0.2em",
                        "textTransform": "uppercase",
                        "verticalAlign": "middle",
                    }),
                ], style={"marginTop": "4px"}),
            ]),

        ], style={
            "display": "flex", "alignItems": "center", "gap": "12px",
            "marginBottom": "0",
            "padding": "16px 14px",
            "background": "linear-gradient(135deg, rgba(124,90,243,0.08) 0%, rgba(0,210,255,0.04) 100%)",
            "borderRadius": "14px",
            "border": "1px solid rgba(124,90,243,0.2)",
            "boxShadow": "inset 0 1px 0 rgba(255,255,255,0.04)",
        }),

        # Thin divider with gradient
        html.Div(style={
            "height": "1px",
            "background": "linear-gradient(90deg, rgba(124,90,243,0.6), rgba(0,210,255,0.4), rgba(0,0,0,0))",
            "margin": "14px 0",
        }),

        # ── FILTERS HEADER ──────────────────────
        html.Div([
            # Left: icon + label
            html.Div([
                html.Div("⚙", style={
                    "fontSize": "0.8rem",
                    "background": "rgba(0,210,255,0.12)",
                    "border": "1px solid rgba(0,210,255,0.25)",
                    "borderRadius": "6px",
                    "width": "24px", "height": "24px",
                    "display": "flex", "alignItems": "center",
                    "justifyContent": "center",
                    "marginRight": "8px",
                }),
                html.Span("Filters", style={
                    "fontSize": "0.7rem", "fontWeight": "800",
                    "letterSpacing": "0.14em", "textTransform": "uppercase",
                    "color": TEXT,
                }),
            ], style={"display": "flex", "alignItems": "center"}),

            # Right: glowing dot indicator
            html.Div([
                html.Span(style={
                    "display": "inline-block",
                    "width": "7px", "height": "7px",
                    "borderRadius": "50%",
                    "background": CYAN,
                    "boxShadow": f"0 0 8px {CYAN}",
                    "marginRight": "5px",
                }),
                html.Span("Active", style={
                    "fontSize": "0.55rem", "color": CYAN,
                    "fontWeight": "700", "letterSpacing": "0.1em",
                    "textTransform": "uppercase",
                }),
            ], style={"display": "flex", "alignItems": "center"}),

        ], style={
            "display": "flex", "alignItems": "center",
            "justifyContent": "space-between",
            "background": "linear-gradient(135deg, rgba(0,210,255,0.06), rgba(124,90,243,0.06))",
            "border": "1px solid rgba(0,210,255,0.18)",
            "borderLeft": f"3px solid {CYAN}",
            "borderRadius": "10px",
            "padding": "9px 12px",
            "marginBottom": "14px",
            "boxShadow": f"0 0 12px rgba(0,210,255,0.06)",
        }),

        # ── DROPDOWN SECTION ────────────────────
        html.Div([

            # Region
            html.Div([
                html.Div([
                    html.Span(style={
                        "width": "3px", "height": "14px",
                        "background": CYAN,
                        "borderRadius": "2px",
                        "display": "inline-block",
                        "marginRight": "8px",
                        "boxShadow": f"0 0 6px {CYAN}",
                    }),
                    html.Span("Region", style={
                        "color": "#c2d4e8", "fontSize": "0.65rem",
                        "fontWeight": "700", "letterSpacing": "0.1em",
                        "textTransform": "uppercase",
                    }),
                ], style={"display": "flex", "alignItems": "center", "marginBottom": "5px"}),
                dcc.Dropdown(id="region-filter", placeholder="All Regions", multi=True),
            ], style={"marginBottom": "12px"}),

            # Country
            html.Div([
                html.Div([
                    html.Span(style={
                        "width": "3px", "height": "14px",
                        "background": VIOLET,
                        "borderRadius": "2px",
                        "display": "inline-block",
                        "marginRight": "8px",
                        "boxShadow": f"0 0 6px {VIOLET}",
                    }),
                    html.Span("Country", style={
                        "color": "#c2d4e8", "fontSize": "0.65rem",
                        "fontWeight": "700", "letterSpacing": "0.1em",
                        "textTransform": "uppercase",
                    }),
                ], style={"display": "flex", "alignItems": "center", "marginBottom": "5px"}),
                dcc.Dropdown(id="country-filter", placeholder="All Countries", multi=True),
            ], style={"marginBottom": "12px"}),

            # Category
            html.Div([
                html.Div([
                    html.Span(style={
                        "width": "3px", "height": "14px",
                        "background": EMERALD,
                        "borderRadius": "2px",
                        "display": "inline-block",
                        "marginRight": "8px",
                        "boxShadow": f"0 0 6px {EMERALD}",
                    }),
                    html.Span("Category", style={
                        "color": "#c2d4e8", "fontSize": "0.65rem",
                        "fontWeight": "700", "letterSpacing": "0.1em",
                        "textTransform": "uppercase",
                    }),
                ], style={"display": "flex", "alignItems": "center", "marginBottom": "5px"}),
                dcc.Dropdown(id="category-filter", placeholder="All Categories", multi=True),
            ], style={"marginBottom": "12px"}),

            # Segment
            html.Div([
                html.Div([
                    html.Span(style={
                        "width": "3px", "height": "14px",
                        "background": AMBER,
                        "borderRadius": "2px",
                        "display": "inline-block",
                        "marginRight": "8px",
                        "boxShadow": f"0 0 6px {AMBER}",
                    }),
                    html.Span("Segment", style={
                        "color": "#c2d4e8", "fontSize": "0.65rem",
                        "fontWeight": "700", "letterSpacing": "0.1em",
                        "textTransform": "uppercase",
                    }),
                ], style={"display": "flex", "alignItems": "center", "marginBottom": "5px"}),
                dcc.Dropdown(
                    id="segment-filter", placeholder="All Segments", multi=True,
                    options=[
                        {"label": "Consumer",    "value": "Consumer"},
                        {"label": "Corporate",   "value": "Corporate"},
                        {"label": "Home Office", "value": "Home Office"},
                    ],
                ),
            ], style={"marginBottom": "12px"}),

            # Ship Mode
            html.Div([
                html.Div([
                    html.Span(style={
                        "width": "3px", "height": "14px",
                        "background": PINK,
                        "borderRadius": "2px",
                        "display": "inline-block",
                        "marginRight": "8px",
                        "boxShadow": f"0 0 6px {PINK}",
                    }),
                    html.Span("Ship Mode", style={
                        "color": "#c2d4e8", "fontSize": "0.65rem",
                        "fontWeight": "700", "letterSpacing": "0.1em",
                        "textTransform": "uppercase",
                    }),
                ], style={"display": "flex", "alignItems": "center", "marginBottom": "5px"}),
                dcc.Dropdown(
                    id="shipmode-filter", placeholder="All Ship Modes", multi=True,
                    options=[
                        {"label": "Standard Class", "value": "Standard Class"},
                        {"label": "Second Class",   "value": "Second Class"},
                        {"label": "First Class",    "value": "First Class"},
                        {"label": "Same Day",       "value": "Same Day"},
                    ],
                ),
            ], style={"marginBottom": "4px"}),

        ], style={
            "background": "rgba(255,255,255,0.02)",
            "border": "1px solid rgba(255,255,255,0.05)",
            "borderRadius": "12px",
            "padding": "12px 10px",
            "marginBottom": "14px",
        }),

        # ── RANGE SLIDERS SECTION ────────────────
        html.Div([

            html.Div("Range Filters", style={
                "color": "#c2d4e8", "fontSize": "0.6rem", "fontWeight": "800",
                "letterSpacing": "0.12em", "textTransform": "uppercase",
                "marginBottom": "14px",
                "display": "flex", "alignItems": "center", "gap": "6px",
            }),

            # Year slider
            html.Div([
                html.Div([
                    html.Span("📅", style={"fontSize": "0.75rem"}),
                    html.Span("Year Range", style={
                        "color": "#c2d4e8", "fontSize": "0.62rem",
                        "fontWeight": "700", "letterSpacing": "0.08em",
                        "marginLeft": "6px",
                    }),
                ], style={"display": "flex", "alignItems": "center", "marginBottom": "10px"}),
                dcc.RangeSlider(
                    id="year-slider",
                    min=2011, max=2014, step=1,
                    value=[2011, 2014],
                    marks={y: {"label": str(y),
                               "style": {"color": "#7a8fa8", "fontSize": "0.6rem"}}
                           for y in [2011, 2012, 2013, 2014]},
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
            ], style={
                "background": "rgba(0,210,255,0.04)",
                "border": "1px solid rgba(0,210,255,0.12)",
                "borderRadius": "10px",
                "padding": "10px 10px 14px",
                "marginBottom": "10px",
            }),

            # Sales slider
            html.Div([
                html.Div([
                    html.Span("💰", style={"fontSize": "0.75rem"}),
                    html.Span("Sales ($)", style={
                        "color": "#c2d4e8", "fontSize": "0.62rem",
                        "fontWeight": "700", "letterSpacing": "0.08em",
                        "marginLeft": "6px",
                    }),
                ], style={"display": "flex", "alignItems": "center", "marginBottom": "10px"}),
                dcc.RangeSlider(
                    id="sales-slider",
                    min=0, max=22638, step=500,
                    value=[0, 22638],
                    marks={
                        0:     {"label": "$0",   "style": {"color": "#7a8fa8", "fontSize": "0.6rem"}},
                        22638: {"label": "$22K", "style": {"color": "#7a8fa8", "fontSize": "0.6rem"}},
                    },
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
            ], style={
                "background": "rgba(124,90,243,0.04)",
                "border": "1px solid rgba(124,90,243,0.12)",
                "borderRadius": "10px",
                "padding": "10px 10px 14px",
                "marginBottom": "10px",
            }),

            # Discount slider
            html.Div([
                html.Div([
                    html.Span("🏷️", style={"fontSize": "0.75rem"}),
                    html.Span("Discount", style={
                        "color": "#c2d4e8", "fontSize": "0.62rem",
                        "fontWeight": "700", "letterSpacing": "0.08em",
                        "marginLeft": "6px",
                    }),
                ], style={"display": "flex", "alignItems": "center", "marginBottom": "10px"}),
                dcc.RangeSlider(
                    id="discount-slider",
                    min=0, max=0.85, step=0.05,
                    value=[0, 0.85],
                    marks={
                        0:    {"label": "0%",  "style": {"color": "#7a8fa8", "fontSize": "0.6rem"}},
                        0.85: {"label": "85%", "style": {"color": "#7a8fa8", "fontSize": "0.6rem"}},
                    },
                    tooltip={"placement": "bottom", "always_visible": False},
                ),
            ], style={
                "background": "rgba(255,183,71,0.04)",
                "border": "1px solid rgba(255,183,71,0.12)",
                "borderRadius": "10px",
                "padding": "10px 10px 14px",
            }),

        ], style={
            "background": "rgba(255,255,255,0.02)",
            "border": "1px solid rgba(255,255,255,0.05)",
            "borderRadius": "12px",
            "padding": "12px 10px",
            "marginBottom": "14px",
        }),

        # Hidden year dropdown kept for callback compat
        dcc.Dropdown(id="year-filter", multi=True,
                     style={"display": "none"}),

        # ── EXPORT BUTTON ────────────────────────
        html.Button([
            html.Span("⬇", style={"marginRight": "6px"}),
            html.Span("Export CSV"),
        ], id="download-btn", style={
            "width": "100%", "padding": "11px",
            "background": "linear-gradient(135deg, rgba(0,210,255,0.1), rgba(124,90,243,0.1))",
            "color": CYAN,
            "border": "1px solid rgba(0,210,255,0.3)",
            "borderRadius": "10px", "fontFamily": FONT,
            "fontSize": "0.72rem", "fontWeight": "700",
            "letterSpacing": "0.08em", "cursor": "pointer",
            "display": "flex", "alignItems": "center", "justifyContent": "center",
        }),
        dcc.Download(id="download-data"),

        html.Div(id="record-count", style={
            "color": "#5a7080", "fontSize": "0.56rem",
            "textAlign": "center", "marginTop": "10px",
            "letterSpacing": "0.08em",
        }),

    ], style={
        "position": "fixed", "top": "0", "left": "0",
        "width": "260px", "height": "100vh",
        "background": "linear-gradient(180deg, #0d1424 0%, #0a0f1e 100%)",
        "padding": "18px 14px",
        "overflowY": "auto",
        "borderRight": "1px solid rgba(124,90,243,0.15)",
        "zIndex": "100",
    }),

    # ═══════════════════════════════
    # MAIN CONTENT
    # ═══════════════════════════════
    html.Div([

        # ── HEADER BAR ──────────────────────────────
        html.Div([

            # Left — title block
            html.Div([

                # Eyebrow line with animated dot
                html.Div([
                    html.Span(style={
                        "display": "inline-block",
                        "width": "6px", "height": "6px",
                        "borderRadius": "50%",
                        "background": CYAN,
                        "marginRight": "7px",
                        "boxShadow": f"0 0 8px {CYAN}",
                        "animation": "pulse 2s ease-in-out infinite",
                    }),
                    html.Span("Global Superstore  ·  Business Intelligence", style={
                        "fontSize": "0.58rem", "fontWeight": "700",
                        "letterSpacing": "0.16em", "textTransform": "uppercase",
                        "color": CYAN,
                    }),
                ], style={"display": "flex", "alignItems": "center", "marginBottom": "6px"}),

                # Main title with gradient text via inline style trick
                html.Div([
                    html.Span("Global Superstore ", style={
                        "color": TEXT,
                        "fontSize": "1.45rem", "fontWeight": "800",
                        "letterSpacing": "0.01em",
                        "fontFamily": FONT,
                    }),
                    html.Span("Dashboard", style={
                        "fontSize": "1.45rem", "fontWeight": "800",
                        "letterSpacing": "0.01em",
                        "fontFamily": FONT,
                        "background": "linear-gradient(90deg, #00d2ff, #7c5af3)",
                        "WebkitBackgroundClip": "text",
                        "WebkitTextFillColor": "transparent",
                        "backgroundClip": "text",
                    }),
                ], style={"display": "flex", "alignItems": "baseline", "gap": "0px"}),

                # Subtitle
                html.Div("Interactive Analytics Platform  ·  51,290 Records", style={
                    "fontSize": "0.6rem", "color": "#5a7a94",
                    "letterSpacing": "0.1em", "textTransform": "uppercase",
                    "marginTop": "4px",
                }),

            ]),

            # Right — badges
            html.Div([

                # Filter badge
                html.Div(id="filter-badge", style={
                    "background": "rgba(124,90,243,0.12)",
                    "border": "1px solid rgba(124,90,243,0.35)",
                    "color": "#b39dfc",
                    "fontSize": "0.6rem", "fontWeight": "700",
                    "letterSpacing": "0.1em", "textTransform": "uppercase",
                    "padding": "6px 14px",
                    "borderRadius": "999px",
                    "marginRight": "8px",
                }),

                # Live data badge
                html.Div([
                    html.Span(style={
                        "display": "inline-block",
                        "width": "7px", "height": "7px",
                        "borderRadius": "50%",
                        "background": EMERALD,
                        "marginRight": "7px",
                        "boxShadow": f"0 0 10px {EMERALD}",
                    }),
                    html.Span("Live Data", style={
                        "fontSize": "0.6rem", "fontWeight": "700",
                        "letterSpacing": "0.1em", "color": EMERALD,
                        "textTransform": "uppercase",
                    }),
                ], style={
                    "display": "flex", "alignItems": "center",
                    "background": "rgba(0,229,160,0.08)",
                    "border": "1px solid rgba(0,229,160,0.3)",
                    "padding": "6px 14px",
                    "borderRadius": "999px",
                }),

            ], style={"display": "flex", "alignItems": "center", "flexShrink": "0"}),

        ], style={
            "display": "flex", "alignItems": "center",
            "justifyContent": "space-between",
            "background": "linear-gradient(135deg, #0d1a2e 0%, #0f1829 60%, #130d2a 100%)",
            "border": "1px solid rgba(124,90,243,0.2)",
            "borderTop": "2px solid transparent",
            "borderImage": "linear-gradient(90deg, #00d2ff, #7c5af3, #00e5a0) 1",
            "borderRadius": "16px",
            "padding": "18px 24px",
            "marginBottom": "16px",
            "boxShadow": "0 8px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(124,90,243,0.1), inset 0 1px 0 rgba(255,255,255,0.04)",
            "position": "relative",
            "overflow": "hidden",
        }),

        # ── KPI CARDS ────────────────────────────────
        html.Div([
            html.Div(id="kpi-sales",    style={"flex": "1", "minWidth": "0"}),
            html.Div(id="kpi-profit",   style={"flex": "1", "minWidth": "0"}),
            html.Div(id="kpi-orders",   style={"flex": "1", "minWidth": "0"}),
            html.Div(id="kpi-margin",   style={"flex": "1", "minWidth": "0"}),
            html.Div(id="kpi-shipping", style={"flex": "1", "minWidth": "0"}),
        ], style={
            "display": "flex", "gap": "12px",
            "marginBottom": "16px",
        }),

        # ── ROW 1 ─────────────────────────────────────
        html.Div([
            _chart_panel(CYAN, "Sales Trend",
                [_toggle_btn("LINE", "trend-line-btn", True),
                 _toggle_btn("BAR",  "trend-bar-btn")],
                "sales-trend"),
            _chart_panel(VIOLET, "Profit by Category",
                [_toggle_btn("BAR",  "cat-bar-btn", True),
                 _toggle_btn("PIE",  "cat-pie-btn"),
                 _toggle_btn("LINE", "cat-line-btn")],
                "profit-category"),
        ], style={"display": "flex", "gap": "14px", "marginBottom": "14px"}),

        # ── ROW 2 ─────────────────────────────────────
        html.Div([
            _chart_panel(EMERALD, "Top Products by Sales",
                [_toggle_btn("BAR",  "prod-bar-btn", True),
                 _toggle_btn("LINE", "prod-line-btn")],
                "top-products"),
            _chart_panel(PINK, "Discount vs Profit",
                [_toggle_btn("SCATTER", "disc-scatter-btn", True),
                 _toggle_btn("BAR",     "disc-bar-btn")],
                "discount-profit"),
        ], style={"display": "flex", "gap": "14px", "marginBottom": "14px"}),

        # ── ROW 3 ─────────────────────────────────────
        html.Div([
            _chart_panel(AMBER, "Profit Heatmap",
                [_toggle_btn("HEATMAP", "heat-heatmap-btn", True),
                 _toggle_btn("BAR",     "heat-bar-btn")],
                "profit-heatmap"),
            _chart_panel(BLUE, "Product Demand",
                [_toggle_btn("BAR",  "dem-bar-btn", True),
                 _toggle_btn("LINE", "dem-line-btn")],
                "product-demand"),
        ], style={"display": "flex", "gap": "14px", "marginBottom": "14px"}),

        # ── ROW 4 ─────────────────────────────────────
        html.Div([
            _chart_panel(VIOLET, "Customer Segmentation",
                [_toggle_btn("SCATTER", "seg-scatter-btn", True),
                 _toggle_btn("BAR",     "seg-bar-btn")],
                "customer-segmentation"),
            _chart_panel(EMERALD, "Sales Forecast (ML)",
                [_toggle_btn("LINE", "fore-line-btn", True),
                 _toggle_btn("BAR",  "fore-bar-btn")],
                "sales-forecast"),
        ], style={"display": "flex", "gap": "14px", "marginBottom": "14px"}),

        # ── ROW 5: Full-width geo map ──────────────────
        _chart_panel(PINK, "Global Sales Distribution",
            [_toggle_btn("MAP", "geo-map-btn", True),
             _toggle_btn("BAR", "geo-bar-btn")],
            "geo-sales",
            full_width=True),

        html.Div(style={"height": "30px"}),

    ], style={
        "marginLeft": "268px",
        "padding": "16px 18px",
        "background": BG_VOID,
        "minHeight": "100vh",
    }),

])