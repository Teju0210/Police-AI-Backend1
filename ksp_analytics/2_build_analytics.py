"""
Analytics layer for the KSP Crime Dashboard.
Reads the CSVs produced by generate_data.py (swap this step for a real SQL pull
against CaseMaster / Accused / Victim / ArrestSurrender when connected to the
live DB) and produces a single JSON payload the dashboard.html consumes.
"""
import pandas as pd
import numpy as np
import networkx as nx
import json
from datetime import date
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import OrdinalEncoder

df_case = pd.read_csv("data/CaseMaster.csv")
df_victim = pd.read_csv("data/Victim.csv")
df_accused = pd.read_csv("data/Accused.csv")
df_arrest = pd.read_csv("data/ArrestSurrender.csv")
df_profile = pd.read_csv("data/DistrictProfile.csv")

payload = {}

# ---------------------------------------------------------------------------
# KPI strip
# ---------------------------------------------------------------------------
total_cases = len(df_case)
solved = df_case["CaseStatus"].isin(["Charge Sheeted", "Closed"]).sum()
payload["kpis"] = {
    "total_cases": int(total_cases),
    "heinous_pct": round(100 * (df_case["GravityOffence"] == "Heinous").mean(), 1),
    "solve_rate_pct": round(100 * solved / total_cases, 1),
    "unique_accused": int(df_accused["RepeatIdentity"].nunique()),
    "repeat_offenders": int(df_accused["RepeatIdentity"].value_counts().gt(1).sum()),
    "districts_covered": int(df_case["District"].nunique()),
}

# ---------------------------------------------------------------------------
# District-wise analysis
# ---------------------------------------------------------------------------
dist_counts = df_case.groupby("District").size().sort_values(ascending=False)
payload["district_counts"] = [{"district": d, "count": int(c)} for d, c in dist_counts.items()]

# ---------------------------------------------------------------------------
# Crime trend graphs: yearly + monthly/seasonal
# ---------------------------------------------------------------------------
yearly = df_case.groupby("Year").size().sort_index()
payload["yearly_trend"] = [{"year": int(y), "count": int(c)} for y, c in yearly.items()]

monthly = df_case.groupby("Month").size().reindex(range(1, 13), fill_value=0)
payload["seasonal_trend"] = [{"month": int(m), "count": int(c)} for m, c in monthly.items()]

year_month = df_case.groupby(["Year", "Month"]).size().reset_index(name="count")
payload["timeline"] = [
    {"year": int(r.Year), "month": int(r.Month), "count": int(r.count)}
    for r in year_month.itertuples()
]
seasonal_matrix = df_case.groupby(["Year", "Month"]).size().unstack(fill_value=0).reindex(columns=range(1, 13), fill_value=0)
payload["seasonal_matrix"] = [
    {
        "year": int(year),
        "monthly_counts": [int(v) for v in seasonal_matrix.loc[year].tolist()],
        "peak_month": int(seasonal_matrix.loc[year].idxmax()),
        "peak_count": int(seasonal_matrix.loc[year].max()),
    }
    for year in seasonal_matrix.index
]
avg_monthly = seasonal_matrix.mean(axis=0)
payload["seasonal_insights"] = {
    "peak_month": int(avg_monthly.idxmax()),
    "peak_avg": round(float(avg_monthly.max()), 1),
    "low_month": int(avg_monthly.idxmin()),
    "low_avg": round(float(avg_monthly.min()), 1),
}

# ---------------------------------------------------------------------------
# Crime type breakdown
# ---------------------------------------------------------------------------
head_counts = df_case.groupby("CrimeHead").size().sort_values(ascending=False)
payload["crime_head_counts"] = [{"head": h, "count": int(c)} for h, c in head_counts.items()]

subhead_counts = df_case.groupby(["CrimeHead", "CrimeSubHead"]).size().reset_index(name="count")
payload["crime_subhead_counts"] = [
    {"head": r.CrimeHead, "sub": r.CrimeSubHead, "count": int(r.count)}
    for r in subhead_counts.itertuples()
]

