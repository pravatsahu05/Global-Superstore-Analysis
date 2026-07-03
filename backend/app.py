from dash import Dash
from backend.layout import layout
from backend.callbacks import register_callbacks
from backend.data_service import get_processed_data

app = Dash(
    __name__,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap"
    ]
)

# ── Expose Flask server for gunicorn (required for deployment) ──
server = app.server

app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>Global Superstore BI</title>
    {%favicon%}
    {%css%}
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        html, body {
            background: #080b12 !important;
            color: #e8edf5 !important;
            min-height: 100vh;
            font-family: Syne, Arial, sans-serif;
        }

        /* ── Plotly transparent bg ── */
        .js-plotly-plot .plotly .main-svg { background: transparent !important; }
        .js-plotly-plot .bg { fill: transparent !important; }

        /* ── Scrollbar ── */
        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-track { background: #0d1117; }
        ::-webkit-scrollbar-thumb { background: #1a2236; border-radius: 999px; }
        ::-webkit-scrollbar-thumb:hover { background: #00d2ff; }

        /* ── Pulse animation for live dot ── */
        @keyframes pulse {
            0%, 100% { opacity: 1; box-shadow: 0 0 8px #00d2ff; }
            50%       { opacity: 0.5; box-shadow: 0 0 3px #00d2ff; }
        }

        /* ── Header gradient border fix (borderImage breaks borderRadius) ── */
        /* We use a pseudo-element approach via box-shadow instead */
        .header-bar {
            border-radius: 16px !important;
            border: 1px solid rgba(124,90,243,0.2) !important;
            box-shadow:
                0 8px 40px rgba(0,0,0,0.5),
                inset 0 1px 0 rgba(255,255,255,0.05),
                0 -1px 0 rgba(0,210,255,0.3) inset !important;
        }

        /* ── Download button ── */
        #download-btn:hover {
            background: linear-gradient(135deg, #00d2ff, #7c5af3) !important;
            color: #080b12 !important;
            box-shadow: 0 0 28px rgba(0,210,255,0.25) !important;
            border-color: transparent !important;
        }

        /* ── Toggle buttons hover ── */
        button:hover {
            border-color: rgba(0,210,255,0.6) !important;
            color: #00d2ff !important;
        }

        /* ── Range slider track ── */
        .rc-slider-track { background: #7c5af3 !important; }
        .rc-slider-handle {
            background: #7c5af3 !important;
            border-color: #7c5af3 !important;
            box-shadow: 0 0 6px rgba(124,90,243,0.6) !important;
        }
        .rc-slider-handle:hover, .rc-slider-handle:active {
            border-color: #00d2ff !important;
            background: #00d2ff !important;
            box-shadow: 0 0 10px rgba(0,210,255,0.7) !important;
        }
        .rc-slider-rail { background: rgba(255,255,255,0.08) !important; }
        .rc-slider-dot { border-color: rgba(255,255,255,0.15) !important; background: #0d1424 !important; }
        .rc-slider-dot-active { border-color: #7c5af3 !important; }
        .rc-slider-mark-text { color: #7a8fa8 !important; font-family: Syne, sans-serif !important; }
        .rc-slider-tooltip-inner {
            background: #1a2236 !important;
            font-family: Syne, sans-serif !important;
            font-size: 0.7rem !important;
            color: #e8edf5 !important;
            border: 1px solid rgba(0,210,255,0.2) !important;
        }

        /* ── Dash 2.x Dropdown ── */
        .dash-dropdown { background: transparent !important; }
        .dash-dropdown .Select-control, .Select-control {
            background-color: #1a2236 !important;
            border: 1px solid rgba(255,255,255,0.10) !important;
            border-radius: 10px !important;
            min-height: 38px !important;
            box-shadow: none !important;
        }
        .dash-dropdown .Select.is-open > .Select-control {
            border-color: rgba(0,210,255,0.45) !important;
            border-bottom-left-radius: 0 !important;
            border-bottom-right-radius: 0 !important;
        }
        .dash-dropdown .Select-placeholder, .Select-placeholder {
            color: #7a8fa8 !important;
            font-family: Syne, Arial, sans-serif !important;
            font-size: 0.78rem !important;
        }
        .dash-dropdown .Select-value-label, .Select-value-label {
            color: #e8edf5 !important;
            font-family: Syne, Arial, sans-serif !important;
            font-size: 0.78rem !important;
        }
        .dash-dropdown .Select-input > input,
        .dash-dropdown input,
        .Select-input input {
            background: #1a2236 !important;
            background-color: #1a2236 !important;
            color: #e8edf5 !important;
            caret-color: #00d2ff !important;
            font-family: Syne, Arial, sans-serif !important;
            font-size: 0.78rem !important;
            border: none !important;
            outline: none !important;
        }
        .dash-dropdown .Select-input, .Select-input {
            background: #1a2236 !important;
            background-color: #1a2236 !important;
        }
        .dash-dropdown .Select-menu-outer, .Select-menu-outer {
            background: #131c2e !important;
            background-color: #131c2e !important;
            border: 1px solid rgba(0,210,255,0.25) !important;
            border-top: none !important;
            border-radius: 0 0 10px 10px !important;
            box-shadow: 0 20px 50px rgba(0,0,0,0.8) !important;
            z-index: 99999 !important;
        }
        .dash-dropdown .Select-menu, .Select-menu {
            background: #131c2e !important;
            background-color: #131c2e !important;
        }
        .dash-dropdown .Select-option, .Select-option {
            background: #131c2e !important;
            color: #c2cede !important;
            font-family: Syne, Arial, sans-serif !important;
            font-size: 0.78rem !important;
            padding: 9px 14px !important;
            border-bottom: 1px solid rgba(255,255,255,0.04) !important;
        }
        .dash-dropdown .Select-option.is-focused,
        .Select-option.is-focused,
        .Select-option:hover {
            background: rgba(0,210,255,0.10) !important;
            background-color: rgba(0,210,255,0.10) !important;
            color: #00d2ff !important;
        }
        .dash-dropdown .Select-option.is-selected, .Select-option.is-selected {
            background: rgba(124,90,243,0.20) !important;
            color: #c4b5fd !important;
        }
        .Select-arrow { border-top-color: #4a5f80 !important; }
        .is-open .Select-arrow {
            border-top-color: transparent !important;
            border-bottom-color: #00d2ff !important;
        }
        .Select-clear-zone { color: #3d4f6a !important; }
        .Select-clear-zone:hover { color: #ff4f7b !important; }
        .Select-noresults {
            background: #131c2e !important;
            color: #3d4f6a !important;
            font-family: Syne, Arial, sans-serif !important;
        }

        /* ── Selected value tags (multi-select pills) ── */
        .Select-value {
            background: rgba(124,90,243,0.18) !important;
            border: 1px solid rgba(124,90,243,0.55) !important;
            border-radius: 6px !important;
            margin: 3px 3px !important;
            padding: 1px 2px !important;
        }
        .Select-value-label {
            color: #c4b5fd !important;
            font-family: Syne, Arial, sans-serif !important;
            font-size: 0.75rem !important;
            font-weight: 600 !important;
            padding: 2px 4px !important;
        }
        .Select-value-icon {
            color: #7c5af3 !important;
            border-right: 1px solid rgba(124,90,243,0.4) !important;
            padding: 2px 6px !important;
            font-size: 0.85rem !important;
        }
        .Select-value-icon:hover {
            background: rgba(255,79,123,0.15) !important;
            color: #ff4f7b !important;
            border-radius: 5px 0 0 5px !important;
        }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
    <script>
    (function() {
        function styleDropdownInputs() {
            document.querySelectorAll('.dash-dropdown input, .Select-input input').forEach(function(el) {
                el.style.setProperty('background', '#1a2236', 'important');
                el.style.setProperty('background-color', '#1a2236', 'important');
                el.style.setProperty('color', '#e8edf5', 'important');
                el.style.setProperty('caret-color', '#00d2ff', 'important');
                el.style.setProperty('font-family', 'Syne, Arial, sans-serif', 'important');
                el.style.setProperty('font-size', '0.78rem', 'important');
                el.style.setProperty('border', 'none', 'important');
                el.style.setProperty('outline', 'none', 'important');
            });
            document.querySelectorAll('.Select-input, .dash-dropdown .Select-input').forEach(function(el) {
                el.style.setProperty('background', '#1a2236', 'important');
                el.style.setProperty('background-color', '#1a2236', 'important');
            });
            document.querySelectorAll('.Select-option, .dash-dropdown .Select-option').forEach(function(el) {
                if (!el.dataset.styled) {
                    el.style.setProperty('background', '#131c2e', 'important');
                    el.style.setProperty('color', '#c2cede', 'important');
                    el.dataset.styled = '1';
                    el.addEventListener('mouseenter', function() {
                        el.style.setProperty('background', 'rgba(0,210,255,0.10)', 'important');
                        el.style.setProperty('color', '#00d2ff', 'important');
                    });
                    el.addEventListener('mouseleave', function() {
                        el.style.setProperty('background', '#131c2e', 'important');
                        el.style.setProperty('color', '#c2cede', 'important');
                    });
                }
            });
            document.querySelectorAll('.Select-menu-outer').forEach(function(el) {
                el.style.setProperty('background', '#131c2e', 'important');
                el.style.setProperty('border', '1px solid rgba(0,210,255,0.25)', 'important');
            });
        }
        document.addEventListener('DOMContentLoaded', styleDropdownInputs);
        var observer = new MutationObserver(function(mutations) {
            if (mutations.some(function(m) { return m.addedNodes.length > 0; }))
                styleDropdownInputs();
        });
        observer.observe(document.body, { childList: true, subtree: true });
    })();
    </script>
</body>
</html>
'''

df = get_processed_data()
app.layout = layout
register_callbacks(app, df)

if __name__ == "__main__":
    app.run(debug=True)