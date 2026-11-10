# Sample data: verify names, coordinates and village counts before presenting.
LAKES = [  # name, district, lat, lon, villages at risk, vulnerability weight
    ("Golen Gol", "Chitral", 35.92, 71.82, 12, 1.20),
    ("Reshun Glacial Lake", "Chitral", 36.15, 72.10, 9, 1.15),
    ("Arkari Water Basin", "Chitral", 36.00, 71.50, 5, 0.80),
    ("Shisper Glacier Lake", "Hunza", 36.43, 74.77, 8, 1.10),
    ("Hinarchi", "Nagar", 36.28, 74.80, 9, 0.95),
    ("Badswat", "Ghizer", 36.35, 73.55, 5, 0.70),
    ("Chiantar Glacier Pool", "Hunza", 36.80, 73.05, 4, 0.60),
]
VILLAGES = ["Buni", "Golen", "Mogh", "Reshun", "Kuru", "Other"]
EVENTS = {  # temperature slider, lake expansion slider, note
    "Normal baseline": (6.5, 12, "Calm starting point, below the 8 °C and 20% alert lines."),
    "Reshun flood (2015)": (15.0, 30, "16 Jul 2015 reanalysis max at 4,100 m was 17.1 °C, so temperature sits on the 15 °C slider cap. Lake area was not mapped; expansion is set to 30%."),
    "Shisper surge (2019)": (13.0, 50, "Snout-level max was 13.0 °C on 19 Jun 2019. The lake grew from 0.042 km² (Nov 2018) to about 0.35 km², so expansion is maxed at 50%."),
}
MESSAGES = {
    "Urdu": "خبردار: سار-آب نظام کی طرف سے الرٹ۔ چترال کے بالائی گلیشیئر میں پانی کا بہاؤ بڑھ گیا ہے۔ ندی نالوں سے دور رہیں اور انتظامیہ کی ہدایات پر عمل کریں۔",
    "Pashto": "خبرداری: د سار-آب سیسټم له لوري بیړنی خبرداری. په چترال کې د ګلیشیر ویلې کیدو له امله د سیند کچه لوړه شوې. د سیند غاړو ته مه ځئ.",
    "English": "Warning from Sar-Ab: water flow near {lake} has risen sharply. Stay away from streams and follow district administration instructions.",
}
TILES = [  # name, url, attribution (the first one is the default map)
    ("Satellite", "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", "Tiles © Esri"),
    ("Terrain", "https://tile.opentopomap.org/{z}/{x}/{y}.png", "© OpenTopoMap, © OpenStreetMap contributors"),
    ("Street map", "https://tile.openstreetmap.org/{z}/{x}/{y}.png", "© OpenStreetMap contributors"),
]
