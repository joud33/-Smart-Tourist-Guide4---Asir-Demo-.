import streamlit as st
from dataclasses import dataclass
from typing import List, Dict

st.set_page_config(page_title="الدليل السياحي الذكي - عسير", page_icon="🏞️", layout="wide")

ASIR_CSS = """
<style>
:root{
  --asir-green:#0f6b4f;
  --asir-dark:#0b2e24;
  --asir-sand:#efe7d6;
  --asir-fog:#f6f7f7;
  --asir-accent:#b07a3a;
}

html, body, [class*="css"]  { direction: rtl; font-family: "Tahoma", "Arial", sans-serif; }
.stApp { background: linear-gradient(180deg, var(--asir-fog) 0%, #ffffff 55%, var(--asir-sand) 120%); }

.hero{
  background: linear-gradient(135deg, var(--asir-green), var(--asir-dark));
  border-radius: 18px;
  padding: 22px 22px;
  color: white;
  box-shadow: 0 10px 24px rgba(0,0,0,0.10);
}
.hero h1{ margin: 0; font-size: 30px; }
.hero p{ margin: 6px 0 0 0; opacity: 0.92; line-height: 1.7; }

.badge{
  display:inline-block;
  background: rgba(255,255,255,0.16);
  padding: 6px 10px;
  border-radius: 999px;
  margin-left: 8px;
  font-size: 12px;
}

.card{
  background: white;
  border-radius: 16px;
  padding: 16px;
  border: 1px solid rgba(15,107,79,0.15);
  box-shadow: 0 6px 16px rgba(0,0,0,0.06);
  height: 100%;
}
.tag{
  display:inline-block;
  border: 1px solid rgba(176,122,58,0.45);
  color: var(--asir-accent);
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  margin: 4px 6px 0 0;
}
.smallmuted{ color: rgba(0,0,0,0.60); font-size: 13px; }
hr{ border: none; border-top: 1px solid rgba(0,0,0,0.08); margin: 14px 0; }
</style>
"""

st.markdown(ASIR_CSS, unsafe_allow_html=True)

@dataclass
class Place:
    name: str
    city: str
    category: str
    duration_hours: float
    cost_level: str   # "منخفض" / "متوسط" / "مرتفع"
    best_time: str    # "صباح" / "ظهر" / "مساء"
    description: str
    maps_url: str

PLACES: List[Place] = [
    Place(
        name="ممشى الضباب",
        city="أبها",
        category="طبيعة",
        duration_hours=2.0,
        cost_level="منخفض",
        best_time="مساء",
        description="ممشى لطيف بإطلالة جميلة وجو غالبًا منعش خصوصًا المساء.",
        maps_url="https://www.google.com/maps/search/?api=1&query=ممشى+الضباب+أبها"
    ),
    Place(
        name="الجبل الأخضر",
        city="أبها",
        category="طبيعة",
        duration_hours=2.5,
        cost_level="متوسط",
        best_time="مساء",
        description="وجهة مشهورة بإطلالات وتجربة تلفريك/جلسات حسب الموسم.",
        maps_url="https://www.google.com/maps/search/?api=1&query=الجبل+الأخضر+أبها"
    ),
    Place(
        name="قرية المفتاحة",
        city="أبها",
        category="ثقافة/تراث",
        duration_hours=2.0,
        cost_level="منخفض",
        best_time="مساء",
        description="ساحة ثقافية وفنية وممرات جميلة للتصوير وتجربة الفن المحلي.",
        maps_url="https://www.google.com/maps/search/?api=1&query=قرية+المفتاحة+أبها"
    ),
    Place(
        name="قرية رجال ألمع التراثية",
        city="رجال ألمع",
        category="ثقافة/تراث",
        duration_hours=3.0,
        cost_level="متوسط",
        best_time="صباح",
        description="موقع تراثي مميز بعمارة عسيرية وتجربة غنية للزوار.",
        maps_url="https://www.google.com/maps/search/?api=1&query=قرية+رجال+ألمع+التراثية"
    ),
    Place(
        name="ممشى الخميس",
        city="خميس مشيط",
        category="تجربة/جلسات",
        duration_hours=1.5,
        cost_level="منخفض",
        best_time="مساء",
        description="ممشى مناسب للعائلات وجلسات قريبة وخيارات خفيفة.",
        maps_url="https://www.google.com/maps/search/?api=1&query=ممشى+خميس+مشيط"
    ),
    Place(
        name="قهوة مختصة (اقتراح تجريبي)",
        city="أبها / خميس مشيط",
        category="مقاهي",
        duration_hours=1.0,
        cost_level="متوسط",
        best_time="مساء",
        description="خيار مرن — ضعي اسم المقهى لاحقًا أو اتركيه كاقتراح عام في النسخة التجريبية.",
        maps_url="https://www.google.com/maps/search/?api=1&query=Specialty+coffee+Asir"
    ),
    Place(
        name="هايكنق / مسار مشي (اقتراح)",
        city="عسير",
        category="مغامرات",
        duration_hours=3.0,
        cost_level="منخفض",
        best_time="صباح",
        description="للتجربة: إضافة مسار مشي مناسب حسب الموسم والطقس.",
        maps_url="https://www.google.com/maps/search/?api=1&query=Hiking+Asir"
    ),
]

