import streamlit as st
import json
from engine import BaziEngine

st.set_page_config(page_title="八字测算", layout="centered")
st.title("🔮 八字测算系统")

with open("rules.json", "r", encoding="utf-8") as f:
    rules = json.load(f)
engine = BaziEngine(rules)

c1, c2 = st.columns(2)
with c1:
    y = st.number_input("年", 1900, 2100, 1982)
    m = st.number_input("月", 1, 12, 8)
    d = st.number_input("日", 1, 31, 23)
with c2:
    h = st.number_input("时", 0, 23, 19)
    mi = st.number_input("分", 0, 59, 15)
    gender = st.selectbox("性别", ["男", "女"])

if st.button("开始测算", type="primary"):
    bazi, lunar = engine.paipan(int(y), int(m), int(d), int(h), int(mi), gender)
    r = engine.analyze(bazi)
    
    st.divider()
    st.subheader("📜 四柱命盘")
    cols = st.columns(4)
    names = ["年柱","月柱","日柱","时柱"]
    keys = ["year","month","day","hour"]
    for i,(n,k) in enumerate(zip(names,keys)):
        g,zh = bazi[k]
        with cols[i]:
            st.metric(n, f"{g}{zh}")
            st.caption(f"天干：{r['shishen'][k]['gan']} | 纳音：{r['nayin'][k]}")
            cg_text = " | ".join([f"{cg}({ss})" for cg,ss in r['shishen'][k]['zhi'].items()])
            st.caption(f"藏干：{cg_text}")
    
    st.divider()
    st.subheader("⚖️ 五行力量")
    wx_cols = st.columns(5)
    for i,(wx,val) in enumerate(r['wuxing_stats'].items()):
        pct = min(val/6, 1.0)
        with wx_cols[i]:
            st.progress(pct, text=f"{wx} {val:.1f}")
    
    st.divider()
    st.subheader("💪 旺衰详解")
    ws = r['wangshuai_detail']
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info(f"**得令：{ws['deling']['text']}**\n\n{ws['deling']['desc']}")
    with c2:
        st.info(f"**得地：{ws['dedi']['text']}**\n\n{ws['dedi']['desc']}")
    with c3:
        st.info(f"**得势：{ws['deshi']['text']}**\n\n{ws['deshi']['desc']}")
    st.success(f"综合判定：**{ws['wangshuai']}**（得分：{ws['score']}/3）")
    
    st.divider()
    a,b,c = st.columns(3)
    a.info(f"**格局：** {r['geju']['name']}")
    b.info(f"**喜用神：** {', '.join(r['xiyong'])}")
    c.info(f"**忌神：** {', '.join(r['geju']['ji_shen'])}")
    
    st.divider()
    st.subheader("🎯 命局分析")
    st.write(r["geju"]["desc"])
    
    if r["combos"]:
        st.subheader("🔮 十神组合")
        for combo in r["combos"]:
            if combo["level"]=="吉":
                with st.container(border=True):
                    st.success(f"**{combo['name']}**（吉）")
                    st.write(combo["detail"])
                    for adv in combo["advice"]:
                        st.markdown(f"✅ {adv}")
            elif combo["level"]=="凶":
                with st.container(border=True):
                    st.error(f"**{combo['name']}**（凶）")
                    st.write(combo["detail"])
                    for adv in combo["advice"]:
                        st.markdown(f"⚠️ {adv}")
            else:
                with st.container(border=True):
                    st.warning(f"**{combo['name']}**（平）")
                    st.write(combo["detail"])
                    for adv in combo["advice"]:
                        st.markdown(f"ℹ️ {adv}")
    
    if r["chonghe"]:
        st.subheader("⚡ 刑冲合害")
        for ch in r["chonghe"]:
            if ch["type"] == "冲":
                st.error(f"**{ch['name']}**：{ch['position']} → {ch['effect']}")
            elif ch["type"] == "伏吟":
                st.warning(f"**{ch['name']}**：{ch['position']} → {ch['effect']}")
            else:
                st.info(f"**{ch['name']}**：{ch['position']} → {ch['effect']}")
    
    st.divider()
    st.subheader("📋 人生建议")
    tabs = st.tabs(["事业","财运","婚姻","健康"])
    with tabs[0]:
        for item in r["advice"]["xingye"]:
            st.markdown(f"- {item}")
    with tabs[1]:
        for item in r["advice"]["caifu"]:
            st.markdown(f"- {item}")
    with tabs[2]:
        for item in r["advice"]["hunyin"]:
            st.markdown(f"- {item}")
    with tabs[3]:
        for item in r["advice"]["jiankang"]:
            st.markdown(f"- {item}")