"""
서은주 선생님의 80년 - 생명 존중 게임 (Streamlit 버전)
"""
import time
import random
import streamlit as st

# ============================================================
# 게임 상수
# ============================================================
YEARS_PER_TURN = 5
MAX_AGE = 80
TOTAL_TURNS = MAX_AGE // YEARS_PER_TURN

CRISIS_CHANCE = 0.22
GOOD_EVENT_CHANCE = 0.35

STAT_EMOJI = {"영양": "🍚", "건강": "💊", "안전": "🌡️", "수면": "😴"}

ACTIONS = {
    "1": {"name": "🍚 밥·물 챙기기", "stat": "영양", "amount": 35, "full": False},
    "2": {"name": "💊 건강 관리",     "stat": "건강", "amount": 30, "full": False},
    "3": {"name": "🌡️ 안전 보호",    "stat": "안전", "amount": 30, "full": False},
    "4": {"name": "😴 푹 재우기",    "stat": "수면", "amount": 70, "full": True},
}

STAGE_DECAY = {
    "유년기":   {"영양": 15, "건강": 10, "안전": 10, "수면": 20, "생명력": 0},
    "학창시절": {"영양": 15, "건강": 10, "안전": 15, "수면": 25, "생명력": 0},
    "중년":     {"영양": 20, "건강": 15, "안전": 15, "수면": 25, "생명력": 0},
    "노년":     {"영양": 25, "건강": 20, "안전": 20, "수면": 25, "생명력": 5},
    "황혼기":   {"영양": 30, "건강": 25, "안전": 25, "수면": 30, "생명력": 10},
}

# 단계별 잘못된 선택의 음수 효과 배율
STAGE_SEVERITY = {
    "유년기": 1.0, "학창시절": 1.3, "중년": 1.6, "노년": 2.0, "황혼기": 2.5,
}

GOOD_EVENTS_BY_STAGE = {
    "유년기": [
        "🌸 봄날 친구들과 신나게 뛰어 놀았어요!",
        "🎠 놀이터에서 즐거운 하루를 보냈어요!",
        "🍭 선생님께 사탕을 받았어요!",
        "🌙 달콤한 꿈을 꿨어요.",
        "🎨 그림 그리기 시간이 너무 재밌었어요!",
        "🐶 귀여운 강아지를 만났어요!",
        "🎂 친구 생일 파티에 초대받았어요!",
    ],
    "학창시절": [
        "🌸 따뜻한 봄날, 기분이 좋아 보여요.",
        "👏 선생님께 칭찬을 받았어요!",
        "📝 시험에서 좋은 점수를 받았어요!",
        "👫 친구들과 즐거운 방과 후를 보냈어요.",
        "🌙 좋은 꿈을 꿨어요.",
        "🎵 좋아하는 음악을 실컷 들었어요.",
        "🎂 친구들이 깜짝 파티를 열어줬어요!",
    ],
    "중년": [
        "👏 학생들에게 감사 인사를 받았어요!",
        "☕ 좋아하는 커피를 마셨어요.",
        "🌸 따뜻한 봄날, 기분이 좋아 보여요.",
        "🌙 오랜만에 푹 잤어요.",
        "📚 좋은 책을 읽었어요.",
        "🚶 가벼운 산책으로 기분이 좋아졌어요.",
        "🎂 동료들과 작은 파티를 했어요.",
    ],
    "노년": [
        "🌸 따뜻한 봄날, 기분이 좋아 보여요.",
        "☕ 좋아하는 커피를 천천히 즐겼어요.",
        "🎁 옛 제자가 찾아와 선물을 줬어요.",
        "🌙 오랜만에 꿀잠을 잤어요.",
        "📚 좋은 책을 읽었어요.",
        "🚶 공원 산책이 너무 좋았어요.",
        "👨‍👩‍👧 가족들과 즐거운 시간을 보냈어요.",
    ],
    "황혼기": [
        "🌸 창가에 따뜻한 햇살이 들었어요.",
        "☕ 따뜻한 차를 마시며 여유를 즐겼어요.",
        "🌙 오랜만에 아주 깊이 잘 잤어요.",
        "📷 오래된 사진을 꺼내 추억을 떠올렸어요.",
        "👨‍👩‍👧 가족이 찾아와 함께 시간을 보냈어요.",
        "🌻 마당의 꽃이 활짝 피었어요.",
        "🎶 오래된 노래를 들으며 미소 지었어요.",
    ],
}

STAGE_BG = {
    "유년기":   "#FFF4E6",
    "학창시절": "#E6F7FF",
    "중년":     "#F0F0F0",
    "노년":     "#FFF0E6",
    "황혼기":   "#FFE6F0",
}

STAGE_DESC = {
    "유년기":   "세상이 온통 새롭고 신기한 시절이에요.",
    "학창시절": "꿈을 키우고 세상을 배워나가는 시절이에요.",
    "중년":     "인생의 무게를 지고 달려가는 시절이에요.",
    "노년":     "삶의 지혜가 깊어지는 시절이에요.",
    "황혼기":   "소중한 것들을 돌아보는 시절이에요.",
}

# ============================================================
# 게임 상태
# ============================================================
class GameState:
    def __init__(self):
        self.age = 0
        self.turn = 0
        self.alive = True
        self.stats = {"영양": 80, "건강": 80, "안전": 80, "수면": 80}
        self.life = 100
        self.stat_care_count = {"영양": 0, "건강": 0, "안전": 0, "수면": 0}
        self.crisis_handled_well = 0
        self.crisis_failed = 0
        self.good_turns = 0
        self.bad_turns = 0
        self.death_cause = None

    def clamp(self):
        for k in self.stats:
            self.stats[k] = max(0, min(100, self.stats[k]))
        self.life = max(0, min(100, self.life))

    def snapshot(self):
        return {**self.stats, "생명력": self.life}


# ============================================================
# 위기 이벤트 - 공통 풀 (10개)
# ============================================================
def crisis_dizziness(state):
    non_sleep = sorted(
        [(s, v) for s, v in state.stats.items() if s != "수면"],
        key=lambda x: x[1],
    )
    lowest = non_sleep[0][0]
    options = [
        {
            "text": "밥과 물을 챙겨준다",
            "tier": "correct" if lowest == "영양" else "wrong",
            "effects": {"영양": 30} if lowest == "영양" else {"영양": 10, "건강": -20, "life": -15},
        },
        {
            "text": "푹 쉬게 한다",
            "tier": "correct" if state.stats["수면"] < 40 else "partial",
            "effects": {"수면": 30, "건강": 10},
        },
        {"text": "병원에 데려간다",       "tier": "partial", "effects": {"건강": 20}},
        {"text": "그냥 좀 누워있게 한다", "tier": "fatal",   "effects": {"건강": -30, "안전": -20, "life": -25}},
    ]
    return {
        "title": "😵‍💫 갑자기 어지러워해요!",
        "options": options,
        "explanation": {
            "correct": "정확히 원인을 짚었어요. 빠른 회복!",
            "partial": "도움은 됐지만 근본 원인은 아니었어요.",
            "wrong":   "엉뚱한 처방이었어요. 상태가 더 나빠졌어요.",
            "fatal":   "방치에 가까운 선택. 큰일날 뻔했어요.",
        },
    }


def crisis_stomach_ache(state):
    options = [
        {"text": "병원에 데려가서 진찰받게 한다",  "tier": "correct", "effects": {"건강": 30}},
        {"text": "따뜻한 차를 끓여준다",            "tier": "partial", "effects": {"건강": 10, "안전": 5}},
        {"text": "약장에서 아무 약이나 먹인다",     "tier": "wrong",   "effects": {"건강": -25, "life": -15}},
        {"text": "참으면 낫는다고 한다",            "tier": "fatal",   "effects": {"건강": -35, "영양": -15, "life": -25}},
    ]
    return {
        "title": "🤢 배가 너무 아프대요...",
        "options": options,
        "explanation": {
            "correct": "원인을 정확히 알아낸 게 큰 도움이었어요.",
            "partial": "잠시 완화는 됐지만 원인은 그대로였어요.",
            "wrong":   "엉뚱한 약을 먹어서 더 나빠졌어요!",
            "fatal":   "참기엔 너무 심한 통증이었어요...",
        },
    }


