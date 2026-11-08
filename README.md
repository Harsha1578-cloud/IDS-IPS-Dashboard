
# IDS/IPS Deployment with Suricata

## Objective
Develop a security monitoring dashboard for intrusion detection and prevention using Suricata.

## Technologies Used
- Suricata IDS/IPS
- Kali Linux
- Visual Studio Code
- HTML, CSS and JavaScript

## Features
- Professional security operations dashboard
- Intrusion detection monitoring
- IPS rule documentation
- Security event and alert monitoring

## Project Status
Dashboard frontend created. Live event integration and IPS blocking verification are separate tasks to complete.

## Disclaimer
This project is intended for authorized testing in a controlled lab environment.
## Project Status

The Real-Time IDS/IPS Monitoring Dashboard integrates Suricata with a Python API and a web-based SOC dashboard. It displays live network events, timestamps, source and destination IP addresses, alert signatures, actions, and severity levels. The dashboard refreshes automatically and supports monitoring of network activity in the lab. The current setup demonstrates IDS monitoring; inline IPS traffic blocking has not yet been verified.
## Testing and Results

- **Real-time detection:** Suricata recorded network events in its log.
- **API integration:** A Python API provided event data to the web dashboard.
- **Live dashboard:** The SENTINEL dashboard displayed Suricata events.
- **IPS validation:** A controlled local test confirmed that matching traffic to the test server was dropped by the configured Suricata NFQUEUE rule.
- **Recovery verification:** After removing the temporary blocking rule, the local test server responded successfully again.

### Tools and Technologies
- Kali Linux
- Suricata IDS/IPS
- Python
- HTML, CSS and JavaScript
- Visual Studio Code
- Oracle VirtualBox

### Conclusion
This project demonstrates real-time security event monitoring, dashboard integration and a controlled IPS blocking test in a local lab environment.
