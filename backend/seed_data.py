"""
Seed data for AWS Data Center Expansion — Lubbock Region, Phase 2.

Targets:
  - 3 GCs: Turner Construction, Hensel Phelps, McCarthy Building Companies
  - 47 RFIs:  32 Closed, 11 In Review, 4 Open+overdue
  - 18 Submittals: 14 Approved, 3 Pending, 1 Rejected
  - 12 Change Orders: all Pending Approval, sum = exactly $1,870,000
  - 8 OFM items: 6 Green, 1 Amber, 1 Red
  - 5 Vendors: 2 Fully Onboarded, 2 Orientation Pending, 1 NDA Outstanding

Run: python seed_data.py  (from backend/ directory with venv active)
"""

import os
import sys
from datetime import date, timedelta

# Ensure the app package is importable
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.rfi import RFI
from app.models.submittal import Submittal
from app.models.change_order import ChangeOrder
from app.models.ofm import OFMItem
from app.models.vendor import Vendor

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./tracker.db")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

GCS = ["Turner Construction", "Hensel Phelps", "McCarthy Building Companies"]

SPEC_SECTIONS = [
    "03 30 00",   # Cast-in-Place Concrete
    "05 12 00",   # Structural Steel Framing
    "08 11 13",   # Hollow Metal Doors and Frames
    "23 00 00",   # HVAC
    "26 24 16",   # Panelboards
    "26 05 19",   # Low-Voltage Conductors
    "07 54 23",   # TPO Roofing
    "09 91 00",   # Painting
    "21 12 00",   # Fire Suppression Standpipes
    "28 13 00",   # Access Control
]

SUBMITTERS = [
    "J. Ramirez (Turner)", "K. Park (Hensel)", "D. Okonkwo (McCarthy)",
    "S. Chen (Turner)", "A. Vasquez (Hensel)",
]


def clear(db):
    for model in [RFI, Submittal, ChangeOrder, OFMItem, Vendor]:
        db.query(model).delete()
    db.commit()
    print("Cleared existing records.")


def seed_rfis(db):
    rfis = []

    # 32 Closed RFIs — dates range back 6 months
    closed_titles = [
        "Clarify concrete compressive strength at slab-on-grade",
        "Anchor bolt pattern for structural steel column base plates",
        "Hollow metal door frame installation at server room entry",
        "HVAC equipment clearance at mechanical mezzanine",
        "Panelboard location conflict with cable tray routing",
        "Confirm fire suppression head spacing in raised floor zone",
        "Paint finish specification for exterior mechanical screen walls",
        "Structural steel connection detail at roof level",
        "Conduit sleeve penetration detail through 2-hr rated wall",
        "Generator fuel line routing beneath slab",
        "Cooling tower connection to chilled water loop",
        "Raised floor pedestal height variation tolerance",
        "Grounding electrode conductor routing at main switchgear",
        "Expansion joint detail at building addition interface",
        "Emergency egress lighting photometrics at data hall",
        "Confirm door hardware schedule revision C applicability",
        "Seismic bracing requirement for 12-in duct runs",
        "TPO roofing overlap at penetration boot",
        "Rebar splice location at shear wall",
        "Cable tray support spacing above dropped ceiling",
        "Perforated ceiling tile specification in office wing",
        "Transformer pad dimensions and anchor bolt template",
        "Access control panel mounting height — ADA compliance",
        "Confirm busway plug-in unit ampacity",
        "Epoxy floor coating prep requirements at loading dock",
        "Pipe insulation specification for chilled water supply",
        "Firestop detail at duct penetration in 2-hr partition",
        "Stormwater detention pond outlet structure clarification",
        "Security camera conduit stub-out locations",
        "Interior signage mounting substrate at server corridors",
        "Confirm window unit types at break room façade",
        "Structural opening size for future generator addition",
    ]
    for i, title in enumerate(closed_titles, start=1):
        offset = i * 4  # spread over ~4 months
        rfis.append(RFI(
            rfi_number=f"RFI-{i:03d}",
            title=title,
            description=f"Field coordination required. See attached sketch RFI-{i:03d}-SK.",
            status="Closed",
            priority="Medium" if i % 3 != 0 else "Low",
            assigned_gc=GCS[i % 3],
            submitted_by=SUBMITTERS[i % 5],
            submitted_date=date(2025, 1, 6) + timedelta(days=offset),
            due_date=date(2025, 1, 20) + timedelta(days=offset),
            closed_date=date(2025, 1, 25) + timedelta(days=offset),
            spec_section=SPEC_SECTIONS[i % len(SPEC_SECTIONS)],
        ))

    # 11 In Review RFIs
    in_review_titles = [
        "Mechanical room clearance at secondary UPS area",
        "Confirm cable tray fill percentage — Zone B",
        "Roof drain leader pipe material specification",
        "Steel deck diaphragm attachment at re-entrant corner",
        "Low-voltage lighting control panel location at IT corridor",
        "Exterior insulation thickness at parapet detail",
        "Suspended slab reinforcement at equipment pad",
        "Fuel oil secondary containment liner material",
        "Interior metal partition attachment at existing structure",
        "Battery room ventilation rate calculation basis",
        "Loading dock leveler pit reinforcement detail",
    ]
    for j, title in enumerate(in_review_titles, start=len(closed_titles) + 1):
        offset = (j - len(closed_titles)) * 5  # spread due dates 5 days apart
        rfis.append(RFI(
            rfi_number=f"RFI-{j:03d}",
            title=title,
            description="Under technical review by design team. Response expected within 10 business days.",
            status="In Review",
            priority="High" if j % 4 == 0 else "Medium",
            assigned_gc=GCS[j % 3],
            submitted_by=SUBMITTERS[j % 5],
            submitted_date=date(2026, 3, 1) + timedelta(days=offset),
            due_date=date(2026, 4, 1) + timedelta(days=offset),  # future dates
            spec_section=SPEC_SECTIONS[j % len(SPEC_SECTIONS)],
        ))

    # 4 Open + overdue RFIs (due dates in the past)
    overdue_data = [
        ("Clarify seismic category for non-structural MEP bracing", "High", GCS[0], "03 30 00"),
        ("Confirm UPS battery room floor load capacity", "High", GCS[1], "26 24 16"),
        ("Exterior wall assembly R-value at thermal bridge", "Medium", GCS[2], "07 54 23"),
        ("Fire alarm notification appliance circuit wiring method", "High", GCS[0], "21 12 00"),
    ]
    for k, (title, priority, gc, spec) in enumerate(overdue_data, start=len(closed_titles) + len(in_review_titles) + 1):
        rfis.append(RFI(
            rfi_number=f"RFI-{k:03d}",
            title=title,
            description="OVERDUE — Immediate response required. Field work is blocked.",
            status="Open",
            priority=priority,
            assigned_gc=gc,
            submitted_by=SUBMITTERS[k % 5],
            submitted_date=date(2025, 11, 1),
            due_date=date(2025, 12, 1),  # past due
            spec_section=spec,
        ))

    db.add_all(rfis)
    db.commit()
    print(f"Seeded {len(rfis)} RFIs.")