def crisis_cold_weather(state):
    options = [
        {"text": "따뜻한 옷·이불·난방을 차근차근 챙긴다", "tier": "correct", "effects": {"안전": 35, "건강": 5}},
        {"text": "두꺼운 옷만 입혀준다",                   "tier": "partial", "effects": {"안전": 15}},
        {"text": "뜨거운 물로 샤워하게 한다",              "tier": "wrong",   "effects": {"안전": -15, "건강": -20, "life": -15}},
        {"text": "곧 풀린다며 그냥 둔다",                  "tier": "fatal",   "effects": {"안전": -30, "건강": -20, "life": -25}},
    ]
    return {
        "title": "❄️ 한파 경보! 난방이 고장났어요!",
        "options": options,
        "explanation": {
            "correct": "차근차근 따뜻하게. 완벽한 대처였어요.",
            "partial": "추위는 막았지만 충분하진 않았어요.",
            "wrong":   "급격한 온도 변화는 오히려 몸에 무리예요!",
            "fatal":   "한파를 우습게 봤어요. 동상 위험까지...",
        },
    }


def crisis_fatigue(state):
    options = [
        {"text": "모든 일정을 미루고 푹 쉬게 한다",   "tier": "correct", "effects": {"수면": 40, "건강": 15}},
        {"text": "에너지 드링크를 마시게 한다",        "tier": "wrong",   "effects": {"수면": -20, "건강": -15, "life": -15}},
        {"text": "운동시켜서 활력을 준다",             "tier": "wrong",   "effects": {"수면": -15, "건강": -20, "life": -10}},
        {"text": "맛있는 거 먹이고 다시 일하게 한다",  "tier": "fatal",   "effects": {"영양": 5, "수면": -25, "건강": -25, "life": -20}},
    ]
    return {
        "title": "🥱 며칠째 잠을 거의 못 잤어요...",
        "options": options,
        "explanation": {
            "correct": "푹 쉬어서 완전히 회복했어요.",
            "partial": "일시적인 효과만 있었어요.",
            "wrong":   "오히려 더 피곤해졌어요. 카페인은 정답이 아니에요.",
            "fatal":   "혹사시켰어요. 정말 위험한 상태예요...",
        },
    }


def crisis_sadness(state):
    options = [
        {"text": "옆에 앉아 이야기를 끝까지 들어준다",  "tier": "correct",  "effects": {"건강": 20, "수면": 15}},
        {"text": "맛있는 음식을 만들어준다",             "tier": "partial",  "effects": {"영양": 15, "건강": 5}},
        {"text": "기분 전환하라며 밖으로 끌고 나간다",  "tier": "wrong",    "effects": {"건강": -15, "안전": -10, "life": -10}},
        {"text": "약한 모습 보이지 말라고 한다",         "tier": "fatal",    "effects": {"건강": -30, "수면": -20, "life": -25}},
    ]
    return {
        "title": "😢 깊은 슬픔에 빠져있어요...",
        "options": options,
        "explanation": {
            "correct": "들어주는 것만으로도 큰 위로가 됐어요.",
            "partial": "마음은 쓰셨지만, 정작 필요했던 건 따로 있었어요.",
            "wrong":   "본인의 시간이 필요했는데... 강요는 역효과였어요.",
            "fatal":   "가장 힘들 때 가장 큰 상처를 줬어요.",
        },
    }


def crisis_pain(state):
    options = [
        {"text": "즉시 병원에 가서 정밀 검사를 받게 한다", "tier": "correct",  "effects": {"건강": 30}},
        {"text": "찜질팩으로 통증 부위를 데워준다",         "tier": "partial",  "effects": {"건강": 10}},
        {"text": "진통제만 먹이고 지켜본다",                "tier": "wrong",    "effects": {"건강": -20, "life": -15}},
        {"text": "꾀병이라며 무시한다",                     "tier": "fatal",    "effects": {"건강": -35, "안전": -10, "life": -30}},
    ]
    return {
        "title": "😖 가슴이 답답하고 통증이 있대요",
        "options": options,
        "explanation": {
            "correct": "조기에 발견했어요. 정말 다행이에요.",
            "partial": "통증은 줄었지만 원인은 그대로...",
            "wrong":   "진통제로 가렸을 뿐, 병은 깊어졌어요.",
            "fatal":   "심각한 신호를 놓쳤어요. 큰일났어요...",
        },
    }


def crisis_heatstroke(state):
    options = [
        {"text": "서늘한 곳으로 이동시키고 물을 마시게 한다", "tier": "correct", "effects": {"안전": 30, "건강": 15, "영양": 10}},
        {"text": "찬물을 머리에 끼얹는다",                    "tier": "partial", "effects": {"안전": 15, "건강": 5}},
        {"text": "뜨거운 차를 마시게 해서 땀을 뺀다",         "tier": "wrong",   "effects": {"안전": -20, "건강": -25, "life": -20}},
        {"text": "그냥 그늘에서 쉬면 된다고 한다",            "tier": "fatal",   "effects": {"건강": -35, "안전": -20, "life": -30}},
    ]
    return {
        "title": "☀️ 야외에서 쓰러질 것 같아요! 열사병이에요!",
        "options": options,
        "explanation": {
            "correct": "빠른 냉각과 수분 보충이 열사병 응급처치의 핵심이에요.",
            "partial": "식히긴 했지만 수분 보충을 빠뜨렸어요.",
            "wrong":   "더운 음료는 체온을 더 올려요. 역효과가 났어요!",
            "fatal":   "열사병은 골든타임이 있어요. 방치는 위험해요...",
        },
    }


def crisis_dehydration(state):
    options = [
        {"text": "소금과 설탕을 탄 물을 조금씩 자주 마시게 한다", "tier": "correct", "effects": {"영양": 30, "건강": 15}},
        {"text": "이온 음료를 마시게 한다",                        "tier": "partial", "effects": {"영양": 20, "건강": 5}},
        {"text": "한 번에 물을 많이 마시게 한다",                  "tier": "wrong",   "effects": {"영양": 10, "건강": -20, "life": -15}},
        {"text": "조금 쉬면 괜찮아질 거라고 그냥 둔다",            "tier": "fatal",   "effects": {"영양": -20, "건강": -30, "life": -25}},
    ]
    return {
        "title": "💧 입술이 바짝 타고 어지러워해요. 탈수예요!",
        "options": options,
        "explanation": {
            "correct": "전해질 보충이 탈수 회복의 핵심이에요.",
            "partial": "이온 음료도 좋은 선택이에요.",
            "wrong":   "급하게 많이 마시면 저나트륨혈증이 올 수 있어요!",
            "fatal":   "탈수를 방치하면 의식을 잃을 수 있어요...",
        },
    }


def crisis_insomnia(state):
    options = [
        {"text": "규칙적인 수면 환경을 만들고 스트레스를 줄여준다", "tier": "correct", "effects": {"수면": 35, "건강": 10}},
        {"text": "수면제를 바로 처방받아 먹인다",                   "tier": "wrong",   "effects": {"수면": 15, "건강": -20, "life": -15}},
        {"text": "낮잠을 실컷 자게 한다",                           "tier": "wrong",   "effects": {"수면": -10, "건강": -15, "life": -10}},
        {"text": "밤을 새워 리듬을 리셋시킨다",                     "tier": "fatal",   "effects": {"수면": -30, "건강": -25, "life": -25}},
    ]
    return {
        "title": "🌙 며칠째 잠을 전혀 못 자고 있어요...",
        "options": options,
        "explanation": {
            "correct": "수면 위생 개선이 만성 불면의 근본 해결책이에요.",
            "partial": "일시적인 효과는 있었어요.",
            "wrong":   "수면제 의존과 낮잠은 밤 수면을 더 망가뜨려요.",
            "fatal":   "억지로 밤을 새우면 오히려 더 깊은 불면에 빠져요...",
        },
    }


def crisis_bradycardia(state):
    options = [
        {"text": "신경과에 가본다",     "tier": "wrong",   "effects": {"건강": -25, "안전": 10, "life": -15}},
        {"text": "신경외과에 가본다",   "tier": "fatal",   "effects": {"건강": -30, "수면": -30, "life": -25}},
        {"text": "순환기내과에 가본다", "tier": "correct", "effects": {"건강": 25, "안전": 10}},
        {"text": "흉부외과에 가본다",   "tier": "partial", "effects": {"건강": 15, "수면": 5}},
    ]
    return {
        "title": "💓 어지러움과 흉통이 있어요. 맥박이 너무 느려요!",
        "options": options,
        "explanation": {
            "correct": "서맥은 순환기내과 담당이에요. 정확한 선택!",
            "partial": "흉부외과도 도움은 됐지만 전문과는 아니에요.",
            "wrong":   "원인을 찾지 못해서 더 나빠졌어요...",
            "fatal":   "불필요한 검사를 받고 상태가 악화됐어요...",
        },
    }


