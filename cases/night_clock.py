"""Case 01 data: edit this file to change the story without touching the GUI."""

from copy import deepcopy

CASE = {
    "id": "night-clock",
    "number": "案件 · 01",
    "title": "午夜钟声疑案",
    "subtitle": "斯图尔特庄园的克拉拉.斯图尔特夫人被发现死在钟塔中。生前的一周她和财务主管维克多黑尔在调查一起异常的财务失窃事件。",
    "cover": "assets/ui/greedy_guilty.png",
    "locations": [
        {
            "id": "lobby",
            "code": "地点 / 01",
            "name": "庄园门厅",
            "meta": "门禁记录与访客簿",
            "title": "雨夜不会说谎",
            "description": "暴雨在 20:00 后开始。门厅的黄铜门禁读卡器仍记录着每一张刷过的工作卡。",
            "background": "assets/cases/night-clock/locations/lobby.png",
            "evidence": ["access-log", "guest-book-blotter", "umbrella-paint-fleck"],
            "testimonies": ["andrew-claim"],
            "timeline": "20:18 安德鲁的工作卡打开了档案室侧门。",
        },
        {
            "id": "tower",
            "code": "地点 / 02",
            "name": "钟楼",
            "meta": "停摆的古董钟",
            "title": "停在 20:14",
            "description": "克拉拉倒在钟楼顶层。有人故意锁死摆锤，控制柜上还留着新鲜的钟表油。",
            "background": "assets/cases/night-clock/locations/tower.png",
            "evidence": ["stopped-clock", "oil-smear", "tourist-coin", "maintenance-route-sketch"],
            "testimonies": ["elena-claim"],
            "timeline": "20:14 古董钟停摆；最后签领应急钥匙的人是钟表匠。",
        },
        {
            "id": "archive",
            "code": "地点 / 03",
            "name": "西侧档案室",
            "meta": "被翻找过的信件",
            "title": "撕碎的警告",
            "description": "第三个档案抽屉被翻开。克拉拉写给董事会的信件碎片散落在地，湿墨迹仍清晰可见。",
            "background": "assets/cases/night-clock/locations/archive.png",
            "evidence": ["warning-letter", "key-register", "dinner-place-card", "repair-invoice-copy"],
            "testimonies": ["marco-claim"],
            "timeline": "20:20 克拉拉的信被撕碎，内容提到伪造的修复工程账目。",
        },
        {
            "id": "garden",
            "code": "地点 / 04",
            "name": "玻璃花房",
            "meta": "温室与足迹",
            "title": "离开现场的痕迹",
            "description": "一串蓝色油漆脚印从玻璃花房延伸向钟楼，沿着只有员工使用的维修通道前进。",
            "background": "assets/cases/night-clock/locations/garden.png",
            "evidence": ["blue-footprint", "rain-soaked-glove", "gatehouse-umbrella-tag"],
            "testimonies": [],
            "timeline": "20:25 蓝色油漆脚印从钟楼通向西侧走廊。",
        },
        {
            "id": "corridor",
            "code": "地点 / 05",
            "name": "员工走廊",
            "meta": "洗衣记录与服务门",
            "title": "最狭窄的不在场证明",
            "description": "员工走廊连接档案室、钟楼楼梯和旧洗衣房。嗡鸣的服务灯下，留着考勤板与一件被丢下的维修围裙。",
            "background": "assets/cases/night-clock/locations/corridor.png",
            "evidence": ["laundry-ticket", "staff-supper-menu", "service-passage-keyring"],
            "testimonies": ["naomi-claim"],
            "timeline": "20:19 洗衣票记录了安德鲁沾有钟表油的维修围裙出现在员工走廊。",
        },
        {
            "id": "boathouse",
            "code": "地点 / 06",
            "name": "旧船屋",
            "meta": "财务账册与上锁的寄送箱",
            "title": "甲板下的账目",
            "description": "修缮期间，庄园旧档案被移到船屋。雨点敲打屋顶，一只寄送箱里放着克拉拉准备寄往董事会的付款记录副本。",
            "background": "assets/cases/night-clock/locations/boathouse.png",
            "evidence": ["transfer-ledger", "fishing-lease", "waterproof-envelope"],
            "testimonies": ["victor-claim"],
            "timeline": "20:22 一笔带有安德鲁审批的修复款转账被抄录进董事会寄送账册。",
        },
    ],
    "evidence": [
        {"id": "access-log", "icon": "⌁", "name": "侧门门禁记录", "detail": "20:18，安德鲁的工作卡打开了档案室侧门。", "kind": "case"},
        {"id": "guest-book-blotter", "icon": "✎", "name": "访客簿吸墨纸", "detail": "数名客人在暴雨前签到。湿墨迹与晚餐时间一致，不能改变任何人的不在场证明。", "kind": "distractor"},
        {
            "id": "umbrella-paint-fleck",
            "icon": "◈",
            "name": "伞钩上的蓝色油漆点",
            "partial_detail": "伞钩上有一小点钴蓝色油漆。它可能只是旧装饰，也可能来自别处。",
            "connection_detail": "玻璃花房也有同一种罕见的钴蓝色维修油漆。这证明有人走过员工路线，却无法指认是谁。",
            "related_location": "garden",
            "kind": "cross-scene",
        },
        {"id": "stopped-clock", "icon": "◷", "name": "停摆的摆锤", "detail": "应急钥匙在 20:14 锁死了古董钟。", "kind": "case"},
        {"id": "oil-smear", "icon": "◉", "name": "黑色油痕", "detail": "控制柜上的钟表油与安德鲁手套上的油痕一致。", "kind": "case"},
        {"id": "tourist-coin", "icon": "◌", "name": "钟楼纪念币", "detail": "栏杆后卡着一枚纪念币，属于 2019 年游客套装，与这场雨夜案件无关。", "kind": "distractor"},
        {
            "id": "maintenance-route-sketch",
            "icon": "⌁",
            "name": "折叠的维修路线图",
            "partial_detail": "一张带油渍的草图画着通往西侧的窄道，终点被水渍遮住了。",
            "connection_detail": "玻璃花房的足迹补全了这条路线：它连接钟楼与西侧走廊。该路线对员工开放，只能缩小机会范围，无法证明身份。",
            "related_location": "garden",
            "kind": "cross-scene",
        },
        {"id": "warning-letter", "icon": "✉", "name": "警告信碎片", "detail": "克拉拉计划举报伪造修复工程账目的人。", "kind": "case"},
        {"id": "key-register", "icon": "⌘", "name": "应急钥匙登记册", "detail": "那晚，只有安德鲁签领过钟楼应急钥匙。", "kind": "case"},
        {"id": "dinner-place-card", "icon": "◇", "name": "晚餐席位卡", "detail": "马可的席位卡上有头道菜留下的酒渍，只能证明他出席了晚餐。", "kind": "distractor"},
        {
            "id": "repair-invoice-copy",
            "icon": "▤",
            "name": "被丢弃的维修发票",
            "partial_detail": "一张复写件列出了钟楼维修工具包。签名模糊，日期本身不能将它与破坏行为联系起来。",
            "connection_detail": "钟楼控制柜使用同一维修工具包编号。发票只证明有人日常接触材料，不能证明其在案发时使用过。",
            "related_location": "tower",
            "kind": "cross-scene",
        },
        {"id": "blue-footprint", "icon": "◒", "name": "蓝色油漆脚印", "detail": "这串足迹经过一条仅供员工使用的维修通道。", "kind": "case"},
        {"id": "rain-soaked-glove", "icon": "⌁", "name": "被雨浸湿的园艺手套", "detail": "手套陈旧、无标记，存放在公用雨具中，无法与任何嫌疑人对应。", "kind": "distractor"},
        {
            "id": "gatehouse-umbrella-tag",
            "icon": "▱",
            "name": "雨伞寄存标签",
            "partial_detail": "一张写着“门厅伞架”的标签卡在花房长椅下。它证明有把雨伞被移动过，却不能证明是谁拿走的。",
            "connection_detail": "标签与门厅伞钩及其钴蓝色油漆点相互对应。它们共同显示两处场景之间存在路线，但持伞者仍未知。",
            "related_location": "lobby",
            "kind": "cross-scene",
        },
        {"id": "laundry-ticket", "icon": "▣", "name": "沾油的洗衣票", "detail": "20:19，一张洗衣票记录安德鲁沾雨的维修围裙出现在员工走廊。这与他从未离开钟楼的说法不符。", "kind": "case"},
        {"id": "staff-supper-menu", "icon": "≡", "name": "员工晚餐菜单", "detail": "菜单显示 19:45 供应汤和面包，无法证明暴雨开始后任何人在何处。", "kind": "distractor"},
        {
            "id": "service-passage-keyring",
            "icon": "⌘",
            "name": "服务通道钥匙圈",
            "partial_detail": "备用钥匙圈上挂着褪色的“归还钟楼”标签。其压印时间过早，不能证明当晚是谁携带。",
            "connection_detail": "钟楼维修路线图确认这串钥匙属于西侧服务路线。它证明路线可用，却不能证明案发时谁走过。",
            "related_location": "tower",
            "kind": "cross-scene",
        },
        {"id": "transfer-ledger", "icon": "▤", "name": "修复款转账账册", "detail": "董事会寄送副本记录：安德鲁审批过一笔汇往虚构“哈罗与芬奇修复公司”账户的款项。", "kind": "case"},
        {"id": "fishing-lease", "icon": "⚓", "name": "过期捕鱼租约", "detail": "这份租约三年前已过期，登记的租客案发当晚在国外。", "kind": "distractor"},
        {
            "id": "waterproof-envelope",
            "icon": "✉",
            "name": "防水董事会信封",
            "partial_detail": "密封信封写给董事会，但附件不在其中。编号可能与庄园别处的文件匹配。",
            "connection_detail": "档案室的信件碎片与信封编号一致。克拉拉确实在准备正式举报，这强化了财务动机，却不能将任何人放到钟楼。",
            "related_location": "archive",
            "kind": "cross-scene",
        },
    ],
    "testimonies": [
        {"id": "andrew-claim", "person": "安德鲁·魏", "role": "钟表匠", "text": "“从 20:00 到 20:25，我一直在钟楼修钟，从未离开。”", "portrait": "assets/cases/night-clock/portraits/andrew.png"},
        {"id": "elena-claim", "person": "艾琳娜·朴", "role": "园丁", "text": "“我在玻璃花房整理雨具时，听见了钟声停下。”", "portrait": "assets/cases/night-clock/portraits/elena.png"},
        {"id": "marco-claim", "person": "马可·陈", "role": "档案研究员", "text": "“晚餐后，克拉拉打算给董事会寄一封信。”", "portrait": "assets/cases/night-clock/portraits/marco.png"},
        {"id": "naomi-claim", "person": "娜奥米·贝尔", "role": "管家", "text": "“大约 20:19，我看见安德鲁没穿维修围裙站在员工走廊。他说钟楼太冷，没法干活。”", "portrait": "assets/cases/night-clock/portraits/naomi.png"},
        {"id": "victor-claim", "person": "维克多·黑尔", "role": "庄园财务主管", "text": "“安德鲁无权审批修复款，只有我的办公室处理这些账目。”", "portrait": "assets/cases/night-clock/portraits/victor.png"},
    ],
    "suspects": [
        {"id": "andrew", "name": "安德鲁·魏"},
        {"id": "elena", "name": "艾琳娜·朴"},
        {"id": "marco", "name": "马可·陈"},
        {"id": "naomi", "name": "娜奥米·贝尔"},
        {"id": "victor", "name": "维克多·黑尔"},
    ],
    "reasoning_rules": [
        {
            "id": "andrew-alibi",
            "statement": "andrew-claim",
            "evidence": "access-log",
            "outcome": "contradiction",
            "message": "发现矛盾：安德鲁称自己在 20:00 至 20:25 从未离开钟楼，但门禁记录证明他在 20:18 打开了档案室侧门。两者不可能同时为真；他的虚假时间线已被记录。",
        },
        {
            "statement": "andrew-claim",
            "evidence": "key-register",
            "outcome": "related",
            "message": "高度相关，但单独不足以构成矛盾：登记册只能证明安德鲁能够进入钟楼，不能证明他未曾离开。请将完整时间线与门禁记录比对。",
        },
        {
            "id": "andrew-alibi",
            "statement": "andrew-claim",
            "evidence": "laundry-ticket",
            "outcome": "contradiction",
            "message": "发现矛盾：20:19 的洗衣票显示安德鲁沾雨的维修围裙出现在员工走廊，而他声称从未离开钟楼。这张票独立推翻了他的时间线。",
        },
        {
            "statement": "marco-claim",
            "evidence": "warning-letter",
            "outcome": "confirmed",
            "message": "已印证：信件碎片支持马可关于致信董事会的说法。这不是矛盾。",
        },
        {
            "statement": "elena-claim",
            "evidence": "stopped-clock",
            "outcome": "confirmed",
            "message": "已印证：记录中的停摆时间与艾琳娜听见钟声停止的说法一致。",
        },
        {
            "id": "victor-accounting",
            "statement": "victor-claim",
            "evidence": "transfer-ledger",
            "outcome": "contradiction",
            "message": "发现矛盾：董事会寄送副本带有安德鲁的付款审批。维克多关于账目权限的说法不实，但这本身不能证明维克多犯下谋杀。",
        },
    ],
    "fallback_reasoning": "证据不足：这些事实尚未直接冲突。寻找能独立证明某人在何时、何地或是否离开的记录。",
    "final_accusation": {
        "culprit": "andrew",
        "required_evidence": ["access-log", "stopped-clock", "oil-smear", "warning-letter", "key-register", "blue-footprint", "laundry-ticket", "transfer-ledger"],
        "required_contradictions": ["andrew-alibi"],
        "success": "案件告破：安德鲁·魏。门禁记录与洗衣票推翻了他的不在场证明；应急钥匙和油痕证明他有进入钟楼并破坏摆钟的手段；警告信与转账账册则证明他有掩盖伪造账目的动机。证据链已满足结案条件。",
        "failure": "现有证据链不支持这项指控。已证实的时间线矛盾、钟楼钥匙、油痕与欺诈转账都指向安德鲁。请重新审视事实。",
    },
}


