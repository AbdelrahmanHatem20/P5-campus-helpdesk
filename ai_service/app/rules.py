# app/rules.py

# Keywords used to detect the ticket category
CATEGORY_RULES = {
    "Network": [
        "wifi",
        "wi-fi",
        "internet",
        "network",
        "connection",
        "router",
        "ethernet"
    ],

    "Hardware": [
        "computer",
        "pc",
        "laptop",
        "keyboard",
        "mouse",
        "monitor",
        "screen",
        "printer",
        "projector",
        "device"
    ],

    "Software": [
        "software",
        "application",
        "app",
        "program",
        "system",
        "login",
        "error",
        "crash",
        "bug"
    ],

    "Electrical": [
        "electricity",
        "power",
        "socket",
        "plug",
        "electric",
        "light",
        "lights"
    ],

    "Facilities": [
        "door",
        "chair",
        "desk",
        "room",
        "air conditioner",
        "air conditioning",
        "ac",
        "window"
    ],

    "Cleaning": [
        "dirty",
        "cleaning",
        "trash",
        "garbage",
        "dust",
        "clean"
    ],

    "Security": [
        "security",
        "access",
        "access card",
        "unauthorized",
        "lost card",
        "intruder"
    ]
}


# Keywords used to determine priority
PRIORITY_RULES = {
    "Critical": [
        "fire",
        "smoke",
        "danger",
        "emergency",
        "security breach",
        "life threatening"
    ],

    "High": [
        "urgent",
        "asap",
        "immediately",
        "not working",
        "cannot access",
        "can't access",
        "exam",
        "lecture",
        "deadline",
        "important"
    ],

    "Medium": [
        "slow",
        "intermittent",
        "sometimes",
        "problem",
        "issue",
        "unstable"
    ],

    "Low": [
        "request",
        "minor",
        "question",
        "when possible",
        "suggestion"
    ]
}