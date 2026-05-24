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

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# ─── THEME ────────────────────────────────────────────────────────────────────
def get_theme():
    if st.session_state.dark_mode:
        return {
            "bg":         "#0F1117",
            "card":       "#1E2130",
            "card2":      "#262B3D",
            "text":       "#F0F2F6",
            "muted":      "#8B92A5",
            "border":     "#2D3147",
            "primary":    "#4F8EF7",
            "success":    "#2DD4BF",
            "warning":    "#FBBF24",
            "danger":     "#F87171",
            "accent":     "#A78BFA",
            "orange":     "#FB923C",
            "grid":       "#2D3147",
            "plot_bg":    "rgba(0,0,0,0)",
            "cats": ["#4F8EF7","#2DD4BF","#FBBF24","#F87171","#A78BFA",
                     "#34D399","#FB923C","#60A5FA","#F472B6","#38BDF8",
                     "#C084FC","#FCD34D"],
            # cohort colorscale — no alpha hex, use rgb
            "coh_scale": [
                [0.0,  "rgb(15,17,23)"],
                [0.15, "rgb(30,40,80)"],
                [0.35, "rgb(40,80,160)"],
                [0.6,  "rgb(60,120,220)"],
                [1.0,  "rgb(79,142,247)"],
            ],
        }
    else:
        return {
            "bg":         "#F8FAFC",
            "card":       "#FFFFFF",
            "card2":      "#F1F5F9",
            "text":       "#0F172A",
            "muted":      "#64748B",
            "border":     "#E2E8F0",
            "primary":    "#3B82F6",
            "success":    "#0D9488",
            "warning":    "#D97706",
            "danger":     "#DC2626",
            "accent":     "#7C3AED",
            "orange":     "#EA580C",
            "grid":       "#E2E8F0",
            "plot_bg":    "rgba(0,0,0,0)",
            "cats": ["#3B82F6","#0D9488","#D97706","#DC2626","#7C3AED",
                     "#059669","#EA580C","#2563EB","#DB2777","#0284C7",
                     "#9333EA","#CA8A04"],
            "coh_scale": [
                [0.0,  "rgb(248,250,252)"],
                [0.15, "rgb(219,234,254)"],
                [0.35, "rgb(147,197,253)"],
                [0.6,  "rgb(96,165,250)"],
                [1.0,  "rgb(59,130,246)"],
            ],
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

/* Fix: white mode full background */
.main, .block-container, [data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"] {{
    background-color: {T['bg']} !important;
}}

[data-testid="stSidebar"] {{
    background-color: {T['card']} !important;
    border-right: 1px solid {T['border']} !important;
}}
[data-testid="stSidebar"] * {{ color: {T['text']} !important; }}
[data-testid="stSidebar"] .stRadio label {{ color: {T['text']} !important; }}

.block-container {{ padding: 1.5rem 2rem !important; }}
.stPlotlyChart {{ border-radius: 10px; }}

/* KPI card */
.kpi-card {{
    background: {T['card']};
    border: 1px solid {T['border']};
    border-radius: 10px;
    padding: 18px 20px;
    margin-bottom: 12px;
    border-left: 3px solid var(--ac, {T['primary']});
}}
.kpi-label {{
    font-size: 11px;
    font-weight: 600;
    color: {T['muted']};
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}}
.kpi-value {{
    font-size: 24px;
    font-weight: 700;
    color: {T['text']};
    line-height: 1.15;
}}
.kpi-sub  {{ font-size: 12px; color: {T['muted']}; margin-top: 3px; }}
.kpi-up   {{ font-size: 12px; color: {T['success']}; margin-top: 3px; }}
.kpi-down {{ font-size: 12px; color: {T['danger']};  margin-top: 3px; }}

/* Section title */
.sec-title {{
    font-size: 12px;
    font-weight: 600;
    color: {T['muted']};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 0 0 10px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid {T['border']};
}}

/* Alert */
.alert {{
    border-radius: 8px;
    padding: 9px 13px;
    font-size: 12px;
    font-weight: 500;
    margin: 5px 0;
    border-left: 3px solid;
}}
.alert-warn    {{ background:rgba(251,191,36,0.1);  border-color:{T['warning']}; color:{T['warning']}; }}
.alert-danger  {{ background:rgba(248,113,113,0.1); border-color:{T['danger']};  color:{T['danger']};  }}
.alert-success {{ background:rgba(45,212,191,0.1);  border-color:{T['success']}; color:{T['success']}; }}
.alert-info    {{ background:rgba(79,142,247,0.1);  border-color:{T['primary']}; color:{T['primary']}; }}

