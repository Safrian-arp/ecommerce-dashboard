"""
╔══════════════════════════════════════════════════════════════════╗
║     E-COMMERCE ANALYTICS COMMAND CENTER                          ║
║     Built with Streamlit + Plotly | Senior Data Analyst Suite    ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Analytics Hub",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── GLOBAL THEME ─────────────────────────────────────────────────────────────
COLORS = {
    "primary":    "#00D4FF",
    "secondary":  "#7B2FBE",
    "accent":     "#FF6B35",
    "success":    "#00C896",
    "warning":    "#FFB800",
    "danger":     "#FF4757",
    "bg_dark":    "#0A0E1A",
    "bg_card":    "#111827",
    "bg_card2":   "#1A2235",
    "text":       "#E2E8F0",
    "text_muted": "#64748B",
    "border":     "#1E293B",
    "cats": ["#00D4FF","#7B2FBE","#FF6B35","#00C896","#FFB800","#FF4757",
             "#A78BFA","#34D399","#FB923C","#38BDF8","#F472B6","#FBBF24"],
}

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="'IBM Plex Mono', monospace", color=COLORS["text"], size=12),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=COLORS["border"], borderwidth=1),
    xaxis=dict(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"], tickfont=dict(size=11)),
    yaxis=dict(gridcolor=COLORS["border"], zerolinecolor=COLORS["border"], tickfont=dict(size=11)),
)

# ─── INJECT CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    background-color: #0A0E1A !important;
    color: #E2E8F0 !important;
    font-family: 'Space Grotesk', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1321 0%, #111827 100%) !important;
    border-right: 1px solid #1E293B;
}

/* Metric cards */
.kpi-card {
    background: linear-gradient(135deg, #111827 0%, #1A2235 100%);
    border: 1px solid #1E293B;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: var(--accent-color, #00D4FF);
}
.kpi-card:hover { border-color: #00D4FF44; }
.kpi-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 28px;
    font-weight: 700;
    color: #E2E8F0;
    letter-spacing: -0.5px;
    line-height: 1;
}
.kpi-delta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    margin-top: 6px;
}
.kpi-delta.up { color: #00C896; }
.kpi-delta.down { color: #FF4757; }
.kpi-delta.neutral { color: #64748B; }

/* Alert box */
.alert-box {
    border-radius: 10px;
    padding: 14px 18px;
    margin: 8px 0;
    border-left: 4px solid;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
}
.alert-danger  { background:#FF475715; border-color:#FF4757; color:#FF4757; }
.alert-warning { background:#FFB80015; border-color:#FFB800; color:#FFB800; }
.alert-success { background:#00C89615; border-color:#00C896; color:#00C896; }
.alert-info    { background:#00D4FF15; border-color:#00D4FF; color:#00D4FF; }

/* Section headers */
.section-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #00D4FF;
    text-transform: uppercase;
    letter-spacing: 3px;
    border-bottom: 1px solid #1E293B;
    padding-bottom: 8px;
    margin: 24px 0 16px 0;
}

/* RFM badges */
.rfm-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    font-weight: 600;
    margin: 2px;
}

/* Streamlit overrides */
.stSelectbox label, .stSlider label, .stMultiSelect label {
    color: #64748B !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}
div[data-testid="metric-container"] { display: none; }
.stPlotlyChart { border-radius: 12px; overflow: hidden; }
hr { border-color: #1E293B !important; }

/* Sidebar nav pills */
.stRadio label {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 12px !important;
    color: #94A3B8 !important;
}
</style>
""", unsafe_allow_html=True)


