"""
╔══════════════════════════════════════════════════════════════╗
║   mos | NEXIS  —  Action & Review                            ║
║   Digital Management Operating System                        ║
║   Version 1.1  •  10 April 2026  •  Yeppoon, Queensland     ║
║   "We will always have a plan."                              ║
╚══════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from collections import Counter
import plotly.graph_objects as go
import io

st.set_page_config(
    page_title="NEXIS Action & Review",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════
#  STYLES  — MOS Brand Compliant v2 Dec 2025
#  Tokens: bg #0d1117 | sidebar #071539 | surface #161b27
#          border #1e3a5f | cyan #22d3ee | overdue #FF3B30
#          in-progress #34C759 | pending #FF9500
# ═══════════════════════════════════════════════════════════════
st.markdown("""<style>
.stApp{background:#0d1117}
.main .block-container{padding-top:1.3rem;padding-bottom:2rem}
p,span,label,li{color:#e6edf3}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#071539 0%,#091e4a 100%);border-right:1px solid #1a3060}
[data-testid="stSidebar"] *{color:#c9d8f0!important}
[data-testid="stSidebar"] hr{border-color:#1a3060!important;opacity:.4}
h1{color:#22d3ee!important;font-size:1.8rem!important;letter-spacing:-.5px;margin-bottom:.15rem!important}
h2{color:#22d3ee!important;font-size:1.28rem!important}
h3{color:#93c5d6!important;font-size:1.05rem!important}
[data-testid="stMetric"]{background:#161b27;border:1px solid #1e3a5f;border-radius:12px;padding:15px 17px;transition:border-color .2s}
[data-testid="stMetric"]:hover{border-color:rgba(34,211,238,.45)}
[data-testid="stMetricValue"]{color:#22d3ee!important;font-size:1.7rem!important;font-weight:700!important}
[data-testid="stMetricLabel"]{color:#8b949e!important;font-size:.75rem!important;text-transform:uppercase;letter-spacing:.5px}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#0891b2,#22d3ee)!important;color:#071539!important;border:none!important;border-radius:8px!important;font-weight:700!important;padding:9px 20px!important;transition:all .18s!important;box-shadow:0 2px 8px rgba(34,211,238,.22)!important}
.stButton>button[kind="primary"]:hover{transform:translateY(-1px) scale(1.015)!important;box-shadow:0 6px 18px rgba(34,211,238,.4)!important}
.stButton>button:not([kind="primary"]){background:#161b27!important;color:#22d3ee!important;border:1px solid #1e3a5f!important;border-radius:8px!important;font-weight:600!important;transition:all .18s!important}
.stButton>button:not([kind="primary"]):hover{border-color:#22d3ee!important;background:rgba(34,211,238,.08)!important;transform:translateY(-1px)!important}
.stTextInput input,.stTextArea textarea,.stNumberInput input{background:#161b27!important;border:1px solid #1e3a5f!important;border-radius:8px!important;color:#e6edf3!important}
.stTextInput input:focus,.stTextArea textarea:focus{border-color:#22d3ee!important;box-shadow:0 0 0 2px rgba(34,211,238,.15)!important}
[data-baseweb="select"]>div:first-child{background:#161b27!important;border-color:#1e3a5f!important;border-radius:8px!important}
[data-baseweb="select"] span{color:#e6edf3!important}
.stDateInput input{background:#161b27!important;border-color:#1e3a5f!important;border-radius:8px!important;color:#e6edf3!important}
.stTabs [data-baseweb="tab-list"]{background:transparent;border-bottom:1px solid #1e3a5f;gap:2px}
.stTabs [data-baseweb="tab"]{background:transparent!important;color:#6b7280!important;border-radius:6px 6px 0 0;padding:8px 18px;font-weight:500}
.stTabs [aria-selected="true"]{color:#22d3ee!important;background:rgba(34,211,238,.07)!important;border-bottom:2px solid #22d3ee!important}
[data-testid="stDataEditor"],[data-testid="stDataFrameResizable"]{border:1px solid #1e3a5f!important;border-radius:10px!important;overflow:hidden}
hr{border:none;border-top:1px solid #1e3a5f!important;margin:12px 0}
details summary{background:#161b27!important;border-radius:8px;color:#22d3ee!important;padding:10px 14px}
details{border:1px solid #1e3a5f;border-radius:8px;margin:5px 0}
details>div{background:#101520;padding:12px 14px;border-radius:0 0 8px 8px}
.stProgress>div>div>div>div{background:linear-gradient(90deg,#0891b2,#22d3ee)!important}
.stFileUploader{background:#161b27!important;border:1px dashed #22d3ee!important;border-radius:8px!important}
.badge{display:inline-block;padding:3px 11px;border-radius:20px;font-size:11.5px;font-weight:600;letter-spacing:.3px}
.badge-overdue{background:rgba(255,59,48,.15);color:#FF3B30;border:1px solid rgba(255,59,48,.3)}
.badge-active{background:rgba(34,211,238,.15);color:#22d3ee;border:1px solid rgba(34,211,238,.3)}
.badge-inprogress{background:rgba(52,199,89,.15);color:#34C759;border:1px solid rgba(52,199,89,.3)}
.badge-pending{background:rgba(255,149,0,.15);color:#FF9500;border:1px solid rgba(255,149,0,.3)}
.badge-closed{background:rgba(110,110,110,.12);color:#9ca3af;border:1px solid rgba(110,110,110,.3)}
.badge-live{background:rgba(34,211,238,.22);color:#22d3ee;border:1px solid #22d3ee;animation:pulse 1.5s infinite}
.badge-scheduled{background:rgba(147,197,214,.14);color:#93c5d6;border:1px solid rgba(147,197,214,.3)}
.badge-completed{background:rgba(52,199,89,.14);color:#34C759;border:1px solid rgba(52,199,89,.3)}
.badge-cancelled{background:rgba(255,59,48,.12);color:#FF3B30;border:1px solid rgba(255,59,48,.25)}
.badge-open{background:rgba(255,149,0,.14);color:#FF9500;border:1px solid rgba(255,149,0,.3)}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.55}}
.pbar-wrap{background:#1e3a5f;border-radius:5px;height:7px;overflow:hidden;margin-top:5px}
.pbar-fill{height:100%;background:linear-gradient(90deg,#0891b2,#22d3ee);border-radius:5px}
.section-lbl{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:1.2px;color:#6b7280;margin:18px 0 8px 0;padding-bottom:6px;border-bottom:1px solid #1e3a5f}
.meeting-card{background:#161b27;border:1px solid #1e3a5f;border-radius:11px;padding:14px 18px;margin:8px 0;transition:all .2s}
.meeting-card:hover{border-color:rgba(34,211,238,.5);box-shadow:0 4px 14px rgba(34,211,238,.07)}
.action-origin{background:rgba(34,211,238,.06);border:1px solid rgba(34,211,238,.2);border-radius:6px;padding:6px 12px;font-size:12px;color:#93c5d6;margin-top:6px;display:inline-block}
.attach-zone{border:1px dashed rgba(34,211,238,.4);border-radius:8px;padding:16px;text-align:center;color:#6b7280;font-size:13px;background:rgba(34,211,238,.03);margin:8px 0}
.kpi-alert{background:rgba(255,149,0,.1);border:1px solid rgba(255,149,0,.35);border-radius:8px;padding:10px 14px;font-size:13px;color:#FF9500;margin:6px 0}
.deviation-card{background:rgba(255,149,0,.06);border-left:3px solid #FF9500;border-radius:6px;padding:10px 14px;margin:6px 0;font-size:13px}
.nexis-footer{text-align:center;color:rgba(34,211,238,.45);font-size:11px;font-style:italic;letter-spacing:.8px;padding:20px 0 6px 0}
#MainMenu{visibility:hidden}
footer{visibility:hidden}
</style>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  SESSION STATE  —  full data model
# ═══════════════════════════════════════════════════════════════
def _init():
    today = date.today()

    if "user" not in st.session_state:
        st.session_state.user = "Lauris G."

    if "actions" not in st.session_state:
        st.session_state.actions = [
            {"id":487,"title":"Complete safety audit on all access points",
             "details":"Full inspection of all 12 access control points including door seals, card readers, and emergency releases.",
             "originator":"Lauris G.","responsible":"Emma T.","team":"Engineering",
             "project":"Building Maintenance Upgrade","due":date(2026,4,8),"progress":40,"status":"Overdue",
             "closed_comment":"","notify":True,
             "notes":[{"date":"2026-04-06","text":"Started zones 1–3. Card readers replaced."},
                      {"date":"2026-04-07","text":"Zones 4–6 done. Zone 7 needs replacement seal."}],
             "attachments":[],"origin_meeting":"Daily Operations Review","origin_id":1,"raised":date(2026,3,28)},
            {"id":492,"title":"Update KPI dashboard for April",
             "details":"Refresh all metric definitions and Q2 targets. Include new shift performance indicators.",
             "originator":"Lauris G.","responsible":"Lauris G.","team":"Operations",
             "project":"IT System Refresh","due":date(2026,4,15),"progress":75,"status":"Active",
             "closed_comment":"","notify":False,
             "notes":[{"date":"2026-04-09","text":"Metrics imported. Validating with dept heads."}],
             "attachments":[],"origin_meeting":"Weekly Leadership Update","origin_id":2,"raised":date(2026,4,1)},
            {"id":501,"title":"Review incident report from Shift 2",
             "details":"Formal review of near-miss reported 7 April. Includes CCTV footage review and witness statements.",
             "originator":"James K.","responsible":"James K.","team":"Facilities",
             "project":"","due":date(2026,4,12),"progress":20,"status":"In Progress",
             "closed_comment":"","notify":True,"notes":[],"attachments":[],
             "origin_meeting":"Safety Committee Meeting","origin_id":3,"raised":date(2026,4,7)},
            {"id":505,"title":"Staff rostering review for Q2",
             "details":"Review roster model vs Q2 demand forecast. Identify gaps and overtime risk.",
             "originator":"Lauris G.","responsible":"Sarah M.","team":"HR",
             "project":"","due":date(2026,4,18),"progress":55,"status":"Active",
             "closed_comment":"","notify":True,
             "notes":[{"date":"2026-04-08","text":"Two shift gaps identified in Zone C."}],
             "attachments":[],"origin_meeting":"Weekly Leadership Update","origin_id":2,"raised":date(2026,4,2)},
            {"id":508,"title":"Fire suppression system annual test",
             "details":"Annual test of all fire suppression zones. Schedule contractor, notify occupants 72h in advance.",
             "originator":"Emma T.","responsible":"James K.","team":"Facilities",
             "project":"Building Maintenance Upgrade","due":date(2026,4,22),"progress":0,"status":"Pending",
             "closed_comment":"","notify":False,"notes":[],"attachments":[],
             "origin_meeting":"Safety Committee Meeting","origin_id":3,"raised":date(2026,4,5)},
            {"id":510,"title":"Monthly cost variance report – March",
             "details":"Compile variance analysis against March budget. Present to GM by COB 14 April.",
             "originator":"Lauris G.","responsible":"Tom R.","team":"Finance",
             "project":"","due":date(2026,4,14),"progress":65,"status":"In Progress",
             "closed_comment":"","notify":False,
             "notes":[{"date":"2026-04-09","text":"Labour & materials complete. Working on overhead."}],
             "attachments":[],"origin_meeting":"Weekly Leadership Update","origin_id":2,"raised":date(2026,4,3)},
            {"id":515,"title":"Q2 training schedule update",
             "details":"Update mandatory training records and schedule refreshers including new compliance modules.",
             "originator":"Sarah M.","responsible":"Sarah M.","team":"Training",
             "project":"Staff Wellness Program","due":date(2026,4,20),"progress":30,"status":"Active",
             "closed_comment":"","notify":False,"notes":[],"attachments":[],
             "origin_meeting":"Daily Operations Review","origin_id":1,"raised":date(2026,4,4)},
        ]

    if "meetings" not in st.session_state:
        st.session_state.meetings = [
            {"id":1,"title":"Daily Operations Review","type":"Daily Review","private":False,
             "summary":"Morning operational review covering safety, production, staffing, and priorities.",
             "team":"Operations","location":"Boardroom A","facilitator":"Lauris G.",
             "start_dt":datetime(today.year,today.month,today.day,8,0),
             "frequency":"Daily","duration":30,"status":"Scheduled",
             "attendees":[{"name":"Lauris G.","present":False,"facilitator":True},
                          {"name":"Emma T.","present":False,"facilitator":False},
                          {"name":"James K.","present":False,"facilitator":False},
                          {"name":"Sarah M.","present":False,"facilitator":False}],
             "agenda":[{"title":"Safety Share","subtitle":"Hazards or near-misses past 24h","type":"Default","notes":""},
                       {"title":"Yesterday's Results","subtitle":"Actuals vs target","type":"Review","notes":""},
                       {"title":"Today's Priorities","subtitle":"Key tasks and blockers","type":"Decision","notes":""}],
             "kpis":["Safety incidents","Attendance rate","Tasks completed"],
             "delay_metrics":True,"auto_rca":False,
             "attachments":[],"linked_actions":[487,515],
             "history":[{"ts":"2026-04-09 08:02","event":"Meeting created by Lauris G."}]},
            {"id":2,"title":"Weekly Leadership Update","type":"Weekly Team Update","private":False,
             "summary":"Cross-functional leadership sync covering strategy, performance and people.",
             "team":"Leadership","location":"Executive Suite","facilitator":"Lauris G.",
             "start_dt":datetime(today.year,today.month,today.day,14,0),
             "frequency":"Weekly","duration":60,"status":"Scheduled",
             "attendees":[{"name":"Lauris G.","present":False,"facilitator":True},
                          {"name":"Emma T.","present":False,"facilitator":False},
                          {"name":"Tom R.","present":False,"facilitator":False},
                          {"name":"Sarah M.","present":False,"facilitator":False}],
             "agenda":[{"title":"KPI Dashboard Review","subtitle":"All depts – actuals vs targets","type":"Review","notes":""},
                       {"title":"Open Actions Review","subtitle":"Overdue and at-risk actions","type":"Review","notes":""},
                       {"title":"Strategic Updates","subtitle":"Project progress and decisions required","type":"Decision","notes":""},
                       {"title":"People & Culture","subtitle":"Staffing, wellbeing, training","type":"Default","notes":""}],
             "kpis":["Overdue actions","Budget variance %","Staff turnover rate"],
             "delay_metrics":False,"auto_rca":False,
             "attachments":[],"linked_actions":[492,505,510],
             "history":[{"ts":"2026-04-03 09:15","event":"Meeting created by Lauris G."}]},
            {"id":3,"title":"Safety Committee Meeting","type":"Problem-Solving Session","private":False,
             "summary":"Monthly safety review, incident follow-up, and risk register update.",
             "team":"Facilities","location":"Meeting Room 2","facilitator":"James K.",
             "start_dt":datetime(2026,4,17,9,0),
             "frequency":"Every 4 weeks","duration":90,"status":"Scheduled",
             "attendees":[{"name":"James K.","present":False,"facilitator":True},
                          {"name":"Lauris G.","present":False,"facilitator":False},
                          {"name":"Emma T.","present":False,"facilitator":False}],
             "agenda":[{"title":"Incident Review","subtitle":"All incidents & near-misses since last meeting","type":"Review","notes":""},
                       {"title":"Open Safety Actions","subtitle":"Status update on all safety actions","type":"Review","notes":""},
                       {"title":"Risk Register Review","subtitle":"New risks, changed ratings","type":"Decision","notes":""}],
             "kpis":["LTIFR","Near-miss rate","Safety action closure %"],
             "delay_metrics":True,"auto_rca":True,
             "attachments":[],"linked_actions":[501,508],
             "history":[{"ts":"2026-03-20 10:00","event":"Meeting created by James K."}]},
        ]

    if "rcas" not in st.session_state:
        st.session_state.rcas = [
            {"id":1,"title":"Near-Miss – Shift 2 Access Control Failure","date":date(2026,4,7),
             "exec_summary":"A near-miss occurred during Shift 2 when an access control point failed to lock correctly, allowing unauthorised entry into a restricted zone. No injury resulted.",
             "five_whys":["The access door failed to lock after shift handover.",
                          "The electronic latch mechanism had a software fault.",
                          "Firmware update was not applied during the last maintenance window.",
                          "The maintenance schedule did not include firmware version checks.",
                          "No formal process exists for firmware version control on security hardware."],
             "timeline":[{"time":"22:15","event":"Shift 2 handover completed, zone handed over."},
                         {"time":"22:32","event":"Supervisor noticed door A-7 was unsecured."},
                         {"time":"22:34","event":"Zone locked manually. Incident reported to facilities."},
                         {"time":"22:50","event":"Engineering notified. Door tagged out of service."}],
             "factors":{"systems":"No firmware version control for security hardware.",
                        "people":"Maintenance staff unaware of pending firmware update.",
                        "equipment":"XT-440 latch – firmware v2.1.3 (current: v2.2.1).",
                        "environment":"High-traffic area; shift changeover creates supervision gap.",
                        "organisational":"Maintenance schedule excludes software/firmware items."},
             "recommendations":"1. Implement firmware version control register.\n2. Add firmware check to maintenance checklist.\n3. Audit all access control units within 7 days.\n4. Brief maintenance team on new process.",
             "linked_actions":[487,501],"status":"Open"},
        ]

    if "projects" not in st.session_state:
        st.session_state.projects = [
            {"id":1,"name":"Building Maintenance Upgrade","owner":"James K.","team":"Facilities",
             "start":date(2026,2,1),"end":date(2026,6,30),"progress":65,"actions":2,"status":"Active"},
            {"id":2,"name":"IT System Refresh","owner":"Tom R.","team":"IT",
             "start":date(2026,3,1),"end":date(2026,8,31),"progress":30,"actions":1,"status":"Active"},
            {"id":3,"name":"Staff Wellness Program","owner":"Sarah M.","team":"HR",
             "start":date(2026,1,15),"end":date(2026,12,31),"progress":80,"actions":1,"status":"Active"},
        ]

    if "admin" not in st.session_state:
        st.session_state.admin = {
            "teams":["Engineering","Operations","Facilities","HR","Finance","IT","Training","Leadership","Nursing","Security"],
            "locations":["Boardroom A","Executive Suite","Meeting Room 1","Meeting Room 2","Meeting Room 3",
                         "Training Centre","Microsoft Teams","Zoom","On-site – Main Gate"],
            "meeting_types":["Daily Review","Weekly Team Update","Training Session","Problem-Solving Session",
                             "Project Review","Ad-hoc Meeting","Root Cause Analysis","Custom"],
            "users":["Lauris G.","Emma T.","James K.","Sarah M.","Tom R.","Alex B.","Maria C."],
            "metric_defs":[
                {"name":"Safety Incidents","unit":"Count","type":"Number","kpi":True},
                {"name":"Attendance Rate","unit":"%","type":"Percentage","kpi":True},
                {"name":"Budget Variance","unit":"%","type":"Percentage","kpi":True},
                {"name":"Action Closure Rate","unit":"%","type":"Percentage","kpi":True},
            ],
        }

    if "deviations" not in st.session_state:
        st.session_state.deviations = [
            {"id":1,"what":"Production target missed – Shift 1","why":"Equipment downtime on line 3",
             "immediate":"Manual override applied, production rerouted.","team":"Operations",
             "ts":"2026-04-09 06:15","linked":492},
            {"id":2,"what":"Staff shortfall – 2 no-shows, Zone C","why":"Unplanned leave – illness",
             "immediate":"Supervisor covered; roster review requested.","team":"HR",
             "ts":"2026-04-10 07:55","linked":505},
        ]

    for k,v in [("next_action_id",520),("next_meeting_id",4),("next_rca_id",2),
                ("next_project_id",4),("next_dev_id",3),("sel_meeting",None),("sel_rca",None)]:
        if k not in st.session_state:
            st.session_state[k] = v

_init()


# ═══════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════
def badge(status):
    cls={"Overdue":"badge-overdue","Active":"badge-active","In Progress":"badge-inprogress",
         "Pending":"badge-pending","Closed":"badge-closed","Live":"badge-live",
         "Scheduled":"badge-scheduled","Completed":"badge-completed","Cancelled":"badge-cancelled",
         "Open":"badge-open"}.get(status,"badge-active")
    return f'<span class="badge {cls}">{status}</span>'

def pbar(pct):
    return f'<div class="pbar-wrap"><div class="pbar-fill" style="width:{pct}%"></div></div>'

def get_action(aid): return next((a for a in st.session_state.actions if a["id"]==aid),None)
def get_meeting(mid): return next((m for m in st.session_state.meetings if m["id"]==mid),None)
def get_rca(rid):    return next((r for r in st.session_state.rcas if r["id"]==rid),None)
def mtg_idx(mid):    return next((i for i,m in enumerate(st.session_state.meetings) if m["id"]==mid),None)
def rca_idx(rid):    return next((i for i,r in enumerate(st.session_state.rcas) if r["id"]==rid),None)

def overdue_actions(): t=date.today(); return [a for a in st.session_state.actions if a["due"]<t and a["status"]!="Closed"]
def my_actions():      return [a for a in st.session_state.actions if a["responsible"]==st.session_state.user and a["status"]!="Closed"]
def today_meetings():  t=date.today(); return [m for m in st.session_state.meetings if m["start_dt"].date()==t and m["status"]!="Cancelled"]

def actions_to_excel():
    rows=[{"ID":a["id"],"Title":a["title"],"Team":a["team"],"Responsible":a["responsible"],
           "Status":a["status"],"Due Date":a["due"],"Progress %":a["progress"],
           "Originator":a["originator"],"Project":a.get("project",""),
           "Origin Meeting":a.get("origin_meeting",""),"Raised":a.get("raised","")}
          for a in st.session_state.actions]
    df=pd.DataFrame(rows)
    try:
        buf=io.BytesIO(); df.to_excel(buf,index=False,engine="openpyxl"); buf.seek(0)
        return buf.getvalue(),"xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    except Exception:
        return df.to_csv(index=False).encode(),"csv","text/csv"

def performance_report_excel():
    """Automated Business Performance Report – pulls overdue actions, meeting outcomes, deviations."""
    buf=io.BytesIO()
    try:
        with pd.ExcelWriter(buf,engine="openpyxl") as w:
            # Overdue actions
            od=[{"ID":a["id"],"Title":a["title"],"Team":a["team"],"Responsible":a["responsible"],
                 "Due":a["due"],"Progress %":a["progress"]} for a in overdue_actions()]
            pd.DataFrame(od if od else [{"Note":"No overdue actions"}]).to_excel(w,sheet_name="Overdue Actions",index=False)
            # All actions summary
            acts=[{"ID":a["id"],"Title":a["title"],"Status":a["status"],"Team":a["team"],
                   "Responsible":a["responsible"],"Progress %":a["progress"]} for a in st.session_state.actions]
            pd.DataFrame(acts).to_excel(w,sheet_name="All Actions",index=False)
            # Meetings
            mtgs=[{"Title":m["title"],"Type":m["type"],"Status":m["status"],
                   "Date":m["start_dt"].strftime("%d %b %Y %H:%M"),"Facilitator":m["facilitator"],
                   "Linked Actions":len(m["linked_actions"])} for m in st.session_state.meetings]
            pd.DataFrame(mtgs).to_excel(w,sheet_name="Meetings",index=False)
            # Deviations
            devs=[{"ID":d["id"],"What":d["what"],"Why":d["why"],"Team":d["team"],"Timestamp":d["ts"]}
                  for d in st.session_state.deviations]
            pd.DataFrame(devs if devs else [{"Note":"No deviations logged"}]).to_excel(w,sheet_name="Deviations",index=False)
        buf.seek(0)
        return buf.getvalue()
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════
#  DIALOGS
# ═══════════════════════════════════════════════════════════════
@st.dialog("Action", width="large")
def action_dialog(action_id=None, prefill_origin=None):
    a=get_action(action_id) if action_id else None
    edit=a is not None
    st.markdown(f"### {'✏️ Edit Action  #'+str(action_id) if edit else '➕ Create New Action'}")
    st.divider()
    c1,c2=st.columns(2)
    users=st.session_state.admin["users"]
    teams=st.session_state.admin["teams"]
    projects=[""]+[p["name"] for p in st.session_state.projects]
    statuses=["Active","In Progress","Pending","Overdue","Closed"]
    with c1:
        st.markdown("**Details**")
        title=st.text_input("Title *",value=a["title"] if edit else "")
        details=st.text_area("Extra Details",value=a["details"] if edit else "",height=90)
        orig_i=users.index(a["originator"]) if edit and a["originator"] in users else 0
        originator=st.selectbox("Originator",users,index=orig_i)
    with c2:
        st.markdown("**Assignment & Schedule**")
        resp_i=users.index(a["responsible"]) if edit and a["responsible"] in users else 0
        responsible=st.selectbox("Responsible Person",users,index=resp_i)
        team_i=teams.index(a["team"]) if edit and a["team"] in teams else 0
        team=st.selectbox("Team / Function",teams,index=team_i)
        proj_i=projects.index(a["project"]) if edit and a.get("project") in projects else 0
        project=st.selectbox("Linked Project",projects,index=proj_i)
        due=st.date_input("Due Date",value=a["due"] if edit else date.today()+timedelta(days=7))
        progress=st.slider("Progress %",0,100,value=a["progress"] if edit else 0,step=5)
        stat_i=statuses.index(a["status"]) if edit and a["status"] in statuses else 0
        status=st.selectbox("Status",statuses,index=stat_i)
        closed_comment=""
        if status=="Closed":
            closed_comment=st.text_input("Closed Comment",value=a.get("closed_comment","") if edit else "")

    # Origin link
    origin_txt=(a["origin_meeting"] if edit else (prefill_origin or "Manual Entry"))
    st.markdown(f'<div class="action-origin">📎 Origin: <strong>{origin_txt}</strong></div>',unsafe_allow_html=True)
    if edit and a.get("origin_id"):
        if st.button("🔗 GO TO ORIGIN MEETING",key=f"goto_{action_id}"):
            st.session_state.sel_meeting=a["origin_id"]
            st.session_state.nav_radio="Meetings"
            st.rerun()

    st.divider()
    # Attachments (simulated)
    st.markdown('<p class="section-lbl">Attachments</p>',unsafe_allow_html=True)
    st.markdown('<div class="attach-zone">📎 Drag & drop files here or use file upload<br><small>PDF, Word, Excel, Images supported</small></div>',unsafe_allow_html=True)
    uploaded=st.file_uploader("Upload file",label_visibility="collapsed",key=f"upl_{action_id}")
    if edit and a.get("attachments"):
        for att in a["attachments"]:
            st.markdown(f'<span style="font-size:12px;color:#22d3ee">📄 {att}</span>',unsafe_allow_html=True)

    # Email / Notify
    ec1,ec2=st.columns([1,1])
    with ec1:
        notify=st.checkbox("✉️ Notify Responsible",value=a.get("notify",True) if edit else True)
    with ec2:
        if st.button("📧 Email Direct from Action",key=f"email_{action_id}"):
            st.toast(f"Email sent to {responsible} (demo) ✅")

    # Progress notes
    if edit:
        st.divider()
        st.markdown('<p class="section-lbl">Progress Notes History</p>',unsafe_allow_html=True)
        for n in a.get("notes",[]):
            st.markdown(f'<div style="font-size:13px;color:#8b949e;padding:4px 0;border-bottom:1px solid #1e3a5f"><strong style="color:#22d3ee">{n["date"]}</strong> — {n["text"]}</div>',unsafe_allow_html=True)
        new_note=st.text_input("Add Note","",placeholder="Add a progress note…",key=f"note_{action_id}")

    st.divider()
    bc1,bc2=st.columns(2)
    with bc1:
        if st.button("Cancel",use_container_width=True): st.rerun()
    with bc2:
        if st.button("💾 Save Action",type="primary",use_container_width=True):
            if not title.strip(): st.error("Title is required."); return
            att_list=(a.get("attachments",[]) if edit else [])
            if uploaded: att_list=att_list+[uploaded.name]
            if edit:
                a.update({"title":title,"details":details,"originator":originator,"responsible":responsible,
                          "team":team,"project":project,"due":due,"progress":progress,
                          "status":status,"closed_comment":closed_comment,"notify":notify,"attachments":att_list})
                if new_note.strip(): a["notes"].append({"date":str(date.today()),"text":new_note.strip()})
            else:
                st.session_state.actions.append({
                    "id":st.session_state.next_action_id,"title":title,"details":details,
                    "originator":originator,"responsible":responsible,"team":team,"project":project,
                    "due":due,"progress":progress,"status":status,"closed_comment":closed_comment,
                    "notify":notify,"notes":[],"attachments":att_list,
                    "origin_meeting":prefill_origin or "Manual Entry","origin_id":None,"raised":date.today()})
                st.session_state.next_action_id+=1
            st.rerun()


@st.dialog("Create New Meeting", width="large")
def meeting_dialog(from_rca=False):
    tab_g,tab_s=st.tabs(["📋  General","📅  Schedule"])
    with tab_g:
        title=st.text_input("Meeting Title *","")
        mtypes=st.session_state.admin["meeting_types"]
        def_i=mtypes.index("Root Cause Analysis") if from_rca and "Root Cause Analysis" in mtypes else 0
        mtype=st.selectbox("Meeting Type",mtypes,index=def_i)
        private=st.checkbox("🔒 Private Meeting")
        summary=st.text_area("Summary / Purpose","",height=70)
        c1,c2=st.columns(2)
        with c1: team=st.selectbox("Team / Function",st.session_state.admin["teams"])
        with c2: loc=st.selectbox("Location",st.session_state.admin["locations"])
        fac=st.selectbox("Owner / Facilitator",st.session_state.admin["users"])
        st.markdown('<p class="section-lbl">KPIs & Delay Metrics</p>',unsafe_allow_html=True)
        kpi_raw=st.text_input("KPIs to Track (comma-separated)","Safety incidents, Attendance rate")
        kc1,kc2=st.columns(2)
        with kc1: delay_metrics=st.checkbox("📊 Enable Delay Metrics tracking",value=True)
        with kc2: auto_rca=st.checkbox("🔍 Auto-RCA on delay trigger",value=False)
    with tab_s:
        start_d=st.date_input("Start Date",date.today())
        start_t=st.time_input("Start Time",datetime.now().replace(minute=0,second=0,microsecond=0))
        freq=st.selectbox("Frequency",["One-off","Daily","Weekly","Every 2 weeks","Every 3 weeks","Every 4 weeks","Monthly","Quarterly"])
        dur=st.selectbox("Duration (minutes)",[15,30,45,60,90,120],index=2)
    st.divider()
    bc1,bc2=st.columns(2)
    with bc1:
        if st.button("Cancel",use_container_width=True): st.rerun()
    with bc2:
        if st.button("💾 Save Meeting",type="primary",use_container_width=True):
            if not title.strip(): st.error("Title required."); return
            kpis=[k.strip() for k in kpi_raw.split(",") if k.strip()]
            new_m={"id":st.session_state.next_meeting_id,"title":title,"type":mtype,"private":private,
                   "summary":summary,"team":team,"location":loc,"facilitator":fac,
                   "start_dt":datetime.combine(start_d,start_t),"frequency":freq,"duration":dur,
                   "status":"Scheduled","attendees":[{"name":fac,"present":False,"facilitator":True}],
                   "agenda":[],"kpis":kpis,"delay_metrics":delay_metrics,"auto_rca":auto_rca,
                   "attachments":[],"linked_actions":[],
                   "history":[{"ts":str(datetime.now())[:16],"event":f"Meeting created by {st.session_state.user}"}]}
            st.session_state.meetings.append(new_m)
            st.session_state.next_meeting_id+=1
            if from_rca:
                new_r={"id":st.session_state.next_rca_id,"title":title,"date":date.today(),
                        "exec_summary":"","five_whys":["","","","",""],"timeline":[],
                        "factors":{"systems":"","people":"","equipment":"","environment":"","organisational":""},
                        "recommendations":"","linked_actions":[],"status":"Open"}
                st.session_state.rcas.append(new_r)
                st.session_state.sel_rca=new_r["id"]
                st.session_state.next_rca_id+=1
            else:
                st.session_state.sel_meeting=new_m["id"]
            st.rerun()


@st.dialog("⚠️  Log Deviation — Short Interval Control", width="large")
def deviation_dialog():
    st.caption("One-tap deviation log for immediate containment and tracking.")
    what=st.text_area("What happened? *","",height=60)
    why=st.text_area("Why? (initial assessment)","",height=55)
    immediate=st.text_area("Immediate action taken","",height=55)
    team=st.selectbox("Team",st.session_state.admin["teams"])
    link_act=st.checkbox("Create a linked action from this deviation")
    st.divider()
    bc1,bc2=st.columns(2)
    with bc1:
        if st.button("Cancel",use_container_width=True): st.rerun()
    with bc2:
        if st.button("📌 Log Deviation",type="primary",use_container_width=True):
            if not what.strip(): st.error("Please describe what happened."); return
            dev={"id":st.session_state.next_dev_id,"what":what,"why":why,"immediate":immediate,
                 "team":team,"ts":str(datetime.now())[:16],"linked":None}
            st.session_state.deviations.append(dev)
            st.session_state.next_dev_id+=1
            if link_act:
                new_a={"id":st.session_state.next_action_id,"title":f"[Deviation] {what[:65].strip()}",
                        "details":f"Why: {why}\nImmediate: {immediate}","originator":st.session_state.user,
                        "responsible":st.session_state.user,"team":team,"project":"",
                        "due":date.today()+timedelta(days=1),"progress":10,"status":"Active",
                        "closed_comment":"","notify":True,"notes":[],"attachments":[],
                        "origin_meeting":"Short Interval Control","origin_id":None,"raised":date.today()}
                st.session_state.actions.append(new_a)
                dev["linked"]=new_a["id"]
                st.session_state.next_action_id+=1
            st.rerun()


@st.dialog("Create New Project")
def project_dialog():
    name=st.text_input("Project Name *","")
    owner=st.selectbox("Owner",st.session_state.admin["users"])
    team=st.selectbox("Team",st.session_state.admin["teams"])
    start=st.date_input("Start Date",date.today())
    end=st.date_input("Target End Date",date.today()+timedelta(days=180))
    st.divider()
    bc1,bc2=st.columns(2)
    with bc1:
        if st.button("Cancel",use_container_width=True): st.rerun()
    with bc2:
        if st.button("💾 Save",type="primary",use_container_width=True):
            if not name.strip(): st.error("Name required."); return
            st.session_state.projects.append({"id":st.session_state.next_project_id,"name":name,
                "owner":owner,"team":team,"start":start,"end":end,"progress":0,"actions":0,"status":"Active"})
            st.session_state.next_project_id+=1
            st.rerun()


# ═══════════════════════════════════════════════════════════════
#  PAGE: DASHBOARD
# ═══════════════════════════════════════════════════════════════
def render_dashboard():
    hr=datetime.now().hour
    greeting="Good morning" if hr<12 else ("Good afternoon" if hr<17 else "Good evening")
    first=st.session_state.user.split()[0]
    st.title("Action & Review")
    st.subheader(f"{greeting}, {first}")

    od=overdue_actions(); tm=today_meetings(); my_a=my_actions()
    exp_data,ext,mime=actions_to_excel()
    rpt=performance_report_excel()

    m1,m2,m3,m4,m5=st.columns(5)
    with m1: st.metric("Overdue Actions",len(od),"⚠️ Attention needed" if od else "✅ All clear")
    with m2:
        live_n=sum(1 for m in tm if m["status"]=="Live")
        st.metric("Meetings Today",len(tm),f"🔴 {live_n} live" if live_n else "Scheduled")
    with m3:
        my_od=sum(1 for a in my_a if a["status"]=="Overdue")
        st.metric("My Open Actions",len(my_a),f"🔴 {my_od} overdue" if my_od else "On track")
    with m4:
        st.download_button("📤 Export Actions",data=exp_data,
            file_name=f"nexis_actions_{date.today()}.{ext}",mime=mime,
            use_container_width=True,type="primary")
    with m5:
        if rpt:
            st.download_button("📊 Daily Report",data=rpt,
                file_name=f"nexis_performance_{date.today()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,type="primary")
        else:
            if st.button("📊 Daily Report",use_container_width=True,type="primary"):
                st.toast("Report generated ✅")

    # Orb
    st.markdown("""
    <div style="text-align:center;padding:28px 0 16px 0">
      <div style="display:inline-flex;flex-direction:column;align-items:center;justify-content:center;
           width:190px;height:190px;border-radius:50%;
           background:radial-gradient(circle at 35% 30%,#1a4a7a 0%,#071539 70%);
           box-shadow:0 0 50px rgba(34,211,238,.32),0 0 100px rgba(34,211,238,.1),
                      inset 0 0 30px rgba(34,211,238,.07);
           border:1.5px solid rgba(34,211,238,.28)">
        <span style="color:rgba(34,211,238,.7);font-size:11px;font-weight:300;letter-spacing:4px;text-transform:uppercase">mos</span>
        <span style="color:#e6edf3;font-size:21px;font-weight:700;letter-spacing:-1px;margin:2px 0">NEXIS</span>
        <span style="color:#93c5d6;font-size:9px;letter-spacing:2.5px;text-transform:uppercase">Action &amp; Review</span>
      </div>
    </div>""",unsafe_allow_html=True)

    # Quick actions
    qc=st.columns(6)
    btns=[("📅","Create Meeting","primary"),("➕","Create Action","primary"),("🔍","Run RCA","primary"),
          ("⚠️","Log Deviation","secondary"),("📂","Projects","secondary"),("🗓️","All Meetings","secondary")]
    for col,(icon,label,kind) in zip(qc,btns):
        with col:
            if st.button(f"{icon}  {label}",use_container_width=True,
                         type="primary" if kind=="primary" else "secondary"):
                if label=="Create Meeting": meeting_dialog()
                elif label=="Create Action": action_dialog()
                elif label=="Run RCA": meeting_dialog(from_rca=True)
                elif label=="Log Deviation": deviation_dialog()
                elif label=="Projects": st.session_state.nav_radio="Projects"; st.rerun()
                elif label=="All Meetings": st.session_state.nav_radio="Meetings"; st.rerun()

    st.divider()

    # KPI Delay alert
    delay_mtgs=[m for m in st.session_state.meetings if m.get("delay_metrics") and m["status"]=="Scheduled"]
    if delay_mtgs:
        st.markdown(f'<div class="kpi-alert">📊 <strong>Delay Metrics Active</strong> — {len(delay_mtgs)} meeting(s) have KPI delay tracking enabled. '
                    f'{"Auto-RCA will trigger if thresholds are breached." if any(m.get("auto_rca") for m in delay_mtgs) else ""}'
                    f'</div>',unsafe_allow_html=True)

    left,right=st.columns([3,2])

    with left:
        st.markdown('<p class="section-lbl">My Open Actions</p>',unsafe_allow_html=True)
        mine=my_actions()
        if mine:
            for a in mine[:6]:
                bdr={"Overdue":"#FF3B30","Active":"#22d3ee","In Progress":"#34C759","Pending":"#FF9500"}.get(a["status"],"#22d3ee")
                overdue_flag=a["due"]<date.today()
                sc_cls={"Overdue":"badge-overdue","Active":"badge-active","In Progress":"badge-inprogress","Pending":"badge-pending"}.get(a["status"],"badge-active")
                st.markdown(f"""
                <div style="background:#161b27;border:1px solid #1e3a5f;border-left:3px solid {bdr};
                  border-radius:10px;padding:11px 15px;margin:5px 0">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start">
                    <div style="flex:1">
                      <span style="font-size:11px;color:#6b7280">#{a['id']}</span>
                      <div style="font-weight:600;color:#e6edf3;font-size:14px;margin:2px 0">{a['title']}</div>
                      <span style="font-size:11px;color:#8b949e">{a['team']} &nbsp;•&nbsp; Due: {a['due'].strftime('%d %b %Y')}
                      {'&nbsp; 🔴 OVERDUE' if overdue_flag and a['status']!='Overdue' else ''}</span>
                    </div>
                    <span class="badge {sc_cls}">{a['status']}</span>
                  </div>
                  {pbar(a['progress'])}
                  <span style="font-size:11px;color:#6b7280">{a['progress']}% complete</span>
                </div>""",unsafe_allow_html=True)
        else:
            st.info("🎉 No open actions assigned to you.")

        # Deviation log
        st.markdown('<p class="section-lbl" style="margin-top:22px">Short Interval Control — Recent Deviations</p>',unsafe_allow_html=True)
        for d in list(reversed(st.session_state.deviations))[:3]:
            st.markdown(f"""
            <div class="deviation-card">
              <div style="font-weight:600;color:#FF9500">{d['what'][:70]}{'…' if len(d['what'])>70 else ''}</div>
              <div style="color:#8b949e;margin-top:3px;font-size:12px">{d['team']} &nbsp;•&nbsp; {d['ts']}
              {' &nbsp;•&nbsp; 🔗 Action #'+str(d['linked']) if d['linked'] else ''}</div>
            </div>""",unsafe_allow_html=True)
        if st.button("⚠️ Log New Deviation"):
            deviation_dialog()

    with right:
        st.markdown('<p class="section-lbl">Today\'s Meetings</p>',unsafe_allow_html=True)
        for m in today_meetings():
            st.markdown(f"""
            <div style="background:#161b27;border:1px solid #1e3a5f;border-radius:10px;padding:12px 15px;margin:6px 0">
              <div style="font-weight:700;color:#e6edf3;font-size:14px">{m['title']}</div>
              <div style="font-size:12px;color:#8b949e;margin-top:3px">
                {m['start_dt'].strftime('%H:%M')} &nbsp;•&nbsp; {m['duration']} min &nbsp;•&nbsp; {m['location']}
              </div>
              <div style="font-size:12px;color:#8b949e">{m['type']} &nbsp;•&nbsp; {len(m['attendees'])} attendees</div>
            </div>""",unsafe_allow_html=True)
        if not today_meetings():
            st.info("No meetings today.")

        # Deviation heatmap by team
        st.markdown('<p class="section-lbl" style="margin-top:18px">Deviation Heatmap by Team</p>',unsafe_allow_html=True)
        if st.session_state.deviations:
            tc=Counter(d["team"] for d in st.session_state.deviations)
            fig=go.Figure(go.Bar(
                x=list(tc.keys()),y=list(tc.values()),
                marker_color=["#FF3B30" if v>1 else "#FF9500" for v in tc.values()],
                text=list(tc.values()),textposition="outside",textfont=dict(color="#e6edf3",size=11)))
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                              margin=dict(t=8,b=8,l=8,r=8),height=160,
                              xaxis=dict(color="#8b949e",showgrid=False),
                              yaxis=dict(color="#8b949e",showgrid=False))
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

        # Status donut
        st.markdown('<p class="section-lbl">Action Status</p>',unsafe_allow_html=True)
        if st.session_state.actions:
            cnts=Counter(a["status"] for a in st.session_state.actions)
            cols={"Overdue":"#FF3B30","Active":"#22d3ee","In Progress":"#34C759","Pending":"#FF9500","Closed":"#6E6E6E"}
            fig2=go.Figure(go.Pie(labels=list(cnts.keys()),values=list(cnts.values()),
                marker_colors=[cols.get(k,"#22d3ee") for k in cnts.keys()],
                hole=.62,textinfo="percent+label",textfont=dict(color="#e6edf3",size=11)))
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False,margin=dict(t=6,b=6,l=6,r=6),height=175,
                annotations=[dict(text=f"<b>{len(st.session_state.actions)}</b><br>Total",
                    x=.5,y=.5,font_color="#22d3ee",font_size=12,showarrow=False)])
            st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})


# ═══════════════════════════════════════════════════════════════
#  PAGE: ACTIONS
# ═══════════════════════════════════════════════════════════════
def render_actions():
    st.title("Actions")
    fc=st.columns([2.5,1.7,1.7,1.7,1.3,1])
    with fc[0]: q=st.text_input("🔍","",placeholder="Search by # or keyword",label_visibility="collapsed")
    with fc[1]: team_f=st.selectbox("Team",["All"]+st.session_state.admin["teams"],label_visibility="collapsed")
    with fc[2]: stat_f=st.selectbox("Status",["All","Active","In Progress","Pending","Overdue","Closed"],label_visibility="collapsed")
    with fc[3]: resp_f=st.selectbox("Person",["All"]+st.session_state.admin["users"],label_visibility="collapsed")
    with fc[4]:
        exp_data,ext,mime=actions_to_excel()
        st.download_button("⬇️ Export",data=exp_data,file_name=f"actions_{date.today()}.{ext}",
            mime=mime,use_container_width=True,help="Export to Excel")
    with fc[5]:
        if st.button("➕ New",type="primary",use_container_width=True): action_dialog()

    al=st.session_state.actions
    if q: ql=q.lower(); al=[a for a in al if ql in a["title"].lower() or ql in str(a["id"])]
    if team_f!="All": al=[a for a in al if a["team"]==team_f]
    if stat_f!="All": al=[a for a in al if a["status"]==stat_f]
    if resp_f!="All": al=[a for a in al if a["responsible"]==resp_f]

    st.markdown(f'<p style="font-size:12px;color:#8b949e;margin:6px 0 2px 0">{len(al)} action{"s" if len(al)!=1 else ""} found</p>',unsafe_allow_html=True)
    hdr=st.columns([1,5,2,2,2,2,2.5,1,1])
    for col,lbl in zip(hdr,["ID","Title","Team","Responsible","Status","Due","Progress","Edit","Origin"]):
        col.markdown(f'<span style="font-size:10px;font-weight:600;color:#6b7280;text-transform:uppercase;letter-spacing:.5px">{lbl}</span>',unsafe_allow_html=True)
    st.markdown('<hr style="margin:3px 0">',unsafe_allow_html=True)

    for a in al[:50]:
        overdue=a["due"]<date.today() and a["status"]!="Closed"
        due_html=f'<span style="color:#FF3B30">{a["due"].strftime("%d %b")}</span>' if overdue else a["due"].strftime("%d %b %Y")
        rc=st.columns([1,5,2,2,2,2,2.5,1,1])
        rc[0].markdown(f'<span style="color:#6b7280;font-size:13px">#{a["id"]}</span>',unsafe_allow_html=True)
        rc[1].markdown(f'<span style="font-size:13px;color:#e6edf3">{a["title"][:50]}{"…" if len(a["title"])>50 else ""}</span>',unsafe_allow_html=True)
        rc[2].markdown(f'<span style="font-size:12px;color:#8b949e">{a["team"]}</span>',unsafe_allow_html=True)
        rc[3].markdown(f'<span style="font-size:12px;color:#8b949e">{a["responsible"]}</span>',unsafe_allow_html=True)
        rc[4].markdown(badge(a["status"]),unsafe_allow_html=True)
        rc[5].markdown(f'<span style="font-size:12px">{due_html}</span>',unsafe_allow_html=True)
        rc[6].markdown(f'{pbar(a["progress"])}<span style="font-size:11px;color:#6b7280">{a["progress"]}%</span>',unsafe_allow_html=True)
        if rc[7].button("✏️",key=f"ea_{a['id']}",help=f"Edit #{a['id']}"): action_dialog(action_id=a["id"])
        if a.get("origin_id"):
            if rc[8].button("🔗",key=f"go_{a['id']}",help="Go to origin meeting"):
                st.session_state.sel_meeting=a["origin_id"]
                st.session_state.nav_radio="Meetings"
                st.rerun()


# ═══════════════════════════════════════════════════════════════
#  PAGE: MEETINGS list
# ═══════════════════════════════════════════════════════════════
def render_meetings():
    if st.session_state.sel_meeting:
        m=get_meeting(st.session_state.sel_meeting)
        if m: render_meeting_detail(m); return
        st.session_state.sel_meeting=None

    st.title("Meetings")
    bc1,_,bc2=st.columns([2,6,2])
    with bc1:
        if st.button("📅 Create New Meeting",type="primary",use_container_width=True): meeting_dialog()
    with bc2:
        view=st.selectbox("View",["All Meetings","Today","This Week","My Meetings"],label_visibility="collapsed")

    st.divider()
    ml=st.session_state.meetings
    today_d=date.today()
    if view=="Today": ml=[m for m in ml if m["start_dt"].date()==today_d]
    elif view=="This Week": ml=[m for m in ml if today_d<=m["start_dt"].date()<=today_d+timedelta(days=7)]
    elif view=="My Meetings":
        me=st.session_state.user
        ml=[m for m in ml if m["facilitator"]==me or any(a["name"]==me for a in m["attendees"])]

    if not ml: st.info("No meetings match the current filter.")
    for m in ml:
        sc={"Scheduled":"badge-scheduled","Live":"badge-live","Completed":"badge-completed","Cancelled":"badge-cancelled"}.get(m["status"],"badge-scheduled")
        delay_flag=' &nbsp;•&nbsp; 📊 Delay Metrics ON' if m.get("delay_metrics") else ''
        auto_flag=' &nbsp;•&nbsp; 🔍 Auto-RCA' if m.get("auto_rca") else ''
        col_c,col_b=st.columns([9,1])
        with col_c:
            st.markdown(f"""
            <div class="meeting-card">
              <div style="display:flex;justify-content:space-between;align-items:flex-start">
                <div>
                  <div style="font-weight:700;color:#e6edf3;font-size:15px">{m['title']}</div>
                  <div style="font-size:12px;color:#8b949e;margin-top:4px">
                    {m['type']} &nbsp;•&nbsp; 📅 {m['start_dt'].strftime('%a %d %b %Y, %H:%M')}
                    &nbsp;•&nbsp; ⏱ {m['duration']} min &nbsp;•&nbsp; 📍 {m['location']}
                    &nbsp;•&nbsp; 👤 {m['facilitator']}{delay_flag}{auto_flag}
                  </div>
                  <div style="font-size:12px;color:#8b949e;margin-top:2px">
                    {m['frequency']} &nbsp;•&nbsp; {len(m['attendees'])} attendees
                    &nbsp;•&nbsp; {len(m['linked_actions'])} linked actions
                    &nbsp;•&nbsp; {len(m.get('kpis',[]))} KPIs
                  </div>
                </div>
                <span class="badge {sc}">{m['status']}</span>
              </div>
            </div>""",unsafe_allow_html=True)
        with col_b:
            st.markdown("<div style='height:20px'></div>",unsafe_allow_html=True)
            if st.button("Open",key=f"om_{m['id']}",use_container_width=True):
                st.session_state.sel_meeting=m["id"]; st.rerun()


def render_meeting_detail(m):
    if st.button("← Back to Meetings"): st.session_state.sel_meeting=None; st.rerun()
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#071539,#0a2050);border:1px solid #1e3a5f;
         border-radius:14px;padding:19px 23px;margin-bottom:13px">
      <div style="display:flex;justify-content:space-between;align-items:flex-start">
        <div>
          <div style="font-size:10px;color:#8b949e;text-transform:uppercase;letter-spacing:1.2px">{m['type']}</div>
          <h1 style="color:#22d3ee;margin:3px 0;font-size:1.5rem">{m['title']}</h1>
          <div style="font-size:13px;color:#8b949e">
            📅 {m['start_dt'].strftime('%A %d %b %Y, %H:%M')} &nbsp;•&nbsp; ⏱ {m['duration']} min
            &nbsp;•&nbsp; 📍 {m['location']} &nbsp;•&nbsp; 👤 {m['facilitator']} &nbsp;•&nbsp; {m['frequency']}
          </div>
          {('<div style="font-size:12px;color:#6b7280;margin-top:4px">'+m.get("summary","")+'</div>') if m.get("summary") else ""}
          {('<div style="margin-top:6px"><span style="font-size:12px;color:#22d3ee">📊 KPIs: '+' &nbsp;|&nbsp; '.join(m.get("kpis",[]))+'</span></div>') if m.get("kpis") else ""}
          {('<div style="margin-top:4px"><span style="font-size:12px;color:#FF9500">🔍 Auto-RCA enabled on delay trigger</span></div>') if m.get("auto_rca") else ""}
        </div>
        {badge(m['status'])}
      </div>
    </div>""",unsafe_allow_html=True)

    idx=mtg_idx(m["id"])
    bc=st.columns([2,2,2,2,4])
    with bc[0]:
        if m["status"]=="Scheduled":
            if st.button("▶️ Start Meeting",type="primary",use_container_width=True):
                if idx is not None:
                    st.session_state.meetings[idx]["status"]="Live"
                    st.session_state.meetings[idx]["history"].append({"ts":str(datetime.now())[:16],"event":f"Started by {st.session_state.user}"})
                st.rerun()
        elif m["status"]=="Live":
            st.markdown('<div class="live-timer" style="background:rgba(34,211,238,.1);border:1px solid #22d3ee;border-radius:8px;padding:6px 12px;color:#22d3ee;font-size:13px">🔴 LIVE</div>',unsafe_allow_html=True)
    with bc[1]:
        if st.button("✅ Confirm Attendance",use_container_width=True): st.toast("Attendance confirmed ✅")
    with bc[2]:
        if m["status"]=="Live":
            if st.button("⏹ End Meeting",use_container_width=True):
                if idx is not None:
                    st.session_state.meetings[idx]["status"]="Completed"
                    st.session_state.meetings[idx]["history"].append({"ts":str(datetime.now())[:16],"event":f"Ended by {st.session_state.user}"})
                st.rerun()
    with bc[3]:
        if m["status"] not in ("Completed","Cancelled"):
            if st.button("❌ Cancel Meeting",use_container_width=True):
                if idx is not None:
                    st.session_state.meetings[idx]["status"]="Cancelled"
                    st.session_state.meetings[idx]["history"].append({"ts":str(datetime.now())[:16],"event":f"Cancelled by {st.session_state.user}"})
                st.rerun()

    t_att,t_agenda,t_attach,t_act,t_hist=st.tabs(["👥 Attendees","📋 Agenda","📎 Attachments","✅ Actions","📜 History"])

    with t_att:
        st.markdown('<p class="section-lbl">Attendee List</p>',unsafe_allow_html=True)
        for ai,att in enumerate(m["attendees"]):
            ac=st.columns([3,2,2])
            ac[0].markdown(f'<span style="color:#e6edf3">{"🎤" if att["facilitator"] else "👤"} {att["name"]}</span>',unsafe_allow_html=True)
            present=ac[1].checkbox("Present",value=att["present"],key=f"att_{m['id']}_{ai}")
            if present!=att["present"] and idx is not None:
                st.session_state.meetings[idx]["attendees"][ai]["present"]=present; st.rerun()
            ac[2].markdown(f'<span style="font-size:12px;color:{"#22d3ee" if att["facilitator"] else "#8b949e"}">{"Facilitator" if att["facilitator"] else "Attendee"}</span>',unsafe_allow_html=True)
        st.divider()
        nc1,nc2=st.columns([3,1])
        with nc1: new_guest=st.text_input("Add Guest","",placeholder="Guest name…",label_visibility="collapsed")
        with nc2:
            if st.button("Add",use_container_width=True) and new_guest.strip():
                if idx is not None: st.session_state.meetings[idx]["attendees"].append({"name":new_guest.strip(),"present":False,"facilitator":False})
                st.rerun()

    with t_agenda:
        live_mode=m["status"]=="Live"
        st.markdown(f'<p class="section-lbl">{"🔴 Live Minutes Mode" if live_mode else "Agenda"}</p>',unsafe_allow_html=True)
        for ai,item in enumerate(m["agenda"]):
            with st.expander(f"**{item['title']}** — {item['subtitle']}  ·  [{item['type']}]"):
                if live_mode:
                    nv=st.text_area("Notes",value=item.get("notes",""),key=f"an_{m['id']}_{ai}",height=70)
                    if nv!=item.get("notes","") and idx is not None: st.session_state.meetings[idx]["agenda"][ai]["notes"]=nv
                    if st.button("🔗 Link Action",key=f"la_{m['id']}_{ai}",type="primary"): action_dialog(prefill_origin=m["title"])
                else:
                    st.markdown(f'<span style="font-size:13px;color:#8b949e">{item.get("notes","No notes yet.")}</span>',unsafe_allow_html=True)
        st.divider()
        with st.expander("➕ Add Agenda Item"):
            ai_t=st.text_input("Title","",key=f"ai_t_{m['id']}"); ai_s=st.text_input("Subtitle","",key=f"ai_s_{m['id']}")
            ai_y=st.selectbox("Type",["Default","Review","Decision","Training","Blocker"],key=f"ai_y_{m['id']}")
            if st.button("Add Item",type="primary",key=f"ai_add_{m['id']}") and ai_t.strip():
                if idx is not None: st.session_state.meetings[idx]["agenda"].append({"title":ai_t,"subtitle":ai_s,"type":ai_y,"notes":""})
                st.rerun()

    with t_attach:
        st.markdown('<p class="section-lbl">Attachments</p>',unsafe_allow_html=True)
        st.markdown('<div class="attach-zone">📎 Drag & drop files here<br><small>PDF, Word, Excel, Images</small></div>',unsafe_allow_html=True)
        upl=st.file_uploader("Upload",label_visibility="collapsed",key=f"mupl_{m['id']}")
        if upl and idx is not None:
            if upl.name not in st.session_state.meetings[idx]["attachments"]:
                st.session_state.meetings[idx]["attachments"].append(upl.name); st.rerun()
        for att in m.get("attachments",[]):
            st.markdown(f'<span style="font-size:13px;color:#22d3ee">📄 {att}</span>',unsafe_allow_html=True)
        if not m.get("attachments"): st.caption("No attachments yet.")

    with t_act:
        st.markdown('<p class="section-lbl">Linked Actions</p>',unsafe_allow_html=True)
        linked=[get_action(aid) for aid in m["linked_actions"] if get_action(aid)]
        for a in linked:
            st.markdown(f"""
            <div style="background:#161b27;border:1px solid #1e3a5f;border-radius:8px;
              padding:10px 14px;margin:5px 0;display:flex;justify-content:space-between;align-items:center">
              <div><span style="color:#6b7280;font-size:11px">#{a['id']}</span>
              <span style="color:#e6edf3;font-size:13px;margin-left:8px">{a['title']}</span>
              <div style="font-size:11px;color:#8b949e;margin-top:2px">{a['team']} &nbsp;•&nbsp; {a['responsible']} &nbsp;•&nbsp; Due: {a['due'].strftime('%d %b %Y')}</div>
              </div>{badge(a['status'])}</div>""",unsafe_allow_html=True)
        if not linked: st.info("No actions linked yet.")
        if st.button("➕ Create Action for this Meeting",type="primary",key=f"caf_{m['id']}"): action_dialog(prefill_origin=m["title"])

    with t_hist:
        st.markdown('<p class="section-lbl">History Log</p>',unsafe_allow_html=True)
        for h in reversed(m.get("history",[])):
            st.markdown(f'<div style="font-size:13px;color:#8b949e;padding:5px 0;border-bottom:1px solid #1e3a5f"><strong style="color:#22d3ee">{h["ts"]}</strong> — {h["event"]}</div>',unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE: ROOT CAUSE ANALYSIS
# ═══════════════════════════════════════════════════════════════
def render_rca():
    if st.session_state.sel_rca:
        r=get_rca(st.session_state.sel_rca)
        if r: render_rca_detail(r); return
        st.session_state.sel_rca=None
    st.title("Root Cause Analysis")
    bc1,_,bc2=st.columns([2,6,2])
    with bc1:
        if st.button("🔍 New RCA",type="primary",use_container_width=True): meeting_dialog(from_rca=True)
    st.divider()
    if not st.session_state.rcas: st.info("No RCAs created yet. Click **New RCA** to begin.")
    for r in st.session_state.rcas:
        col_c,col_b=st.columns([9,1])
        with col_c:
            st.markdown(f"""
            <div class="meeting-card">
              <div style="display:flex;justify-content:space-between;align-items:flex-start">
                <div>
                  <div style="font-weight:700;color:#e6edf3;font-size:15px">RCA #{r['id']} — {r['title']}</div>
                  <div style="font-size:12px;color:#8b949e;margin-top:4px">
                    📅 {r['date'].strftime('%d %b %Y')} &nbsp;•&nbsp;
                    {len(r['linked_actions'])} linked action{'s' if len(r['linked_actions'])!=1 else ''}
                  </div>
                </div>{badge(r['status'])}</div></div>""",unsafe_allow_html=True)
        with col_b:
            st.markdown("<div style='height:20px'></div>",unsafe_allow_html=True)
            if st.button("Open",key=f"or_{r['id']}",use_container_width=True):
                st.session_state.sel_rca=r["id"]; st.rerun()


def render_rca_detail(r):
    if st.button("← Back to RCA List"): st.session_state.sel_rca=None; st.rerun()
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#071539,#0a2050);border:1px solid #1e3a5f;
         border-radius:14px;padding:19px 23px;margin-bottom:13px">
      <div style="font-size:10px;color:#8b949e;text-transform:uppercase;letter-spacing:1.2px">Root Cause Analysis</div>
      <h1 style="color:#22d3ee;margin:3px 0;font-size:1.45rem">RCA #{r['id']} — {r['title']}</h1>
      <div style="font-size:13px;color:#8b949e">📅 {r['date'].strftime('%d %b %Y')} &nbsp;•&nbsp; Status: {r['status']}</div>
    </div>""",unsafe_allow_html=True)
    ri=rca_idx(r["id"])
    tabs=st.tabs(["📄 Summary","❓ 5 Whys","📅 Timeline","⚙️ Factors","💡 Recommendations","✅ Actions"])

    with tabs[0]:
        st.markdown('<p class="section-lbl">Executive Summary</p>',unsafe_allow_html=True)
        es=st.text_area("",value=r["exec_summary"],height=140,key=f"es_{r['id']}")
        if st.button("Save Summary",type="primary",key=f"ses_{r['id']}"):
            if ri is not None: st.session_state.rcas[ri]["exec_summary"]=es
            st.toast("Summary saved ✅")

    with tabs[1]:
        st.markdown('<p class="section-lbl">5 Whys Analysis</p>',unsafe_allow_html=True)
        st.caption("Start with the immediate problem and ask 'why' five times to reach the root cause.")
        updated=[]
        for wi,w in enumerate(r["five_whys"]):
            val=st.text_input(f"Why {wi+1}",value=w,key=f"w_{r['id']}_{wi}")
            updated.append(val)
        if st.button("Save 5 Whys",type="primary",key=f"s5w_{r['id']}"):
            if ri is not None: st.session_state.rcas[ri]["five_whys"]=updated
            st.toast("5 Whys saved ✅")
        if st.button("🔗 Link Action to 5 Whys",key=f"la5w_{r['id']}"): action_dialog(prefill_origin=f"RCA #{r['id']}")

    with tabs[2]:
        st.markdown('<p class="section-lbl">Key Events Timeline</p>',unsafe_allow_html=True)
        for te in r["timeline"]:
            st.markdown(f'<div style="display:flex;gap:14px;padding:8px 0;border-bottom:1px solid #1e3a5f"><span style="color:#22d3ee;font-weight:600;min-width:55px;font-size:13px">{te["time"]}</span><span style="color:#e6edf3;font-size:13px">{te["event"]}</span></div>',unsafe_allow_html=True)
        st.divider()
        tc1,tc2=st.columns([1,3])
        with tc1: nt=st.text_input("Time","",placeholder="e.g. 14:30",key=f"tlt_{r['id']}")
        with tc2: ne=st.text_input("Event","",placeholder="Describe the event…",key=f"tle_{r['id']}")
        if st.button("Add Event",key=f"tla_{r['id']}") and nt.strip() and ne.strip():
            if ri is not None: st.session_state.rcas[ri]["timeline"].append({"time":nt.strip(),"event":ne.strip()})
            st.rerun()
        if st.button("🔗 Link Action to Timeline",key=f"latl_{r['id']}"): action_dialog(prefill_origin=f"RCA #{r['id']}")

    with tabs[3]:
        st.markdown('<p class="section-lbl">Contributing Factors</p>',unsafe_allow_html=True)
        icons={"systems":"🔧","people":"👥","equipment":"⚙️","environment":"🌐","organisational":"🏢"}
        lbls={"systems":"Systems","people":"People","equipment":"Equipment","environment":"Environment","organisational":"Organisational"}
        upd={}
        for fk in r["factors"]:
            upd[fk]=st.text_area(f"{icons[fk]}  {lbls[fk]}",value=r["factors"][fk],height=68,key=f"f_{r['id']}_{fk}")
            if st.button(f"🔗 Link Action to {lbls[fk]}",key=f"lacf_{r['id']}_{fk}",use_container_width=False):
                action_dialog(prefill_origin=f"RCA #{r['id']} – {lbls[fk]}")
        if st.button("Save Contributing Factors",type="primary",key=f"scf_{r['id']}"):
            if ri is not None: st.session_state.rcas[ri]["factors"]=upd
            st.toast("Factors saved ✅")

    with tabs[4]:
        st.markdown('<p class="section-lbl">Recommendations</p>',unsafe_allow_html=True)
        rec=st.text_area("",value=r["recommendations"],height=130,key=f"rec_{r['id']}")
        rc1,rc2,rc3=st.columns(3)
        with rc1:
            if st.button("Save",type="primary",key=f"srec_{r['id']}"):
                if ri is not None: st.session_state.rcas[ri]["recommendations"]=rec
                st.toast("Recommendations saved ✅")
        with rc2:
            if st.button("🔗 Create Action",key=f"carec_{r['id']}",type="primary"): action_dialog(prefill_origin=f"RCA #{r['id']}")
        with rc3:
            if st.button("📄 Export PDF (Demo)",key=f"pdf_{r['id']}"):
                st.info("PDF export available in the full enterprise build.")

    with tabs[5]:
        st.markdown('<p class="section-lbl">Linked Actions</p>',unsafe_allow_html=True)
        linked=[get_action(aid) for aid in r["linked_actions"] if get_action(aid)]
        for a in linked:
            st.markdown(f"""
            <div style="background:#161b27;border:1px solid #1e3a5f;border-radius:8px;padding:10px 14px;margin:5px 0;
              display:flex;justify-content:space-between;align-items:center">
              <div><span style="color:#6b7280;font-size:11px">#{a['id']}</span>
              <span style="color:#e6edf3;font-size:13px;margin-left:8px">{a['title']}</span>
              <div style="font-size:11px;color:#8b949e">{a['team']} &nbsp;•&nbsp; {a['responsible']}</div>
              </div>{badge(a['status'])}</div>""",unsafe_allow_html=True)
        if not linked: st.info("No actions linked yet.")
        if st.button("➕ Link New Action",type="primary",key=f"larc_{r['id']}"): action_dialog(prefill_origin=f"RCA #{r['id']}")
        st.divider()
        new_stat="Closed" if r["status"]=="Open" else "Open"
        if st.button(f"{'🔒 Close' if r['status']=='Open' else '🔓 Reopen'} RCA",key=f"rcs_{r['id']}"):
            if ri is not None: st.session_state.rcas[ri]["status"]=new_stat
            st.rerun()


# ═══════════════════════════════════════════════════════════════
#  PAGE: PROJECTS
# ═══════════════════════════════════════════════════════════════
def render_projects():
    st.title("Projects")
    bc1,_=st.columns([2,8])
    with bc1:
        if st.button("➕ New Project",type="primary",use_container_width=True): project_dialog()
    st.divider()
    if not st.session_state.projects: st.info("No projects yet.")
    for p in st.session_state.projects:
        days_left=(p["end"]-date.today()).days
        c_info,c_prog=st.columns([6,2])
        with c_info:
            st.markdown(f"""
            <div style="background:#161b27;border:1px solid #1e3a5f;border-radius:12px;padding:15px 19px;height:105px;display:flex;flex-direction:column;justify-content:center">
              <div style="font-weight:700;color:#e6edf3;font-size:15px">{p['name']}</div>
              <div style="font-size:12px;color:#8b949e;margin-top:4px">👤 {p['owner']} &nbsp;•&nbsp; 🏷 {p['team']}</div>
              <div style="font-size:12px;color:#8b949e;margin-top:2px">
                📅 {p['start'].strftime('%d %b %Y')} → {p['end'].strftime('%d %b %Y')}
                &nbsp;•&nbsp; {'🔴 '+str(abs(days_left))+' days overdue' if days_left<0 else '⏳ '+str(days_left)+' days remaining'}
                &nbsp;•&nbsp; ✅ {p['actions']} linked actions
              </div>
            </div>""",unsafe_allow_html=True)
        with c_prog:
            st.markdown(f"""
            <div style="background:#161b27;border:1px solid #1e3a5f;border-radius:12px;padding:15px;text-align:center;height:105px;display:flex;flex-direction:column;justify-content:center">
              <div style="font-size:2rem;font-weight:700;color:#22d3ee">{p['progress']}%</div>
              <div style="font-size:10px;color:#8b949e;text-transform:uppercase;letter-spacing:.5px;margin:2px 0">Complete</div>
              {pbar(p['progress'])}
            </div>""",unsafe_allow_html=True)
        st.markdown("<div style='height:7px'></div>",unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  PAGE: ADMIN CONFIGURATION
# ═══════════════════════════════════════════════════════════════
def render_admin():
    st.title("Admin Configuration")
    st.caption("Manage all configurable lists, labels, users, and metric definitions.")
    st.divider()
    tabs=st.tabs(["🏷 Teams","📍 Locations","📋 Meeting Types","👥 Users","📊 Metric Definitions","🎨 Status Labels"])

    def editable_list(key,label,nk,bk):
        items=st.session_state.admin[key]
        for i,item in enumerate(items):
            c1,c2=st.columns([8,1])
            c1.markdown(f'<span style="color:#e6edf3;font-size:13px">• {item}</span>',unsafe_allow_html=True)
            if c2.button("✕",key=f"dl_{key}_{i}"): st.session_state.admin[key].pop(i); st.rerun()
        nv=st.text_input(f"Add {label}","",key=nk)
        if st.button(f"Add {label}",type="primary",key=bk) and nv.strip():
            st.session_state.admin[key].append(nv.strip()); st.rerun()

    with tabs[0]:
        st.markdown('<p class="section-lbl">Teams / Functions</p>',unsafe_allow_html=True)
        editable_list("teams","Team","nt","abt")
    with tabs[1]:
        st.markdown('<p class="section-lbl">Locations & Rooms</p>',unsafe_allow_html=True)
        editable_list("locations","Location","nl","abl")
    with tabs[2]:
        st.markdown('<p class="section-lbl">Meeting Types</p>',unsafe_allow_html=True)
        editable_list("meeting_types","Meeting Type","nm","abm")
    with tabs[3]:
        st.markdown('<p class="section-lbl">Users</p>',unsafe_allow_html=True)
        for i,u in enumerate(st.session_state.admin["users"]):
            c1,c2=st.columns([8,1])
            is_me=u==st.session_state.user
            c1.markdown(f'<span style="color:{"#22d3ee" if is_me else "#e6edf3"};font-size:13px">{"🔵 " if is_me else "• "}{u}{"  (you)" if is_me else ""}</span>',unsafe_allow_html=True)
            if c2.button("✕",key=f"dlu_{i}") and not is_me: st.session_state.admin["users"].pop(i); st.rerun()
        nu=st.text_input("Add User","",key="nu_inp")
        if st.button("Add User",type="primary",key="abu") and nu.strip():
            st.session_state.admin["users"].append(nu.strip()); st.rerun()
        st.divider()
        st.markdown('<p class="section-lbl">Switch Current User (Demo)</p>',unsafe_allow_html=True)
        users=st.session_state.admin["users"]
        me_i=users.index(st.session_state.user) if st.session_state.user in users else 0
        new_me=st.selectbox("Log in as",users,index=me_i)
        if st.button("Switch User") and new_me!=st.session_state.user:
            st.session_state.user=new_me; st.rerun()
    with tabs[4]:
        st.markdown('<p class="section-lbl">Metric Definitions</p>',unsafe_allow_html=True)
        st.caption("Define KPI metrics available across the system for meetings, reports, and dashboards.")
        for md in st.session_state.admin.get("metric_defs",[]):
            kpi_tag = '<span style="color:#34C759">KPI</span>' if md["kpi"] else ""
            row_html = '<div style="padding:8px 0;border-bottom:1px solid #1e3a5f;color:#e6edf3">' + md["name"] + '  |  ' + md["unit"] + '  |  ' + md["type"] + '  ' + kpi_tag + '</div>'
            st.markdown(row_html, unsafe_allow_html=True)
        with st.expander("➕ Add Metric Definition"):
            mn=st.text_input("Metric Name",""); mu=st.text_input("Unit (e.g. %, Count, $)","")
            mt=st.selectbox("Type",["Number","Percentage","Currency","Rate"]); mk=st.checkbox("Mark as KPI",value=True)
            if st.button("Add Metric",type="primary") and mn.strip():
                st.session_state.admin["metric_defs"].append({"name":mn,"unit":mu,"type":mt,"kpi":mk}); st.rerun()
    with tabs[5]:
        st.markdown('<p class="section-lbl">Status Colour Reference</p>',unsafe_allow_html=True)
        for s,hx,nm in [("Active","#22d3ee","Cyan"),("In Progress","#34C759","Green"),
                         ("Pending","#FF9500","Amber"),("Overdue","#FF3B30","Red"),("Closed","#6E6E6E","Grey")]:
            st.markdown(f'<div style="display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px solid #1e3a5f"><div style="width:16px;height:16px;border-radius:50%;background:{hx}"></div><span style="color:#e6edf3;min-width:120px">{s}</span><code style="color:#8b949e">{hx}</code><span style="color:#6b7280;font-size:12px">— {nm}</span></div>',unsafe_allow_html=True)
        st.caption("Colour customisation available in the full enterprise build.")


# ═══════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:6px 0 18px 0">
      <div style="display:flex;align-items:center;gap:10px">
        <div style="width:38px;height:38px;border-radius:50%;
             background:radial-gradient(circle at 35% 30%,#1a4a7a,#071539);
             border:1.5px solid rgba(34,211,238,.5);
             display:flex;align-items:center;justify-content:center">
          <span style="color:#22d3ee;font-weight:900;font-size:17px">M</span>
        </div>
        <div>
          <div style="color:#22d3ee;font-weight:700;font-size:17px;letter-spacing:-.5px">mos | NEXIS</div>
          <div style="color:#6b7280;font-size:9.5px;letter-spacing:1.2px;text-transform:uppercase">Action &amp; Review</div>
        </div>
      </div>
    </div>""",unsafe_allow_html=True)

    od_count=len(overdue_actions())
    if od_count:
        st.markdown(
            f'<div style="background:rgba(255,59,48,.12);border:1px solid rgba(255,59,48,.3);'
            f'border-radius:8px;padding:7px 12px;margin-bottom:10px;font-size:12px;color:#FF3B30">'
            f'⚠️ {od_count} overdue action{"s" if od_count!=1 else ""}</div>',
            unsafe_allow_html=True)

    st.divider()
   nav_pages = ["Dashboard", "Actions", "Meetings", "Root Cause Analysis", "Projects", "Admin Configuration"]
    icons = {"Dashboard":"🏠", "Actions":"✅", "Meetings":"📅", "Root Cause Analysis":"🔍", "Projects":"📂", "Admin Configuration":"⚙️"}

    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    selected = st.radio(
        label="Navigation",
        options=nav_pages,
        key="nav_radio",
        index=nav_pages.index(st.session_state.page),
        label_visibility="collapsed",
        format_func=lambda x: f"{icons.get(x, '')}  {x}"
    )
    st.session_state.page = selected   # safe sync
    st.divider()
    if st.button("⚠️ Log Deviation",use_container_width=True,key="sb_dev"): deviation_dialog()
    st.divider()
    st.markdown(f"""
    <div style="padding:6px 0">
      <div style="font-size:10px;color:#6b7280;text-transform:uppercase;letter-spacing:.5px;margin-bottom:5px">Logged in as</div>
      <div style="color:#22d3ee;font-weight:600;font-size:14px">{st.session_state.user}</div>
      <div style="font-size:11px;color:#6b7280">Site Executive</div>
    </div>""",unsafe_allow_html=True)
    st.divider()
    st.markdown('<p style="font-size:9.5px;color:rgba(34,211,238,.38);font-style:italic;text-align:center;letter-spacing:.6px">We will always have a plan.</p>',unsafe_allow_html=True)
    st.caption("10 April 2026  •  Yeppoon, Queensland")


# ═══════════════════════════════════════════════════════════════
#  ROUTING
# ═══════════════════════════════════════════════════════════════
{
    "Dashboard":           render_dashboard,
    "Actions":             render_actions,
    "Meetings":            render_meetings,
    "Root Cause Analysis": render_rca,
    "Projects":            render_projects,
    "Admin Configuration": render_admin,
}.get(selected, render_dashboard)()


# ═══════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════
st.divider()
st.markdown('<p class="nexis-footer">We will always have a plan. &nbsp;—&nbsp; mos | NEXIS Action &amp; Review &nbsp;•&nbsp; Yeppoon, Queensland</p>',unsafe_allow_html=True)