status_counts = df_case.groupby("CaseStatus").size()
payload["status_counts"] = [{"status": s, "count": int(c)} for s, c in status_counts.items()]

# ---------------------------------------------------------------------------
# Gender analysis (victims + accused)
# ---------------------------------------------------------------------------
payload["gender_victim"] = [
    {"gender": g, "count": int(c)} for g, c in df_victim["GenderID"].value_counts().items()
]
payload["gender_accused"] = [
    {"gender": g, "count": int(c)} for g, c in df_accused["GenderID"].value_counts().items()
]

# ---------------------------------------------------------------------------
# Age analysis (victims + accused) -- bucketed
# ---------------------------------------------------------------------------
bins = [0, 12, 18, 25, 35, 45, 60, 100]
labels = ["0-12", "13-18", "19-25", "26-35", "36-45", "46-60", "60+"]

df_victim["age_bucket"] = pd.cut(df_victim["AgeYear"], bins=bins, labels=labels, right=True)
payload["age_victim"] = [
    {"bucket": b, "count": int(c)} for b, c in df_victim["age_bucket"].value_counts().reindex(labels, fill_value=0).items()
]

df_accused["age_bucket"] = pd.cut(df_accused["AgeYear"], bins=bins, labels=labels, right=True)
payload["age_accused"] = [
    {"bucket": b, "count": int(c)} for b, c in df_accused["age_bucket"].value_counts().reindex(labels, fill_value=0).items()
]

def age_gender_breakdown(df, role):
    grouped = df.groupby(["age_bucket", "GenderID"], observed=False).size().reset_index(name="count")
    return [
        {"role": role, "bucket": str(r.age_bucket), "gender": r.GenderID, "count": int(r.count)}
        for r in grouped.itertuples()
    ]

payload["age_gender_breakdown"] = age_gender_breakdown(df_victim, "Victims") + age_gender_breakdown(df_accused, "Accused")
age_totals = {
    "Victims": int(df_victim["AgeYear"].notna().sum()),
    "Accused": int(df_accused["AgeYear"].notna().sum()),
}
payload["age_summary"] = {
    "totals": age_totals,
    "victim_peak_bucket": max(payload["age_victim"], key=lambda x: x["count"])["bucket"],
    "accused_peak_bucket": max(payload["age_accused"], key=lambda x: x["count"])["bucket"],
}

# ---------------------------------------------------------------------------
# Heatmap points (sampled case coordinates)
# ---------------------------------------------------------------------------
heat_sample = df_case[["latitude", "longitude"]].sample(min(2500, len(df_case)), random_state=7)
payload["heatmap_points"] = heat_sample.values.round(5).tolist()

