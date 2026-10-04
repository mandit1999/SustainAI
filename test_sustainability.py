import pandas as pd

from src.sustainability_score import calculate_sustainability_score


# Load dataset

df = pd.read_csv(
    "data/facility_data.csv"
)


# Calculate sustainability score

scores = calculate_sustainability_score(
    df
)


# Display results

print("\n===================================")
print("     SUSTAINABILITY SCORE")
print("===================================")

print(
    f"\nOverall Score: "
    f"{scores['overall_score']} / 100"
)

print(
    f"Energy Score: "
    f"{scores['energy_score']}"
)

print(
    f"Water Score: "
    f"{scores['water_score']}"
)

print(
    f"Waste Score: "
    f"{scores['waste_score']}"
)

print(
    f"Air Quality Score: "
    f"{scores['air_quality_score']}"
)

print(
    f"Occupancy Score: "
    f"{scores['occupancy_score']}"
)

print(
    f"Incident Score: "
    f"{scores['incident_score']}"
)

print("\nSustainability score calculated successfully!")