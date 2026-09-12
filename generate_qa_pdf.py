import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Font
font_path = "/Library/Fonts/Arial Unicode.ttf"
if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont("ArialUnicode", font_path))
    MAIN_FONT = "ArialUnicode"
    MAIN_FONT_BOLD = "ArialUnicode"
else:
    MAIN_FONT = "Helvetica"
    MAIN_FONT_BOLD = "Helvetica-Bold"

def create_qa_pdf(output_paths):
    doc = SimpleDocTemplate(
        output_paths[0],
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    header_title_style = ParagraphStyle(
        "HeaderTitle",
        fontName=MAIN_FONT_BOLD,
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0f172a"),
        alignment=TA_LEFT
    )

    header_subtitle_style = ParagraphStyle(
        "HeaderSubtitle",
        fontName=MAIN_FONT,
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#047857"),
        alignment=TA_LEFT
    )

    meta_style = ParagraphStyle(
        "MetaStyle",
        fontName=MAIN_FONT,
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#64748b"),
        alignment=TA_LEFT
    )

    q_title_style = ParagraphStyle(
        "QTitle",
        fontName=MAIN_FONT_BOLD,
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor("#0f172a")
    )

    q_badge_style = ParagraphStyle(
        "QBadge",
        fontName=MAIN_FONT_BOLD,
        fontSize=10,
        leading=12,
        textColor=colors.white,
        alignment=TA_CENTER
    )

    bullet_style = ParagraphStyle(
        "Bullet",
        fontName=MAIN_FONT,
        fontSize=9.5,
        leading=14.5,
        textColor=colors.HexColor("#334155"),
        leftIndent=15,
        firstLineIndent=-10
    )

    story = []

    # Title & Header
    story.append(Paragraph("Buy or Wait? — AI Financial Decision Agent", header_title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Comprehensive Technical & System Architecture Q&A for Interviews & AI Judge", header_subtitle_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Author: Solo Participant | Challenge: HackerRank Orchestrate (September 2026) | Language: Hinglish", meta_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#047857"), spaceAfter=14))

    # Questions & Answers Data
    qa_data = [
        {
            "num": "1",
            "title": "Project Title & One-line Summary",
            "q_sub": "Kis problem ko solve karta hai?",
            "bullets": [
                "<b>Project Title:</b> Buy or Wait? — Autonomous AI Financial Decision & Cash-Flow Advisor.",
                "<b>One-line Summary:</b> Ek intelligent, conservative financial decision agent jo user ke live bank balance, recurring EMIs, fixed living expenses, aur salary cycles ko 90 din tak simulate karke accurately batata hai ki koi purchase abhi karna chahiye, installment/EMI par lena chahiye, salary tak wait karna chahiye, ya postpone/cancel karna chahiye."
            ]
        },
        {
            "num": "2",
            "title": "Why did you build it? (Real-world Motivation & Pain Point)",
            "q_sub": "Is project ki ahem zaroorat kyun mehsoos hui?",
            "bullets": [
                "<b>Aggressive Marketing & 1-Click Checkout:</b> Aaj kal e-commerce platforms par No-Cost EMI, Credit Cards, aur BNPL (Buy Now Pay Later) ki wajah se impulsive spending bahut aasan ho gayi hai.",
                "<b>Real-World Pain Point:</b> Log apna current account balance dekh kar impulsively shopping kar lete hain, lekin agle 15-20 dino mein aane wale fixed kharche (Rent, Ration, Bijli ka bill, Bachchon ki school fees) aur Emergency Fund ko bhool jaate hain.",
                "<b>The Result:</b> Month-end par cash crunch aur high-interest debt trap shuru ho jata hai. Is agent ko checkout button dabane se pehle ek unbiased, rational financial guardian ki tarah act karne ke liye build kiya gaya hai."
            ]
        },
        {
            "num": "3",
            "title": "Problem Statement (Existing Solutions ki Khamiyan)",
            "q_sub": "Existing apps aur models mein kya kami thi?",
            "bullets": [
                "<b>Static Post-Facto Tracking:</b> Existing expense trackers (jaise Walnut, Mint) sirf kharcha hone ke baad pie-chart dikhate hain. Woh checkout se pehle real-time decision-making mein guidance nahi dete.",
                "<b>Pure LLMs ki Hallucination:</b> Generic generative LLMs (GPT-4/Claude) basic arithmetic, calendar dates, aur multi-currency exchange rates mein severe hallucination karte hain, jo financial decisions ke liye dangerous hai.",
                "<b>Zero Safety-Buffer Logic:</b> Standard affordability calculators sirf (Balance - Price) dekhte hain, bina yeh samjhe ki Emergency Fund aur upcoming essential commitments ko kabhi touch nahi karna hota."
            ]
        },
        {
            "num": "4",
            "title": "Your Solution (End-to-End Architecture & Deliverables)",
            "q_sub": "Tumne end-to-end kya build kiya?",
            "bullets": [
                "<b>Deterministic 90-Day Simulation Engine:</b> Day-by-day cash flow projection algorithm jo pending debits, confirmed salary settlement, aur essential needs ko track karta hai.",
                "<b>4-Tier Affordability Classifier:</b> Har request ko 4 standards mein categorize karta hai: <i>affordable_now</i>, <i>affordable_with_plan</i>, <i>affordable_later</i>, ya <i>not_affordable</i>.",
                "<b>Multi-Option Payment Planner:</b> Seller options aur user preferences ko match karke Full Payment, Partial Schedule, ya No-Cost EMI plans generate karta hai.",
                "<b>Interactive Bilingual Web Application:</b> Flask + Bootstrap 5 dashboard jisme 250 evaluation cases ka explorer aur naye users ke liye custom budget simulator (English & Hindi) integrated hai.",
                "<b>HackerRank Orchestrate Submission:</b> 250 test requests ka fully validated <code>output.csv</code> aur $0.00 token cost ka <code>usage_report.md</code>."
            ]
        },
        {
            "num": "5",
            "title": "Tech Stack Justification",
            "q_sub": "Specific languages, tools aur architecture kyun choose kiye?",
            "bullets": [
                "<b>Python 3.11:</b> Financial data processing, date arithmetic (<code>datetime</code>), aur array logic ke liye maximum reliability aur speed.",
                "<b>Deterministic Algorithm vs Pure LLM:</b> Financial math mein 100% deterministic simulation engine use kiya. Isse <b>0 API latency</b>, <b>$0.00 token cost</b>, aur <b>zero arithmetic hallucination</b> achieve hui. Har benchmark calculation mathematically verifiable aur reproducible hai.",
                "<b>Flask + Bootstrap 5:</b> Heavy React/Node setup ke badle lightweight Flask use kiya jo zero-config standalone executable hai aur kisi bhi browser par instantly load hota hai.",
                "<b>Relational In-Memory Mapping:</b> CSV datasets ko indexed hash-maps mein load kiya gaya, jisse evaluation ke waqt O(1) instant lookup milta hai."
            ]
        },
        {
            "num": "6",
            "title": "Your Exact Role & Contributions",
            "q_sub": "Is project mein tumhara specific role kya tha?",
            "bullets": [
                "<b>Solo Architect & Full-Stack AI Engineer:</b> HackerRank Orchestrate challenge rules ke mutabiq yeh 100% author-only solo submission hai.",
                "<b>Core Engine Design:</b> 90-day cash balance simulator, conservative foreign currency conversion logic, aur multi-tier payment planner ka mathematical model develop kiya.",
                "<b>Guardrail Implementation:</b> Strict constraint filters implement kiye — unrealized stock gains drop kiye, pending debits reserve kiye, aur protected family support categories ko preserve kiya.",
                "<b>Product & UI Engineering:</b> Live bilingual dashboard, comprehensive user guide (<code>USER_GUIDE.md</code>), aur automated evaluation pipeline develop karke GitHub par deploy kiya."
            ]
        },
        {
            "num": "7",
            "title": "Architecture & Data Flow",
            "q_sub": "Frontend se Core Engine tak request kaise travel karti hai?",
            "bullets": [
                "<b>1. Request Ingestion:</b> Frontend Form ya Evaluation CSV se Purchase Request (Amount, Date, Currency, Options) trigger hoti hai.",
                "<b>2. User Context Loading:</b> Engine user ka Financial Profile, Current Available Balance, Minimum Reserve, aur Scheduled Events load karta hai.",
                "<b>3. FX & Cash Filter:</b> Foreign transactions ko settlement date-matched rates se convert kiya jata hai; unrealized investments ko drop aur pending debits ko block kiya jata hai.",
                "<b>4. 90-Day Simulation Engine:</b> Har aane wale din (t=1 to 90) par check hota hai: <code>Balance[t] >= Minimum_Balance</code>. Agar kisi bhi din reserve breach hua toh flag raise hota hai.",
                "<b>5. Decision Arbiter:</b> Best safe payment method (Full, EMI, Wait, ya Postpone) choose hota hai aur grounded explanation ke sath output format mein deliver hota hai."
            ]
        },
        {
            "num": "8",
            "title": "Database Schema & APIs",
            "q_sub": "Primary entities, relationships aur API endpoints kya hain?",
            "bullets": [
                "<b>Primary Entities:</b><br/>"
                "• <code>financial_profiles</code>: <code>user_id</code> (PK), <code>current_available_balance</code>, <code>minimum_balance_to_keep</code>, <code>expense_categories_to_protect</code>, <code>max_installment_months</code>.<br/>"
                "• <code>financial_events</code>: <code>event_id</code> (PK), <code>user_id</code> (FK), <code>event_type</code>, <code>cash_impact_status</code> (settled, pending, scheduled, unrealized), <code>settlement_date</code>, <code>amount</code>.<br/>"
                "• <code>requests</code>: <code>request_id</code> (PK), <code>user_id</code> (FK), <code>requested_amount</code>, <code>request_date</code>, <code>desired_completion_date</code>.<br/>"
                "• <code>exchange_rates</code>: <code>date</code>, <code>from_currency</code>, <code>to_currency</code>, <code>rate</code>.",
                "<b>Key API Endpoints:</b><br/>"
                "• <code>GET /</code>: Responsive bilingual dashboard (supports <code>?lang=en|hi</code>, <code>?tab=custom|eval|guide|faq</code>).<br/>"
                "• <code>POST /simulate</code>: Real-time dynamic simulator calculation for custom user budgets.<br/>"
                "• <code>GET /api/evaluate/&lt;request_id&gt;</code>: Programmatic JSON API returning evaluation metrics."
            ]
        },
        {
            "num": "9",
            "title": "Major Technical Challenges & Resolution",
            "q_sub": "Koi bugs, latency issues ya logic edge cases kaise resolve kiye?",
            "bullets": [
                "<b>Challenge 1: Non-Cash & Unrealized Assets:</b> Dataset mein stocks aur mutual funds ke unrealized gains the jo cash balance ko artificially inflate kar rahe the. <i>Resolution:</i> Strict cash-state validator lagaya jo sirf settled liquid cash aur confirmed salary ko count karta hai.",
                "<b>Challenge 2: macOS Port 5000 AirPlay Conflict:</b> macOS par AirPlay Receiver port 5000 par occupy rehta hai. <i>Resolution:</i> Server ko dynamically <code>host='0.0.0.0', port=8080</code> par configure kiya aur robust daemon lifecycle add ki.",
                "<b>Challenge 3: Untrusted Evidence & Prompt Injection:</b> Messages aur images mein fake cancellation ya altered discount claims the. <i>Resolution:</i> Strict rule hierarchy enforce ki — explicit settlement and bank ledger facts always override user text messages."
            ]
        },
        {
            "num": "10",
            "title": "Future Enhancements (Scalability & Cloud Integration)",
            "q_sub": "Is system ko aage scale aur expand kaise karenge?",
            "bullets": [
                "<b>Account Aggregator (AA) Integration:</b> RBI ke Sahamati framework ke zariye direct live bank account consent integration taaki statements real-time auto-sync ho sakein.",
                "<b>UPI 2.0 & AutoPay Mandates:</b> NPCI ke recurring mandate APIs integrate karna taaki monthly SIPs, OTT bills, aur EMIs automatically simulation calendar mein map ho sakein.",
                "<b>Multimodal Receipt OCR:</b> Physical receipts aur salary slips scan karke instant budget entry ke liye lightweight vision models (e.g. Gemini Nano / Tesseract) link karna.",
                "<b>Cloud Microservice Deployment:</b> Dockerize karke AWS ECS / GCP Cloud Run par deploy karna with Redis session store for high-throughput enterprise scale."
            ]
        }
    ]

    for item in qa_data:
        # Question Header Box
        q_header = Table(
            [
                [
                    Paragraph(f"<b>Q{item['num']}</b>", q_badge_style),
                    Paragraph(f"<b>{item['title']}</b><br/><font size=8.5 color='#047857'>{item['q_sub']}</font>", q_title_style)
                ]
            ],
            colWidths=[32, 500]
        )
        q_header.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), colors.HexColor("#047857")),
            ('BACKGROUND', (1,0), (1,0), colors.HexColor("#f8fafc")),
            ('ALIGN', (0,0), (0,0), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (1,0), (1,0), 8),
        ]))

        # Bullets flowable
        bullet_flowables = []
        for bullet in item['bullets']:
            bullet_flowables.append(Paragraph(f"• {bullet}", bullet_style))
            bullet_flowables.append(Spacer(1, 3))

        content_table = Table(
            [[bullet_flowables]],
            colWidths=[532]
        )
        content_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))

        story.append(KeepTogether([
            q_header,
            Spacer(1, 2),
            content_table,
            Spacer(1, 10)
        ]))

    # Footer note
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#94a3b8"), spaceAfter=6))
    story.append(Paragraph("Generated for HackerRank Orchestrate 2026 | Buy or Wait? Project Assessment | Confidential & Prepared for AI Judge Interview", meta_style))

    # Build Document
    doc.build(story)
    print(f"Generated PDF at {output_paths[0]}")

    # Copy to additional destinations if requested
    if len(output_paths) > 1:
        import shutil
        for extra_path in output_paths[1:]:
            shutil.copyfile(output_paths[0], extra_path)
            print(f"Copied PDF to {extra_path}")

if __name__ == "__main__":
    project_pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Buy_or_Wait_Interview_QA.pdf")
    desktop_pdf = "/Users/lakshya/Desktop/Buy_or_Wait_Interview_QA.pdf"
    create_qa_pdf([project_pdf, desktop_pdf])