district_centroids = df_case.groupby("District").agg(
    lat=("latitude", "mean"), lon=("longitude", "mean"), count=("CaseMasterID", "count")
).reset_index()
payload["district_centroids"] = [
    {"district": r.District, "lat": round(r.lat, 5), "lon": round(r.lon, 5), "count": int(r.count)}
    for r in district_centroids.itertuples()
]
POLICE_STATIONS = {

    "Bagalkot": [
        "Bagalkot Town", "Navanagar", "Badami", "Hungund", "Jamkhandi", "Mudhol"
    ],

    "Ballari": [
        "Ballari Town", "Gandhinagar", "Hospet Town","Ballari Rural","Cowl Bazaar", "Kampli"
    ],

    "Belagavi": [
        "Gokak Town ", "Market", "Tilakwadi", "Shahapur", "Belagavi Rural", "Athani"
    ],

    "Bengaluru City": [
        "Ashok Nagar", "Cubbon Park", "Jayanagar", "Koramangala",
        "Whitefield", "Madiwala", "Yelahanka", "Basavanagudi"
    ],

    "Bengaluru Rural": [
        "Anekal", "Attibele", "Jigani", "Sarjapura",
        "Bannerghatta", "Nelamangala"
    ],

    "Bidar": [
        "Bidar Town", "Hulsoor", "Basavakalyan", "Bhalki", "Humnabad", "Aurad"
    ],

    "Chamarajanagar": [
        "Chamarajanagar Town", "Kollegal", "Yelandur", "Gundlupet", "Hanur", "Rural"
    ],

    "Chikkaballapur": [
        "Chikkaballapur Town", "Bagepalli", "Gauribidanur", "Sidlaghatta", "Chintamani", "Gauribidanur"
    ],

    "Chikkamagaluru": [
        "Chikkamagaluru Town", "Mudigere", "Kadur", "Koppa", "Sringeri", "Tarikere"
    ],

    "Chitradurga": [
        "Chitradurga Town", "Hiriyur", "Hosadurga", "Molakalmuru", "Holalkere", "Challakere"
    ],

    "Dakshina Kannada": [
        "Puttur Town", "Sullia", "Kadaba", "Dharmasthala ", "Surathkal", "Bantwal", "Belthangady"
    ],

    "Davanagere": [
        "KTJ Nagar", "Vidyanagar", "Davangere Rural ", "Harihar", "Honnali", "Channagiri"
    ],

    "Dharwad": [
        "Old Hubballi","Dharwad Town" , "Keshwapur","Sub Urban", "Navanagar","Vidyanagar"
    ],

    "Gadag": [
        "Gadag Town", "Betageri", "Mundargi", "Shirahatti","Ron", "Nargund"
    ],

    "Kalaburagi": [
        "Brahmapur", "Station Bazaar",  "Ashok Nagar", "Sedam", "Jewargi","University",
    ],

    "Hassan": [
        "Hassan Town", "Belur", "Arsikere", "Sakleshpur", "Alur", "Holenarasipura"
    ],

    "Haveri": [
        "Haveri Town", "Ranebennur", "Hirekerur", "Byadgi", "Savanur", "Shiggaon"
    ],

    "Kodagu": [
        "Madikeri Town", "Virajpet", "Kushalnagar", "Somwarpet", "Napoklu", "Suntikoppa"
    ],

    "Kolar": [
        "Kolar Town", "KGF", "Bangarpet", "Malur", "Mulbagal", "Srinivaspur"
    ],

    "Koppal": [
        "Koppal Town", "Gangavathi", "Kushtagi", "Yelburga", "Kanakagiri", "Karatagi"
    ],

    "Mandya": [
        "Mandya Town", "Maddur", "Malavalli", "Nagamangala", "Pandavapura", "Srirangapatna"
    ],

    "Mysuru": [
        "Nazarbad", "Lakshmipuram", "Vijayanagar", "Devaraja", "Alanahalli", "Hebbal"
    ],

    "Raichur": [
        "Raichur Town", "Lingasugur", "Manvi", "Sindhanur", "Devadurga", "Maski"
    ],

    "Ramanagara": [
        "Ramanagara Town", "Kanakapura", "Magadi", "Channapatna", "Bidadi", "Harohalli"
    ],

    "Shivamogga": [
        "Doddapete", "Tunga Nagar", "Vinobanagar", "Rural", "Bhadravathi", "Sagara"
    ],

    "Tumakuru": [
        "Tumakuru Town", "Kyathsandra", "Gubbi", "Turuvekere", "Madhugiri", "Sira"
    ],

    "Udupi": [
        "Udupi Town", "Manipal", "Karkala", "Kundapura", "Brahmavar", "Byndoor"
    ],

    "Uttara Kannada": [
        "Karwar Town", "Sirsi", "Dandeli", "Bhatkal", "Kumta", "Honnavar"
    ],

    "Vijayapura": [
        "Vijayapura Town", "Basavan Bagewadi", "Indi", "Sindagi", "Muddebihal", "Tikota"
    ],

    "Yadgir": [
        "Yadgir Town", "Shahapur", "Surpur", "Gurmitkal", "Hunasagi", "Rural"
    ]
}
# ---------------------------------------------------------------------------
# Police-station level drill-down (District -> Police Station Name)
# ---------------------------------------------------------------------------