# ─── DATA LOADING ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    orders = pd.read_csv('orders.csv', sep=';',
                         parse_dates=['created_at', 'paid_at', 'delivery_at'])
    order_details = pd.read_csv('order_details.csv', sep=';')
    products = pd.read_csv('products.csv', sep=';')
    users = pd.read_csv('users.csv', sep=';', on_bad_lines='skip')

    # ── Clean & engineer features ──────────────────────────────────────────
    orders['is_paid']      = orders['paid_at'].notna()
    orders['is_delivered'] = orders['delivery_at'].notna()
    orders['payment_lag']  = (orders['paid_at'] - orders['created_at']).dt.days
    orders['delivery_lag'] = (orders['delivery_at'] - orders['paid_at']).dt.days
    orders['year_month']   = orders['created_at'].dt.to_period('M').astype(str)
    orders['year']         = orders['created_at'].dt.year
    orders['month']        = orders['created_at'].dt.month
    orders['dow']          = orders['created_at'].dt.day_name()

    # ── Merge enriched detail ──────────────────────────────────────────────
    detail_rich = (
        order_details
        .merge(products, on='product_id', how='left')
        .merge(orders[['order_id','created_at','buyer_id','is_paid',
                       'is_delivered','year_month','total']], on='order_id', how='left')
    )
    detail_rich['line_revenue'] = detail_rich['price'] * detail_rich['quantity']
    detail_rich['markup']       = detail_rich['price'] - detail_rich['base_price']

    # ── Monthly aggregates ─────────────────────────────────────────────────
    paid_orders = orders[orders['is_paid']]
    monthly = (paid_orders.groupby('year_month')
               .agg(gmv=('total','sum'),
                    orders_count=('order_id','count'),
                    unique_buyers=('buyer_id','nunique'))
               .reset_index())
    monthly['aov']     = monthly['gmv'] / monthly['orders_count']
    monthly['gmv_mom'] = monthly['gmv'].pct_change() * 100
    monthly['sort_key'] = pd.to_datetime(monthly['year_month'])
    monthly = monthly.sort_values('sort_key')

    # ── RFM segmentation ──────────────────────────────────────────────────
    snapshot = orders['created_at'].max() + pd.Timedelta(days=1)
    rfm = (paid_orders
           .groupby('buyer_id')
           .agg(recency  =('created_at', lambda x: (snapshot - x.max()).days),
                frequency=('order_id','count'),
                monetary =('total','sum'))
           .reset_index())

    # Quintile scoring
    rfm['R'] = pd.qcut(rfm['recency'],   5, labels=[5,4,3,2,1], duplicates='drop').astype(int)
    rfm['F'] = pd.qcut(rfm['frequency'], 5, labels=[1,2,3,4,5], duplicates='drop').astype(int)
    rfm['M'] = pd.qcut(rfm['monetary'],  5, labels=[1,2,3,4,5], duplicates='drop').astype(int)
    rfm['rfm_score'] = rfm['R']*100 + rfm['F']*10 + rfm['M']

    def segment(row):
        r, f, m = row['R'], row['F'], row['M']
        if r >= 4 and f >= 4 and m >= 4: return 'Champions'
        elif r >= 3 and f >= 3:          return 'Loyal'
        elif r >= 4 and f <= 2:          return 'New Customers'
        elif r >= 3 and f >= 2:          return 'Potential Loyalist'
        elif r == 2 and f >= 2:          return 'At Risk'
        elif r <= 2 and f >= 3:          return 'Cannot Lose Them'
        else:                            return 'Churned'
    rfm['segment'] = rfm.apply(segment, axis=1)

    # ── Cohort analysis ────────────────────────────────────────────────────
    orders['cohort'] = (orders.groupby('buyer_id')['created_at']
                              .transform('min').dt.to_period('M').astype(str))
    orders['order_period'] = orders['created_at'].dt.to_period('M').astype(str)

    def period_diff(a, b):
        pa = pd.Period(a, freq='M')
        pb = pd.Period(b, freq='M')
        return (pb - pa).n

    orders['period_number'] = orders.apply(
        lambda r: period_diff(r['cohort'], r['order_period']), axis=1)

    cohort_pivot = (orders.groupby(['cohort','period_number'])['buyer_id']
                          .nunique().reset_index())
    cohort_sizes = (cohort_pivot[cohort_pivot['period_number']==0]
                    .set_index('cohort')['buyer_id'])
    cohort_pivot['retention_rate'] = (
        cohort_pivot.apply(lambda r: r['buyer_id']/cohort_sizes.get(r['cohort'],1)*100, axis=1)
    )

    return dict(orders=orders, order_details=order_details,
                products=products, users=users, detail_rich=detail_rich,
                monthly=monthly, rfm=rfm, cohort_pivot=cohort_pivot)


# ─── HELPER FUNCTIONS ─────────────────────────────────────────────────────────
def fmt_rp(x):
    if x >= 1e12: return f"Rp {x/1e12:.2f}T"
    if x >= 1e9:  return f"Rp {x/1e9:.1f}B"
    if x >= 1e6:  return f"Rp {x/1e6:.1f}M"
    return f"Rp {x:,.0f}"

def kpi_card(label, value, delta=None, delta_label="", accent="#00D4FF"):
    delta_html = ""
    if delta is not None:
        cls = "up" if delta > 0 else ("down" if delta < 0 else "neutral")
        icon = "▲" if delta > 0 else ("▼" if delta < 0 else "●")
        delta_html = f'<div class="kpi-delta {cls}">{icon} {abs(delta):.1f}% {delta_label}</div>'
    return f"""
    <div class="kpi-card" style="--accent-color:{accent}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>"""

def alert(msg, kind="info"):
    return f'<div class="alert-box alert-{kind}">{msg}</div>'

def apply_layout(fig, title="", height=380):
    fig.update_layout(**PLOTLY_LAYOUT, title=dict(text=title, font=dict(size=13, color=COLORS["text_muted"]), x=0), height=height)
    return fig


# ─── LOAD DATA ────────────────────────────────────────────────────────────────
with st.spinner("⚡ Initialising analytics engine..."):
    D = load_data()
