#!/usr/bin/env python3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

CAMBRIDGE_BLUE = colors.Color(142/255, 232/255, 216/255)  # #8EE8D8

BLOCK_TITLES = [
    "Block 1: Early Season Focus",
    "Block 2: Mid-Season Development",
    "Block 3: Pre-Race Preparation",
]

PRINCIPLES = [
    "Posture & Alignment",
    "Rhythm & Cadence",
    "Efficiency & Relaxation",
    "Tactical Awareness",
    "Competitive Intent",
]

def draw_header(c, width, height, page_label, color=True):
    if color:
        c.setFillColor(CAMBRIDGE_BLUE)
        c.rect(0, height-70, width, 70, fill=1, stroke=0)
        c.setFillColor(colors.black)
    else:
        c.setFillColor(colors.black)
        c.rect(0, height-70, width, 70, fill=0, stroke=1)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height-40, "CUBC - W")
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(width/2, height-55, f"Controlling my Controllables – A Reflective Performance Journey ({page_label})")

def draw_block(c, form, width, height, block_index, title, mock=False):
    y = height - 100
    # Section title
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, title)
    y -= 20

    # Reflection prompts
    c.setFont("Helvetica", 10)
    questions = [
        ("race_goal", "What are we trying to achieve when we race?"),
        ("principles", "Key principles of running effectively (in your own words):"),
        ("feel_look", "What does effective racing feel and look like to me?")
    ]

    mock_values = [
        "Control the base rhythm, stay long through the mid‑1k, attack in last 500m.",
        "Tall posture, relaxed shoulders, clean catches, connected drive, quiet recovery.",
        "Calm, elastic rhythm; blades drop in without splash; boat runs between strokes."
    ]

    for idx, (fname, label) in enumerate(questions):
        c.drawString(40, y, label)
        value = mock_values[idx] if mock else ""
        form.textfield(
            name=f"{fname}_{block_index}",
            x=300, y=y-5, width=220, height=15,
            value=value
        )
        y -= 30

    # Review dates
    c.drawString(40, y, "Review Date:")
    form.textfield(name=f"review_{block_index}", x=130, y=y-5, width=80, height=15,
                   value=("2025-11-01" if mock and block_index==0 else ""))
    c.drawString(250, y, "Next Review Date:")
    form.textfield(name=f"nextreview_{block_index}", x=380, y=y-5, width=80, height=15,
                   value=("2025-11-21" if mock and block_index==0 else ""))
    y -= 30

    # Principles table
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y, "Performance Principles Dual Assessment (E/D/A/O) + Comments")
    y -= 15
    c.setFont("Helvetica", 9)

    # Provide mock rating/comments for block progression
    mock_scale = [
        ("D", "Finding length under pressure"),
        ("A", "Cadence consistent in crosswind"),
        ("D", "Breathing + relax on recovery"),
        ("D", "Better calls at 750m"),
        ("A", "Owning rhythm in base pace"),
    ]
    mock_scale_mid = [
        ("A", "Hips under, chest open"),
        ("A", "Rate control improving"),
        ("A", "Looser shoulders in 3rd 500"),
        ("A", "Reads field; holds lane"),
        ("A", "Initiates push in last 600"),
    ]
    mock_scale_pre = [
        ("O", "Tall & stacked at catch"),
        ("A", "Base rate locked"),
        ("A", "Relaxed under max effort"),
        ("A", "Anticipates surges early"),
        ("O", "Confident race identity"),
    ]
    mock_tables = [mock_scale, mock_scale_mid, mock_scale_pre]

    for i, p in enumerate(PRINCIPLES):
        c.drawString(40, y, p)
        # Athlete rating
        form.textfield(name=f"{p[:6]}_a_{block_index}", x=200, y=y-5, width=40, height=15,
                       value=(mock_tables[block_index][i][0] if mock else ""))
        # Athlete comment
        form.textfield(name=f"{p[:6]}_ac_{block_index}", x=260, y=y-5, width=100, height=15,
                       value=(mock_tables[block_index][i][1] if mock else ""))
        # Coach rating
        form.textfield(name=f"{p[:6]}_c_{block_index}", x=380, y=y-5, width=40, height=15,
                       value=(mock_tables[block_index][i][0] if mock else ""))
        # Coach comment
        coach_note = "" if not mock else ("Good progress" if block_index==0 else ("Sharper entries" if block_index==1 else "Ready to race"))
        form.textfield(name=f"{p[:6]}_cc_{block_index}", x=440, y=y-5, width=100, height=15,
                       value=coach_note)
        y -= 25

    # Ownership actions
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y, "Ownership Actions")
    y -= 15
    lines = [
        ("focus", "One focus area I will work on this block:"),
        ("success", "What success will look/feel like:"),
        ("account", "Coach accountability:"),
    ]
    mock_actions = [
        "Hold rhythm through crosswind; keep catches clean.",
        "Boat runs with minimal check; consistent split at base pace.",
        "Ask for feedback on catch timing each session."
    ]
    for idx, (fname, label) in enumerate(lines):
        c.drawString(40, y, label)
        value = (mock_actions[idx] if mock else "")
        form.textfield(name=f"{fname}_{block_index}", x=300, y=y-5, width=220, height=15, value=value)
        y -= 25

    # Progress tracker
    c.setFont("Helvetica", 10)
    c.drawString(40, y, "Progress Tracker (0-100%):")
    c.rect(180, y-5, 200, 10, stroke=1, fill=0)  # manual shading bar
    form.textfield(name=f"progress_{block_index}", x=400, y=y-8, width=40, height=15,
                   value=("65" if mock and block_index==0 else ("78" if mock and block_index==1 else ("88" if mock and block_index==2 else ""))))
    y -= 30

    # Coach notes
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y, "Coach Notes:")
    form.textfield(name=f"coachnote_{block_index}", x=150, y=y-5, width=370, height=40,
                   value=("Composure improving; keep quiet top hand." if mock else ""))