station_counts = (
    df_case.groupby(["District", "PoliceStationNo"])
    .size()
    .reset_index(name="count")
)

station_by_district = {}

for r in station_counts.itertuples():

    district = r.District
    ps_no = int(r.PoliceStationNo)

    station_list = POLICE_STATIONS.get(district)

    if station_list:
        # Map station number to a real station name
        station_name = station_list[(ps_no - 1) % len(station_list)]
    else:
        station_name = f"Police Station {ps_no}"

    station_by_district.setdefault(district, []).append({
        "station": station_name,
        "count": int(r.count)
    })

for district in station_by_district:
    station_by_district[district].sort(
        key=lambda x: x["count"],
        reverse=True
    )

payload["station_by_district"] = station_by_district


# ---------------------------------------------------------------------------
# Station-wise Crime Head Mix
# ---------------------------------------------------------------------------

station_head = (
    df_case.groupby(["District", "PoliceStationNo", "CrimeHead"])
    .size()
    .reset_index(name="count")
)

station_head_by_district = {}

for r in station_head.itertuples():

    district = r.District
    ps_no = int(r.PoliceStationNo)

    station_list = POLICE_STATIONS.get(district)

    if station_list:
        station_name = station_list[(ps_no - 1) % len(station_list)]
    else:
        station_name = f"Police Station {ps_no}"

    station_head_by_district.setdefault(district, []).append({
        "station": station_name,
        "head": r.CrimeHead,
        "count": int(r.count)
    })

payload["station_head_by_district"] = station_head_by_district

# ---------------------------------------------------------------------------
# Spatiotemporal clusters: heatmap points layered by time-of-day bucket
# ---------------------------------------------------------------------------
TOD_ORDER = ["Morning (6AM-12PM)", "Afternoon (12PM-6PM)", "Evening (6PM-12AM)", "Night (12AM-6AM)"]
heat_by_tod = {}
for tod in TOD_ORDER:
    sub = df_case[df_case["TimeOfDay"] == tod]
    samp = sub[["latitude", "longitude"]].sample(min(1200, len(sub)), random_state=7) if len(sub) else sub[["latitude", "longitude"]]
    heat_by_tod[tod] = samp.values.round(5).tolist()
payload["heat_by_tod"] = heat_by_tod
payload["tod_order"] = TOD_ORDER
payload["tod_counts"] = [{"tod": t, "count": int((df_case["TimeOfDay"] == t).sum())} for t in TOD_ORDER]
tod_district = df_case.groupby(["TimeOfDay", "District"]).size().reset_index(name="count")
payload["tod_district_counts"] = [
    {"tod": r.TimeOfDay, "district": r.District, "count": int(r.count)}
    for r in tod_district.itertuples()
]
payload["tod_hotspots"] = {}
for tod in TOD_ORDER:
    top = tod_district[tod_district["TimeOfDay"] == tod].sort_values("count", ascending=False).head(5)
    payload["tod_hotspots"][tod] = [
        {"district": r.District, "count": int(r.count)}
        for r in top.itertuples()
    ]

# ---------------------------------------------------------------------------
# Criminal relationship network (NetworkX) -- co-accused graph
# Two accused are linked if they appear together on the same CaseMasterID.
# We keep only identities involved in >1 case OR sharing a case with someone
# else (this is the part that's invisible in flat Excel exports).
# ---------------------------------------------------------------------------
G = nx.Graph()