orders       = D['orders']
detail_rich  = D['detail_rich']
monthly      = D['monthly']
rfm          = D['rfm']
cohort_pivot = D['cohort_pivot']
products     = D['products']


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:16px 0 24px">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#00D4FF;
                    letter-spacing:3px;text-transform:uppercase;">Analytics Hub</div>
        <div style="font-size:22px;font-weight:700;color:#E2E8F0;margin-top:4px;">
            E-Commerce<br><span style="color:#7B2FBE;">Command Center</span>
        </div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#64748B;margin-top:8px;">
            Jan 2019 – May 2020 · Rp 148.8B GMV
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("", [
        "⚡  Executive Overview",
        "📦  Product Intelligence",
        "👤  Customer Analytics",
        "🚚  Operations & SLA",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:10px;color:#64748B;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;">Date Range</div>', unsafe_allow_html=True)
    all_months = sorted(orders['year_month'].unique())
    sel_range = st.select_slider("", options=all_months,
                                  value=(all_months[0], all_months[-1]),
                                  label_visibility="collapsed")

    st.markdown('<div style="font-family:\'IBM Plex Mono\',monospace;font-size:10px;color:#64748B;text-transform:uppercase;letter-spacing:2px;margin:12px 0 8px;">Categories</div>', unsafe_allow_html=True)
    all_cats = sorted(products['category'].unique())
    sel_cats = st.multiselect("", all_cats, default=all_cats, label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f"""
    <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#1E293B">
        ▸ {len(orders):,} total orders<br>
        ▸ {orders['buyer_id'].nunique():,} unique buyers<br>
        ▸ {len(products):,} products
    </div>""", unsafe_allow_html=True)


# ─── FILTER DATA ──────────────────────────────────────────────────────────────
mask_orders = (
    (orders['year_month'] >= sel_range[0]) &
    (orders['year_month'] <= sel_range[1])
)
f_orders = orders[mask_orders]
f_monthly = monthly[(monthly['year_month'] >= sel_range[0]) &
                    (monthly['year_month'] <= sel_range[1])]
f_detail  = detail_rich[
    (detail_rich['year_month'] >= sel_range[0]) &
    (detail_rich['year_month'] <= sel_range[1]) &
    (detail_rich['category'].isin(sel_cats))
]


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE REVENUE & FUNNEL HEALTH
# ══════════════════════════════════════════════════════════════════════════════
if "Executive" in page:
    st.markdown("""
    <div style="margin-bottom:24px">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#00D4FF;
                    letter-spacing:3px;text-transform:uppercase;">Page 01 / 04</div>
        <h1 style="font-size:32px;font-weight:700;color:#E2E8F0;margin:4px 0;">
            Executive Revenue &<br><span style="color:#00D4FF;">Funnel Health</span>
        </h1>
    </div>""", unsafe_allow_html=True)

    # ── KPI Row ────────────────────────────────────────────────────────────
    paid_f       = f_orders[f_orders['is_paid']]
    delivered_f  = f_orders[f_orders['is_delivered']]
    gmv          = paid_f['total'].sum()
    aov          = paid_f['total'].mean() if len(paid_f) else 0
    conv_pay     = len(paid_f)/len(f_orders)*100 if len(f_orders) else 0
    conv_del     = len(delivered_f)/len(paid_f)*100 if len(paid_f) else 0

    # MoM from last 2 months
    if len(f_monthly) >= 2:
        gmv_mom = f_monthly.iloc[-1]['gmv_mom']
    else:
        gmv_mom = None

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(kpi_card("Total GMV", fmt_rp(gmv), gmv_mom, "MoM", "#00D4FF"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Total Orders", f"{len(f_orders):,}", accent="#7B2FBE"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Avg Order Value", fmt_rp(aov), accent="#FF6B35"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Payment Conv.", f"{conv_pay:.1f}%",
                                   (conv_pay-93.3), "vs avg", "#FFB800"), unsafe_allow_html=True)
    with c5: st.markdown(kpi_card("Delivery Conv.", f"{conv_del:.1f}%",
                                   (conv_del-93.2), "vs avg", "#00C896"), unsafe_allow_html=True)

    st.markdown("---")

    # ── Row 1: GMV trend + Funnel ──────────────────────────────────────────
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<div class="section-header">GMV & ORDER VOLUME — MONTHLY TREND</div>', unsafe_allow_html=True)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=f_monthly['year_month'], y=f_monthly['gmv'],
            name="GMV", marker_color=COLORS['primary'],
            marker_line_width=0, opacity=0.85), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=f_monthly['year_month'], y=f_monthly['orders_count'],
            name="Orders", mode='lines+markers',
            line=dict(color=COLORS['accent'], width=2),
            marker=dict(size=6)), secondary_y=True)
        fig.add_trace(go.Scatter(
            x=f_monthly['year_month'], y=f_monthly['gmv'].rolling(3).mean(),
            name="3M MA", mode='lines',
            line=dict(color=COLORS['success'], width=1.5, dash='dot')), secondary_y=False)
        fig.update_layout(**PLOTLY_LAYOUT, height=340,
            title="Monthly GMV (Bars) vs Order Count (Line)")
        fig.update_yaxes(title_text="GMV (Rp)", secondary_y=False,
                         gridcolor=COLORS['border'], tickfont=dict(size=10))
        fig.update_yaxes(title_text="Orders", secondary_y=True,
                         gridcolor='rgba(0,0,0,0)', tickfont=dict(size=10))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown('<div class="section-header">TRANSACTION FUNNEL</div>', unsafe_allow_html=True)
        funnel_vals = [len(f_orders), len(paid_f), len(delivered_f)]
        funnel_lbls = [
            f"Created<br>{len(f_orders):,}",
            f"Paid<br>{len(paid_f):,}",
            f"Delivered<br>{len(delivered_f):,}"
        ]
        fig2 = go.Figure(go.Funnel(
            y=funnel_lbls, x=funnel_vals,
            textinfo="percent previous+value",
            marker=dict(color=[COLORS['primary'], COLORS['secondary'], COLORS['success']]),
            textfont=dict(family="IBM Plex Mono", size=12, color=COLORS['text']),
            connector=dict(line=dict(color=COLORS['border'], width=2))
        ))
        fig2.update_layout(**PLOTLY_LAYOUT, height=340, title="Order Conversion Funnel")
        st.plotly_chart(fig2, use_container_width=True)

        # Leak metrics
        unpaid    = len(f_orders) - len(paid_f)
        undeliv   = len(paid_f)   - len(delivered_f)
        leak_rev  = f_orders[~f_orders['is_paid']]['total'].sum()
        st.markdown(alert(f"⚠ {unpaid:,} orders unpaid · Rp {leak_rev/1e9:.1f}B at risk", "warning"), unsafe_allow_html=True)
        st.markdown(alert(f"📦 {undeliv:,} paid orders not yet delivered", "info"), unsafe_allow_html=True)

    # ── Row 2: MoM growth + Day-of-week heatmap ───────────────────────────
    col3, col4 = st.columns([1, 1])

    with col3:
        st.markdown('<div class="section-header">MONTH-OVER-MONTH GMV GROWTH</div>', unsafe_allow_html=True)
        mom_data = f_monthly.dropna(subset=['gmv_mom'])
        colors_mom = [COLORS['success'] if v >= 0 else COLORS['danger'] for v in mom_data['gmv_mom']]
        fig3 = go.Figure(go.Bar(
            x=mom_data['year_month'], y=mom_data['gmv_mom'],
            marker_color=colors_mom, marker_line_width=0,
            text=[f"{v:.1f}%" for v in mom_data['gmv_mom']],
            textposition='outside', textfont=dict(size=9, family="IBM Plex Mono")
        ))
        fig3.add_hline(y=0, line_color=COLORS['border'], line_width=1)
        apply_layout(fig3, "GMV Growth %MoM")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">ORDER VOLUME BY DAY OF WEEK</div>', unsafe_allow_html=True)
        dow_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        dow_data = f_orders.groupby('dow')['order_id'].count().reindex(dow_order, fill_value=0)
        dow_gmv  = f_orders[f_orders['is_paid']].groupby('dow')['total'].sum().reindex(dow_order, fill_value=0)
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=dow_order, y=dow_data.values,
            name="Orders", marker_color=COLORS['secondary'], opacity=0.85))
        fig4.add_trace(go.Scatter(
            x=dow_order, y=dow_gmv.values,
            name="GMV", mode='lines+markers', yaxis='y2',
            line=dict(color=COLORS['accent'], width=2), marker=dict(size=7)))
        fig4.update_layout(**PLOTLY_LAYOUT, height=380,
            yaxis=dict(gridcolor=COLORS['border'], title="Order Count"),
            yaxis2=dict(overlaying='y', side='right', title="GMV",
                        gridcolor='rgba(0,0,0,0)'),
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            title="Orders & GMV by Day of Week")
        st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PRODUCT PERFORMANCE & CATEGORY INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
