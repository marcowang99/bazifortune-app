from lunar_python import Solar, Lunar

class BaziEngine:
    def __init__(self, rules):
        self.rules = rules
        self.gan_wx = {"甲":"木","乙":"木","丙":"火","丁":"火","戊":"土","己":"土","庚":"金","辛":"金","壬":"水","癸":"水"}
        self.zhi_wx = {"子":"水","丑":"土","寅":"木","卯":"木","辰":"土","巳":"火","午":"火","未":"土","申":"金","酉":"金","戌":"土","亥":"水"}
        self.gan_yy = {"甲":"阳","乙":"阴","丙":"阳","丁":"阴","戊":"阳","己":"阴","庚":"阳","辛":"阴","壬":"阳","癸":"阴"}
        self.sheng = {"木":"水","火":"木","土":"火","金":"土","水":"金"}
        self.zhi_cg = {
            "子":["癸"],"丑":["己","癸","辛"],"寅":["甲","丙","戊"],"卯":["乙"],
            "辰":["戊","乙","癸"],"巳":["丙","庚","戊"],"午":["丁","己"],
            "未":["己","丁","乙"],"申":["庚","壬","戊"],"酉":["辛"],
            "戌":["戊","辛","丁"],"亥":["壬","甲"]
        }
        self.nayin = {
            '甲子':'海中金','乙丑':'海中金','丙寅':'炉中火','丁卯':'炉中火',
            '戊辰':'大林木','己巳':'大林木','庚午':'路旁土','辛未':'路旁土',
            '壬申':'剑锋金','癸酉':'剑锋金','甲戌':'山头火','乙亥':'山头火',
            '丙子':'涧下水','丁丑':'涧下水','戊寅':'城头土','己卯':'城头土',
            '庚辰':'白蜡金','辛巳':'白蜡金','壬午':'杨柳木','癸未':'杨柳木',
            '甲申':'泉中水','乙酉':'泉中水','丙戌':'屋上土','丁亥':'屋上土',
            '戊子':'霹雳火','己丑':'霹雳火','庚寅':'松柏木','辛卯':'松柏木',
            '壬辰':'长流水','癸巳':'长流水','甲午':'砂中金','乙未':'砂中金',
            '丙申':'山下火','丁酉':'山下火','戊戌':'平地木','己亥':'平地木',
            '庚子':'壁上土','辛丑':'壁上土','壬寅':'金箔金','癸卯':'金箔金',
            '甲辰':'覆灯火','乙巳':'覆灯火','丙午':'天河水','丁未':'天河水',
            '戊申':'大驿土','己酉':'大驿土','庚戌':'钗钏金','辛亥':'钗钏金',
            '壬子':'桑柘木','癸丑':'桑柘木','甲寅':'大溪水','乙卯':'大溪水',
            '丙辰':'沙中土','丁巳':'沙中土','戊午':'天上火','己未':'天上火',
            '庚申':'石榴木','辛酉':'石榴木','壬戌':'大海水','癸亥':'大海水'
        }
    
    def get_nayin(self, gan, zhi):
        return self.nayin.get(gan+zhi, '未知')
    
    def shishen(self, day_gan, target):
        d_wx, d_yy = self.gan_wx[day_gan], self.gan_yy[day_gan]
        t_wx, t_yy = self.gan_wx[target], self.gan_yy[target]
        if t_wx == d_wx: return "比肩" if t_yy==d_yy else "劫财"
        if self.sheng[d_wx] == t_wx: return "偏印" if t_yy==d_yy else "正印"
        if (d_wx=="木" and t_wx=="火") or (d_wx=="火" and t_wx=="土") or (d_wx=="土" and t_wx=="金") or (d_wx=="金" and t_wx=="水") or (d_wx=="水" and t_wx=="木"):
            return "食神" if t_yy==d_yy else "伤官"
        if (d_wx=="木" and t_wx=="金") or (d_wx=="火" and t_wx=="水") or (d_wx=="土" and t_wx=="木") or (d_wx=="金" and t_wx=="火") or (d_wx=="水" and t_wx=="土"):
            return "七杀" if t_yy==d_yy else "正官"
        return "偏财" if t_yy==d_yy else "正财"
    
    def paipan(self, y, m, d, h, min, gender):
        solar = Solar.fromYmdHms(y, m, d, h, min, 0)
        lunar = solar.getLunar()
        year_gz = lunar.getYearInGanZhi()
        month_gz = lunar.getMonthInGanZhi()
        day_gz = lunar.getDayInGanZhi()
        hour_gz = lunar.getTimeInGanZhi()
        bazi = {
            "year": (year_gz[0], year_gz[1]),
            "month": (month_gz[0], month_gz[1]),
            "day": (day_gz[0], day_gz[1]),
            "hour": (hour_gz[0], hour_gz[1])
        }
        return bazi, lunar
    
    def calc_wuxing_stats(self, bazi):
        stats = {"木":0, "火":0, "土":0, "金":0, "水":0}
        for z,(g,zh) in bazi.items():
            stats[self.gan_wx[g]] += 1
        for z,(g,zh) in bazi.items():
            cgs = self.zhi_cg[zh]
            for i,cg in enumerate(cgs):
                w = 0.5 if i==0 else (0.3 if i==1 else 0.2)
                stats[self.gan_wx[cg]] += w
        return stats
    
    def calc_wangshuai_detail(self, bazi, day_gan):
        dg = day_gan
        dwx = self.gan_wx[dg]
        mz = bazi["month"][1]
        dz = bazi["day"][1]
        
        month_wx = self.zhi_wx[mz]
        deling = month_wx in [self.sheng[dwx], dwx]
        if month_wx == self.sheng[dwx]:
            deling_desc = f"月令{mz}({month_wx})生扶日主{dwx}，当令而旺"
        elif month_wx == dwx:
            deling_desc = f"月令{mz}({month_wx})与日主同五行，比劫当令"
        else:
            deling_desc = f"月令{mz}({month_wx})泄耗/克制日主{dwx}，失令"
        
        has_root = False
        root_zhi = []
        for z,(g,zh) in bazi.items():
            cgs = self.zhi_cg[zh]
            if any(self.gan_wx[cg]==dwx for cg in cgs):
                has_root = True
                root_zhi.append(zh)
        has_root = has_root or self.zhi_wx[dz] == dwx
        dedi_desc = f"地支{'、'.join(root_zhi)}中藏有{dwx}根气，日主有根" if root_zhi else "地支无强根，日主虚浮"
        
        gan_list = [bazi["year"][0], bazi["month"][0], bazi["hour"][0]]
        bj = sum(1 for g in gan_list if self.shishen(dg,g) in ["比肩","劫财"])
        deshi_desc = f"天干有{bj}个比劫帮身，{'有势' if bj>=1 else '孤立无援'}"
        
        score = (1 if deling else 0) + (1 if has_root else 0) + (1 if bj>=1 else 0)
        wangshuai = "身强" if score >= 2 else ("身弱" if score == 0 else "中和")
        
        return {
            "wangshuai": wangshuai,
            "score": score,
            "deling": {"text": "得令" if deling else "不得令", "desc": deling_desc, "value": deling},
            "dedi": {"text": "得地" if has_root else "不得地", "desc": dedi_desc, "value": has_root},
            "deshi": {"text": "得势" if bj>=1 else "不得势", "desc": deshi_desc, "value": bj>=1}
        }
    
    def check_chonghe(self, bazi):
        chonghe = []
        zhi_list = [bazi["year"][1], bazi["month"][1], bazi["day"][1], bazi["hour"][1]]
        zhi_names = ["年支","月支","日支","时支"]
        
        chong_pairs = [("子","午"),("丑","未"),("寅","申"),("卯","酉"),("辰","戌"),("巳","亥")]
        for i in range(4):
            for j in range(i+1, 4):
                if (zhi_list[i], zhi_list[j]) in chong_pairs or (zhi_list[j], zhi_list[i]) in chong_pairs:
                    chonghe.append({
                        "type": "冲",
                        "name": f"{zhi_list[i]}{zhi_list[j]}冲",
                        "position": f"{zhi_names[i]}与{zhi_names[j]}",
                        "effect": "动荡变动，主迁移、冲突、分离"
                    })
        
        for i in range(4):
            for j in range(i+1, 4):
                if zhi_list[i] == zhi_list[j]:
                    chonghe.append({
                        "type": "伏吟",
                        "name": f"{zhi_list[i]}伏吟",
                        "position": f"{zhi_names[i]}与{zhi_names[j]}",
                        "effect": "反复多磨，主旧事重演、情绪反复"
                    })
        
        if "寅" in zhi_list and "午" in zhi_list and "戌" in zhi_list:
            chonghe.append({"type":"合","name":"寅午戌三合火","position":"地支","effect":"火局成势，主热情、奔波、文书"})
        if "申" in zhi_list and "子" in zhi_list and "辰" in zhi_list:
            chonghe.append({"type":"合","name":"申子辰三合水","position":"地支","effect":"水局成势，主流动、智慧、财旺"})
        
        return chonghe
    
    def check_combos(self, bazi, shishen_map):
        combos = []
        gs = [v["gan"] for v in shishen_map.values()]
        zhi_ss = []
        for v in shishen_map.values():
            zhi_ss.extend(v["zhi"].values())
        
        bj_c = gs.count("比肩")+gs.count("劫财")
        cx_c = gs.count("正财")+gs.count("偏财")
        
        if bj_c>=2 and cx_c>=1:
            combos.append({
                "name":"比劫夺财",
                "level":"凶",
                "priority": 95,
                "desc":"比劫重重克财星，易因朋友、合伙、借贷破财",
                "detail": f"天干比劫{bj_c}个，财星{cx_c}个，比劫近克财星，财来财去难留存。",
                "advice":["不宜合伙创业","不宜为人担保","合同必须明算账","重大投资需独立决策"]
            })
        
        ss_c = gs.count("食神")+gs.count("伤官")
        if ss_c>=1 and cx_c>=1:
            combos.append({
                "name":"食神生财",
                "level":"吉",
                "priority": 90,
                "desc":"食神泄秀生财，头脑灵活善经营",
                "detail": "食神泄日主之秀气而生财，主聪明、口才好、有商业头脑，适合以技术、信息、渠道变现。",
                "advice":["宜跑动求财","适合做贸易/渠道/中介","宜轻资产运营","发挥口才与创意"]
            })
        
        if "七杀" in gs and ("食神" in zhi_ss or "伤官" in zhi_ss):
            combos.append({
                "name":"食神制杀",
                "level":"吉",
                "priority": 85,
                "desc":"七杀有制化为权，有魄力能承压",
                "detail": "七杀主压力、权威、小人，食神制之则化压力为动力，主能承压、善管理、有威严。",
                "advice":["宜开拓性工作","管理岗位有利","可从事公检法、军警、项目管理"]
            })
        
        if gs.count("偏财") >= 2:
            combos.append({
                "name":"偏财双透",
                "level":"中",
                "priority": 70,
                "desc":"财星双透，财源多但难聚",
                "detail": "偏财心性明显，善于捕捉机会、偏门财路多、花钱大方，但财透天干易被人觊觎。",
                "advice":["多开源但需节流","避免炫耀财富","理财宜分散配置"]
            })
        
        if "伤官" in gs and "正官" in gs:
            combos.append({
                "name":"伤官见官",
                "level":"凶",
                "priority": 100,
                "desc":"伤官克正官，与上级冲突，官非口舌",
                "detail": "正官代表规矩、领导、官职，伤官克之则主叛逆、不服管、易有口舌官非。",
                "advice":["不宜体制内","避免与直属领导硬刚","说话留三分"]
            })
        
        if ("正官" in gs or "七杀" in gs) and ("正印" in gs or "偏印" in gs):
            combos.append({
                "name":"官印相生",
                "level":"吉",
                "priority": 80,
                "desc":"官印相护，名利双收",
                "detail": "官生印、印生身，主有贵人提携、学历功名、名利双全。",
                "advice":["宜考学考证","宜公职/管理","重视人脉经营"]
            })
        
        return sorted(combos, key=lambda x: x["priority"], reverse=True)
    
    def get_advice(self, r):
        wangshuai = r["wangshuai_detail"]["wangshuai"]
        xiyong = r["xiyong"]
        combos = r["combos"]
        chonghe = r["chonghe"]
        day_gan = r["bazi"]["day"][0]
        
        advice = {"xingye": [], "caifu": [], "hunyin": [], "jiankang": []}
        
        has_shishengcai = any(c["name"]=="食神生财" for c in combos)
        has_bijieduocai = any(c["name"]=="比劫夺财" for c in combos)
        has_shishenzhisha = any(c["name"]=="食神制杀" for c in combos)
        
        if has_shishengcai:
            advice["xingye"].append("食神生财格，天生适合经商、贸易、渠道分销，能把资源变现")
            advice["xingye"].append("宜选择轻资产、高流动性的行业，如供应链、技术中介、信息服务")
        if has_shishenzhisha:
            advice["xingye"].append("食神制杀，有魄力承压，适合开拓型、管理型岗位")
        if has_bijieduocai:
            advice["xingye"].append("⚠️ 比劫夺财：不宜合伙创业，合作必须股权清晰、账目独立")
        
        advice["xingye"].append(f"喜用神为{'、'.join(xiyong)}，宜从事{'/'.join(xiyong)}属性行业")
        
        if has_bijieduocai:
            advice["caifu"].append("⚠️ 财来财去，易因朋友、合伙、担保破财，重大资金决策需独立")
            advice["caifu"].append("偏财透干，赚钱机会多，但比劫分夺，到手易散，需强制储蓄")
        else:
            advice["caifu"].append("财星有源，求财有道，宜主动开拓")
        
        if "金" in xiyong:
            advice["caifu"].append("金为财源，宜从事金融、五金、科技、汽车等金属性行业")
        if "水" in xiyong:
            advice["caifu"].append("水为流动之财，宜从事贸易、物流、跨境、旅游等流动性行业")
        if "木" in xiyong:
            advice["caifu"].append("木为疏土之神，宜从事文化、教育、农林、服装等木属性行业")
        
        day_zhi = r["bazi"]["day"][1]
        day_zhi_ss = r["shishen"]["day"]["zhi"]
        sp = list(day_zhi_ss.values())[0] if day_zhi_ss else "未知"
        advice["hunyin"].append(f"日支{day_zhi}，配偶宫坐{sp}，配偶多是有主见、有性格之人")
        
        if any(c["type"]=="冲" and "日支" in c["position"] for c in chonghe):
            advice["hunyin"].append("⚠️ 日支逢冲，婚姻易有波动，宜晚婚，婚后聚少离多反而有利")
        else:
            advice["hunyin"].append("配偶宫稳定，婚姻关系相对平和")
        
        if any(c["name"]=="偏财双透" for c in combos):
            advice["hunyin"].append("偏财双透，异性缘佳，但感情选择多，需专一")
        
        wx_stats = r["wuxing_stats"]
        max_wx = max(wx_stats, key=wx_stats.get)
        min_wx = min(wx_stats, key=wx_stats.get)
        
        advice["jiankang"].append(f"五行中{max_wx}最旺({wx_stats[max_wx]:.1f})，{min_wx}最弱({wx_stats[min_wx]:.1f})")
        
        if wx_stats["土"] > 4:
            advice["jiankang"].append("土旺，注意脾胃消化系统，忌过饱过腻")
        if wx_stats["火"] < 1.5:
            advice["jiankang"].append("火弱，注意心血管、血压、眼睛，避免熬夜")
        if wx_stats["木"] < 1:
            advice["jiankang"].append("木弱，注意肝胆、筋骨，适当运动舒展")
        if any(c["name"]=="寅申冲" for c in chonghe):
            advice["jiankang"].append("寅申冲，注意肝胆、筋骨、神经系统，防交通安全")
        
        return advice
    
    def analyze(self, bazi):
        dg = bazi["day"][0]
        shishen_map = {}
        for z,(g,zh) in bazi.items():
            shishen_map[z] = {"gan":self.shishen(dg,g), "zhi":{cg:self.shishen(dg,cg) for cg in self.zhi_cg[zh]}}
        
        nayin = {z:self.get_nayin(g,zh) for z,(g,zh) in bazi.items()}
        wuxing_stats = self.calc_wuxing_stats(bazi)
        wangshuai_detail = self.calc_wangshuai_detail(bazi, dg)
        
        mz = bazi["month"][1]
        bq = self.zhi_cg[mz][0]
        bq_ss = self.shishen(dg, bq)
        geju = self.rules.get("geju_rules", {}).get(bq_ss, {"name":"普通格","xi_yong":["调候"],"ji_shen":[],"desc":"格局平平"})
        
        combos = self.check_combos(bazi, shishen_map)
        chonghe = self.check_chonghe(bazi)
        xiyong = geju["xi_yong"] if "身强" in wangshuai_detail["wangshuai"] else (geju["xi_yong"] if "身弱" in wangshuai_detail["wangshuai"] else ["调候"])
        
        res = {
            "bazi": bazi, "nayin": nayin, "shishen": shishen_map,
            "wuxing_stats": wuxing_stats, "wangshuai_detail": wangshuai_detail,
            "geju": geju, "combos": combos, "chonghe": chonghe, "xiyong": xiyong
        }
        res["advice"] = self.get_advice(res)
        return res