case_groups = df_accused.groupby("CaseMasterID")["RepeatIdentity"].apply(list)
for case_id, identities in case_groups.items():
    uniq = list(dict.fromkeys(identities))
    for ident in uniq:
        G.add_node(ident)
    for i in range(len(uniq)):
        for j in range(i + 1, len(uniq)):
            if G.has_edge(uniq[i], uniq[j]):
                G[uniq[i]][uniq[j]]["weight"] += 1
            else:
                G.add_edge(uniq[i], uniq[j], weight=1)

# case-count per identity (repeat offender signal) drives risk + node importance
identity_case_counts = df_accused.groupby("RepeatIdentity")["CaseMasterID"].nunique()
identity_gender = df_accused.groupby("RepeatIdentity")["GenderID"].first()
identity_district = df_accused.groupby("RepeatIdentity")["District"].first()

# gravity-weighted risk score: heinous cases count double, plus network degree
case_gravity_map = df_case.set_index("CaseMasterID")["GravityOffence"]
accused_case_gravity = df_accused.copy()
accused_case_gravity["gravity"] = accused_case_gravity["CaseMasterID"].map(case_gravity_map)
gravity_weight = accused_case_gravity.groupby("RepeatIdentity")["gravity"].apply(
    lambda s: (s == "Heinous").sum() * 2 + (s == "Non-Heinous").sum()
)

degree = pd.Series(dict(G.degree()))
risk_raw = (
    gravity_weight.reindex(identity_case_counts.index, fill_value=0) * 3
    + degree.reindex(identity_case_counts.index, fill_value=0) * 4
    + identity_case_counts * 2
)
risk_score = (100 * risk_raw / risk_raw.max()).round(1)

# Keep the graph focused on what's actually investigatively interesting:
# repeat offenders (linked to >1 case), scoped to the top-N by risk so the
# force-directed view stays readable. A flat "everyone who ever shared a
# case" graph is just noise -- this filtering is the actual point of doing
# network analysis instead of a flat Excel export.
repeat_ids = identity_case_counts[identity_case_counts > 1].index
top_repeat_ids = risk_score.reindex(repeat_ids).sort_values(ascending=False).head(180).index
G_sub = G.subgraph([n for n in top_repeat_ids if n in G]).copy()
for n in top_repeat_ids:
    if n not in G_sub:
        G_sub.add_node(n)

nodes_out = []
for n in G_sub.nodes():
    nodes_out.append({
        "id": int(n),
        "cases": int(identity_case_counts.get(n, 1)),
        "gender": identity_gender.get(n, "M"),
        "district": identity_district.get(n, ""),
        "risk": float(risk_score.get(n, 0)),
    })
edges_out = [{"source": int(u), "target": int(v), "weight": int(d["weight"])} for u, v, d in G_sub.edges(data=True)]

payload["network"] = {"nodes": nodes_out, "edges": edges_out}

# top risk offenders table
top_risk = risk_score.sort_values(ascending=False).head(15)
payload["top_risk_offenders"] = [
    {
        "id": int(idx), "risk": float(val),
        "cases": int(identity_case_counts.get(idx, 1)),
        "district": identity_district.get(idx, ""),
        "degree": int(degree.get(idx, 0)),
    }
    for idx, val in top_risk.items()
]

# ---------------------------------------------------------------------------
# Early warning: districts whose latest-year count exceeds their own
# historical (prior years) average by a threshold -- simple z-score style flag
# ---------------------------------------------------------------------------
pivot = df_case.groupby(["District", "Year"]).size().unstack(fill_value=0)
latest_year = int(df_case["Year"].max())
alerts = []
if latest_year in pivot.columns and len(pivot.columns) > 1:
    hist_years = [y for y in pivot.columns if y != latest_year]
    hist_mean = pivot[hist_years].mean(axis=1)
    hist_std = pivot[hist_years].std(axis=1).replace(0, 1)
    latest = pivot[latest_year]
    zscore = (latest - hist_mean) / hist_std
    spike_districts = zscore.sort_values(ascending=False)
    for d, z in spike_districts.items():
        if z > 0.8 and latest[d] >= 5:
            pct_change = round(100 * (latest[d] - hist_mean[d]) / max(hist_mean[d], 1), 1)
            alerts.append({
                "district": d, "year": latest_year, "count": int(latest[d]),
                "historical_avg": round(float(hist_mean[d]), 1),
                "pct_change": pct_change, "zscore": round(float(z), 2),
            })