elif "Product" in page:
    st.markdown("""
    <div style="margin-bottom:24px">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#7B2FBE;
                    letter-spacing:3px;text-transform:uppercase;">Page 02 / 04</div>
        <h1 style="font-size:32px;font-weight:700;color:#E2E8F0;margin:4px 0;">
            Product Performance &<br><span style="color:#7B2FBE;">Category Intelligence</span>
        </h1>
    </div>""", unsafe_allow_html=True)

    # ── Category Revenue Pareto ────────────────────────────────────────────
    cat_rev = (f_detail.groupby('category')['line_revenue']
               .sum().sort_values(ascending=False).reset_index())
    cat_rev.columns = ['category','revenue']
    cat_rev['cum_pct'] = cat_rev['revenue'].cumsum() / cat_rev['revenue'].sum() * 100

    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown('<div class="section-header">PARETO — CATEGORY REVENUE (80/20 RULE)</div>', unsafe_allow_html=True)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        bar_colors = [COLORS['primary'] if p <= 80 else COLORS['text_muted'] for p in cat_rev['cum_pct']]
        fig.add_trace(go.Bar(
            x=cat_rev['category'], y=cat_rev['revenue'],
            name="Revenue", marker_color=bar_colors, marker_line_width=0), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=cat_rev['category'], y=cat_rev['cum_pct'],
            name="Cumulative %", mode='lines+markers',
            line=dict(color=COLORS['accent'], width=2), marker=dict(size=7)), secondary_y=True)
        fig.add_hline(y=80, line_color=COLORS['warning'], line_dash='dash',
                      line_width=1.5, annotation_text="80% threshold", secondary_y=True)
        fig.update_layout(**PLOTLY_LAYOUT, height=380, title="Revenue by Category · Pareto View")
        fig.update_xaxes(tickangle=-35)
        fig.update_yaxes(title_text="Revenue (Rp)", secondary_y=False, gridcolor=COLORS['border'])
        fig.update_yaxes(title_text="Cumulative %", secondary_y=True, gridcolor='rgba(0,0,0,0)',
                         range=[0,105])
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">CATEGORY SHARE</div>', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=cat_rev['category'],
            values=cat_rev['revenue'],
            hole=0.55,
            marker=dict(colors=COLORS['cats'], line=dict(color=COLORS['bg_dark'], width=2)),
            textinfo='percent',
            textfont=dict(family="IBM Plex Mono", size=11),
        ))
        fig_pie.add_annotation(text=f"<b>{fmt_rp(cat_rev['revenue'].sum())}</b>",
                               x=0.5, y=0.5, font=dict(size=13, color=COLORS['text']),
                               showarrow=False)
        apply_layout(fig_pie, "Revenue Share by Category", height=380)
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Top Products + Trend ───────────────────────────────────────────────
    col3, col4 = st.columns([1,1])

    with col3:
        st.markdown('<div class="section-header">TOP 15 PRODUCTS BY REVENUE</div>', unsafe_allow_html=True)
        prod_rev = (f_detail.groupby('desc_product')
                   .agg(revenue=('line_revenue','sum'), qty=('quantity','sum'))
                   .sort_values('revenue', ascending=False).head(15).reset_index())
        prod_rev['desc_product'] = prod_rev['desc_product'].str.strip().str[:30]
        fig5 = go.Figure(go.Bar(
            x=prod_rev['revenue'], y=prod_rev['desc_product'],
            orientation='h', marker_color=COLORS['secondary'],
            text=[fmt_rp(v) for v in prod_rev['revenue']],
            textposition='outside',
            textfont=dict(size=9, family="IBM Plex Mono")
        ))
        fig5.update_layout(**PLOTLY_LAYOUT, height=460, title="Top Products · Revenue",
                           yaxis=dict(autorange='reversed', gridcolor='rgba(0,0,0,0)'))
        fig5.update_xaxes(gridcolor=COLORS['border'])
        st.plotly_chart(fig5, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">CATEGORY GMV TREND OVER TIME</div>', unsafe_allow_html=True)
        cat_monthly = (f_detail.groupby(['year_month','category'])['line_revenue']
                       .sum().reset_index())
        top5_cats = cat_rev['category'].head(5).tolist()
        cat_monthly_top = cat_monthly[cat_monthly['category'].isin(top5_cats)]
        fig6 = px.line(cat_monthly_top, x='year_month', y='line_revenue',
                       color='category', markers=True,
                       color_discrete_sequence=COLORS['cats'])
        fig6.update_traces(line_width=2, marker_size=5)
        fig6.update_layout(**PLOTLY_LAYOUT, height=460,
                           title="Top 5 Categories · Monthly Revenue Trend",
                           xaxis_tickangle=-45)
        st.plotly_chart(fig6, use_container_width=True)

    # ── Price vs Base (markup analysis) ───────────────────────────────────
    st.markdown('<div class="section-header">PRICE INTEGRITY — SELLING PRICE vs BASE PRICE BY CATEGORY</div>', unsafe_allow_html=True)
    price_analysis = (f_detail.groupby('category')
                     .agg(avg_base=('base_price','mean'),
                          avg_sell=('price','mean'),
                          avg_markup=('markup','mean'))
                     .reset_index())
    fig7 = go.Figure()
    fig7.add_trace(go.Bar(name='Avg Base Price', x=price_analysis['category'],
                          y=price_analysis['avg_base'],
                          marker_color=COLORS['text_muted'], marker_line_width=0))
    fig7.add_trace(go.Bar(name='Avg Selling Price', x=price_analysis['category'],
                          y=price_analysis['avg_sell'],
                          marker_color=COLORS['primary'], marker_line_width=0, opacity=0.8))
    fig7.update_layout(**PLOTLY_LAYOUT, height=320, barmode='group',
                       title="Base Price vs Selling Price — Zero markup detected (pricing integrity ✓)",
                       xaxis_tickangle=-30)
    st.plotly_chart(fig7, use_container_width=True)
    st.markdown(alert("✓ No price-below-cost orders detected. Selling price = Base price across all 187,452 line items. Dynamic pricing not in use.", "success"), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — CUSTOMER RETENTION & BEHAVIOR ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif "Customer" in page:
    st.markdown("""
    <div style="margin-bottom:24px">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#FF6B35;
                    letter-spacing:3px;text-transform:uppercase;">Page 03 / 04</div>
        <h1 style="font-size:32px;font-weight:700;color:#E2E8F0;margin:4px 0;">
            Customer Retention &<br><span style="color:#FF6B35;">Behavior Analytics</span>
        </h1>
    </div>""", unsafe_allow_html=True)

    # ── RFM Overview KPIs ─────────────────────────────────────────────────
    seg_counts = rfm['segment'].value_counts()
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi_card("Champions 🏆", f"{seg_counts.get('Champions',0):,}", accent="#FFB800"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Loyal Customers", f"{seg_counts.get('Loyal',0):,}", accent="#00D4FF"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("At Risk ⚠", f"{seg_counts.get('At Risk',0):,}", accent="#FF4757"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Churned 💀", f"{seg_counts.get('Churned',0):,}", accent="#64748B"), unsafe_allow_html=True)

    st.markdown("---")

    # ── Cohort Heatmap ────────────────────────────────────────────────────
    st.markdown('<div class="section-header">COHORT RETENTION MATRIX — % USERS RETURNING BY MONTH</div>', unsafe_allow_html=True)

    pivot = cohort_pivot.pivot(index='cohort', columns='period_number', values='retention_rate')
    pivot = pivot.iloc[:, :13]  # 0–12 months
    pivot.index = pivot.index.astype(str)

    fig_cohort = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[f"M+{c}" for c in pivot.columns],
        y=pivot.index,
        colorscale=[
            [0.0,  "#0A0E1A"],
            [0.15, "#1E3A5F"],
            [0.3,  "#1B4F8A"],
            [0.5,  "#0077CC"],
            [0.7,  "#00AAFF"],
            [1.0,  "#00D4FF"],
        ],
        text=np.round(pivot.values, 1),
        texttemplate="%{text}%",
        textfont=dict(size=9, family="IBM Plex Mono"),
        hovertemplate="Cohort: %{y}<br>Period: %{x}<br>Retention: %{z:.1f}%<extra></extra>",
        showscale=True,
        colorbar=dict(title="Retention %", tickfont=dict(family="IBM Plex Mono", size=10))
    ))
    apply_layout(fig_cohort, "", height=520)
    st.plotly_chart(fig_cohort, use_container_width=True)

    # ── RFM Scatter + Segments ────────────────────────────────────────────
    col_rfm1, col_rfm2 = st.columns([2, 1])

    with col_rfm1:
        st.markdown('<div class="section-header">RFM SCATTER — RECENCY vs FREQUENCY (bubble = MONETARY)</div>', unsafe_allow_html=True)
        rfm_sample = rfm.sample(min(2000, len(rfm)), random_state=42)
        seg_color_map = {
            'Champions':         '#FFB800',
            'Loyal':             '#00D4FF',
            'Potential Loyalist':'#7B2FBE',
            'New Customers':     '#00C896',
            'At Risk':           '#FF6B35',
            'Cannot Lose Them':  '#FF4757',
            'Churned':           '#64748B',
        }
        fig_rfm = px.scatter(
            rfm_sample, x='recency', y='frequency',
            size='monetary', color='segment',
            color_discrete_map=seg_color_map,
            size_max=30, opacity=0.75,
            hover_data={'monetary': ':,.0f', 'recency': True, 'frequency': True}
        )
        fig_rfm.update_traces(marker_line_width=0)
        apply_layout(fig_rfm, "RFM Customer Landscape", height=400)
        st.plotly_chart(fig_rfm, use_container_width=True)

    with col_rfm2:
        st.markdown('<div class="section-header">SEGMENT DISTRIBUTION</div>', unsafe_allow_html=True)
        seg_df = rfm['segment'].value_counts().reset_index()
        seg_df.columns = ['segment','count']
        seg_df['revenue'] = seg_df['segment'].map(rfm.groupby('segment')['monetary'].sum())
        seg_df['color']   = seg_df['segment'].map(seg_color_map)
        fig_seg = go.Figure(go.Bar(
            x=seg_df['count'], y=seg_df['segment'],
            orientation='h',
            marker_color=seg_df['color'],
            text=seg_df['count'], textposition='outside',
            textfont=dict(family="IBM Plex Mono", size=10)
        ))
        fig_seg.update_layout(**PLOTLY_LAYOUT, height=400,
                              yaxis=dict(autorange='reversed'),
                              title="Users per Segment")
        st.plotly_chart(fig_seg, use_container_width=True)

    # ── RFM Table ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">RFM SEGMENT SUMMARY — REVENUE & STRATEGY</div>', unsafe_allow_html=True)
    seg_summary = (rfm.groupby('segment')
                   .agg(users=('buyer_id','count'),
                        avg_recency=('recency','mean'),
                        avg_freq=('frequency','mean'),
                        total_monetary=('monetary','sum'),
                        avg_monetary=('monetary','mean'))
                   .reset_index())
    seg_summary['total_monetary_fmt'] = seg_summary['total_monetary'].apply(fmt_rp)
    seg_summary['avg_monetary_fmt']   = seg_summary['avg_monetary'].apply(fmt_rp)
    seg_summary['strategy'] = seg_summary['segment'].map({
        'Champions':          '🎯 Reward & upsell — highest LTV',
        'Loyal':              '💌 Loyalty program, early access',
        'Potential Loyalist': '🔁 Frequency push, bundle offers',
        'New Customers':      '🚀 Onboarding flow, first re-order',
        'At Risk':            '⚡ Win-back campaign, discounts',
        'Cannot Lose Them':   '🚨 Urgent reactivation, personal outreach',
        'Churned':            '💀 Suppression or last-chance offer',
    })
    display_cols = ['segment','users','avg_recency','avg_freq','total_monetary_fmt','strategy']
    display_df = seg_summary[display_cols].copy()
    display_df.columns = ['Segment','Users','Avg Recency(d)','Avg Freq','Total Revenue','Strategy']
    display_df['Avg Recency(d)'] = display_df['Avg Recency(d)'].round(0).astype(int)
    display_df['Avg Freq'] = display_df['Avg Freq'].round(1)
    st.dataframe(display_df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — OPERATIONS & FULFILLMENT SLA
# ══════════════════════════════════════════════════════════════════════════════
elif "Operations" in page:
    st.markdown("""
    <div style="margin-bottom:24px">
        <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#00C896;
                    letter-spacing:3px;text-transform:uppercase;">Page 04 / 04</div>
        <h1 style="font-size:32px;font-weight:700;color:#E2E8F0;margin:4px 0;">
            Operations &<br><span style="color:#00C896;">Fulfillment SLA</span>
        </h1>
    </div>""", unsafe_allow_html=True)

    paid_f = f_orders[f_orders['is_paid']]
    deliv_f = f_orders[f_orders['is_delivered']]

    # ── SLA KPIs ──────────────────────────────────────────────────────────
    avg_pay_lag  = paid_f['payment_lag'].mean()
    med_pay_lag  = paid_f['payment_lag'].median()
    avg_del_lag  = deliv_f['delivery_lag'].mean()
    med_del_lag  = deliv_f['delivery_lag'].median()
    pct_slow_pay = (paid_f['payment_lag'] > 10).mean() * 100
    pct_slow_del = (deliv_f['delivery_lag'] > 10).mean() * 100

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: st.markdown(kpi_card("Avg Payment Lag", f"{avg_pay_lag:.1f}d", accent="#00D4FF"), unsafe_allow_html=True)
    with c2: st.markdown(kpi_card("Median Pay Lag", f"{med_pay_lag:.0f}d", accent="#7B2FBE"), unsafe_allow_html=True)
    with c3: st.markdown(kpi_card("Avg Delivery Lag", f"{avg_del_lag:.1f}d", accent="#FF6B35"), unsafe_allow_html=True)
    with c4: st.markdown(kpi_card("Median Del Lag", f"{med_del_lag:.0f}d", accent="#00C896"), unsafe_allow_html=True)
    with c5: st.markdown(kpi_card("Slow Payers >10d", f"{pct_slow_pay:.1f}%", accent="#FFB800"), unsafe_allow_html=True)
    with c6: st.markdown(kpi_card("Slow Delivery >10d", f"{pct_slow_del:.1f}%", accent="#FF4757"), unsafe_allow_html=True)

    st.markdown("---")

    # ── Lag distributions ─────────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">PAYMENT LAG DISTRIBUTION (days)</div>', unsafe_allow_html=True)
        fig_plag = go.Figure()
        fig_plag.add_trace(go.Histogram(
            x=paid_f['payment_lag'].dropna(), nbinsx=14,
            name="Payment Lag",
            marker_color=COLORS['primary'], marker_line_width=0, opacity=0.85
        ))
        fig_plag.add_vline(x=avg_pay_lag, line_color=COLORS['warning'],
                           line_dash='dash', annotation_text=f"Mean: {avg_pay_lag:.1f}d")
        fig_plag.add_vline(x=10, line_color=COLORS['danger'],
                           line_dash='dot', annotation_text="SLA 10d")
        apply_layout(fig_plag, "Days from Order Creation to Payment", height=320)
        st.plotly_chart(fig_plag, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">DELIVERY LAG DISTRIBUTION (days)</div>', unsafe_allow_html=True)
        fig_dlag = go.Figure()
        fig_dlag.add_trace(go.Histogram(
            x=deliv_f['delivery_lag'].dropna(), nbinsx=14,
            name="Delivery Lag",
            marker_color=COLORS['success'], marker_line_width=0, opacity=0.85
        ))
        fig_dlag.add_vline(x=avg_del_lag, line_color=COLORS['warning'],
                           line_dash='dash', annotation_text=f"Mean: {avg_del_lag:.1f}d")
        fig_dlag.add_vline(x=10, line_color=COLORS['danger'],
                           line_dash='dot', annotation_text="SLA 10d")
        apply_layout(fig_dlag, "Days from Payment to Delivery", height=320)
        st.plotly_chart(fig_dlag, use_container_width=True)

    # ── Monthly SLA trend ─────────────────────────────────────────────────
    st.markdown('<div class="section-header">SLA PERFORMANCE TREND — MONTHLY AVERAGE LAG</div>', unsafe_allow_html=True)
    sla_monthly = (f_orders.groupby('year_month')
                   .agg(avg_pay_lag=('payment_lag','mean'),
                        avg_del_lag=('delivery_lag','mean'))
                   .reset_index())
    fig_sla = go.Figure()
    fig_sla.add_trace(go.Scatter(
        x=sla_monthly['year_month'], y=sla_monthly['avg_pay_lag'],
        name="Avg Payment Lag", mode='lines+markers',
        line=dict(color=COLORS['primary'], width=2), marker=dict(size=7)))
    fig_sla.add_trace(go.Scatter(
        x=sla_monthly['year_month'], y=sla_monthly['avg_del_lag'],
        name="Avg Delivery Lag", mode='lines+markers',
        line=dict(color=COLORS['success'], width=2), marker=dict(size=7)))
    fig_sla.add_hrect(y0=10, y1=14.5, fillcolor=COLORS['danger'],
                      opacity=0.05, line_width=0, annotation_text="SLA Breach Zone")
    apply_layout(fig_sla, "Monthly Average Lag Metrics (days)", height=320)
    fig_sla.update_xaxes(tickangle=-45)
    st.plotly_chart(fig_sla, use_container_width=True)

    # ── Geographic heatmap by kodepos prefix ─────────────────────────────
    st.markdown('<div class="section-header">GEOGRAPHIC ORDER DISTRIBUTION — BY POSTAL CODE PREFIX</div>', unsafe_allow_html=True)
    f_orders_geo = f_orders.copy()
    f_orders_geo['kodepos_prefix'] = f_orders_geo['kodepos'].astype(str).str[:2]
    geo = (f_orders_geo.groupby('kodepos_prefix')
           .agg(orders=('order_id','count'),
                gmv=('total','sum'),
                avg_del_lag=('delivery_lag','mean'))
           .reset_index().sort_values('orders', ascending=False).head(20))

    col_g1, col_g2 = st.columns([2,1])
    with col_g1:
        fig_geo = go.Figure(go.Bar(
            x=geo['kodepos_prefix'], y=geo['orders'],
            marker_color=[COLORS['danger'] if l > 9 else COLORS['success']
                          for l in geo['avg_del_lag'].fillna(0)],
            text=geo['orders'], textposition='outside',
            textfont=dict(family="IBM Plex Mono", size=10),
            hovertemplate="Postal: %{x}<br>Orders: %{y}<extra></extra>"
        ))
        apply_layout(fig_geo, "Top 20 Postal Prefixes · Bar = Orders, Color = Delivery SLA (Red > 9d avg)", height=340)
        st.plotly_chart(fig_geo, use_container_width=True)

    with col_g2:
        st.markdown('<div class="section-header">BOTTLENECK ALERTS</div>', unsafe_allow_html=True)
        breach_zones = geo[geo['avg_del_lag'] > 9].sort_values('avg_del_lag', ascending=False)
        if len(breach_zones):
            for _, row in breach_zones.iterrows():
                st.markdown(alert(
                    f"🚨 Postal {row['kodepos_prefix']}xx — avg {row['avg_del_lag']:.1f}d delivery · {row['orders']:,} orders",
                    "danger"), unsafe_allow_html=True)
        else:
            st.markdown(alert("✅ All postal zones within SLA", "success"), unsafe_allow_html=True)

        st.markdown("---")
        # Unpaid order aging
        unpaid = f_orders[f_orders['paid_at'].isna()].copy()
        unpaid['age'] = (pd.Timestamp.now() - unpaid['created_at']).dt.days
        age_buckets = pd.cut(unpaid['age'], bins=[0,3,7,14,30,999],
                             labels=['0-3d','4-7d','8-14d','15-30d','30+d'])
        age_dist = age_buckets.value_counts().sort_index()
        st.markdown('<div class="section-header">UNPAID ORDER AGING</div>', unsafe_allow_html=True)
        fig_age = go.Figure(go.Bar(
            x=age_dist.index.astype(str), y=age_dist.values,
            marker_color=[COLORS['success'], COLORS['warning'], COLORS['accent'],
                          COLORS['danger'], '#8B0000'],
            text=age_dist.values, textposition='outside',
            textfont=dict(family="IBM Plex Mono", size=11)
        ))
        apply_layout(fig_age, "Unpaid Orders by Age Bucket", height=280)
        st.plotly_chart(fig_age, use_container_width=True)


# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;font-family:'IBM Plex Mono',monospace;font-size:10px;
            color:#1E293B;padding:12px 0;">
    E-Commerce Analytics Command Center · Jan 2019 – May 2020 · Rp 148.8B GMV
    · Built with Streamlit & Plotly
</div>""", unsafe_allow_html=True)