CRISIS_FUNCTIONS = [
    crisis_dizziness, crisis_stomach_ache, crisis_cold_weather,
    crisis_fatigue, crisis_sadness, crisis_pain,
    crisis_heatstroke, crisis_dehydration, crisis_insomnia, crisis_bradycardia,
]

# ============================================================
# 나이별 위기 이벤트 (단계별 4개 = 20개)
# ============================================================

# ── 유년기 ──
def crisis_childhood_fever(state):
    options = [
        {"text": "해열제를 먹이고 미지근한 물수건으로 닦아준다", "tier": "correct", "effects": {"건강": 30, "안전": 10}},
        {"text": "두꺼운 이불을 덮어서 땀을 뺀다",              "tier": "wrong",   "effects": {"건강": -25, "life": -20}},
        {"text": "빨리 병원에 데려간다",                        "tier": "correct", "effects": {"건강": 25}},
        {"text": "자고 나면 낫겠지 하고 그냥 둔다",             "tier": "fatal",   "effects": {"건강": -35, "life": -30}},
    ]
    return {
        "title": "🤧 갑자기 열이 펄펄 나요!",
        "options": options,
        "explanation": {
            "correct": "빠르게 대처해서 금방 좋아졌어요.",
            "partial": "조금 나아졌지만 충분하진 않았어요.",
            "wrong":   "땀을 빼려다 오히려 열이 더 올랐어요!",
            "fatal":   "고열을 방치했어요. 심각한 상태가 됐어요...",
        },
    }


def crisis_childhood_injury(state):
    options = [
        {"text": "상처를 깨끗이 소독하고 병원에 간다",  "tier": "correct", "effects": {"안전": 30, "건강": 10}},
        {"text": "침으로 닦아주고 그냥 둔다",            "tier": "wrong",   "effects": {"안전": -20, "건강": -20, "life": -15}},
        {"text": "밴드만 붙여주고 지켜본다",             "tier": "partial", "effects": {"안전": 10}},
        {"text": "괜찮다고 달래고 신경 안 쓴다",         "tier": "fatal",   "effects": {"안전": -25, "건강": -15, "life": -20}},
    ]
    return {
        "title": "🩹 넘어져서 무릎이 크게 찢어졌어요!",
        "options": options,
        "explanation": {
            "correct": "적절한 처치로 감염 없이 잘 나았어요.",
            "partial": "지혈은 됐지만 제대로 소독이 안 됐어요.",
            "wrong":   "세균이 들어갔어요. 상처가 덧났어요!",
            "fatal":   "방치한 상처가 심하게 곪았어요...",
        },
    }


def crisis_childhood_choking(state):
    options = [
        {"text": "등을 세게 두드리는 하임리히법을 시행한다", "tier": "correct", "effects": {"건강": 30, "안전": 20}},
        {"text": "119에 신고하고 기다린다",                  "tier": "partial", "effects": {"건강": 10, "안전": 10}},
        {"text": "입안을 손으로 파낸다",                     "tier": "wrong",   "effects": {"건강": -20, "안전": -15, "life": -20}},
        {"text": "물을 마시게 한다",                         "tier": "fatal",   "effects": {"건강": -40, "안전": -20, "life": -35}},
    ]
    return {
        "title": "😱 음식이 목에 걸려 숨을 못 쉬어요!",
        "options": options,
        "explanation": {
            "correct": "하임리히법은 기도 폐쇄 응급처치의 기본이에요!",
            "partial": "119를 불렀지만 기다리는 동안 위험할 수 있었어요.",
            "wrong":   "손으로 파내면 더 깊이 들어갈 수 있어요!",
            "fatal":   "기도 막힘에 물은 절대 금물이에요! 큰일났어요...",
        },
    }


def crisis_childhood_nosebleed(state):
    options = [
        {"text": "고개를 앞으로 숙이고 코를 꽉 눌러 지혈한다", "tier": "correct", "effects": {"건강": 25, "안전": 15}},
        {"text": "코에 휴지를 꽉 넣어준다",                    "tier": "partial", "effects": {"건강": 10, "안전": 5}},
        {"text": "고개를 뒤로 젖히게 한다",                    "tier": "wrong",   "effects": {"건강": -20, "안전": -10, "life": -15}},
        {"text": "그러다 멈추겠지 하고 놔둔다",                "tier": "fatal",   "effects": {"건강": -25, "영양": -15, "life": -20}},
    ]
    return {
        "title": "🩸 코피가 멈추질 않아요!",
        "options": options,
        "explanation": {
            "correct": "고개를 앞으로 숙이고 눌러야 혈액이 기도로 안 들어가요.",
            "partial": "지혈은 됐지만 완벽한 방법은 아니에요.",
            "wrong":   "뒤로 젖히면 피가 목으로 넘어가요. 위험해요!",
            "fatal":   "코피를 방치하면 과다 출혈로 이어질 수 있어요...",
        },
    }


# ── 학창시절 ──
def crisis_teen_burnout(state):
    options = [
        {"text": "공부를 잠시 멈추고 충분히 재운다",  "tier": "correct", "effects": {"수면": 40, "건강": 15}},
        {"text": "카페인 음료로 버티게 한다",          "tier": "wrong",   "effects": {"수면": -25, "건강": -15, "life": -15}},
        {"text": "밥이라도 잘 챙겨준다",               "tier": "partial", "effects": {"영양": 20, "건강": 5}},
        {"text": "성적이 먼저니까 계속 공부시킨다",   "tier": "fatal",   "effects": {"수면": -30, "건강": -20, "life": -25}},
    ]
    return {
        "title": "📚 시험 기간, 며칠째 잠을 거의 못 잤어요...",
        "options": options,
        "explanation": {
            "correct": "쉬고 나서 오히려 집중력이 올랐어요.",
            "partial": "영양은 보충됐지만 수면 부족은 그대로예요.",
            "wrong":   "카페인 의존이 심해졌어요. 더 힘들어졌어요.",
            "fatal":   "수면 부채가 쌓여서 몸이 한계에 달했어요...",
        },
    }


def crisis_teen_social(state):
    options = [
        {"text": "끝까지 이야기를 들어주고 공감해준다", "tier": "correct",  "effects": {"건강": 25, "수면": 10}},
        {"text": "맛있는 것을 사주며 기분을 풀어준다",  "tier": "partial",  "effects": {"영양": 15, "건강": 5}},
        {"text": "그냥 참으면 된다고 한다",             "tier": "wrong",    "effects": {"건강": -20, "수면": -10, "life": -15}},
        {"text": "약한 소리 하지 말라고 한다",          "tier": "fatal",    "effects": {"건강": -30, "수면": -20, "life": -25}},
    ]
    return {
        "title": "😔 학교에서 친구 관계가 너무 힘들대요...",
        "options": options,
        "explanation": {
            "correct": "들어주는 것만으로 마음이 많이 풀렸어요.",
            "partial": "잠깐은 나아졌지만 근본적인 해소는 안 됐어요.",
            "wrong":   "억누른 감정이 결국 더 큰 문제로 번졌어요.",
            "fatal":   "가장 필요할 때 상처받았어요. 마음이 닫혔어요.",
        },
    }


def crisis_teen_depression(state):
    options = [
        {"text": "전문 상담사에게 연결해서 정기 상담을 받게 한다", "tier": "correct", "effects": {"건강": 30, "수면": 15}},
        {"text": "충분히 쉬고 좋아하는 일을 하게 한다",           "tier": "partial", "effects": {"건강": 15, "수면": 10}},
        {"text": "힘내라고 응원하며 곁에 있어준다",               "tier": "partial", "effects": {"건강": 10, "수면": 5}},
        {"text": "의지력이 약한 거라며 더 열심히 살라고 한다",    "tier": "fatal",   "effects": {"건강": -35, "수면": -25, "life": -30}},
    ]
    return {
        "title": "😶 아무것도 하기 싫고 매일 슬프다고 해요...",
        "options": options,
        "explanation": {
            "correct": "청소년 우울증은 전문적 도움이 필요해요. 탁월한 선택!",
            "partial": "도움이 됐지만 전문적 치료는 아니었어요.",
            "wrong":   "의지력 문제가 아니에요. 상태가 더 악화됐어요.",
            "fatal":   "청소년 우울증에 질책은 가장 위험한 대처예요...",
        },
    }