payload["early_warning"] = sorted(alerts, key=lambda x: -x["zscore"])[:8]
spike_set = {a["district"] for a in payload["early_warning"]}
for d in payload["district_centroids"]:
    d["spike"] = d["district"] in spike_set

# ---------------------------------------------------------------------------
# Modus Operandi (MO) & behavioural analysis
# ---------------------------------------------------------------------------
mo_counts = df_accused["ModusOperandi"].value_counts().head(12)
payload["mo_counts"] = [{"mo": m, "count": int(c)} for m, c in mo_counts.items()]

# repeat offenders: their signature MO + how many DIFFERENT districts they've
# operated in -- this is the "recurring MO across jurisdictions" requirement.
repeat_grp = df_accused[df_accused["RepeatIdentity"].isin(repeat_ids)].groupby("RepeatIdentity")
mo_profiles = []
for ident, g in repeat_grp:
    mo_top = g["ModusOperandi"].value_counts()
    districts_hit = sorted(g["District"].unique().tolist())
    mo_profiles.append({
        "id": int(ident),
        "primary_mo": mo_top.index[0] if len(mo_top) else "Unclassified",
        "mo_variety": int(g["ModusOperandi"].nunique()),
        "districts": districts_hit,
        "district_count": len(districts_hit),
        "cases": int(identity_case_counts.get(ident, 1)),
        "risk": float(risk_score.get(ident, 0)),
    })
payload["mo_profiles"] = sorted(
    [p for p in mo_profiles if p["district_count"] > 1],
    key=lambda x: (-x["district_count"], -x["risk"])
)[:20]

# ---------------------------------------------------------------------------
# Sociological overlay: crime rate vs socio-economic indicators (DistrictProfile)
# "why behind the where"
# ---------------------------------------------------------------------------
case_counts_by_district = df_case.groupby("District").size().rename("CrimeCount")
soc = df_profile.set_index("District").join(case_counts_by_district).reset_index()
soc["CrimeRatePer100k"] = round(100000 * soc["CrimeCount"] / soc["Population"], 2)
payload["socio_economic"] = [
    {
        "district": r.District, "population": int(r.Population),
        "urbanization_pct": float(r.UrbanizationPct), "literacy_pct": float(r.LiteracyRatePct),
        "unemployment_pct": float(r.UnemploymentPct), "police_stations": int(r.PoliceStationCount),
        "crime_count": int(r.CrimeCount), "crime_rate_per_100k": float(r.CrimeRatePer100k),
    }
    for r in soc.itertuples()
]


def pearson_r(x, y):
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    if x.std() == 0 or y.std() == 0:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


payload["socio_correlations"] = {
    "urbanization": round(pearson_r(soc["UrbanizationPct"], soc["CrimeRatePer100k"]), 3),
    "literacy": round(pearson_r(soc["LiteracyRatePct"], soc["CrimeRatePer100k"]), 3),
    "unemployment": round(pearson_r(soc["UnemploymentPct"], soc["CrimeRatePer100k"]), 3),
}

# ---------------------------------------------------------------------------
# AI/ML predictive risk scoring: forecast next-period case volume per district
# using a RandomForestRegressor trained on (district, year) -> count, then
# extrapolate one year forward. Small/noisy dataset by design (demo scale),
# but this is a real fitted model, not a hand-rolled heuristic.
# ---------------------------------------------------------------------------
dy = df_case.groupby(["District", "Year"]).size().reset_index(name="count")
enc = OrdinalEncoder()
dy["district_code"] = enc.fit_transform(dy[["District"]])
X = dy[["district_code", "Year"]].values
y = dy["count"].values
rf = RandomForestRegressor(n_estimators=300, max_depth=6, random_state=42)
rf.fit(X, y)