# The investigation rules and asset paths are language-neutral.  The English
# case is a deep copy so both versions keep the same ids and game logic.
CASE_EN = deepcopy(CASE)
CASE_EN.update(
    {
        "number": "CASE · 01",
        "title": "The Midnight Chime",
        "subtitle": "Clara Stuart is found dead in the manor clock tower. In the week before her death, she and finance manager Victor Hale had been investigating suspicious restoration payments.",
    }
)

_LOCATION_EN = {
    "lobby": {
        "code": "LOCATION / 01",
        "name": "Manor Foyer",
        "meta": "Access records and visitor log",
        "title": "Rain Does Not Lie",
        "description": "The downpour began after 20:00. The foyer's brass access reader still records every staff card that passed through it.",
        "timeline": "20:18 Andrew's work card opened the archive side door.",
    },
    "tower": {
        "code": "LOCATION / 02",
        "name": "Clock Tower",
        "meta": "A stopped antique clock",
        "title": "Stopped at 20:14",
        "description": "Clara lies on the tower's upper floor. Someone deliberately locked the pendulum, and fresh clock oil remains on the control cabinet.",
        "timeline": "20:14 The antique clock stopped; the clockmaker was the last person to sign out the emergency key.",
    },
    "archive": {
        "code": "LOCATION / 03",
        "name": "West Archive",
        "meta": "Letters searched and torn apart",
        "title": "A Torn Warning",
        "description": "The third archive drawer has been searched. Fragments of Clara's letter to the board lie on the floor, their wet ink still legible.",
        "timeline": "20:20 Clara's letter was torn apart; it mentioned forged restoration accounts.",
    },
    "garden": {
        "code": "LOCATION / 04",
        "name": "Glasshouse",
        "meta": "Greenhouse and footprints",
        "title": "Tracks Leaving the Scene",
        "description": "A trail of blue paint footprints leads from the glasshouse toward the clock tower by a maintenance route reserved for staff.",
        "timeline": "20:25 Blue paint footprints lead from the tower toward the west corridor.",
    },
    "corridor": {
        "code": "LOCATION / 05",
        "name": "Staff Corridor",
        "meta": "Laundry record and service door",
        "title": "The Narrowest Alibi",
        "description": "The staff corridor links the archive, tower stairs, and old laundry. Beneath its humming service light sit an attendance board and an abandoned repair apron.",
        "timeline": "20:19 A laundry ticket records Andrew's clock-oil-stained repair apron in the staff corridor.",
    },
    "boathouse": {
        "code": "LOCATION / 06",
        "name": "Old Boathouse",
        "meta": "Financial ledger and locked dispatch box",
        "title": "Accounts Beneath the Deck",
        "description": "During restoration, the manor's old files were moved to the boathouse. A dispatch box holds copies of the payment records Clara planned to send to the board.",
        "timeline": "20:22 A restoration transfer approved by Andrew was copied into the board dispatch ledger.",
    },
}