def crisis_teen_sprain(state):
    options = [
        {"text": "RICE 처치(휴식·냉찜질·압박·거상)를 한다", "tier": "correct", "effects": {"안전": 30, "건강": 10}},
        {"text": "정형외과에서 엑스레이를 찍어본다",         "tier": "partial", "effects": {"안전": 15, "건강": 5}},
        {"text": "바로 뜨거운 찜질을 한다",                  "tier": "wrong",   "effects": {"안전": -20, "건강": -20, "life": -15}},
        {"text": "파스를 붙이고 계속 걷게 한다",             "tier": "fatal",   "effects": {"안전": -25, "건강": -25, "life": -20}},
    ]
    return {
        "title": "🦶 체육 시간에 발목을 삐었어요!",
        "options": options,
        "explanation": {
            "correct": "RICE 처치가 염좌 초기 대처의 표준이에요.",
            "partial": "병원 확인도 좋지만 초기 냉찜질이 먼저예요.",
            "wrong":   "초기에 뜨거운 찜질은 붓기를 더 키워요!",
            "fatal":   "부상 부위를 계속 사용하면 인대가 더 손상돼요...",
        },
    }


# ── 중년 ──
def crisis_adult_burnout(state):
    options = [
        {"text": "휴가를 내고 며칠 동안 푹 쉬게 한다",  "tier": "correct", "effects": {"수면": 35, "건강": 15}},
        {"text": "가벼운 운동을 권한다",                 "tier": "partial", "effects": {"건강": 10, "수면": 5}},
        {"text": "좋아하는 취미 활동을 찾아준다",        "tier": "partial", "effects": {"건강": 15, "수면": 10}},
        {"text": "더 열심히 해야 한다고 독려한다",       "tier": "fatal",   "effects": {"수면": -30, "건강": -25, "life": -25}},
    ]
    return {
        "title": "😮‍💨 번아웃이 왔어요. 아무것도 하기 싫대요...",
        "options": options,
        "explanation": {
            "correct": "충분히 쉬고 나서 활력을 되찾았어요.",
            "partial": "조금 나아졌지만 완전한 회복은 아니에요.",
            "wrong":   "일시적인 효과만 있었어요.",
            "fatal":   "한계를 넘었어요. 몸이 먼저 쓰러졌어요...",
        },
    }


def crisis_adult_health_check(state):
    options = [
        {"text": "즉시 전문의에게 상담을 받게 한다",    "tier": "correct", "effects": {"건강": 30}},
        {"text": "식단을 건강하게 바꿔준다",            "tier": "partial", "effects": {"영양": 15, "건강": 10}},
        {"text": "인터넷에서 찾아보고 자가 치료한다",   "tier": "wrong",   "effects": {"건강": -25, "life": -20}},
        {"text": "바쁘니까 나중에 보자고 한다",         "tier": "fatal",   "effects": {"건강": -30, "life": -25}},
    ]
    return {
        "title": "🫀 건강검진에서 이상 소견이 나왔어요",
        "options": options,
        "explanation": {
            "correct": "조기에 발견하고 제대로 치료받았어요.",
            "partial": "식습관 개선은 도움이 됐지만 부족해요.",
            "wrong":   "잘못된 자가 치료로 상태가 더 나빠졌어요!",
            "fatal":   "나중에 발견했을 때는 이미 많이 진행됐어요...",
        },
    }


def crisis_adult_back_pain(state):
    options = [
        {"text": "물리치료와 적절한 운동 치료를 받는다",  "tier": "correct", "effects": {"건강": 30, "안전": 10}},
        {"text": "가벼운 스트레칭으로 관리한다",          "tier": "partial", "effects": {"건강": 15, "안전": 5}},
        {"text": "누워서 절대 안정을 취한다",             "tier": "wrong",   "effects": {"건강": -20, "수면": -10, "life": -15}},
        {"text": "진통제로 버티면서 일을 계속한다",       "tier": "fatal",   "effects": {"건강": -30, "안전": -10, "life": -25}},
    ]
    return {
        "title": "💪 허리가 너무 아파서 움직이기 힘들어요...",
        "options": options,
        "explanation": {
            "correct": "전문적 물리치료가 허리 통증의 근본 해결책이에요.",
            "partial": "스트레칭은 도움이 되지만 충분하지 않을 수 있어요.",
            "wrong":   "완전 안정은 오히려 허리 근육을 약화시켜요.",
            "fatal":   "진통제로 신호를 무시하면 디스크가 더 손상돼요...",
        },
    }


def crisis_adult_hypertension(state):
    options = [
        {"text": "전문의와 상담 후 혈압약을 처방받는다",     "tier": "correct", "effects": {"건강": 30}},
        {"text": "짜게 먹지 말고 운동을 시작한다",           "tier": "partial", "effects": {"건강": 15, "영양": 10}},
        {"text": "혈압이 높은 날만 약을 먹는다",             "tier": "wrong",   "effects": {"건강": -25, "life": -20}},
        {"text": "나이 들면 원래 높아지는 거라고 무시한다",  "tier": "fatal",   "effects": {"건강": -35, "life": -30}},
    ]
    return {
        "title": "🩺 혈압이 심각하게 높다는 검진 결과가 나왔어요",
        "options": options,
        "explanation": {
            "correct": "고혈압은 꾸준한 약 복용이 가장 중요해요.",
            "partial": "생활 습관 개선도 중요하지만 약이 필요할 수 있어요.",
            "wrong":   "고혈압 약은 꾸준히 매일 먹어야 효과가 있어요!",
            "fatal":   "고혈압 방치는 뇌졸중·심근경색의 원인이에요...",
        },
    }


# ── 노년 ──
def crisis_senior_fall(state):
    options = [
        {"text": "미끄럼방지 매트와 안전 손잡이를 설치한다", "tier": "correct", "effects": {"안전": 35, "건강": 5}},
        {"text": "넘어지지 않게 늘 옆에서 잡아준다",        "tier": "partial", "effects": {"안전": 20, "건강": 5}},
        {"text": "위험한 곳에는 아예 못 가게 한다",         "tier": "partial", "effects": {"안전": 15}},
        {"text": "조심하면 된다고 하고 그냥 둔다",          "tier": "fatal",   "effects": {"안전": -30, "건강": -20, "life": -30}},
    ]
    return {
        "title": "🦴 계단에서 미끄러져 넘어질 뻔했어요!",
        "options": options,
        "explanation": {
            "correct": "환경 자체를 안전하게 바꿨어요. 완벽한 예방이에요.",
            "partial": "당장의 위험은 줄었지만 근본 해결은 아니에요.",
            "wrong":   "또 사고가 날 수 있어요. 낙상은 노년에 치명적이에요.",
            "fatal":   "방치한 위험이 결국 사고로 이어졌어요...",
        },
    }


def crisis_senior_medication(state):
    options = [
        {"text": "복약 알림 앱과 약통에 날짜를 표시해준다",  "tier": "correct", "effects": {"건강": 30}},
        {"text": "보호자가 직접 매일 챙겨주기로 한다",       "tier": "partial", "effects": {"건강": 20}},
        {"text": "잊으면 안 된다고 혼낸다",                  "tier": "wrong",   "effects": {"건강": -15, "수면": -10, "life": -10}},
        {"text": "못 먹은 약을 한 번에 몰아서 먹인다",       "tier": "fatal",   "effects": {"건강": -35, "life": -30}},
    ]
    return {
        "title": "💊 약을 언제 먹었는지 자꾸 기억을 못 해요",
        "options": options,
        "explanation": {
            "correct": "체계적인 관리로 복약 순응도가 높아졌어요.",
            "partial": "당분간은 잘 챙겨드렸어요.",
            "wrong":   "꾸짖음은 오히려 스트레스가 됐어요.",
            "fatal":   "약을 한꺼번에 먹으면 과복용 위험이 있어요!",
        },
    }


def crisis_senior_pneumonia(state):
    options = [
        {"text": "즉시 병원에 입원해 항생제 치료를 받는다", "tier": "correct", "effects": {"건강": 30, "안전": 10}},
        {"text": "폐렴구균 백신을 맞았으니 지켜본다",       "tier": "wrong",   "effects": {"건강": -20, "life": -15}},
        {"text": "집에서 따뜻하게 쉬게 한다",              "tier": "wrong",   "effects": {"건강": -25, "수면": -10, "life": -20}},
        {"text": "시판 기침약을 먹이고 버틴다",            "tier": "fatal",   "effects": {"건강": -35, "life": -30}},
    ]
    return {
        "title": "🫁 열과 기침이 일주일째 낫질 않아요...",
        "options": options,
        "explanation": {
            "correct": "노인 폐렴은 빠른 입원 치료가 필수예요.",
            "partial": "집에서의 휴식만으로는 부족해요.",
            "wrong":   "일반 기침약으로 폐렴은 치료되지 않아요!",
            "fatal":   "폐렴을 방치하면 패혈증으로 발전할 수 있어요...",
        },
    }