def seed_submittals(db):
    subs = []

    # 14 Approved
    approved_data = [
        ("SUB-001", "03 30 00", "Concrete mix design — slab-on-grade", GCS[0], "Approved"),
        ("SUB-002", "05 12 00", "Structural steel shop drawings — columns", GCS[0], "Approved"),
        ("SUB-003", "05 12 00", "Structural steel shop drawings — beams", GCS[0], "Approved"),
        ("SUB-004", "08 11 13", "Hollow metal doors product data", GCS[1], "Approved"),
        ("SUB-005", "08 11 13", "Hollow metal frames shop drawings", GCS[1], "Approved"),
        ("SUB-006", "23 00 00", "HVAC equipment submittals — AHUs", GCS[2], "Approved"),
        ("SUB-007", "23 00 00", "Chilled water pipe insulation product data", GCS[2], "Approved"),
        ("SUB-008", "26 24 16", "Panelboard shop drawings — LP-1A", GCS[0], "Approved"),
        ("SUB-009", "26 24 16", "Panelboard shop drawings — LP-1B", GCS[0], "Approved"),
        ("SUB-010", "26 05 19", "Low-voltage cable product data", GCS[1], "Approved"),
        ("SUB-011", "07 54 23", "TPO roofing product data", GCS[2], "Approved"),
        ("SUB-012", "07 54 23", "Roofing warranty documentation", GCS[2], "Approved"),
        ("SUB-013", "21 12 00", "Fire suppression sprinkler head product data", GCS[0], "Approved"),
        ("SUB-014", "28 13 00", "Access control hardware submittals", GCS[1], "Approved"),
    ]
    for i, (num, spec, desc, gc, status) in enumerate(approved_data):
        subs.append(Submittal(
            submittal_number=num,
            spec_section=spec,
            description=desc,
            assigned_gc=gc,
            reviewer="R. Lan (Project Engineer)",
            submitted_date=date(2025, 1, 15) + timedelta(days=i * 7),
            response_due=date(2025, 2, 5) + timedelta(days=i * 7),
            returned_date=date(2025, 2, 3) + timedelta(days=i * 7),
            status=status,
            revision=1,
        ))

    # 3 Pending
    pending_data = [
        ("SUB-015", "09 91 00", "Exterior paint color samples — mechanical screen", GCS[0]),
        ("SUB-016", "26 24 16", "Main switchgear shop drawings", GCS[1]),
        ("SUB-017", "23 00 00", "Cooling tower product data and performance curves", GCS[2]),
    ]
    for num, spec, desc, gc in pending_data:
        subs.append(Submittal(
            submittal_number=num,
            spec_section=spec,
            description=desc,
            assigned_gc=gc,
            reviewer="R. Lan (Project Engineer)",
            submitted_date=date(2025, 11, 15),
            response_due=date(2025, 12, 5),
            status="Pending",
            revision=1,
        ))

    # 1 Rejected
    subs.append(Submittal(
        submittal_number="SUB-018",
        spec_section="03 30 00",
        description="Concrete mix design — elevated structural slab (Revision 1)",
        assigned_gc=GCS[0],
        reviewer="R. Lan (Project Engineer)",
        submitted_date=date(2025, 10, 1),
        response_due=date(2025, 10, 21),
        returned_date=date(2025, 10, 19),
        status="Rejected",
        revision=1,
        notes="Compressive strength does not meet 5000 psi specification. Resubmit with corrected water/cement ratio.",
    ))

    db.add_all(subs)
    db.commit()
    print(f"Seeded {len(subs)} submittals.")


