"""
E-Commerce Analytics Dashboard
Clean · Professional · Dark/Light Mode
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
    page_title="E-Commerce Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── THEME TOGGLE ─────────────────────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# ─── THEME COLORS ─────────────────────────────────────────────────────────────
def get_theme():
    if st.session_state.dark_mode:
        return {
            "bg":           "#0F1117",
            "card":         "#1A1D27",
            "card2":        "#22263A",
            "text":         "#F0F2F6",
            "text_muted":   "#8B92A5",
            "border":       "#2D3147",
            "primary":      "#4F8EF7",
            "success":      "#2DD4BF",
            "warning":      "#FBBF24",
            "danger":       "#F87171",
            "accent":       "#A78BFA",
            "plot_bg":      "rgba(0,0,0,0)",
            "paper_bg":     "rgba(0,0,0,0)",
            "grid":         "#2D3147",
            "font_color":   "#F0F2F6",
            "cats": ["#4F8EF7","#2DD4BF","#FBBF24","#F87171","#A78BFA",
                     "#34D399","#FB923C","#60A5FA","#F472B6","#38BDF8",
                     "#C084FC","#FCD34D"],
        }
    else:
        return {
            "bg":           "#F8FAFC",
            "card":         "#FFFFFF",
            "card2":        "#F1F5F9",
            "text":         "#0F172A",
            "text_muted":   "#64748B",
            "border":       "#E2E8F0",
            "primary":      "#3B82F6",
            "success":      "#0D9488",
            "warning":      "#D97706",
            "danger":       "#DC2626",
            "accent":       "#7C3AED",
            "plot_bg":      "rgba(0,0,0,0)",
            "paper_bg":     "rgba(0,0,0,0)",
            "grid":         "#E2E8F0",
            "font_color":   "#0F172A",
            "cats": ["#3B82F6","#0D9488","#D97706","#DC2626","#7C3AED",
                     "#059669","#EA580C","#2563EB","#DB2777","#0284C7",
                     "#9333EA","#CA8A04"],
        }

T = get_theme()

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
    background-color: {T['bg']} !important;
    color: {T['text']} !important;
}}
[data-testid="stSidebar"] {{
    background-color: {T['card']} !important;
    border-right: 1px solid {T['border']} !important;
}}
[data-testid="stSidebar"] * {{ color: {T['text']} !important; }}
.block-container {{ padding: 1.5rem 2rem !important; }}
.stPlotlyChart {{ border-radius: 12px; }}

/* KPI Cards */
.kpi-card {{
    background: {T['card']};
    border: 1px solid {T['border']};
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
    border-left: 4px solid var(--accent);
}}
.kpi-label {{
    font-size: 12px;
    font-weight: 500;
    color: {T['text_muted']};
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}}
.kpi-value {{
    font-size: 26px;
    font-weight: 700;
    color: {T['text']};
    line-height: 1.1;
}}
.kpi-sub {{
    font-size: 12px;
    color: {T['text_muted']};
    margin-top: 4px;
}}
.kpi-up   {{ color: {T['success']}; font-size: 12px; margin-top: 4px; }}
.kpi-down {{ color: {T['danger']};  font-size: 12px; margin-top: 4px; }}

/* Section title */
.sec-title {{
    font-size: 13px;
    font-weight: 600;
    color: {T['text_muted']};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid {T['border']};
}}

/* Chart wrapper */
.chart-box {{
    background: {T['card']};
    border: 1px solid {T['border']};
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
}}

/* Alert */
.alert {{
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    font-weight: 500;
    margin: 6px 0;
    border-left: 3px solid;
}}
.alert-warn    {{ background:{T['warning']}18; border-color:{T['warning']}; color:{T['warning']}; }}
.alert-danger  {{ background:{T['danger']}18;  border-color:{T['danger']};  color:{T['danger']};  }}
.alert-success {{ background:{T['success']}18; border-color:{T['success']}; color:{T['success']}; }}
.alert-info    {{ background:{T['primary']}18; border-color:{T['primary']}; color:{T['primary']}; }}

/* Page header */
.page-header {{
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 2px solid {T['border']};
}}
.page-header h1 {{
    font-size: 26px;
    font-weight: 700;
    color: {T['text']};
    margin: 0;
}}
.page-header p {{
    font-size: 13px;
    color: {T['text_muted']};
    margin: 4px 0 0 0;
}}

div[data-testid="metric-container"] {{ display: none; }}
hr {{ border-color: {T['border']} !important; }}
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ──────────────────────────────────────────────────────────────────
def fmt_rp(x):
    if x >= 1e12: return f"Rp {x/1e12:.2f}T"
    if x >= 1e9:  return f"Rp {x/1e9:.1f}B"
    if x >= 1e6:  return f"Rp {x/1e6:.1f}M"
    return f"Rp {x:,.0f}"

def kpi(label, value, sub="", delta=None, accent=None):
    accent = accent or T['primary']
    delta_html = ""
    if delta is not None:
        cls = "kpi-up" if delta >= 0 else "kpi-down"
        icon = "▲" if delta >= 0 else "▼"
        delta_html = f'<div class="{cls}">{icon} {abs(delta):.1f}% MoM</div>'
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return f"""
    <div class="kpi-card" style="--accent:{accent}; border-left-color:{accent}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {sub_html}{delta_html}
    </div>"""

def alert(msg, kind="info"):
    return f'<div class="alert alert-{kind}">{msg}</div>'

def base_layout(title="", height=360):
    return dict(
        paper_bgcolor=T['paper_bg'],
        plot_bgcolor=T['plot_bg'],
        font=dict(family="Inter", color=T['font_color'], size=12),
        title=dict(text=title, font=dict(size=13, color=T['text_muted']), x=0),
        margin=dict(l=10, r=10, t=40, b=10),
        height=height,
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=T['border'],
                    borderwidth=1, font=dict(size=11)),
        xaxis=dict(gridcolor=T['grid'], zerolinecolor=T['grid'],
                   tickfont=dict(size=11), linecolor=T['border']),
        yaxis=dict(gridcolor=T['grid'], zerolinecolor=T['grid'],
                   tickfont=dict(size=11), linecolor=T['border']),
    )


# ─── DATA LOADING ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    orders = pd.read_csv('orders.csv', sep=';',
                         parse_dates=['created_at','paid_at','delivery_at'])
    order_details = pd.read_csv('order_details.csv', sep=';')
    products = pd.read_csv('products.csv', sep=';')
    users = pd.read_csv('users.csv', sep=';', on_bad_lines='skip')

    orders['is_paid']      = orders['paid_at'].notna()
    orders['is_delivered'] = orders['delivery_at'].notna()
    orders['payment_lag']  = (orders['paid_at'] - orders['created_at']).dt.days
    orders['delivery_lag'] = (orders['delivery_at'] - orders['paid_at']).dt.days
    orders['year_month']   = orders['created_at'].dt.to_period('M').astype(str)
    orders['dow']          = orders['created_at'].dt.day_name()

    detail = (order_details
              .merge(products, on='product_id', how='left')
              .merge(orders[['order_id','created_at','buyer_id','is_paid',
                             'is_delivered','year_month','total']], on='order_id', how='left'))
    detail['line_revenue'] = detail['price'] * detail['quantity']

    paid = orders[orders['is_paid']]
    monthly = (paid.groupby('year_month')
               .agg(gmv=('total','sum'), orders_n=('order_id','count'),
                    buyers=('buyer_id','nunique'))
               .reset_index())
    monthly['aov']     = monthly['gmv'] / monthly['orders_n']
    monthly['gmv_mom'] = monthly['gmv'].pct_change() * 100
    monthly['sort_k']  = pd.to_datetime(monthly['year_month'])
    monthly = monthly.sort_values('sort_k')

    snapshot = orders['created_at'].max() + pd.Timedelta(days=1)
    rfm = (paid.groupby('buyer_id')
           .agg(recency=('created_at', lambda x: (snapshot-x.max()).days),
                frequency=('order_id','count'),
                monetary=('total','sum'))
           .reset_index())
    rfm['R'] = pd.qcut(rfm['recency'],   5, labels=[5,4,3,2,1], duplicates='drop').astype(int)
    rfm['F'] = pd.qcut(rfm['frequency'], 5, labels=[1,2,3,4,5], duplicates='drop').astype(int)
    rfm['M'] = pd.qcut(rfm['monetary'],  5, labels=[1,2,3,4,5], duplicates='drop').astype(int)

    def segment(r):
        rv, f, m = r['R'], r['F'], r['M']
        if rv >= 4 and f >= 4 and m >= 4: return 'Champions'
        elif rv >= 3 and f >= 3:          return 'Loyal'
        elif rv >= 4 and f <= 2:          return 'New Customers'
        elif rv >= 3 and f >= 2:          return 'Potential Loyalist'
        elif rv == 2 and f >= 2:          return 'At Risk'
        elif rv <= 2 and f >= 3:          return 'Cannot Lose Them'
        else:                             return 'Churned'
    rfm['segment'] = rfm.apply(segment, axis=1)

    orders['cohort'] = (orders.groupby('buyer_id')['created_at']
                              .transform('min').dt.to_period('M').astype(str))
    orders['order_period'] = orders['created_at'].dt.to_period('M').astype(str)

    def pdiff(a, b):
        return (pd.Period(b,'M') - pd.Period(a,'M')).n

    orders['period_n'] = orders.apply(lambda r: pdiff(r['cohort'], r['order_period']), axis=1)
    coh = orders.groupby(['cohort','period_n'])['buyer_id'].nunique().reset_index()
    sizes = coh[coh['period_n']==0].set_index('cohort')['buyer_id']
    coh['retention'] = coh.apply(lambda r: r['buyer_id']/sizes.get(r['cohort'],1)*100, axis=1)

    return dict(orders=orders, detail=detail, products=products,
                monthly=monthly, rfm=rfm, cohort=coh)

with st.spinner("Loading data..."):
    D = load_data()

orders   = D['orders']
detail   = D['detail']
products = D['products']
monthly  = D['monthly']
rfm      = D['rfm']
cohort   = D['cohort']


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo + Toggle
    col_logo, col_toggle = st.columns([3,1])
    with col_logo:
        st.markdown(f"""
        <div style="padding:8px 0 16px">
            <div style="font-size:11px;font-weight:600;color:{T['primary']};
                        letter-spacing:2px;text-transform:uppercase;">Analytics</div>
            <div style="font-size:20px;font-weight:700;color:{T['text']};margin-top:2px;">
                E-Commerce<br>Dashboard
            </div>
            <div style="font-size:11px;color:{T['text_muted']};margin-top:4px;">
                Jan 2019 – May 2020
            </div>
        </div>""", unsafe_allow_html=True)
    with col_toggle:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🌙" if st.session_state.dark_mode else "☀️", help="Toggle Dark/Light"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    st.markdown(f'<hr style="border-color:{T["border"]};margin:0 0 16px">', unsafe_allow_html=True)

    # Navigation
    st.markdown(f'<div style="font-size:11px;font-weight:600;color:{T["text_muted"]};text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Navigation</div>', unsafe_allow_html=True)
    page = st.radio("", [
        "📊  Executive Overview",
        "📦  Product Intelligence",
        "👤  Customer Analytics",
        "🚚  Operations & SLA",
    ], label_visibility="collapsed")

    st.markdown(f'<hr style="border-color:{T["border"]};margin:16px 0">', unsafe_allow_html=True)

    # Filters
    st.markdown(f'<div style="font-size:11px;font-weight:600;color:{T["text_muted"]};text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Filters</div>', unsafe_allow_html=True)

    all_months = sorted(orders['year_month'].unique())
    sel_range = st.select_slider(
        "Date Range",
        options=all_months,
        value=(all_months[0], all_months[-1])
    )

    all_cats = sorted(products['category'].unique())
    sel_cats = st.multiselect(
        "Categories",
        options=all_cats,
        default=all_cats,
        placeholder="Select categories..."
    )
    if not sel_cats:
        sel_cats = all_cats

    st.markdown(f'<hr style="border-color:{T["border"]};margin:16px 0">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:11px;color:{T['text_muted']};line-height:1.8">
        📋 {len(orders):,} total orders<br>
        👤 {orders['buyer_id'].nunique():,} unique buyers<br>
        🏷️ {len(products):,} products<br>
        🗂️ {len(all_cats)} categories
    </div>""", unsafe_allow_html=True)


