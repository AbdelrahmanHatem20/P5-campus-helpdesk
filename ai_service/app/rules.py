# Keywords used to detect the ticket category
CATEGORY_RULES = {
    "WiFi": [
        "wifi",
        "wi-fi",
        "wireless"
    ],

    "Network": [
        "internet",
        "network",
        "connection",
        "router",
        "ethernet"
    ],

    "Computer": [
        "computer",
        "pc",
        "laptop",
        "desktop"
    ],

    "Printer": [
        "printer",
        "printing",
        "print"
    ],

    "Projector": [
        "projector",
        "projection"
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

    "Electricity": [
        "electricity",
        "power",
        "socket",
        "plug",
        "electric"
    ],

    "Lighting": [
        "light",
        "lights",
        "lighting",
        "lamp",
        "bulb"
    ],

    "Air Conditioning": [
        "air conditioner",
        "air conditioning",
        "air conditioning unit",
        "ac"
    ],

    "Furniture": [
        "chair",
        "desk",
        "table",
        "furniture",
        "seat"
    ],

    "Cleanliness": [
        "dirty",
        "cleaning",
        "trash",
        "garbage",
        "dust",
        "clean",
        "waste"
    ],

    "Plumbing": [
        "water",
        "leak",
        "pipe",
        "plumbing",
        "faucet",
        "toilet",
        "sink"
    ]
}


# Emergency keywords
EMERGENCY_KEYWORDS = [
    "fire",
    "smoke",
    "gas leak",
    "danger",
    "emergency",
    "life threatening"
]


# Priority Matrix: Impact x Urgency
PRIORITY_MATRIX = {
    "Low": {
        "Low": "Low",
        "Medium": "Low",
        "High": "Medium"
    },

    "Medium": {
        "Low": "Low",
        "Medium": "Medium",
        "High": "High"
    },

    "High": {
        "Low": "High",
        "Medium": "High",
        "High": "Critical"
    }
}