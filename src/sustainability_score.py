import pandas as pd


def calculate_sustainability_score(df):
    """
    Calculate a sustainability score between 0 and 100.

    Higher scores indicate better overall sustainability
    performance.
    """

    data = df.copy()

    # ---------------------------------------------------------
    # 1. ENERGY SCORE
    # ---------------------------------------------------------

    energy_mean = data["electricity_kwh"].mean()

    energy_median = data["electricity_kwh"].median()

    if energy_mean <= energy_median:
        energy_score = 100
    else:
        energy_ratio = energy_median / energy_mean

        energy_score = energy_ratio * 100

    energy_score = max(
        0,
        min(100, energy_score)
    )


    # ---------------------------------------------------------
    # 2. WATER SCORE
    # ---------------------------------------------------------

    water_mean = data["water_liters"].mean()

    water_median = data["water_liters"].median()

    if water_mean <= water_median:
        water_score = 100
    else:
        water_ratio = water_median / water_mean

        water_score = water_ratio * 100

    water_score = max(
        0,
        min(100, water_score)
    )


    # ---------------------------------------------------------
    # 3. WASTE SCORE
    # ---------------------------------------------------------

    waste_mean = data["waste_kg"].mean()

    waste_median = data["waste_kg"].median()

    if waste_mean <= waste_median:
        waste_score = 100
    else:
        waste_ratio = waste_median / waste_mean

        waste_score = waste_ratio * 100

    waste_score = max(
        0,
        min(100, waste_score)
    )


    # ---------------------------------------------------------
    # 4. AIR QUALITY SCORE
    # ---------------------------------------------------------

    aqi_mean = data["aqi"].mean()

    # Lower AQI is generally better.
    # This simple prototype scoring approach maps
    # AQI values into a 0-100 score.

    if aqi_mean <= 50:

        aqi_score = 100

    elif aqi_mean <= 100:

        aqi_score = 80

    elif aqi_mean <= 150:

        aqi_score = 60

    elif aqi_mean <= 200:

        aqi_score = 40

    elif aqi_mean <= 300:

        aqi_score = 20

    else:

        aqi_score = 0


    # ---------------------------------------------------------
    # 5. OCCUPANCY / RESOURCE UTILIZATION SCORE
    # ---------------------------------------------------------

    occupancy_mean = data[
        "occupancy_percent"
    ].mean()

    # Moderate utilization is treated as efficient
    # for this prototype.

    if occupancy_mean <= 30:

        occupancy_score = 70

    elif occupancy_mean <= 60:

        occupancy_score = 90

    elif occupancy_mean <= 80:

        occupancy_score = 100

    elif occupancy_mean <= 90:

        occupancy_score = 85

    else:

        occupancy_score = 70


    # ---------------------------------------------------------
    # 6. INCIDENT SCORE
    # ---------------------------------------------------------

    total_incidents = (
        data["maintenance_incidents"].sum()
        +
        data["safety_incidents"].sum()
    )

    number_of_records = len(data)

    if number_of_records > 0:

        incidents_per_record = (
            total_incidents /
            number_of_records
        )

    else:

        incidents_per_record = 0


    if incidents_per_record == 0:

        incident_score = 100

    elif incidents_per_record <= 0.02:

        incident_score = 90

    elif incidents_per_record <= 0.05:

        incident_score = 75

    elif incidents_per_record <= 0.10:

        incident_score = 60

    else:

        incident_score = 40


    # ---------------------------------------------------------
    # FINAL SCORE
    # ---------------------------------------------------------

    overall_score = (
        energy_score * 0.25
        +
        water_score * 0.20
        +
        waste_score * 0.15
        +
        aqi_score * 0.20
        +
        occupancy_score * 0.10
        +
        incident_score * 0.10
    )


    overall_score = max(
        0,
        min(100, overall_score)
    )


    # ---------------------------------------------------------
    # RETURN RESULTS
    # ---------------------------------------------------------

    scores = {

        "overall_score":
            round(overall_score, 2),

        "energy_score":
            round(energy_score, 2),

        "water_score":
            round(water_score, 2),

        "waste_score":
            round(waste_score, 2),

        "air_quality_score":
            round(aqi_score, 2),

        "occupancy_score":
            round(occupancy_score, 2),

        "incident_score":
            round(incident_score, 2)
    }


    return scores