def draw_dashboard(c, width, height, form, color=True, mock=False):
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height-100, "Coach Summary Dashboard")
    c.setFont("Helvetica", 10)
    c.drawString(40, height-120, "Athlete Performance Overview")

    headers = ["Athlete", "Posture", "Rhythm", "Efficiency", "Awareness", "Intent"]
    x_positions = [40, 150, 230, 310, 390, 470]
    y = height - 140

    for i, h in enumerate(headers):
        if color:
            c.setFillColor(CAMBRIDGE_BLUE)
            c.rect(x_positions[i], y, 70, 20, fill=1, stroke=0)
            c.setFillColor(colors.black)
        else:
            c.rect(x_positions[i], y, 70, 20, stroke=1, fill=0)
        c.drawCentredString(x_positions[i] + 35, y+7, h)

    y -= 25
    sample_rows = [
        ("J. Smith", "A", "A", "D", "A", "A"),
        ("L. Evans", "D", "A", "A", "D", "A"),
        ("R. Brown", "A", "D", "A", "A", "A"),
    ]
    for row in range(10):
        for i in range(6):
            c.rect(x_positions[i], y, 70, 18, stroke=1, fill=0)
        if mock and row < len(sample_rows):
            vals = sample_rows[row]
            c.setFont("Helvetica", 9)
            c.drawString(x_positions[0]+3, y+4, vals[0])
            for col in range(1, 6):
                c.drawString(x_positions[col]+30, y+4, vals[col])
        y -= 20

def build_pdf(output_path: str, mock: bool):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    form = c.acroForm
    # Three blocks
    for i, title in enumerate(BLOCK_TITLES):
        draw_header(c, width, height, "Digital Edition", color=True)
        draw_block(c, form, width, height, i, title, mock=mock)
        c.showPage()
    # Dashboard
    draw_header(c, width, height, "Digital Edition", color=True)
    draw_dashboard(c, width, height, form, color=True, mock=mock)
    c.save()

if __name__ == "__main__":
    build_pdf("CUBC_IDP_Digital_Blank.pdf", mock=False)
    build_pdf("CUBC_IDP_Digital_MockFilled.pdf", mock=True)
    print("Generated: CUBC_IDP_Digital_Blank.pdf, CUBC_IDP_Digital_MockFilled.pdf")
