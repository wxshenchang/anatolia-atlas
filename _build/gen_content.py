#!/usr/bin/env python3
"""安纳托利亚历史地图集 —— 内容层：里程碑 / 古今地名 / 史料出处
生成 js/map_data.js（DYNASTY_DATA + CORRIDOR_DATA）、js/lore_core.js 追加数据、data/sources/*.json
所有史事与地名均取自下列公开学术文献（见 SOURCES），坐标为通行考古/地理定位。
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------- 史料出处
SOURCES = {
    "hittite": [
        "Bryce, Trevor. *The Kingdom of the Hittites*. 2nd ed. Oxford University Press, 2005.",
        "Bryce, Trevor. *The Routledge Handbook of the People and Places of Ancient Western Asia*. Routledge, 2009.",
        "Beckman, Gary. *Hittite Diplomatic Texts*. SBL, 1999（卡迭石和约文本）。",
        "《剑桥古代史》第 2 卷第 1、2 分册 (CAH II.1–II.2), Cambridge University Press, 1973.",
        "Kühne, Hartmut / Otten, Heinrich, in *Reallexikon der Assyriologie*, s.v. Ḫattuša.",
        "Klengel, Horst. *Geschichte des hethitischen Reiches*. Brill, 1999（德文）。",
    ],
    "post_hittite": [
        "Bryce, Trevor. *The World of the Neo-Hittite Kingdoms*. Oxford University Press, 2012.",
        "Zimansky, Paul. *Ecology and Empire: The Structure of the Urartian State*. Chicago, 1985.",
        "Sams, G. Kenneth. *The Early Phrygian Pottery* (Gordion Excavations), 1994.",
        "《剑桥古代史》第 3 卷第 1 分册 (CAH III.1), 1982.",
        "Bittel, Kurt. *Die Hethiter*. C. H. Beck, 1976（德文）。",
    ],
    "lydia": [
        "Herodotus. *Histories*, I.6–94（吕底亚与居鲁士）。",
        "Roosevelt, Christopher H. *The Archaeology of Lydia, from Gyges to Alexander*. Cambridge UP, 2009.",
        "Cahill, Nicholas (ed.). *The Lydians and Their World*. Yapı Kredi, 2010.",
        "《剑桥古代史》第 3 卷第 3 分册 (CAH III.3), 1982.",
        "Radner, Karen. *Ancient Assyria: A Very Short Introduction*. OUP, 2015.",
    ],
    "achaemenid": [
        "Herodotus. *Histories*, V–IX（爱奥尼亚起义与希波战争）。",
        "Briant, Pierre. *From Cyrus to Alexander: A History of the Persian Empire*. Eisenbrauns, 2002.",
        "Kuhrt, Amélie. *The Persian Empire: A Corpus of Sources from the Achaemenid Period*. Routledge, 2007.",
        "Dusinberre, Elspeth R. M. *Empire, Authority, and Autonomy in Achaemenid Anatolia*. Cambridge UP, 2013.",
        "《伊朗百科全书》(Encyclopaedia Iranica), s.v. “Anatolia”, “Satrapy”.",
    ],
    "diadochi": [
        "Arrian. *Anabasis of Alexander*, I–III（伊苏斯、高加米拉）。",
        "Diodorus Siculus. *Bibliotheca historica*, XVIII–XX（继业者战争）。",
        "Billows, Richard A. *Antigonos the One-Eyed and the Creation of the Hellenistic State*. UC Press, 1990.",
        "《剑桥古代史》第 7 卷第 1 分册 (CAH VII.1), 2nd ed. 1984.",
        "Plutarch. *Life of Eumenes*, *Life of Demetrius*.",
    ],
    "hellenistic": [
        "Hansen, Esther V. *The Attalids of Pergamon*. 2nd ed. Cornell UP, 1971.",
        "McGing, Brian C. *The Foreign Policy of Mithridates VI Eupator, King of Pontus*. Brill, 1986.",
        "Strabo. *Geographia*, XII–XIV（小亚细亚地理）。",
        "Ma, John. *Antiochos III and the Cities of Western Asia Minor*. Oxford UP, 1999.",
        "《剑桥古代史》第 8 卷 (CAH VIII), 2nd ed. 1989.",
    ],
    "roman_conquest": [
        "Appian. *Mithridatic Wars*; Plutarch. *Life of Pompey*, *Life of Sulla*.",
        "Magie, David. *Roman Rule in Asia Minor to the End of the Third Century*. Princeton UP, 1950.",
        "Cicero. *Epistulae ad Familiares*, XV（西里西亚总督任内书信）。",
        "Syme, Ronald. *The Roman Revolution*. Oxford UP, 1939.",
        "《剑桥古代史》第 9 卷 (CAH IX), 2nd ed. 1994.",
    ],
    "roman_empire": [
        "Magie, David. *Roman Rule in Asia Minor*. Princeton UP, 1950.",
        "Mitchell, Stephen. *Anatolia: Land, Men, and Gods in Asia Minor* (2 vols.). Oxford UP, 1993.",
        "Halfmann, Helmut. *Éphèse et Pergame: urbanisme et commanditaires*. De Boccard, 2004（法文）。",
        "《罗马帝国碑铭集成》(CIL) 第 III 卷小亚细亚铭文。",
        "Potter, David S. *The Roman Empire at Bay, AD 180–395*. Routledge, 2004.",
    ],
    "byzantine": [
        "Ostrogorsky, Georg. *Geschichte des byzantinischen Staates*. C. H. Beck, 1963（德文；英译 *History of the Byzantine State*）。",
        "Whittow, Mark. *The Making of Orthodox Byzantium, 600–1025*. Macmillan, 1996.",
        "Haldon, John. *Byzantium in the Seventh Century*. Cambridge UP, 1997（军区制）。",
        "Treadgold, Warren. *A History of the Byzantine State and Society*. Stanford UP, 1997.",
        "《牛津拜占庭研究手册》(The Oxford Handbook of Byzantine Studies), OUP, 2008.",
    ],
    "seljuk": [
        "Cahen, Claude. *Pre-Ottoman Turkey*. Sidgwick & Jackson, 1968.",
        "Peacock, A. C. S. *The Great Seljuk Empire*. Edinburgh UP, 2015.",
        "Hillenbrand, Carole. *Turkish Myth and Muslim Symbol: The Battle of Manzikert*. Edinburgh UP, 2007.",
        "Anna Komnene. *Alexiad*（曼努埃尔时期的拜占庭视角）。",
        "《伊斯兰百科全书》第 2 版 (EI²), s.v. “Rūm”, “Dānishmendids”, “Mengüjek”. ",
        "Korobeinikov, Dimitri. *Byzantium and the Turks in the Thirteenth Century*. Oxford UP, 2014.",
    ],
    "mongol": [
        "Jackson, Peter. *The Mongols and the Islamic World*. Yale UP, 2017.",
        "Melville, Charles. *The History of the Mongols* (Ilkhanate chapters).",
        "《伊斯兰百科全书》第 2 版 (EI²), s.v. “Īlkhānids”, “Ḳarāmān-oghullari”, “Germiyān-oghullari”. ",
        "Wittek, Paul. *The Rise of the Ottoman Empire*. Royal Asiatic Society, 1938.",
        "Kafadar, Cemal. *Between Two Worlds: The Construction of the Ottoman State*. UC Press, 1995.",
    ],
    "beylik": [
        "Zachariadou, Elizabeth A. *Trade and Crusade: Venetian Crete and the Emirates of Menteshe and Aydin*. Venice, 1983.",
        "Fleet, Kate. *European and Islamic Trade in the Early Ottoman State*. Cambridge UP, 1999.",
        "《伊斯兰百科全书》第 2 版 (EI²), s.v. “Orkhan”, “Murād I”, “Bāyazīd I”, “Timūr”. ",
        "İnalcık, Halil. *The Ottoman Empire: The Classical Age 1300–1600*. Weidenfeld, 1973.",
        "Doukas. *Historia Turco-Byzantina*（1453 年围城）。",
    ],
    "ottoman": [
        "İnalcık, Halil. *The Ottoman Empire: The Classical Age 1300–1600*. 1973.",
        "《剑桥土耳其史》第 2 卷 (The Cambridge History of Turkey, vol. 2: The Ottoman Empire as a World Power, 1453–1603), CUP, 2013.",
        "Faroqhi, Suraiya. *The Ottoman Empire and the World Around It*. I.B. Tauris, 2004.",
        "《伊斯兰百科全书》第 2 版 (EI²), s.v. “Süleymān I”, “Selīm I”, “Eyalet”. ",
        "Agoston, Gabor. *Guns for the Sultan*. Cambridge UP, 2005.",
    ],
    "ottoman_late": [
        "《剑桥土耳其史》第 4 卷 (The Cambridge History of Turkey, vol. 4: Turkey in the Modern World), CUP, 2008.",
        "Quataert, Donald. *The Ottoman Empire, 1700–1922*. 2nd ed. Cambridge UP, 2005.",
        "Zürcher, Erik J. *Turkey: A Modern History*. 4th ed. I.B. Tauris, 2017.",
        "Suny, Ronald Grigor. *“They Can Live in the Desert but Nowhere Else”: A History of the Armenian Genocide*. Princeton UP, 2015.",
        "土耳其宗教基金会《伊斯兰百科全书》(TDV İslâm Ansiklopedisi), s.v. “Tanzimat”, “Meşrutiyet”.",
        "Shaw, Stanford J. & Shaw, Ezel Kural. *History of the Ottoman Empire and Modern Turkey*, vol. 2. CUP, 1977.",
    ],
    "republic": [
        "Zürcher, Erik J. *Turkey: A Modern History*. 4th ed. I.B. Tauris, 2017.",
        "《剑桥土耳其史》第 4 卷 (CUP, 2008).",
        "Mango, Andrew. *Atatürk: The Biography of the Founder of Modern Turkey*. Overlook, 1999.",
        "Ahmad, Feroz. *The Making of Modern Turkey*. Routledge, 1993.",
        "土耳其统计局 (TÜİK) 人口与行政区划数据; 《伊斯兰百科全书》第 3 版 s.v. “Turkey”. ",
    ],
}

# ---------------------------------------------------------------- 里程碑 + 古今地名
# coord 为通行考古/城市定位（WGS84）

# ---------------------------------------------------------------- 事件详情（点开浮签后展开）
# 每个事件：背景 → 经过 → 影响；附一手/代表性出处。外文史料中文名按通行译名。
MILESTONE_DETAIL = {
 "hittite:-1650": [
  "哈图西里一世（约前 1650—前 1620 在位）把都城从库沙拉迁到哈图沙（今博阿兹卡莱），统一安纳托利亚中部。赫梯由此从若干城邦联盟变成中央集权的王国，并继承阿卡德-亚述式书吏传统，留下印欧语系最早的大宗文献档案。",
  "Bryce《赫梯王国》"
 ],
 "hittite:-1595": [
  "穆尔西里一世沿幼发拉底河南下，攻陷巴比伦、推翻古巴比伦第一王朝（汉谟拉比之后的末代）。因远征过远、后方空虚，他回国后即被刺杀，赫梯进入「黑暗期」，巴比伦则被加喜特人占据。",
  "《赫梯诏令》与巴比伦编年史"
 ],
 "hittite:-1274": [
  "埃及法老拉美西斯二世北征叙利亚，与赫梯国王穆瓦塔里二世在奥龙特斯河畔的卡迭石相遇。双方都宣称获胜：埃及的战报刻在神庙墙上，赫梯的版本存于泥板。此役是古代规模最大的战车会战之一（双方各约 2 万—3 万人）。",
  "埃及《卡迭石铭文》/ 赫梯泥板"
 ],
 "hittite:-1259": [
  "十六年后，哈图西里三世与拉美西斯二世以「兄弟」相称缔结和约，划定势力范围并规定引渡逃犯。原本刻在银板上（已佚），埃及卡尔纳克与赫梯档案各存一份；今联合国总部陈列其复制件，被称为「最早的和平条约」。",
  "埃及与赫梯双语文本"
 ],
 "hittite:-1180": [
  "东地中海在数十年间同时崩溃：海上民族袭掠沿海、迈锡尼与乌加里特毁城、埃及退回尼罗河。赫梯首都哈图沙被焚，中央政权消失，书写传统中断，安纳托利亚进入约四百年的「黑暗时代」。",
  "《剑桥古代史》卷 II.2"
 ],
 "post_hittite:-1180": [
  "赫梯中央政权消失后，安纳托利亚不再有单一强权：东南部由卢维人的「新赫梯」城邦（卡赫美什、马尔丁）延续赫梯文化，中西部为弗里吉亚人，东部高原为乌拉尔图与亚美尼亚部落。这段空白期主要靠考古地层而非文献复原。",
  "Bryce《新赫梯诸王国》"
 ],
 "post_hittite:-900": [
  "乌拉尔图（亚述语称 Urartu，《圣经》中的亚拉腊）在凡湖以东兴起，以图什帕（今凡城）为都，凭山地水利与冶金立国。它与亚述争夺东部商路与铁矿，留下了大量楔形文字岩刻与运河遗迹。",
  "Zimansky《古代乌拉尔图》"
 ],
 "post_hittite:-800": [
  "希腊传统把戈尔迪乌姆的国王称为「迈达斯」（Midas），与德尔斐神谕和「点石成金」传说相关。考古在戈尔迪乌姆发现大型木构陵墓与希腊进口陶器，说明弗里吉亚与爱琴海世界贸易密切。",
  "戈尔迪乌姆发掘报告"
 ],
 "post_hittite:-717": [
  "亚述国王萨尔贡二世攻陷卡赫美什，终结最后一个重要的新赫梯城邦。亚述把东南安纳托利亚划为行省，赫梯-卢维的书吏与艺术传统随之被亚述吸收。萨爾贡二世随后建都杜尔-沙鲁金（今霍尔萨巴德）。",
  "《剑桥古代史》卷 III.1"
 ],
 "post_hittite:-696": [
  "辛梅里安人自高加索南下，攻破戈尔迪乌姆，弗里吉亚王国崩溃。希腊史料记迈达斯王饮牛血自尽。此后吕底亚接替弗里吉亚成为西部霸主，辛梅里安人又被吕底亚逐出。",
  "希罗多德《历史》i.15"
 ],
 "lydia:-680": [
  "古革斯（Gyges）刺杀坎道列斯夺取王位，建立梅尔姆纳德王朝，都萨第斯。他派使者赴亚述求援对抗辛梅里安人，是安纳托利亚西部君主首次与两河强权直接交涉；其名字见于亚述泥板（Gugu）。",
  "希罗多德 i.8—14 / 亚述泥板"
 ],
 "lydia:-630": [
  "辛梅里安人破萨第斯，古革斯战死，其子阿尔迪斯继位。吕底亚一度向亚述称臣求援，最终在前 6 世纪初把辛梅里安人逐出安纳托利亚。这场战乱让萨第斯在考古地层中留下明显的破坏层。",
  "希罗多德 i.15—16"
 ],
 "lydia:-610": [
  "吕底亚铸造西方最早的标准钱币：天然金银合金（electrum）的「斯塔特」，一面有狮子头印记。以弗所阿耳忒弥斯神庙遗址出土的早期钱币窖藏是直接证据。货币化推动了爱琴海贸易与国家财政。",
  "以弗所钱币窖藏 / 大英博物馆藏品"
 ],
 "lydia:-585": [
  "吕底亚与米底争夺东部，哈里斯河（今克孜勒河）畔会战时恰逢日全食（天文学可精确推算为前 585 年 5 月 28 日），双方视为天谴而罢兵，以河为界。这是史上第一次有确切日期的战役，也标定希罗多德的年代学。",
  "希罗多德 i.74"
 ],
 "lydia:-547": [
  "居鲁士二世围攻萨第斯十四天后破城，吕底亚国王克里苏斯（《圣经》中的 Croesus）被俘。吕底亚的金库与铸币技术为波斯所用，安纳托利亚西部自此成为阿契美尼德的行省（萨尔迪斯行省）。",
  "希罗多德 i.76—84"
 ],
 "achaemenid:-547": [
  "居鲁士二世灭吕底亚后，把安纳托利亚西部编为萨尔迪斯行省，保留吕底亚的行政与铸币体系，并在萨第斯派驻总督。波斯由此获得爱琴海东岸的希腊城邦与丰厚税源。",
  "希罗多德 i.153—160"
 ],
 "achaemenid:-499": [
  "米利都僭主阿里斯塔哥拉斯鼓动爱奥尼亚希腊城邦反抗波斯，并赴希腊本土求援。雅典派 20 艘船、埃雷特里亚派 5 艘，义军一度焚毁萨第斯。这次「烧城」成为波斯大王薛西斯远征希腊的口实。",
  "希罗多德 v.28—v.103"
 ],
 "achaemenid:-494": [
  "波斯舰队在米利都以西的拉德岛海战击溃爱奥尼亚联合舰队，随后屠米利都、迁其民。雅典上演普律尼科斯悲剧《米利都的陷落》时观众痛哭，被罚千德拉克马——这是希波战争情绪的直接证据。",
  "希罗多德 vi.18—21"
 ],
 "achaemenid:-480": [
  "薛西斯一世以浮桥渡赫勒斯滂，号称百万大军远征希腊。温泉关、萨拉米斯海战后波斯海军受挫，次年普拉蒂亚陆战再败。安纳托利亚的希腊城邦短暂获得自主。",
  "希罗多德 vii—ix"
 ],
 "achaemenid:-386": [
  "斯巴达与波斯签订《安塔尔基达斯和约》（大王和约）：小亚细亚希腊城邦重归波斯，换取波斯的金钱支持。这是希腊城邦体系首次以「大王」意志划界，也埋下了马其顿东进的伏笔。",
  "色诺芬《希腊史》v.1.31"
 ],
 "diadochi:-334": [
  "亚历山大率马其顿军渡赫勒斯滂，在格拉尼库斯河与波斯诸总督的联军首战。他亲自率骑兵冲锋，几乎被砍死；此役后小亚细亚西部门户洞开，诸城次第归附。",
  "阿里安《远征记》i.13—16 / 普鲁塔克"
 ],
 "diadochi:-333": [
  "伊苏斯之战，亚历山大以右翼骑兵突入波斯中军，大流士三世弃车而逃，其母、妻、女被俘。亚历山大以礼待之，宣称自己是「大流士的继承者」而非毁灭者。",
  "阿里安 ii.6—13"
 ],
 "diadochi:-331": [
  "高加米拉（今伊拉克北部）决战，亚历山大以斜线阵诱使波斯战线出现缺口，直插大流士中军。大流士再度逃离，随后被部将杀死，阿契美尼德帝国灭亡，亚历山大成为「亚洲之王」。",
  "阿里安 iii.8—15"
 ],
 "diadochi:-323": [
  "亚历山大在巴比伦病逝（或中毒），年仅 32，未指定继承人。部将随即「巴比伦分封」，安纳托利亚被划给多个将领，由此开始四十年继业者战争。",
  "阿里安 vii.24—28 / 狄奥多罗斯"
 ],
 "diadochi:-301": [
  "伊普苏斯之战，安提柯一世与其子德米特里对阵塞琉古、利西马科斯与卡山德联军。安提柯战死，其领地被瓜分；安纳托利亚由此分为利西马科斯（西部）、塞琉古（东部）与本土王朝三块。",
  "普鲁塔克《德米特里传》/ 狄奥多罗斯 xx"
 ],
 "hellenistic:-281": [
  "库鲁佩迪安之战，塞琉古一世击败并杀死利西马科斯，短暂统一小亚细亚；他随即被托勒密·克劳努斯刺杀。塞琉古王朝由此稳固叙利亚与小亚细亚，帕加马、本都、比提尼亚趁机自立。",
  "阿庇安《叙利亚史》"
 ],
 "hellenistic:-261": [
  "帕加马的腓莱泰罗斯原为利西马科斯的守库人，前 281 年后自立；其侄欧迈尼斯一世在库鲁佩迪安战后正式建立阿塔罗斯王朝，定都帕加马。帕加马凭银矿、羊皮纸与阿塔罗斯柱廊成为东部文化中心。",
  "Strabo xiii / 帕加马铭文"
 ],
 "hellenistic:-230": [
  "加拉太人（凯尔特三支：特罗克米、托里斯托波基、托利斯托波吉）入侵安纳托利亚中部。阿塔罗斯一世在卡伊科斯河源两度击败他们，取得「救主」（Soter）称号并立碑纪念；加拉太人此后定居高原，成为各王国的雇佣兵来源。",
  "李维《罗马史》xxxviii / 帕加马纪念碑"
 ],
 "hellenistic:-188": [
  "《阿帕米亚和约》结束罗马-塞琉古战争：安条克三世割让托罗斯山以北全部领地并赔款。帕加马与本都分得除奇里乞亚外的西部；罗马首次以「仲裁者」身份决定小亚细亚版图。",
  "波利比乌斯 xxi / 李维 xxxviii"
 ],
 "hellenistic:-133": [
  "帕加马末代国王阿塔罗斯三世在遗嘱中把王国赠予罗马，罗马以其地设「亚细亚行省」（Asia），是全罗马最富的省份之一。此后罗马以行省+附庸王国的双层结构管理安纳托利亚。",
  "斯特拉波 xiv / 罗马史学家"
 ],
 "roman_empire:114": [
  "图拉真东征安息，攻陷泰西封，短暂设立亚美尼亚与美索不达米亚两行省，帝国东部抵达波斯湾。这是罗马版图的最大范围，但图拉真死后即被放弃。",
  "狄奥·卡西乌斯 lxviii"
 ],
 "roman_empire:117": [
  "哈德良继位后放弃图拉真的东方新省，退回幼发拉底河一线，以「守成为主」。他巡视东方、重建安条克与以弗所的公共建筑，东方行省进入长期和平与城市化高峰。",
  "《奥古斯都史》哈德良传"
 ],
 "roman_empire:260": [
  "萨珊皇帝沙普尔一世在埃德萨之战中俘获罗马皇帝瓦勒良（Valerian），这是罗马史上罕见的一次皇帝被俘。萨珊铭文（纳克什-鲁斯塔姆）把此事列为三大功业之一，罗马东方防线长期动摇。",
  "《奥古斯都史》/ 沙普尔铭文"
 ],
 "roman_empire:325": [
  "君士坦丁召集第一次尼西亚公会议，确立《尼西亚信经》并谴责阿里乌派。安纳托利亚教会由此形成以君士坦丁堡、以弗所、尼西亚为中心的格局，此后数百年教义争论都围绕这片土地展开。",
  "优西比乌《君士坦丁传》/ 会议文献"
 ],
 "roman_empire:330": [
  "君士坦丁把首都从罗马迁到博斯普鲁斯海峡西岸的拜占庭，改名君士坦丁堡。帝国重心东移，安纳托利亚从「东部行省」变成帝国的腹地，城市、道路与军防体系随之重塑。",
  "佐西莫斯《新史》/ 编年史"
 ],
 "byzantine:330": [
  "君士坦丁堡建都后，安纳托利亚成为帝国的主要兵源与粮仓。君士坦丁堡的人口、元老院与教会使之成为「新罗马」，西部则逐渐在蛮族迁徙中脱离。",
  "Ostrogorsky《拜占庭国家史》"
 ],
 "byzantine:636": [
  "雅尔穆克战役，拜占庭东方军被阿拉伯穆斯林军击溃，希拉克略皇帝退出叙利亚。此后安纳托利亚成为拜占庭与哈里发之间的边境地带，托罗斯山沿线形成要塞化的「边境区」。",
  "Theophanes《编年史》/ 早期伊斯兰史料"
 ],
 "byzantine:717": [
  "阿拉伯哈里发苏莱曼的军队自陆海两面围攻君士坦丁堡一年余，因希腊火、饥荒与保加尔的袭扰而失败。此役使拜占庭得以存续，也终结了倭马亚王朝的北进。",
  "Theophanes / 阿拉伯史料"
 ],
 "byzantine:963": [
  "尼基弗鲁斯二世（拜占庭将领，曾收复克里特与塞浦路斯）登基后大举东征，967—969 年收复奇里乞亚、塞浦路斯与安条克。安纳托利亚东部从边境变成帝国腹地，马其顿王朝进入中兴。",
  "Leo the Deacon《历史》"
 ],
 "byzantine:1071": [
  "曼齐刻尔特之战，塞尔柱苏丹阿尔普·阿尔斯兰击败并俘虏拜占庭皇帝罗曼努斯四世。拜占庭随即爆发内战，突厥部落大规模进入安纳托利亚腹地，帝国从此失去对高原的控制。",
  "Attaleiates《历史》/ Cahen"
 ],
 "seljuk:1071": [
  "曼齐刻尔特之后，塞尔柱宗王苏莱曼·伊本·库塔尔米什在安纳托利亚建罗姆苏丹国（「罗姆」即罗马之地），先后定都尼西亚、科尼亚。突厥化与伊斯兰化从此在高原加速。",
  "Cahen《前奥斯曼土耳其》"
 ],
 "seljuk:1077": [
  "苏莱曼·伊本·库塔尔米什是塞尔柱宗室，曼齐刻尔特之后在安纳托利亚西部自立，先以尼西亚为都，前推至科尼亚。\n「罗姆」意即罗马之地，宣称继承拜占庭在东方的统治；1097 年尼西亚被十字军夺走后，苏丹国重心南移科尼亚。",
  "Cahen《前奥斯曼土耳其》"
 ],
 "seljuk:1097": [
  "第一次十字军应拜占庭皇帝阿莱克修斯之请东征：攻下尼西亚交还拜占庭，多里莱乌姆之战击溃罗姆苏丹基利杰阿尔斯兰一世。十字军随后建立安条克公国与埃德萨伯国。",
  "Anna Komnene《阿莱克修斯传》"
 ],
 "seljuk:1176": [
  "拜占庭皇帝曼努埃尔一世亲征罗姆苏丹国，在密列奥塞法隆山口的隘路遭基利杰阿尔斯兰二世伏击而惨败。这是他最后一次试图清除突厥人的努力，拜占庭此后转守。",
  "Kinnamos / Choniates"
 ],
 "seljuk:1243": [
  "蒙古将领拜住（Baiju）在克塞山之战击溃罗姆苏丹凯霍斯鲁二世，罗姆苏丹国成为蒙古（伊儿汗国）的藩属。安纳托利亚进入蒙古宗主权+突厥贝伊国的双轨时代，塞尔柱财富被征税抽走。",
  "《剑桥土耳其史》卷 i"
 ],
 "mongol:1243": [
  "克塞山之战后，罗姆苏丹国的外交、军事与征税权均受伊儿汗监督，苏丹由蒙古册立。1260/1277 年马穆鲁克反攻与蒙古内乱使安纳托利亚成为代理战场。",
  "Peacock《大塞尔柱帝国》"
 ],
 "mongol:1277": [
  "马穆鲁克苏丹拜巴尔斯在埃尔比斯坦击败蒙古军，短暂介入安纳托利亚；此后蒙古加重税赋与行政直辖，土库曼贝伊与游牧部众向西北边境迁移，奥斯曼等贝伊国由此成形。",
  "拜巴尔斯传 / 伊儿汗史料"
 ],
 "mongol:1299": [
  "奥斯曼一世（Osman Gazi）在瑟于特（Söğüt）一带建立自己的贝伊国，处拜占庭与蒙古势力的夹缝。此后数十年它以联姻、雇佣与吸收流亡为手段向比提尼亚扩张。",
  "奥斯曼早期编年史"
 ],
 "mongol:1300": [
  "安纳托利亚进入「诸贝伊国」并立时期：卡拉曼、格尔米扬、艾登、门泰塞、萨鲁汗、卡雷西、奥斯曼等在蒙古宗主权下各自为政，也共享突厥-拜占庭边境的掠夺经济。",
  "Zachariadou 关于贝伊国的研究"
 ],
 "beylik:1326": [
  "奥斯曼之子奥尔汗夺下比提尼亚的布尔萨，定为都城，并铸币、立行会、建清真寺。这是奥斯曼从边陲公国转为「国家」的关键一步。",
  "奥斯曼编年史 / 早期铭文"
 ],
 "beylik:1361": [
  "穆拉德一世夺取阿德里安堡（埃迪尔内）并迁都于此，把扩张方向转向巴尔干。安纳托利亚诸贝伊国由此被纳入奥斯曼的册封体系，色雷斯成为帝国的新核心。",
  "奥斯曼编年史"
 ],
 "beylik:1389": [
  "科索沃之战，穆拉德一世死于战场但奥斯曼军获胜，塞尔维亚诸侯称臣。此役确立了奥斯曼在巴尔干的支配地位，也让统治重心长期不在安纳托利亚。",
  "奥斯曼/塞尔维亚史料"
 ],
 "beylik:1402": [
  "帖木儿在安卡拉之战击败并俘虏巴耶济德一世，此前被吞并的贝伊国复立。奥斯曼进入 1402—1413 年的「空位期」（大空位），直到穆罕默德一世重新统一。",
  "奥斯曼编年史 / 帖木儿史料"
 ],
 "beylik:1453": [
  "穆罕默德二世以巨炮与运河绕行、陆路运船入金角湾，经 53 天围攻攻陷君士坦丁堡。拜占庭帝国灭亡，奥斯曼成为跨欧亚的帝国，圣索菲亚改为清真寺。",
  "Kritovoulos / 奥斯曼史料"
 ],
 "ottoman:1453": [
  "攻陷君士坦丁堡后，穆罕默德二世自称「恺撒」，恢复东正教牧首制以统御基督徒，并把安纳托利亚的旧贝伊国整编为行省（eyalet）与桑贾克。伊斯坦布尔成为欧亚商业枢纽。",
  "《剑桥土耳其史》"
 ],
 "ottoman:1514": [
  "查尔迪兰之战，塞利姆一世以火炮与火枪击败萨法维沙阿伊斯玛仪，控制东西商路与库尔德斯坦。此役确立了逊尼派奥斯曼对什叶派萨法维的东部均势。",
  "奥斯曼编年史 / 萨法维史料"
 ],
 "ottoman:1517": [
  "塞利姆一世南下击败马穆鲁克，取叙利亚、埃及与希贾兹，并取得麦加谢里夫的效忠与「哈里发」名分。帝国由此获得伊斯兰圣地的监护权与红海贸易。",
  "奥斯曼编年史"
 ],
 "ottoman:1529": [
  "苏莱曼一世首次围攻维也纳未克，但已把匈牙利中部纳入附庸。中欧由此形成奥斯曼与哈布斯堡长达两百年的对峙线，安纳托利亚成为帝国兵源与粮仓。",
  "《剑桥土耳其史》"
 ],
 "ottoman:1571": [
  "勒班陀海战，神圣同盟舰队击溃奥斯曼海军，但帝国在一年内重建舰队。此役象征地中海霸权转向，奥斯曼转向印度洋与北非战略。",
  "奥斯曼/威尼斯史料"
 ],
 "ottoman_late:1699": [
  "《卡尔洛维茨条约》结束大土耳其战争，奥斯曼首次大规模割地：匈牙利、特兰西瓦尼亚、亚速与部分摩里亚让出。帝国转入守势，安纳托利亚成为核心区与税基。",
  "《剑桥土耳其史》"
 ],
 "ottoman_late:1839": [
  "《花厅御诏》宣布保障全体臣民的生命财产、废除包税、建立常备军与近代行政。坦志麦特改革开启，安纳托利亚的行省制（vilayet）与土地制度随之重组。",
  "Zürcher《现代土耳其史》"
 ],
 "ottoman_late:1876": [
  "《米德哈特宪法》颁布，确立两院制议会与臣民权利，是伊斯兰世界第一部成文宪法。但苏丹阿卜杜勒哈米德二世在 1878 年即中止其效力。",
  "Zürcher / 宪法文本"
 ],
 "ottoman_late:1915": [
  "加里波利（恰纳卡莱）之战，奥斯曼军在穆斯塔法·凯末尔指挥下击退英法协约国登陆，粉碎了打通海峡的战略。此役使凯末尔成为民族英雄，也推迟了帝国解体。",
  "《一战中的奥斯曼帝国》"
 ],
 "ottoman_late:1920": [
  "《色佛尔条约》把安纳托利亚瓜分为希腊、意大利、法国势力范围与库尔德、亚美尼亚区。凯末尔领导的安卡拉政府在民族战争中逆转局势，最终以 1923 年《洛桑条约》取代之。",
  "Zürcher / 条约文本"
 ],
 "republic:1923": [
  "1923 年 10 月 29 日，大国民议会宣布成立土耳其共和国，凯末尔当选首任总统，定都安卡拉。洛桑条约确认了土耳其的现代疆界，苏丹制与哈里发制先后被废除。",
  "Zürcher"
 ],
 "republic:1928": [
  "土耳其以拉丁字母取代阿拉伯-波斯字母，配套推行国民教育与「语言改革」。此举大幅提高识字率，也造成与伊斯兰书写传统的断裂。",
  "Zürcher / 改革文献"
 ],
 "republic:1934": [
  "妇女获得选举权与被选举权（早于法国、意大利等国），同时颁布姓氏法、废除旧称号。改革以国家主义、世俗化为纲，安纳托利亚社会结构剧烈变动。",
  "Zürcher"
 ],
 "republic:1939": [
  "哈塔伊（亚历山德勒塔）经公投并入土耳其，是共和国唯一一次领土扩张。该地区 1936 年后由法国托管叙利亚，二战后叙利亚长期不承认此举。",
  "Zürcher / 国际联盟档案"
 ],
 "republic:1952": [
  "土耳其加入北约，成为西方在黑海与中东之间的战略支点。朝鲜战争出兵换取成员资格，此后接受马歇尔计划援助并与美国建立军事同盟。",
  "Zürcher"
 ],
 "republic:1980": [
  "1980 年 9 月 12 日军方第三次政变，解散议会与政党，随后制定 1982 年宪法（至今仍部分有效）。政变带来长期的政治稳定，也强化了军方与中央集权。",
  "Zürcher"
 ]
}

CONTENT = [
    dict(key="dawn",
         milestones=[
             dict(year=-3200, headline="乌鲁克的楔形文字与城市革命", site="乌鲁克", coord=[45.64, 31.32],
                  detail="乌鲁克（瓦尔卡）在捷姆迭特那色时期扩张为近 100 公顷的城市，出现塔庙（Eanna 与 Anu 区）、圆柱印章、"
                         "记账泥板与最早的数字符号；文字从经济会计中产生，是世界上最早的书写系统。",
                  source="《剑桥古代史》卷 1（Uruk 期）/ 乌鲁克-瓦尔卡发掘报告（德国考古研究所）"),
             dict(year=-2600, headline="乌尔王陵与早期王权", site="乌尔", coord=[46.10, 30.96],
                  detail="伍莱（Leonard Woolley）1920—30 年代在乌尔发掘的王陵（约前 2600—前 2500）出土金器、青金石、"
                         "镶饰军旗与人殉墓室，显示早期城邦的王权与远程贸易网络已相当发达。",
                  source="Woolley《Ur Excavations》卷 2（Royal Cemetery）"),
             dict(year=-2334, headline="萨尔贡建立阿卡德帝国", site="阿卡德", coord=[44.30, 33.10],
                  detail="萨尔贡（Šarru-kīn）以阿卡德城为中心击败乌鲁克与乌玛诸邦，建立跨族群的帝国，"
                         "以阿卡德语取代苏美尔语为行政语言，并留下「天下四方之王」的头衔；阿卡德城位置至今未确认。",
                  source="《剑桥古代史》卷 1 / 阿卡德时期铭文（Sargon 传说与 Naram-Sin 铭文）"),
             dict(year=-2112, headline="乌尔第三王朝与乌尔纳姆法典", site="乌尔", coord=[46.10, 30.96],
                  detail="乌尔纳姆驱逐古提人、统一南部两河，颁布现存最早的成文法典（乌尔纳姆法典，早于汉谟拉比约三百年）；"
                         "王朝以「阿卡德与苏美尔之王」自居，留下数十万件行政与经济泥板。",
                  source="《剑桥古代史》卷 1 / 乌尔纳姆法典泥板（伊斯坦布尔、宾大藏）"),
             dict(year=-1894, headline="巴比伦第一王朝崛起", site="巴比伦", coord=[44.42, 32.54],
                  detail="阿摩利人苏穆阿布姆（Sumu-abum）在巴比伦建城立朝，此时巴比伦只是伊辛、拉尔萨、埃什努那之间的"
                         "小邦；此后一个半世纪逐步扩张，成为两河南部的中心。",
                  source="《剑桥古代史》卷 1 / 巴比伦王名表（Babylonian King List A）"),
             dict(year=-1750, headline="汉谟拉比法典刻石", site="巴比伦", coord=[44.42, 32.54],
                  detail="汉谟拉比击败拉尔萨与马里统一两河，把判例法刻在 2.25 米高的闪长岩石碑上（1901 年于苏萨发现，今卢浮宫），"
                         "顶部为汉谟拉比受权于太阳神沙马什的浮雕；马尔杜克由此升为全国主神。",
                  source="汉谟拉比法典石碑（Louvre Sb 8）/《剑桥古代史》卷 1"),
             dict(year=-1650, headline="赫梯登上安纳托利亚舞台", site="哈图沙", coord=[34.62, 40.02],
                  detail="哈图西里一世定都哈图沙，赫梯王国成形；此后一个半世纪内赫梯南下叙利亚、并前 1595 年劫掠巴比伦，"
                         "从安纳托利亚的区域势力变为近东强权。",
                  source="Bryce《赫梯王国》/ 哈图沙档案（Boğazköy 泥板）"),
         ],
         settlements=[
             dict(ancient="乌鲁克", modern="瓦尔卡（伊拉克）", coord=[45.64, 31.32], isCapital=True, remark="前 4 千年最大的城市，楔形文字发源地"),
             dict(ancient="乌尔", modern="乌尔遗址（伊拉克）", coord=[46.10, 30.96], remark="南纳神庙与乌尔王陵"),
             dict(ancient="尼普尔", modern="努法尔（伊拉克）", coord=[45.23, 32.13], remark="恩利尔神庙，两河宗教中心"),
             dict(ancient="巴比伦", modern="巴比伦遗址（伊拉克）", coord=[44.42, 32.54], remark="前 18 世纪起为巴比伦尼亚核心"),
             dict(ancient="孟菲斯", modern="孟菲斯遗址（埃及）", coord=[31.25, 29.85], remark="埃及早王朝首都"),
             dict(ancient="比布鲁斯", modern="朱拜勒（黎巴嫩）", coord=[35.65, 34.12], remark="腓尼基最古老的港口，木材转口"),
             dict(ancient="埃布拉", modern="特尔马尔迪赫（叙利亚）", coord=[36.80, 35.80], remark="前 3 千年的叙利亚商队王国"),
             dict(ancient="哈图沙", modern="博阿兹卡莱", coord=[34.62, 40.02], remark="前 17 世纪成为赫梯都城"),
         ]),
    dict(key="hittite",
         milestones=[
             dict(year=-1650, headline="哈图西里一世定都哈图沙，赫梯王国成形", site="哈图沙", coord=[34.62, 40.02]),
             dict(year=-1595, headline="穆尔西里一世远征巴比伦，古巴比伦灭亡", site="巴比伦", coord=[44.42, 32.54]),
             dict(year=-1274, headline="卡迭石之战：穆瓦塔里二世与拉美西斯二世对峙", site="卡迭石", coord=[36.52, 34.56]),
             dict(year=-1259, headline="《卡迭石和约》：已知最早的国际和平条约", site="哈图沙", coord=[34.62, 40.02]),
             dict(year=-1180, headline="青铜时代崩溃，赫梯帝国解体", site="哈图沙", coord=[34.62, 40.02]),
         ],
         settlements=[
             dict(ancient="哈图沙", modern="博阿兹卡莱", coord=[34.62, 40.02], isCapital=True, remark="赫梯都城，世界遗产"),
             dict(ancient="巴比伦", modern="巴比伦遗址（伊拉克）", coord=[44.42, 32.54], remark="古巴比伦都城，前 1595 年被赫梯攻陷"),
             dict(ancient="沙皮努瓦", modern="舒沙特（Çorum）", coord=[34.95, 40.55], isCapital=False, remark="赫梯宗教中心"),
             dict(ancient="内萨", modern="屈尔泰佩", coord=[35.48, 38.73], isCapital=False, remark="早期赫梯/亚述商馆"),
             dict(ancient="卡尼什", modern="屈尔泰佩", coord=[35.48, 38.73], isCapital=False),
             dict(ancient="阿尔扎瓦", modern="以弗所一带", coord=[27.34, 37.94], isCapital=False, remark="赫梯文献中的西部同盟"),
             dict(ancient="米拉", modern="米拉斯", coord=[27.78, 37.31], isCapital=False),
             dict(ancient="塔尔胡恩塔萨", modern="卡拉曼马拉什", coord=[36.93, 37.58], isCapital=False),
             dict(ancient="阿勒颇", modern="阿勒颇", coord=[37.16, 36.20], isCapital=False, remark="赫梯与埃及争夺的北叙利亚枢纽"),
         ]),
    dict(key="post_hittite",
         milestones=[
             dict(year=-1180, headline="帝国崩溃，安纳托利亚进入多中心时代", site="哈图沙", coord=[34.62, 40.02]),
             dict(year=-900, headline="乌拉尔图以图什帕（凡城）为都，与亚述争雄", site="图什帕", coord=[43.38, 38.49]),
             dict(year=-800, headline="弗里吉亚戈尔迪乌姆的迈达斯王，与希腊德尔斐神谕相关", site="戈尔迪乌姆", coord=[31.98, 39.65]),
             dict(year=-717, headline="亚述萨尔贡二世灭卡赫美什，新赫梯诸邦终", site="卡赫美什", coord=[38.02, 36.83]),
             dict(year=-696, headline="辛梅里安人攻灭弗里吉亚", site="戈尔迪乌姆", coord=[31.98, 39.65]),
         ],
         settlements=[
             dict(ancient="戈尔迪乌姆", modern="波拉特勒", coord=[31.98, 39.65], isCapital=True, remark="弗里吉亚都城"),
             dict(ancient="图什帕", modern="凡城", coord=[43.38, 38.49], isCapital=True, remark="乌拉尔图都城"),
             dict(ancient="卡赫美什", modern="杰拉布卢斯", coord=[38.02, 36.83], isCapital=False),
             dict(ancient="马尔丁", modern="马尔丁", coord=[40.74, 37.31], isCapital=False),
             dict(ancient="米利都", modern="巴拉特", coord=[27.28, 37.53], isCapital=False, remark="爱奥尼亚希腊城邦"),
             dict(ancient="士麦那", modern="伊兹密尔", coord=[27.14, 38.42], isCapital=False),
             dict(ancient="锡诺普", modern="锡诺普", coord=[35.15, 42.03], isCapital=False, remark="黑海希腊殖民城"),
         ]),
    dict(key="lydia",
         milestones=[
             dict(year=-680, headline="古革斯建立吕底亚梅尔姆纳德王朝", site="萨第斯", coord=[28.04, 38.48]),
             dict(year=-630, headline="辛梅里安人攻掠萨第斯，古革斯战死", site="萨第斯", coord=[28.04, 38.48]),
             dict(year=-610, headline="小亚细亚最早的钱币（琥珀金）在吕底亚流通", site="萨第斯", coord=[28.04, 38.48]),
             dict(year=-585, headline="哈里斯河之战后与米底划界（日食之年）", site="克孜勒河", coord=[35.0, 39.2]),
             dict(year=-547, headline="居鲁士二世攻陷萨第斯，吕底亚亡", site="萨第斯", coord=[28.04, 38.48]),
         ],
         settlements=[
             dict(ancient="萨第斯", modern="萨尔特", coord=[28.04, 38.48], isCapital=True, remark="吕底亚都城，铸币起源地"),
             dict(ancient="以弗所", modern="塞尔丘克", coord=[27.34, 37.94], isCapital=False, remark="阿尔忒弥斯神庙"),
             dict(ancient="米利都", modern="巴拉特", coord=[27.28, 37.53], isCapital=False, remark="泰勒斯与自然哲学"),
             dict(ancient="普里耶涅", modern="普里耶涅", coord=[27.30, 37.66], isCapital=False),
             dict(ancient="桑索斯", modern="克尼克", coord=[29.31, 36.36], isCapital=False, remark="吕基亚都城"),
             dict(ancient="戈尔德翁", modern="波拉特勒", coord=[31.98, 39.65], isCapital=False),
             dict(ancient="埃克巴坦那", modern="哈马丹", coord=[48.52, 34.80], isCapital=False, remark="米底都城"),
         ]),
    dict(key="achaemenid",
         milestones=[
             dict(year=-547, headline="居鲁士二世灭吕底亚，安纳托利亚并入波斯", site="萨第斯", coord=[28.04, 38.48]),
             dict(year=-499, headline="爱奥尼亚起义：米利都求援雅典", site="米利都", coord=[27.28, 37.53]),
             dict(year=-494, headline="拉德海战，米利都被毁", site="米利都", coord=[27.28, 37.53]),
             dict(year=-480, headline="薛西斯一世渡赫勒斯滂远征希腊", site="达达尼尔", coord=[26.4, 40.2]),
             dict(year=-386, headline="《大王和约》：西部希腊城邦复归波斯", site="苏萨", coord=[48.26, 32.19]),
         ],
         settlements=[
             dict(ancient="萨尔迪斯行省治所", modern="萨尔特", coord=[28.04, 38.48], isCapital=True, remark="波斯小亚细亚行政中心"),
             dict(ancient="达斯基雷翁", modern="埃尔吉耶斯一带", coord=[30.16, 39.30], isCapital=False, remark="弗里吉亚行省治所"),
             dict(ancient="波斯波利斯", modern="设拉子附近", coord=[52.89, 29.94], isCapital=False, remark="帝国礼仪都城"),
             dict(ancient="苏萨", modern="舒什", coord=[48.26, 32.19], isCapital=False, remark="帝国行政都城"),
             dict(ancient="哈利卡纳苏斯", modern="博德鲁姆", coord=[27.42, 37.04], isCapital=False, remark="摩索拉斯陵墓"),
             dict(ancient="帕加马", modern="贝尔加马", coord=[27.18, 39.12], isCapital=False),
             dict(ancient="特拉佩祖斯", modern="特拉布宗", coord=[39.72, 41.00], isCapital=False, remark="黑海希腊殖民城"),
         ]),
    dict(key="diadochi",
         milestones=[
             dict(year=-334, headline="亚历山大渡赫勒斯滂，格拉尼库斯之战", site="格拉尼库斯河", coord=[27.25, 40.13]),
             dict(year=-333, headline="伊苏斯之战：亚历山大击溃大流士三世", site="伊苏斯", coord=[36.20, 36.85]),
             dict(year=-331, headline="高加米拉之战，波斯帝国灭亡", site="高加米拉", coord=[43.55, 36.55]),
             dict(year=-323, headline="亚历山大卒于巴比伦，继业者战争爆发", site="巴比伦", coord=[44.42, 32.54]),
             dict(year=-301, headline="伊普苏斯之战：安纳托利亚三分", site="伊普苏斯", coord=[31.15, 38.85]),
         ],
         settlements=[
             dict(ancient="亚历山大里亚·特洛阿斯", modern="达尔扬", coord=[26.16, 39.55], isCapital=False),
             dict(ancient="安条克", modern="安塔基亚", coord=[36.16, 36.20], isCapital=False, remark="塞琉古西部都城（前 300 建）"),
             dict(ancient="塞琉西亚", modern="巴格达附近", coord=[44.52, 33.10], isCapital=False, remark="底格里斯河畔塞琉古都城"),
             dict(ancient="吕西马基亚", modern="盖利博卢半岛", coord=[26.70, 40.55], isCapital=True, remark="利西马科斯都城"),
             dict(ancient="帕加马", modern="贝尔加马", coord=[27.18, 39.12], isCapital=False),
             dict(ancient="尼西亚", modern="伊兹尼克", coord=[29.72, 40.43], isCapital=False),
             dict(ancient="阿马西亚", modern="阿马西亚", coord=[35.83, 40.65], isCapital=False, remark="本都王国旧都"),
         ]),
    dict(key="hellenistic",
         milestones=[
             dict(year=-281, headline="库鲁佩迪安之战，利西马科斯阵亡", site="库鲁佩迪安", coord=[27.05, 38.55]),
             dict(year=-261, headline="帕加马独立，阿塔罗斯王朝建立", site="帕加马", coord=[27.18, 39.12]),
             dict(year=-230, headline="阿塔罗斯一世击败加拉太人，取“救主”称号", site="帕加马", coord=[27.18, 39.12]),
             dict(year=-188, headline="《阿帕米亚和约》：塞琉古退出托罗斯山以北", site="阿帕米亚", coord=[30.16, 38.07]),
             dict(year=-133, headline="阿塔罗斯三世遗赠帕加马予罗马，亚细亚行省设立", site="帕加马", coord=[27.18, 39.12]),
         ],
         settlements=[
             dict(ancient="帕加马", modern="贝尔加马", coord=[27.18, 39.12], isCapital=True, remark="阿塔罗斯王朝都城，大祭坛与图书馆"),
             dict(ancient="锡诺普", modern="锡诺普", coord=[35.15, 42.03], isCapital=True, remark="本都王国都城"),
             dict(ancient="尼科米底亚", modern="伊兹米特", coord=[29.92, 40.77], isCapital=True, remark="比提尼亚王国都城"),
             dict(ancient="马扎卡", modern="开塞利", coord=[35.49, 38.73], isCapital=True, remark="卡帕多细亚王国都城"),
             dict(ancient="安卡拉（安基拉）", modern="安卡拉", coord=[32.86, 39.93], isCapital=False, remark="加拉太部族中心"),
             dict(ancient="阿芙洛狄西亚斯", modern="格伊拉", coord=[28.72, 37.71], isCapital=False),
             dict(ancient="米特里达提翁", modern="克尔克基莱西", coord=[33.68, 39.85], isCapital=False),
             dict(ancient="萨莫萨塔", modern="阿德亚曼", coord=[38.28, 37.76], isCapital=False, remark="科马基尼王国都城"),
         ]),
    dict(key="roman_conquest",
         milestones=[
             dict(year=-133, headline="亚细亚行省设立，以弗所为首府", site="以弗所", coord=[27.34, 37.94]),
             dict(year=-88, headline="本都米特里达梯六世发动“亚洲晚祷”，屠杀罗马人", site="以弗所", coord=[27.34, 37.94]),
             dict(year=-63, headline="庞培灭本都王国、废塞琉古，重组东方", site="阿马西亚", coord=[35.83, 40.65]),
             dict(year=-48, headline="法萨卢斯之战：凯撒击败庞培", site="法萨卢斯", coord=[22.38, 39.30]),
             dict(year=-27, headline="奥古斯都确立元首制，东方行省稳定", site="罗马", coord=[12.48, 41.89]),
         ],
         settlements=[
             dict(ancient="以弗所", modern="塞尔丘克", coord=[27.34, 37.94], isCapital=True, remark="亚细亚行省首府"),
             dict(ancient="尼科米底亚", modern="伊兹米特", coord=[29.92, 40.77], isCapital=True, remark="比提尼亚-本都行省首府"),
             dict(ancient="塔尔苏斯", modern="塔尔苏斯", coord=[34.90, 36.92], isCapital=False, remark="奇里乞亚都会，保罗出生地"),
             dict(ancient="安条克", modern="安塔基亚", coord=[36.16, 36.20], isCapital=False, remark="叙利亚行省首府"),
             dict(ancient="萨第斯", modern="萨尔特", coord=[28.04, 38.48], isCapital=False),
             dict(ancient="特拉勒斯", modern="艾登", coord=[27.84, 37.85], isCapital=False),
             dict(ancient="萨莫萨塔", modern="阿德亚曼", coord=[38.28, 37.76], isCapital=False, remark="科马基尼附庸王"),
         ]),
    dict(key="roman_empire",
         milestones=[
             dict(year=114, headline="图拉真设亚美尼亚、美索不达米亚行省", site="泰西封", coord=[44.58, 33.09]),
             dict(year=117, headline="哈德良放弃东方新省，退回幼发拉底河", site="安条克", coord=[36.16, 36.20]),
             dict(year=260, headline="埃德萨之战：萨珊沙普尔一世俘获瓦勒良", site="埃德萨", coord=[38.79, 37.15]),
             dict(year=325, headline="尼西亚公会议：基督教大公会议首次召开", site="尼西亚", coord=[29.72, 40.43]),
             dict(year=330, headline="君士坦丁迁都君士坦丁堡", site="君士坦丁堡", coord=[28.98, 41.01]),
         ],
         settlements=[
             dict(ancient="以弗所", modern="塞尔丘克", coord=[27.34, 37.94], isCapital=False, remark="亚细亚都会，塞尔苏斯图书馆"),
             dict(ancient="帕加马", modern="贝尔加马", coord=[27.18, 39.12], isCapital=False, remark="阿斯克勒庇俄斯圣所"),
             dict(ancient="拜占庭", modern="伊斯坦布尔", coord=[28.98, 41.01], isCapital=False, remark="330 年成为新都"),
             dict(ancient="尼西亚", modern="伊兹尼克", coord=[29.72, 40.43], isCapital=False),
             dict(ancient="凯撒利亚（马扎卡）", modern="开塞利", coord=[35.49, 38.73], isCapital=False),
             dict(ancient="安基拉", modern="安卡拉", coord=[32.86, 39.93], isCapital=False, remark="奥古斯都神庙铭文"),
             dict(ancient="梅利泰内", modern="马拉蒂亚", coord=[38.31, 38.35], isCapital=False, remark="东部军区重镇"),
         ]),
    dict(key="byzantine",
         milestones=[
             dict(year=330, headline="君士坦丁堡建都，东罗马时代开始", site="君士坦丁堡", coord=[28.98, 41.01]),
             dict(year=636, headline="雅尔穆克战役后阿拉伯人夺取叙利亚", site="雅尔穆克", coord=[35.85, 32.80]),
             dict(year=717, headline="阿拉伯人围攻君士坦丁堡失败", site="君士坦丁堡", coord=[28.98, 41.01]),
             dict(year=963, headline="尼基弗鲁斯二世收复奇里乞亚与安条克", site="安条克", coord=[36.16, 36.20]),
             dict(year=1071, headline="曼齐刻尔特之战：拜占庭丢失安纳托利亚门户", site="曼齐刻尔特", coord=[42.53, 39.15]),
         ],
         settlements=[
             dict(ancient="君士坦丁堡", modern="伊斯坦布尔", coord=[28.98, 41.01], isCapital=True),
             dict(ancient="阿莫里翁", modern="阿菲永附近", coord=[30.60, 38.85], isCapital=False, remark="安纳托利亚军区重镇"),
             dict(ancient="安基拉", modern="安卡拉", coord=[32.86, 39.93], isCapital=False),
             dict(ancient="塞琉西亚", modern="锡利夫凯", coord=[33.93, 36.38], isCapital=False),
             dict(ancient="阿尼", modern="阿尼（卡尔斯）", coord=[43.57, 40.51], isCapital=False, remark="亚美尼亚巴格拉图尼王朝都城"),
             dict(ancient="特拉布宗", modern="特拉布宗", coord=[39.72, 41.00], isCapital=False),
             dict(ancient="阿塔利亚", modern="安塔利亚", coord=[30.70, 36.89], isCapital=False),
         ]),
    dict(key="seljuk",
         milestones=[
             dict(year=1071, headline="曼齐刻尔特之战，突厥人进入安纳托利亚", site="曼齐刻尔特", coord=[42.53, 39.15]),
             dict(year=1077, headline="苏莱曼·伊本·库塔尔米什立罗姆苏丹国", site="尼西亚", coord=[29.72, 40.43]),
             dict(year=1097, headline="第一次十字军收复尼西亚，多里莱乌姆之战", site="多里莱乌姆", coord=[30.52, 39.62]),
             dict(year=1176, headline="密列奥塞法隆之战：曼努埃尔一世败于基利杰阿尔斯兰二世", site="密列奥塞法隆", coord=[31.35, 38.15]),
             dict(year=1243, headline="克塞山之战：苏丹国臣属蒙古", site="克塞山", coord=[38.60, 40.05]),
         ],
         settlements=[
             dict(ancient="科尼亚（伊科尼翁）", modern="科尼亚", coord=[32.49, 37.87], isCapital=True, remark="罗姆苏丹国都城，鲁米陵墓"),
             dict(ancient="锡瓦斯", modern="锡瓦斯", coord=[37.02, 39.75], isCapital=False, remark="达尼什曼德王朝都城"),
             dict(ancient="尼西亚", modern="伊兹尼克", coord=[29.72, 40.43], isCapital=False, remark="1097—1261 尼西亚帝国都城"),
             dict(ancient="特拉布宗", modern="特拉布宗", coord=[39.72, 41.00], isCapital=False, remark="1204 年特拉布宗帝国建立"),
             dict(ancient="开塞利", modern="开塞利", coord=[35.49, 38.73], isCapital=False),
             dict(ancient="阿拉尼亚", modern="阿拉尼亚", coord=[32.00, 36.54], isCapital=False, remark="基利杰阿尔斯兰二世夏宫"),
             dict(ancient="狄夫里吉", modern="迪夫里伊", coord=[38.11, 39.37], isCapital=False, remark="1228 年大清真寺与医院，世界遗产"),
         ]),
    dict(key="mongol",
         milestones=[
             dict(year=1243, headline="克塞山之战后罗姆苏丹国成为伊儿汗国藩属", site="克塞山", coord=[38.60, 40.05]),
             dict(year=1277, headline="马穆鲁克苏丹拜巴尔斯介入安纳托利亚", site="埃尔比斯坦", coord=[37.20, 38.20]),
             dict(year=1299, headline="奥斯曼一世在瑟于特建立贝伊国", site="瑟于特", coord=[30.18, 40.02]),
             dict(year=1300, headline="安纳托利亚诸贝伊国并立", site="卡拉曼", coord=[33.22, 37.18]),
         ],
         settlements=[
             dict(ancient="科尼亚", modern="科尼亚", coord=[32.49, 37.87], isCapital=False, remark="苏丹国旧都，蒙古宗主权下"),
             dict(ancient="卡拉曼", modern="卡拉曼", coord=[33.22, 37.18], isCapital=False, remark="卡拉曼贝伊国都城"),
             dict(ancient="瑟于特", modern="瑟于特", coord=[30.18, 40.02], isCapital=False, remark="奥斯曼贝伊国发源地"),
             dict(ancient="屈塔希亚", modern="屈塔希亚", coord=[29.98, 39.42], isCapital=False, remark="格尔米扬贝伊国都城"),
             dict(ancient="比尔吉", modern="比尔吉", coord=[27.28, 38.31], isCapital=False, remark="艾登贝伊国都城"),
             dict(ancient="大不里士", modern="大不里士", coord=[46.29, 38.07], isCapital=False, remark="伊儿汗国都城"),
             dict(ancient="锡瓦斯", modern="锡瓦斯", coord=[37.02, 39.75], isCapital=False),
         ]),
    dict(key="beylik",
         milestones=[
             dict(year=1326, headline="奥斯曼夺取布尔萨，定为都城", site="布尔萨", coord=[29.06, 40.19]),
             dict(year=1361, headline="穆拉德一世取阿德里安堡（埃迪尔内）", site="埃迪尔内", coord=[26.56, 41.68]),
             dict(year=1389, headline="科索沃之战，奥斯曼控制巴尔干", site="科索沃", coord=[21.07, 42.72]),
             dict(year=1402, headline="安卡拉之战：帖木儿击败巴耶济德一世，帝国进入空位期", site="安卡拉", coord=[33.03, 40.24]),
             dict(year=1453, headline="穆罕默德二世攻陷君士坦丁堡", site="君士坦丁堡", coord=[28.98, 41.01]),
         ],
         settlements=[
             dict(ancient="布尔萨", modern="布尔萨", coord=[29.06, 40.19], isCapital=True, remark="奥斯曼首个正式都城"),
             dict(ancient="埃迪尔内", modern="埃迪尔内", coord=[26.56, 41.68], isCapital=True, remark="1369 年后欧洲侧都城"),
             dict(ancient="君士坦丁堡", modern="伊斯坦布尔", coord=[28.98, 41.01], isCapital=True, remark="1453 年后帝国都城"),
             dict(ancient="卡拉曼", modern="卡拉曼", coord=[33.22, 37.18], isCapital=False),
             dict(ancient="锡瓦斯", modern="锡瓦斯", coord=[37.02, 39.75], isCapital=False, remark="卡迪·布尔汉丁国都城"),
             dict(ancient="迪亚巴克尔", modern="迪亚巴克尔", coord=[40.23, 37.91], isCapital=False, remark="白羊王朝都城"),
             dict(ancient="安卡拉", modern="安卡拉", coord=[32.86, 39.93], isCapital=False, remark="1402 年帖木儿战场"),
         ]),
    dict(key="ottoman",
         milestones=[
             dict(year=1453, headline="攻陷君士坦丁堡，拜占庭帝国终结", site="伊斯坦布尔", coord=[28.98, 41.01]),
             dict(year=1514, headline="查尔迪兰之战：塞利姆一世击败萨法维", site="查尔迪兰", coord=[44.09, 39.19]),
             dict(year=1517, headline="灭马穆鲁克，取叙利亚与埃及", site="开罗", coord=[31.24, 30.04]),
             dict(year=1529, headline="苏莱曼一世首次围攻维也纳", site="维也纳", coord=[16.37, 48.21]),
             dict(year=1571, headline="勒班陀海战：奥斯曼舰队受挫", site="勒班陀", coord=[21.42, 38.42]),
         ],
         settlements=[
             dict(ancient="伊斯坦布尔", modern="伊斯坦布尔", coord=[28.98, 41.01], isCapital=True),
             dict(ancient="埃迪尔内", modern="埃迪尔内", coord=[26.56, 41.68], isCapital=False, remark="夏都与巴尔干门户"),
             dict(ancient="布尔萨", modern="布尔萨", coord=[29.06, 40.19], isCapital=False),
             dict(ancient="阿勒颇", modern="阿勒颇", coord=[37.16, 36.20], isCapital=False, remark="帝国第三大城"),
             dict(ancient="大马士革", modern="大马士革", coord=[36.29, 33.51], isCapital=False),
             dict(ancient="开罗", modern="开罗", coord=[31.24, 30.04], isCapital=False, remark="埃及行省首府"),
             dict(ancient="特拉布宗", modern="特拉布宗", coord=[39.72, 41.00], isCapital=False, remark="1461 年并入奥斯曼"),
         ]),
    dict(key="ottoman_late",
         milestones=[
             dict(year=1699, headline="《卡尔洛维茨条约》：奥斯曼首次大规模割地", site="卡尔洛维茨", coord=[19.93, 45.20]),
             dict(year=1839, headline="《花厅御诏》开启坦志麦特改革", site="伊斯坦布尔", coord=[28.98, 41.01]),
             dict(year=1876, headline="《米德哈特宪法》颁布，首次立宪", site="伊斯坦布尔", coord=[28.98, 41.01]),
             dict(year=1915, headline="加里波利之战：奥斯曼击退协约国登陆", site="加里波利", coord=[26.30, 40.24]),
             dict(year=1920, headline="《色佛尔条约》签署，被 1923 年《洛桑条约》取代", site="塞夫勒", coord=[2.22, 48.80]),
         ],
         settlements=[
             dict(ancient="伊斯坦布尔", modern="伊斯坦布尔", coord=[28.98, 41.01], isCapital=True),
             dict(ancient="伊兹密尔", modern="伊兹密尔", coord=[27.14, 38.42], isCapital=False, remark="爱琴海贸易口岸"),
             dict(ancient="阿达纳", modern="阿达纳", coord=[35.32, 37.00], isCapital=False),
             dict(ancient="萨洛尼卡", modern="塞萨洛尼基", coord=[22.94, 40.64], isCapital=False, remark="凯末尔出生地"),
             dict(ancient="的黎波里", modern="的黎波里（黎巴嫩）", coord=[35.84, 34.44], isCapital=False),
             dict(ancient="巴格达", modern="巴格达", coord=[44.40, 33.31], isCapital=False, remark="1917 年被英军占领"),
             dict(ancient="耶路撒冷", modern="耶路撒冷", coord=[35.21, 31.77], isCapital=False),
         ]),
    dict(key="republic",
         milestones=[
             dict(year=1923, headline="10 月 29 日土耳其共和国成立，定都安卡拉", site="安卡拉", coord=[32.86, 39.93]),
             dict(year=1928, headline="文字改革：以拉丁字母取代阿拉伯字母", site="安卡拉", coord=[32.86, 39.93]),
             dict(year=1934, headline="妇女获得选举权与被选举权", site="安卡拉", coord=[32.86, 39.93]),
             dict(year=1939, headline="哈塔伊并入土耳其", site="安塔基亚", coord=[36.16, 36.20]),
             dict(year=1952, headline="加入北约", site="安卡拉", coord=[32.86, 39.93]),
             dict(year=1980, headline="第三次军事政变与 1982 年宪法", site="安卡拉", coord=[32.86, 39.93]),
         ],
         settlements=[
             dict(ancient="安卡拉", modern="安卡拉", coord=[32.86, 39.93], isCapital=True, remark="1923 年起共和国首都"),
             dict(ancient="伊斯坦布尔", modern="伊斯坦布尔", coord=[28.98, 41.01], isCapital=False, remark="最大城市与经济中心"),
             dict(ancient="伊兹密尔", modern="伊兹密尔", coord=[27.14, 38.42], isCapital=False),
             dict(ancient="加济安泰普", modern="加济安泰普", coord=[37.38, 37.07], isCapital=False),
             dict(ancient="迪亚巴克尔", modern="迪亚巴克尔", coord=[40.23, 37.91], isCapital=False, remark="东南部库尔德地区中心"),
             dict(ancient="特拉布宗", modern="特拉布宗", coord=[39.72, 41.00], isCapital=False),
             dict(ancient="安塔基亚", modern="安塔基亚", coord=[36.16, 36.20], isCapital=False, remark="1939 年并入"),
         ]),
]

PERIODS_META = {
    "hittite": ("赫梯帝国", "赫梯", -1650, -1180, -1350, "#a8452f", "哈图沙（博阿兹卡莱）"),
    "post_hittite": ("后赫梯时代", "铁器早期", -1180, -700, -900, "#8a5a2b", "戈尔迪乌姆 · 图什帕 · 卡赫美什"),
    "lydia": ("吕底亚与东方诸国", "吕底亚", -700, -547, -600, "#b8892f", "萨第斯"),
    "achaemenid": ("阿契美尼德波斯", "波斯行省", -547, -334, -450, "#9a5f8f", "萨尔迪斯 · 达斯基雷翁"),
    "diadochi": ("继业者战争", "继业者", -334, -281, -310, "#8f6f3f", "吕西马基亚 · 安条克"),
    "hellenistic": ("希腊化诸王国", "希腊化", -281, -133, -200, "#b8892f", "帕加马 · 锡诺普 · 尼科米底亚"),
    "roman_conquest": ("罗马入主", "罗马征服", -133, -27, -80, "#8f3f3f", "以弗所 · 尼科米底亚"),
    "roman_empire": ("罗马帝国", "罗马", -27, 330, 117, "#8f3f3f", "以弗所 · 尼科米底亚 · 安条克"),
    "byzantine": ("拜占庭安纳托利亚", "拜占庭", 330, 1071, 950, "#8f3f6f", "君士坦丁堡"),
    "seljuk": ("曼齐刻尔特之后", "罗姆苏丹国", 1071, 1243, 1150, "#3f8f6a", "科尼亚 · 锡瓦斯 · 尼西亚"),
    "mongol": ("蒙古宗主权与贝伊国", "伊儿汗", 1243, 1300, 1275, "#7a5a8a", "科尼亚（藩属）· 卡拉曼"),
    "beylik": ("贝伊国与奥斯曼崛起", "贝伊国", 1300, 1453, 1400, "#a8452f", "布尔萨 · 埃迪尔内"),
    "ottoman": ("奥斯曼帝国鼎盛", "奥斯曼", 1453, 1683, 1566, "#a8452f", "伊斯坦布尔"),
    "ottoman_late": ("奥斯曼晚期", "晚期奥斯曼", 1683, 1922, 1880, "#a8452f", "伊斯坦布尔"),
    "republic": ("土耳其共和国", "共和国", 1923, 2026, 1938, "#a8452f", "安卡拉"),
}


def build_map_data():
    order = ["hittite", "post_hittite", "lydia", "achaemenid", "diadochi", "hellenistic",
             "roman_conquest", "roman_empire", "byzantine", "seljuk", "mongol", "beylik",
             "ottoman", "ottoman_late", "republic"]
    by_key = {c["key"]: c for c in CONTENT}
    dyn = []
    for k in order:
        c = by_key[k]
        title, badge, fy, ty, focus, tint, seat = PERIODS_META[k]
        dyn.append({
            "key": k,
            "title": title,
            "badge": badge,
            "fromYear": fy,
            "toYear": ty,
            "focusYear": focus,
            "tint": tint,
            "seat": seat,
            "summary": SUMMARY[k],
            "phases": [{"until": ty, "snap": f"s_{k}", "overview": f"{fy} — {ty} · {title}"}],
            "milestones": c["milestones"],
            "settlements": c["settlements"],
        })
    return dyn


SUMMARY = {}  # 由 gen_atlas.PERIODS 的 note 填充（见 main）

# 历史通道 / 商路（对应原项目 CORRIDOR_DATA 的“长城/运河”图层）
CORRIDORS = [
    {
        "key": "royal_road", "kind": "route", "title": "波斯“御道”（皇家大道）",
        "span": [-550, -330],
        "summary": "希罗多德记载的波斯御道自以弗所经萨第斯、弗里吉亚、奇里乞亚诸关隘至苏萨，全长约 450 帕拉桑（parasang），沿途设驿站，是阿契美尼德帝国控制小亚细亚的动脉。",
        "labelAt": [32.5, 38.6],
        "segments": [[[27.34, 37.94], [28.04, 38.48], [30.16, 38.07], [32.86, 39.93],
                      [35.49, 38.73], [36.16, 36.20], [38.79, 37.15], [40.23, 37.91],
                      [44.40, 33.31], [48.26, 32.19]]],
    },
    {
        "key": "via_maris", "kind": "route", "title": "罗马“海上大道”（Via Sebaste 与以弗所—塔尔苏斯干线）",
        "span": [-25, 400],
        "summary": "奥古斯都于前 6 年修筑 Via Sebaste，连接加拉太、皮西迪亚与潘菲利亚；以弗所—塔尔苏斯—安条克一线为帝国东部陆路主干，与海运互补。",
        "labelAt": [31.5, 38.0],
        "segments": [[[27.34, 37.94], [29.27, 37.74], [30.70, 36.89], [31.5, 37.2],
                      [34.90, 36.92], [36.16, 36.20]]],
    },
    {
        "key": "caravan_road", "kind": "route", "title": "安纳托利亚商队干线（丝绸之路西段）",
        "span": [1071, 1683],
        "summary": "塞尔柱与奥斯曼时期，科尼亚—开塞利—锡瓦斯—埃尔祖鲁姆—特拉布宗/大不里士的商队道（caravan sarayları）把黑海港口与波斯市场连接起来，13 世纪的苏丹哈尼（Sultanhanı）等驿站至今可见。",
        "labelAt": [37.0, 39.2],
        "segments": [[[32.49, 37.87], [34.70, 37.93], [35.49, 38.73], [37.02, 39.75],
                      [39.32, 39.67], [41.27, 39.90], [46.29, 38.07]]],
    },
]



# ---------------------------------------------------------------- 扩容事件（第二批）
EXTRA_MILESTONES = {
 "hittite": [
  {
   "year": -1610,
   "headline": "《铁列平诏令》确立王位继承法",
   "site": "哈图沙",
   "coord": [
    34.62,
    40.02
   ],
   "detail": "铁列平颁布诏令，规定王位只能由王室成员按次序继承，并设贵族议事会审理命案。这是赫梯最早的「宪法性」文献，试图终结此前频繁的宫廷谋杀。",
   "source": "《铁列平诏令》"
  },
  {
   "year": -1440,
   "headline": "图特哈里二世重建帝国",
   "site": "哈图沙",
   "coord": [
    34.62,
    40.02
   ],
   "detail": "中王国衰落后，图特哈里二世修复哈图沙城墙、重建对卡什卡与阿尔扎瓦的控制，为苏庇路里乌玛一世的扩张奠定基础。",
   "source": "赫梯泥板档案"
  },
  {
   "year": -1344,
   "headline": "苏庇路里乌玛一世即位",
   "site": "哈图沙",
   "coord": [
    34.62,
    40.02
   ],
   "detail": "他以军事与外交并用，先平西部阿尔扎瓦，再南下肢解米坦尼，把赫梯推上近东一等强国；其子穆尔西里二世延续扩张。",
   "source": "赫梯《苏庇路里乌玛功业录》"
  },
  {
   "year": -1295,
   "headline": "穆瓦塔里二世南迁都城塔尔胡恩塔萨",
   "site": "塔尔胡恩塔萨",
   "coord": [
    36.93,
    37.58
   ],
   "detail": "为贴近叙利亚前线，穆瓦塔里二世把政治中心南迁到塔尔胡恩塔萨；哈图沙仍为宗教中心，卡迭石之战即由此调度。",
   "source": "赫梯档案与考古"
  },
  {
   "year": -1190,
   "headline": "哈图沙的毁灭层",
   "site": "哈图沙",
   "coord": [
    34.62,
    40.02
   ],
   "detail": "考古在哈图沙发现火烧与弃城层，与青铜时代崩溃同期。赫梯书吏传统中断，城市荒废三千年，直到 19 世纪被重新发现、20 世纪由德国考古队系统发掘。",
   "source": "博阿兹卡莱发掘报告"
  }
 ],
 "post_hittite": [
  {
   "year": -1150,
   "headline": "弗里吉亚人进入安纳托利亚",
   "site": "戈尔迪乌姆",
   "coord": [
    31.98,
    39.65
   ],
   "detail": "希腊传统认为弗里吉亚人自巴尔干迁入，考古显示其陶器与墓葬在公元前 12—11 世纪突然出现于中西部，与赫梯崩溃的时间吻合。",
   "source": "《剑桥古代史》卷 II.2"
  },
  {
   "year": -850,
   "headline": "乌拉尔图的阿尔吉什提一世",
   "site": "图什帕",
   "coord": [
    43.38,
    38.49
   ],
   "detail": "阿尔吉什提一世把乌拉尔图扩张至亚美尼亚高原与库拉河，留下埃里温附近的「阿尔吉什提碑」，是乌拉尔图最盛期的铭文证据。",
   "source": "乌拉尔图楔形文字铭文"
  },
  {
   "year": -730,
   "headline": "辛梅里安人越过高加索",
   "site": "锡诺普",
   "coord": [
    35.15,
    42.03
   ],
   "detail": "辛梅里安人自高加索南下，先冲击乌拉尔图，再进入安纳托利亚中部，成为亚述与吕底亚共同的头号边患，也促成了安纳托利亚各邦的军事化。",
   "source": "亚述王室铭文"
  },
  {
   "year": -710,
   "headline": "迈达斯与亚述的角力",
   "site": "戈尔迪乌姆",
   "coord": [
    31.98,
    39.65
   ],
   "detail": "亚述王萨尔贡二世记载与「米塔」（Mita，即迈达斯）争夺东部商路；此后弗里吉亚被辛梅里安摧毁，戈尔迪乌姆的大墓成为其文明的最后遗存。",
   "source": "萨尔贡二世铭文"
  },
  {
   "year": -676,
   "headline": "乌拉尔图终被米底与斯基泰所灭",
   "site": "图什帕",
   "coord": [
    43.38,
    38.49
   ],
   "detail": "乌拉尔图在斯基泰与米底夹击下瓦解，凡城一带归米底；其水利工程、青铜工艺与岩刻传统被后继的亚美尼亚与波斯文化吸收。",
   "source": "希罗多德 / 巴比伦编年史"
  }
 ],
 "lydia": [
  {
   "year": -660,
   "headline": "吕底亚与爱奥尼亚希腊城邦的长期战争",
   "site": "米利都",
   "coord": [
    27.28,
    37.53
   ],
   "detail": "古革斯与阿尔迪斯进攻爱奥尼亚诸城，围攻米利都十余年未克；双方后来转为雇佣与贸易关系，吕底亚的骑兵与希腊的重装步兵互相补充。",
   "source": "希罗多德 i.14—22"
  },
  {
   "year": -590,
   "headline": "萨第斯的王家坟冢与阿耳忒弥斯神庙",
   "site": "萨第斯",
   "coord": [
    28.04,
    38.48
   ],
   "detail": "辛梅里安人撤走后萨第斯重建，出现巨型土墩王陵（tumulus，如 Bintepeler）与阿耳忒弥斯神庙，显示吕底亚王室财富与希腊工匠的结合。",
   "source": "萨第斯发掘报告"
  },
  {
   "year": -560,
   "headline": "克罗伊斯即位与德尔斐献礼",
   "site": "萨第斯",
   "coord": [
    28.04,
    38.48
   ],
   "detail": "克罗伊斯征服爱奥尼亚诸城、向德尔斐阿波罗神庙献厚礼并与斯巴达结盟，是「富如克罗伊斯」典故的由来，也是吕底亚外交的巅峰。",
   "source": "希罗多德 i.26—56"
  },
  {
   "year": -546,
   "headline": "帕克托罗斯河的砂金与铸币",
   "site": "萨第斯",
   "coord": [
    28.04,
    38.48
   ],
   "detail": "吕底亚金币的原料来自帕克托罗斯河冲积砂金；波斯接管后沿用其铸币重量标准与税制，希腊世界由此进入货币经济时代。",
   "source": "希罗多德 / 冶金考古"
  }
 ],
 "achaemenid": [
  {
   "year": -540,
   "headline": "大流士一世推行行省（satrapy）制度",
   "site": "萨第斯",
   "coord": [
    28.04,
    38.48
   ],
   "detail": "大流士把帝国划为二十余行省，安纳托利亚分属萨尔迪斯、赫勒斯滂弗里吉亚、卡帕多细亚等，实行定额贡赋与定期巡查，是古代最早的大规模官僚税制之一。",
   "source": "希罗多德 iii.89—97"
  },
  {
   "year": -520,
   "headline": "「王之道」与驿站系统",
   "site": "萨第斯",
   "coord": [
    28.04,
    38.48
   ],
   "detail": "自萨第斯直通苏萨的御道约 2500 公里、设约 90 处驿站，信使接力传递。希罗多德赞叹「无论雨雪黑夜都不能阻止他们跑完全程」。",
   "source": "希罗多德 v.52—53"
  },
  {
   "year": -492,
   "headline": "第一次波斯远征希腊",
   "site": "达达尼尔",
   "coord": [
    26.4,
    40.2
   ],
   "detail": "马多尼乌斯渡赫勒斯滂，舰队在阿陀斯海角遇风暴覆没；两年后达提斯与阿尔塔弗涅斯再度出征，在马拉松被雅典击败。",
   "source": "希罗多德 vi"
  },
  {
   "year": -480,
   "headline": "卡里亚女王阿耳忒弥西亚随军出征",
   "site": "哈利卡纳苏斯",
   "coord": [
    27.42,
    37.04
   ],
   "detail": "哈利卡纳苏斯的阿耳忒弥西亚一世以卡里亚与科斯等城之兵随薛西斯远征，萨拉米斯海战中为波斯殿军，被希罗多德称为「最有谋略的指挥官」。",
   "source": "希罗多德 vii—viii"
  },
  {
   "year": -334,
   "headline": "波斯治下的城市与混合精英",
   "site": "以弗所",
   "coord": [
    27.34,
    37.94
   ],
   "detail": "波斯时期安纳托利亚城市由「僭主—总督—神庙」三重结构治理，地方贵族与波斯王室通婚，形成融合希腊、吕底亚与波斯元素的精英阶层。",
   "source": "Briant《从居鲁士到亚历山大》"
  }
 ],
 "diadochi": [
  {
   "year": -330,
   "headline": "焚毁波斯波利斯",
   "site": "波斯波利斯",
   "coord": [
    52.89,
    29.94
   ],
   "detail": "亚历山大火焚波斯波利斯王宫，象征阿契美尼德王朝终结；他随后采用波斯宫廷礼仪与「君主崇拜」，引发马其顿旧部不满。",
   "source": "阿里安 iii.18"
  },
  {
   "year": -315,
   "headline": "安提柯一世控制小亚细亚",
   "site": "安条克",
   "coord": [
    36.16,
    36.2
   ],
   "detail": "继业者战争中安提柯一世占据小亚细亚大部，自称「亚洲统帅」，引发塞琉古、利西马科斯、卡山德结盟对抗，最终在伊普苏斯决战。",
   "source": "狄奥多罗斯 xix"
  },
  {
   "year": -305,
   "headline": "塞琉古一世营建安条克",
   "site": "安条克",
   "coord": [
    36.16,
    36.2
   ],
   "detail": "塞琉古在奥龙特斯河畔建安条克，成为希腊化东方最大城市之一，与埃及的亚历山大里亚并称；其港口塞琉西亚是地中海—内陆贸易枢纽。",
   "source": "斯特拉波 xvi"
  },
  {
   "year": -283,
   "headline": "安纳托利亚诸小王国自立",
   "site": "尼科米底亚",
   "coord": [
    29.92,
    40.77
   ],
   "detail": "塞琉古与利西马科斯相继身死后，帕加马、本都、比提尼亚、卡帕多细亚等本土王朝纷纷自立，形成「小王国林立」的格局，为罗马的介入留出空间。",
   "source": "斯特拉波 xii"
  }
 ],
 "hellenistic": [
  {
   "year": -222,
   "headline": "帕加马图书馆与羊皮纸",
   "site": "帕加马",
   "coord": [
    27.18,
    39.12
   ],
   "detail": "帕加马图书馆藏书约二十万卷；因托勒密王朝禁止纸草出口，当地发展出精制羊皮纸（pergamena），与亚历山大里亚图书馆争雄。",
   "source": "老普林尼《博物志》xiii"
  },
  {
   "year": -190,
   "headline": "马格尼西亚之战",
   "site": "马格尼西亚",
   "coord": [
    27.5,
    38.6
   ],
   "detail": "罗马与帕加马联军击败塞琉古安条克三世，确立罗马在小亚细亚的仲裁权；次年《阿帕米亚和约》使塞琉古退出托罗斯山以北。",
   "source": "李维 xxxvii"
  },
  {
   "year": -150,
   "headline": "加拉太人与雇佣兵经济",
   "site": "安卡拉",
   "coord": [
    32.86,
    39.93
   ],
   "detail": "加拉太诸部以武力出租为业，帕加马、比提尼亚、本都争相雇佣；其地后成为罗马的「加拉太行省」，安卡拉即其行政中心。",
   "source": "斯特拉波 xii"
  },
  {
   "year": -70,
   "headline": "米特里达梯战争的终结",
   "site": "锡诺普",
   "coord": [
    35.15,
    42.03
   ],
   "detail": "米特里达梯六世三度与罗马交战，最终在庞培追击下自尽；本都与比提尼亚并入罗马行省，黑海南岸的政治格局彻底改变。",
   "source": "阿庇安《米特里达梯战争》"
  }
 ],
 "roman_empire": [
  {
   "year": -129,
   "headline": "亚细亚行省的包税制",
   "site": "以弗所",
   "coord": [
    27.34,
    37.94
   ],
   "detail": "罗马以包税公司（publicani）征收亚细亚行省税，引发地方商人与元老院的长期冲突；西塞罗曾为被控勒索的总督弗拉库斯辩护。",
   "source": "西塞罗《为弗拉库斯辩护》"
  },
  {
   "year": 64,
   "headline": "保罗在以弗所传道与银匠骚乱",
   "site": "以弗所",
   "coord": [
    27.34,
    37.94
   ],
   "detail": "使徒保罗在亚细亚行省传道两年，以弗所的阿耳忒弥斯神庙与银匠行会因神像生意受损而暴动；基督教自此在小亚细亚扎根。",
   "source": "《使徒行传》19"
  },
  {
   "year": 117,
   "headline": "罗马大道与里程碑网络",
   "site": "以弗所",
   "coord": [
    27.34,
    37.94
   ],
   "detail": "罗马在安纳托利亚修筑数万公里石铺道路并立里程碑，以弗所—安条克干线是东方最繁忙的商道，也是军团调动的骨架。",
   "source": "罗马道路考古研究"
  },
  {
   "year": 251,
   "headline": "哥特人袭掠黑海南岸",
   "site": "特拉布宗",
   "coord": [
    39.72,
    41.0
   ],
   "detail": "哥特人自黑海北岸渡海袭掠本都与卡帕多细亚，焚毁神庙与城市，暴露三世纪危机中的海防漏洞；特拉布宗此后加筑城墙。",
   "source": "佐西莫斯 i.32"
  },
  {
   "year": 381,
   "headline": "君士坦丁堡公会议",
   "site": "君士坦丁堡",
   "coord": [
    28.98,
    41.01
   ],
   "detail": "第二次大公会议确立尼西亚—君士坦丁堡信经，并把君士坦丁堡教座提到罗马之后；安纳托利亚的教会格局（君士坦丁堡、以弗所、尼西亚）由此定型。",
   "source": "会议文献 / 教会史"
  }
 ],
 "byzantine": [
  {
   "year": 532,
   "headline": "尼卡暴动与圣索菲亚重建",
   "site": "君士坦丁堡",
   "coord": [
    28.98,
    41.01
   ],
   "detail": "君士坦丁堡的尼卡暴动几乎推翻查士丁尼，事后他重建圣索菲亚大教堂，成为拜占庭宗教建筑与帝国意识形态的巅峰。",
   "source": "普罗可比《战史》"
  },
  {
   "year": 626,
   "headline": "阿瓦尔人与波斯人围攻君士坦丁堡",
   "site": "君士坦丁堡",
   "coord": [
    28.98,
    41.01
   ],
   "detail": "阿瓦尔人与萨珊联军自陆海两面围城，拜占庭靠海军与城内补给守住城市；此役与随后的雅尔穆克形成帝国命运的分水岭。",
   "source": "《复活节编年史》"
  },
  {
   "year": 843,
   "headline": "圣像崇拜恢复",
   "site": "君士坦丁堡",
   "coord": [
    28.98,
    41.01
   ],
   "detail": "圣像破坏运动结束，「正统周日」确立；安纳托利亚的修道院（如卡帕多细亚岩窟修道院）与圣像艺术随之复兴。",
   "source": "Theophanes《编年史》"
  },
  {
   "year": 1037,
   "headline": "塞尔柱人西进与亚美尼亚高原",
   "site": "大不里士",
   "coord": [
    46.29,
    38.07
   ],
   "detail": "图格里勒贝格建立大塞尔柱帝国，控制伊朗与亚美尼亚高原，开始对高加索与安纳托利亚边境施压，为 1071 年的曼齐刻尔特埋下伏笔。",
   "source": "《剑桥伊朗史》"
  },
  {
   "year": 1176,
   "headline": "密列奥塞法隆之后的拜占庭战略转向",
   "site": "君士坦丁堡",
   "coord": [
    28.98,
    41.01
   ],
   "detail": "战败后拜占庭放弃清除突厥人的努力，转为修筑边境要塞、依赖通婚与雇佣突厥部队维持秩序，安纳托利亚的突厥化由此不可逆。",
   "source": "Choniates《历史》"
  }
 ],
 "seljuk": [
  {
   "year": 1081,
   "headline": "尼西亚成为罗姆苏丹国都城",
   "site": "尼西亚",
   "coord": [
    29.72,
    40.43
   ],
   "detail": "罗姆苏丹国以尼西亚为都，控制博斯普鲁斯对岸，直接威胁君士坦丁堡；直到 1097 年第一次十字军夺取尼西亚，苏丹国才南迁科尼亚。",
   "source": "Anna Komnene《阿莱克修斯传》"
  },
  {
   "year": 1116,
   "headline": "拜占庭—罗姆边界的长期稳定",
   "site": "科尼亚",
   "coord": [
    32.49,
    37.87
   ],
   "detail": "阿莱克修斯与约翰二世时期，双方以门德雷斯河与幼发拉底一线形成长期边界，游牧定居、贸易与朝贡并行，安纳托利亚出现突厥-希腊混合社会。",
   "source": "《剑桥土耳其史》"
  },
  {
   "year": 1145,
   "headline": "塞尔柱商队驿站网络成形",
   "site": "锡瓦斯",
   "coord": [
    37.02,
    39.75
   ],
   "detail": "罗姆苏丹国修建数十座商队客栈（han），提供三日免费食宿与武装保护；安纳托利亚由此成为欧亚贸易的枢纽，锡瓦斯与开塞利最盛。",
   "source": "塞尔柱建筑铭文与瓦克夫文书"
  },
  {
   "year": 1147,
   "headline": "第二次十字军穿越安纳托利亚",
   "site": "多里莱乌姆",
   "coord": [
    30.5,
    39.5
   ],
   "detail": "康拉德三世的德意志军队在多里莱乌姆被突厥骑兵击溃，撤退途中大量死亡；此役暴露十字军对突厥骑射战术与缺水的严重误判。",
   "source": "奥托《腓特烈一世纪》"
  }
 ],
 "mongol": [
  {
   "year": 1244,
   "headline": "伊儿汗国设罗姆行省",
   "site": "科尼亚",
   "coord": [
    32.49,
    37.87
   ],
   "detail": "蒙古在安纳托利亚设罗姆行省，派驻达鲁花赤与书记官，直接征收牧税、商税与户口调查，塞尔柱苏丹沦为税收承包人。",
   "source": "伊儿汗国文书"
  },
  {
   "year": 1277,
   "headline": "土库曼部众西迁",
   "site": "卡拉曼",
   "coord": [
    33.22,
    37.18
   ],
   "detail": "蒙古与马穆鲁克的拉锯迫使游牧部众向西北迁移，卡拉曼、奥斯曼等贝伊国在拜占庭边境成形，安纳托利亚的人口与族群结构被重塑。",
   "source": "贝伊国研究（Zachariadou 等）"
  },
  {
   "year": 1295,
   "headline": "加赞汗改宗伊斯兰教",
   "site": "大不里士",
   "coord": [
    46.29,
    38.07
   ],
   "detail": "伊儿汗国加赞汗改宗伊斯兰教并改革税制，安纳托利亚的蒙古统治者随之穆斯林化，与突厥贝伊国的文化隔阂缩小，也为伊儿汗国带来短暂复兴。",
   "source": "拉施特《史集》"
  }
 ],
 "beylik": [
  {
   "year": 1331,
   "headline": "奥尔汗铸币与行会制度",
   "site": "布尔萨",
   "coord": [
    29.06,
    40.19
   ],
   "detail": "奥尔汗首铸奥斯曼银币（akçe），扶植行会（ahi）并管制市场，标志奥斯曼从掠夺经济转向城市财政与常备行政。",
   "source": "早期奥斯曼铭文"
  },
  {
   "year": 1366,
   "headline": "加里波利地震与奥斯曼占领",
   "site": "加里波利",
   "coord": [
    26.67,
    40.42
   ],
   "detail": "地震毁坏加里波利城墙，奥斯曼趁机占领，取得越过达达尼尔的第一个桥头堡，此后向巴尔干持续扩张。",
   "source": "拜占庭编年史"
  },
  {
   "year": 1402,
   "headline": "空位期的兄弟战争",
   "site": "埃迪尔内",
   "coord": [
    26.56,
    41.68
   ],
   "detail": "巴耶济德的诸子在巴尔干与安纳托利亚混战十一年（1402—1413），最终穆罕默德一世重新统一；此期贝伊国复立、帝国元气大伤。",
   "source": "奥斯曼编年史"
  }
 ],
 "ottoman": [
  {
   "year": 1461,
   "headline": "特拉布宗帝国灭亡",
   "site": "特拉布宗",
   "coord": [
    39.72,
    41.0
   ],
   "detail": "穆罕默德二世吞并特拉布宗帝国，黑海南岸归入奥斯曼，黑海成为「内湖」，热那亚与威尼斯的黑海殖民地随之终结。",
   "source": "Kritovoulos《穆罕默德二世史》"
  },
  {
   "year": 1514,
   "headline": "查尔迪兰之战与火器优势",
   "site": "查尔迪兰",
   "coord": [
    44.0,
    38.5
   ],
   "detail": "奥斯曼以火炮与火枪车阵击败萨法维骑兵，确立「火药帝国」的军事范式；此役也确定了逊尼派奥斯曼与什叶派萨法维的东部均势。",
   "source": "奥斯曼编年史"
  },
  {
   "year": 1571,
   "headline": "塞浦路斯战争与法马古斯塔围城",
   "site": "法马古斯塔",
   "coord": [
    33.93,
    35.12
   ],
   "detail": "奥斯曼围攻法马古斯塔十一个月，威尼斯最终割让塞浦路斯；同年勒班陀海战成为基督教世界的报复性胜利，但塞浦路斯已归奥斯曼。",
   "source": "威尼斯与奥斯曼史料"
  },
  {
   "year": 1638,
   "headline": "穆拉德四世的巴格达远征",
   "site": "巴格达",
   "coord": [
    44.4,
    33.31
   ],
   "detail": "穆拉德四世重夺巴格达，暂时稳住东方边疆；但十七世纪的安纳托利亚经历杰拉里叛乱、人口下降与税制崩坏，乡村经济长期低迷。",
   "source": "《剑桥土耳其史》"
  }
 ],
 "ottoman_late": [
  {
   "year": 1730,
   "headline": "郁金香时代的终结",
   "site": "伊斯坦布尔",
   "coord": [
    28.98,
    41.01
   ],
   "detail": "帕特罗纳·哈利勒起义推翻郁金香时代的宫廷文化，艾哈迈德三世退位；此后的改革在保守派与改革派之间反复摆荡。",
   "source": "《剑桥土耳其史》"
  },
  {
   "year": 1826,
   "headline": "消灭近卫军（吉祥事变）",
   "site": "伊斯坦布尔",
   "coord": [
    28.98,
    41.01
   ],
   "detail": "马哈茂德二世炮轰近卫军营，废除这支延续四百余年、屡次废立苏丹的旧军，建立近代化新军与中央集权的行省体系。",
   "source": "Zürcher《现代土耳其史》"
  },
  {
   "year": 1856,
   "headline": "《巴黎条约》与改革诏书",
   "site": "伊斯坦布尔",
   "coord": [
    28.98,
    41.01
   ],
   "detail": "克里米亚战争后奥斯曼被纳入欧洲协调体系，《哈蒂-胡马云诏书》承诺宗教平等与改革，但引发保守派与地方势力抵制，成为「东方问题」的一部分。",
   "source": "Zürcher / 条约文本"
  },
  {
   "year": 1913,
   "headline": "巴尔干战争与穆斯林难民潮",
   "site": "埃迪尔内",
   "coord": [
    26.56,
    41.68
   ],
   "detail": "巴尔干战争后数十万穆斯林难民涌入安纳托利亚，改变人口与土地结构，也为后来的民族政治与人口交换埋下伏笔。",
   "source": "Zürcher"
  }
 ],
 "republic": [
  {
   "year": 1924,
   "headline": "废除哈里发制",
   "site": "安卡拉",
   "coord": [
    32.86,
    39.93
   ],
   "detail": "大国民议会废除哈里发制、关闭宗教法庭与宗教学校，世俗化改革正式启动；这是伊斯兰世界第一次以国家法令终结哈里发制度。",
   "source": "Zürcher"
  },
  {
   "year": 1946,
   "headline": "多党制的开端",
   "site": "安卡拉",
   "coord": [
    32.86,
    39.93
   ],
   "detail": "民主党成立并在 1950 年大选中获胜，实现土耳其首次和平政权更替；此前二十余年由共和人民党一党执政。",
   "source": "Zürcher"
  },
  {
   "year": 1999,
   "headline": "成为欧盟候选国",
   "site": "安卡拉",
   "coord": [
    32.86,
    39.93
   ],
   "detail": "赫尔辛基峰会给予土耳其候选国地位，随后推行法治、军队文职化与少数文化权利改革，以开启入盟谈判。",
   "source": "欧盟理事会文件"
  },
  {
   "year": 2016,
   "headline": "未遂政变与紧急状态",
   "site": "安卡拉",
   "coord": [
    32.86,
    39.93
   ],
   "detail": "2016 年 7 月政变未遂后实施两年紧急状态，大规模清洗军警与公务员；2017 年公投改行总统制，政治体制发生根本变化。",
   "source": "国际观察报告 / Zürcher 修订版"
  }
 ]
}



# ---------------------------------------------------------------- 扩容事件（第三批：战争细节/经济/灾害/文化）
EXTRA_MILESTONES_2 = {
 "hittite": [
  {
   "year": -1620,
   "headline": "赫梯南下阿勒颇与幼发拉底",
   "site": "阿勒颇",
   "coord": [
    37.16,
    36.2
   ],
   "detail": "哈图西里一世南下攻阿勒颇与幼发拉底沿线，确立赫梯在叙利亚的第一次扩张，并带回巴比伦的战利品与书吏传统。",
   "source": "赫梯泥板档案"
  },
  {
   "year": -1500,
   "headline": "卡什卡诸部南下侵扰北境",
   "site": "卡什卡山地",
   "coord": [
    36.5,
    41.0
   ],
   "detail": "山地部族卡什卡趁赫梯中衰南下，反复劫掠北境，甚至威胁哈图沙；赫梯以筑垒、迁徙与季节征讨应对，成为长期边患。",
   "source": "赫梯档案"
  },
  {
   "year": -1330,
   "headline": "阿马尔那书信时代",
   "site": "哈图沙",
   "coord": [
    34.62,
    40.02
   ],
   "detail": "埃及、赫梯、米坦尼、巴比伦之间的泥板外交书信（阿马尔那文书）是青铜时代国际关系的一手材料，内容涉及王朝联姻、礼物交换与逃犯引渡。",
   "source": "阿马尔那书信 / 赫梯档案"
  },
  {
   "year": -1258,
   "headline": "沿海劫掠与「海上民族」前夜",
   "site": "哈图沙",
   "coord": [
    34.62,
    40.02
   ],
   "detail": "赫梯档案记载 Ahhiyawa 与沿海劫掠活动，塞浦路斯（阿拉西亚）与南岸最先受冲击；这是 1180 年大崩溃前数十年的预警信号。",
   "source": "赫梯泥板 / 乌加里特文书"
  }
 ],
 "post_hittite": [
  {
   "year": -1000,
   "headline": "铁器技术随帝国崩溃扩散",
   "site": "卡赫美什",
   "coord": [
    38.02,
    36.83
   ],
   "detail": "赫梯长期垄断的冶铁与锻打技术随帝国解体向外流散，安纳托利亚成为铁器早期扩散的核心区之一，农具与武器成本随之下降。",
   "source": "冶金考古研究"
  },
  {
   "year": -930,
   "headline": "草原压力与筑垒化定居",
   "site": "锡瓦斯",
   "coord": [
    37.02,
    39.75
   ],
   "detail": "高加索与黑海草原的游牧压力加剧，东部安纳托利亚出现密集的筑垒定居点与山地避难所，村落网络比青铜时代更分散。",
   "source": "安纳托利亚考古调查"
  },
  {
   "year": -830,
   "headline": "亚述驿道与贡赋体系",
   "site": "迪亚巴克尔",
   "coord": [
    40.23,
    37.91
   ],
   "detail": "亚述在东南安纳托利亚设驿道与行省，向当地小邦征收铁、马匹与木料，把高原经济纳入两河流域的帝国体系。",
   "source": "亚述行政文书"
  },
  {
   "year": -760,
   "headline": "迈达斯向德尔斐献金座",
   "site": "戈尔迪乌姆",
   "coord": [
    31.98,
    39.65
   ],
   "detail": "迈达斯王向德尔斐阿波罗神庙献上宝座，是安纳托利亚君主首次直接介入希腊宗教中心，反映弗里吉亚与爱琴海世界的贸易与外交深度。",
   "source": "希罗多德 i.14"
  }
 ],
 "lydia": [
  {
   "year": -640,
   "headline": "吕底亚骑兵东进卡帕多细亚",
   "site": "卡帕多细亚",
   "coord": [
    35.5,
    38.7
   ],
   "detail": "吕底亚以骑射与重装骑兵称雄，向东推进至哈里斯河一线，与米底形成长期对峙，东部诸小邦夹在两者之间。",
   "source": "希罗多德 i.73—74"
  },
  {
   "year": -600,
   "headline": "萨第斯的手工业与染坊区",
   "site": "萨第斯",
   "coord": [
    28.04,
    38.48
   ],
   "detail": "考古在萨第斯发现染坊、作坊与商业街区，显示吕底亚宫廷财富与手工业者、希腊工匠之间的共生关系。",
   "source": "萨第斯发掘报告"
  },
  {
   "year": -580,
   "headline": "吕底亚与米利都的互不侵犯条约",
   "site": "米利都",
   "coord": [
    27.28,
    37.53
   ],
   "detail": "吕底亚与米利都达成和平与雇佣协议：米利都获得内陆市场，吕底亚获得海军技术与外交通道，是「强国—城邦」共生的典型。",
   "source": "希罗多德 i.22"
  },
  {
   "year": -550,
   "headline": "居鲁士遣使与斯巴达的迟疑",
   "site": "萨第斯",
   "coord": [
    28.04,
    38.48
   ],
   "detail": "居鲁士遣使要求吕底亚臣服，克罗伊斯转向斯巴达求援；斯巴达援军未及赶赴，萨第斯在两周内陷落。",
   "source": "希罗多德 i.69—81"
  }
 ],
 "achaemenid": [
  {
   "year": -513,
   "headline": "大流士远征斯基泰与色雷斯",
   "site": "达达尼尔",
   "coord": [
    26.4,
    40.2
   ],
   "detail": "大流士渡博斯普鲁斯与多瑙河远征斯基泰，虽未成功，却确立了对赫勒斯滂与色雷斯的控制，为希波战争完成战略布局。",
   "source": "希罗多德 iv"
  },
  {
   "year": -480,
   "headline": "萨拉米斯海战与波斯撤军",
   "site": "萨第斯",
   "coord": [
    28.04,
    38.48
   ],
   "detail": "波斯舰队在萨拉米斯覆没，薛西斯退回亚洲；安纳托利亚的希腊城邦短暂摆脱波斯控制，但前 386 年后再度归附。",
   "source": "希罗多德 viii / 埃斯库罗斯《波斯人》"
  },
  {
   "year": -450,
   "headline": "萨尔迪斯的铸币与行省税",
   "site": "萨第斯",
   "coord": [
    28.04,
    38.48
   ],
   "detail": "波斯在萨尔迪斯铸造金币（daric）与银币（siglos），安纳托利亚既是帝国税基也是货币经济最发达的地区之一。",
   "source": "钱币学研究"
  },
  {
   "year": -400,
   "headline": "小居鲁士在萨第斯起兵",
   "site": "萨第斯",
   "coord": [
    28.04,
    38.48
   ],
   "detail": "波斯王子小居鲁士在萨第斯集结希腊雇佣军反叛兄长阿尔塔薛西斯二世，库纳克萨战死后希腊人北撤，即色诺芬《长征记》记载的撤退。",
   "source": "《长征记》i"
  }
 ],
 "diadochi": [
  {
   "year": -323,
   "headline": "巴比伦分封与安纳托利亚的瓜分",
   "site": "塔尔苏斯",
   "coord": [
    34.9,
    36.92
   ],
   "detail": "亚历山大的部将依「巴比伦分封」划分疆土，安纳托利亚被分给培松与安提柯，随后三十年成为继业者战争的主战场。",
   "source": "狄奥多罗斯 xviii"
  },
  {
   "year": -312,
   "headline": "塞琉古夺回巴比伦",
   "site": "安条克",
   "coord": [
    36.16,
    36.2
   ],
   "detail": "塞琉古夺回巴比伦并建立塞琉古纪元（312 年），随后西进小亚细亚，奠定塞琉古王朝对叙利亚与东部的统治。",
   "source": "阿庇安《叙利亚史》"
  },
  {
   "year": -305,
   "headline": "希腊化君主崇拜的兴起",
   "site": "帕加马",
   "coord": [
    27.18,
    39.12
   ],
   "detail": "继业者纷纷采用「救主」「胜利者」「显神者」等神性称号，安纳托利亚城市以神庙、竞技庆典与纪年回应，形成新的城市宗教政治。",
   "source": "希腊化时期铭文"
  },
  {
   "year": -285,
   "headline": "利西马基亚的建立",
   "site": "吕西马基亚",
   "coord": [
    26.7,
    40.55
   ],
   "detail": "利西马科斯在色雷斯与赫勒斯滂之间建新都吕西马基亚，成为连接欧洲与安纳托利亚的军事枢纽与贸易口岸。",
   "source": "斯特拉波 / 考古"
  }
 ],
 "hellenistic": [
  {
   "year": -230,
   "headline": "「垂死的高卢人」与胜利纪念",
   "site": "帕加马",
   "coord": [
    27.18,
    39.12
   ],
   "detail": "击败加拉太人后，帕加马在卫城立「垂死的高卢人」等组雕，以希腊化艺术宣示胜利，是古代政治宣传与艺术结合的典范。",
   "source": "老普林尼《博物志》/ 帕加马卫城"
  },
  {
   "year": -197,
   "headline": "罗马成为东方事务的裁决者",
   "site": "以弗所",
   "coord": [
    27.34,
    37.94
   ],
   "detail": "库诺斯克法莱之战后，罗马成为希腊—安纳托利亚事务的仲裁者，帕加马与本都皆以「罗马之友」自居并借此扩张。",
   "source": "波利比乌斯 / 李维"
  },
  {
   "year": -133,
   "headline": "阿塔罗斯遗嘱与阿里斯托尼库斯起义",
   "site": "帕加马",
   "coord": [
    27.18,
    39.12
   ],
   "detail": "阿塔罗斯三世把王国遗赠罗马，引发阿里斯托尼库斯领导的反抗（「太阳城」运动），罗马镇压后正式设亚细亚行省。",
   "source": "斯特拉波 xiv"
  },
  {
   "year": -85,
   "headline": "《达达诺斯和约》",
   "site": "达达诺斯",
   "coord": [
    26.2,
    40.1
   ],
   "detail": "苏拉与米特里达梯六世缔结和约：本都赔款并退出西部，安纳托利亚城市在战火后普遍负债，罗马包税制度的弊端由此暴露。",
   "source": "阿庇安《米特里达梯战争》"
  }
 ],
 "roman_empire": [
  {
   "year": -88,
   "headline": "「亚洲晚祷」大屠杀",
   "site": "以弗所",
   "coord": [
    27.34,
    37.94
   ],
   "detail": "米特里达梯六世策划一夜之间屠杀安纳托利亚的罗马与意大利商人（古代文献称约八万人），是古代规模最大的商业侨民屠杀之一。",
   "source": "阿庇安 / 普鲁塔克《苏拉传》"
  },
  {
   "year": 17,
   "headline": "提比略的地震赈灾",
   "site": "以弗所",
   "coord": [
    27.34,
    37.94
   ],
   "detail": "公元 17 年大地震毁坏以弗所等十二座城市，提比略免除赋税并拨巨款重建；罗马皇帝由此被纳入东方城市的宗教性颂扬体系。",
   "source": "塔西佗《编年史》ii.47"
  },
  {
   "year": 120,
   "headline": "罗马道路网与邮驿",
   "site": "安卡拉",
   "coord": [
    32.86,
    39.93
   ],
   "detail": "以弗所—安卡拉—安条克的道路网承担军团调动与邮驿，安卡拉成为加拉太行省枢纽，并留下奥古斯都神庙的《功德录》双语碑铭。",
   "source": "罗马道路研究 / 安卡拉纪念碑"
  },
  {
   "year": 249,
   "headline": "德西乌斯迫害与殉道记忆",
   "site": "以弗所",
   "coord": [
    27.34,
    37.94
   ],
   "detail": "德西乌斯下令全帝国献祭，安纳托利亚基督徒大量殉道；「叛教者」能否重新入会引发长期争论，塑造了教会的忏悔制度。",
   "source": "优西比乌《教会史》"
  }
 ],
 "byzantine": [
  {
   "year": 541,
   "headline": "查士丁尼瘟疫",
   "site": "君士坦丁堡",
   "coord": [
    28.98,
    41.01
   ],
   "detail": "鼠疫自埃及经海路传入，君士坦丁堡死亡过半；安纳托利亚人口与税基长期萎缩，帝国由扩张转为守成。",
   "source": "普罗可比《战史》ii"
  },
  {
   "year": 614,
   "headline": "萨珊劫掠安纳托利亚城市",
   "site": "凯撒利亚",
   "coord": [
    35.49,
    38.73
   ],
   "detail": "萨珊军队劫掠安纳托利亚城市并夺取「真十字架」，拜占庭在 7 世纪初一度濒临崩溃，直到 628 年反攻得手。",
   "source": "《复活节编年史》"
  },
  {
   "year": 740,
   "headline": "阿克罗伊农之战",
   "site": "阿克罗伊农",
   "coord": [
    30.6,
    38.85
   ],
   "detail": "利奥三世与君士坦丁五世在阿克罗伊农击败倭马亚军队，终结阿拉伯对安纳托利亚腹地的大规模入侵，军区制由此稳固。",
   "source": "Theophanes《编年史》"
  },
  {
   "year": 860,
   "headline": "罗斯人袭掠博斯普鲁斯",
   "site": "君士坦丁堡",
   "coord": [
    28.98,
    41.01
   ],
   "detail": "罗斯舰队袭击博斯普鲁斯沿岸与王子群岛，拜占庭以外交与通商（与可萨、罗斯）应对，黑海贸易格局随之变化。",
   "source": "牧首佛提乌讲道"
  }
 ],
 "seljuk": [
  {
   "year": 1086,
   "headline": "突厥化与「两重社会」",
   "site": "科尼亚",
   "coord": [
    32.49,
    37.87
   ],
   "detail": "突厥游牧部落与希腊农民混居，形成草原税制与城市手工业并存的双重社会；地名大量突厥化，基督教社群逐步减少。",
   "source": "Cahen《前奥斯曼土耳其》"
  },
  {
   "year": 1158,
   "headline": "曼努埃尔的东方远征",
   "site": "阿达纳",
   "coord": [
    35.32,
    37.0
   ],
   "detail": "曼努埃尔一世迫使罗姆苏丹称臣、奇里乞亚亚美尼亚王国割地，短暂恢复拜占庭在东南的宗主权；但其后继者无力维持。",
   "source": "Choniates《历史》"
  },
  {
   "year": 1214,
   "headline": "尼西亚帝国与罗姆的边界协定",
   "site": "尼西亚",
   "coord": [
    29.72,
    40.43
   ],
   "detail": "第四次十字军后，尼西亚帝国成为拜占庭正统继承者，与罗姆苏丹国划定边界，安纳托利亚西部形成长期均势。",
   "source": "Akropolites《编年史》"
  },
  {
   "year": 1219,
   "headline": "罗姆苏丹国夺取黑海与地中海港口",
   "site": "阿拉尼亚",
   "coord": [
    32.0,
    36.54
   ],
   "detail": "凯库巴德一世夺取阿拉尼亚与锡诺普，使罗姆苏丹国同时拥有地中海与黑海出口，商队税与过境贸易收入大增。",
   "source": "塞尔柱建筑铭文与瓦克夫文书"
  }
 ],
 "mongol": [
  {
   "year": 1261,
   "headline": "尼西亚光复与东方困局",
   "site": "君士坦丁堡",
   "coord": [
    28.98,
    41.01
   ],
   "detail": "尼西亚帝国收复君士坦丁堡，但安纳托利亚的蒙古宗主权与贝伊国割据已成定局，拜占庭再也无力恢复东方领土。",
   "source": "Akropolites / 拜占庭史料"
  },
  {
   "year": 1280,
   "headline": "伊儿汗国的货币与税册统一",
   "site": "大不里士",
   "coord": [
    46.29,
    38.07
   ],
   "detail": "伊儿汗国统一银币（dirham）与税册，安纳托利亚的货币、度量衡与征税周期被纳入蒙古体系，商路秩序短期改善。",
   "source": "伊儿汗国文书"
  },
  {
   "year": 1300,
   "headline": "贝伊国的海上劫掠与联合反击",
   "site": "伊兹密尔",
   "coord": [
    27.14,
    38.42
   ],
   "detail": "艾登、门泰塞等贝伊国以海盗舰队袭扰爱琴海，引发威尼斯、热那亚与医院骑士团的联合反击，促成了 14 世纪的「十字军同盟」。",
   "source": "威尼斯档案"
  }
 ],
 "beylik": [
  {
   "year": 1329,
   "headline": "佩莱卡农之战",
   "site": "佩莱卡农",
   "coord": [
    29.4,
    40.8
   ],
   "detail": "奥尔汗击败拜占庭摄政约翰六世，控制比提尼亚通道；拜占庭从此再无反击能力，只能以雇佣与联姻维持。",
   "source": "拜占庭史料（坎塔库泽努斯）"
  },
  {
   "year": 1354,
   "headline": "加里波利站稳脚跟",
   "site": "加里波利",
   "coord": [
    26.67,
    40.42
   ],
   "detail": "奥斯曼在加里波利移民驻军，向色雷斯扩张；巴尔干由此成为帝国重心，安纳托利亚反而成为后方。",
   "source": "奥斯曼编年史"
  },
  {
   "year": 1400,
   "headline": "帖木儿的安纳托利亚战役",
   "site": "锡瓦斯",
   "coord": [
    37.02,
    39.75
   ],
   "detail": "帖木儿攻掠锡瓦斯并屠守军，随后南下叙利亚击溃马穆鲁克；安纳托利亚的贝伊国格局被重新洗牌，为安卡拉之战铺路。",
   "source": "帖木儿史料 / 伊本·阿拉布沙"
  }
 ],
 "ottoman": [
  {
   "year": 1475,
   "headline": "夺取卡法与黑海贸易",
   "site": "锡诺普",
   "coord": [
    35.15,
    42.03
   ],
   "detail": "奥斯曼夺取热那亚在黑海的据点卡法，把黑海贸易与克里米亚汗国纳入体系，安纳托利亚北岸港口因此受益。",
   "source": "奥斯曼档案"
  },
  {
   "year": 1492,
   "headline": "塞法迪犹太人迁入",
   "site": "伊斯坦布尔",
   "coord": [
    28.98,
    41.01
   ],
   "detail": "西班牙驱逐令后大批塞法迪犹太人迁入奥斯曼，定居伊斯坦布尔、伊兹密尔与萨洛尼卡，带来印刷术、金融与巴尔干贸易网络。",
   "source": "奥斯曼档案研究"
  },
  {
   "year": 1555,
   "headline": "《阿马西亚和约》",
   "site": "阿马西亚",
   "coord": [
    35.83,
    40.65
   ],
   "detail": "奥斯曼与萨法维划定东部边界，战线稳定数十年；安纳托利亚东部得以恢复农业与商路，凡城与埃尔祖鲁姆重新繁荣。",
   "source": "奥斯曼/萨法维史料"
  },
  {
   "year": 1580,
   "headline": "白银流入与「大逃亡」",
   "site": "伊斯坦布尔",
   "coord": [
    28.98,
    41.01
   ],
   "detail": "美洲白银流入引发物价革命，奥斯曼财政失衡，安纳托利亚出现农民弃田逃亡（Büyük Kaçgun），土地荒废与杰拉里叛乱随之而来。",
   "source": "《剑桥土耳其史》"
  }
 ],
 "ottoman_late": [
  {
   "year": 1789,
   "headline": "塞利姆三世的「新秩序」",
   "site": "伊斯坦布尔",
   "coord": [
    28.98,
    41.01
   ],
   "detail": "塞利姆三世推行新军（Nizam-ı Cedid）与常驻大使馆，被保守派推翻；但「改革—反扑—再改革」的循环由此定型。",
   "source": "Zürcher"
  },
  {
   "year": 1863,
   "headline": "奥斯曼银行与公共债务",
   "site": "伊斯坦布尔",
   "coord": [
    28.98,
    41.01
   ],
   "detail": "设立奥斯曼银行（后为帝国银行）与公共债务管理署，欧洲资本进入安纳托利亚的铁路、港口与矿业，财政主权逐步外移。",
   "source": "Zürcher"
  },
  {
   "year": 1896,
   "headline": "安纳托利亚铁路通车",
   "site": "安卡拉",
   "coord": [
    32.86,
    39.93
   ],
   "detail": "伊斯坦布尔—安卡拉铁路通车，内陆城市与港口连成一体，安纳托利亚的经济地理与行政中心由此重写。",
   "source": "Zürcher"
  },
  {
   "year": 1908,
   "headline": "青年土耳其党革命",
   "site": "伊斯坦布尔",
   "coord": [
    28.98,
    41.01
   ],
   "detail": "青年土耳其党在萨洛尼卡起事，迫使苏丹恢复 1876 年宪法，开启第二立宪时期；政治重心从宫廷转向政党与军队。",
   "source": "Zürcher"
  }
 ],
 "republic": [
  {
   "year": 1930,
   "headline": "女性获得市政选举权",
   "site": "安卡拉",
   "coord": [
    32.86,
    39.93
   ],
   "detail": "1930 年女性获得市政选举权，1934 年获得全国选举权与被选举权，是同期欧洲较早实现的国家之一。",
   "source": "Zürcher"
  },
  {
   "year": 1963,
   "headline": "《安卡拉协定》与欧共体",
   "site": "安卡拉",
   "coord": [
    32.86,
    39.93
   ],
   "detail": "土耳其与欧共体签订《安卡拉协定》成为联系国，此后关税同盟与入盟进程构成其外交与经济政策的主轴。",
   "source": "欧盟文件"
  },
  {
   "year": 1984,
   "headline": "东南部的长期冲突",
   "site": "迪亚巴克尔",
   "coord": [
    40.23,
    37.91
   ],
   "detail": "PKK 开始武装行动，东南部进入长期冲突状态，村庄撤离与人口迁徙加剧区域发展失衡，成为共和国后期的核心议题。",
   "source": "学术研究与公开报告"
  },
  {
   "year": 2023,
   "headline": "共和国百年",
   "site": "安卡拉",
   "coord": [
    32.86,
    39.93
   ],
   "detail": "2023 年土耳其迎来共和国百年，同年经历东南大地震与总统选举；区域差距、叙利亚难民与通胀仍是核心议题。",
   "source": "公开报告"
  }
 ]
}


# 南界扩到 29.5°N 后的埃及—黎凡特—两河名城：按时代挂到对应阶段
EXTRA_SETTLEMENTS = {
    "hittite": [
        dict(ancient="孟菲斯", modern="孟菲斯遗址（埃及）", coord=[31.25, 29.85], remark="埃及新王国北都，卡迭石之战的一方"),
        dict(ancient="底比斯", modern="卢克索（埃及）", coord=[32.65, 25.70], remark="埃及新王国宗教首都（图外以南）"),
        dict(ancient="尼尼微", modern="摩苏尔附近（伊拉克）", coord=[43.15, 36.36], remark="中亚述都城"),
        dict(ancient="乌尔", modern="乌尔遗址（伊拉克）", coord=[46.10, 30.96], remark="两河南部圣城"),
    ],
    "post_hittite": [
        dict(ancient="大马士革", modern="大马士革（叙利亚）", coord=[36.29, 33.51], remark="亚兰-大马士革王国都城"),
        dict(ancient="推罗", modern="苏尔（黎巴嫩）", coord=[35.20, 33.27], remark="腓尼基殖民母邦，前 9 世纪建立迦太基"),
        dict(ancient="尼尼微", modern="摩苏尔附近（伊拉克）", coord=[43.15, 36.36], remark="亚述帝国晚期都城"),
    ],
    "lydia": [
        dict(ancient="耶路撒冷", modern="耶路撒冷", coord=[35.23, 31.78], remark="前 586 年第一圣殿被新巴比伦焚毁"),
        dict(ancient="孟菲斯", modern="孟菲斯遗址（埃及）", coord=[31.25, 29.85], remark="埃及后王朝都城之一"),
        dict(ancient="推罗", modern="苏尔（黎巴嫩）", coord=[35.20, 33.27], remark="尼布甲尼撒围城十三年未克"),
    ],
    "achaemenid": [
        dict(ancient="耶路撒冷", modern="耶路撒冷", coord=[35.23, 31.78], remark="波斯敕令归回重建圣殿"),
        dict(ancient="苏萨", modern="舒什（伊朗）", coord=[48.25, 32.19], remark="阿契美尼德冬都，《以斯帖记》场景"),
        dict(ancient="孟菲斯", modern="孟菲斯遗址（埃及）", coord=[31.25, 29.85], remark="波斯埃及行省首府"),
        dict(ancient="西顿", modern="赛达（黎巴嫩）", coord=[35.37, 33.56], remark="腓尼基城邦，波斯海军主要提供者"),
    ],
    "alexander": [
        dict(ancient="亚历山大港", modern="亚历山大（埃及）", coord=[29.92, 31.20], remark="前 331 年建城，托勒密王朝首都"),
        dict(ancient="孟菲斯", modern="孟菲斯遗址（埃及）", coord=[31.25, 29.85], remark="亚历山大在孟菲斯加冕"),
        dict(ancient="推罗", modern="苏尔（黎巴嫩）", coord=[35.20, 33.27], remark="前 332 年被亚历山大围攻七月而陷"),
        dict(ancient="加沙", modern="加沙", coord=[34.47, 31.50], remark="前 332 年围城，波斯埃及通道的要点"),
    ],
    "diadochi": [
        dict(ancient="亚历山大港", modern="亚历山大（埃及）", coord=[29.92, 31.20], remark="托勒密王朝首都，地中海学术中心"),
        dict(ancient="安条克", modern="安塔基亚（土耳其）", coord=[36.16, 36.20], remark="前 300 年建城，塞琉古王朝西都"),
        dict(ancient="耶路撒冷", modern="耶路撒冷", coord=[35.23, 31.78], remark="塞琉古与托勒密反复争夺的圣城"),
    ],
    "roman_empire": [
        dict(ancient="亚历山大港", modern="亚历山大（埃及）", coord=[29.92, 31.20], remark="罗马埃及行省首府，帝国第二大城市"),
        dict(ancient="耶路撒冷", modern="耶路撒冷", coord=[35.23, 31.78], remark="70 年第二圣殿被毁"),
        dict(ancient="帕尔米拉", modern="泰德穆尔（叙利亚）", coord=[38.27, 34.55], remark="沙漠商队之城，270 年自立为帝国"),
        dict(ancient="安条克", modern="安塔基亚（土耳其）", coord=[36.16, 36.20], remark="罗马叙利亚行省首府，东方军团大本营"),
    ],
    "byzantine": [
        dict(ancient="亚历山大港", modern="亚历山大（埃及）", coord=[29.92, 31.20], remark="641 年落入阿拉伯人之手，帝国粮仓尽失"),
        dict(ancient="耶路撒冷", modern="耶路撒冷", coord=[35.23, 31.78], remark="614 年萨珊劫掠，638 年阿拉伯接管"),
        dict(ancient="大马士革", modern="大马士革（叙利亚）", coord=[36.29, 33.51], remark="635 年陷落，661 年起为倭马亚王朝首都"),
        dict(ancient="开罗", modern="福斯塔特—开罗（埃及）", coord=[31.24, 30.04], remark="641 年福斯塔特建城，埃及行省新首府"),
    ],
    "seljuk": [
        dict(ancient="开罗", modern="开罗（埃及）", coord=[31.24, 30.04], remark="969 年法蒂玛建城，1171 年后阿尤布都城"),
        dict(ancient="大马士革", modern="大马士革（叙利亚）", coord=[36.29, 33.51], remark="赞吉与阿尤布王朝的叙利亚中枢"),
        dict(ancient="耶路撒冷", modern="耶路撒冷", coord=[35.23, 31.78], remark="1099 年十字军攻陷，1187 年萨拉丁收复"),
        dict(ancient="阿勒颇", modern="阿勒颇（叙利亚）", coord=[37.16, 36.20], remark="赞吉王朝重镇，与十字军反复易手"),
    ],
    "mongol": [
        dict(ancient="开罗", modern="开罗（埃及）", coord=[31.24, 30.04], remark="马穆鲁克苏丹国首都，1260 年艾因贾鲁特阻击蒙古"),
        dict(ancient="大马士革", modern="大马士革（叙利亚）", coord=[36.29, 33.51], remark="马穆鲁克叙利亚首府"),
        dict(ancient="耶路撒冷", modern="耶路撒冷", coord=[35.23, 31.78], remark="1291 年阿卡陷落后十字军彻底退出黎凡特"),
    ],
    "ottoman": [
        dict(ancient="开罗", modern="开罗（埃及）", coord=[31.24, 30.04], remark="1517 年塞利姆一世灭马穆鲁克，设埃及行省"),
        dict(ancient="大马士革", modern="大马士革（叙利亚）", coord=[36.29, 33.51], remark="奥斯曼叙利亚行省首府，朝觐队伍集结点"),
        dict(ancient="耶路撒冷", modern="耶路撒冷", coord=[35.23, 31.78], remark="奥斯曼耶路撒冷桑贾克，苏莱曼重修城墙"),
        dict(ancient="亚历山大港", modern="亚历山大（埃及）", coord=[29.92, 31.20], remark="奥斯曼海军基地，1798 年拿破仑登陆"),
    ],
    "ottoman_late": [
        dict(ancient="开罗", modern="开罗（埃及）", coord=[31.24, 30.04], remark="1805 年穆罕默德·阿里自立，名义仍属奥斯曼"),
        dict(ancient="苏伊士", modern="苏伊士（埃及）", coord=[32.55, 29.97], remark="1869 年运河通航，帝国近东地位受制于英法"),
        dict(ancient="耶路撒冷", modern="耶路撒冷", coord=[35.23, 31.78], remark="1917 年英军入城，奥斯曼统治结束"),
        dict(ancient="大马士革", modern="大马士革（叙利亚）", coord=[36.29, 33.51], remark="1918 年费萨尔在此宣布阿拉伯王国"),
    ],
    "republic": [
        dict(ancient="开罗", modern="开罗（埃及）", coord=[31.24, 30.04], remark="1952 年自由军官革命，地区政治重心之一"),
        dict(ancient="大马士革", modern="大马士革（叙利亚）", coord=[36.29, 33.51], remark="叙利亚内战与外溢的主要受影响城市"),
        dict(ancient="耶路撒冷", modern="耶路撒冷", coord=[35.23, 31.78], remark="巴以问题的核心地点"),
    ],
}


# ---------------------------------------------------------------- 合并新增聚落
_extra_settle_merged = False


# ---------------------------------------------------------------- 聚落出处
# 逐个遗址的一手/权威出处；未列出的按时代取该时代的参考书目（见 data/sources/<era>.json）
SITE_SOURCE = {
    "哈图沙": "Boğazköy（哈图沙）发掘报告 / Bryce《赫梯王国》",
    "沙皮努瓦": "Boğazköy 档案与 Kayalıpınar 发掘 / Bryce",
    "内萨": "Kültepe（卡尼什）发掘报告（Tahsin Özgüç）",
    "卡尼什": "Kültepe 亚述商馆档案（TC III）/ Özgüç",
    "塔尔胡恩塔萨": "Yalburt 与 Gavurkale 铭文 / Bryce",
    "戈尔迪乌姆": "Gordion 发掘报告（宾夕法尼亚大学）/《剑桥古代史》卷 3",
    "萨第斯": "Sardis 发掘报告（哈佛—康奈尔）/ 希罗多德 i",
    "以弗所": "ÖAI 以弗所发掘报告 /《以弗所铭文集成》(IvE)",
    "米利都": "Milet 发掘报告（柏林）/ 希罗多德 v",
    "帕加马": "Altertümer von Pergamon 系列 / Hansen《阿塔罗斯王朝的帕加马》",
    "特洛伊": "Troia 发掘报告（Korfmann）/ 荷马《伊利亚特》",
    "图什帕": "凡城城堡与 Kef Kalesi 铭文 / Zimansky《古代乌拉尔图》",
    "卡赫美什": "Carchemish 发掘报告（Hogarth/Woolley）/ Bryce",
    "尼尼微": "Nineveh 发掘报告（Layard 等）/《剑桥古代史》卷 3",
    "巴比伦": "Babylon 发掘（Koldewey）/ 汉谟拉比法典石碑",
    "乌鲁克": "Uruk-Warka 发掘报告（德国考古研究所）",
    "乌尔": "Woolley《Ur Excavations》卷 2 / 乌尔纳姆法典",
    "尼普尔": "Nippur 发掘报告（宾夕法尼亚大学）",
    "埃布拉": "Ebla 档案（Matthiah 等）/ 罗马大学发掘报告",
    "马里": "Mari 王宫档案（ARM 系列）/ Parrot 发掘报告",
    "开罗": "《剑桥埃及史》/ Ibn Iyas《历代奇事》",
    "孟菲斯": "Memphis 发掘报告（埃及文物最高委员会）",
    "底比斯": "《牛津古埃及史》/ 底比斯墓葬测绘（MMA）",
    "亚历山大港": "Fraser《托勒密时期的亚历山大》",
    "耶路撒冷": "约瑟夫斯《犹太战记》/《新编考古百科全书》",
    "大马士革": "《剑桥伊斯兰史》卷 1 / Ibn ʿAsākir《大马士革史》",
    "阿勒颇": "《剑桥伊斯兰史》卷 1 / Ibn al-ʿAdim",
    "安条克": "Libanius 与《安条克志》/ Downey《安条克史》",
    "推罗": "希罗多德 ii.44 / 亚历山大的推罗围城（阿里安 ii）",
    "西顿": "《剑桥古代史》卷 4 / Eshmunazar 石棺铭文",
    "尼科米底亚": "《剑桥古代史》卷 8 / TIB（Bithynia）",
    "尼西亚": "Akropolites《编年史》/ TIB",
    "特拉布宗": "Ostrogorsky / Bryer《特拉布宗帝国》",
    "科尼亚": "Ibn Bibi《塞尔柱史》/ Cahen",
    "锡瓦斯": "《剑桥土耳其史》/ Evliya Çelebi《游记》",
    "安卡拉": "Zürcher《现代土耳其史》/ Evliya Çelebi",
    "布尔萨": "奥斯曼早期铭文 /《剑桥土耳其史》",
    "伊斯坦布尔": "Zürcher / TDV《伊斯兰百科全书》（DİA）",
    "埃德萨": "《剑桥古代史》卷 12 / Segal《埃德萨》",
    "哈兰": "《剑桥古代史》卷 3 / 哈兰月神庙铭文",
    "帕尔米拉": "Palmyra 铭文集成（PAT）/《剑桥古代史》卷 12",
    "苏萨": "Susa 发掘报告（de Morgan、Ghirshman）/ 汉谟拉比法典出土记录",
    "泰西封": "《剑桥伊朗史》卷 3 / Ctesiphon 发掘",
}

SITE_SOURCE_BY_ERA = {
    "dawn": "《剑桥古代史》卷 1 / 《牛津古埃及史》",
    "hittite": "Bryce《赫梯王国》/ 土耳其文化遗产名录",
    "post_hittite": "《剑桥古代史》卷 3 / 土耳其文化遗产名录",
    "lydia": "希罗多德《历史》/《剑桥古代史》卷 4",
    "achaemenid": "Briant《从居鲁士到亚历山大》",
    "alexander": "阿里安《远征记》",
    "diadochi": "狄奥多罗斯《历史丛书》卷 18—20",
    "hellenistic": "《剑桥古代史》卷 7—8",
    "roman_conquest": "《剑桥古代史》卷 9—10 / Magie",
    "roman_empire": "《巴林顿希腊罗马世界地图集》/ Magie《罗马统治下的小亚细亚》",
    "byzantine": "Tabula Imperii Byzantini / Ostrogorsky《拜占庭国家史》",
    "seljuk": "Cahen《奥斯曼以前土耳其的史前史》/《剑桥土耳其史》",
    "mongol": "拉施特《史集》/《剑桥伊朗史》卷 5",
    "beylik": "《剑桥土耳其史》/ 威尼斯档案",
    "ottoman": "TDV《伊斯兰百科全书》(DİA) / Evliya Çelebi《游记》",
    "ottoman_late": "Zürcher《现代土耳其史》",
    "republic": "Zürcher《现代土耳其史》",
}


def attach_settlement_sources():
    """给每个聚落补出处：先查逐个遗址表，再退到所属时代书目（幂等）"""
    for era in CONTENT:
        key = era["key"]
        default = SITE_SOURCE_BY_ERA.get(key, "《剑桥古代史》")
        for s in era.get("settlements") or []:
            if s.get("source"):
                continue
            s["source"] = SITE_SOURCE.get(s["ancient"], default)

def merge_extra_settlements():
    """把 EXTRA_SETTLEMENTS 并入 CONTENT 各时代的 settlements（幂等）"""
    global _extra_settle_merged
    if _extra_settle_merged:
        return
    for era in CONTENT:
        add = EXTRA_SETTLEMENTS.get(era["key"]) or []
        cur = era.setdefault("settlements", [])
        have = {d["ancient"] for d in cur}
        for d in add:
            if d["ancient"] not in have:
                cur.append(d)
                have.add(d["ancient"])
    _extra_settle_merged = True


merge_extra_settlements()


def attach_details():
    """把 MILESTONE_DETAIL 挂到各内容的 milestones 上"""
    for c in CONTENT:
        extra = (EXTRA_MILESTONES.get(c["key"]) or []) + (EXTRA_MILESTONES_2.get(c["key"]) or [])
        if extra:
            merged = list(c.get("milestones", []))
            seen = {m["year"] for m in merged}
            for x in extra:
                if x["year"] in seen:
                    continue
                merged.append(dict(x))
                seen.add(x["year"])
            c["milestones"] = sorted(merged, key=lambda m: m["year"])
        for m in c.get("milestones", []):
            hit = MILESTONE_DETAIL.get(f"{c['key']}:{m['year']}")
            if hit:
                m["detail"], m["source"] = hit


def main():
    attach_details()
    # 复用 gen_atlas 的 note 作为 summary
    import importlib.util
    spec = importlib.util.spec_from_file_location("ga", os.path.join(ROOT, "_build", "gen_atlas.py"))
    ga = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ga)
    for per in ga.PERIODS:
        SUMMARY[per["key"]] = per["note"]

    dyn = build_map_data()
    js = ("window.DYNASTY_DATA = [\n" +
          ",\n".join("  " + json.dumps(d, ensure_ascii=False) for d in dyn) +
          "\n];\n\nwindow.CORRIDOR_DATA = [\n" +
          ",\n".join("  " + json.dumps(c, ensure_ascii=False) for c in CORRIDORS) +
          "\n];\n")
    open(os.path.join(ROOT, "js", "map_data.js"), "w", encoding="utf-8").write(js)
    print(f"js/map_data.js 写入 {len(dyn)} 个时期 / {len(CORRIDORS)} 条古道")

    # 史料出处
    os.makedirs(os.path.join(ROOT, "data", "sources"), exist_ok=True)
    for k, refs in SOURCES.items():
        out = {
            "period": k,
            "note": "本时期史事与地名归属的参考出处（学术著作与原始史料）。边界为近似示意，不代表测绘边界。",
            "references": [{"citation": r} for r in refs],
        }
        json.dump(out, open(os.path.join(ROOT, "data", "sources", f"{k}.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
    print(f"data/sources/ 写入 {len(SOURCES)} 个时期共 {sum(len(v) for v in SOURCES.values())} 条引用")


if __name__ == "__main__":
    main()


merge_extra_settlements()
attach_settlement_sources()