COST_RANK = {"منخفض": 1, "متوسط": 2, "مرتفع": 3}

def budget_to_rank(budget: str) -> int:
    if budget == "اقتصادي":
        return 1
    if budget == "متوسط":
        return 2
    return 3

def pick_places(days: int, budget: str, interests: List[str]) -> Dict[int, List[Place]]:
    max_rank = budget_to_rank(budget)
    filtered = [
        p for p in PLACES
        if COST_RANK.get(p.cost_level, 2) <= max_rank and (p.category in interests)
    ]
    if not filtered:
        filtered = [p for p in PLACES if (p.category in interests)] or PLACES[:]

    plan: Dict[int, List[Place]] = {}
    slots_per_day = 3 if days <= 2 else 2
    idx = 0
    for d in range(1, days + 1):
        day_list = []
        for _ in range(slots_per_day):
            if idx >= len(filtered):
                idx = 0
            day_list.append(filtered[idx])
            idx += 1
        plan[d] = day_list
    return plan

def place_card(p: Place):
    st.markdown(
        f"""
        <div class="card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;">
            <div>
              <div style="font-size:18px;font-weight:700;color:#0b2e24;">{p.name}</div>
              <div class="smallmuted">{p.city} • {p.best_time} • {p.duration_hours} ساعة تقريبًا</div>
            </div>
            <div class="tag">{p.cost_level}</div>
          </div>
          <hr/>
          <div class="smallmuted" style="line-height:1.7;">{p.description}</div>
          <div style="margin-top:12px;">
            <a href="{p.maps_url}" target="_blank" style="text-decoration:none;">
              <span class="tag">📍 فتح في الخرائط</span>
            </a>
            <span class="tag">{p.category}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class="hero">
      <span class="badge">نسخة تجريبية</span>
      <span class="badge">هوية عسير</span>
      <h1>🏞️ الدليل السياحي الذكي - عسير</h1>
      <p>اختاري عدد الأيام واهتماماتك وميزانيتك… ويطلع لك برنامج زيارة مقترح بأماكن محدودة كتجربة توضيحية قابلة للتطوير.</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")
colA, colB = st.columns([1, 2], gap="large")

with colA:
    st.subheader("إعداد رحلتك")
    days = st.slider("عدد الأيام", 1, 5, 2)
    budget = st.radio("الميزانية", ["اقتصادي", "متوسط", "مرتفعة"], horizontal=True)

    interests_all = ["طبيعة", "ثقافة/تراث", "مقاهي", "مغامرات", "تجربة/جلسات"]
    interests = st.multiselect("اهتماماتك", interests_all, default=["طبيعة", "ثقافة/تراث"])

    st.caption("ملاحظة: هذه نسخة تجريبية ببيانات محدودة للتوضيح فقط.")

with colB:
    st.subheader("النتيجة")
    if len(interests) == 0:
        st.info("اختاري اهتمام واحد على الأقل عشان نبني لك الخطة.")
    else:
        plan = pick_places(days, budget, interests)
        for d, places in plan.items():
            st.markdown(f"### اليوم {d}")
            c1, c2 = st.columns(2, gap="medium")
            for i, p in enumerate(places):
                with (c1 if i % 2 == 0 else c2):
                    place_card(p)

st.write("")
st.markdown("—")
st.caption("© نموذج تجريبي توضيحي — قابل للتطوير بإضافة أماكن رسمية، خرائط تفاعلية، وحجز/تقييمات.")