def seed_change_orders(db):
    # 12 COs, all Pending Approval, sum = exactly $1,870,000
    cos_data = [
        ("CO-001", "Turner Construction", "Additional rebar at shear wall — structural engineer directive", 185000, 5),
        ("CO-002", "Hensel Phelps", "Increased HVAC capacity for revised IT load density", 210000, 14),
        ("CO-003", "McCarthy Building Companies", "Underground conduit reroute — buried conflict with drainage", 95000, 7),
        ("CO-004", "Turner Construction", "Generator fuel tank secondary containment upgrade", 145000, 3),
        ("CO-005", "Hensel Phelps", "Additional cooling tower structural pad and piping", 175000, 10),
        ("CO-006", "McCarthy Building Companies", "Fire suppression system scope addition — server room B", 88000, 5),
        ("CO-007", "Turner Construction", "Seismic bracing additions for MEP equipment — Zone C", 122000, 7),
        ("CO-008", "Hensel Phelps", "Electrical switchgear pad enlargement per revised layout", 67000, 3),
        ("CO-009", "McCarthy Building Companies", "Exterior insulation upgrade to exceed energy code by 15%", 110000, 0),
        ("CO-010", "Turner Construction", "Security camera additional conduit runs — perimeter expansion", 58000, 2),
        ("CO-011", "Hensel Phelps", "Raised floor extension into secondary IT room", 445000, 21),
        ("CO-012", "McCarthy Building Companies", "Roof drain additional downspouts and yard piping", 170000, 5),
    ]

    # Verify sum
    total = sum(c[3] for c in cos_data)
    assert total == 1870000, f"CO total mismatch: {total}"

    cos = []
    for i, (num, gc, scope, cost, sched) in enumerate(cos_data):
        cos.append(ChangeOrder(
            co_number=num,
            title=scope.split(" — ")[0] if " — " in scope else scope[:60],
            scope=scope,
            assigned_gc=gc,
            cost_impact=float(cost),
            schedule_impact=sched,
            status="Pending Approval",
            submitted_date=date(2025, 11, 1) + timedelta(days=i * 3),
        ))

    db.add_all(cos)
    db.commit()
    print(f"Seeded {len(cos)} change orders (total ${total:,}).")


