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
        
        # 术语白话词典（专业术语 → 括号里的白话解释）
        self.terms = {
            # 十神
            "比肩": "比肩（同辈兄弟，代表竞争、合作、朋友）",
            "劫财": "劫财（争夺钱财，代表破财、竞争、小人）",
            "食神": "食神（才华输出，代表聪明、口才、创意、享受）",
            "伤官": "伤官（叛逆创新，代表才华、口才、不服管）",
            "偏财": "偏财（意外之财，代表投资、偏门、流动性收入）",
            "正财": "正财（稳定工资，代表固定收入、节俭、踏实）",
            "七杀": "七杀（压力权威，代表压力、挑战、小人、魄力）",
            "正官": "正官（规矩领导，代表官职、约束、名誉、责任）",
            "偏印": "偏印（偏门学问，代表灵感、孤独、技术）",
            "正印": "正印（正统学问，代表学历、贵人、母亲、房产）",
            # 旺衰
            "身强": "身强（自身能量足，能担财担官，不怕压力）",
            "身弱": "身弱（自身能量弱，需要帮扶，宜保守）",
            "中和": "中和（能量平衡，适应力强，但缺乏突出优势）",
            # 状态
            "得令": "得令（出生月份对你有利，底子好）",
            "不得令": "不得令（出生月份对你不利，底子薄）",
            "得地": "得地（地支有根气，有后台支撑）",
            "不得地": "不得地（地支无根气，缺乏根基）",
            "得势": "得势（天干有帮手，人缘好）",
            "不得势": "不得势（天干孤立，单打独斗）",
            # 组合
            "食神生财": "食神生财（用才华赚钱，适合做生意、做渠道）",
            "比劫夺财": "比劫夺财（朋友来分你的钱，合伙容易闹翻）",
            "食神制杀": "食神制杀（有压力但能扛住，越压越勇）",
            "伤官见官": "伤官见官（不服管，容易和领导吵架）",
            "官印相生": "官印相生（有贵人提携，学历功名有利）",
            "偏财双透": "偏财双透（赚钱机会多，但花钱也大手大脚）",
            # 冲合
            "寅申冲": "寅申冲（金木交战，奔波变动，注意交通安全）",
            "巳亥冲": "巳亥冲（水火相冲，思想冲突，情绪不稳定）",
            "子午冲": "子午冲（水火不容，情绪起伏大，事业感情波动）",
            "丑未冲": "丑未冲（土土相冲，内心纠结，容易自我矛盾）",
            "卯酉冲": "卯酉冲（金木相冲，感情不顺，易有桃花劫）",
            "辰戌冲": "辰戌冲（土库对冲，财库不稳，容易破财）",
            # 其他
            "调候": "调候（根据季节调节，夏天生人喜水降温，冬天生人喜火取暖）",
            "伏吟": "伏吟（同样的事情容易重复发生，旧事重演）",
            "三合": "三合（三个地支合成一种五行，能量集中）"
        }
        
        # 五行特征白话
        self.wuxing_traits = {
            "木旺": "性格直爽、有主见、向上心强，但容易固执",
            "火旺": "热情外向、表现力强、急躁冲动，容易得罪人",
            "土旺": "稳重诚信、包容心强、慢热保守，容易错失机会",
            "金旺": "理性果断、重规则、讲效率，容易冷漠无情",
            "水旺": "灵活变通、善沟通、适应力强，容易优柔寡断",
            "木弱": "缺乏主见、容易随波逐流、优柔寡断",
            "火弱": "缺乏热情、内向保守、行动力不足",
            "土弱": "缺乏诚信、根基不稳、容易焦虑",
            "金弱": "缺乏决断、容易犹豫、缺乏原则",
            "水弱": "缺乏变通、固执己见、沟通能力弱"
        }
    
    def get_term(self, term):
        """获取术语+白话"""
        return self.terms.get(term, term)
    
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
            deling_desc = f"出生在{mz}月({month_wx}旺)，{month_wx}能生你({dwx})，底子好、有底气"
        elif month_wx == dwx:
            deling_desc = f"出生在{mz}月({month_wx}旺)，和你({dwx})同属性，兄弟姐妹多、竞争大"
        else:
            deling_desc = f"出生在{mz}月({month_wx}旺)，{month_wx}克泄你({dwx})，底子薄、起步难"
        
        has_root = False
        root_zhi = []
        for z,(g,zh) in bazi.items():
            cgs = self.zhi_cg[zh]
            if any(self.gan_wx[cg]==dwx for cg in cgs):
                has_root = True
                root_zhi.append(zh)
        has_root = has_root or self.zhi_wx[dz] == dwx
        dedi_desc = f"地支{'、'.join(root_zhi)}里藏有你的根气，有后台、有退路" if root_zhi else "地支里没有你的根气，像浮萍一样缺乏根基"
        
        gan_list = [bazi["year"][0], bazi["month"][0], bazi["hour"][0]]
        bj = sum(1 for g in gan_list if self.shishen(dg,g) in ["比肩","劫财"])
        deshi_desc = f"天干有{bj}个同属性帮手，人缘不错、有人帮" if bj>=1 else "天干没有帮手，单打独斗、全靠自己"
        
        score = (1 if deling else 0) + (1 if has_root else 0) + (1 if bj>=1 else 0)
        wangshuai = "身强" if score >= 2 else ("身弱" if score == 0 else "中和")
        
        wangshuai_baihua = {
            "身强": "能量充足，能扛事、能担财，适合主动出击",
            "身弱": "能量偏弱，需要借力，适合保守稳健",
            "中和": "能量平衡，适应力强，但缺乏爆发力"
        }
        
        return {
            "wangshuai": wangshuai,
            "wangshuai_baihua": wangshuai_baihua[wangshuai],
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
        chong_baihua = {
            "子午冲": "水火不容，情绪起伏大，事业感情波动",
            "丑未冲": "土土相冲，内心纠结，容易自我矛盾",
            "寅申冲": "金木交战，奔波变动，注意交通安全",
            "卯酉冲": "金木相冲，感情不顺，易有桃花劫",
            "辰戌冲": "土库对冲，财库不稳，容易破财",
            "巳亥冲": "水火相冲，思想冲突，情绪不稳定"
        }
        
        for i in range(4):
            for j in range(i+1, 4):
                if (zhi_list[i], zhi_list[j]) in chong_pairs or (zhi_list[j], zhi_list[i]) in chong_pairs:
                    name = f"{zhi_list[i]}{zhi_list[j]}冲"
                    chonghe.append({
                        "type": "冲",
                        "name": name,
                        "position": f"{zhi_names[i]}与{zhi_names[j]}",
                        "effect": chong_baihua.get(name, "动荡变动，主迁移、冲突、分离")
                    })
        
        for i in range(4):
            for j in range(i+1, 4):
                if zhi_list[i] == zhi_list[j]:
                    chonghe.append({
                        "type": "伏吟",
                        "name": f"{zhi_list[i]}伏吟",
                        "position": f"{zhi_names[i]}与{zhi_names[j]}",
                        "effect": "反复多磨，同样的事情容易重复发生"
                    })
        
        if "寅" in zhi_list and "午" in zhi_list and "戌" in zhi_list:
            chonghe.append({"type":"合","name":"寅午戌三合火","position":"地支","effect":"火局成势，热情奔放，但容易急躁冲动"})
        if "申" in zhi_list and "子" in zhi_list and "辰" in zhi_list:
            chonghe.append({"type":"合","name":"申子辰三合水","position":"地支","effect":"水局成势，聪明灵活，但容易多变"})
        if "亥" in zhi_list and "卯" in zhi_list and "未" in zhi_list:
            chonghe.append({"type":"合","name":"亥卯未三合木","position":"地支","effect":"木局成势，仁慈向上，但容易固执"})
        if "巳" in zhi_list and "酉" in zhi_list and "丑" in zhi_list:
            chonghe.append({"type":"合","name":"巳酉丑三合金","position":"地支","effect":"金局成势，理性果断，但容易冷漠"})
        
        return chonghe
    
    def check_combos(self, bazi, shishen_map):
        combos = []
        gs = [v["gan"] for v in shishen_map.values()]
        zhi_ss = []
        for v in shishen_map.values():
            zhi_ss.extend(v["zhi"].values())
        
        bj_c = gs.count("比肩")+gs.count("劫财")
        cx_c = gs.count("正财")+gs.count("偏财")
        ss_c = gs.count("食神")+gs.count("伤官")
        sg_c = gs.count("正官")+gs.count("七杀")
        yx_c = gs.count("正印")+gs.count("偏印")
        
        # 1. 比劫夺财
        if bj_c>=2 and cx_c>=1:
            combos.append({
                "name":"比劫夺财",
                "level":"凶",
                "priority": 95,
                "baihua": "朋友来分你的钱，合伙容易闹翻",
                "desc":"比劫重重克财星，易因朋友、合伙、借贷破财",
                "detail": f"天干有{bj_c}个比劫（竞争对手），{cx_c}个财星，竞争对手离你太近，财来财去留不住。",
                "advice":[
                    "❌ 不要和朋友合伙创业（股权纠纷是最大雷区）",
                    "❌ 不要给人担保（别人还不上，你背债）",
                    "✅ 合作必须签合同、明算账（口头承诺不算数）",
                    "✅ 重大投资自己决定，不听朋友劝（朋友好心但不懂你的命）"
                ]
            })
        
        # 2. 食神生财
        if ss_c>=1 and cx_c>=1:
            combos.append({
                "name":"食神生财",
                "level":"吉",
                "priority": 90,
                "baihua": "靠才华和口才赚钱，脑子活络",
                "desc":"食神泄秀生财，头脑灵活善经营",
                "detail": "你有才华、口才好，能把想法变成钱，适合做销售、中介、创意类工作。",
                "advice":[
                    "✅ 做贸易、渠道、中介类工作（信息差就是钱）",
                    "✅ 轻资产运营，不要重投入（租办公室不如跑客户）",
                    "✅ 发挥口才和创意（演讲、培训、咨询都是财路）",
                    "❌ 不要死守死工资（你的财在流动中）"
                ]
            })
        
        # 3. 食神制杀
        if sg_c>=1 and (ss_c>=1 or "食神" in zhi_ss or "伤官" in zhi_ss):
            combos.append({
                "name":"食神制杀",
                "level":"吉",
                "priority": 85,
                "baihua": "有压力但能扛住，越压越勇",
                "desc":"七杀有制化为权，有魄力能承压",
                "detail": "你天生能抗压，别人觉得难的事你能搞定，适合做管理、带团队、做项目。",
                "advice":[
                    "✅ 做管理岗位、项目经理（你能镇住场子）",
                    "✅ 从事公检法、军警等高压职业（压力越大你越兴奋）",
                    "✅ 主动承担有挑战的任务（逃避压力等于浪费天赋）",
                    "❌ 不要逃避压力，越躲越弱（你的成长在压力中）"
                ]
            })
        
        # 4. 伤官见官
        if "伤官" in gs and "正官" in gs:
            combos.append({
                "name":"伤官见官",
                "level":"凶",
                "priority": 100,
                "baihua": "不服管，容易和领导吵架",
                "desc":"伤官克正官，与上级冲突，官非口舌",
                "detail": "你能力强但脾气倔，看不惯规矩，容易和领导顶撞，体制内很难混。",
                "advice":[
                    "❌ 不要考公务员、进国企（你会被规矩憋死）",
                    "❌ 避免和直属领导硬刚（赢了吵架，输了前途）",
                    "✅ 去私营企业、创业公司（相对自由）",
                    "✅ 自己做老板最合适（没人管你，你管别人）"
                ]
            })
        
        # 5. 官印相生
        if sg_c>=1 and yx_c>=1:
            combos.append({
                "name":"官印相生",
                "level":"吉",
                "priority": 80,
                "baihua": "有贵人提携，学历功名有利",
                "desc":"官印相护，名利双收",
                "detail": "领导赏识你，长辈愿意帮你，考学考证容易成功，适合走正统路线。",
                "advice":[
                    "✅ 考学历、考证书（证书是你的敲门砖）",
                    "✅ 进大公司、体制内（有人罩着你）",
                    "✅ 重视人脉和贵人关系（逢年过节走动走动）",
                    "✅ 多向长辈请教（他们的话要听）"
                ]
            })
        
        # 6. 偏财双透
        if gs.count("偏财") >= 2:
            combos.append({
                "name":"偏财双透",
                "level":"中",
                "priority": 70,
                "baihua": "赚钱机会多，但花钱也大手大脚",
                "desc":"财星双透，财源多但难聚",
                "detail": "你眼光敏锐，能发现赚钱机会，但财来财去，存不住钱，容易冲动消费。",
                "advice":[
                    "✅ 多开源，多渠道赚钱（不要把鸡蛋放一个篮子）",
                    "✅ 强制储蓄，工资到账先存30%（剩下的再花）",
                    "❌ 不要炫耀财富（财不露白，露白招小人）",
                    "❌ 避免高风险投机（偏财多的人容易赌性重）"
                ]
            })
        
        # 7. 印旺身弱
        if yx_c>=2 and bj_c==0:
            combos.append({
                "name":"印旺身弱",
                "level":"中",
                "priority": 65,
                "baihua": "想得多做得少，容易懒",
                "desc":"印星太旺，思想负担重，行动力不足",
                "detail": "你爱学习、爱思考，但容易想太多做太少，依赖心强，需要逼自己行动。",
                "advice":[
                    "✅ 设定 deadline，先做了再想（完美主义是敌人）",
                    "✅ 找执行力强的合伙人互补（你出脑子，他出腿）",
                    "❌ 不要一直学习不实践（知识不变现就是负债）",
                    "❌ 避免过度依赖长辈（独立才能成长）"
                ]
            })
        
        # 8. 财多身弱
        if cx_c>=2 and bj_c==0 and ss_c==0:
            combos.append({
                "name":"财多身弱",
                "level":"凶",
                "priority": 90,
                "baihua": "赚钱机会多但扛不住，有钱也累",
                "desc":"财星太旺，身弱不担财，财多反成负担",
                "detail": "你看到的赚钱机会很多，但身体或精力跟不上，有钱赚没命花，或者赚了也守不住。",
                "advice":[
                    "❌ 不要贪多，专注一个领域（少即是多）",
                    "✅ 先强身健体，精力是本钱（熬夜赚钱是亏本生意）",
                    "✅ 找合伙人分担（你出资源，他出力气）",
                    "❌ 避免借贷扩张（杠杆会压垮你）"
                ]
            })
        
        # 9. 伤官配印
        if "伤官" in gs and yx_c>=1:
            combos.append({
                "name":"伤官配印",
                "level":"吉",
                "priority": 75,
                "baihua": "才华横溢但有约束，能成大事",
                "desc":"伤官有印制，才华得用，名利双收",
                "detail": "你有才华但不太叛逆，印星约束了你的野性，让你能把才华用在正道上。",
                "advice":[
                    "✅ 从事创意+规范结合的行业（如设计师、建筑师）",
                    "✅ 考专业证书，用学历背书（让你的才华有敲门砖）",
                    "✅ 找有阅历的长辈做导师（他们能管住你）",
                    "❌ 不要完全放飞自我（自由需要边界）"
                ]
            })
        
        # 10. 杀印相生
        if "七杀" in gs and yx_c>=1:
            combos.append({
                "name":"杀印相生",
                "level":"吉",
                "priority": 82,
                "baihua": "压力变动力，贵人化险为夷",
                "desc":"七杀生印，印生身，化压力为贵人",
                "detail": "你遇到的压力和挑战，最终会变成你的贵人或学历，越难的事越能成就你。",
                "advice":[
                    "✅ 主动迎接挑战（难做的事才是护城河）",
                    "✅ 重视学历和证书（证书是化杀为权的工具）",
                    "✅ 找有权威的长辈做靠山（他们能化解你的压力）",
                    "❌ 不要逃避困难（逃一次，弱一次）"
                ]
            })
        
        # 11. 比劫抗官杀
        if bj_c >= 2 and sg_c >= 1 and ss_c == 0:
            combos.append({
                "name":"比劫抗官杀",
                "level":"中",
                "priority": 60,
                "baihua": "硬扛压力，靠毅力拼过去",
                "desc":"比劫抗官杀，靠硬拼取胜",
                "detail": "你不喜欢走捷径，遇到问题硬上，虽然能成但过程很苦，容易身心俱疲。",
                "advice":[
                    "✅ 培养团队，不要单打独斗（一个人扛不如一群人扛）",
                    "✅ 学会借力，不要硬扛（聪明人的力气用在刀刃上）",
                    "❌ 避免长期高压工作（身体是革命的本钱）",
                    "✅ 适当放松，劳逸结合（休息是为了更好地扛）"
                ]
            })
        
        # 12. 食神过多
        if ss_c >= 3:
            combos.append({
                "name":"食神过多",
                "level":"中",
                "priority": 55,
                "baihua": "太会享受，容易懒、容易胖",
                "desc":"食神太旺，贪图安逸，缺乏进取",
                "detail": "你聪明、会享受、口福好，但容易安于现状，缺乏拼劲，身材也容易发福。",
                "advice":[
                    "✅ 设定明确目标，逼自己跳出舒适区（安逸是慢性毒药）",
                    "✅ 控制饮食，多运动（食神旺的人容易胖）",
                    "❌ 不要沉迷享乐（享受要有限度）",
                    "✅ 找一个有冲劲的合伙人推着你走"
                ]
            })
        
        return sorted(combos, key=lambda x: x["priority"], reverse=True)
    
    def get_xiyong(self, wangshuai, day_wx, month_wx, combos):
        xiyong = []
        jishen = []
        
        if wangshuai == "身强":
            if day_wx == "火":
                xiyong = ["水", "金", "土"]
                jishen = ["木", "火"]
            elif day_wx == "土":
                xiyong = ["木", "水", "金"]
                jishen = ["火", "土"]
            elif day_wx == "金":
                xiyong = ["火", "木", "水"]
                jishen = ["土", "金"]
            elif day_wx == "水":
                xiyong = ["土", "火", "木"]
                jishen = ["金", "水"]
            elif day_wx == "木":
                xiyong = ["金", "土", "火"]
                jishen = ["水", "木"]
        elif wangshuai == "身弱":
            if day_wx == "火":
                xiyong = ["木", "火"]
                jishen = ["水", "金"]
            elif day_wx == "土":
                xiyong = ["火", "土"]
                jishen = ["木", "水"]
            elif day_wx == "金":
                xiyong = ["土", "金"]
                jishen = ["火", "木"]
            elif day_wx == "水":
                xiyong = ["金", "水"]
                jishen = ["土", "火"]
            elif day_wx == "木":
                xiyong = ["水", "木"]
                jishen = ["金", "土"]
        else:
            if month_wx in ["火", "土"]:
                xiyong = ["水", "金"]
                jishen = ["火"]
            elif month_wx in ["水", "金"]:
                xiyong = ["火", "木"]
                jishen = ["水"]
            else:
                xiyong = ["调候"]
                jishen = ["过旺五行"]
        
        return xiyong, jishen
    
    def get_advice(self, r):
        wangshuai = r["wangshuai_detail"]["wangshuai"]
        xiyong = r["xiyong"]
        jishen = r["jishen"]
        combos = r["combos"]
        chonghe = r["chonghe"]
        day_gan = r["bazi"]["day"][0]
        day_wx = self.gan_wx[day_gan]
        wx_stats = r["wuxing_stats"]
        xingye_map = self.rules.get("xingye_mapping", {})
        
        advice = {"xingye": [], "caifu": [], "hunyin": [], "jiankang": []}
        
        has_shishengcai = any(c["name"]=="食神生财" for c in combos)
        has_bijieduocai = any(c["name"]=="比劫夺财" for c in combos)
        has_shishenzhisha = any(c["name"]=="食神制杀" for c in combos)
        has_shangguanjianguan = any(c["name"]=="伤官见官" for c in combos)
        has_guanyinxiangsheng = any(c["name"]=="官印相生" for c in combos)
        has_caiduoshenruo = any(c["name"]=="财多身弱" for c in combos)
        has_shangguanpeiyin = any(c["name"]=="伤官配印" for c in combos)
        
        # === 事业建议 ===
        if has_shishengcai:
            advice["xingye"].append("✅ 你适合做生意、跑渠道、做中介，靠信息和资源差赚钱")
            advice["xingye"].append("✅ 轻资产运营，不要重投入，越灵活越赚钱")
        if has_shishenzhisha:
            advice["xingye"].append("✅ 你能扛压力，适合做管理、带团队、做项目")
            advice["xingye"].append("✅ 高压行业如公检法、军警、项目管理也适合你")
        if has_shangguanjianguan:
            advice["xingye"].append("❌ 你不服管，体制内、国企、大公司难混")
            advice["xingye"].append("✅ 去私营企业、创业公司，或者自己做老板")
        if has_guanyinxiangsheng:
            advice["xingye"].append("✅ 你有贵人缘，适合大公司、体制内，考学历考证有利")
        if has_shangguanpeiyin:
            advice["xingye"].append("✅ 你适合创意+规范结合的行业，如设计师、建筑师、策划")
        if has_bijieduocai:
            advice["xingye"].append("❌ 不要和朋友合伙创业，股权必须清晰")
        if has_caiduoshenruo:
            advice["xingye"].append("❌ 不要贪多，专注一个领域，先强身再赚钱")
        
        # 根据喜用神补充具体行业
        for wx in xiyong:
            if wx in xingye_map:
                industries = xingye_map[wx]["行业"]
                jobs = xingye_map[wx]["职业"]
                trait = xingye_map[wx]["特征"]
                advice["xingye"].append(f"✅ 【{wx}属性】{trait}，适合：{', '.join(industries[:5])}")
                advice["xingye"].append(f"   具体职业：{', '.join(jobs[:5])}")
        
        if not advice["xingye"]:
            advice["xingye"].append(f"✅ 你五行喜{'、'.join(xiyong)}，选择与这些属性相关的行业更有利")
            advice["xingye"].append("✅ 身强宜主动出击，身弱宜保守稳健，中和宜灵活应变")
        
        # === 财运建议 ===
        if has_bijieduocai:
            advice["caifu"].append("❌ 财来财去，朋友借钱、合伙投资、给人担保都是漏财口")
            advice["caifu"].append("✅ 工资到账先强制储蓄30%，剩下的再花")
            advice["caifu"].append("✅ 理财宜分散，不要把钱放在一个篮子里")
        elif has_caiduoshenruo:
            advice["caifu"].append("❌ 赚钱机会多但扛不住，专注一个领域，不要贪多")
            advice["caifu"].append("✅ 先强身健体，精力是本钱")
            advice["caifu"].append("✅ 找合伙人分担，你出资源他出力气")
        elif has_shishengcai:
            advice["caifu"].append("✅ 你有赚钱头脑，适合多渠道收入，不要死守死工资")
            advice["caifu"].append("✅ 信息差、资源差都是你的财路")
        else:
            advice["caifu"].append("✅ 财星有源，求财有道，宜主动开拓")
        
        # 方位建议
        fangwei = {"金":"西方/西北","木":"东方/东南","水":"北方","火":"南方","土":"中央/本地"}
        for wx in xiyong[:2]:
            if wx in fangwei:
                advice["caifu"].append(f"💰 {wx}为财，{fangwei[wx]}有利，多往这个方向走动")
        
        # 颜色建议
        yanse = {"金":"白色、金色、银色","木":"绿色、青色","水":"黑色、蓝色、灰色","火":"红色、紫色、橙色","土":"黄色、棕色、咖啡色"}
        for wx in xiyong[:2]:
            if wx in yanse:
                advice["caifu"].append(f"💰 多用{yanse[wx]}物品，有助于提升财运")
        
        # === 婚姻建议 ===
        day_zhi = r["bazi"]["day"][1]
        day_zhi_ss = r["shishen"]["day"]["zhi"]
        sp = list(day_zhi_ss.values())[0] if day_zhi_ss else "未知"
        sp_baihua = self.terms.get(sp, sp).split("（")[1].rstrip("）") if "（" in self.terms.get(sp, sp) else ""
        
        advice["hunyin"].append(f"💑 日支是{day_zhi}，配偶宫坐{sp}（{sp_baihua}），配偶多是这种性格的人")
        
        if any(c["type"]=="冲" and "日支" in c["position"] for c in chonghe):
            advice["hunyin"].append("❌ 日支逢冲，婚姻易有波动，宜晚婚，婚后适当保持距离反而有利")
        else:
            advice["hunyin"].append("✅ 配偶宫稳定，婚姻关系相对平和")
        
        if any(c["name"]=="偏财双透" for c in combos):
            advice["hunyin"].append("⚠️ 异性缘好，但感情选择多，需专一")
        
        if has_shangguanjianguan:
            advice["hunyin"].append("⚠️ 你对伴侣要求高，容易挑剔，学会包容")
        
        if has_bijieduocai:
            advice["hunyin"].append("⚠️ 比劫旺，感情中容易有竞争者，或配偶强势")
        
        # 配偶五行建议
        if wangshuai == "身强":
            advice["hunyin"].append(f"💑 你身强，配偶宜选{', '.join(jishen[:2])}属性的人，能互补")
        elif wangshuai == "身弱":
            advice["hunyin"].append(f"💑 你身弱，配偶宜选{', '.join(xiyong[:2])}属性的人，能帮扶")
        
        # === 健康建议 ===
        max_wx = max(wx_stats, key=wx_stats.get)
        min_wx = min(wx_stats, key=wx_stats.get)
        
        advice["jiankang"].append(f"🏥 五行中{max_wx}最旺({wx_stats[max_wx]:.1f})，{min_wx}最弱({wx_stats[min_wx]:.1f})")
        
        # 旺的五行
        if wx_stats["土"] > 4:
            advice["jiankang"].append("⚠️ 土太旺，注意脾胃、消化系统，忌暴饮暴食、油腻食物")
        if wx_stats["火"] > 4:
            advice["jiankang"].append("⚠️ 火太旺，注意心脏、血压、眼睛，避免熬夜、情绪激动")
        if wx_stats["水"] > 4:
            advice["jiankang"].append("⚠️ 水太旺，注意肾脏、泌尿系统，避免寒凉")
        if wx_stats["木"] > 4:
            advice["jiankang"].append("⚠️ 木太旺，注意肝胆、筋骨，避免过度劳累")
        if wx_stats["金"] > 4:
            advice["jiankang"].append("⚠️ 金太旺，注意肺、呼吸系统，避免干燥环境")
        
        # 弱的五行
        if wx_stats["火"] < 1.5:
            advice["jiankang"].append("⚠️ 火弱，注意心血管、血压、眼睛，多晒太阳补阳气")
        if wx_stats["水"] < 1.5:
            advice["jiankang"].append("⚠️ 水弱，注意肾脏、内分泌，多喝水")
        if wx_stats["木"] < 1:
            advice["jiankang"].append("⚠️ 木弱，注意肝胆、筋骨，适当运动舒展")
        if wx_stats["金"] < 1:
            advice["jiankang"].append("⚠️ 金弱，注意肺、呼吸系统，多吃白色食物")
        if wx_stats["土"] < 1:
            advice["jiankang"].append("⚠️ 土弱，注意脾胃、消化吸收，规律饮食")
        
        # 冲合影响
        for c in chonghe:
            if c["name"] == "寅申冲":
                advice["jiankang"].append("⚠️ 寅申冲，注意肝胆、筋骨、神经系统，防交通安全")
            elif c["name"] == "巳亥冲":
                advice["jiankang"].append("⚠️ 巳亥冲，注意心脑血管、情绪稳定，避免大起大落")
            elif c["name"] == "子午冲":
                advice["jiankang"].append("⚠️ 子午冲，注意心脏、血压、泌尿系统")
            elif c["name"] == "卯酉冲":
                advice["jiankang"].append("⚠️ 卯酉冲，注意肝胆、呼吸系统、情绪")
        
        return advice
    
    def analyze(self, bazi):
        dg = bazi["day"][0]
        dwx = self.gan_wx[dg]
        
        shishen_map = {}
        for z,(g,zh) in bazi.items():
            shishen_map[z] = {"gan":self.shishen(dg,g), "zhi":{cg:self.shishen(dg,cg) for cg in self.zhi_cg[zh]}}
        
        nayin = {z:self.get_nayin(g,zh) for z,(g,zh) in bazi.items()}
        wuxing_stats = self.calc_wuxing_stats(bazi)
        wangshuai_detail = self.calc_wangshuai_detail(bazi, dg)
        
        mz = bazi["month"][1]
        bq = self.zhi_cg[mz][0]
        bq_ss = self.shishen(dg, bq)
        
        geju_rules = self.rules.get("geju_rules", {})
        geju = geju_rules.get(bq_ss, {"name":"普通格","xi_yong":[],"ji_shen":[],"desc":"格局平平，需看组合定吉凶"})
        
        combos = self.check_combos(bazi, shishen_map)
        chonghe = self.check_chonghe(bazi)
        
        xiyong, jishen = self.get_xiyong(
            wangshuai_detail["wangshuai"], 
            dwx, 
            self.zhi_wx[mz],
            combos
        )
        
        if geju.get("xi_yong") and wangshuai_detail["wangshuai"] == "中和":
            xiyong = geju["xi_yong"]
        if geju.get("ji_shen"):
            jishen = geju["ji_shen"]
        
        res = {
            "bazi": bazi, "nayin": nayin, "shishen": shishen_map,
            "wuxing_stats": wuxing_stats, "wangshuai_detail": wangshuai_detail,
            "geju": geju, "combos": combos, "chonghe": chonghe,
            "xiyong": xiyong, "jishen": jishen, "terms": self.terms,
            "wuxing_traits": self.wuxing_traits
        }
        res["advice"] = self.get_advice(res)
        return res
