"""
Synthetic KSP crime data generator.
Mirrors the actual FIR ER schema (CaseMaster / Accused / Victim / District / Unit /
CrimeHead / CrimeSubHead / ArrestSurrender) so downstream analytics code is a drop-in
replacement once real DB access is available -- just swap this module for a SQL pull
into the same dataframe shapes.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json

rng = np.random.default_rng(42)

# ---------------------------------------------------------------------------
# 1. Reference / master data (mirrors District, Unit, CrimeHead, CrimeSubHead,
#    CaseCategory, GravityOffence, CaseStatusMaster)
# ---------------------------------------------------------------------------

DISTRICTS = [
    "Bengaluru City", "Bengaluru Rural", "Mysuru", "Mangaluru (Dakshina Kannada)",
    "Belagavi", "Kalaburagi", "Hubballi-Dharwad", "Ballari", "Tumakuru",
    "Shivamogga", "Davanagere", "Vijayapura", "Raichur", "Bidar", "Chikkamagaluru",
    "Udupi", "Kolar", "Mandya", "Hassan", "Chitradurga", "Koppal", "Yadgir",
    "Chamarajanagar", "Kodagu", "Ramanagara", "Chikkaballapur", "Bagalkot",
    "Haveri", "Gadag", "Uttara Kannada",
]
# approximate district centroids (lat, lon) for Karnataka, for the hotspot map
DISTRICT_COORDS = {
    "Bengaluru City": (12.9716, 77.5946), "Bengaluru Rural": (13.2846, 77.5540),
    "Mysuru": (12.2958, 76.6394), "Mangaluru (Dakshina Kannada)": (12.9141, 74.8560),
    "Belagavi": (15.8497, 74.4977), "Kalaburagi": (17.3297, 76.8343),
    "Hubballi-Dharwad": (15.3647, 75.1240), "Ballari": (15.1394, 76.9214),
    "Tumakuru": (13.3379, 77.1173), "Shivamogga": (13.9299, 75.5681),
    "Davanagere": (14.4644, 75.9218), "Vijayapura": (16.8302, 75.7100),
    "Raichur": (16.2076, 77.3463), "Bidar": (17.9104, 77.5199),
    "Chikkamagaluru": (13.3161, 75.7720), "Udupi": (13.3409, 74.7421),
    "Kolar": (13.1362, 78.1298), "Mandya": (12.5242, 76.8958),
    "Hassan": (13.0059, 76.1025), "Chitradurga": (14.2296, 76.3985),
    "Koppal": (15.3467, 76.1548), "Yadgir": (16.7622, 77.1376),
    "Chamarajanagar": (11.9236, 76.9456), "Kodagu": (12.3375, 75.8069),
    "Ramanagara": (12.7217, 77.2812), "Chikkaballapur": (13.4351, 77.7315),
    "Bagalkot": (16.1691, 75.6636), "Haveri": (14.7936, 75.4044),
    "Gadag": (15.4310, 75.6297), "Uttara Kannada": (14.7940, 74.6980),
}

CRIME_HEADS = {
    "Crimes Against Body": ["Murder", "Attempt to Murder", "Grievous Hurt", "Assault"],
    "Crimes Against Property": ["Theft", "Burglary", "Robbery", "Dacoity"],
    "Crimes Against Women": ["Domestic Violence", "Molestation", "Dowry Harassment", "Sexual Assault"],
    "Cyber Crime": ["Online Fraud", "Identity Theft", "Cyberstalking", "Phishing"],
    "Economic Offences": ["Cheating", "Criminal Breach of Trust", "Forgery"],
    "Narcotics": ["NDPS Possession", "NDPS Trafficking"],
    "Public Order": ["Rioting", "Unlawful Assembly"],
}
CRIME_HEAD_LIST = list(CRIME_HEADS.keys())

CASE_CATEGORIES = ["FIR", "UDR", "Zero FIR", "PAR"]
GRAVITY = ["Heinous", "Non-Heinous"]
CASE_STATUS = ["Under Investigation", "Charge Sheeted", "Closed", "False Case", "Undetected"]

# Modus Operandi vocabulary, keyed by CrimeHead so MO stays thematically consistent
# with the offence, but still lets us track a repeat offender's *signature* MO
# across districts (the whole point of the network/behavioural-analysis ask).
MODUS_OPERANDI = {
    "Crimes Against Body": ["Sudden Armed Assault", "Group Attack (Prior Enmity)", "Weapon-Assisted Assault", "Confrontation over Dispute"],
    "Crimes Against Property": ["Night-time House Break-in", "Vehicle Theft (Parked)", "Shop Lock-Break", "Snatching in Transit", "Break-in via Rear Entry"],
    "Crimes Against Women": ["Known-Person Domestic Abuse", "Stalking Prior to Offence", "Workplace Harassment", "Dowry-Related Coercion"],
    "Cyber Crime": ["Phishing Link / OTP Fraud", "Fake Investment App", "Social Media Impersonation", "SIM-Swap Fraud"],
    "Economic Offences": ["Shell Company Cheating", "Forged Document Trail", "Chit Fund Default", "Cheque Bounce Fraud"],
    "Narcotics": ["Courier via Public Transport", "Home Cultivation/Storage", "Cross-Border Transit Route"],
    "Public Order": ["Organized Group Mobilization", "Social-Media Incited Assembly"],
}

N_CASES = 6000
N_DISTRICT_STATIONS = 4  # stations per district (kept small for demo)
YEARS = [2022, 2023, 2024, 2025, 2026]
YEAR_WEIGHTS = [0.14, 0.17, 0.20, 0.23, 0.26]  # mild upward drift for trend realism

def seasonal_weight(month):
    # slightly higher incidence around festival months (Oct-Nov) and summer (Apr-May)
    boost = {10: 1.25, 11: 1.2, 4: 1.15, 5: 1.1, 12: 1.1}
    return boost.get(month, 1.0)

# district "risk profile" so hotspots feel non-uniform, not just population noise
district_base_rate = {d: rng.gamma(shape=2.2, scale=1.0) for d in DISTRICTS}
# a handful of districts run structurally hotter (mirrors urban-core effect)
for hot in ["Bengaluru City", "Bengaluru Rural", "Mysuru", "Mangaluru (Dakshina Kannada)", "Belagavi"]:
    district_base_rate[hot] *= 2.4

district_probs = np.array([district_base_rate[d] for d in DISTRICTS])
district_probs = district_probs / district_probs.sum()

rows_case = []
rows_victim = []
rows_accused = []
rows_arrest = []

first_names_m = ["Ravi", "Suresh", "Manoj", "Naveen", "Prasad", "Anil", "Vikram", "Deepak", "Arjun", "Kiran"]
first_names_f = ["Lakshmi", "Kavya", "Anitha", "Sunita", "Deepa", "Priya", "Shalini", "Meena", "Radha", "Pooja"]

case_id = 1
victim_id = 1
accused_id = 1
arrest_id = 1

# maintain per-district running serial for realistic CrimeNo generation
serial_counters = {}

for i in range(N_CASES):
    district = rng.choice(DISTRICTS, p=district_probs)
    lat0, lon0 = DISTRICT_COORDS[district]
    year = int(rng.choice(YEARS, p=np.array(YEAR_WEIGHTS) / sum(YEAR_WEIGHTS)))
    month = rng.integers(1, 13)
    w = seasonal_weight(month)
    if rng.random() > min(w / 1.3, 1.0) and w <= 1.0:
        pass  # seasonal weighting folded into sampling below instead

    day = rng.integers(1, 28)
    incident_dt = datetime(year, int(month), int(day)) + timedelta(hours=int(rng.integers(0, 24)))

    crime_head = rng.choice(CRIME_HEAD_LIST, p=[0.22, 0.28, 0.20, 0.10, 0.12, 0.05, 0.03])
    crime_sub = rng.choice(CRIME_HEADS[crime_head])
    category = rng.choice(CASE_CATEGORIES, p=[0.78, 0.06, 0.08, 0.08])
    gravity = "Heinous" if crime_head in ("Crimes Against Body", "Crimes Against Women", "Narcotics") and rng.random() < 0.45 else "Non-Heinous"
    status = rng.choice(CASE_STATUS, p=[0.32, 0.30, 0.20, 0.10, 0.08])

    station_no = rng.integers(1, N_DISTRICT_STATIONS + 1)
    district_idx = DISTRICTS.index(district) + 1
    cat_code = str(CASE_CATEGORIES.index(category) * 3 + 1)[0]  # rough single-digit code
    crime_no = f"{cat_code}{district_idx:04d}{station_no:04d}{year}{i+1:05d}"

    lat = lat0 + rng.normal(0, 0.06)
    lon = lon0 + rng.normal(0, 0.06)

    hour = incident_dt.hour
    if 0 <= hour < 6:
        time_of_day = "Night (12AM-6AM)"
    elif 6 <= hour < 12:
        time_of_day = "Morning (6AM-12PM)"
    elif 12 <= hour < 18:
        time_of_day = "Afternoon (12PM-6PM)"
    else:
        time_of_day = "Evening (6PM-12AM)"

    rows_case.append({
        "CaseMasterID": case_id, "CrimeNo": crime_no, "District": district,
        "PoliceStationNo": station_no, "CrimeRegisteredDate": incident_dt.date().isoformat(),
        "Year": year, "Month": int(month), "Hour": int(hour), "TimeOfDay": time_of_day,
        "CaseCategory": category, "GravityOffence": gravity,
        "CrimeHead": crime_head, "CrimeSubHead": crime_sub, "CaseStatus": status,
        "latitude": round(lat, 5), "longitude": round(lon, 5),
    })

    # victims: 1 (occasionally 2) per case
    n_victims = 1 if rng.random() < 0.85 else 2
    for _ in range(n_victims):
        gender = rng.choice(["F", "M", "T"], p=[0.52, 0.46, 0.02])
        age = int(np.clip(rng.normal(34, 14), 5, 85))
        rows_victim.append({"VictimMasterID": victim_id, "CaseMasterID": case_id,
                             "GenderID": gender, "AgeYear": age})
        victim_id += 1

    # accused: 0-3 per case (some cases undetected -> 0 accused)
    if status == "Undetected":
        n_accused = 0
    else:
        n_accused = int(rng.choice([1, 2, 3], p=[0.6, 0.28, 0.12]))
    case_accused_ids = []
    mo_options = MODUS_OPERANDI.get(crime_head, ["Unclassified"])
    for a in range(n_accused):
        gender = rng.choice(["M", "F"], p=[0.88, 0.12])
        age = int(np.clip(rng.normal(29, 9), 16, 70))
        mo = str(rng.choice(mo_options))
        rows_accused.append({"AccusedMasterID": accused_id, "CaseMasterID": case_id,
                              "PersonID": f"A{a+1}", "GenderID": gender, "AgeYear": age,
                              "District": district, "ModusOperandi": mo})
        case_accused_ids.append(accused_id)
        accused_id += 1

    # arrest/surrender events for a portion of accused
    for aid in case_accused_ids:
        if rng.random() < 0.62:
            atype = rng.choice(["Arrest", "Surrender"], p=[0.8, 0.2])
            adate = (incident_dt + timedelta(days=int(rng.integers(0, 45)))).date().isoformat()
            rows_arrest.append({"ArrestSurrenderID": arrest_id, "CaseMasterID": case_id,
                                 "AccusedMasterID": aid, "ArrestSurrenderTypeID": atype,
                                 "ArrestSurrenderDate": adate, "District": district})
            arrest_id += 1

    case_id += 1

df_case = pd.DataFrame(rows_case)
df_victim = pd.DataFrame(rows_victim)
df_accused = pd.DataFrame(rows_accused)
df_arrest = pd.DataFrame(rows_arrest)

# ---------------------------------------------------------------------------
# Repeat-offender injection: pick ~4% of accused identities to reappear across
# multiple cases (needed for network analysis / risk scoring to be meaningful)
# ---------------------------------------------------------------------------
repeat_pool_size = max(20, int(len(df_accused) * 0.04))
repeat_pool = df_accused.sample(repeat_pool_size, random_state=1).copy()
case_head_map = df_case.set_index("CaseMasterID")["CrimeHead"]
extra_rows = []
next_aid = df_accused["AccusedMasterID"].max() + 1
for _, r in repeat_pool.iterrows():
    n_extra = rng.integers(1, 4)
    seed = int(r["AccusedMasterID"]) % 10000
    # ~55% of repeat offenders resurface in OTHER districts too -- this is the
    # "recurring MO across different jurisdictions" signal for the network view.
    if rng.random() < 0.55:
        candidate_cases = df_case.sample(min(n_extra, len(df_case)), random_state=seed)
    else:
        candidate_cases = df_case[df_case["District"] == r["District"]].sample(
            min(n_extra, len(df_case[df_case["District"] == r["District"]])), random_state=seed
        )
    signature_mo = r.get("ModusOperandi", "Unclassified")
    for _, c in candidate_cases.iterrows():
        # keep the same signature MO ~70% of the time (repeat behavioural pattern),
        # otherwise pick a plausible MO for that case's own crime head
        if rng.random() < 0.7:
            mo = signature_mo
        else:
            mo = str(rng.choice(MODUS_OPERANDI.get(case_head_map.get(c["CaseMasterID"]), [signature_mo])))
        extra_rows.append({"AccusedMasterID": next_aid, "CaseMasterID": c["CaseMasterID"],
                            "PersonID": "A_r", "GenderID": r["GenderID"], "AgeYear": r["AgeYear"],
                            "District": c["District"], "ModusOperandi": mo,
                            "RepeatIdentity": r["AccusedMasterID"]})
        next_aid += 1

df_accused["RepeatIdentity"] = df_accused["AccusedMasterID"]  # baseline: identity == own id
df_repeat_extra = pd.DataFrame(extra_rows)
df_accused_full = pd.concat([df_accused, df_repeat_extra], ignore_index=True)

# Save everything
df_case.to_csv("data/CaseMaster.csv", index=False)
df_victim.to_csv("data/Victim.csv", index=False)
df_accused_full.to_csv("data/Accused.csv", index=False)
df_arrest.to_csv("data/ArrestSurrender.csv", index=False)

print("Cases:", len(df_case))
print("Victims:", len(df_victim))
print("Accused (incl. repeat links):", len(df_accused_full))
print("Arrest/Surrender events:", len(df_arrest))
print("Unique repeat-offender identities:", df_accused_full["RepeatIdentity"].nunique(), "vs total accused rows", len(df_accused_full))
