def calculate_risk(cvss):

    if cvss >= 9:
        return "CRITICAL"

    elif cvss >= 7:
        return "HIGH"

    elif cvss >= 4:
        return "MEDIUM"

    elif cvss > 0:
        return "LOW"

    return "NONE"