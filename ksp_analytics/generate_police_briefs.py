import pandas as pd
import os

def generate_briefs():
    csv_path = "data/CaseMaster.csv"
    output_path = "data/police_briefs.txt"
    
    if not os.path.exists(csv_path):
        print(f"Error: Could not find {csv_path}")
        return

    # Read top 3 rows
    df = pd.read_csv(csv_path).head(3)
    
    briefs = []
    briefs.append("POLICE CASE BRIEFS MASTER DOCUMENT\n")
    briefs.append("The following are the verified case briefs from the Karnataka State Police Database.\n")
    
    for _, row in df.iterrows():
        brief = (
            f"Case Number: {row.get('CrimeNo', 'Unknown')}\n"
            f"Date Registered: {row.get('CrimeRegisteredDate', 'Unknown')} at {row.get('Hour', 'Unknown')}:00 hours ({row.get('TimeOfDay', 'Unknown')})\n"
            f"Location: {row.get('District', 'Unknown')} (Police Station No: {row.get('PoliceStationNo', 'Unknown')})\n"
            f"Category: {row.get('CaseCategory', 'Unknown')} - {row.get('GravityOffence', 'Unknown')}\n"
            f"Crime Type: {row.get('CrimeHead', 'Unknown')} ({row.get('CrimeSubHead', 'Unknown')})\n"
            f"Status: {row.get('CaseStatus', 'Unknown')}\n"
            f"Coordinates: Latitude {row.get('latitude', 'Unknown')}, Longitude {row.get('longitude', 'Unknown')}\n"
            f"Summary: On {row.get('CrimeRegisteredDate', 'Unknown')}, an incident of {row.get('CrimeSubHead', 'Unknown')} "
            f"({row.get('CrimeHead', 'Unknown')}) occurred in {row.get('District', 'Unknown')}. "
            f"The case is classified as {row.get('GravityOffence', 'Unknown')} and is currently {row.get('CaseStatus', 'Unknown')}.\n"
            "-" * 40 + "\n"
        )
        briefs.append(brief)
        
    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(briefs)
        
    print(f"Successfully generated {len(df)} case briefs in {output_path}")

if __name__ == "__main__":
    generate_briefs()