def crisis_senior_stroke_warning(state):
    options = [
        {"text": "즉시 119에 신고하고 골든타임을 지킨다", "tier": "correct", "effects": {"건강": 30, "life": 10}},
        {"text": "주변 사람에게 알리고 병원으로 모신다",  "tier": "partial", "effects": {"건강": 15, "life": 5}},
        {"text": "물을 마시게 하고 안정시킨다",           "tier": "wrong",   "effects": {"건강": -25, "life": -25}},
        {"text": "집에서 쉬게 하면서 나아지길 기다린다", "tier": "fatal",   "effects": {"건강": -40, "life": -35}},
    ]
    return {
        "title": "🧠 갑자기 한쪽 팔다리가 마비되고 말이 어눌해져요!",
        "options": options,
        "explanation": {
            "correct": "뇌졸중 골든타임은 4.5시간! 즉각 신고가 생명을 지켜요.",
            "partial": "병원에 갔지만 119보다 느릴 수 있어요.",
            "wrong":   "물과 안정만으로는 뇌졸중이 해결되지 않아요!",
            "fatal":   "뇌졸중 골든타임을 놓쳤어요. 되돌이킬 수 없는 손상이...",
        },
    }


# ── 황혼기 ──
def crisis_elder_cardiac(state):
    options = [
        {"text": "즉시 119에 신고하고 심폐소생술을 준비한다", "tier": "correct", "effects": {"건강": 30, "life": 15}},
        {"text": "주변 사람에게 큰 소리로 도움을 요청한다",   "tier": "partial", "effects": {"건강": 15, "life": 5}},
        {"text": "물을 먹이고 누워있게 한다",                 "tier": "wrong",   "effects": {"건강": -30, "life": -30}},
        {"text": "잠깐 쉬면 괜찮아질 거라고 기다린다",        "tier": "fatal",   "effects": {"건강": -40, "life": -35}},
    ]
    return {
        "title": "🫀 갑자기 가슴을 잡고 쓰러지셨어요!",
        "options": options,
        "explanation": {
            "correct": "골든타임을 지켰어요! 빠른 신고가 생명을 살렸어요.",
            "partial": "도움을 구해서 다행이에요.",
            "wrong":   "심장 응급에 물을 먹이면 절대 안 돼요!",
            "fatal":   "골든타임을 놓쳤어요. 너무 늦었어요...",
        },
    }


def crisis_elder_dementia(state):
    options = [
        {"text": "전문 의료진에게 인지 기능 검진을 받게 한다", "tier": "correct", "effects": {"건강": 25, "안전": 10}},
        {"text": "GPS 위치 추적기를 달아준다",                 "tier": "partial", "effects": {"안전": 20}},
        {"text": "기억력 훈련 앱을 찾아서 같이 해본다",        "tier": "partial", "effects": {"건강": 15, "수면": 5}},
        {"text": "왜 그랬냐고 혼내고 다음엔 잘하라고 한다",   "tier": "fatal",   "effects": {"건강": -30, "수면": -20, "life": -25}},
    ]
    return {
        "title": "🧠 오늘 혼자 집을 못 찾아오셨어요...",
        "options": options,
        "explanation": {
            "correct": "조기에 발견해서 적절한 돌봄 계획을 세웠어요.",
            "partial": "안전은 챙겼지만 근본 원인 파악이 필요해요.",
            "wrong":   "혼내면 오히려 더 위축되고 증상이 나빠질 수 있어요.",
            "fatal":   "인지 저하 초기에 혼냄은 가장 큰 상처예요...",
        },
    }


def crisis_elder_aspiration(state):
    options = [
        {"text": "음식 농도를 조절하고 앉아서 천천히 먹게 한다", "tier": "correct", "effects": {"건강": 25, "영양": 10}},
        {"text": "폐렴 예방 주사를 맞는다",                      "tier": "partial", "effects": {"건강": 10, "안전": 5}},
        {"text": "식사를 완전히 끊고 링거로 영양 보충한다",       "tier": "wrong",   "effects": {"영양": -20, "건강": -20, "life": -20}},
        {"text": "그냥 천천히 먹으면 된다고 한다",                "tier": "fatal",   "effects": {"건강": -35, "영양": -20, "life": -30}},
    ]
    return {
        "title": "🍜 식사 중에 자꾸 사레들려 폐로 음식이 넘어가요...",
        "options": options,
        "explanation": {
            "correct": "연하 장애는 식이 조절과 바른 자세가 핵심이에요.",
            "partial": "예방 주사도 도움이 되지만 직접적 해결은 아니에요.",
            "wrong":   "링거만으로는 장기적 영양 유지가 어렵고 근본 해결이 안 돼요.",
            "fatal":   "흡인성 폐렴으로 악화됐어요. 노년에 매우 위험해요...",
        },
    }


def crisis_elder_depression(state):
    options = [
        {"text": "정신건강의학과에서 노인 우울증 치료를 받게 한다", "tier": "correct", "effects": {"건강": 30, "수면": 15}},
        {"text": "산책과 취미 활동을 권한다",                       "tier": "partial", "effects": {"건강": 15, "수면": 10}},
        {"text": "가족이 자주 찾아오기로 한다",                      "tier": "partial", "effects": {"건강": 15, "수면": 5}},
        {"text": "나이 들면 원래 우울한 거라고 한다",                "tier": "fatal",   "effects": {"건강": -35, "수면": -25, "life": -30}},
    ]
    return {
        "title": "😔 아무것도 하기 싫고 죽고 싶다는 말씀을 하세요...",
        "options": options,
        "explanation": {
            "correct": "노인 우울증은 자살 위험이 높아요. 전문 치료가 필수예요.",
            "partial": "활동과 사회적 연결이 도움이 돼요.",
            "wrong":   "노인 우울증은 질병이에요. 당연한 게 아니에요!",
            "fatal":   "방치한 노인 우울증은 극단적 선택으로 이어질 수 있어요...",
        },
    }


CRISIS_BY_STAGE = {
    "유년기":   [crisis_childhood_fever, crisis_childhood_injury,
                 crisis_childhood_choking, crisis_childhood_nosebleed],
    "학창시절": [crisis_teen_burnout,    crisis_teen_social,
                 crisis_teen_depression, crisis_teen_sprain],
    "중년":     [crisis_adult_burnout,   crisis_adult_health_check,
                 crisis_adult_back_pain, crisis_adult_hypertension],
    "노년":     [crisis_senior_fall,     crisis_senior_medication,
                 crisis_senior_pneumonia, crisis_senior_stroke_warning],
    "황혼기":   [crisis_elder_cardiac,   crisis_elder_dementia,
                 crisis_elder_aspiration, crisis_elder_depression],
}

# ============================================================
# 게임 로직 함수
# ============================================================
def get_life_stage(age):
    if age <= 10:   return "유년기",   "👶"
    elif age <= 25: return "학창시절", "🧒"
    elif age <= 50: return "중년",     "🧑‍🏫"
    elif age <= 70: return "노년",     "🧓"
    else:           return "황혼기",   "🎉"


def get_face_emoji(state):
    if state.life < 20:
        return "💀"
    elif any(v < 20 for v in state.stats.values()):
        return "😭"
    elif state.life < 50:
        return "😔"
    elif all(v >= 60 for v in state.stats.values()):
        return "😊"
    else:
        return "😐"


def calculate_life_change(state):
    delta = 0
    for val in state.stats.values():
        if val < 20:   delta -= 15
        elif val < 40: delta -= 5
    if state.stats["수면"] < 30:
        delta -= 10
    if all(v >= 60 for v in state.stats.values()):
        delta += 5
    return delta


def end_turn_decay(state):
    stage, _ = get_life_stage(state.age)
    decay = STAGE_DECAY[stage]
    for stat in state.stats:
        state.stats[stat] -= decay[stat]
    state.life -= decay["생명력"]


def check_alive(state):
    if state.life <= 0:
        state.alive = False
        worst = min(state.stats, key=state.stats.get)
        state.death_cause = {
            "영양": "영양실조로", "건강": "병환으로",
            "안전": "사고로",     "수면": "탈진으로",
        }[worst]
        return False
    return True