_EVIDENCE_EN = {
    "access-log": {"name": "Side-door access log", "detail": "At 20:18, Andrew's work card opened the archive side door."},
    "guest-book-blotter": {"name": "Visitor-log blotter", "detail": "Several guests signed in before the downpour. The wet ink matches dinner time and cannot change anyone's alibi."},
    "umbrella-paint-fleck": {
        "name": "Blue paint fleck on umbrella hook",
        "partial_detail": "A tiny fleck of cobalt-blue paint sits on the umbrella hook. It may be old decoration or may have come from elsewhere.",
        "connection_detail": "The glasshouse contains the same rare cobalt-blue maintenance paint. This proves someone used the staff route, but not who it was.",
    },
    "stopped-clock": {"name": "Stopped pendulum", "detail": "The emergency key locked the antique clock at 20:14."},
    "oil-smear": {"name": "Black oil smear", "detail": "The clock oil on the control cabinet matches the oil marks on Andrew's gloves."},
    "tourist-coin": {"name": "Clock-tower souvenir coin", "detail": "A souvenir coin from a 2019 visitor set is caught behind the railing; it has nothing to do with this rainy-night case."},
    "maintenance-route-sketch": {
        "name": "Folded maintenance-route sketch",
        "partial_detail": "An oil-stained sketch shows a narrow westbound passage, but water damage hides its destination.",
        "connection_detail": "The glasshouse footprints complete the route: it links the tower and west corridor. Staff could use it, but it cannot identify the user.",
    },
    "warning-letter": {"name": "Warning-letter fragments", "detail": "Clara intended to report whoever forged the restoration accounts."},
    "key-register": {"name": "Emergency-key register", "detail": "Only Andrew signed out the clock-tower emergency key that night."},
    "dinner-place-card": {"name": "Dinner place card", "detail": "Marco's place card bears a wine stain from the first course, proving only that he attended dinner."},
    "repair-invoice-copy": {
        "name": "Discarded repair invoice",
        "partial_detail": "A carbon copy lists a clock-tower repair toolkit. The signature is blurred, and its date alone cannot tie it to sabotage.",
        "connection_detail": "The tower cabinet uses the same toolkit number. The invoice proves routine access to materials, not their use at the time of the crime.",
    },
    "blue-footprint": {"name": "Blue paint footprints", "detail": "The trail crosses a maintenance route used only by staff."},
    "rain-soaked-glove": {"name": "Rain-soaked gardening glove", "detail": "The glove is old, unmarked, and stored with shared rain gear; it cannot be connected to a suspect."},
    "gatehouse-umbrella-tag": {
        "name": "Umbrella-storage tag",
        "partial_detail": "A tag reading 'foyer umbrella stand' is caught beneath a glasshouse bench. It proves an umbrella moved, not who moved it.",
        "connection_detail": "The tag matches the foyer hook and its cobalt-blue paint fleck. Together they show a route between scenes, but the umbrella carrier remains unknown.",
    },
    "laundry-ticket": {"name": "Oil-stained laundry ticket", "detail": "At 20:19, a laundry ticket records Andrew's rain-spattered repair apron in the staff corridor. That conflicts with his claim that he never left the tower."},
    "staff-supper-menu": {"name": "Staff supper menu", "detail": "The menu shows soup and bread served at 19:45; it cannot prove where anyone was after the rain began."},
    "service-passage-keyring": {
        "name": "Service-passage keyring",
        "partial_detail": "A spare keyring bears a faded 'return to tower' tag. Its old stamp cannot show who carried it that night.",
        "connection_detail": "The tower route sketch confirms these keys served the west-side route. They prove the route was available, not who used it at the time.",
    },
    "transfer-ledger": {"name": "Restoration-transfer ledger", "detail": "The board dispatch copy records Andrew approving a payment to the fictitious 'Harrow & Finch Restoration Company' account."},
    "fishing-lease": {"name": "Expired fishing lease", "detail": "This lease expired three years ago, and its listed tenant was overseas on the night of the murder."},
    "waterproof-envelope": {
        "name": "Waterproof board envelope",
        "partial_detail": "The sealed envelope is addressed to the board, but its enclosure is missing. Its number may match a document elsewhere in the manor.",
        "connection_detail": "The archive fragments share the envelope number. Clara was preparing a formal report, strengthening a financial motive without placing anyone in the tower.",
    },
}

