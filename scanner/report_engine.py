from port_scanner import open_ports

def generate_summary(open_ports):

    summary = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }

