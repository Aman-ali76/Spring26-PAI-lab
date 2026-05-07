"""
Step 4 — Offense → Section Mapping
Maps 26 common offense types to their relevant law sections + reporting agency
To add a new offense: copy one block and fill in the fields
"""


def get_offense_map():
    print("\n[STEP 4] Building offense → section map...")

    offense_map = {

        # ── CYBER OFFENSES ────────────────────────────────────────
        "online_harassment": {
            "description": "Harassment, abuse or intimidation conducted online",
            "laws":        [{"name": "PECA 2016", "sections": ["16", "20", "24"]}],
            "report_to":   ["FIA — 1991", "NCCIA — helpdesk@nr3c.gov.pk", "DRF — 0800-39393"],
            "portal":      "https://complaint.fia.gov.pk",
        },
        "cyberstalking": {
            "description": "Digitally following, monitoring or tracking a person",
            "laws":        [{"name": "PECA 2016", "sections": ["16"]}],
            "report_to":   ["FIA — 1991", "NCCIA"],
            "portal":      "https://complaint.fia.gov.pk",
        },
        "non_consensual_images": {
            "description": "Sharing intimate/explicit images without consent",
            "laws":        [{"name": "PECA 2016", "sections": ["14", "24"]}],
            "report_to":   ["FIA — 1991", "DRF — 0800-39393"],
            "portal":      "https://complaint.fia.gov.pk",
        },
        "hacking": {
            "description": "Unauthorized access to computer systems or networks",
            "laws":        [{"name": "PECA 2016", "sections": ["3", "4", "5", "6"]}],
            "report_to":   ["FIA — 1991", "NCCIA"],
            "portal":      "https://complaint.fia.gov.pk",
        },
        "online_fraud": {
            "description": "Financial fraud, phishing or scams conducted online",
            "laws":        [
                {"name": "PECA 2016",  "sections": ["10"]},
                {"name": "PPC 1860",   "sections": ["420", "468"]},
            ],
            "report_to":   ["FIA — 1991", "FBR — 051-111-772-772"],
            "portal":      "https://complaint.fia.gov.pk",
        },
        "fake_news_online": {
            "description": "Spreading deliberate misinformation or fake news online",
            "laws":        [{"name": "PECA 2016", "sections": ["20", "26-A"]}],
            "report_to":   ["FIA — 1991", "NCCIA"],
            "portal":      "https://complaint.fia.gov.pk",
        },
        "hate_speech_online": {
            "description": "Posting content promoting religious/racial/sectarian hatred",
            "laws":        [{"name": "PECA 2016", "sections": ["21"]}],
            "report_to":   ["FIA — 1991", "PTA — complaint@pta.gov.pk"],
            "portal":      "https://complaint.fia.gov.pk",
        },
        "cyber_terrorism": {
            "description": "Using internet to threaten national security or terrorize",
            "laws":        [{"name": "PECA 2016", "sections": ["9"]}],
            "report_to":   ["FIA — 1991", "NACTA"],
            "portal":      "https://complaint.fia.gov.pk",
        },
        "child_pornography": {
            "description": "Production, distribution or possession of CSAM",
            "laws":        [{"name": "PECA 2016", "sections": ["25"]}],
            "report_to":   ["FIA — 1991", "NCCIA"],
            "portal":      "https://complaint.fia.gov.pk",
        },
        "spam": {
            "description": "Sending unsolicited bulk messages or emails",
            "laws":        [{"name": "PECA 2016", "sections": ["17"]}],
            "report_to":   ["PTA — 0800-55055"],
            "portal":      "https://complaint.pta.gov.pk",
        },
        "illegal_sim": {
            "description": "Illegal SIM card, IMEI tampering or SIM box fraud",
            "laws":        [{"name": "PECA 2016", "sections": ["19"]}],
            "report_to":   ["PTA — 0800-55055"],
            "portal":      "https://complaint.pta.gov.pk",
        },
        "electronic_forgery": {
            "description": "Forging digital documents, fake degrees or IDs",
            "laws":        [{"name": "PECA 2016", "sections": ["11"]}],
            "report_to":   ["FIA — 1991", "NCCIA"],
            "portal":      "https://complaint.fia.gov.pk",
        },

        # ── PHYSICAL OFFENSES (PPC) ───────────────────────────────
        "murder": {
            "description": "Intentional killing of a person",
            "laws":        [{"name": "PPC 1860", "sections": ["302"]}],
            "report_to":   ["Police — 15"],
            "portal":      "https://complaint.punjabpolice.gov.pk",
        },
        "rape": {
            "description": "Sexual assault or rape",
            "laws":        [{"name": "PPC 1860", "sections": ["375", "376"]}],
            "report_to":   ["Police — 15", "Women Helpline — 1043"],
            "portal":      "https://complaint.punjabpolice.gov.pk",
        },
        "assault": {
            "description": "Physical assault or use of criminal force",
            "laws":        [{"name": "PPC 1860", "sections": ["351", "354", "354-A"]}],
            "report_to":   ["Police — 15"],
            "portal":      "https://complaint.punjabpolice.gov.pk",
        },
        "defamation": {
            "description": "Making false statements to damage someone's reputation",
            "laws":        [
                {"name": "PPC 1860",  "sections": ["499", "500"]},
                {"name": "PECA 2016", "sections": ["20"]},
            ],
            "report_to":   ["Police — 15", "FIA — 1991", "Court"],
            "portal":      "https://complaint.fia.gov.pk",
        },
        "criminal_intimidation": {
            "description": "Threatening a person with harm or death",
            "laws":        [{"name": "PPC 1860", "sections": ["503", "506"]}],
            "report_to":   ["Police — 15"],
            "portal":      "https://complaint.punjabpolice.gov.pk",
        },
        "woman_modesty": {
            "description": "Insulting modesty or eve-teasing of a woman",
            "laws":        [{"name": "PPC 1860", "sections": ["509", "354"]}],
            "report_to":   ["Police — 15", "Women Helpline — 1043"],
            "portal":      "https://complaint.punjabpolice.gov.pk",
        },
        "fraud_cheating": {
            "description": "Cheating, forgery or dishonest inducement",
            "laws":        [{"name": "PPC 1860", "sections": ["420", "468", "469"]}],
            "report_to":   ["Police — 15", "FIA — 1991", "NAB — 1800-888-999"],
            "portal":      "https://complaint.fia.gov.pk",
        },

        # ── WORKPLACE / GENDER ────────────────────────────────────
        "workplace_harassment": {
            "description": "Sexual or other harassment at the workplace",
            "laws":        [{"name": "Protection Against Harassment of Women at Workplace Act 2010", "sections": ["3", "4", "5"]}],
            "report_to":   ["Wafaqi Mohtasib — 1055", "NCHR"],
            "portal":      "https://www.mohtasib.gov.pk/complaint",
        },

        # ── FINANCIAL / CORPORATE ─────────────────────────────────
        "corruption": {
            "description": "Corruption, bribery or misuse of public office",
            "laws":        [{"name": "NAB Ordinance 1999", "sections": ["9", "10"]}],
            "report_to":   ["NAB — 1800-888-999"],
            "portal":      "https://www.nab.gov.pk/complaint",
        },
        "tax_evasion": {
            "description": "Evasion of income tax or other taxes",
            "laws":        [{"name": "Income Tax Ordinance 2001", "sections": ["192", "193"]}],
            "report_to":   ["FBR — 051-111-772-772"],
            "portal":      "https://iris.fbr.gov.pk",
        },
        "corporate_fraud": {
            "description": "Fraud in corporate or company affairs",
            "laws":        [{"name": "Companies Act 2017", "sections": ["462", "463"]}],
            "report_to":   ["SECP — 0800-88008"],
            "portal":      "https://xs.secp.gov.pk",
        },
        "banking_fraud": {
            "description": "Fraud in banking or financial transactions",
            "laws":        [{"name": "Banking Companies Ordinance 1962", "sections": ["25-A"]}],
            "report_to":   ["SBP — 111-727-273", "FIA — 1991"],
            "portal":      "https://www.sbp.org.pk/cpd/complaint.asp",
        },
        "money_laundering": {
            "description": "Laundering proceeds of crime through the financial system",
            "laws":        [{"name": "Anti-Money Laundering Act 2010", "sections": ["3", "4"]}],
            "report_to":   ["FIA — 1991", "FMU"],
            "portal":      "https://complaint.fia.gov.pk",
        },

        # ── NARCOTICS / MEDIA ─────────────────────────────────────
        "drug_possession": {
            "description": "Possession or trafficking of narcotics or drugs",
            "laws":        [{"name": "Control of Narcotic Substances Act 1997", "sections": ["6", "9"]}],
            "report_to":   ["Police — 15", "ANF"],
            "portal":      "https://complaint.punjabpolice.gov.pk",
        },
        "media_complaint": {
            "description": "Complaint against TV channel, radio or news media",
            "laws":        [{"name": "PEMRA Ordinance 2002", "sections": ["27", "29"]}],
            "report_to":   ["PEMRA — 0800-73672"],
            "portal":      "https://www.pemra.gov.pk/complaints",
        },
    }

    print(f"  ✅ {len(offense_map)} offense mappings built")
    return offense_map