# ─── APPLY FILTERS ────────────────────────────────────────────────────────────
f_orders = orders[
    (orders['year_month'] >= sel_range[0]) &
    (orders['year_month'] <= sel_range[1])
]
f_monthly = monthly[
    (monthly['year_month'] >= sel_range[0]) &
    (monthly['year_month'] <= sel_range[1])
]
f_detail = detail[
    (detail['year_month'] >= sel_range[0]) &
    (detail['year_month'] <= sel_range[1]) &
    (detail['category'].isin(sel_cats))
]
f_paid    = f_orders[f_orders['is_paid']]
f_deliv   = f_orders[f_orders['is_delivered']]


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if "Executive" in page:
    st.markdown(f"""
    <div class="page-header">
        <h1>📊 Executive Overview</h1>
        <p>Revenue performance, funnel health, and growth trends · {sel_range[0]} to {sel_range[1]}</p>
    </div>""", unsafe_allow_html=True)

    # KPIs
    gmv      = f_paid['total'].sum()
    aov      = f_paid['total'].mean() if len(f_paid) else 0
    n_orders = len(f_orders)
    conv_pay = len(f_paid)/n_orders*100 if n_orders else 0
    conv_del = len(f_deliv)/len(f_paid)*100 if len(f_paid) else 0
    gmv_mom  = f_monthly.iloc[-1]['gmv_mom'] if len(f_monthly) >= 2 else None

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.markdown(kpi("Total GMV", fmt_rp(gmv), f"{len(f_paid):,} paid orders",
                              gmv_mom, T['primary']), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Total Orders", f"{n_orders:,}",
                              f"{len(f_orders)-len(f_paid):,} unpaid", accent=T['accent']), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Avg Order Value", fmt_rp(aov), "per paid order",
                              accent=T['success']), unsafe_allow_html=True)
    with c4: st.markdown(kpi("Payment Rate", f"{conv_pay:.1f}%",
                              f"{len(f_orders)-len(f_paid):,} not paid", accent=T['warning']), unsafe_allow_html=True)
    with c5: st.markdown(kpi("Delivery Rate", f"{conv_del:.1f}%",
                              f"{len(f_paid)-len(f_deliv):,} not delivered", accent=T['danger']), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 1: GMV Trend + Funnel
    col1, col2 = st.columns([3,2])

    with col1:
        st.markdown('<div class="sec-title">GMV Trend & Order Volume</div>', unsafe_allow_html=True)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=f_monthly['year_month'], y=f_monthly['gmv'],
            name="GMV", marker_color=T['primary'], opacity=0.85,
            marker_line_width=0), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=f_monthly['year_month'], y=f_monthly['orders_n'],
            name="Orders", mode='lines+markers',
            line=dict(color=T['accent'], width=2), marker=dict(size=5)),
            secondary_y=True)
        fig.update_layout(**base_layout(height=320))
        fig.update_xaxes(tickangle=-45, gridcolor=T['grid'])
        fig.update_yaxes(gridcolor=T['grid'], tickfont=dict(size=10), secondary_y=False)
        fig.update_yaxes(gridcolor='rgba(0,0,0,0)', tickfont=dict(size=10),
                         showgrid=False, secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-title">Order Conversion Funnel</div>', unsafe_allow_html=True)
        fig2 = go.Figure(go.Funnel(
            y=["Created", "Paid", "Delivered"],
            x=[len(f_orders), len(f_paid), len(f_deliv)],
            textinfo="percent previous+value",
            marker=dict(color=[T['primary'], T['success'], T['accent']]),
            textfont=dict(family="Inter", size=12)
        ))
        fig2.update_layout(**base_layout(height=320))
        st.plotly_chart(fig2, use_container_width=True)

        unpaid_rev = f_orders[~f_orders['is_paid']]['total'].sum()
        st.markdown(alert(f"⚠ {len(f_orders)-len(f_paid):,} orders belum dibayar · {fmt_rp(unpaid_rev)} at risk", "warn"), unsafe_allow_html=True)
        st.markdown(alert(f"📦 {len(f_paid)-len(f_deliv):,} orders paid tapi belum dikirim", "info"), unsafe_allow_html=True)

    # Row 2: MoM Growth + Day of Week
    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="sec-title">Month-over-Month GMV Growth (%)</div>', unsafe_allow_html=True)
        mom = f_monthly.dropna(subset=['gmv_mom'])
        fig3 = go.Figure(go.Bar(
            x=mom['year_month'], y=mom['gmv_mom'],
            marker_color=[T['success'] if v >= 0 else T['danger'] for v in mom['gmv_mom']],
            marker_line_width=0,
            text=[f"{v:+.1f}%" for v in mom['gmv_mom']],
            textposition='outside',
            textfont=dict(size=10)
        ))
        fig3.add_hline(y=0, line_color=T['border'], line_width=1)
        fig3.update_layout(**base_layout(height=300))
        fig3.update_xaxes(tickangle=-45)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="sec-title">Orders by Day of Week</div>', unsafe_allow_html=True)
        dow_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        dow_cnt = f_orders.groupby('dow')['order_id'].count().reindex(dow_order, fill_value=0)
        fig4 = go.Figure(go.Bar(
            x=dow_order,
            y=dow_cnt.values,
            marker_color=T['primary'],
            marker_line_width=0,
            opacity=0.85,
            text=dow_cnt.values,
            textposition='outside',
            textfont=dict(size=10)
        ))
        fig4.update_layout(**base_layout(height=300))
        fig4.update_xaxes(tickangle=-30)
        st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PRODUCT INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
elif "Product" in page:
    st.markdown(f"""
    <div class="page-header">
        <h1>📦 Product Intelligence</h1>
        <p>Category performance, top products, and revenue distribution · {sel_range[0]} to {sel_range[1]}</p>
    </div>""", unsafe_allow_html=True)

    # Category Revenue
    cat_rev = (f_detail.groupby('category')['line_revenue']
               .sum().sort_values(ascending=False).reset_index())
    cat_rev.columns = ['category','revenue']
    cat_rev['cum_pct'] = cat_rev['revenue'].cumsum() / cat_rev['revenue'].sum() * 100
    cat_rev['share']   = cat_rev['revenue'] / cat_rev['revenue'].sum() * 100

    # KPIs
    c1,c2,c3,c4 = st.columns(4)
    top_cat = cat_rev.iloc[0]
    with c1: st.markdown(kpi("Total Revenue", fmt_rp(cat_rev['revenue'].sum()),
                              f"{len(sel_cats)} categories", accent=T['primary']), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Top Category", top_cat['category'],
                              fmt_rp(top_cat['revenue']), accent=T['accent']), unsafe_allow_html=True)
    with c3:
        top3_share = cat_rev.head(3)['share'].sum()
        st.markdown(kpi("Top 3 Share", f"{top3_share:.1f}%",
                         "of total revenue", accent=T['success']), unsafe_allow_html=True)
    with c4:
        n_products = f_detail['product_id'].nunique()
        st.markdown(kpi("Active Products", f"{n_products:,}",
                         "in filtered period", accent=T['warning']), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Pareto + Pie
    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown('<div class="sec-title">Category Revenue — Pareto Analysis (80/20)</div>', unsafe_allow_html=True)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        bar_colors = [T['primary'] if p <= 80 else T['text_muted'] for p in cat_rev['cum_pct']]
        fig.add_trace(go.Bar(
            x=cat_rev['category'], y=cat_rev['revenue'],
            name="Revenue", marker_color=bar_colors,
            marker_line_width=0, opacity=0.9,
            text=[fmt_rp(v) for v in cat_rev['revenue']],
            textposition='outside', textfont=dict(size=9)
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=cat_rev['category'], y=cat_rev['cum_pct'],
            name="Cumulative %", mode='lines+markers',
            line=dict(color=T['warning'], width=2), marker=dict(size=6)
        ), secondary_y=True)
        fig.add_hline(y=80, line_color=T['danger'], line_dash='dash',
                      line_width=1, secondary_y=True)
        fig.update_layout(**base_layout(height=360))
        fig.update_xaxes(tickangle=-35, gridcolor=T['grid'])
        fig.update_yaxes(gridcolor=T['grid'], secondary_y=False, tickfont=dict(size=10))
        fig.update_yaxes(showgrid=False, secondary_y=True, range=[0,110],
                         tickfont=dict(size=10), ticksuffix="%")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-title">Revenue Share by Category</div>', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=cat_rev['category'],
            values=cat_rev['revenue'],
            hole=0.5,
            marker=dict(colors=T['cats'],
                        line=dict(color=T['bg'], width=2)),
            textinfo='percent',
            textfont=dict(family="Inter", size=11),
        ))
        fig_pie.add_annotation(
            text=f"<b>{fmt_rp(cat_rev['revenue'].sum())}</b>",
            x=0.5, y=0.5,
            font=dict(size=12, color=T['text']),
            showarrow=False
        )
        fig_pie.update_layout(**base_layout(height=360))
        st.plotly_chart(fig_pie, use_container_width=True)

    # Top 15 Products + Category Trend
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="sec-title">Top 15 Products by Revenue</div>', unsafe_allow_html=True)
        prod_rev = (f_detail.groupby('desc_product')
                   .agg(revenue=('line_revenue','sum'), qty=('quantity','sum'))
                   .sort_values('revenue', ascending=False).head(15).reset_index())
        prod_rev['desc_product'] = prod_rev['desc_product'].str.strip().str[:28]
        fig5 = go.Figure(go.Bar(
            x=prod_rev['revenue'],
            y=prod_rev['desc_product'],
            orientation='h',
            marker_color=T['accent'],
            marker_line_width=0,
            opacity=0.85,
            text=[fmt_rp(v) for v in prod_rev['revenue']],
            textposition='outside',
            textfont=dict(size=9)
        ))
        fig5.update_layout(**base_layout(height=460))
        fig5.update_yaxes(autorange='reversed', gridcolor='rgba(0,0,0,0)',
                          tickfont=dict(size=10))
        fig5.update_xaxes(gridcolor=T['grid'])
        st.plotly_chart(fig5, use_container_width=True)

    with col4:
        st.markdown('<div class="sec-title">Top 5 Categories — Monthly Trend</div>', unsafe_allow_html=True)
        top5 = cat_rev.head(5)['category'].tolist()
        cat_monthly = (f_detail[f_detail['category'].isin(top5)]
                       .groupby(['year_month','category'])['line_revenue']
                       .sum().reset_index())
        fig6 = px.line(cat_monthly, x='year_month', y='line_revenue',
                       color='category', markers=True,
                       color_discrete_sequence=T['cats'])
        fig6.update_traces(line_width=2, marker_size=5)
        fig6.update_layout(**base_layout(height=460))
        fig6.update_xaxes(tickangle=-45, gridcolor=T['grid'])
        fig6.update_yaxes(gridcolor=T['grid'])
        st.plotly_chart(fig6, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — CUSTOMER ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif "Customer" in page:
    st.markdown(f"""
    <div class="page-header">
        <h1>👤 Customer Analytics</h1>
        <p>RFM segmentation, cohort retention, and customer lifetime value analysis</p>
    </div>""", unsafe_allow_html=True)

    seg_counts = rfm['segment'].value_counts()
    seg_colors = {
        'Champions':          T['warning'],
        'Loyal':              T['primary'],
        'Potential Loyalist': T['accent'],
        'New Customers':      T['success'],
        'At Risk':            '#FB923C',
        'Cannot Lose Them':   T['danger'],
        'Churned':            T['text_muted'],
    }

    # KPIs
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi("Champions 🏆", f"{seg_counts.get('Champions',0):,}",
                              "Highest value users", accent=T['warning']), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Loyal Users", f"{seg_counts.get('Loyal',0):,}",
                              "Regular buyers", accent=T['primary']), unsafe_allow_html=True)
    with c3: st.markdown(kpi("At Risk ⚠", f"{seg_counts.get('At Risk',0):,}",
                              "Need win-back", accent='#FB923C'), unsafe_allow_html=True)
    with c4: st.markdown(kpi("Churned", f"{seg_counts.get('Churned',0):,}",
                              "Inactive users", accent=T['text_muted']), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Cohort Matrix
    st.markdown('<div class="sec-title">Cohort Retention Matrix — % Users Returning Each Month</div>', unsafe_allow_html=True)
    pivot = cohort.pivot(index='cohort', columns='period_n', values='retention')
    pivot = pivot.iloc[:, :13]
    pivot.index = pivot.index.astype(str)

    fig_coh = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[f"M+{c}" for c in pivot.columns],
        y=pivot.index,
        colorscale=[
            [0.0, T['bg']],
            [0.3, T['primary']+'44'],
            [0.6, T['primary']+'AA'],
            [1.0, T['primary']],
        ],
        text=np.where(np.isnan(pivot.values), "", np.round(pivot.values, 0).astype(int).astype(str) + "%"),
        texttemplate="%{text}",
        textfont=dict(size=9, family="Inter"),
        showscale=True,
        colorbar=dict(
            title="Retention",
            tickfont=dict(family="Inter", size=10),
            ticksuffix="%"
        )
    ))
    fig_coh.update_layout(**base_layout(height=500))
    st.plotly_chart(fig_coh, use_container_width=True)

    # RFM Scatter + Segment Bar
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown('<div class="sec-title">RFM Landscape — Recency vs Frequency (bubble = spend)</div>', unsafe_allow_html=True)
        sample = rfm.sample(min(1500, len(rfm)), random_state=42)
        fig_rfm = px.scatter(
            sample, x='recency', y='frequency',
            size='monetary', color='segment',
            color_discrete_map=seg_colors,
            size_max=25, opacity=0.7,
            hover_data={'monetary': ':,.0f', 'recency': True, 'frequency': True}
        )
        fig_rfm.update_traces(marker_line_width=0)
        fig_rfm.update_layout(**base_layout(height=380))
        fig_rfm.update_xaxes(title="Recency (days)", gridcolor=T['grid'])
        fig_rfm.update_yaxes(title="Frequency (orders)", gridcolor=T['grid'])
        st.plotly_chart(fig_rfm, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-title">Users per Segment</div>', unsafe_allow_html=True)
        seg_df = rfm['segment'].value_counts().reset_index()
        seg_df.columns = ['segment','count']
        seg_df['color'] = seg_df['segment'].map(seg_colors)
        fig_seg = go.Figure(go.Bar(
            x=seg_df['count'],
            y=seg_df['segment'],
            orientation='h',
            marker_color=seg_df['color'].tolist(),
            marker_line_width=0,
            opacity=0.85,
            text=seg_df['count'],
            textposition='outside',
            textfont=dict(size=10)
        ))
        fig_seg.update_layout(**base_layout(height=380))
        fig_seg.update_yaxes(autorange='reversed', gridcolor='rgba(0,0,0,0)',
                             tickfont=dict(size=11))
        fig_seg.update_xaxes(gridcolor=T['grid'])
        st.plotly_chart(fig_seg, use_container_width=True)

    # Segment Table
    st.markdown('<div class="sec-title">Segment Strategy Summary</div>', unsafe_allow_html=True)
    strategies = {
        'Champions':          '🎯 Reward & upsell — highest LTV, early access to new products',
        'Loyal':              '💌 Loyalty program, tier upgrade nudge, bundle offers',
        'Potential Loyalist': '🔁 Frequency push, targeted promo, referral incentive',
        'New Customers':      '🚀 Onboarding flow, educational content, first re-order promo',
        'At Risk':            '⚡ Win-back campaign, "we miss you" email, exclusive discount',
        'Cannot Lose Them':   '🚨 Urgent personal outreach, VIP treatment, major incentive',
        'Churned':            '💀 Last-chance offer or suppress from expensive channels',
    }
    seg_tbl = (rfm.groupby('segment')
               .agg(users=('buyer_id','count'),
                    avg_recency=('recency','mean'),
                    avg_freq=('frequency','mean'),
                    total_rev=('monetary','sum'),
                    avg_rev=('monetary','mean'))
               .reset_index())
    seg_tbl['Avg Recency']  = seg_tbl['avg_recency'].round(0).astype(int).astype(str) + "d"
    seg_tbl['Avg Frequency'] = seg_tbl['avg_freq'].round(1)
    seg_tbl['Total Revenue'] = seg_tbl['total_rev'].apply(fmt_rp)
    seg_tbl['Avg Revenue']   = seg_tbl['avg_rev'].apply(fmt_rp)
    seg_tbl['Strategy']      = seg_tbl['segment'].map(strategies)
    st.dataframe(
        seg_tbl[['segment','users','Avg Recency','Avg Frequency','Total Revenue','Strategy']]
        .rename(columns={'segment':'Segment','users':'Users'}),
        use_container_width=True, hide_index=True
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — OPERATIONS & SLA
# ══════════════════════════════════════════════════════════════════════════════
elif "Operations" in page:
    st.markdown(f"""
    <div class="page-header">
        <h1>🚚 Operations & SLA</h1>
        <p>Payment lag, delivery performance, geographic bottlenecks · {sel_range[0]} to {sel_range[1]}</p>
    </div>""", unsafe_allow_html=True)

    paid_f  = f_orders[f_orders['is_paid']]
    deliv_f = f_orders[f_orders['is_delivered']]

    avg_pay = paid_f['payment_lag'].mean()
    med_pay = paid_f['payment_lag'].median()
    avg_del = deliv_f['delivery_lag'].mean()
    med_del = deliv_f['delivery_lag'].median()
    pct_slow_pay = (paid_f['payment_lag'] > 7).mean() * 100
    pct_slow_del = (deliv_f['delivery_lag'] > 7).mean() * 100

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: st.markdown(kpi("Avg Payment Lag", f"{avg_pay:.1f}d", "target < 7d",
                              accent=T['primary']), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Median Pay Lag", f"{med_pay:.0f}d", "50th percentile",
                              accent=T['accent']), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Avg Delivery Lag", f"{avg_del:.1f}d", "target < 7d",
                              accent=T['success']), unsafe_allow_html=True)
    with c4: st.markdown(kpi("Median Del Lag", f"{med_del:.0f}d", "50th percentile",
                              accent=T['warning']), unsafe_allow_html=True)
    with c5: st.markdown(kpi("Slow Payers >7d", f"{pct_slow_pay:.1f}%", "of paid orders",
                              accent='#FB923C'), unsafe_allow_html=True)
    with c6: st.markdown(kpi("Slow Delivery >7d", f"{pct_slow_del:.1f}%", "of deliveries",
                              accent=T['danger']), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Distributions
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sec-title">Payment Lag Distribution</div>', unsafe_allow_html=True)
        fig1 = go.Figure(go.Histogram(
            x=paid_f['payment_lag'].dropna(), nbinsx=15,
            marker_color=T['primary'], marker_line_width=0, opacity=0.85,
            name="Payment Lag"
        ))
        fig1.add_vline(x=avg_pay, line_color=T['warning'], line_dash='dash',
                       annotation_text=f"Avg: {avg_pay:.1f}d",
                       annotation_font_color=T['warning'])
        fig1.add_vline(x=7, line_color=T['danger'], line_dash='dot',
                       annotation_text="SLA: 7d",
                       annotation_font_color=T['danger'])
        fig1.update_layout(**base_layout("Days from Order to Payment", height=300))
        fig1.update_xaxes(title="Days", gridcolor=T['grid'])
        fig1.update_yaxes(title="Count", gridcolor=T['grid'])
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-title">Delivery Lag Distribution</div>', unsafe_allow_html=True)
        fig2 = go.Figure(go.Histogram(
            x=deliv_f['delivery_lag'].dropna(), nbinsx=15,
            marker_color=T['success'], marker_line_width=0, opacity=0.85,
            name="Delivery Lag"
        ))
        fig2.add_vline(x=avg_del, line_color=T['warning'], line_dash='dash',
                       annotation_text=f"Avg: {avg_del:.1f}d",
                       annotation_font_color=T['warning'])
        fig2.add_vline(x=7, line_color=T['danger'], line_dash='dot',
                       annotation_text="SLA: 7d",
                       annotation_font_color=T['danger'])
        fig2.update_layout(**base_layout("Days from Payment to Delivery", height=300))
        fig2.update_xaxes(title="Days", gridcolor=T['grid'])
        fig2.update_yaxes(title="Count", gridcolor=T['grid'])
        st.plotly_chart(fig2, use_container_width=True)

    # SLA Monthly Trend
    st.markdown('<div class="sec-title">SLA Performance Trend — Monthly Average</div>', unsafe_allow_html=True)
    sla_m = (f_orders.groupby('year_month')
             .agg(pay_lag=('payment_lag','mean'), del_lag=('delivery_lag','mean'))
             .reset_index())
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=sla_m['year_month'], y=sla_m['pay_lag'],
        name="Payment Lag", mode='lines+markers',
        line=dict(color=T['primary'], width=2), marker=dict(size=6)))
    fig3.add_trace(go.Scatter(
        x=sla_m['year_month'], y=sla_m['del_lag'],
        name="Delivery Lag", mode='lines+markers',
        line=dict(color=T['success'], width=2), marker=dict(size=6)))
    fig3.add_hline(y=7, line_color=T['danger'], line_dash='dash',
                   annotation_text="SLA Target (7d)", annotation_font_color=T['danger'])
    fig3.update_layout(**base_layout("Average Lag per Month (days)", height=300))
    fig3.update_xaxes(tickangle=-45, gridcolor=T['grid'])
    fig3.update_yaxes(title="Days", gridcolor=T['grid'])
    st.plotly_chart(fig3, use_container_width=True)

    # Geographic + Bottleneck
    col3, col4 = st.columns([2,1])
    with col3:
        st.markdown('<div class="sec-title">Orders by Postal Code Prefix (Top 20)</div>', unsafe_allow_html=True)
        geo = f_orders.copy()
        geo['prefix'] = geo['kodepos'].astype(str).str[:2]
        geo_agg = (geo.groupby('prefix')
                   .agg(orders=('order_id','count'),
                        avg_del=('delivery_lag','mean'))
                   .reset_index().sort_values('orders', ascending=False).head(20))

        bar_colors = [T['danger'] if (d and d > 7) else T['success']
                      for d in geo_agg['avg_del'].fillna(0)]
        fig4 = go.Figure(go.Bar(
            x=geo_agg['prefix'], y=geo_agg['orders'],
            marker_color=bar_colors, marker_line_width=0, opacity=0.85,
            text=geo_agg['orders'], textposition='outside', textfont=dict(size=9)
        ))
        fig4.update_layout(**base_layout("🔴 = avg delivery > 7d (SLA breach)", height=320))
        fig4.update_xaxes(gridcolor=T['grid'])
        fig4.update_yaxes(gridcolor=T['grid'])
        st.plotly_chart(fig4, use_container_width=True)

    with col4:
        st.markdown('<div class="sec-title">Bottleneck Alerts</div>', unsafe_allow_html=True)
        breach = geo_agg[geo_agg['avg_del'] > 7].sort_values('avg_del', ascending=False)
        if len(breach):
            for _, row in breach.iterrows():
                st.markdown(alert(
                    f"🚨 Postal {row['prefix']}xx — {row['avg_del']:.1f}d avg · {row['orders']:,} orders",
                    "danger"), unsafe_allow_html=True)
        else:
            st.markdown(alert("✅ Semua zona dalam SLA target", "success"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="sec-title">Unpaid Order Aging</div>', unsafe_allow_html=True)
        unpaid = f_orders[f_orders['paid_at'].isna()].copy()
        if len(unpaid):
            unpaid['age'] = (pd.Timestamp.now() - unpaid['created_at']).dt.days
            buckets = pd.cut(unpaid['age'], bins=[0,3,7,14,30,9999],
                             labels=['0-3d','4-7d','8-14d','15-30d','30+d'])
            age_dist = buckets.value_counts().sort_index()
            fig5 = go.Figure(go.Bar(
                x=age_dist.index.astype(str), y=age_dist.values,
                marker_color=[T['success'], T['warning'], '#FB923C', T['danger'], '#7F1D1D'],
                marker_line_width=0,
                text=age_dist.values, textposition='outside', textfont=dict(size=11)
            ))
            fig5.update_layout(**base_layout(height=260))
            fig5.update_xaxes(gridcolor='rgba(0,0,0,0)')
            fig5.update_yaxes(gridcolor=T['grid'])
            st.plotly_chart(fig5, use_container_width=True)


# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;font-size:11px;color:{T['text_muted']};
            padding:20px 0 8px;border-top:1px solid {T['border']};margin-top:24px">
    E-Commerce Analytics Dashboard · Jan 2019 – May 2020 · Built with Streamlit & Plotly
</div>""", unsafe_allow_html=True)
