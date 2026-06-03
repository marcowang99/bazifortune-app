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
    
    # 术语解释弹窗
    with st.expander("📖 看不懂术语？点这里查看白话解释"):
        terms = r.get("terms", {})
        for term, meaning in terms.items():
            st.markdown(f"**{term}**：{meaning}")
    
    st.divider()
    st.subheader("📜 你的八字命盘")
    cols = st.columns(4)
    names = ["年柱（祖上/童年）","月柱（父母/青年）","日柱（自己/中年）","时柱（子女/晚年）"]
    keys = ["year","month","day","hour"]
    for i,(n,k) in enumerate(zip(names,keys)):
        g,zh = bazi[k]
        with cols[i]:
            st.metric(n, f"{g}{zh}")
            ss = r['shishen'][k]['gan']
            ss_full = r['terms'].get(ss, ss)
            st.caption(f"天干：{ss_full}")
            st.caption(f"纳音：{r['nayin'][k]}")
            cg_items = []
            for cg,ss in r['shishen'][k]['zhi'].items():
                ss_full = r['terms'].get(ss, ss)
                # 提取括号里的白话
                if "（" in ss_full:
                    baihua = ss_full.split("（")[1].rstrip("）")
                    cg_items.append(f"{cg}({baihua})")
                else:
                    cg_items.append(f"{cg}({ss})")
            st.caption(f"藏干：{' | '.join(cg_items)}")
    
    st.divider()
    st.subheader("⚖️ 五行能量分布")
    wx_cols = st.columns(5)
    for i,(wx,val) in enumerate(r['wuxing_stats'].items()):
        pct = min(val/6, 1.0)
        with wx_cols[i]:
            st.progress(pct, text=f"{wx} {val:.1f}")
    
    # 五行强弱解读
    max_wx = max(r['wuxing_stats'], key=r['wuxing_stats'].get)
    min_wx = min(r['wuxing_stats'], key=r['wuxing_stats'].get)
    max_trait = r['wuxing_traits'].get(f"{max_wx}旺", "")
    min_trait = r['wuxing_traits'].get(f"{min_wx}弱", "")
    st.info(f"💡 **五行解读**：你命中{max_wx}最旺（{r['wuxing_stats'][max_wx]:.1f}），{max_trait}；{min_wx}最弱（{r['wuxing_stats'][min_wx]:.1f}），{min_trait}")
    
    st.divider()
    st.subheader("💪 你的能量状态（旺衰）")
    ws = r['wangshuai_detail']
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info(f"**{ws['deling']['text']}（{r['terms'].get(ws['deling']['text'], ws['deling']['text'])}）**\n\n{ws['deling']['desc']}")
    with c2:
        st.info(f"**{ws['dedi']['text']}（{r['terms'].get(ws['dedi']['text'], ws['dedi']['text'])}）**\n\n{ws['dedi']['desc']}")
    with c3:
        st.info(f"**{ws['deshi']['text']}（{r['terms'].get(ws['deshi']['text'], ws['deshi']['text'])}）**\n\n{ws['deshi']['desc']}")
    
    st.success(f"综合判定：**{ws['wangshuai']}**（{ws['wangshuai_baihua']}）— 得分：{ws['score']}/3")
    
    st.divider()
    a,b,c = st.columns(3)
    a.info(f"**格局：** {r['geju']['name']}")
    b.success(f"**喜用神（对你有利）：** {', '.join(r['xiyong'])}")
    c.error(f"**忌神（对你不利）：** {', '.join(r['jishen'])}")
    
    # 喜用神白话解释
    xiyong_baihua = {
        "金": "金（金融、汽车、科技、白色/金色）",
        "木": "木（教育、文化、服装、绿色）",
        "水": "水（贸易、物流、旅游、黑色/蓝色）",
        "火": "火（餐饮、能源、美容、红色）",
        "土": "土（房地产、建筑、农业、黄色/棕色）",
        "调候": "调候（夏天喜水降温，冬天喜火取暖）"
    }
    st.write("💡 **喜用神白话**：" + "；".join([xiyong_baihua.get(x, x) for x in r['xiyong']]))
    
    st.divider()
    st.subheader("🎯 命局分析")
    st.write(r["geju"]["desc"])
    
    if r["combos"]:
        st.subheader("🔮 你的命运组合（关键特征）")
        for combo in r["combos"]:
            if combo["level"]=="吉":
                with st.container(border=True):
                    st.success(f"✅ **{combo['name']}** — {combo['baihua']}")
                    st.write(combo["detail"])
                    for adv in combo["advice"]:
                        st.markdown(adv)
            elif combo["level"]=="凶":
                with st.container(border=True):
                    st.error(f"❌ **{combo['name']}** — {combo['baihua']}")
                    st.write(combo["detail"])
                    for adv in combo["advice"]:
                        st.markdown(adv)
            else:
                with st.container(border=True):
                    st.warning(f"⚠️ **{combo['name']}** — {combo['baihua']}")
                    st.write(combo["detail"])
                    for adv in combo["advice"]:
                        st.markdown(adv)
    
    if r["chonghe"]:
        st.subheader("⚡ 命运波动点（刑冲合害）")
        for ch in r["chonghe"]:
            if ch["type"] == "冲":
                st.error(f"💥 **{ch['name']}**：{ch['position']} → {ch['effect']}")
            elif ch["type"] == "伏吟":
                st.warning(f"🔄 **{ch['name']}**：{ch['position']} → {ch['effect']}")
            else:
                st.info(f"🔗 **{ch['name']}**：{ch['position']} → {ch['effect']}")
    
    st.divider()
    st.subheader("📋 人生建议（按场景分类）")
    tabs = st.tabs(["💼 事业","💰 财运","💑 婚姻","🏥 健康"])
    with tabs[0]:
        st.markdown("### 事业方向")
        for item in r["advice"]["xingye"]:
            st.markdown(item)
        if not r["advice"]["xingye"]:
            st.write("暂无特殊建议，根据喜用神选择相关行业即可")
    with tabs[1]:
        st.markdown("### 财富积累")
        for item in r["advice"]["caifu"]:
            st.markdown(item)
        if not r["advice"]["caifu"]:
            st.write("暂无特殊建议，稳健理财即可")
    with tabs[2]:
        st.markdown("### 感情婚姻")
        for item in r["advice"]["hunyin"]:
            st.markdown(item)
        if not r["advice"]["hunyin"]:
            st.write("暂无特殊建议，顺其自然")
    with tabs[3]:
        st.markdown("### 健康提醒")
        for item in r["advice"]["jiankang"]:
            st.markdown(item)
        if not r["advice"]["jiankang"]:
            st.write("暂无特殊建议，保持规律作息")