/* Page header */
.page-hdr {{ margin-bottom: 18px; padding-bottom: 14px; border-bottom: 1px solid {T['border']}; }}
.page-hdr h1 {{ font-size: 22px; font-weight: 700; color: {T['text']}; margin: 0 0 3px 0; }}
.page-hdr p  {{ font-size: 12px; color: {T['muted']}; margin: 0; }}

/* Sidebar brand */
.brand {{ padding: 4px 0 12px; }}
.brand-tag  {{ font-size: 10px; font-weight: 600; color: {T['primary']}; letter-spacing: 2px; text-transform: uppercase; }}
.brand-name {{ font-size: 18px; font-weight: 700; color: {T['text']}; margin-top: 2px; line-height: 1.25; }}
.brand-sub  {{ font-size: 11px; color: {T['muted']}; margin-top: 3px; }}

/* Toggle button — small */
div[data-testid="stButton"] button {{
    padding: 4px 10px !important;
    font-size: 13px !important;
    border-radius: 6px !important;
    height: auto !important;
    min-height: 0 !important;
    background: {T['card2']} !important;
    border: 1px solid {T['border']} !important;
    color: {T['text']} !important;
}}

div[data-testid="metric-container"] {{ display: none; }}
hr {{ border-color: {T['border']} !important; margin: 12px 0 !important; }}
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ──────────────────────────────────────────────────────────────────
def fmt_rp(x):
    if x >= 1e12: return f"Rp {x/1e12:.2f}T"
    if x >= 1e9:  return f"Rp {x/1e9:.1f}B"
    if x >= 1e6:  return f"Rp {x/1e6:.1f}M"
    return f"Rp {x:,.0f}"

def kpi(label, value, sub="", delta=None, ac=None):
    ac = ac or T['primary']
    d_html = ""
    if delta is not None:
        cls = "kpi-up" if delta >= 0 else "kpi-down"
        icon = "▲" if delta >= 0 else "▼"
        d_html = f'<div class="{cls}">{icon} {abs(delta):.1f}% MoM</div>'
    s_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return f"""<div class="kpi-card" style="--ac:{ac}; border-left-color:{ac}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {s_html}{d_html}
    </div>"""

def alert(msg, kind="info"):
    return f'<div class="alert alert-{kind}">{msg}</div>'

def BL(title="", h=360):
    """Base plotly layout — no nested yaxis/xaxis keys"""
    return dict(
        paper_bgcolor=T['plot_bg'],
        plot_bgcolor=T['plot_bg'],
        font=dict(family="Inter", color=T['text'], size=12),
        title=dict(text=title, font=dict(size=12, color=T['muted']), x=0),
        margin=dict(l=10, r=10, t=36, b=10),
        height=h,
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=T['border'],
                    borderwidth=1, font=dict(size=11)),
    )

def apply_axes(fig, x_angle=0, secondary=False):
    """Apply grid/tick styling via update_xaxes / update_yaxes"""
    fig.update_xaxes(gridcolor=T['grid'], zerolinecolor=T['grid'],
                     tickfont=dict(size=10), tickangle=x_angle,
                     linecolor=T['border'])
    fig.update_yaxes(gridcolor=T['grid'], zerolinecolor=T['grid'],
                     tickfont=dict(size=10), linecolor=T['border'])
    return fig