next_year = int(df_case["Year"].max()) + 1
DISTRICTS_ALL = sorted(df_case["District"].unique())
all_codes = enc.transform(pd.DataFrame({"District": DISTRICTS_ALL}))
X_next = np.column_stack([all_codes.flatten(), np.full(len(DISTRICTS_ALL), next_year)])
pred = rf.predict(X_next)

hist_avg_map = dy.groupby("District")["count"].mean()
forecast = []
for d, p in zip(DISTRICTS_ALL, pred):
    hist_avg = float(hist_avg_map.get(d, p))
    delta_pct = round(100 * (p - hist_avg) / max(hist_avg, 1), 1)
    tier = "High" if p >= np.percentile(pred, 75) else ("Medium" if p >= np.percentile(pred, 40) else "Low")
    forecast.append({
        "district": d, "predicted_count": round(float(p), 1),
        "historical_avg": round(hist_avg, 1), "delta_pct": delta_pct, "risk_tier": tier,
    })
payload["forecast"] = sorted(forecast, key=lambda x: -x["predicted_count"])
payload["forecast_year"] = next_year
payload["forecast_model"] = "RandomForestRegressor(n_estimators=300, max_depth=6) on (District, Year) -> case volume"

# ---------------------------------------------------------------------------
# AI/ML anomaly detection: IsolationForest over case-level behavioural
# features flags incidents that deviate from normal patterns (visual call-outs)
# ---------------------------------------------------------------------------
feat_df = df_case.copy()
feat_enc = OrdinalEncoder()
feat_df["district_code"] = feat_enc.fit_transform(feat_df[["District"]])
head_enc = OrdinalEncoder()
feat_df["head_code"] = head_enc.fit_transform(feat_df[["CrimeHead"]])
feat_df["gravity_code"] = (feat_df["GravityOffence"] == "Heinous").astype(int)
features = feat_df[["district_code", "head_code", "gravity_code", "Hour", "Month"]].values

iso = IsolationForest(n_estimators=250, contamination=0.02, random_state=42)
feat_df["anomaly_score"] = -iso.fit(features).score_samples(features)  # higher = more anomalous
feat_df["is_anomaly"] = iso.predict(features) == -1

anomalies = feat_df[feat_df["is_anomaly"]].sort_values("anomaly_score", ascending=False).head(25)
payload["anomalies"] = [
    {
        "case_id": int(r.CaseMasterID), "crime_no": str(r.CrimeNo), "district": r.District,
        "crime_head": r.CrimeHead, "crime_sub": r.CrimeSubHead, "date": r.CrimeRegisteredDate,
        "time_of_day": r.TimeOfDay, "gravity": r.GravityOffence, "status": r.CaseStatus,
        "score": round(float(r.anomaly_score), 3),
    }
    for r in anomalies.itertuples()
]
payload["anomaly_model"] = "IsolationForest(n_estimators=250, contamination=0.02) on district/crime-type/gravity/hour/month"
payload["anomaly_count"] = int(feat_df["is_anomaly"].sum())

with open("output/dashboard_data.json", "w") as f:
    json.dump(payload, f)

print("KPIs:", payload["kpis"])
print("Network nodes/edges:", len(nodes_out), len(edges_out))
print("Early warning alerts:", len(payload["early_warning"]))
print("MO profiles (multi-district repeat offenders):", len(payload["mo_profiles"]))
print("Socio-economic correlations (r):", payload["socio_correlations"])
print(f"Forecast for {payload['forecast_year']}: top district ->", payload["forecast"][0])
print("Anomalies flagged:", payload["anomaly_count"])
print("Wrote output/dashboard_data.json")