def seed_ofm(db):
    items = [
        # 6 Green
        OFMItem(
            equipment_tag="UPS-A1",
            description="Uninterruptible Power Supply — Module A1 (500kVA)",
            supplier="Eaton Power Quality",
            expected_delivery=date(2025, 9, 15),
            actual_delivery=date(2025, 9, 12),
            variance_days=-3,
            rag_status="Green",
        ),
        OFMItem(
            equipment_tag="UPS-A2",
            description="Uninterruptible Power Supply — Module A2 (500kVA)",
            supplier="Eaton Power Quality",
            expected_delivery=date(2025, 9, 15),
            actual_delivery=date(2025, 9, 15),
            variance_days=0,
            rag_status="Green",
        ),
        OFMItem(
            equipment_tag="CT-01",
            description="Cooling Tower — 1200-ton closed-circuit",
            supplier="Baltimore Aircoil Company",
            expected_delivery=date(2025, 10, 1),
            actual_delivery=date(2025, 9, 29),
            variance_days=-2,
            rag_status="Green",
        ),
        OFMItem(
            equipment_tag="SWGR-MDP",
            description="Main Distribution Panel — 3000A 480V switchgear",
            supplier="Square D / Schneider Electric",
            expected_delivery=date(2025, 10, 20),
            actual_delivery=date(2025, 10, 18),
            variance_days=-2,
            rag_status="Green",
        ),
        OFMItem(
            equipment_tag="GEN-01",
            description="Emergency Generator — 2MW diesel",
            supplier="Caterpillar",
            expected_delivery=date(2025, 11, 1),
            actual_delivery=date(2025, 11, 5),
            variance_days=4,
            rag_status="Green",
            notes="Minor delay; did not impact critical path.",
        ),
        OFMItem(
            equipment_tag="CRAC-01",
            description="Computer Room Air Conditioner — 60-ton",
            supplier="Stulz Air Technology",
            expected_delivery=date(2025, 11, 10),
            actual_delivery=date(2025, 11, 10),
            variance_days=0,
            rag_status="Green",
        ),
        # 1 Amber
        OFMItem(
            equipment_tag="XFMR-01",
            description="Step-down Transformer — 2500 kVA dry-type 13.8kV/480V",
            supplier="ABB Ltd.",
            expected_delivery=date(2025, 11, 20),
            actual_delivery=None,
            variance_days=None,
            rag_status="Amber",
            notes="Lead time extended 3 weeks by manufacturer; monitoring weekly.",
        ),
        # 1 Red
        OFMItem(
            equipment_tag="PDU-B1",
            description="Power Distribution Unit — 250kVA floor-mount Zone B",
            supplier="Vertiv Group",
            expected_delivery=date(2025, 10, 15),
            actual_delivery=None,
            variance_days=None,
            rag_status="Red",
            notes="CRITICAL — Delayed 6+ weeks due to component shortage. Impacts critical path for Zone B energization. Expediting in progress.",
        ),
    ]

    db.add_all(items)
    db.commit()
    print(f"Seeded {len(items)} OFM items.")


def seed_vendors(db):
    vendors = [
        # 2 Fully Onboarded
        Vendor(
            company_name="Turner Construction",
            contact_name="Mike Sullivan",
            contact_email="m.sullivan@turner.com",
            trade="General Contractor",
            nda_signed=True,
            orientation_complete=True,
            badge_issued=True,
            site_access_approved=True,
            notes="Prime GC — Lubbock Phase 2.",
        ),
        Vendor(
            company_name="Hensel Phelps",
            contact_name="Jessica Park",
            contact_email="j.park@henselphelps.com",
            trade="General Contractor",
            nda_signed=True,
            orientation_complete=True,
            badge_issued=True,
            site_access_approved=True,
        ),
        # 2 Orientation Pending
        Vendor(
            company_name="Mesa Electrical Contractors",
            contact_name="Carlos Reyes",
            contact_email="c.reyes@mesaelec.com",
            trade="Electrical",
            nda_signed=True,
            orientation_complete=False,
            badge_issued=False,
            site_access_approved=False,
            notes="Orientation scheduled for next Monday.",
        ),
        Vendor(
            company_name="Southland Industries",
            contact_name="Amy Thornton",
            contact_email="a.thornton@southlandind.com",
            trade="Mechanical / HVAC",
            nda_signed=True,
            orientation_complete=False,
            badge_issued=False,
            site_access_approved=False,
            notes="Awaiting completion of site-specific safety training module.",
        ),
        # 1 NDA Outstanding
        Vendor(
            company_name="Airoha Fire Protection",
            contact_name="David Kim",
            contact_email="d.kim@airohafire.com",
            trade="Fire Protection",
            nda_signed=False,
            orientation_complete=False,
            badge_issued=False,
            site_access_approved=False,
            notes="NDA sent 2025-11-10. Awaiting signed return.",
        ),
    ]

    db.add_all(vendors)
    db.commit()
    print(f"Seeded {len(vendors)} vendors.")


def main():
    with Session() as db:
        clear(db)
        seed_rfis(db)
        seed_submittals(db)
        seed_change_orders(db)
        seed_ofm(db)
        seed_vendors(db)
        print("\nSeed complete!")

        # Quick verification
        from sqlalchemy import func
        from app.models.rfi import RFI as R
        from app.models.change_order import ChangeOrder as CO
        total_rfis = db.query(func.count(R.id)).scalar()
        co_total = db.query(func.sum(CO.cost_impact)).scalar()
        open_rfis = db.query(func.count(R.id)).filter(R.status == "Open").scalar()
        print(f"  RFIs: {total_rfis}  (Open: {open_rfis})")
        print(f"  CO total: ${co_total:,.0f}")


if __name__ == "__main__":
    main()