# ─── DATA ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    orders = pd.read_csv('orders.csv', sep=';',
                         parse_dates=['created_at','paid_at','delivery_at'])
    od     = pd.read_csv('order_details.csv', sep=';')
    prods  = pd.read_csv('products.csv', sep=';')
    users  = pd.read_csv('users.csv', sep=';', on_bad_lines='skip')

    orders['is_paid']      = orders['paid_at'].notna()
    orders['is_delivered'] = orders['delivery_at'].notna()
    orders['payment_lag']  = (orders['paid_at'] - orders['created_at']).dt.days
    orders['delivery_lag'] = (orders['delivery_at'] - orders['paid_at']).dt.days
    orders['year_month']   = orders['created_at'].dt.to_period('M').astype(str)
    orders['dow']          = orders['created_at'].dt.day_name()

    detail = (od.merge(prods, on='product_id', how='left')
                .merge(orders[['order_id','created_at','buyer_id','is_paid',
                               'is_delivered','year_month','total']],
                       on='order_id', how='left'))
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

    # RFM
    snapshot = orders['created_at'].max() + pd.Timedelta(days=1)
    rfm = (paid.groupby('buyer_id')
           .agg(recency=('created_at', lambda x: (snapshot - x.max()).days),
                frequency=('order_id','count'),
                monetary=('total','sum'))
           .reset_index())
    rfm['R'] = pd.qcut(rfm['recency'],   5, labels=[5,4,3,2,1], duplicates='drop').astype(int)
    rfm['F'] = pd.qcut(rfm['frequency'], 5, labels=[1,2,3,4,5], duplicates='drop').astype(int)
    rfm['M'] = pd.qcut(rfm['monetary'],  5, labels=[1,2,3,4,5], duplicates='drop').astype(int)

    def seg(r):
        rv,f,m = r['R'],r['F'],r['M']
        if rv>=4 and f>=4 and m>=4: return 'Champions'
        elif rv>=3 and f>=3:        return 'Loyal'
        elif rv>=4 and f<=2:        return 'New Customers'
        elif rv>=3 and f>=2:        return 'Potential Loyalist'
        elif rv==2 and f>=2:        return 'At Risk'
        elif rv<=2 and f>=3:        return 'Cannot Lose Them'
        else:                       return 'Churned'
    rfm['segment'] = rfm.apply(seg, axis=1)

    # Cohort
    orders['cohort'] = (orders.groupby('buyer_id')['created_at']
                              .transform('min').dt.to_period('M').astype(str))
    orders['order_period'] = orders['created_at'].dt.to_period('M').astype(str)
    orders['period_n'] = orders.apply(
        lambda r: (pd.Period(r['order_period'],'M') - pd.Period(r['cohort'],'M')).n, axis=1)

    coh = orders.groupby(['cohort','period_n'])['buyer_id'].nunique().reset_index()
    sizes = coh[coh['period_n']==0].set_index('cohort')['buyer_id']
    coh['retention'] = coh.apply(
        lambda r: r['buyer_id'] / sizes.get(r['cohort'], 1) * 100, axis=1)

    return dict(orders=orders, detail=detail, products=prods,
                monthly=monthly, rfm=rfm, cohort=coh)

with st.spinner("Loading..."):
    D = load_data()

orders  = D['orders']
detail  = D['detail']
prods   = D['products']
monthly = D['monthly']
rfm     = D['rfm']
cohort  = D['cohort']


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    col_a, col_b = st.columns([5, 2])
    with col_a:
        st.markdown(f"""
        <div class="brand">
            <div class="brand-tag">Analytics</div>
            <div class="brand-name">E-Commerce<br>Dashboard</div>
            <div class="brand-sub">Jan 2019 – May 2020</div>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown("<div style='margin-top:14px'></div>", unsafe_allow_html=True)
        icon = "🌙" if st.session_state.dark_mode else "☀️"
        if st.button(icon, help="Toggle dark/light mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

    st.markdown("---")
    st.markdown(f'<div style="font-size:11px;font-weight:600;color:{T["muted"]};text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">Navigation</div>', unsafe_allow_html=True)
    page = st.radio("", [
        "📊  Executive Overview",
        "📦  Product Intelligence",
        "👤  Customer Analytics",
        "🚚  Operations & SLA",
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f'<div style="font-size:11px;font-weight:600;color:{T["muted"]};text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">Filters</div>', unsafe_allow_html=True)

    all_months = sorted(orders['year_month'].unique())
    sel_range = st.select_slider("Date Range", options=all_months,
                                  value=(all_months[0], all_months[-1]))

    all_cats = sorted(prods['category'].unique())
    sel_cats = st.multiselect("Categories", options=all_cats, default=all_cats,
                               placeholder="Select categories...")
    if not sel_cats:
        sel_cats = all_cats

    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:11px;color:{T['muted']};line-height:2">
        📋 {len(orders):,} total orders<br>
        👤 {orders['buyer_id'].nunique():,} unique buyers<br>
        🏷️ {len(prods):,} products<br>
        🗂️ {len(all_cats)} categories
    </div>""", unsafe_allow_html=True)


# ─── FILTERS ──────────────────────────────────────────────────────────────────
fo = orders[(orders['year_month'] >= sel_range[0]) &
            (orders['year_month'] <= sel_range[1])]
fm = monthly[(monthly['year_month'] >= sel_range[0]) &
             (monthly['year_month'] <= sel_range[1])]
fd = detail[(detail['year_month'] >= sel_range[0]) &
            (detail['year_month'] <= sel_range[1]) &
            (detail['category'].isin(sel_cats))]
