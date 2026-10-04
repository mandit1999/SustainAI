def generate_recommendation(category, value):

    if category == "Electricity":
        return (
            "Investigate abnormal electricity consumption. "
            "Check HVAC systems, lighting, and high-energy equipment."
        )

    elif category == "Water":
        return (
            "Check for water leakage, abnormal usage, "
            "and plumbing-system issues."
        )

    elif category == "Waste":
        return (
            "Investigate the source of increased waste generation "
            "and review waste segregation practices."
        )

    elif category == "Air Quality":
        return (
            "Monitor air quality and inspect ventilation, "
            "filtration, and indoor air circulation."
        )

    else:
        return "Investigate the abnormal facility metric."