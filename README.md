# ⚡ E-Commerce Analytics Command Center
### Senior Data Analyst Framework | Jan 2019 – May 2020 | Rp 148.8B GMV

---

## 🚀 QUICK START

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy your CSV files into this folder
cp path/to/orders.csv .
cp path/to/order_details.csv .
cp path/to/products.csv .
cp path/to/users.csv .

# 3. Launch
streamlit run app.py
```

---

## 🏗️ DASHBOARD ARCHITECTURE

### PAGE 1 — Executive Revenue & Funnel Health
| KPI | Formula | Business Logic |
|-----|---------|----------------|
| GMV | `SUM(orders.total WHERE paid_at IS NOT NULL)` | Only count confirmed revenue |
| AOV | `GMV / COUNT(paid orders)` | Average basket size signal |
| Payment Conv. | `paid / created * 100` | Demand-capture efficiency |
| Delivery Conv. | `delivered / paid * 100` | Logistics execution quality |
| MoM Growth | `(GMV_curr - GMV_prev) / GMV_prev * 100` | Velocity indicator |

**Charts:** GMV/Volume dual-axis trend, Conversion Funnel, MoM waterfall, Day-of-week heatmap

---

### PAGE 2 — Product Performance & Category Intelligence
| Analysis | Method | Insight |
|----------|--------|---------|
| Pareto 80/20 | Cumulative revenue curve | Top 3 categories = ~68% of revenue |
| Category Share | Pie/Donut | Kebersihan Diri dominates at 31% |
| Top Products | Ranked bar | Blackmores vitamins are top performers |
| Price Integrity | base_price vs selling price | Zero markdown detected |
| Category Trend | Multi-line time series | Growth patterns by category |

---

### PAGE 3 — Customer Retention & RFM
#### Cohort Retention Matrix
- **Method:** Group buyers by first-purchase month → track % returning each subsequent month
- **Key Insight:** Identify the exact month retention drops significantly

#### RFM Scoring Logic
```
R Score: Quintile rank of (snapshot_date - last_order_date) → INVERTED (5=recent)
F Score: Quintile rank of order_count
M Score: Quintile rank of lifetime spend

Segment Rules:
┌─────────────────────────┬────────────────────────────────┐
│ Champions               │ R≥4 AND F≥4 AND M≥4           │
│ Loyal                   │ R≥3 AND F≥3                    │
│ New Customers           │ R≥4 AND F≤2                    │
│ Potential Loyalist      │ R≥3 AND F≥2                    │
│ At Risk                 │ R=2 AND F≥2                    │
│ Cannot Lose Them        │ R≤2 AND F≥3                    │
│ Churned                 │ Everything else                 │
└─────────────────────────┴────────────────────────────────┘
```

---

### PAGE 4 — Operations & Fulfillment SLA
| Metric | Formula | SLA Target |
|--------|---------|------------|
| Payment Lag | `paid_at - created_at` | ≤ 7 days |
| Delivery Lag | `delivery_at - paid_at` | ≤ 7 days |
| Slow Payers | `payment_lag > 10d` | < 15% |
| Slow Deliveries | `delivery_lag > 10d` | < 15% |

**Geographic Analysis:** Postal code prefix (first 2 digits) groups orders by region, colored by delivery SLA breach.

---

## 📊 KEY FINDINGS

### Transaction Funnel
```
74,874 orders created
  └─ 69,828 paid      (93.3% conversion) → 5,046 unpaid orders
       └─ 65,084 delivered (93.2% of paid) → 4,744 undelivered
```
**Revenue at risk from unpaid orders: ~Rp 10B**

### Revenue by Category (Top 5)
| Category | Revenue | Share |
|----------|---------|-------|
| Kebersihan Diri | Rp 46.5B | 31.2% |
| Pakaian Pria | Rp 29.1B | 19.5% |
| Fresh Food | Rp 27.3B | 18.4% |
| Pakaian Wanita | Rp 17.4B | 11.7% |
| Vitamin | Rp 13.0B | 8.8% |

### SLA Metrics
- Avg Payment Lag: **7.5 days** (median: 7d)
- Avg Delivery Lag: **6.6 days** (median: 7d)
- Max observed lag: **14 days** (hard ceiling — likely business rule)

---

## 🎯 STRATEGIC RECOMMENDATION MATRIX

### 1. GROWTH MARKETING — Recover Unpaid Orders
```
Problem: 5,046 orders (Rp ~10B) abandoned pre-payment
Tactics:
  ▸ T+1 day: Push notification — "Complete your purchase"
  ▸ T+3 day: Email with urgency (stock expiry)
  ▸ T+5 day: SMS with 5% discount code
  ▸ T+7 day: Final reminder, offer payment installment
  
Expected recovery: 15-25% of abandoned orders
Projected GMV recovery: Rp 1.5B – 2.5B
```

### 2. INVENTORY & SUPPLY CHAIN — Category Optimization
```
HIGH PRIORITY (Scale Up):
  ▸ Kebersihan Diri — 31% of GMV, maintain stock depth
  ▸ Fresh Food — High velocity, optimize cold chain SLA
  ▸ Vitamin — Blackmores dominates, explore private label

LOW PRIORITY (Rationalize):
  ▸ Makanan Kaleng — Only 0.8% GMV — reduce SKU count by 40%
  ▸ Minuman Ringan — 1.5% GMV — curate top 20 SKUs only
  ▸ Pakaian Tidur Wanita — 1.5% GMV — reduce to best sellers
```

### 3. CUSTOMER LOYALTY — RFM-Based Treatment
```
Champions (~top 20% by RFM):
  ▸ VIP early access to new products
  ▸ Dedicated account manager for B2B-tier buyers
  ▸ Birthday/anniversary surprise gifts

Loyal & Potential Loyalist:
  ▸ Points-based loyalty program
  ▸ Tier upgrade communication ("You're 2 orders from Gold!")
  ▸ Bundle recommendations based on purchase history

At Risk & Cannot Lose:
  ▸ Win-back campaigns with personalized offers
  ▸ "We miss you" email series
  ▸ Free shipping threshold reduction

Churned:
  ▸ Suppression from expensive channels
  ▸ Quarterly last-chance mailer
  ▸ Sunset after 18 months of inactivity
```

### 4. OPERATIONS — SLA Improvement
```
Payment SLA (currently 7.5d avg, target <5d):
  ▸ Offer instant payment methods (GoPay, OVO, Dana)
  ▸ Auto-cancel unpaid orders after 7 days to clear inventory
  ▸ Introduce 0% installment payment to reduce friction

Delivery SLA (currently 6.6d avg, target <5d):
  ▸ Partner with additional last-mile couriers
  ▸ Geo-based carrier routing (reduce cross-province shipments)
  ▸ Alert sellers for orders unpicked after 24h
```

---

## 📁 FILE STRUCTURE
```
dashboard/
├── app.py              ← Main Streamlit application
├── requirements.txt    ← Python dependencies
├── README.md           ← This file
├── orders.csv          ← Place data files here
├── order_details.csv
├── products.csv
└── users.csv
```

---

*Built with Streamlit · Plotly · Pandas | Framework by Senior Data Analyst Suite*
