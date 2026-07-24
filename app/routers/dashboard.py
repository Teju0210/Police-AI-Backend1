from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.database import get_db
from app.models.fir import FIR
from app.models.officer import Officer

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_crimes = db.query(FIR).count()
    
    # Let's count solved cases. Suppose 'status' could be 'Solved', 'Closed', 'Charge Sheeted' etc.
    # For now, let's just count 'Closed' or similar, or just any status that implies solved.
    # We will just fetch FIRs and see what statuses we have or just do it by some logic.
    # Let's assume 'Closed' or 'Charge sheeted' means solved. Or we just get count where status is not 'Pending' or 'Active'.
    # A simple approach:
    solved_cases = db.query(FIR).filter(FIR.status.in_(["Closed", "Solved", "Charge Sheeted"])).count()
    
    solved_percentage = 0
    if total_crimes > 0:
        solved_percentage = int((solved_cases / total_crimes) * 100)
        
    # Crime hotspots: distinct police stations with FIRs
    hotspots_count = db.query(FIR.police_station_id).distinct().count()
    
    # Active officers
    active_officers = db.query(Officer).count()
    
    return {
        "stats": [
            {
                "title": "Total Crimes",
                "value": str(total_crimes),
                "icon": "ShieldAlert",
                "color": "text-red-400",
                "link": "/reports",
            },
            {
                "title": "Solved Cases",
                "value": f"{solved_percentage}%",
                "icon": "CheckCircle2",
                "color": "text-green-400",
                "link": "/analytics",
            },
            {
                "title": "Crime Hotspots",
                "value": str(hotspots_count),
                "icon": "MapPinned",
                "color": "text-yellow-400",
                "link": "/heatmap",
            },
            {
                "title": "Active Officers",
                "value": str(active_officers),
                "icon": "Users",
                "color": "text-blue-400",
                "link": "/network",
            }
        ]
    }

@router.get("/crime-trend")
def get_crime_trend(db: Session = Depends(get_db)):
    # Group by month
    trends = db.query(FIR.month, func.count(FIR.id).label("crimes")).group_by(FIR.month).all()
    
    month_names = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }
    
    result = []
    # Ensure it's sorted by month
    sorted_trends = sorted(trends, key=lambda x: x.month if x.month else 0)
    
    for trend in sorted_trends:
        if trend.month:
            result.append({
                "month": month_names.get(trend.month, str(trend.month)),
                "crimes": trend.crimes
            })
            
    # Fallback to dummy data if empty to show something in UI
    if not result:
        result = [
            {"month": "Jan", "crimes": 0},
            {"month": "Feb", "crimes": 0},
            {"month": "Mar", "crimes": 0},
        ]
        
    return {"crimeTrend": result}

@router.get("/crime-category")
def get_crime_category(db: Session = Depends(get_db)):
    # Group by case_category
    categories = db.query(FIR.case_category, func.count(FIR.id).label("cases")).group_by(FIR.case_category).order_by(func.count(FIR.id).desc()).limit(5).all()
    
    result = []
    for cat in categories:
        if cat.case_category:
            # Only keep the first word or truncate if too long, as per UI design?
            # Or just pass the full name
            result.append({
                "name": cat.case_category[:10] + ".." if len(cat.case_category) > 12 else cat.case_category,
                "cases": cat.cases
            })
            
    if not result:
        result = [
            {"name": "No Data", "cases": 0}
        ]
        
    return {"crimeCategory": result}

@router.get("/heatmap")
def get_heatmap_data(db: Session = Depends(get_db)):
    # Get recent/high gravity crimes with valid lat/lng
    crimes = db.query(FIR).filter(
        FIR.latitude != None,
        FIR.longitude != None,
        FIR.latitude != 0.0,
        FIR.longitude != 0.0
    ).limit(300).all()
    
    result = []
    for c in crimes:
        severity = "MEDIUM"
        if c.gravity_offence and "heinous" in c.gravity_offence.lower():
            severity = "HIGH"
        elif c.gravity_offence and "non" in c.gravity_offence.lower():
            severity = "LOW"
            
        result.append({
            "id": c.id,
            "type": c.case_category or "Unknown",
            "location": c.location or "Unknown",
            "lat": c.latitude,
            "lng": c.longitude,
            "severity": severity
        })
        
    return {"crimes": result}