_TESTIMONY_EN = {
    "andrew-claim": {"person": "Andrew Wei", "role": "Clockmaker", "text": "“From 20:00 to 20:25, I was repairing the clock tower and never left.”"},
    "elena-claim": {"person": "Elena Park", "role": "Gardener", "text": "“While I was sorting rain gear in the glasshouse, I heard the clock stop.”"},
    "marco-claim": {"person": "Marco Chen", "role": "Archive researcher", "text": "“After dinner, Clara planned to send a letter to the board.”"},
    "naomi-claim": {"person": "Naomi Bell", "role": "Housekeeper", "text": "“At about 20:19, I saw Andrew in the staff corridor without his repair apron. He said the tower was too cold to work in.”"},
    "victor-claim": {"person": "Victor Hale", "role": "Manor finance manager", "text": "“Andrew had no authority to approve restoration payments; only my office handled those accounts.”"},
}

for location in CASE_EN["locations"]:
    location.update(_LOCATION_EN[location["id"]])
for evidence in CASE_EN["evidence"]:
    evidence.update(_EVIDENCE_EN[evidence["id"]])
for testimony in CASE_EN["testimonies"]:
    testimony.update(_TESTIMONY_EN[testimony["id"]])

for suspect, name in zip(CASE_EN["suspects"], ("Andrew Wei", "Elena Park", "Marco Chen", "Naomi Bell", "Victor Hale")):
    suspect["name"] = name