fp = fo[fo['is_paid']]
fv = fo[fo['is_delivered']]


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — EXECUTIVE OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if "Executive" in page:
    st.markdown(f"""<div class="page-hdr">
        <h1>📊 Executive Overview</h1>
        <p>Revenue performance, funnel health, and growth trends · {sel_range[0]} to {sel_range[1]}</p>
    </div>""", unsafe_allow_html=True)

    gmv     = fp['total'].sum()
    aov     = fp['total'].mean() if len(fp) else 0
    n       = len(fo)
    cpay    = len(fp)/n*100 if n else 0
    cdel    = len(fv)/len(fp)*100 if len(fp) else 0
    mom     = fm.iloc[-1]['gmv_mom'] if len(fm) >= 2 else None

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.markdown(kpi("Total GMV", fmt_rp(gmv), f"{len(fp):,} paid orders", mom, T['primary']), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Total Orders", f"{n:,}", f"{n-len(fp):,} unpaid", ac=T['accent']), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Avg Order Value", fmt_rp(aov), "per paid order", ac=T['success']), unsafe_allow_html=True)
    with c4: st.markdown(kpi("Payment Rate", f"{cpay:.1f}%", f"{n-len(fp):,} not paid", ac=T['warning']), unsafe_allow_html=True)
    with c5: st.markdown(kpi("Delivery Rate", f"{cdel:.1f}%", f"{len(fp)-len(fv):,} not delivered", ac=T['danger']), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown('<div class="sec-title">GMV Trend & Order Volume</div>', unsafe_allow_html=True)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(x=fm['year_month'], y=fm['gmv'], name="GMV",
                             marker_color=T['primary'], opacity=0.85, marker_line_width=0), secondary_y=False)
        fig.add_trace(go.Scatter(x=fm['year_month'], y=fm['orders_n'], name="Orders",
                                 mode='lines+markers', line=dict(color=T['accent'], width=2),
                                 marker=dict(size=5)), secondary_y=True)
        fig.update_layout(**BL(h=320))
        fig.update_xaxes(tickangle=-45, gridcolor=T['grid'], tickfont=dict(size=10))
        fig.update_yaxes(gridcolor=T['grid'], tickfont=dict(size=10), secondary_y=False)
        fig.update_yaxes(showgrid=False, tickfont=dict(size=10), secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-title">Order Conversion Funnel</div>', unsafe_allow_html=True)
        fig2 = go.Figure(go.Funnel(
            y=["Created","Paid","Delivered"],
            x=[len(fo), len(fp), len(fv)],
            textinfo="percent previous+value",
            marker=dict(color=[T['primary'], T['success'], T['accent']]),
            textfont=dict(family="Inter", size=12)
        ))
        fig2.update_layout(**BL(h=260))
        st.plotly_chart(fig2, use_container_width=True)
        unpaid_rev = fo[~fo['is_paid']]['total'].sum()
        st.markdown(alert(f"⚠ {n-len(fp):,} orders belum dibayar · {fmt_rp(unpaid_rev)} at risk", "warn"), unsafe_allow_html=True)
        st.markdown(alert(f"📦 {len(fp)-len(fv):,} paid orders belum dikirim", "info"), unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="sec-title">Month-over-Month GMV Growth (%)</div>', unsafe_allow_html=True)
        mom_df = fm.dropna(subset=['gmv_mom'])
        fig3 = go.Figure(go.Bar(
            x=mom_df['year_month'], y=mom_df['gmv_mom'],
            marker_color=[T['success'] if v>=0 else T['danger'] for v in mom_df['gmv_mom']],
            marker_line_width=0,
            text=[f"{v:+.1f}%" for v in mom_df['gmv_mom']],
            textposition='outside', textfont=dict(size=9)
        ))
        fig3.add_hline(y=0, line_color=T['border'], line_width=1)
        fig3.update_layout(**BL(h=300))
        fig3.update_xaxes(tickangle=-45, gridcolor=T['grid'], tickfont=dict(size=10))
        fig3.update_yaxes(gridcolor=T['grid'], tickfont=dict(size=10))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="sec-title">Orders by Day of Week</div>', unsafe_allow_html=True)
        dow_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        dow_cnt = fo.groupby('dow')['order_id'].count().reindex(dow_order, fill_value=0)
        fig4 = go.Figure(go.Bar(
            x=dow_order, y=dow_cnt.values,
            marker_color=T['primary'], marker_line_width=0, opacity=0.85,
            text=dow_cnt.values, textposition='outside', textfont=dict(size=10)
        ))
        fig4.update_layout(**BL(h=300))
        fig4.update_xaxes(tickangle=-30, gridcolor=T['grid'], tickfont=dict(size=10))
        fig4.update_yaxes(gridcolor=T['grid'], tickfont=dict(size=10))
        st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — PRODUCT INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
elif "Product" in page:
    st.markdown(f"""<div class="page-hdr">
        <h1>📦 Product Intelligence</h1>
        <p>Category performance, top products, and revenue distribution · {sel_range[0]} to {sel_range[1]}</p>
    </div>""", unsafe_allow_html=True)

    cat_rev = (fd.groupby('category')['line_revenue']
               .sum().sort_values(ascending=False).reset_index())
    cat_rev.columns = ['category','revenue']
    cat_rev['cum_pct'] = cat_rev['revenue'].cumsum() / cat_rev['revenue'].sum() * 100
    cat_rev['share']   = cat_rev['revenue'] / cat_rev['revenue'].sum() * 100

    c1,c2,c3,c4 = st.columns(4)
    top = cat_rev.iloc[0]
    with c1: st.markdown(kpi("Total Revenue", fmt_rp(cat_rev['revenue'].sum()), f"{len(sel_cats)} categories", ac=T['primary']), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Top Category", top['category'], fmt_rp(top['revenue']), ac=T['accent']), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Top 3 Share", f"{cat_rev.head(3)['share'].sum():.1f}%", "of total revenue", ac=T['success']), unsafe_allow_html=True)
    with c4: st.markdown(kpi("Active Products", f"{fd['product_id'].nunique():,}", "in filtered period", ac=T['warning']), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown('<div class="sec-title">Category Revenue — Pareto 80/20</div>', unsafe_allow_html=True)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        bar_c = [T['primary'] if p <= 80 else T['muted'] for p in cat_rev['cum_pct']]
        fig.add_trace(go.Bar(x=cat_rev['category'], y=cat_rev['revenue'], name="Revenue",
                             marker_color=bar_c, marker_line_width=0, opacity=0.9,
                             text=[fmt_rp(v) for v in cat_rev['revenue']],
                             textposition='outside', textfont=dict(size=9)), secondary_y=False)
        fig.add_trace(go.Scatter(x=cat_rev['category'], y=cat_rev['cum_pct'], name="Cumulative %",
                                 mode='lines+markers', line=dict(color=T['warning'], width=2),
                                 marker=dict(size=6)), secondary_y=True)
        fig.add_hline(y=80, line_color=T['danger'], line_dash='dash', line_width=1, secondary_y=True)
        fig.update_layout(**BL(h=360))
        fig.update_xaxes(tickangle=-35, gridcolor=T['grid'], tickfont=dict(size=10))
        fig.update_yaxes(gridcolor=T['grid'], tickfont=dict(size=10), secondary_y=False)
        fig.update_yaxes(showgrid=False, tickfont=dict(size=10), ticksuffix="%",
                         range=[0,110], secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-title">Revenue Share by Category</div>', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=cat_rev['category'], values=cat_rev['revenue'],
            hole=0.5,
            marker=dict(colors=T['cats'], line=dict(color=T['bg'], width=2)),
            textinfo='percent', textfont=dict(family="Inter", size=11)
        ))
        fig_pie.add_annotation(text=f"<b>{fmt_rp(cat_rev['revenue'].sum())}</b>",
                               x=0.5, y=0.5, font=dict(size=12, color=T['text']), showarrow=False)
        fig_pie.update_layout(**BL(h=360))
        st.plotly_chart(fig_pie, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="sec-title">Top 15 Products by Revenue</div>', unsafe_allow_html=True)
        pr = (fd.groupby('desc_product')
              .agg(revenue=('line_revenue','sum'))
              .sort_values('revenue', ascending=False).head(15).reset_index())
        pr['desc_product'] = pr['desc_product'].str.strip().str[:28]
        fig5 = go.Figure(go.Bar(
            x=pr['revenue'], y=pr['desc_product'], orientation='h',
            marker_color=T['accent'], marker_line_width=0, opacity=0.85,
            text=[fmt_rp(v) for v in pr['revenue']],
            textposition='outside', textfont=dict(size=9)
        ))
        fig5.update_layout(**BL(h=460))
        fig5.update_yaxes(autorange='reversed', gridcolor='rgba(0,0,0,0)', tickfont=dict(size=10))
        fig5.update_xaxes(gridcolor=T['grid'], tickfont=dict(size=10))
        st.plotly_chart(fig5, use_container_width=True)

    with col4:
        st.markdown('<div class="sec-title">Top 5 Categories — Monthly Trend</div>', unsafe_allow_html=True)
        top5 = cat_rev.head(5)['category'].tolist()
        cm = (fd[fd['category'].isin(top5)]
              .groupby(['year_month','category'])['line_revenue'].sum().reset_index())
        fig6 = px.line(cm, x='year_month', y='line_revenue', color='category',
                       markers=True, color_discrete_sequence=T['cats'])
        fig6.update_traces(line_width=2, marker_size=5)
        fig6.update_layout(**BL(h=460))
        fig6.update_xaxes(tickangle=-45, gridcolor=T['grid'], tickfont=dict(size=10))
        fig6.update_yaxes(gridcolor=T['grid'], tickfont=dict(size=10))
        st.plotly_chart(fig6, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — CUSTOMER ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif "Customer" in page:
    st.markdown(f"""<div class="page-hdr">
        <h1>👤 Customer Analytics</h1>
        <p>RFM segmentation, cohort retention, and customer behavior analysis</p>
    </div>""", unsafe_allow_html=True)

    seg_c = rfm['segment'].value_counts()
    SEG_COLORS = {
        'Champions':          T['warning'],
        'Loyal':              T['primary'],
        'Potential Loyalist': T['accent'],
        'New Customers':      T['success'],
        'At Risk':            T['orange'],
        'Cannot Lose Them':   T['danger'],
        'Churned':            T['muted'],
    }

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi("Champions 🏆", f"{seg_c.get('Champions',0):,}", "Highest value users", ac=T['warning']), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Loyal Users", f"{seg_c.get('Loyal',0):,}", "Regular buyers", ac=T['primary']), unsafe_allow_html=True)
    with c3: st.markdown(kpi("At Risk ⚠", f"{seg_c.get('At Risk',0):,}", "Need win-back", ac=T['orange']), unsafe_allow_html=True)
    with c4: st.markdown(kpi("Churned", f"{seg_c.get('Churned',0):,}", "Inactive users", ac=T['muted']), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Cohort heatmap — FIX: use safe colorscale (no hex+alpha), replace NaN properly
    st.markdown('<div class="sec-title">Cohort Retention Matrix — % Users Returning Each Month</div>', unsafe_allow_html=True)

    pivot = cohort.pivot(index='cohort', columns='period_n', values='retention')
    pivot = pivot.iloc[:, :13].copy()
    pivot.index = pivot.index.astype(str)

    z_vals = pivot.values.copy()           # float array with NaN
    z_show = np.where(np.isnan(z_vals), 0, z_vals)  # replace NaN with 0 for colorscale

    # Build text array safely
    text_arr = []
    for row in z_vals:
        row_t = []
        for v in row:
            row_t.append("" if np.isnan(v) else f"{v:.0f}%")
        text_arr.append(row_t)

    fig_coh = go.Figure(go.Heatmap(
        z=z_show,
        x=[f"M+{c}" for c in pivot.columns],
        y=pivot.index.tolist(),
        colorscale=T['coh_scale'],          # safe rgb colorscale
        text=text_arr,
        texttemplate="%{text}",
        textfont=dict(size=9, family="Inter"),
        showscale=True,
        zmin=0, zmax=100,
        colorbar=dict(title="Retention %", tickfont=dict(family="Inter", size=10),
                      ticksuffix="%")
    ))
    fig_coh.update_layout(**BL(h=480))
    fig_coh.update_xaxes(tickfont=dict(size=10))
    fig_coh.update_yaxes(tickfont=dict(size=10))
    st.plotly_chart(fig_coh, use_container_width=True)

    # RFM scatter + segment bar
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown('<div class="sec-title">RFM Landscape — Recency vs Frequency (bubble = spend)</div>', unsafe_allow_html=True)
        samp = rfm.sample(min(1500, len(rfm)), random_state=42)
        fig_rfm = px.scatter(
            samp, x='recency', y='frequency', size='monetary', color='segment',
            color_discrete_map=SEG_COLORS, size_max=25, opacity=0.7,
            hover_data={'monetary':':,.0f','recency':True,'frequency':True}
        )
        fig_rfm.update_traces(marker_line_width=0)
        fig_rfm.update_layout(**BL(h=380))
        fig_rfm.update_xaxes(title="Recency (days)", gridcolor=T['grid'], tickfont=dict(size=10))
        fig_rfm.update_yaxes(title="Frequency (orders)", gridcolor=T['grid'], tickfont=dict(size=10))
        st.plotly_chart(fig_rfm, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-title">Users per Segment</div>', unsafe_allow_html=True)
        sdf = rfm['segment'].value_counts().reset_index()
        sdf.columns = ['segment','count']
        sdf['color'] = sdf['segment'].map(SEG_COLORS).fillna(T['muted'])
        fig_seg = go.Figure(go.Bar(
            x=sdf['count'], y=sdf['segment'], orientation='h',
            marker_color=sdf['color'].tolist(),
            marker_line_width=0, opacity=0.85,
            text=sdf['count'], textposition='outside', textfont=dict(size=10)
        ))
        fig_seg.update_layout(**BL(h=380))
        fig_seg.update_yaxes(autorange='reversed', gridcolor='rgba(0,0,0,0)', tickfont=dict(size=11))
        fig_seg.update_xaxes(gridcolor=T['grid'], tickfont=dict(size=10))
        st.plotly_chart(fig_seg, use_container_width=True)

    # Strategy table
    st.markdown('<div class="sec-title">Segment Strategy Summary</div>', unsafe_allow_html=True)
    strats = {
        'Champions':          '🎯 Reward & upsell — highest LTV, early access',
        'Loyal':              '💌 Loyalty program, tier upgrade nudge',
        'Potential Loyalist': '🔁 Frequency push, bundle offers, referral',
        'New Customers':      '🚀 Onboarding flow, first re-order promo',
        'At Risk':            '⚡ Win-back campaign, "we miss you" email',
        'Cannot Lose Them':   '🚨 Urgent personal outreach, major incentive',
        'Churned':            '💀 Last-chance offer or suppress from expensive channels',
    }
    tbl = (rfm.groupby('segment')
           .agg(users=('buyer_id','count'), avg_rec=('recency','mean'),
                avg_freq=('frequency','mean'), total_rev=('monetary','sum'))
           .reset_index())
    tbl['Avg Recency']   = tbl['avg_rec'].round(0).astype(int).astype(str) + "d"
    tbl['Avg Frequency'] = tbl['avg_freq'].round(1)
    tbl['Total Revenue'] = tbl['total_rev'].apply(fmt_rp)
    tbl['Strategy']      = tbl['segment'].map(strats)
    st.dataframe(
        tbl[['segment','users','Avg Recency','Avg Frequency','Total Revenue','Strategy']]
        .rename(columns={'segment':'Segment','users':'Users'}),
        use_container_width=True, hide_index=True
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — OPERATIONS & SLA
# ══════════════════════════════════════════════════════════════════════════════
elif "Operations" in page:
    st.markdown(f"""<div class="page-hdr">
        <h1>🚚 Operations & SLA</h1>
        <p>Payment lag, delivery performance, geographic bottlenecks · {sel_range[0]} to {sel_range[1]}</p>
    </div>""", unsafe_allow_html=True)

    pp = fo[fo['is_paid']]
    dv = fo[fo['is_delivered']]
    avg_pay = pp['payment_lag'].mean()
    med_pay = pp['payment_lag'].median()
    avg_del = dv['delivery_lag'].mean()
    med_del = dv['delivery_lag'].median()
    slow_pay = (pp['payment_lag'] > 7).mean() * 100
    slow_del = (dv['delivery_lag'] > 7).mean() * 100

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: st.markdown(kpi("Avg Payment Lag", f"{avg_pay:.1f}d", "target < 7d", ac=T['primary']), unsafe_allow_html=True)
    with c2: st.markdown(kpi("Median Pay Lag", f"{med_pay:.0f}d", "50th pct", ac=T['accent']), unsafe_allow_html=True)
    with c3: st.markdown(kpi("Avg Delivery Lag", f"{avg_del:.1f}d", "target < 7d", ac=T['success']), unsafe_allow_html=True)
    with c4: st.markdown(kpi("Median Del Lag", f"{med_del:.0f}d", "50th pct", ac=T['warning']), unsafe_allow_html=True)
    with c5: st.markdown(kpi("Slow Payers >7d", f"{slow_pay:.1f}%", "of paid orders", ac=T['orange']), unsafe_allow_html=True)
    with c6: st.markdown(kpi("Slow Delivery >7d", f"{slow_del:.1f}%", "of deliveries", ac=T['danger']), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sec-title">Payment Lag Distribution</div>', unsafe_allow_html=True)
        fig1 = go.Figure(go.Histogram(
            x=pp['payment_lag'].dropna(), nbinsx=15,
            marker_color=T['primary'], marker_line_width=0, opacity=0.85))
        fig1.add_vline(x=avg_pay, line_color=T['warning'], line_dash='dash',
                       annotation_text=f"Avg: {avg_pay:.1f}d",
                       annotation_font_color=T['warning'])
        fig1.add_vline(x=7, line_color=T['danger'], line_dash='dot',
                       annotation_text="SLA: 7d", annotation_font_color=T['danger'])
        fig1.update_layout(**BL("Days from Order to Payment", h=300))
        fig1.update_xaxes(title="Days", gridcolor=T['grid'], tickfont=dict(size=10))
        fig1.update_yaxes(title="Count", gridcolor=T['grid'], tickfont=dict(size=10))
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown('<div class="sec-title">Delivery Lag Distribution</div>', unsafe_allow_html=True)
        fig2 = go.Figure(go.Histogram(
            x=dv['delivery_lag'].dropna(), nbinsx=15,
            marker_color=T['success'], marker_line_width=0, opacity=0.85))
        fig2.add_vline(x=avg_del, line_color=T['warning'], line_dash='dash',
                       annotation_text=f"Avg: {avg_del:.1f}d",
                       annotation_font_color=T['warning'])
        fig2.add_vline(x=7, line_color=T['danger'], line_dash='dot',
                       annotation_text="SLA: 7d", annotation_font_color=T['danger'])
        fig2.update_layout(**BL("Days from Payment to Delivery", h=300))
        fig2.update_xaxes(title="Days", gridcolor=T['grid'], tickfont=dict(size=10))
        fig2.update_yaxes(title="Count", gridcolor=T['grid'], tickfont=dict(size=10))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="sec-title">SLA Performance Trend — Monthly Average</div>', unsafe_allow_html=True)
    sla_m = (fo.groupby('year_month')
             .agg(pay_lag=('payment_lag','mean'), del_lag=('delivery_lag','mean'))
             .reset_index())
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=sla_m['year_month'], y=sla_m['pay_lag'],
                              name="Payment Lag", mode='lines+markers',
                              line=dict(color=T['primary'], width=2), marker=dict(size=6)))
    fig3.add_trace(go.Scatter(x=sla_m['year_month'], y=sla_m['del_lag'],
                              name="Delivery Lag", mode='lines+markers',
                              line=dict(color=T['success'], width=2), marker=dict(size=6)))
    fig3.add_hline(y=7, line_color=T['danger'], line_dash='dash',
                   annotation_text="SLA Target (7d)", annotation_font_color=T['danger'])
    fig3.update_layout(**BL("Average Lag per Month (days)", h=300))
    fig3.update_xaxes(tickangle=-45, gridcolor=T['grid'], tickfont=dict(size=10))
    fig3.update_yaxes(title="Days", gridcolor=T['grid'], tickfont=dict(size=10))
    st.plotly_chart(fig3, use_container_width=True)

    col3, col4 = st.columns([2,1])
    with col3:
        st.markdown('<div class="sec-title">Orders by Postal Code Prefix (Top 20)</div>', unsafe_allow_html=True)
        geo = fo.copy()
        geo['prefix'] = geo['kodepos'].astype(str).str[:2]
        ga = (geo.groupby('prefix')
              .agg(orders=('order_id','count'), avg_del=('delivery_lag','mean'))
              .reset_index().sort_values('orders', ascending=False).head(20))
        bar_c = [T['danger'] if (not np.isnan(d) and d > 7) else T['success']
                 for d in ga['avg_del'].fillna(0)]
        fig4 = go.Figure(go.Bar(
            x=ga['prefix'], y=ga['orders'],
            marker_color=bar_c, marker_line_width=0, opacity=0.85,
            text=ga['orders'], textposition='outside', textfont=dict(size=9)
        ))
        fig4.update_layout(**BL("🔴 = avg delivery > 7d  |  🟢 = within SLA", h=320))
        fig4.update_xaxes(gridcolor=T['grid'], tickfont=dict(size=10))
        fig4.update_yaxes(gridcolor=T['grid'], tickfont=dict(size=10))
        st.plotly_chart(fig4, use_container_width=True)

    with col4:
        st.markdown('<div class="sec-title">Bottleneck Alerts</div>', unsafe_allow_html=True)
        breach = ga[ga['avg_del'] > 7].sort_values('avg_del', ascending=False)
        if len(breach):
            for _, row in breach.iterrows():
                st.markdown(alert(f"🚨 Postal {row['prefix']}xx — {row['avg_del']:.1f}d avg · {row['orders']:,} orders", "danger"), unsafe_allow_html=True)
        else:
            st.markdown(alert("✅ Semua zona dalam SLA target", "success"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="sec-title">Unpaid Order Aging</div>', unsafe_allow_html=True)
        unpaid = fo[fo['paid_at'].isna()].copy()
        if len(unpaid):
            unpaid['age'] = (pd.Timestamp.now() - unpaid['created_at']).dt.days
            bkts = pd.cut(unpaid['age'], bins=[0,3,7,14,30,9999],
                          labels=['0-3d','4-7d','8-14d','15-30d','30+d'])
            ad = bkts.value_counts().sort_index()
            fig5 = go.Figure(go.Bar(
                x=ad.index.astype(str), y=ad.values,
                marker_color=[T['success'],T['warning'],T['orange'],T['danger'],'#7F1D1D'],
                marker_line_width=0,
                text=ad.values, textposition='outside', textfont=dict(size=11)
            ))
            fig5.update_layout(**BL(h=260))
            fig5.update_xaxes(gridcolor='rgba(0,0,0,0)', tickfont=dict(size=10))
            fig5.update_yaxes(gridcolor=T['grid'], tickfont=dict(size=10))
            st.plotly_chart(fig5, use_container_width=True)


# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;font-size:11px;color:{T['muted']};
            padding:20px 0 8px;border-top:1px solid {T['border']};margin-top:24px">
    E-Commerce Analytics Dashboard · Jan 2019 – May 2020 · Built with Streamlit & Plotly
</div>""", unsafe_allow_html=True)