# ============================================================
# 페이지 설정
# ============================================================
st.set_page_config(
    page_title="서은주 선생님의 80년",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# 세션 상태 초기화
# ============================================================
if "screen" not in st.session_state:
    st.session_state.screen               = "intro"
    st.session_state.gs                   = None
    st.session_state.current_crisis       = None
    st.session_state.crisis_options_order = None
    st.session_state.crisis_result        = None
    st.session_state.actions_done         = []
    st.session_state.full_turn_used       = False
    st.session_state.good_event_text      = None
    st.session_state.last_action_msgs     = []
    st.session_state.pre_turn_stage       = "유년기"
    st.session_state.incoming_stage       = None
    st.session_state.balloons_shown       = False
    st.session_state.used_crises          = set()

# ============================================================
# CSS
# ============================================================
def apply_css(stage: str = "유년기", crisis: bool = False, center: bool = False):
    bg = "#FFF0F0" if crisis else STAGE_BG.get(stage, "#FFFFFF")
    shake_anim = """
        @keyframes crisis-shake {
            0%,100% { transform:translateX(0); }
            20%     { transform:translateX(-7px); }
            40%     { transform:translateX(7px); }
            60%     { transform:translateX(-7px); }
            80%     { transform:translateX(7px); }
        }
        .stApp { animation: crisis-shake 0.4s ease; }
    """ if crisis else ""

    st.markdown(f"""
    <style>
        header[data-testid="stHeader"] {{
            display: none !important;
        }}
        #MainMenu {{
            display: none !important;
        }}
        [data-testid="stToolbar"] {{
            display: none !important;
        }}
        .stApp {{
            background-color: {bg} !important;
            transition: background-color 1.0s ease;
        }}
        .block-container {{
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
            padding-left: 8% !important;
            padding-right: 8% !important;
            max-width: 1400px !important;
            margin: 0 auto !important;
            box-sizing: border-box !important;
            min-height: 100vh !important;
            display: flex !important;
            flex-direction: column !important;
        }}
        .block-container > [data-testid="stVerticalBlock"] {{
            flex: 1 !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: {"center" if center else "space-between"} !important;
        }}
        .big-emoji {{
            text-align: center;
            font-size: 90px;
            line-height: 1.1;
            margin: 0.5rem 0;
        }}
        .stage-emoji {{
            text-align: center;
            font-size: 90px;
            line-height: 1.2;
        }}
        .center-text {{ text-align: center; }}
        [data-testid="stMetric"] {{ padding: 0.5rem 0.8rem !important; }}
        [data-testid="stMetricValue"] {{ font-size: 1.4rem !important; font-weight: 700; }}
        [data-testid="stMetricLabel"] {{ font-size: 0.85rem !important; }}
        div[data-testid="stAlert"] {{ padding: 0.6rem 1rem !important; font-size: 1rem !important; margin-bottom: 0.5rem !important; text-align: center !important; display: flex !important; align-items: center !important; justify-content: center !important; }}
        div[data-testid="stAlert"] > div {{ display: flex !important; align-items: center !important; justify-content: center !important; width: 100% !important; }}
        div[data-testid="stAlert"] p {{ margin: 0 !important; line-height: 1.4 !important; }}
        .stButton > button {{ padding: 0.8rem 1rem !important; font-size: 1rem !important; font-weight: 600 !important; }}
        h1 {{ font-size: 1.6rem !important; margin: 0.4rem 0 !important; }}
        h2 {{ font-size: 1.3rem !important; margin: 0.3rem 0 !important; }}
        h3 {{ font-size: 1.1rem !important; margin: 0.2rem 0 !important; }}
        h4 {{ font-size: 1rem !important; margin: 0.1rem 0 !important; }}
        p  {{ font-size: 1rem !important; margin: 0.2rem 0 !important; }}
        .stCaption p {{ font-size: 0.85rem !important; }}
        hr {{ margin: 0.8rem 0 !important; }}
        div[data-testid="stToastContainer"] {{
            position: fixed !important;
            bottom: 1.5rem !important;
            right: 1.5rem !important;
            left: auto !important;
            top: auto !important;
            max-width: 400px !important;
            width: max-content !important;
            z-index: 9999 !important;
        }}
        div[data-testid="stToastContainer"] [data-testid="stToast"] {{
            white-space: normal !important;
            word-break: keep-all !important;
        }}
        {shake_anim}
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# UI 헬퍼
# ============================================================
_STAT_COLORS = {"영양": "#43A047", "건강": "#1E88E5", "안전": "#FB8C00", "수면": "#8E24AA"}

def render_stat_bars(gs):
    parts = []
    for stat, val in gs.stats.items():
        pct   = min(int(val), 100)
        color = _STAT_COLORS[stat]
        icon  = "🔴" if val < 30 else ("🟡" if val < 50 else "🟢")
        parts.append(
            f"<div style='margin-bottom:7px;'>"
            f"<div style='display:flex;justify-content:space-between;font-size:0.8rem;margin-bottom:3px;'>"
            f"<span>{icon} {STAT_EMOJI[stat]} {stat}</span>"
            f"<b style='color:{color};'>{int(val)}</b></div>"
            f"<div style='background:rgba(0,0,0,0.13);border-radius:99px;height:10px;'>"
            f"<div style='width:{pct}%;background:{color};border-radius:99px;height:10px;"
            f"transition:width 0.4s;'></div></div></div>"
        )
    st.markdown("".join(parts), unsafe_allow_html=True)


def render_life_bar(gs):
    pct = min(int(gs.life), 100)
    if gs.life >= 70:   color, glow = "#e53935", "#e5393555"
    elif gs.life >= 40: color, glow = "#fb8c00", "#fb8c0055"
    else:               color, glow = "#9e9e9e", "#9e9e9e55"
    st.markdown(
        f"<div style='background:rgba(0,0,0,0.07);border-radius:12px;padding:14px 16px;margin-bottom:10px;'>"
        f"<div style='display:flex;justify-content:space-between;font-size:1rem;margin-bottom:8px;'>"
        f"<b>❤️ 생명력</b><b style='color:{color};font-size:1.25rem;'>{int(gs.life)}</b></div>"
        f"<div style='background:rgba(0,0,0,0.13);border-radius:99px;height:22px;'>"
        f"<div style='width:{pct}%;background:{color};border-radius:99px;height:22px;"
        f"box-shadow:0 0 12px {glow};transition:width 0.4s;'></div></div></div>",
        unsafe_allow_html=True
    )


def render_warnings(gs):
    if gs.stats["수면"] < 30:
        st.warning("💡 수면 부족 → 돌봄 효과 절반")
    if gs.life < 40:
        st.error("💡 생명력 위험! 스탯을 60 이상으로")
    if any(v < 20 for v in gs.stats.values()):
        st.error("💡 스탯 20 미만 → 생명력 큰 타격!")


# ============================================================
# 콜백 헬퍼
# ============================================================
def _begin_turn(gs):
    gs.age = gs.turn * YEARS_PER_TURN
    stage, _ = get_life_stage(gs.age)
    st.session_state.pre_turn_stage   = stage
    st.session_state.actions_done     = []
    st.session_state.full_turn_used   = False
    st.session_state.crisis_result    = None
    st.session_state.good_event_text  = None
    st.session_state.last_action_msgs = []
    st.session_state.balloons_shown   = False

    if gs.turn > 0:
        roll = random.random()
        if roll < CRISIS_CHANCE:
            stage_pool = CRISIS_BY_STAGE.get(stage, [])
            full_pool  = CRISIS_FUNCTIONS + stage_pool * 2

            # 이미 나온 위기 제외; 풀 소진 시 해당 풀만 리셋
            unique_in_pool = {f.__name__ for f in full_pool}
            if unique_in_pool <= st.session_state.used_crises:
                st.session_state.used_crises -= unique_in_pool
            available = [f for f in full_pool
                         if f.__name__ not in st.session_state.used_crises]
            if not available:
                available = full_pool

            fn = random.choice(available)
            st.session_state.used_crises.add(fn.__name__)

            crisis  = fn(gs)
            indices = list(range(len(crisis["options"])))
            random.shuffle(indices)
            st.session_state.current_crisis       = crisis
            st.session_state.crisis_options_order = indices
            st.session_state.screen = "crisis"
        elif roll < CRISIS_CHANCE + GOOD_EVENT_CHANCE:
            st.session_state.good_event_text = random.choice(GOOD_EVENTS_BY_STAGE[stage])
            st.session_state.screen = "care"
        else:
            st.session_state.screen = "care"
    else:
        st.session_state.screen = "care"


# ============================================================
# 콜백
# ============================================================
def cb_start_game():
    gs = GameState()
    st.session_state.gs                   = gs
    st.session_state.current_crisis       = None
    st.session_state.crisis_options_order = None
    st.session_state.incoming_stage       = None
    st.session_state.used_crises          = set()
    _begin_turn(gs)


def cb_crisis_choice(picked_idx):
    gs     = st.session_state.gs
    crisis = st.session_state.current_crisis
    picked = crisis["options"][picked_idx]

    stage, _ = get_life_stage(gs.age)
    sev = STAGE_SEVERITY[stage]   # 단계별 페널티 배율

    for key, delta in picked["effects"].items():
        # 잘못된/치명적 선택의 음수 효과를 단계별로 증폭
        if delta < 0 and picked["tier"] in ("wrong", "fatal"):
            delta = int(delta * sev)
        if key == "life":
            gs.life += delta
        else:
            gs.stats[key] += delta
    gs.clamp()

    if picked["tier"] == "correct":
        gs.crisis_handled_well += 1
    elif picked["tier"] == "wrong":
        gs.crisis_failed += 1
    elif picked["tier"] not in ("partial",):
        gs.crisis_failed += 1

    st.session_state.crisis_result = {
        "text":        picked["text"],
        "tier":        picked["tier"],
        "explanation": crisis["explanation"][picked["tier"]],
    }
    st.session_state.screen = "care"


def cb_select_action(key):
    gs = st.session_state.gs
    if st.session_state.full_turn_used or len(st.session_state.actions_done) >= 2:
        return
    a = ACTIONS[key]
    if a["full"] and len(st.session_state.actions_done) > 0:
        return

    mult   = 0.5 if (gs.stats["수면"] < 30 and a["stat"] != "수면") else 1.0
    actual = int(a["amount"] * mult)
    gs.stats[a["stat"]] += actual
    gs.stat_care_count[a["stat"]] += 1
    gs.clamp()

    msg = f"{a['name']} → {a['stat']} +{actual}"
    if mult < 1.0:
        msg += " (절반)"

    st.session_state.actions_done.append(key)
    st.session_state.last_action_msgs.append(msg)
    if a["full"]:
        st.session_state.full_turn_used = True


def cb_end_turn():
    gs = st.session_state.gs
    if not st.session_state.actions_done:
        gs.life -= 5
        st.session_state.last_action_msgs.append("방치 패널티 → 생명력 -5")

    end_turn_decay(gs)
    gs.life += calculate_life_change(gs)
    gs.clamp()

    if all(v >= 60 for v in gs.stats.values()):
        gs.good_turns += 1
    if any(v <= 20 for v in gs.stats.values()):
        gs.bad_turns += 1

    gs.turn += 1

    if not check_alive(gs):
        st.session_state.screen = "ending"
    elif gs.turn >= TOTAL_TURNS:
        gs.age = MAX_AGE
        st.session_state.screen = "ending"
    else:
        st.session_state.screen = "turn_transition"


# ============================================================
# 화면 렌더링
# ============================================================
screen = st.session_state.screen

# ── 인트로 ───────────────────────────────────────────────────
if screen == "intro":
    apply_css("유년기", center=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown("<div class='big-emoji'>🌱</div>", unsafe_allow_html=True)
        st.markdown("<h1 class='center-text'>서은주 선생님의 80년</h1>", unsafe_allow_html=True)
        st.markdown("<p class='center-text' style='color:gray;margin:0'>생명 존중 게임</p>",
                    unsafe_allow_html=True)
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
**📖 게임 방법**
- 총 {TOTAL_TURNS}턴 · 1턴 = {YEARS_PER_TURN}년 (0→{MAX_AGE}세)
- 스탯: 🍚 영양 / 💊 건강 / 🌡️ 안전 / 😴 수면
- 한 턴에 액션 **최대 2개** (재우기는 한 턴 통째)
- 나이 들수록 스탯 감소 속도 빨라짐
- ❤️ 생명력 0이면 사망
""")
        with c2:
            st.markdown("""
**⚠️ 주의사항**
- 수면 30 미만 → 돌봄 효과 **절반**
- 위기 잘못 대처 → **단계별 페널티 배율 적용**
- 노년·황혼기에선 실수가 즉사 수준으로 증폭!
- 스탯 20 미만 → 매 턴 생명력 감소
- 🎯 목표: **80세까지 건강하게 살리기**
""")
        st.divider()
        st.button("🎮 게임 시작!", on_click=cb_start_game, type="primary", use_container_width=True)


# ── 돌봄 화면 ────────────────────────────────────────────────
elif screen == "care":
    gs = st.session_state.gs
    stage, stage_emoji = get_life_stage(gs.age)
    face = get_face_emoji(gs)
    apply_css(stage)

    # ── 헤더: 4 메트릭 ──
    h1, h2, h3, h4 = st.columns(4)
    with h1: st.metric("⏳ 턴", f"{gs.turn + 1} / {TOTAL_TURNS}")
    with h2: st.metric("📅 나이", f"{gs.age}세")
    with h3: st.metric(f"{stage_emoji} 단계", stage)
    with h4: st.metric("❤️ 생명력", f"{int(gs.life)}")

    # ── 얼굴 이모지 + 생명력 바 (가로로 나란히) ──
    fc, lc = st.columns([1, 5])
    with fc:
        st.markdown(f"<div class='big-emoji'>{face}</div>", unsafe_allow_html=True)
    with lc:
        render_life_bar(gs)
        st.markdown(
            f"<div style='background:rgba(0,0,0,0.06);border-radius:10px;"
            f"padding:8px 14px;font-size:0.95rem;color:#444;margin-top:4px;'>"
            f"{stage_emoji} <b>{stage}</b> · {gs.age}세 &nbsp;|&nbsp; {STAGE_DESC[stage]}</div>",
            unsafe_allow_html=True
        )

    # ── 스탯바 (2열 그리드) ──
    sb1, sb2 = st.columns(2)
    stats_items = list(gs.stats.items())
    for i, (stat, val) in enumerate(stats_items):
        pct   = min(int(val), 100)
        color = _STAT_COLORS[stat]
        icon  = "🔴" if val < 30 else ("🟡" if val < 50 else "🟢")
        bar_html = (
            f"<div style='margin-bottom:14px;'>"
            f"<div style='display:flex;justify-content:space-between;font-size:1rem;margin-bottom:6px;'>"
            f"<span>{icon} {STAT_EMOJI[stat]} {stat}</span>"
            f"<b style='color:{color};font-size:1.05rem;'>{int(val)}</b></div>"
            f"<div style='background:rgba(0,0,0,0.13);border-radius:99px;height:18px;'>"
            f"<div style='width:{pct}%;background:{color};border-radius:99px;height:18px;"
            f"transition:width 0.4s;'></div></div></div>"
        )
        with (sb1 if i < 2 else sb2):
            st.markdown(bar_html, unsafe_allow_html=True)

    render_warnings(gs)
    st.divider()

    # ── 이벤트 / 위기 결과 ──
    if st.session_state.good_event_text:
        st.success(f"✨ {st.session_state.good_event_text}")
        if not st.session_state.balloons_shown:
            st.balloons()
            st.session_state.balloons_shown = True

    if st.session_state.crisis_result:
        r    = st.session_state.crisis_result
        tier = r["tier"]
        msg  = f"**{r['text']}**  \n{r['explanation']}"
        if tier == "correct":   st.success(f"✅ {msg}")
        elif tier == "partial": st.warning(f"🔶 {msg}")
        else:                   st.error(f"{'❌' if tier == 'wrong' else '💀'} {msg}")

    if st.session_state.last_action_msgs:
        st.caption("이번 턴: " + "  |  ".join(st.session_state.last_action_msgs))

    # ── 인생 여정 타임라인 ──
    done_bar = "█" * gs.turn
    left_bar = "░" * (TOTAL_TURNS - gs.turn)
    pct_done = int(gs.turn / TOTAL_TURNS * 100)
    st.markdown(
        f"<div style='background:rgba(0,0,0,0.06);border-radius:12px;padding:14px 18px;'>"
        f"<div style='font-size:0.95rem;color:#555;margin-bottom:8px;'>"
        f"📅 인생 여정 &nbsp; <b>{gs.turn}/{TOTAL_TURNS} 턴</b> &nbsp;·&nbsp; {pct_done}% 완료</div>"
        f"<div style='font-family:monospace;font-size:0.8rem;letter-spacing:3px;"
        f"color:#888;word-break:break-all;'>{done_bar}<span style='color:#ccc;'>{left_bar}</span></div>"
        f"</div>",
        unsafe_allow_html=True
    )

    st.divider()

    # ── 돌봄 액션 버튼 ──
    n_done    = len(st.session_state.actions_done)
    full_used = st.session_state.full_turn_used
    can_act   = not full_used and n_done < 2

    if can_act:
        st.markdown(f"**💝 돌봄 액션  (남은 {2 - n_done}개)**")
        cols = st.columns(4)
        for i, (key, a) in enumerate(ACTIONS.items()):
            with cols[i]:
                sleep_blocked = a["full"] and n_done > 0
                st.button(
                    a["name"],
                    key=f"act_{key}_t{gs.turn}_d{n_done}",
                    on_click=cb_select_action,
                    args=(key,),
                    use_container_width=True,
                    disabled=sleep_blocked,
                )
                if a["full"]:
                    st.caption("⛔ 첫 번째만" if sleep_blocked else f"+{a['amount']}")
                else:
                    st.caption(f"+{a['amount']}")
    else:
        st.info("💤 한 턴 통째 사용함." if full_used else "✅ 액션 2개 완료.")

    btn_label = "⏭️ 다음 턴으로  (방치 시 생명력 -5)" if n_done == 0 else "⏭️ 다음 턴으로"
    st.button(btn_label, on_click=cb_end_turn, type="primary", use_container_width=True)


# ── 위기 화면 ────────────────────────────────────────────────
elif screen == "crisis":
    gs = st.session_state.gs
    stage, stage_emoji = get_life_stage(gs.age)
    face = get_face_emoji(gs)
    apply_css(stage, crisis=True)

    # ── 헤더: 4 메트릭 ──
    h1, h2, h3, h4 = st.columns(4)
    with h1: st.metric("⏳ 턴", f"{gs.turn + 1} / {TOTAL_TURNS}")
    with h2: st.metric("📅 나이", f"{gs.age}세")
    with h3: st.metric(f"{stage_emoji} 단계", stage)
    with h4: st.metric("❤️ 생명력", f"{int(gs.life)}")

    # ── 얼굴 이모지 + 생명력 바 ──
    fc, lc = st.columns([1, 5])
    with fc:
        st.markdown(f"<div class='big-emoji'>{face}</div>", unsafe_allow_html=True)
    with lc:
        render_life_bar(gs)
        sev = STAGE_SEVERITY[stage]
        if sev >= 2.0:
            st.error(f"⚠️ **{stage}** — 패널티 ×{sev:.1f}  즉사 위험!")
        elif sev >= 1.3:
            st.warning(f"⚠️ **{stage}** — 패널티 ×{sev:.1f}")

    # ── 스탯바 (2열 그리드) ──
    sb1, sb2 = st.columns(2)
    stats_items = list(gs.stats.items())
    for i, (stat, val) in enumerate(stats_items):
        pct   = min(int(val), 100)
        color = _STAT_COLORS[stat]
        icon  = "🔴" if val < 30 else ("🟡" if val < 50 else "🟢")
        bar_html = (
            f"<div style='margin-bottom:14px;'>"
            f"<div style='display:flex;justify-content:space-between;font-size:1rem;margin-bottom:6px;'>"
            f"<span>{icon} {STAT_EMOJI[stat]} {stat}</span>"
            f"<b style='color:{color};font-size:1.05rem;'>{int(val)}</b></div>"
            f"<div style='background:rgba(0,0,0,0.13);border-radius:99px;height:18px;'>"
            f"<div style='width:{pct}%;background:{color};border-radius:99px;height:18px;"
            f"transition:width 0.4s;'></div></div></div>"
        )
        with (sb1 if i < 2 else sb2):
            st.markdown(bar_html, unsafe_allow_html=True)

    st.divider()

    # ── 위기 내용 + 선택지 ──
    crisis = st.session_state.current_crisis
    st.error(f"### ⚠️ 위기 발생!\n{crisis['title']}")
    st.markdown("**어떻게 하시겠어요?**")
    order = st.session_state.crisis_options_order
    c1, c2 = st.columns(2)
    for i, idx in enumerate(order):
        opt = crisis["options"][idx]
        col = c1 if i % 2 == 0 else c2
        with col:
            st.button(
                f"{i + 1}. {opt['text']}",
                key=f"c_opt_{i}",
                on_click=cb_crisis_choice,
                args=(idx,),
                use_container_width=True,
            )


# ── 턴 전환 ──────────────────────────────────────────────────
elif screen == "turn_transition":
    gs      = st.session_state.gs
    old_age = gs.age
    new_age = gs.turn * YEARS_PER_TURN
    stage, _ = get_life_stage(old_age)
    face    = get_face_emoji(gs)
    apply_css(stage)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown(f"<div class='big-emoji'>{face}</div>", unsafe_allow_html=True)
        st.markdown(
            f"<h2 class='center-text'>⏳ {old_age}세 → {new_age}세</h2>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p class='center-text' style='color:#555'>5년이 흘렀어요...</p>",
            unsafe_allow_html=True,
        )
        if st.session_state.last_action_msgs:
            st.caption("이번 시기: " + "  |  ".join(st.session_state.last_action_msgs))
        with st.spinner("시간이 흐르는 중..."):
            time.sleep(1.5)

    new_stage, new_stage_emoji = get_life_stage(new_age)
    if new_stage != st.session_state.pre_turn_stage:
        st.session_state.incoming_stage = (new_stage, new_stage_emoji)
        st.session_state.screen = "stage_transition"
    else:
        _begin_turn(gs)
    st.rerun()


# ── 생애 단계 전환 ────────────────────────────────────────────
elif screen == "stage_transition":
    gs = st.session_state.gs
    new_stage, new_stage_emoji = st.session_state.incoming_stage
    apply_css(new_stage)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown(f"<div class='stage-emoji'>{new_stage_emoji}</div>",
                    unsafe_allow_html=True)
        st.markdown(f"<h1 class='center-text'>{new_stage}</h1>",
                    unsafe_allow_html=True)
        st.markdown(
            f"<p class='center-text' style='font-size:1.1em'>{STAGE_DESC[new_stage]}</p>",
            unsafe_allow_html=True,
        )

    with st.spinner("새로운 시기가 시작되고 있어요..."):
        time.sleep(2.0)

    _begin_turn(gs)
    st.rerun()


# ── 엔딩 ─────────────────────────────────────────────────────
elif screen == "ending":
    gs = st.session_state.gs
    stage, _ = get_life_stage(gs.age)
    apply_css(stage)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if gs.alive and gs.life >= 50:
            st.balloons()
            st.markdown("<div class='big-emoji'>🎊</div>", unsafe_allow_html=True)
            st.markdown("<h2 class='center-text'>축 하 합 니 다!</h2>", unsafe_allow_html=True)
            st.success(f"서은주 선생님이 {MAX_AGE}세까지 건강하게 살아오셨습니다.")
            st.markdown("""
<p class='center-text'>당신은 한 생명을 끝까지 책임지고 돌봤습니다.</p>
<p class='center-text'>모든 생명은 소중합니다.<br>당신의 관심과 사랑이 한 사람의 인생을 지켜냈어요. 💖</p>
""", unsafe_allow_html=True)
        elif gs.alive:
            st.markdown("<div class='big-emoji'>📖</div>", unsafe_allow_html=True)
            st.info(f"서은주 선생님은 {MAX_AGE}세까지 살아오셨습니다.")
            st.markdown("<p class='center-text'>힘든 순간도 많았지만, 끝까지 함께해주셨네요.</p>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='big-emoji'>🕯️</div>", unsafe_allow_html=True)
            st.error(f"서은주 선생님은 {gs.age}세에 {gs.death_cause} 세상을 떠나셨습니다.")
            st.markdown("""
<p class='center-text'>조금만 더 신경 썼다면 더 오래 함께할 수 있었을 거예요.</p>
<p class='center-text'>생명은 누군가의 지속적인 관심과 돌봄이 필요합니다.</p>
""", unsafe_allow_html=True)

        st.divider()
        st.markdown("#### 📊 생애 통계")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("함께한 시간",        f"{gs.age}년")
            st.metric("🍚 밥·물 챙긴 횟수", f"{gs.stat_care_count['영양']}번")
            st.metric("💊 건강 챙긴 횟수",  f"{gs.stat_care_count['건강']}번")
            st.metric("✓ 위기 잘 대처",     f"{gs.crisis_handled_well}번")
        with c2:
            st.metric("🌟 건강했던 시기",   f"{gs.good_turns}턴")
            st.metric("🌡️ 안전 보호 횟수",  f"{gs.stat_care_count['안전']}번")
            st.metric("😴 푹 재워준 횟수",  f"{gs.stat_care_count['수면']}번")
            st.metric("✗ 위기 잘못 대처",   f"{gs.crisis_failed}번")

        st.divider()
        st.button("🔄 다시 시작", on_click=cb_start_game, type="primary", use_container_width=True)