for rule, message in zip(
    CASE_EN["reasoning_rules"],
    (
        "Contradiction found: Andrew says he never left the clock tower between 20:00 and 20:25, but the access log proves he opened the archive side door at 20:18. Both cannot be true; his false timeline is now recorded.",
        "Highly relevant, but not a contradiction by itself: the register proves Andrew could enter the tower, not that he never left it. Compare the full timeline with the access record.",
        "Contradiction found: the 20:19 laundry ticket places Andrew's rain-spattered repair apron in the staff corridor, while he says he never left the tower. This independent record disproves his timeline.",
        "Confirmed: the letter fragments support Marco's account that Clara intended to write to the board. This is not a contradiction.",
        "Confirmed: the recorded stopping time matches Elena's account of hearing the clock fall silent.",
        "Contradiction found: the board dispatch copy bears Andrew's payment approval. Victor's claim about account authority is false, though it does not by itself prove he committed the murder.",
    ),
):
    rule["message"] = message

CASE_EN["fallback_reasoning"] = "Insufficient evidence: these facts do not directly conflict. Find records that independently establish where someone was, when they were there, or whether they left."
CASE_EN["final_accusation"].update(
    {
        "success": "Case solved: Andrew Wei. The access log and laundry ticket disprove his alibi; the emergency key and oil smear show he had the means to enter the tower and sabotage the clock; the warning letter and transfer ledger establish his motive to conceal forged accounts. The evidence chain meets the conditions for closure.",
        "failure": "The current evidence chain does not support this accusation. The verified timeline contradiction, tower key, oil smear, and fraudulent transfer all point to Andrew. Re-examine the facts.",
    }
)


def case_for_language(language: str) -> dict:
    """Return the Chinese or English presentation of Case 01."""
    return CASE_EN if language == "en" else CASE
