import random
import sys
import math
import ctypes
from pathlib import Path

import pygame


pygame.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("서은주 키우기")

if sys.platform == "win32":
    try:
        window_handle = pygame.display.get_wm_info()["window"]
        ctypes.windll.user32.ShowWindow(window_handle, 3)
    except (KeyError, AttributeError, OSError):
        pass

clock = pygame.time.Clock()

FONT_NAME = "malgungothic"
TITLE_FONT = pygame.font.SysFont("malgungothic", 34, bold=True)
START_TITLE_FONT = pygame.font.SysFont("malgungothic", 58, bold=True)
BIG_FONT = pygame.font.SysFont("malgungothic", 26, bold=True)
FONT = pygame.font.SysFont("malgungothic", 21)
SMALL_FONT = pygame.font.SysFont("malgungothic", 15)
TINY_FONT = pygame.font.SysFont("malgungothic", 13)

SCRIPT_DIR = Path(__file__).resolve().parent
FACE_DIR = "seoeunju_faces"
FACE_SEARCH_DIRS = [
    SCRIPT_DIR / FACE_DIR,
    Path.cwd() / FACE_DIR,
    SCRIPT_DIR,
    Path.cwd(),
]
FACE_ALIASES = {
    "baby": ["baby.png"],
    "kid": ["kid.png"],
    "teenager": ["teenager.png"],
    "adult": ["adult.png"],
    "middleage": ["middleage.png"],
    "old age": ["old age.png"],
    "happy": ["happy.png", "haapy.png"],
    "review_happy": ["haapy.png", "happy.png"],
    "review_neutral": ["무표정.png", "normal.png"],
    "review_sad": ["sad.png"],
    "review_despair": ["절망.png", "sad.png"],
    "hungry": ["hungry.png", "sad.png"],
    "sad": ["sad.png"],
    "stress": ["stress.png", "sad.png"],
    "wash": ["wash.png"],
    "sleep": ["sleep.png"],
    "eat_adult": ["eatAdult.png", "eatadult.png"],
    "eat_middleage": ["eatMiddleage.png", "eatmiddle.png"],
    "eat_old age": ["eatOld.png", "eatold.png"],
    "normal": ["adult.png"],
}
FACE_ALIASES["review_neutral"] = ["\ubb34\ud45c\uc815.png", "normal.png"]
FACE_ALIASES["review_despair"] = ["\uc808\ub9dd.png", "sad.png"]
PHONE = pygame.Rect(24, 12, 852, 626)

WHITE = (255, 255, 255)
BLACK = (34, 30, 28)
DARK = (43, 49, 67)
GRAY = (120, 120, 120)
CREAM = (255, 246, 221)
CARD = (255, 252, 241)
LINE = (218, 199, 160)
YELLOW = (245, 198, 75)
ORANGE = (235, 134, 54)
GREEN = (72, 184, 111)
BLUE = (80, 151, 219)
RED = (225, 82, 82)
PURPLE = (146, 102, 205)
BROWN = (117, 75, 45)
PINK = (238, 126, 151)

HOME_ROOMS = ["화장실", "침실", "거실", "부엌"]
OLD_AGE_HOME_ROOMS = ["화장실", "침실", "거실", "부엌", "아기방", "도박방"]
SCHOOL_ROOMS = ["교무실", "반", "교장실"]
HOUR_DURATION_MS = 2000
FADE_DURATION_MS = 550
LESSON_DURATION_MS = 5000
GRADE_INTERVAL_MS = 500
DECAY_INTERVAL_MS = 1600
HUNGER_DECAY_INTERVAL_MS = 3700
EATING_DURATION_MS = 3000
EATING_FRAME_MS = 300
MEMORY_SEQUENCE_LENGTH = 4
MEMORY_SHOW_FRAMES_PER_ITEM = 45
COFFEE_BOOST_DELAY_MS = 10000
COFFEE_CRASH_DURATION_MS = 20000
EVENT_DAY_MS = HOUR_DURATION_MS * 24
MIN_EVENT_GAP_MS = HOUR_DURATION_MS
REPUTATION_RECOVERY_MS = HOUR_DURATION_MS * 4
BOSS_DURATION_MS = 40000
BOSS_STAGE_TWO_MS = 20000
BOSS_FLASH_MS = 900

FOODS = [
    {"name": "빵", "label": "빵", "price": 8, "hunger": 10},
    {"name": "스테이크", "label": "고기", "price": 15, "hunger": 25},
    {"name": "커피", "label": "커피", "price": 10, "hunger": 5, "energy": 20, "coffee": True},
]

SHOP_ITEMS = [
    {"name": "왕관", "label": "왕관", "price": 80},
    {"name": "리본", "label": "리본", "price": 50},
    {"name": "안경", "label": "안경", "price": 60},
    {"name": "수첩", "label": "수첩", "price": 90},
]

GOOD_EVENTS = [
    ("학생에게 칭찬을 받았습니다.", {"reputation": 5}),
    ("성실한 모습이 인정받았습니다.", {"reputation": 7}),
    ("수업 분위기가 좋았습니다.", {"mental_health": 5}),
    ("업무 처리가 빨랐습니다.", {"work": 5}),
    ("동료 교사에게 도움을 받았습니다.", {"mental_health": 6}),
    ("학부모에게 감사 인사를 받았습니다.", {"reputation": 8}),
    ("컨디션이 좋아 하루가 순조로웠습니다.", {"energy": 5}),
    ("깨끗한 모습이 좋은 인상을 주었습니다.", {"reputation": 4}),
    ("학생들과 좋은 추억을 만들었습니다.", {"mental_health": 8}),
    ("노력한 일이 좋은 결과로 돌아왔습니다.", {"reputation": 10}),
]

BAD_EVENTS = [
    ("위생이 낮다는 소문이 돌았습니다.", {"reputation": -8}),
    ("수업 준비가 부족하다는 말이 나왔습니다.", {"reputation": -6}),
    ("피곤해 보인다는 이야기가 퍼졌습니다.", {"reputation": -4}),
    ("업무가 밀렸다는 소문이 생겼습니다.", {"reputation": -7}),
    ("학생과의 관계가 어색해졌습니다.", {"reputation": -5}),
    ("복도에서 좋지 않은 시선을 받았습니다.", {"reputation": -3}),
    ("교무회의에서 지적을 받았습니다.", {"reputation": -9}),
    ("작은 실수가 크게 퍼졌습니다.", {"reputation": -10}),
    ("주변의 오해가 생겼습니다.", {"reputation": -6}),
    ("평소와 다른 모습에 걱정 섞인 소문이 돌았습니다.", {"reputation": -2}),
]

RESIGNATION_EPILOGUES = [
    {"text": "사퇴 후 카페를 차렸지만, 학생보다 진상 손님이 더 많다는 사실을 깨달았습니다.", "mood": "sad"},
    {"text": "학교를 떠난 뒤 매일 늦잠을 잘 수 있게 되었고, 인생 만족도가 급상승했습니다.", "mood": "happy"},
    {"text": "자유를 얻었지만 월급날이 사라졌다는 사실도 함께 깨달았습니다.", "mood": "normal"},
    {"text": "사퇴 후 세계 여행을 꿈꿨지만, 첫 목적지는 동네 마트였습니다.", "mood": "normal"},
    {"text": "학교를 탈출했지만, 단체 카톡방 알림은 여전히 울렸습니다.", "mood": "sad"},
    {"text": "처음엔 행복했지만, 방학이 없는 삶도 생각보다 쉽지 않았습니다.", "mood": "normal"},
    {"text": "교장실을 나서는 순간 세상이 아름다워 보였습니다. 적어도 3일 동안은요.", "mood": "happy"},
    {"text": "사표는 수리되었고, 그녀는 드디어 알람 없이 아침을 맞이했습니다.", "mood": "happy"},
    {"text": "퇴사 후 건강은 좋아졌지만 통장은 조금 슬퍼졌습니다.", "mood": "normal"},
    {"text": "결국 그녀는 학교를 떠났지만, 꿈에서 계속 종례를 하고 있었습니다.", "mood": "sad"},
]

STAT_INFO = {
    "hunger": ("허기", ORANGE),
    "energy": ("에너지", GREEN),
    "mental_health": ("정신건강", PINK),
    "hygiene": ("위생", BLUE),
    "work": ("업무", PURPLE),
}

DEATH_CAUSES = {
    "hunger": "굶주림으로 사망",
    "energy": "탈진으로 사망",
    "mental_health": "우울증으로 사망",
    "hygiene": "위생 악화로 사망",
    "work": "업무 과부하로 사망",
}

face_images = {}
original_face_images = {}
missing_face_notice_shown = False
current_scene = "start"
scene_start_time = pygame.time.get_ticks()
story_audio_stage_index = None
story_audio_channel = None
story_audio_using_music = False
sound_enabled = True
music_volume = 0.55
effects_volume = 0.70
current_background_track = None
START_VARIANTS = ["baby", "kid", "teenager", "adult", "middleage", "old age"]
START_SWITCH_MS = 500
START_BOUNCE_UP_MS = 80
START_BOUNCE_DOWN_MS = 200
START_BOUNCE_HEIGHT = 18
STORY_STAGE_DURATION_MS = 5000
STORY_DURATION_MS = STORY_STAGE_DURATION_MS * 3
ADULT_INTRO_DURATION_MS = 3000
CARE_ACTION_DURATION_MS = 5000
TEEN_AUDIO_DURATION_MS = STORY_STAGE_DURATION_MS
STORY_AUDIO_VOLUME = 0.85
TEEN_AUDIO_VOLUME = 0.35
GROWTH_SCENE_DURATION_MS = 5000
ENDING_STAGE_MS = 3000
ENDING_EVALUATION_MIN_MS = 20000
DEATH_ANIMATION_FRAMES = [
    ("review_happy", 500),
    ("review_neutral", 500),
    ("review_sad", 500),
    ("review_despair", 1000),
]
DEATH_ANIMATION_DURATION_MS = sum(duration for _variant, duration in DEATH_ANIMATION_FRAMES)
LIFE_STAGE_ORDER = ["baby", "kid", "teenager", "adult", "middleage", "old age"]
LIFE_STAGE_LABELS = {
    "baby": "아기",
    "kid": "어린이",
    "teenager": "청소년",
    "adult": "성인",
    "middleage": "중년",
    "old age": "노년",
}
GROWTH_SCENES = {
    "middleage": ("세월이 흘렀습니다.", "중년이 되었습니다."),
    "old age": ("어느덧 긴 시간이 흘렀습니다.", "노년이 되었습니다."),
}
start_animation = {
    "variant_index": 0,
    "last_switch": 0,
    "bounce_start": 0,
    "offset_y": 0,
}

STORY_STAGES = [
    {
        "variant": "baby",
        "title": "아기 침실",
        "colors": ((248, 226, 229), (255, 245, 238), (232, 196, 205)),
        "audio": ["아기 울음.mp3", "baby.mp3", "baby.wav", "baby_voice.wav", "baby_sound.wav"],
        "texts": ["작은 생명이 세상에 태어났습니다.", "작은 생명이 세상에 태어났습니다."],
    },
    {
        "variant": "kid",
        "title": "놀이터",
        "colors": ((218, 239, 216), (249, 239, 172), (125, 193, 230)),
        "audio": ["노는 소리.mp3", "kid.mp3", "kid.wav", "playground.wav", "children.wav", "kids.wav"],
        "texts": ["세상을 배우고 친구를 만났습니다.", "세상을 배우고 친구를 만났습니다."],
    },
    {
        "variant": "teenager",
        "title": "학교 교실",
        "colors": ((224, 235, 246), (255, 251, 226), (121, 148, 125)),
        "audio": ["청소년 소리.mp3", "teenager.mp3", "teenager.wav", "teen.wav", "school.wav", "classroom.wav"],
        "texts": ["어른이 되기 위한 준비를 시작했습니다.", "어른이 되기 위한 준비를 시작했습니다."],
    },
]
STORY_STAGES[0]["texts"] = [
    "\uc791\uc740 \uc0dd\uba85\uc774 \uccab \uc6b8\uc74c\uc73c\ub85c \uc138\uc0c1\uc744 \ub9cc\ub0ac\uc2b5\ub2c8\ub2e4.",
    "\ub0af\uc120 \ube5b\uacfc \uc18c\ub9ac \uc18d\uc5d0\uc11c \ud558\ub8e8\uc529 \uc790\ub77c\ub0ac\uc2b5\ub2c8\ub2e4.",
]
STORY_STAGES[1]["texts"] = [
    "\uc138\uc0c1\uc744 \ubc30\uc6b0\uba70 \uce5c\uad6c\ub4e4\uacfc \uc6c3\ub358 \uc2dc\uc808\uc785\ub2c8\ub2e4.",
    "\uc791\uc740 \uafc8\ub4e4\uc774 \uad50\uc2e4 \ubc16\uc5d0\uc11c \ucee4\uc838\uac14\uc2b5\ub2c8\ub2e4.",
]
STORY_STAGES[2]["texts"] = [
    "\uc5b4\ub978\uc774 \ub418\uae30 \uc704\ud55c \uc900\ube44\uac00 \uc2dc\uc791\ub418\uc5c8\uc2b5\ub2c8\ub2e4.",
    "\uace0\ubbfc\uacfc \uae30\ub300\ub97c \ud488\uace0 \ub2e4\uc74c \uc2dc\uc808\ub85c \uac78\uc5b4\uac14\uc2b5\ub2c8\ub2e4.",
]


def new_game():
    return {
        "location": "home",
        "room": "집",
        "coins": 35,
        "day": 1,
        "hour": 7,
        "hour_elapsed": 0,
        "last_update": pygame.time.get_ticks(),
        "xp": 0,
        "level": 1,
        "title": "신규 교사",
        "reputation": 78,
        "stats": {
            "hunger": 64,
            "energy": 82,
            "mental_health": 82,
            "hygiene": 78,
            "work": 85,
        },
        "owned": [],
        "wearing": "",
        "message": "사진 속 서은주 선생님을 돌봐주세요.",
        "life_stage": "adult",
        "stage_enter_day": 0,
        "ending_type": "",
        "cheat_notice_until": 0,
        "last_random_event": pygame.time.get_ticks(),
        "event_day": 1,
        "daily_event_target": random.randint(1, 10),
        "today_event_count": 0,
        "next_random_event_at": 0,
        "last_reputation_recovery": pygame.time.get_ticks(),
        "nursery_care_count": 0,
        "nursery_special_count": 0,
        "ending_controls_revealed": False,
        "sleeping": False,
        "eating": {"active": False, "elapsed": 0, "food": None},
        "coffee_count_day": 1,
        "coffee_count": 0,
        "coffee_penalty": {"delay": 0, "remaining_ms": 0, "amount": 0, "tick": 0},
        "care_action": {"type": None, "elapsed": 0},
        "game_over": False,
        "death_animation_done": False,
        "settings_open": False,
        "boss_test_confirm": False,
        "boss_test_notice_until": 0,
        "paused_at": 0,
        "transition": None,
        "resignation_event": None,
        "resignation_epilogue": "",
        "resignation_epilogue_mood": "happy",
        "lesson": {"active": False, "elapsed": 0, "notes": [], "doodle": ""},
        "office_work": {"active": False, "phase": "", "kind": "", "elapsed": 0, "scores": [], "students": [], "documents_done": 0},
        "boss": {"active": False, "elapsed": 0, "x": WIDTH // 2, "hits": 0, "obstacles": [], "spawn": 0, "phase": "fight", "flash": 0},
        "gamble_bet": 10,
        "last_resignation_attempt_day": 0,
        "death_cause": "",
        "final_stats": None,
        "final_reputation": 0,
        "last_decay": 0,
        "hunger_decay_elapsed": 0,
        "effect": None,
        "effect_start": 0,
        "effect_until": 0,
        "mini": {
            "active": False,
            "type": "",
            "timer": 0,
            "score": 0,
            "attempts": 0,
            "total_spawned": 0,
            "papers": [],
            "spawn": 0,
            "target": None,
            "target_timer": 0,
            "sequence": [],
            "sequence_index": 0,
            "show_sequence": True,
            "show_timer": 0,
            "input_options": [],
        },
    }


game = new_game()


def clamp(value):
    return max(0, min(100, int(value)))


def calculate_reputation():
    return clamp(game["reputation"])


def change_reputation(amount):
    game["reputation"] = clamp(game["reputation"] + amount)


def draw_text(label, font, color, x, y, center=False):
    image = font.render(str(label), True, color)
    rect = image.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(image, rect)
    return rect


def draw_text_alpha(label, font, color, x, y, alpha, center=False):
    image = font.render(str(label), True, color).convert_alpha()
    image.set_alpha(max(0, min(255, int(alpha))))
    rect = image.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(image, rect)
    return rect


def wrap_text(text, font, max_width):
    words = str(text).split()
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else f"{current} {word}"
        if font.size(candidate)[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines or [""]


def rounded(rect, color, radius=18, border=None, width=0):
    pygame.draw.rect(screen, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(screen, border, rect, width, border_radius=radius)


def change_scene(scene):
    global current_scene, scene_start_time
    current_scene = scene
    scene_start_time = pygame.time.get_ticks()
    update_background_music(scene)


def start_story():
    global game, story_audio_stage_index
    game = new_game()
    story_audio_stage_index = None
    change_scene("story")


def start_adult_intro():
    stop_story_audio()
    change_scene("adult_intro")


def start_guide():
    change_scene("guide")


def start_game():
    now = pygame.time.get_ticks()
    game["last_decay"] = now
    game["last_update"] = now
    game["last_random_event"] = now
    game["event_day"] = game["day"]
    game["daily_event_target"] = random.randint(1, 10)
    game["today_event_count"] = 0
    schedule_next_random_event(now)
    game["last_reputation_recovery"] = now
    change_scene("game")


def finish_life(ending_type, cause):
    game["game_over"] = True
    game["ending_type"] = ending_type
    game["death_cause"] = cause
    game["death_animation_done"] = False
    game["final_stats"] = game["stats"].copy()
    game["final_reputation"] = calculate_reputation()
    game["ending_controls_revealed"] = False
    game["sleeping"] = False
    game["care_action"] = {"type": None, "elapsed": 0}
    game["eating"] = {"active": False, "elapsed": 0, "food": None}
    game["resignation_event"] = None
    game["resignation_epilogue"] = ""
    game["resignation_epilogue_mood"] = "happy"
    game["transition"] = None
    game["mini"]["active"] = False
    game["lesson"] = {"active": False, "elapsed": 0, "notes": [], "doodle": ""}
    game["office_work"] = {"active": False, "phase": "", "kind": "", "elapsed": 0, "scores": [], "students": [], "documents_done": 0}


def begin_death_transition():
    game["death_animation_done"] = True
    change_scene("death_transition")


def begin_growth(stage):
    game["life_stage"] = stage
    game["stage_enter_day"] = game["day"]
    if stage == "old age":
        game["location"] = "home"
        game["room"] = "집"
    game["sleeping"] = False
    game["care_action"] = {"type": None, "elapsed": 0}
    game["eating"] = {"active": False, "elapsed": 0, "food": None}
    game["effect"] = None
    game["transition"] = None
    game["resignation_event"] = None
    game["resignation_epilogue"] = ""
    game["resignation_epilogue_mood"] = "happy"
    game["mini"]["active"] = False
    game["lesson"] = {"active": False, "elapsed": 0, "notes": [], "doodle": ""}
    game["office_work"] = {"active": False, "phase": "", "kind": "", "elapsed": 0, "scores": [], "students": [], "documents_done": 0}
    change_scene("growth")


def check_growth_progress():
    stage = game["life_stage"]
    days_in_stage = game["day"] - game["stage_enter_day"]
    if stage == "adult" and days_in_stage >= 10:
        begin_growth("middleage")
    elif stage == "middleage" and days_in_stage >= 5:
        begin_growth("old age")
    elif stage == "old age" and days_in_stage >= 5:
        finish_life("clear", "노년까지 삶을 완주했습니다.")
        change_scene("life_review")


def skip_test_day():
    game["day"] += 1
    reset_daily_events(pygame.time.get_ticks())
    game["message"] = "테스트 치트: 하루가 경과했습니다."
    game["cheat_notice_until"] = pygame.time.get_ticks() + 1800
    check_growth_progress()


def restart_game():
    global game
    game = new_game()
    start_game()


def reset_to_start():
    global game, story_audio_stage_index
    stop_story_audio()
    game = new_game()
    story_audio_stage_index = None
    start_animation["last_switch"] = 0
    change_scene("start")


def set_sound_enabled(enabled):
    global sound_enabled
    sound_enabled = enabled
    if not pygame.mixer.get_init():
        return
    pygame.mixer.music.set_volume(music_volume if enabled else 0)
    if story_audio_channel:
        stage_volume = TEEN_AUDIO_VOLUME if story_audio_stage_index == 2 else STORY_AUDIO_VOLUME
        story_audio_channel.set_volume(stage_volume * effects_volume if enabled else 0)


def open_settings(now):
    if game["settings_open"]:
        return
    game["settings_open"] = True
    game["paused_at"] = now


def close_settings(now):
    if not game["settings_open"]:
        return
    paused_duration = now - game["paused_at"]
    game["settings_open"] = False
    game["last_decay"] += paused_duration
    game["last_random_event"] += paused_duration
    if game.get("next_random_event_at"):
        game["next_random_event_at"] += paused_duration
    game["last_reputation_recovery"] += paused_duration
    game["last_update"] = now
    if game["effect"]:
        game["effect_start"] += paused_duration
        game["effect_until"] += paused_duration


def start_location_transition(location, room):
    if game["transition"] or game["settings_open"]:
        return
    game["transition"] = {
        "location": location,
        "room": room,
        "phase": "out",
        "elapsed": 0,
    }


def update_location_transition(delta_ms):
    transition = game["transition"]
    if not transition:
        return
    transition["elapsed"] += delta_ms
    if transition["elapsed"] < FADE_DURATION_MS:
        return
    if transition["phase"] == "out":
        game["location"] = transition["location"]
        game["room"] = transition["room"]
        game["sleeping"] = False
        transition["phase"] = "in"
        transition["elapsed"] = 0
    else:
        game["transition"] = None


def reset_daily_events(now):
    game["event_day"] = game["day"]
    game["daily_event_target"] = random.randint(1, 10)
    game["today_event_count"] = 0
    game["last_random_event"] = now
    schedule_next_random_event(now)
    game["coffee_count_day"] = game["day"]
    game["coffee_count"] = 0
    game["coffee_penalty"] = {"delay": 0, "remaining_ms": 0, "amount": 0, "tick": 0}


def schedule_next_random_event(now):
    remaining = max(0, game["daily_event_target"] - game["today_event_count"])
    if remaining <= 0:
        game["next_random_event_at"] = 0
        return
    elapsed_today = game["hour"] * HOUR_DURATION_MS + game["hour_elapsed"]
    remaining_day = max(MIN_EVENT_GAP_MS, EVENT_DAY_MS - elapsed_today)
    max_delay = max(MIN_EVENT_GAP_MS, remaining_day // remaining)
    delay = random.randint(MIN_EVENT_GAP_MS, max_delay)
    game["next_random_event_at"] = now + delay


def update_game_clock(delta_ms):
    game["hour_elapsed"] += delta_ms
    while game["hour_elapsed"] >= HOUR_DURATION_MS:
        game["hour_elapsed"] -= HOUR_DURATION_MS
        game["hour"] += 1
        if game["hour"] >= 24:
            game["hour"] = 0
            game["day"] += 1
            reset_daily_events(pygame.time.get_ticks())
            check_growth_progress()
            if current_scene != "game":
                return


def elapsed_in_scene(now):
    return now - scene_start_time


def find_audio_file(names):
    candidates = []
    directories = unique_paths([SCRIPT_DIR, Path.cwd()])
    for directory in directories:
        for name in names:
            candidates.append(directory / name)
    for path in unique_paths(candidates):
        if path.is_file():
            return path

    keywords = [Path(name).stem.lower().replace("_", " ").replace("-", " ") for name in names]
    for directory in directories:
        if not directory.is_dir():
            continue
        audio_files = []
        for extension in ("*.mp3", "*.wav", "*.ogg"):
            audio_files.extend(sorted(directory.glob(extension)))
        for path in audio_files:
            stem = path.stem.lower().replace("_", " ").replace("-", " ")
            if any(keyword and keyword in stem for keyword in keywords):
                return path
    return None


def ensure_audio_ready():
    if pygame.mixer.get_init():
        return True
    try:
        pygame.mixer.init()
        return True
    except pygame.error as error:
        print(f"오디오 초기화 실패: {error}")
        return False


def update_background_music(scene):
    global current_background_track
    if not ensure_audio_ready():
        return
    track_name = "끝나는음악.mp3" if scene in ("life_review", "resignation_ending") else "기본음악.mp3"
    path = SCRIPT_DIR / track_name
    if not path.is_file() or current_background_track == track_name:
        pygame.mixer.music.set_volume(music_volume if sound_enabled else 0)
        return
    try:
        pygame.mixer.music.load(str(path))
        pygame.mixer.music.set_volume(music_volume if sound_enabled else 0)
        pygame.mixer.music.play(loops=-1)
        current_background_track = track_name
    except (pygame.error, OSError) as error:
        print(f"배경음악 재생 실패: {path} / {error}")


def stop_story_audio():
    global story_audio_channel, story_audio_using_music
    if not pygame.mixer.get_init():
        story_audio_channel = None
        story_audio_using_music = False
        return
    if story_audio_channel:
        story_audio_channel.stop()
        story_audio_channel = None
    story_audio_using_music = False


def play_story_audio(stage_index):
    global story_audio_stage_index, story_audio_channel, story_audio_using_music
    if story_audio_stage_index == stage_index:
        return

    stop_story_audio()
    story_audio_stage_index = stage_index
    path = find_audio_file(STORY_STAGES[stage_index].get("audio", []))
    if path is None:
        print(f"프롤로그 음성 파일 없음: {STORY_STAGES[stage_index].get('audio', [])}")
        return
    if not ensure_audio_ready():
        return

    try:
        volume = TEEN_AUDIO_VOLUME if stage_index == 2 else STORY_AUDIO_VOLUME
        sound = pygame.mixer.Sound(str(path))
        sound.set_volume(volume * effects_volume if sound_enabled else 0)
        story_audio_channel = sound.play(loops=-1)
        print(f"프롤로그 음성 재생: {path.name}")
    except (pygame.error, OSError) as error:
        print(f"프롤로그 음성 재생 실패: {path} / {error}")
        story_audio_channel = None
        story_audio_using_music = False


def circle_button(center, radius, label, sublabel, mouse, selected=False):
    x, y = center
    base = ORANGE if selected else CREAM
    if (mouse[0] - x) ** 2 + (mouse[1] - y) ** 2 <= radius ** 2:
        base = tuple(min(255, c + 18) for c in base)
    pygame.draw.circle(screen, (0, 0, 0, 45), (x + 3, y + 4), radius)
    pygame.draw.circle(screen, base, (x, y), radius)
    pygame.draw.circle(screen, (166, 119, 54), (x, y), radius, 2)
    draw_text(label, FONT, BLACK, x, y - 5, center=True)
    draw_text(sublabel, TINY_FONT, BROWN, x, y + 16, center=True)


def choose_face_variant(effect):
    if effect in ("sleep", "wash", "sad", "stress"):
        return effect
    if effect in ("work", "grade"):
        return "stress"
    if effect in ("eat", "home", "shop", "wake", "game", "pop"):
        return "happy"
    return "adult"


def unique_paths(paths):
    seen = set()
    result = []
    for path in paths:
        resolved = path.resolve() if path.exists() else path.absolute()
        key = str(resolved).lower()
        if key not in seen:
            seen.add(key)
            result.append(path)
    return result


def find_face_file(variant):
    names = []
    names.extend(FACE_ALIASES.get(variant, [f"{variant}.png"]))
    if f"{variant}.png" not in names:
        names.append(f"{variant}.png")
    names.extend(["normal.png", "image.png"])

    candidates = []
    for directory in FACE_SEARCH_DIRS:
        for name in names:
            candidates.append(directory / name)
    for path in unique_paths(candidates):
        if path.is_file():
            return path

    for directory in FACE_SEARCH_DIRS:
        if directory.is_dir():
            png_files = sorted(directory.glob("*.png"))
            if png_files:
                return png_files[0]
    return None


def make_placeholder_photo():
    photo = pygame.Surface((268, 334), pygame.SRCALPHA)
    photo.fill((245, 224, 198, 255))
    pygame.draw.ellipse(photo, (240, 191, 157), (18, 12, 232, 294))
    pygame.draw.ellipse(photo, (80, 60, 45), (72, 132, 28, 18))
    pygame.draw.ellipse(photo, (80, 60, 45), (168, 132, 28, 18))
    pygame.draw.arc(photo, (120, 70, 60), (88, 198, 92, 46), 0.2, 2.9, 4)
    pygame.draw.rect(photo, (218, 199, 160), (0, 0, 267, 333), 4)
    return photo


def get_teacher_pet_photo_legacy(variant):
    if variant in face_images:
        return face_images[variant]

    path = f"{FACE_DIR}/{variant}.png"
    try:
        photo = pygame.image.load(path).convert_alpha()
    except pygame.error:
        if variant != "normal":
            return get_teacher_pet_photo("normal")
        game["message"] = "표정 PNG 파일을 찾지 못했습니다."
        return None

    face_images[variant] = pygame.transform.smoothscale(photo, (268, 334))
    return face_images[variant]


def get_teacher_pet_photo(variant):
    global missing_face_notice_shown

    if variant in face_images:
        return face_images[variant]

    path = find_face_file(variant)
    if path is not None:
        try:
            photo = pygame.image.load(str(path)).convert_alpha()
        except (FileNotFoundError, OSError, pygame.error):
            photo = make_placeholder_photo()
    else:
        photo = make_placeholder_photo()

    if path is None and not missing_face_notice_shown:
        game["message"] = "PNG 파일을 찾지 못해 기본 그림으로 실행합니다."
        missing_face_notice_shown = True

    face_images[variant] = pygame.transform.smoothscale(photo, (268, 334))
    return face_images[variant]


def get_original_face_photo(variant):
    if variant in original_face_images:
        return original_face_images[variant]
    path = find_face_file(variant)
    if path is None:
        return None
    try:
        image = pygame.image.load(str(path)).convert_alpha()
    except (FileNotFoundError, OSError, pygame.error):
        return None
    original_face_images[variant] = image
    return image


def contain_surface(image, bounds):
    scale = min(bounds.width / image.get_width(), bounds.height / image.get_height())
    size = (max(1, round(image.get_width() * scale)), max(1, round(image.get_height() * scale)))
    fitted = pygame.transform.smoothscale(image, size)
    return fitted, fitted.get_rect(center=bounds.center)


def apply_changes(changes):
    for key, amount in changes.items():
        if key in game["stats"]:
            game["stats"][key] = clamp(game["stats"][key] + amount)
        elif key == "reputation":
            change_reputation(amount)


def start_effect(name, duration=2000):
    """짧게 표시할 표정/행동 이펙트를 예약합니다."""
    now = pygame.time.get_ticks()
    game["effect"] = name
    game["effect_start"] = now
    game["effect_until"] = now + duration


def active_effect(now):
    if game["sleeping"]:
        return "sleep"
    if game["effect"] and now <= game["effect_until"]:
        return game["effect"]
    game["effect"] = None
    if game["mini"]["active"]:
        return "game"
    return None


def is_action_visual_locked():
    return (
        game["sleeping"]
        or game["care_action"]["type"]
        or game["eating"]["active"]
        or game["mini"]["active"]
        or game["lesson"]["active"]
        or game["office_work"]["active"]
    )


def character_motion(effect, now):
    """버튼을 눌렀을 때 잠깐 흠칫하거나 통통 튀는 움직임만 줍니다."""
    if not effect:
        return 0, 0

    elapsed = now - game.get("effect_start", now)
    if game["sleeping"]:
        return 0, int(math.sin(now / 520) * 2)
    if effect == "eat" and game["eating"]["active"]:
        return 0, int(-7 * abs(math.sin(elapsed / 150 * math.pi)))
    if effect == "pop":
        if elapsed > 560:
            return 0, 0
        t = elapsed / 560
        return 0, int(-18 * abs(math.sin(math.pi * 2.5 * t)) * (1 - t * 0.45))
    if elapsed > 320:
        return 0, 0

    t = elapsed / 320
    pop = int(-10 * math.sin(math.pi * t))
    shake = 0
    if effect in ("work", "grade"):
        shake = int(math.sin(elapsed / 22) * (1 - t) * 7)
    elif effect in ("eat", "home", "shop", "wake", "wash"):
        pop = int(-8 * math.sin(math.pi * t))
    return shake, pop


def update_level():
    coins = game["coins"]
    if coins >= 900:
        game["level"], game["title"] = 5, "부장교사"
    elif coins >= 500:
        game["level"], game["title"] = 4, "수행평가의 신"
    elif coins >= 250:
        game["level"], game["title"] = 3, "생활지도 마스터"
    elif coins >= 100:
        game["level"], game["title"] = 2, "담임 교사"
    else:
        game["level"], game["title"] = 1, "신규 교사"


def gain_xp(amount):
    game["xp"] += amount
    need = game["level"] * 45
    if game["xp"] >= need:
        game["xp"] -= need


def check_game_over():
    if game["game_over"]:
        return

    if game["reputation"] <= 0:
        finish_life("reputation_death", "주변의 모함과 비난으로 인해 무너졌습니다.")
        game["message"] = "계속된 스트레스 속에서 삶을 포기했습니다."
        return

    for key in STAT_INFO:
        if game["stats"][key] <= 0:
            finish_life("death", DEATH_CAUSES[key])
            game["message"] = game["death_cause"]
            return


def update_random_events(now):
    if game["game_over"]:
        return
    if game["transition"]:
        return
    if game["resignation_event"]:
        return
    if game.get("event_day") != game["day"]:
        reset_daily_events(now)
    if game["today_event_count"] >= game["daily_event_target"]:
        return
    if not game["next_random_event_at"] or now < game["next_random_event_at"]:
        return

    game["last_random_event"] = now
    game["today_event_count"] += 1
    message, effects = random.choice(GOOD_EVENTS + BAD_EVENTS)
    apply_changes(effects)
    game["message"] = f"랜덤 이벤트: {message}"
    if not is_action_visual_locked():
        start_effect("pop" if effects.get("reputation", 0) >= 0 else "stress", 1800)
    check_game_over()
    schedule_next_random_event(now)


def update_reputation_recovery(now):
    if game["game_over"] or now - game["last_reputation_recovery"] < REPUTATION_RECOVERY_MS:
        return
    game["last_reputation_recovery"] = now
    if min(game["stats"].values()) < 40 or game["reputation"] >= 100:
        return
    change_reputation(1)
    game["message"] = "시간이 지나며 평판이 조금 회복되었습니다."


def decay(now):
    if game["game_over"] or game["mini"]["active"] or game["care_action"]["type"] or game["eating"]["active"]:
        return
    elapsed = now - game["last_decay"]
    if elapsed < DECAY_INTERVAL_MS:
        return
    game["last_decay"] = now

    if game["sleeping"]:
        changes = {"energy": 4, "hygiene": -1}
    else:
        changes = {"energy": -1, "mental_health": -1, "work": -1, "hygiene": -1}
    game["hunger_decay_elapsed"] += elapsed
    if game["hunger_decay_elapsed"] >= HUNGER_DECAY_INTERVAL_MS:
        hunger_ticks = game["hunger_decay_elapsed"] // HUNGER_DECAY_INTERVAL_MS
        game["hunger_decay_elapsed"] %= HUNGER_DECAY_INTERVAL_MS
        changes["hunger"] = -2 * hunger_ticks
    apply_changes(changes)

    check_game_over()


def feed(index):
    if game["eating"]["active"]:
        return
    food = FOODS[index]
    if game["coins"] < food["price"]:
        game["message"] = "코인이 부족합니다."
        return
    game["coins"] -= food["price"]
    game["eating"] = {"active": True, "elapsed": 0, "food": food}
    game["message"] = f"{food['name']}을(를) 먹는 중입니다..."
    start_effect("eat", EATING_DURATION_MS)


def update_eating(delta_ms):
    eating = game["eating"]
    if not eating["active"]:
        return
    eating["elapsed"] += delta_ms
    if eating["elapsed"] < EATING_DURATION_MS:
        return

    food = eating["food"]
    if food.get("coffee"):
        handle_coffee_drink()
        if game["game_over"]:
            game["eating"] = {"active": False, "elapsed": 0, "food": None}
            game["effect"] = None
            return
    else:
        apply_changes({
            "hunger": food.get("hunger", 0),
            "energy": food.get("energy", 0),
            "mental_health": food.get("mental_health", 0),
        })
    game["eating"] = {"active": False, "elapsed": 0, "food": None}
    game["effect"] = None
    gain_xp(7)
    update_level()
    check_game_over()
    game["message"] = f"{food['name']} 섭취 완료!"


def handle_coffee_drink():
    if game["coffee_count_day"] != game["day"]:
        game["coffee_count_day"] = game["day"]
        game["coffee_count"] = 0
    game["coffee_count"] += 1
    count = game["coffee_count"]
    if count >= 5:
        apply_changes({"hunger": 5})
        finish_life("death", "카페인 과다 복용으로 사망")
        game["message"] = "카페인 과다 복용으로 쓰러졌습니다."
        return
    energy_gain = 10 if count == 3 else 20
    apply_changes({"hunger": 5, "energy": energy_gain})
    if count == 3:
        game["coffee_penalty"] = {"delay": COFFEE_BOOST_DELAY_MS, "remaining_ms": COFFEE_CRASH_DURATION_MS, "amount": 20, "tick": 0}
        game["message"] = "커피를 너무 많이 마셨습니다. 곧 기운이 빠질 수 있습니다."
    elif count == 4:
        game["coffee_penalty"] = {"delay": 0, "remaining_ms": COFFEE_CRASH_DURATION_MS, "amount": 30, "tick": 0}
        game["message"] = "카페인이 과합니다. 에너지가 서서히 떨어집니다."


def update_coffee_penalty(delta_ms):
    penalty = game["coffee_penalty"]
    if penalty["delay"] > 0:
        penalty["delay"] = max(0, penalty["delay"] - delta_ms)
        return
    if penalty["remaining_ms"] <= 0 or penalty["amount"] <= 0:
        return
    penalty["remaining_ms"] = max(0, penalty["remaining_ms"] - delta_ms)
    penalty["tick"] += delta_ms
    interval = max(1, COFFEE_CRASH_DURATION_MS // max(1, penalty["amount"]))
    while penalty["tick"] >= interval and penalty["amount"] > 0:
        penalty["tick"] -= interval
        penalty["amount"] -= 1
        apply_changes({"energy": -1})
    check_game_over()


def start_care_action(action_type):
    if game["care_action"]["type"]:
        return
    if action_type == "sleep" and not (game["hour"] >= 22 or game["hour"] <= 6):
        game["message"] = "지금은 잘 시간이 아닙니다."
        return
    game["care_action"] = {"type": action_type, "elapsed": 0}
    if action_type == "sleep":
        game["sleeping"] = True
        game["message"] = "잠자는 중입니다..."
    else:
        game["message"] = "씻는 중입니다..."
    start_effect(action_type, CARE_ACTION_DURATION_MS)


def update_care_action(delta_ms):
    action = game["care_action"]
    if not action["type"]:
        return
    action["elapsed"] += delta_ms
    if action["elapsed"] < CARE_ACTION_DURATION_MS:
        return

    action_type = action["type"]
    game["care_action"] = {"type": None, "elapsed": 0}
    game["effect"] = None
    if action_type == "sleep":
        game["sleeping"] = False
        apply_changes({"energy": 30, "mental_health": 5})
        game["message"] = "푹 자고 일어났습니다. 에너지와 정신건강이 회복되었습니다."
        start_effect("wake", 1200)
    else:
        apply_changes({"hygiene": 35})
        game["message"] = "깨끗하게 씻었습니다. 위생이 회복되었습니다."
        start_effect("wake", 1200)
    gain_xp(5)
    update_level()
    check_game_over()


def office_action(kind):
    if kind == "class":
        reward = random.randint(5, 20)
        game["coins"] += reward
        apply_changes({"work": 15, "mental_health": -10, "energy": -5})
        change_reputation(5)
        game["message"] = f"수업 완료! {reward}C를 벌었습니다. 평판이 올랐습니다."
        start_effect("work")
    elif kind == "grade":
        reward = random.randint(5, 20)
        game["coins"] += reward
        apply_changes({"mental_health": -25, "energy": -15, "work": 20})
        change_reputation(5)
        game["message"] = f"업무 완료! {reward}C를 벌었습니다. 평판이 올랐습니다."
        start_effect("grade", 2000)
    gain_xp(9)
    update_level()
    check_game_over()


def start_lesson():
    if game["lesson"]["active"]:
        return
    lesson_sets = [
        ["오늘의 목표: 개념 이해하기", "예제 문제 풀이", "질문하고 답하기", "수행평가 안내"],
        ["핵심 단어 정리", "짝 활동으로 확인하기", "틀린 문제 다시 보기", "마무리 퀴즈"],
        ["지난 시간 복습", "새 개념 설명", "칠판 문제 풀기", "오늘 배운 점 쓰기"],
        ["모둠 토의 시작", "발표 내용 정리", "질문 카드 작성", "다음 시간 예고"],
    ]
    doodles = ["작은 별", "하트", "웃는 얼굴", "x + y = ?", "학생 낙서"]
    game["lesson"] = {"active": True, "elapsed": 0, "notes": random.choice(lesson_sets), "doodle": random.choice(doodles)}
    game["message"] = "수업을 시작합니다."


def update_lesson(delta_ms):
    lesson = game["lesson"]
    if not lesson["active"]:
        return
    lesson["elapsed"] += delta_ms
    if lesson["elapsed"] < LESSON_DURATION_MS:
        return
    lesson["active"] = False
    reward = random.randint(5, 20)
    game["coins"] += reward
    apply_changes({"work": 20, "energy": -5, "mental_health": -10})
    change_reputation(5)
    gain_xp(9)
    game["message"] = f"수업 완료! {reward}C를 벌었습니다. 수업을 성실히 진행해 평판이 올랐습니다."
    check_game_over()


def start_office_work():
    if game["office_work"]["active"]:
        return
    kind = random.choice(["grades", "documents"])
    if kind == "grades":
        game["office_work"] = {"active": True, "phase": "desktop", "kind": "grades", "elapsed": 0, "scores": [], "students": [], "documents_done": 0}
        game["message"] = "컴퓨터에서 성적 처리 앱을 실행하세요."
    else:
        game["office_work"] = {"active": True, "phase": "documents", "kind": "documents", "elapsed": 0, "scores": [], "students": [], "documents_done": 0}
        game["message"] = "문서 정리를 시작합니다."


def grade_app_button():
    return pygame.Rect(PHONE.centerx - 68, 325, 136, 92)


def open_grade_app():
    work = game["office_work"]
    if not work["active"] or work["phase"] != "desktop":
        return
    work["phase"] = "grades"
    work["elapsed"] = 0
    work["scores"] = []
    work["students"] = ["김학생", "이학생", "박학생", "최학생", "정학생"]
    game["message"] = "학생 성적을 자동 입력하고 있습니다."


def update_office_work(delta_ms):
    work = game["office_work"]
    if not work["active"]:
        return
    work["elapsed"] += delta_ms
    if work["phase"] == "grades":
        expected_count = min(5, work["elapsed"] // GRADE_INTERVAL_MS)
        while len(work["scores"]) < expected_count:
            work["scores"].append(random.randint(50, 100))
        if len(work["scores"]) < 5 or work["elapsed"] < GRADE_INTERVAL_MS * 6:
            return
    elif work["phase"] == "documents":
        work["documents_done"] = min(6, work["elapsed"] // GRADE_INTERVAL_MS)
        if work["documents_done"] < 6 or work["elapsed"] < GRADE_INTERVAL_MS * 7:
            return
    else:
        return
    reward = random.randint(5, 20)
    game["office_work"] = {"active": False, "phase": "", "kind": "", "elapsed": 0, "scores": [], "students": [], "documents_done": 0}
    game["coins"] += reward
    apply_changes({"work": 20, "energy": -8, "mental_health": -10})
    change_reputation(5)
    gain_xp(10)
    game["message"] = f"업무 완료! {reward}C를 벌었습니다. 성실한 업무 처리로 평판이 올랐습니다."
    check_game_over()


def commute():
    if game["location"] == "home":
        if game["life_stage"] == "old age":
            game["message"] = "나이가 들어 더 이상 학교에 나갈 수 없습니다."
            return
        game["message"] = "학교로 출근합니다."
        start_effect("stress", 1500)
        start_location_transition("school", "학교")
    else:
        game["message"] = "집으로 퇴근합니다."
        apply_changes({"energy": -2})
        start_effect("home", 1500)
        start_location_transition("home", "집")


def play_gamble(choice):
    bet = game.get("gamble_bet", 10)
    if game["coins"] < bet:
        game["message"] = "코인이 부족합니다."
        return
    result = random.choice(["홀", "짝"])
    if result == choice:
        game["coins"] += bet
        game["message"] = f"{result}! 도박 성공으로 {bet * 2}C를 받았습니다."
        start_effect("pop", 1000)
    else:
        game["coins"] -= bet
        game["message"] = f"{result}! 도박 실패로 {bet}C를 잃었습니다."
        start_effect("stress", 1000)
    update_level()


def apply_mini_game_result(accuracy):
    if accuracy >= 90:
        change = 40
        message = "정말 뛰어난 실력이었습니다. 게임을 잘해서 기분이 좋습니다."
    elif accuracy >= 70:
        change = 30
        message = "게임을 잘해서 기분이 좋습니다."
    elif accuracy >= 50:
        change = 10
        message = "무난하게 즐겼습니다."
    else:
        change = -10
        message = "게임을 못해서 화가 났습니다."
    apply_changes({"mental_health": change})
    game["message"] = f"정답률 {accuracy}% - {message}"
    game["effect"] = None
    check_game_over()


def nursery_care():
    if game["life_stage"] != "old age":
        return
    game["nursery_care_count"] += 1
    apply_changes({"reputation": 6, "mental_health": 10})
    special_events = [
        "손주의 첫 걸음을 보았습니다.",
        "손주가 처음으로 할머니라고 불렀습니다.",
        "가족과 행복한 시간을 보냈습니다.",
    ]
    if random.random() < 0.25:
        game["nursery_special_count"] += 1
        apply_changes({"reputation": 4, "mental_health": 5})
        game["message"] = random.choice(special_events)
    else:
        game["message"] = "손주를 정성껏 돌보며 따뜻한 시간을 보냈습니다."
    start_effect("pop", 1600)
    check_game_over()


def attempt_resignation():
    if game["last_resignation_attempt_day"] == game["day"]:
        game["message"] = "오늘은 이미 시도했습니다."
        return

    game["last_resignation_attempt_day"] = game["day"]
    game["resignation_event"] = {
        "phase": "choose",
        "elapsed": 0,
        "success": None,
        "player": None,
        "principal": "?",
    }


def choose_resignation_hand(player):
    event = game["resignation_event"]
    if not event or event["phase"] != "choose":
        return

    beats = {"가위": "보", "바위": "가위", "보": "바위"}
    loses_to = {loser: winner for winner, loser in beats.items()}
    success = random.random() < 0.10
    if success:
        principal = beats[player]
    else:
        principal = loses_to[player]
    event.update({
        "phase": "result",
        "elapsed": 0,
        "success": success,
        "player": player,
        "principal": principal,
    })


def update_resignation_event(delta_ms):
    event = game["resignation_event"]
    if not event:
        return
    if event["phase"] != "result":
        return
    event["elapsed"] += delta_ms
    if event["elapsed"] < 2200:
        return

    game["resignation_event"] = None
    if event["success"]:
        game["message"] = "학교 탈출 성공"
        start_resignation_boss()
        return

    change_reputation(-10)
    game["message"] = "사퇴를 시도해 시선이 안 좋아집니다."
    start_effect("stress", 1800)
    check_game_over()


def choose_resignation_epilogue():
    epilogue = random.choice(RESIGNATION_EPILOGUES)
    return epilogue["text"], epilogue["mood"]


def choose_resignation_epilogue_by_hits(hits):
    if hits <= 1:
        pool = [item for item in RESIGNATION_EPILOGUES if item["mood"] == "happy"]
        fallback_mood = "happy"
    elif hits <= 3:
        pool = [item for item in RESIGNATION_EPILOGUES if item["mood"] == "normal"]
        fallback_mood = "normal"
    else:
        pool = [item for item in RESIGNATION_EPILOGUES if item["mood"] == "sad"]
        fallback_mood = "sad"
    epilogue = random.choice(pool or RESIGNATION_EPILOGUES)
    return epilogue["text"], epilogue.get("mood", fallback_mood)


def start_resignation_boss(test_mode=False):
    move_area = boss_move_area()
    game["boss"] = {
        "active": True,
        "elapsed": 0,
        "x": WIDTH // 2,
        "y": move_area.bottom - 44,
        "hits": 0,
        "obstacles": [],
        "spawn": 0,
        "phase": "fight",
        "flash": 0,
        "stage_notice": 0,
        "was_stage_two": False,
        "test_notice": 1000 if test_mode else 0,
    }
    change_scene("resignation_boss")


def boss_move_area():
    return pygame.Rect(PHONE.left + 92, PHONE.top + 330, PHONE.width - 184, PHONE.height - 420)


def laser_swing_points(obstacle):
    progress = min(1.0, obstacle.get("active", 0) / obstacle.get("duration", 2200))
    if obstacle["side"] == "left":
        angle = math.radians(progress * 90)
        pivot = (PHONE.left + 52, PHONE.top + 135)
    else:
        angle = math.radians(180 - progress * 90)
        pivot = (PHONE.right - 52, PHONE.top + 135)
    length = obstacle.get("length", 610)
    end = (
        pivot[0] + math.cos(angle) * length,
        pivot[1] + math.sin(angle) * length,
    )
    return pivot, end


def point_to_segment_distance(point, start, end):
    px, py = point
    sx, sy = start
    ex, ey = end
    dx = ex - sx
    dy = ey - sy
    length_sq = dx * dx + dy * dy
    if length_sq == 0:
        return math.hypot(px - sx, py - sy)
    t = max(0.0, min(1.0, ((px - sx) * dx + (py - sy) * dy) / length_sq))
    closest_x = sx + t * dx
    closest_y = sy + t * dy
    return math.hypot(px - closest_x, py - closest_y)


def spawn_boss_attack(stage):
    attacks = []
    if stage == 1:
        kind = random.choice(["paper", "chalk", "stamp"])
        attacks.append({
            "kind": kind,
            "x": random.randint(PHONE.left + 60, PHONE.right - 60),
            "y": PHONE.top + 120,
            "vx": random.uniform(-1.3, 1.3) if kind == "chalk" else 0,
            "vy": random.randint(4, 7),
            "warn": 0,
        })
    else:
        kind = random.choice(["paper_rain", "side_doc", "laser_swing", "explosion"])
        if kind == "paper_rain":
            for _ in range(random.randint(2, 3)):
                attacks.append({
                    "kind": "paper",
                    "x": random.randint(PHONE.left + 70, PHONE.right - 70),
                    "y": PHONE.top + random.randint(95, 145),
                    "vx": random.uniform(-0.55, 0.55),
                    "vy": random.uniform(5.0, 7.0),
                    "warn": 0,
                })
        elif kind == "side_doc":
            side = random.choice(["left", "right"])
            attacks.append({
                "kind": "side_doc",
                "x": PHONE.left + 12 if side == "left" else PHONE.right - 12,
                "y": random.randint(PHONE.top + 250, PHONE.bottom - 170),
                "vx": 5.4 if side == "left" else -5.4,
                "vy": 0,
                "warn": 0,
            })
        elif kind == "laser_swing":
            side = "left" if game["boss"]["x"] < PHONE.centerx else "right"
            attacks.append({
                "kind": "laser_swing",
                "x": 0,
                "y": 0,
                "vx": 0,
                "vy": 0,
                "warn": 950,
                "active": 0,
                "duration": 2200,
                "side": side,
                "length": 610,
            })
        else:
            attacks.append({
                "kind": "explosion",
                "x": random.randint(PHONE.left + 80, PHONE.right - 80),
                "y": random.randint(PHONE.top + 300, PHONE.bottom - 165),
                "vx": 0,
                "vy": 0,
                "warn": 1100,
                "life": 360,
            })
    return attacks


def update_resignation_boss(delta_ms):
    boss = game["boss"]
    if boss["phase"] == "done":
        boss["flash"] += delta_ms
        if boss["flash"] >= BOSS_FLASH_MS:
            hits = boss["hits"]
            if hits >= 6:
                finish_life("death", "끝내 사표를 내지 못하고 무너졌습니다.")
                begin_death_transition()
                return
            epilogue, mood = choose_resignation_epilogue_by_hits(hits)
            game["resignation_epilogue"] = epilogue
            game["resignation_epilogue_mood"] = mood
            game["final_stats"] = game["stats"].copy()
            game["final_reputation"] = calculate_reputation()
            game["ending_controls_revealed"] = False
            change_scene("resignation_ending")
        return

    boss["elapsed"] += delta_ms
    stage = 2 if boss["elapsed"] >= BOSS_STAGE_TWO_MS else 1
    if stage == 2 and not boss.get("was_stage_two"):
        boss["was_stage_two"] = True
        boss["stage_notice"] = 1800
    if boss.get("stage_notice", 0) > 0:
        boss["stage_notice"] = max(0, boss["stage_notice"] - delta_ms)
    if boss.get("test_notice", 0) > 0:
        boss["test_notice"] = max(0, boss["test_notice"] - delta_ms)

    keys = pygame.key.get_pressed()
    move_area = boss_move_area()
    speed = 5
    if keys[pygame.K_LEFT]:
        boss["x"] -= speed
    if keys[pygame.K_RIGHT]:
        boss["x"] += speed
    if keys[pygame.K_UP]:
        boss["y"] -= speed
    if keys[pygame.K_DOWN]:
        boss["y"] += speed
    boss["x"] = max(move_area.left + 31, min(move_area.right - 31, boss["x"]))
    boss["y"] = max(move_area.top + 40, min(move_area.bottom - 40, boss["y"]))

    boss["spawn"] -= delta_ms
    if boss["spawn"] <= 0:
        boss["spawn"] = random.randint(500, 820) if stage == 1 else random.randint(560, 920)
        boss["obstacles"].extend(spawn_boss_attack(stage))

    player_rect = pygame.Rect(boss["x"] - 16, boss["y"] - 24, 32, 48)
    for obstacle in boss["obstacles"][:]:
        rect = pygame.Rect(-100, -100, 1, 1)
        laser_hit = False
        if obstacle.get("warn", 0) > 0:
            obstacle["warn"] = max(0, obstacle["warn"] - delta_ms)
            if obstacle["kind"] == "explosion" and obstacle["warn"] <= 0:
                rect = pygame.Rect(obstacle["x"] - 36, obstacle["y"] - 36, 72, 72)
        else:
            if obstacle["kind"] == "explosion":
                obstacle["life"] = obstacle.get("life", 420) - delta_ms
            if obstacle["kind"] == "laser_swing":
                obstacle["active"] = obstacle.get("active", 0) + delta_ms
                start, end = laser_swing_points(obstacle)
                laser_hit = point_to_segment_distance(player_rect.center, start, end) <= 11
            else:
                obstacle["x"] += obstacle.get("vx", 0)
                obstacle["y"] += obstacle.get("vy", 0)
            if obstacle["kind"] == "wave":
                obstacle["width"] = min(PHONE.width - 80, obstacle.get("width", 120) + 8)
                rect = pygame.Rect(obstacle["x"] - obstacle["width"] // 2, obstacle["y"] - 10, obstacle["width"], 20)
            elif obstacle["kind"] == "side_doc":
                rect = pygame.Rect(obstacle["x"] - 24, obstacle["y"] - 14, 48, 28)
            elif obstacle["kind"] == "explosion":
                rect = pygame.Rect(obstacle["x"] - 36, obstacle["y"] - 36, 72, 72)
            elif obstacle["kind"] == "laser_swing":
                rect = pygame.Rect(-100, -100, 1, 1)
            else:
                rect = pygame.Rect(obstacle["x"] - 14, obstacle["y"] - 14, 28, 28)
        if laser_hit or rect.colliderect(player_rect):
            boss["hits"] += 1
            boss["obstacles"].remove(obstacle)
        elif (
            obstacle.get("life", 1) <= 0
            or obstacle.get("active", 0) > obstacle.get("duration", 999999)
            or obstacle["y"] > PHONE.bottom - 80
            or obstacle["x"] < PHONE.left - 80
            or obstacle["x"] > PHONE.right + 80
        ):
            boss["obstacles"].remove(obstacle)

    if boss["elapsed"] >= BOSS_DURATION_MS:
        boss["phase"] = "done"
        boss["flash"] = 0


def boss_face_variant(hits):
    if hits <= 1:
        return "review_happy"
    if hits <= 3:
        return "review_neutral"
    if hits == 4:
        return "review_sad"
    return "review_despair"


def draw_resignation_boss():
    boss = game["boss"]
    screen.fill((230, 232, 238))
    remaining = max(0, math.ceil((BOSS_DURATION_MS - boss["elapsed"]) / 1000))
    stage = 2 if boss["elapsed"] >= BOSS_STAGE_TWO_MS else 1
    draw_text("사표 보스전", TITLE_FONT, RED, WIDTH // 2, 34, center=True)
    draw_text("방향키로 공격을 피하세요", FONT, DARK, WIDTH // 2, 72, center=True)
    if boss.get("test_notice", 0) > 0:
        draw_text("개발자 테스트 모드", BIG_FONT, PURPLE, WIDTH // 2, 112, center=True)
    draw_text(f"남은 시간: {remaining}초", BIG_FONT, RED, PHONE.right - 130, 52, center=True)
    draw_text(f"{stage}스테이지", SMALL_FONT, DARK, PHONE.right - 130, 84, center=True)
    move_area = boss_move_area()
    area_overlay = pygame.Surface(move_area.size, pygame.SRCALPHA)
    area_overlay.fill((32, 34, 42, 42))
    screen.blit(area_overlay, move_area.topleft)
    pygame.draw.rect(screen, (245, 198, 75), move_area, 2, border_radius=6)
    pygame.draw.rect(screen, (255, 255, 255), move_area.inflate(-8, -8), 1, border_radius=4)
    draw_text("교장쌤", BIG_FONT, DARK, WIDTH // 2, PHONE.top + 112, center=True)
    pygame.draw.circle(screen, (240, 191, 157), (WIDTH // 2, PHONE.top + 172), 48)
    pygame.draw.rect(screen, (72, 60, 55), (WIDTH // 2 - 64, PHONE.top + 220, 128, 62), border_radius=8)

    variant = boss_face_variant(boss["hits"])
    status_image = get_original_face_photo(variant)
    if status_image is None:
        status_image = get_teacher_pet_photo(variant)
    status_box = pygame.Rect(PHONE.left + 34, PHONE.top + 36, 72, 86)
    rounded(status_box.inflate(12, 12), WHITE, 10, LINE, 2)
    if status_image is not None:
        fitted, rect = contain_surface(status_image, status_box)
        screen.blit(fitted, rect)
    draw_text(f"피격 {boss['hits']}회", TINY_FONT, RED, status_box.centerx, status_box.bottom + 18, center=True)

    for obstacle in boss["obstacles"]:
        x, y = int(obstacle["x"]), int(obstacle["y"])
        kind = obstacle["kind"]
        if kind == "explosion" and obstacle.get("warn", 0) > 0:
            pygame.draw.circle(screen, RED, (x, y), 42, 3)
            draw_text("!", BIG_FONT, RED, x, y, center=True)
        elif kind == "explosion":
            pygame.draw.circle(screen, ORANGE, (x, y), 42)
            draw_text("쾅", FONT, WHITE, x, y, center=True)
        elif kind == "chalk":
            pygame.draw.rect(screen, WHITE, (x - 22, y - 6, 44, 12), border_radius=6)
            pygame.draw.rect(screen, LINE, (x - 22, y - 6, 44, 12), 1, border_radius=6)
        elif kind == "stamp":
            pygame.draw.rect(screen, PURPLE, (x - 18, y - 18, 36, 36), border_radius=6)
            draw_text("도장", TINY_FONT, WHITE, x, y, center=True)
        elif kind == "side_doc":
            pygame.draw.rect(screen, (255, 250, 235), (x - 30, y - 18, 60, 36), border_radius=4)
            pygame.draw.rect(screen, RED, (x - 30, y - 18, 60, 36), 2, border_radius=4)
        elif kind == "wave":
            width = obstacle.get("width", 120)
            pygame.draw.arc(screen, RED, (x - width // 2, y - 34, width, 68), 0, math.pi, 5)
            draw_text("잔소리", TINY_FONT, RED, x, y - 32, center=True)
        elif kind == "laser_swing":
            start, end = laser_swing_points(obstacle)
            if obstacle.get("warn", 0) > 0:
                pygame.draw.line(screen, (255, 228, 92), start, end, 3)
                pygame.draw.circle(screen, (255, 228, 92), (int(start[0]), int(start[1])), 8, 2)
            else:
                pygame.draw.line(screen, (255, 225, 95), start, end, 24)
                pygame.draw.line(screen, RED, start, end, 14)
                pygame.draw.circle(screen, RED, (int(start[0]), int(start[1])), 10)
        else:
            pygame.draw.rect(screen, RED, (x - 18, y - 18, 36, 36), border_radius=4)
            draw_text("서류", TINY_FONT, WHITE, x, y, center=True)

    pet = get_original_face_photo(variant)
    if pet is None:
        pet = get_teacher_pet_photo(variant)
    player_rect = pygame.Rect(boss["x"] - 31, boss["y"] - 40, 62, 80)
    if pet is not None:
        image, rect = contain_surface(pet, player_rect)
        screen.blit(image, rect)
    else:
        pygame.draw.ellipse(screen, PINK, player_rect)

    draw_text(f"피격 {boss['hits']}회", FONT, DARK, WIDTH // 2, PHONE.bottom - 38, center=True)
    if boss.get("stage_notice", 0) > 0:
        draw_text("2스테이지", START_TITLE_FONT, RED, WIDTH // 2, HEIGHT // 2, center=True)
    if boss["phase"] == "done":
        draw_text("사표 투척!", START_TITLE_FONT, RED, WIDTH // 2, HEIGHT // 2, center=True)
        flash_alpha = min(255, int(255 * boss["flash"] / BOSS_FLASH_MS))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, flash_alpha))
        screen.blit(overlay, (0, 0))


def buy_item(index):
    item = SHOP_ITEMS[index]
    if item["name"] in game["owned"]:
        game["wearing"] = item["name"]
        game["message"] = f"{item['name']} 착용!"
        return
    if game["coins"] < item["price"]:
        game["message"] = "코인이 부족합니다."
        return
    game["coins"] -= item["price"]
    game["owned"].append(item["name"])
    game["wearing"] = item["name"]
    game["message"] = f"{item['name']} 구매 완료!"
    start_effect("shop")
    update_level()


def start_mini_game():
    mini = game["mini"]
    mini["active"] = True
    mini["type"] = random.choice(["falling", "reaction", "memory"])
    mini["score"] = 0
    mini["attempts"] = 0
    mini["total_spawned"] = 0
    mini["papers"] = []
    mini["spawn"] = 0
    mini["target"] = None
    mini["target_timer"] = 0
    mini["sequence"] = []
    mini["sequence_index"] = 0
    mini["show_sequence"] = False
    mini["show_timer"] = 0
    mini["input_options"] = []
    if mini["type"] == "falling":
        mini["timer"] = 18 * 60
        game["message"] = "떨어지는 시험지를 클릭하세요!"
    elif mini["type"] == "reaction":
        mini["timer"] = 15 * 60
        spawn_reaction_target()
        game["message"] = "동그라미가 보이면 빠르게 클릭하세요!"
    else:
        mini["timer"] = 0
        start_memory_round()
        game["message"] = "보여준 색깔 순서대로 클릭하세요!"
    start_effect("game", 1600)


def spawn_reaction_target():
    mini = game["mini"]
    radius = 28
    mini["target"] = {
        "x": random.randint(PHONE.left + 85, PHONE.right - 85),
        "y": random.randint(PHONE.top + 265, PHONE.bottom - 145),
        "radius": radius,
    }
    mini["target_timer"] = random.randint(42, 66)
    mini["attempts"] += 1


def start_memory_round():
    mini = game["mini"]
    colors = [
        ("빨강", RED),
        ("초록", GREEN),
        ("노랑", YELLOW),
        ("파랑", BLUE),
    ]
    mini["input_options"] = colors
    mini["sequence"] = [random.randrange(len(colors)) for _ in range(MEMORY_SEQUENCE_LENGTH)]
    mini["sequence_index"] = 0
    mini["show_sequence"] = True
    mini["show_timer"] = MEMORY_SEQUENCE_LENGTH * MEMORY_SHOW_FRAMES_PER_ITEM
    mini["attempts"] += len(mini["sequence"])


def ensure_memory_sequence():
    mini = game["mini"]
    if len(mini.get("input_options", [])) < MEMORY_SEQUENCE_LENGTH:
        mini["input_options"] = [
            ("빨강", RED),
            ("초록", GREEN),
            ("노랑", YELLOW),
            ("파랑", BLUE),
        ]
    sequence = mini.get("sequence", [])
    valid_sequence = (
        len(sequence) >= MEMORY_SEQUENCE_LENGTH
        and all(isinstance(index, int) and 0 <= index < len(mini["input_options"]) for index in sequence[:MEMORY_SEQUENCE_LENGTH])
    )
    if valid_sequence:
        mini["sequence"] = sequence[:MEMORY_SEQUENCE_LENGTH]
        return True
    mini["sequence"] = [random.randrange(len(mini["input_options"])) for _ in range(MEMORY_SEQUENCE_LENGTH)]
    mini["sequence_index"] = 0
    mini["show_sequence"] = True
    mini["show_timer"] = MEMORY_SEQUENCE_LENGTH * MEMORY_SHOW_FRAMES_PER_ITEM
    mini["attempts"] = max(mini["attempts"], MEMORY_SEQUENCE_LENGTH)
    return True


def finish_mini_game():
    mini = game["mini"]
    mini["active"] = False
    if mini["type"] == "falling":
        total = max(1, mini["total_spawned"])
    else:
        total = max(1, mini["attempts"])
    accuracy = round(mini["score"] / total * 100)
    gain_xp(mini["score"] * 3)
    update_level()
    apply_mini_game_result(accuracy)


def update_mini_game():
    mini = game["mini"]
    if not mini["active"]:
        return

    if mini["type"] == "falling":
        mini["timer"] -= 1
        mini["spawn"] -= 1
        if mini["spawn"] <= 0:
            mini["spawn"] = random.randint(23, 42)
            mini["total_spawned"] += 1
            mini["papers"].append({
                "x": random.randint(PHONE.left + 70, PHONE.right - 135),
                "y": PHONE.top + 208,
                "speed": random.randint(3, 6),
                "caught": False,
                "name": random.choice(["시험지", "결재", "민원"]),
            })

        for paper in mini["papers"]:
            paper["y"] += paper["speed"]
        mini["papers"] = [paper for paper in mini["papers"] if paper["y"] < PHONE.bottom - 105]

        if mini["timer"] <= 0:
            finish_mini_game()
    elif mini["type"] == "reaction":
        mini["timer"] -= 1
        mini["target_timer"] -= 1
        if mini["target_timer"] <= 0:
            spawn_reaction_target()
        if mini["timer"] <= 0:
            finish_mini_game()
    elif mini["type"] == "memory":
        if not ensure_memory_sequence():
            return
        if mini["show_sequence"]:
            mini["show_timer"] -= 1
            if mini["show_timer"] <= 0:
                mini["show_sequence"] = False


def click_mini(pos):
    mini = game["mini"]
    if mini["type"] == "falling":
        for paper in reversed(mini["papers"]):
            if paper.get("caught"):
                continue
            rect = pygame.Rect(int(paper["x"]), int(paper["y"]), 76, 42)
            if not rect.collidepoint(pos):
                continue
            paper["caught"] = True
            mini["papers"] = [item for item in mini["papers"] if item is not paper]
            mini["score"] += 1
            start_effect("pop", 560)
            break
    elif mini["type"] == "reaction":
        target = mini["target"]
        if not target:
            return
        distance = math.hypot(pos[0] - target["x"], pos[1] - target["y"])
        if distance <= target["radius"]:
            mini["score"] += 1
            start_effect("pop", 560)
            spawn_reaction_target()
    elif mini["type"] == "memory" and not mini["show_sequence"]:
        if not ensure_memory_sequence():
            return
        option_rects = memory_option_rects()
        for rect, index in option_rects:
            if not rect.collidepoint(pos):
                continue
            try:
                expected = mini["sequence"][mini["sequence_index"]]
            except (IndexError, TypeError):
                start_memory_round()
                return
            if index == expected:
                mini["score"] += 1
                mini["sequence_index"] += 1
                start_effect("pop", 560)
                if mini["sequence_index"] >= len(mini["sequence"]):
                    finish_mini_game()
            else:
                finish_mini_game()
            break


def memory_option_rects():
    y = PHONE.bottom - 180
    gap = 98
    start_x = PHONE.centerx - gap * 3 // 2 - 32
    return [
        (pygame.Rect(start_x + i * gap, y, 64, 64), i)
        for i in range(4)
    ]


def food_buttons():
    result = []
    gap = 112
    start_x = PHONE.centerx - gap * (len(FOODS) - 1) // 2 - 31
    y = PHONE.bottom - 208
    for i, food in enumerate(FOODS):
        result.append((pygame.Rect(start_x + i * gap, y, 62, 72), i, food))
    return result


def gamble_buttons():
    bets = []
    for i, amount in enumerate([10, 50, 100]):
        bets.append((pygame.Rect(PHONE.centerx - 175 + i * 125, PHONE.bottom - 190, 100, 42), amount))
    choices = [
        (pygame.Rect(PHONE.centerx - 120, PHONE.bottom - 132, 104, 46), "홀"),
        (pygame.Rect(PHONE.centerx + 16, PHONE.bottom - 132, 104, 46), "짝"),
    ]
    return bets, choices


def shop_buttons():
    result = []
    gap = 118
    start_x = PHONE.centerx - gap * (len(SHOP_ITEMS) - 1) // 2 - 35
    y = PHONE.bottom - 151
    for i, item in enumerate(SHOP_ITEMS):
        result.append((pygame.Rect(start_x + i * gap, y, 70, 92), i, item))
    return result


def office_buttons():
    x = PHONE.right - 180
    return [
        (pygame.Rect(x, 215, 130, 46), "수업", "class"),
        (pygame.Rect(x, 273, 130, 46), "채점", "grade"),
        (pygame.Rect(x, 331, 130, 46), "퇴근", "home"),
    ]


def room_door_buttons():
    if game["location"] == "home":
        rooms = OLD_AGE_HOME_ROOMS if game["life_stage"] == "old age" else HOME_ROOMS
    else:
        rooms = SCHOOL_ROOMS
    result = []
    if game["location"] == "school":
        positions = [(90, 315), (347, 315), (604, 315)]
        size = (158, 178)
    elif game["life_stage"] == "old age":
        positions = [(55, 290), (341, 290), (627, 290), (55, 410), (341, 410), (627, 410)]
        size = (170, 88)
    else:
        positions = [(145, 290), (527, 290), (145, 405), (527, 405)]
        size = (180, 92)
    for room, (offset_x, y) in zip(rooms, positions):
        result.append((pygame.Rect(PHONE.left + offset_x, y, *size), room))
    return result


def draw_pixel_preview(rect, room):
    preview = rect.inflate(-18, -46)
    preview.y += 24
    colors = {
        "화장실": ((188, 226, 235), (239, 250, 252)),
        "침실": ((117, 105, 165), (218, 214, 242)),
        "거실": ((96, 146, 103), (217, 235, 212)),
        "부엌": ((207, 144, 84), (250, 225, 178)),
        "아기방": ((205, 139, 157), (255, 229, 235)),
        "도박방": ((76, 101, 72), (218, 235, 212)),
        "교무실": ((91, 130, 151), (216, 231, 239)),
        "반": ((64, 111, 76), (226, 235, 208)),
        "교장실": ((105, 70, 50), (226, 205, 181)),
    }
    dark, light = colors[room]
    pygame.draw.rect(screen, light, preview)
    if room == "화장실":
        pygame.draw.rect(screen, dark, (preview.x + 12, preview.y + 18, preview.width - 24, 7))
        pygame.draw.rect(screen, WHITE, (preview.centerx - 24, preview.y + 32, 48, 22))
        pygame.draw.rect(screen, BLUE, (preview.centerx - 4, preview.y + 20, 8, 16))
    elif room == "침실":
        pygame.draw.rect(screen, dark, (preview.x + 12, preview.bottom - 44, preview.width - 24, 34))
        pygame.draw.rect(screen, WHITE, (preview.x + 18, preview.bottom - 40, 35, 16))
    elif room == "거실":
        pygame.draw.rect(screen, DARK, (preview.centerx - 30, preview.y + 12, 60, 36))
        pygame.draw.rect(screen, dark, (preview.x + 10, preview.bottom - 34, preview.width - 20, 25))
    elif room == "부엌":
        pygame.draw.rect(screen, WHITE, (preview.x + 10, preview.y + 8, 30, preview.height - 16))
        pygame.draw.rect(screen, dark, (preview.centerx, preview.bottom - 32, 46, 22))
    elif room == "아기방":
        pygame.draw.rect(screen, WHITE, (preview.x + 15, preview.bottom - 35, preview.width - 30, 25), border_radius=5)
        pygame.draw.ellipse(screen, (240, 191, 157), (preview.centerx - 18, preview.bottom - 33, 36, 19))
    elif room == "도박방":
        pygame.draw.rect(screen, dark, (preview.x + 18, preview.y + 18, preview.width - 36, 42), border_radius=18)
        draw_text("홀짝", TINY_FONT, WHITE, preview.centerx, preview.y + 39, center=True)
    elif room == "교무실":
        pygame.draw.rect(screen, dark, (preview.x + 10, preview.bottom - 33, preview.width - 20, 23))
        pygame.draw.rect(screen, DARK, (preview.centerx - 28, preview.y + 12, 56, 38))
        pygame.draw.rect(screen, WHITE, (preview.centerx - 23, preview.y + 17, 46, 26))
    elif room == "반":
        pygame.draw.rect(screen, dark, (preview.x + 10, preview.y + 10, preview.width - 20, 45))
        for x in range(preview.x + 15, preview.right - 15, 38):
            pygame.draw.rect(screen, BROWN, (x, preview.bottom - 34, 27, 18))
    else:
        pygame.draw.rect(screen, dark, (preview.x + 8, preview.bottom - 45, preview.width - 16, 35))
        pygame.draw.rect(screen, YELLOW, (preview.centerx - 25, preview.y + 12, 50, 18))


def back_button():
    return pygame.Rect(PHONE.left + 42, PHONE.bottom - 72, 94, 40)


def commute_button():
    return pygame.Rect(PHONE.right - 166, PHONE.bottom - 72, 124, 40)


def settings_button():
    return pygame.Rect(PHONE.right - 66, PHONE.top + 27, 32, 32)


def settings_controls():
    return {
        "resume": pygame.Rect(WIDTH // 2 - 120, 250, 240, 42),
        "restart": pygame.Rect(WIDTH // 2 - 120, 300, 240, 42),
        "sound": pygame.Rect(WIDTH // 2 - 120, 350, 240, 42),
        "music": pygame.Rect(WIDTH // 2 - 105, 430, 210, 16),
        "effects": pygame.Rect(WIDTH // 2 - 105, 492, 210, 16),
    }


def boss_test_controls():
    return {
        "yes": pygame.Rect(WIDTH // 2 - 118, 370, 96, 44),
        "no": pygame.Rect(WIDTH // 2 + 22, 370, 96, 44),
    }


def set_music_volume(value):
    global music_volume
    music_volume = max(0.0, min(1.0, value))
    if pygame.mixer.get_init():
        pygame.mixer.music.set_volume(music_volume if sound_enabled else 0)


def set_effects_volume(value):
    global effects_volume
    effects_volume = max(0.0, min(1.0, value))
    if story_audio_channel:
        stage_volume = TEEN_AUDIO_VOLUME if story_audio_stage_index == 2 else STORY_AUDIO_VOLUME
        story_audio_channel.set_volume(stage_volume * effects_volume if sound_enabled else 0)


def resignation_choice_buttons():
    y = 390
    return [
        (pygame.Rect(WIDTH // 2 - 174 + i * 116, y, 104, 48), hand)
        for i, hand in enumerate(("가위", "바위", "보"))
    ]


def draw_outer_background():
    screen.fill((239, 232, 218))
    pygame.draw.circle(screen, (255, 246, 208), (88, 76), 70)
    pygame.draw.circle(screen, (214, 234, 226), (840, 560), 92)


def draw_phone_frame():
    rounded(PHONE.move(0, 4), (0, 0, 0, 70), 34)
    rounded(PHONE, (41, 39, 48), 34)
    rounded(PHONE.inflate(-18, -18), CREAM, 26)
    pygame.draw.circle(screen, (22, 22, 26), (PHONE.centerx, PHONE.top + 10), 5)


def draw_room_background():
    inner = PHONE.inflate(-18, -18)
    clip = screen.get_clip()
    screen.set_clip(inner)

    room = game["room"]
    if room in ("집", "학교"):
        screen.fill((244, 235, 215) if room == "집" else (222, 235, 244))
        floor_color = (190, 145, 102) if room == "집" else (139, 166, 181)
        pygame.draw.rect(screen, floor_color, (PHONE.left + 18, 470, PHONE.width - 36, 140))
        draw_text(f"{room} 내부", TITLE_FONT, DARK, PHONE.centerx, 258, center=True)
    elif room == "화장실":
        screen.fill((216, 244, 248))
        for x in range(PHONE.left + 14, PHONE.right - 14, 44):
            pygame.draw.line(screen, (181, 222, 229), (x, PHONE.top + 20), (x, PHONE.bottom - 20), 2)
        for y in range(PHONE.top + 40, PHONE.bottom - 20, 44):
            pygame.draw.line(screen, (181, 222, 229), (PHONE.left + 10, y), (PHONE.right - 10, y), 2)
        pygame.draw.rect(screen, WHITE, (PHONE.left + 86, 390, 180, 52), border_radius=8)
        pygame.draw.ellipse(screen, (168, 218, 232), (PHONE.left + 118, 402, 116, 24), 4)
        pygame.draw.rect(screen, (125, 177, 190), (PHONE.left + 168, 365, 16, 35))
        pygame.draw.rect(screen, WHITE, (PHONE.right - 250, 345, 135, 100), border_radius=8)
        draw_text("화장실", BIG_FONT, DARK, PHONE.centerx, 258, center=True)
    elif room == "침실":
        screen.fill((151, 160, 190) if game["sleeping"] else (221, 230, 255))
        pygame.draw.circle(screen, (245, 228, 112), (PHONE.right - 75, 220), 30)
        rounded(pygame.Rect(PHONE.left + 90, 420, PHONE.width - 260, 100), (122, 105, 171), 12)
        pygame.draw.rect(screen, WHITE, (PHONE.left + 110, 432, 120, 38), border_radius=8)
        pygame.draw.rect(screen, (88, 72, 129), (PHONE.right - 150, 390, 64, 95), border_radius=6)
        pygame.draw.circle(screen, (255, 224, 128), (PHONE.right - 118, 378), 24)
        draw_text("침실", BIG_FONT, WHITE if game["sleeping"] else DARK, PHONE.centerx, 258, center=True)
    elif room == "거실":
        screen.fill((224, 238, 217))
        draw_text("거실", BIG_FONT, DARK, PHONE.centerx, 258, center=True)
        pygame.draw.rect(screen, DARK, (PHONE.left + 90, 310, 185, 105), border_radius=5)
        pygame.draw.rect(screen, (108, 165, 204), (PHONE.left + 101, 321, 163, 78))
        rounded(pygame.Rect(PHONE.right - 360, 420, 270, 90), (105, 157, 105), 12)
        pygame.draw.rect(screen, BROWN, (PHONE.centerx - 70, 500, 140, 18), border_radius=5)
    elif room == "아기방":
        screen.fill((255, 229, 235))
        draw_text("아기방", BIG_FONT, DARK, PHONE.centerx, 258, center=True)
        crib = pygame.Rect(PHONE.centerx - 185, 355, 370, 175)
        rounded(crib, WHITE, 18, (205, 139, 157), 6)
        for x in range(crib.x + 24, crib.right - 15, 42):
            pygame.draw.line(screen, (226, 174, 188), (x, crib.y + 14), (x, crib.bottom - 14), 4)
        baby = get_teacher_pet_photo("baby")
        if baby is not None:
            baby_image = pygame.transform.rotate(pygame.transform.smoothscale(baby, (145, 180)), 90)
            screen.blit(baby_image, baby_image.get_rect(center=crib.center))
    elif room == "도박방":
        screen.fill((215, 232, 207))
        draw_text("도박방", BIG_FONT, DARK, PHONE.centerx, 258, center=True)
        rounded(pygame.Rect(PHONE.centerx - 220, 350, 440, 150), (58, 111, 64), 28, BROWN, 6)
        draw_text("홀 / 짝", TITLE_FONT, WHITE, PHONE.centerx, 405, center=True)
        draw_text("금액을 고르고 홀짝을 선택하세요.", SMALL_FONT, WHITE, PHONE.centerx, 455, center=True)
    elif room == "부엌":
        screen.fill((255, 231, 178))
        draw_text(room, BIG_FONT, DARK, PHONE.centerx, 258, center=True)
        pygame.draw.rect(screen, WHITE, (PHONE.left + 65, 315, 120, 195), border_radius=6)
        pygame.draw.line(screen, LINE, (PHONE.left + 65, 405), (PHONE.left + 185, 405), 3)
        rounded(pygame.Rect(PHONE.right - 390, 425, 250, 52), (177, 111, 62), 8)
        pygame.draw.circle(screen, ORANGE, (PHONE.right - 315, 420), 15)
        pygame.draw.circle(screen, GREEN, (PHONE.right - 270, 420), 15)
    elif room == "반":
        screen.fill((235, 239, 218))
        rounded(pygame.Rect(PHONE.left + 95, 245, PHONE.width - 190, 130), (68, 112, 78), 5)
        draw_text("오늘의 수업", BIG_FONT, WHITE, PHONE.centerx, 285, center=True)
        for row_y in (435, 500):
            for x in range(PHONE.left + 120, PHONE.right - 100, 150):
                pygame.draw.rect(screen, (173, 123, 75), (x, row_y, 95, 30), border_radius=4)
    elif room == "교장실":
        screen.fill((238, 224, 208))
        draw_text("교장실", BIG_FONT, DARK, PHONE.centerx, 258, center=True)
        rounded(pygame.Rect(PHONE.left + 150, 420, PHONE.width - 300, 100), (111, 75, 52), 8)
        pygame.draw.rect(screen, (66, 54, 48), (PHONE.centerx - 55, 390, 110, 44), border_radius=5)
        pygame.draw.rect(screen, YELLOW, (PHONE.centerx - 48, 435, 96, 24), border_radius=3)
        draw_text("교장", TINY_FONT, DARK, PHONE.centerx, 447, center=True)
        pygame.draw.rect(screen, (92, 64, 48), (PHONE.left + 70, 300, 100, 140), border_radius=4)
    else:
        screen.fill((226, 239, 247))
        draw_text("교무실", BIG_FONT, DARK, PHONE.centerx, 258, center=True)
        rounded(pygame.Rect(PHONE.left + 70, 430, PHONE.width - 140, 80), (178, 123, 76), 6)
        pygame.draw.rect(screen, DARK, (PHONE.left + 110, 330, 170, 105), border_radius=5)
        pygame.draw.rect(screen, (208, 235, 245), (PHONE.left + 120, 340, 150, 76))
        for x in (PHONE.right - 310, PHONE.right - 250, PHONE.right - 190):
            pygame.draw.rect(screen, (246, 244, 226), (x, 390, 44, 55), border_radius=2)

    screen.set_clip(clip)


def draw_top_hud():
    panel = pygame.Rect(PHONE.left + 24, PHONE.top + 18, PHONE.width - 48, 174)
    rounded(panel.move(0, 4), (0, 0, 0, 28), 20)
    rounded(panel, WHITE, 20, LINE, 2)
    clock_rect = pygame.Rect(PHONE.left + 38, PHONE.top + 28, 118, 46)
    rounded(clock_rect, (42, 35, 35), 6, (105, 82, 82), 2)
    draw_text(f"Day {game['day']}", TINY_FONT, (255, 96, 96), clock_rect.centerx, clock_rect.y + 11, center=True)
    draw_text(f"{game['hour']:02d}:00", FONT, (255, 55, 55), clock_rect.centerx, clock_rect.y + 31, center=True)
    draw_warning_box(clock_rect)
    stage_label = LIFE_STAGE_LABELS[game["life_stage"]]
    draw_text(f"서은주 키우기 · {stage_label}", BIG_FONT, DARK, PHONE.centerx, PHONE.top + 45, center=True)
    reputation = calculate_reputation()
    setting = settings_button()
    coin_rect = pygame.Rect(setting.x - 122, setting.y, 112, 32)
    rounded(coin_rect, CARD, 7, LINE, 1)
    draw_text(f"코인: {game['coins']}C", SMALL_FONT, BROWN, coin_rect.centerx, coin_rect.centery, center=True)
    rounded(setting, CARD, 7, LINE, 1)
    draw_text("⚙", FONT, DARK, setting.centerx, setting.centery, center=True)

    order = ["hunger", "energy", "mental_health", "hygiene", "work"]
    bar_x = PHONE.left + 134
    bar_w = PHONE.width - 255
    y = PHONE.top + 83
    for key in order:
        name, color = STAT_INFO[key]
        draw_status_bar(name, game["stats"][key], color, bar_x, y, bar_w)
        y += 16
    draw_status_bar("평판", reputation, PURPLE, bar_x, y, bar_w)


def draw_warning_box(clock_rect):
    warnings = [
        STAT_INFO[key][0]
        for key in ["hunger", "energy", "mental_health", "hygiene", "work"]
        if game["stats"][key] <= 30
    ]
    if calculate_reputation() <= 30:
        warnings.append("평판")
    if not warnings:
        return
    label = "! 경고: " + ", ".join(warnings)
    max_width = PHONE.width - 250
    box_width = min(max_width, TINY_FONT.size(label)[0] + 24)
    rect = pygame.Rect(clock_rect.right + 12, clock_rect.y + 8, box_width, 30)
    rounded(rect, BLACK, 4)
    text = label
    while TINY_FONT.size(text)[0] > rect.width - 18 and len(text) > 5:
        text = text[:-2]
    if text != label:
        text = text[:-1] + "..."
    draw_text(text, TINY_FONT, WHITE, rect.x + 10, rect.y + 8)


def draw_status_bar(name, value, color, x, y, width):
    value = clamp(value)
    label_x = x - 82
    draw_text(name, TINY_FONT, DARK, label_x, y - 2)
    track = pygame.Rect(x, y, width, 11)
    fill = pygame.Rect(x, y, int(width * value / 100), 11)
    pygame.draw.rect(screen, (231, 226, 214), track, border_radius=7)
    if fill.width > 0:
        pygame.draw.rect(screen, color, fill, border_radius=7)
    pygame.draw.rect(screen, (185, 170, 145), track, 1, border_radius=7)
    draw_text(f"{value}%", TINY_FONT, DARK, x + width + 8, y - 3)


def draw_sleep_animation(cx, top, now):
    """잠잘 때 눈이 감기고 Zzz가 위로 떠오르는 애니메이션입니다."""
    bob = int((now // 220) % 4)
    for i, size in enumerate([18, 22, 27]):
        yy = top + 78 - ((now // 28 + i * 18) % 62)
        xx = cx + 116 + i * 24
        draw_text("Z", pygame.font.SysFont("malgungothic", size, bold=True), WHITE, xx, yy - bob, center=True)


def draw_wash_effect(cx, top, now):
    """씻기 버튼을 눌렀을 때 거품과 물방울이 올라갑니다."""
    for i in range(7):
        angle = (now * 0.004 + i * 0.9)
        x = int(cx + 118 * math.cos(angle))
        y = int(top + 178 + 86 * math.sin(angle * 0.7))
        radius = 7 + (i % 4) * 2
        pygame.draw.circle(screen, (235, 250, 255), (x, y), radius)
        pygame.draw.circle(screen, BLUE, (x, y), radius, 2)
    for i in range(4):
        x = cx - 120 + i * 34
        y = top + 70 + ((now // 10 + i * 17) % 130)
        pygame.draw.line(screen, (105, 190, 235), (x, y), (x - 10, y + 20), 3)


def draw_food_particles(cx, top, elapsed):
    mouth_x = cx
    mouth_y = top + 170
    cycle = elapsed % 900
    for i in range(6):
        age = (cycle + i * 137) % 900
        progress = age / 900
        x = mouth_x + int((i - 2.5) * 9 + math.sin(age / 90 + i) * 8)
        y = mouth_y + int(8 + progress * 34)
        radius = max(1, 5 - int(progress * 4))
        color = (196, 132, 66) if i % 2 == 0 else (235, 181, 86)
        pygame.draw.circle(screen, color, (x, y), radius)


def draw_reaction_effects(cx, top, effect, now):
    """꼭 필요한 상황에서만 보조 이펙트를 표시합니다."""
    if effect == "game" and game.get("effect") == "game" and now <= game.get("effect_until", 0):
        draw_text("START!", BIG_FONT, GREEN, cx, top + 92, center=True)
    elif effect == "pop":
        pygame.draw.circle(screen, YELLOW, (cx + 96, top + 96), 34, 5)


def draw_photo_character():
    now = pygame.time.get_ticks()
    effect = active_effect(now)
    cx = PHONE.centerx
    top = 275
    dx, dy = character_motion(effect, now)
    cx += dx
    top += dy
    pet_size = (230, 288)
    pet_rect = pygame.Rect(cx - pet_size[0] // 2, top, *pet_size)

    pygame.draw.ellipse(screen, (0, 0, 0, 52), (cx - 112, top + 278, 224, 34))

    if effect == "eat" and game["eating"]["active"]:
        eating_variant = f"eat_{game['life_stage']}"
        eating_base = get_original_face_photo(eating_variant)
        if eating_base is None:
            eating_base = get_teacher_pet_photo(game["life_stage"])
        if eating_base is None:
            pygame.draw.ellipse(screen, (240, 191, 157), pet_rect)
            draw_text("사진 없음", FONT, RED, pet_rect.centerx, pet_rect.centery, center=True)
        else:
            eating_bounds = pygame.Rect(0, 0, int(pet_rect.width * 1.5), int(pet_rect.height * 1.5))
            eating_bounds.center = pet_rect.center
            eating_image, eating_rect = contain_surface(eating_base, eating_bounds)
            screen.blit(eating_image, eating_rect)
        return

    base_pet = get_teacher_pet_photo(game["life_stage"])
    pet = pygame.transform.smoothscale(base_pet, pet_size) if base_pet is not None else None

    if pet is None:
        pygame.draw.ellipse(screen, (240, 191, 157), pet_rect)
        draw_text("사진 없음", FONT, RED, pet_rect.centerx, pet_rect.centery, center=True)
    else:
        screen.blit(pet, pet_rect)

    variant = choose_face_variant(effect)
    if effect and effect != "eat" and variant != "adult":
        emotion_base = get_teacher_pet_photo(variant)
        if emotion_base is not None:
            emotion = pygame.transform.smoothscale(emotion_base, pet_size)
            alpha = 255
            if game.get("effect") == effect and now <= game.get("effect_until", now):
                elapsed = now - game.get("effect_start", now)
                remaining = max(0, game.get("effect_until", now) - now)
                if elapsed < 160:
                    alpha = int(255 * elapsed / 160)
                if effect not in ("sleep", "game") and remaining < 420:
                    alpha = min(alpha, int(255 * remaining / 420))
            emotion = emotion.copy()
            emotion.set_alpha(max(0, min(255, alpha)))
            screen.blit(emotion, pet_rect)

    if game["wearing"] == "왕관":
        pygame.draw.polygon(screen, YELLOW, [(cx - 70, top + 12), (cx - 35, top - 35), (cx, top + 10), (cx + 35, top - 35), (cx + 70, top + 12)])
        rounded(pygame.Rect(cx - 72, top + 9, 144, 24), YELLOW, 5, BROWN, 2)
    elif game["wearing"] == "리본":
        pygame.draw.polygon(screen, PINK, [(cx - 42, top + 12), (cx - 108, top - 22), (cx - 96, top + 30)])
        pygame.draw.polygon(screen, PINK, [(cx + 42, top + 12), (cx + 108, top - 22), (cx + 96, top + 30)])
        pygame.draw.circle(screen, PINK, (cx, top + 8), 19)
    elif game["wearing"] == "안경":
        pygame.draw.circle(screen, DARK, (cx - 54, top + 145), 32, 4)
        pygame.draw.circle(screen, DARK, (cx + 54, top + 145), 32, 4)
        pygame.draw.line(screen, DARK, (cx - 22, top + 145), (cx + 22, top + 145), 4)
    elif game["wearing"] == "수첩":
        rounded(pygame.Rect(cx - 158, top + 190, 62, 82), BLUE, 8, DARK, 2)
        draw_text("수첩", TINY_FONT, WHITE, cx - 127, top + 232, center=True)

    if effect == "sleep":
        draw_sleep_animation(cx, top, now)
    elif effect == "wash":
        draw_wash_effect(cx, top, now)

    if effect in ("game", "pop"):
        draw_reaction_effects(cx, top, effect, now)


def draw_room_controls(mouse):
    room = game["room"]
    if game["lesson"]["active"] or game["office_work"]["active"] or game["eating"]["active"]:
        return

    if room in ("집", "학교"):
        for rect, target_room in room_door_buttons():
            hover = rect.collidepoint(mouse)
            rounded(rect.move(0, 4), (0, 0, 0, 28), 8)
            rounded(rect, (255, 250, 239) if hover else CARD, 8, BROWN, 2)
            pygame.draw.circle(screen, BROWN, (rect.right - 18, rect.centery), 4)
            draw_text(target_room, SMALL_FONT, DARK, rect.centerx, rect.y + 15, center=True)
            draw_pixel_preview(rect, target_room)
    elif room == "부엌":
        for rect, index, food in food_buttons():
            hover = rect.collidepoint(mouse)
            rounded(rect, WHITE if hover else CARD, 8, LINE, 2)
            pygame.draw.circle(screen, ORANGE, (rect.centerx, rect.y + 26), 19)
            draw_text(food["label"], TINY_FONT, WHITE, rect.centerx, rect.y + 26, center=True)
            draw_text(f"{food['price']}C", TINY_FONT, BROWN, rect.centerx, rect.y + 57, center=True)
    elif room == "화장실":
        rect = pygame.Rect(PHONE.right - 135, 236, 104, 48)
        rounded(rect, GREEN if rect.collidepoint(mouse) else CARD, 18, LINE, 2)
        label = "씻는 중..." if game["care_action"]["type"] == "wash" else "씻기"
        draw_text(label, SMALL_FONT, BLACK, rect.centerx, rect.centery, center=True)
    elif room == "침실":
        rect = pygame.Rect(PHONE.right - 150, 236, 124, 48)
        label = "자는 중..." if game["sleeping"] else "잠자기"
        rounded(rect, BLUE if rect.collidepoint(mouse) else CARD, 18, LINE, 2)
        draw_text(label, FONT, BLACK, rect.centerx, rect.centery, center=True)
    elif room == "아기방":
        rect = pygame.Rect(PHONE.right - 160, 236, 128, 48)
        rounded(rect, PINK if rect.collidepoint(mouse) else CARD, 18, LINE, 2)
        draw_text("육아하기", FONT, DARK, rect.centerx, rect.centery, center=True)
    elif room == "거실":
        if not game["mini"]["active"]:
            mini_rect = pygame.Rect(PHONE.centerx - 70, PHONE.bottom - 145, 140, 44)
            rounded(mini_rect, GREEN if mini_rect.collidepoint(mouse) else CARD, 8, LINE, 2)
            draw_text("미니게임", SMALL_FONT, BLACK, mini_rect.centerx, mini_rect.centery, center=True)
        draw_mini_game()
    elif room == "교무실":
        rect = pygame.Rect(PHONE.right - 174, 270, 130, 46)
        rounded(rect, YELLOW if rect.collidepoint(mouse) else CARD, 8, LINE, 2)
        draw_text("업무 처리", SMALL_FONT, BLACK, rect.centerx, rect.centery, center=True)
    elif room == "반":
        rect = pygame.Rect(PHONE.right - 174, 345, 130, 46)
        rounded(rect, YELLOW if rect.collidepoint(mouse) else CARD, 8, LINE, 2)
        draw_text("수업 진행", SMALL_FONT, BLACK, rect.centerx, rect.centery, center=True)
    elif room == "교장실":
        rect = pygame.Rect(PHONE.right - 188, 270, 144, 48)
        rounded(rect, RED if rect.collidepoint(mouse) else CARD, 8, LINE, 2)
        draw_text("사표 내기", FONT, WHITE if rect.collidepoint(mouse) else RED, rect.centerx, rect.centery, center=True)
    elif room == "도박방":
        bet_buttons, choice_buttons = gamble_buttons()
        for rect, amount in bet_buttons:
            selected = game.get("gamble_bet") == amount
            enabled = game["coins"] >= amount
            color = YELLOW if selected else (CARD if enabled else (210, 205, 196))
            rounded(rect, color, 8, LINE, 2)
            draw_text(f"{amount}C", SMALL_FONT, DARK if enabled else GRAY, rect.centerx, rect.centery, center=True)
        for rect, choice in choice_buttons:
            enabled = game["coins"] >= game.get("gamble_bet", 10)
            rounded(rect, GREEN if enabled and rect.collidepoint(mouse) else CARD, 8, LINE, 2)
            draw_text(choice, FONT, DARK if enabled else GRAY, rect.centerx, rect.centery, center=True)

    if room not in ("집", "학교"):
        rect = back_button()
        rounded(rect, CARD, 8, LINE, 2)
        draw_text("뒤로", SMALL_FONT, DARK, rect.centerx, rect.centery, center=True)

    travel = commute_button()
    rounded(travel, BLUE if travel.collidepoint(mouse) else CARD, 8, LINE, 2)
    label = "출근하기" if game["location"] == "home" else "퇴근하기"
    draw_text(label, SMALL_FONT, DARK, travel.centerx, travel.centery, center=True)


def draw_lesson_animation():
    lesson = game["lesson"]
    if not lesson["active"]:
        return
    board = pygame.Rect(PHONE.left + 82, 238, PHONE.width - 164, 310)
    rounded(board.move(0, 5), (0, 0, 0, 48), 6)
    rounded(board, (38, 86, 58), 6, (94, 64, 42), 8)
    pygame.draw.rect(screen, (53, 112, 76), board.inflate(-26, -26), border_radius=3)
    draw_text("오늘의 수업", BIG_FONT, WHITE, board.centerx, board.y + 35, center=True)
    notes = lesson.get("notes") or ["오늘의 목표: 개념 이해하기", "예제 문제 풀이", "질문하고 답하기", "수행평가 안내"]
    line_interval = LESSON_DURATION_MS / len(notes)
    progress = min(1, lesson["elapsed"] / LESSON_DURATION_MS)
    for index, note in enumerate(notes):
        line_elapsed = lesson["elapsed"] - index * line_interval
        if line_elapsed <= 0:
            continue
        line_progress = min(1, line_elapsed / (line_interval * 0.72))
        text_surface = FONT.render(note, True, (250, 247, 208))
        visible_width = int(text_surface.get_width() * line_progress)
        y = board.y + 90 + index * 45
        if visible_width > 0:
            screen.blit(text_surface, (board.x + 54, y), (0, 0, visible_width, text_surface.get_height()))
        if line_progress < 1:
            cursor_x = board.x + 54 + visible_width + 5
            pygame.draw.line(screen, (250, 247, 208), (cursor_x, y + 4), (cursor_x, y + 24), 3)
    pygame.draw.rect(screen, (239, 222, 173), (board.x + 40, board.bottom - 28, 115, 9), border_radius=3)
    pygame.draw.rect(screen, (238, 225, 182), (board.x + 162, board.bottom - 31, 45, 13), border_radius=2)
    doodle = lesson.get("doodle", "")
    if doodle == "작은 별":
        draw_text("☆", BIG_FONT, YELLOW, board.right - 90, board.y + 88, center=True)
    elif doodle == "하트":
        draw_text("♡", BIG_FONT, PINK, board.right - 90, board.y + 88, center=True)
    elif doodle == "웃는 얼굴":
        draw_text(":)", FONT, WHITE, board.right - 90, board.y + 88, center=True)
    elif doodle == "x + y = ?":
        draw_text("x + y = ?", SMALL_FONT, WHITE, board.right - 135, board.y + 88)
    elif doodle:
        draw_text(doodle, SMALL_FONT, WHITE, board.right - 135, board.y + 88)
    draw_text(f"{int(progress * 100)}%", SMALL_FONT, YELLOW, board.right - 76, board.bottom - 28, center=True)


def draw_office_work_animation():
    work = game["office_work"]
    if not work["active"]:
        return
    monitor = pygame.Rect(PHONE.left + 112, 236, PHONE.width - 224, 316)
    rounded(monitor, (45, 49, 58), 8, BLACK, 4)
    display = monitor.inflate(-22, -22)
    pygame.draw.rect(screen, (220, 235, 242), display, border_radius=4)
    pygame.draw.rect(screen, DARK, (monitor.centerx - 55, monitor.bottom, 110, 18))
    pygame.draw.rect(screen, DARK, (monitor.centerx - 100, monitor.bottom + 17, 200, 15), border_radius=4)

    if work["phase"] == "desktop":
        pygame.draw.rect(screen, (79, 139, 180), display)
        app = grade_app_button()
        rounded(app, WHITE, 8, LINE, 2)
        pygame.draw.rect(screen, BLUE, (app.centerx - 22, app.y + 12, 44, 32), border_radius=4)
        for row in range(3):
            pygame.draw.line(screen, WHITE, (app.centerx - 15, app.y + 20 + row * 8), (app.centerx + 15, app.y + 20 + row * 8), 2)
        draw_text("성적 처리", SMALL_FONT, DARK, app.centerx, app.bottom - 18, center=True)
        draw_text("앱을 클릭하세요", FONT, WHITE, display.centerx, display.bottom - 35, center=True)
        return

    if work["phase"] == "documents":
        pygame.draw.rect(screen, (246, 240, 222), display, border_radius=4)
        draw_text("문서 정리", BIG_FONT, DARK, display.centerx, display.y + 28, center=True)
        done = min(6, work.get("documents_done", 0))
        for index in range(6):
            x = display.x + 80 + (index % 3) * 150
            y = display.y + 95 + (index // 3) * 82
            color = (205, 228, 211) if index < done else (248, 248, 248)
            pygame.draw.rect(screen, color, (x, y, 105, 58), border_radius=5)
            pygame.draw.rect(screen, LINE, (x, y, 105, 58), 2, border_radius=5)
            draw_text("정리 완료" if index < done else "대기 문서", TINY_FONT, GREEN if index < done else GRAY, x + 52, y + 29, center=True)
        draw_text(f"{done}/6", FONT, BLUE, display.centerx, display.bottom - 28, center=True)
        return

    pygame.draw.rect(screen, WHITE, display)
    header = pygame.Rect(display.x, display.y, display.width, 56)
    pygame.draw.rect(screen, (61, 110, 162), header, border_radius=4)
    draw_text("학생 성적표", BIG_FONT, WHITE, display.centerx, display.y + 28, center=True)
    pygame.draw.line(screen, LINE, (display.x + 30, display.y + 66), (display.right - 30, display.y + 66), 2)
    students = work.get("students") or ["김학생", "이학생", "박학생", "최학생", "정학생"]
    for index in range(5):
        y = display.y + 95 + index * 34
        pygame.draw.rect(screen, (241, 245, 247), (display.x + 45, y - 12, display.width - 90, 30), border_radius=4)
        draw_text(students[index], SMALL_FONT, DARK, display.x + 68, y - 3)
        score = f"{work['scores'][index]}점" if index < len(work["scores"]) else "입력 중..."
        color = GREEN if index < len(work["scores"]) else GRAY
        draw_text(score, SMALL_FONT, color, display.right - 125, y - 3)


def draw_mini_game():
    mini = game["mini"]
    if not mini["active"]:
        return

    if mini["type"] == "falling":
        draw_text("시험지 클릭", SMALL_FONT, DARK, PHONE.centerx, 235, center=True)
        draw_text(f"{mini['timer'] // 60}초", SMALL_FONT, DARK, PHONE.left + 54, 235)
        draw_text(f"{mini['score']}개", SMALL_FONT, DARK, PHONE.right - 92, 235)
        for paper in mini["papers"]:
            rect = pygame.Rect(paper["x"], paper["y"], 76, 42)
            rounded(rect, WHITE, 6, DARK, 2)
            draw_text(paper["name"], TINY_FONT, DARK, rect.centerx, rect.centery, center=True)
    elif mini["type"] == "reaction":
        draw_text("순발력 클릭", SMALL_FONT, DARK, PHONE.centerx, 235, center=True)
        draw_text(f"{mini['timer'] // 60}초", SMALL_FONT, DARK, PHONE.left + 54, 235)
        draw_text(f"{mini['score']}/{max(1, mini['attempts'])}", SMALL_FONT, DARK, PHONE.right - 108, 235)
        target = mini["target"]
        if target:
            pulse = int(4 * abs(math.sin(pygame.time.get_ticks() / 120)))
            pygame.draw.circle(screen, YELLOW, (target["x"], target["y"]), target["radius"] + pulse)
            pygame.draw.circle(screen, ORANGE, (target["x"], target["y"]), target["radius"], 4)
    elif mini["type"] == "memory":
        draw_text("기억력 게임", SMALL_FONT, DARK, PHONE.centerx, 235, center=True)
        ensure_memory_sequence()
        if mini["show_sequence"]:
            total_show_time = MEMORY_SEQUENCE_LENGTH * MEMORY_SHOW_FRAMES_PER_ITEM
            elapsed_show = max(0, total_show_time - mini["show_timer"])
            revealed_count = min(MEMORY_SEQUENCE_LENGTH, elapsed_show // MEMORY_SHOW_FRAMES_PER_ITEM + 1)
            y = PHONE.top + 360
            gap = 88
            start_x = PHONE.centerx - gap * (MEMORY_SEQUENCE_LENGTH - 1) // 2
            for order in range(MEMORY_SEQUENCE_LENGTH):
                x = start_x + order * gap
                if order < revealed_count:
                    color_index = mini["sequence"][order]
                    name, color = mini["input_options"][color_index]
                    pygame.draw.circle(screen, color, (x, y), 34)
                    draw_text(name, TINY_FONT, WHITE, x, y, center=True)
                else:
                    pygame.draw.circle(screen, (210, 206, 196), (x, y), 34)
                    draw_text("?", FONT, WHITE, x, y, center=True)
        else:
            draw_text(f"{mini['sequence_index']}/{len(mini['sequence'])}", SMALL_FONT, DARK, PHONE.right - 96, 235)
            for rect, index in memory_option_rects():
                name, color = mini["input_options"][index]
                rounded(rect, color, 10, DARK, 2)
                draw_text(name, TINY_FONT, WHITE, rect.centerx, rect.centery, center=True)


def draw_message():
    rect = pygame.Rect(PHONE.left + 72, PHONE.top + 190, PHONE.width - 144, 38)
    rounded(rect.move(0, 3), (0, 0, 0, 24), 17)
    rounded(rect, WHITE, 17, LINE, 2)
    message = game["message"]
    while TINY_FONT.size(message)[0] > rect.width - 28 and len(message) > 4:
        message = message[:-2]
    if message != game["message"]:
        message = message[:-1] + "..."
    draw_text(message, TINY_FONT, DARK, rect.centerx, rect.centery, center=True)


def draw_cheat_notice(now):
    if now > game.get("cheat_notice_until", 0):
        return
    rect = pygame.Rect(WIDTH // 2 - 180, 18, 360, 42)
    rounded(rect.move(0, 3), (0, 0, 0, 70), 12)
    rounded(rect, (255, 247, 205), 12, YELLOW, 2)
    draw_text("테스트 치트: 하루가 경과했습니다.", SMALL_FONT, DARK, rect.centerx, rect.centery, center=True)


def draw_fade_overlay():
    transition = game["transition"]
    if not transition:
        return
    progress = min(1, transition["elapsed"] / FADE_DURATION_MS)
    alpha = int(255 * progress) if transition["phase"] == "out" else int(255 * (1 - progress))
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, alpha))
    screen.blit(overlay, (0, 0))


def draw_settings_overlay():
    shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    shade.fill((20, 20, 24, 175))
    screen.blit(shade, (0, 0))
    panel = pygame.Rect(WIDTH // 2 - 190, 155, 380, 410)
    rounded(panel, WHITE, 8, LINE, 2)
    draw_text("설정 / 일시정지", TITLE_FONT, DARK, panel.centerx, 205, center=True)
    buttons = settings_controls()
    mouse = pygame.mouse.get_pos()
    labels = {
        "resume": "계속하기",
        "restart": "다시 시작",
        "sound": "소리 끄기" if sound_enabled else "소리 켜기",
    }
    for key in ("resume", "restart", "sound"):
        rect = buttons[key]
        rounded(rect, (238, 244, 247) if rect.collidepoint(mouse) else CARD, 8, LINE, 2)
        draw_text(labels[key], FONT, DARK, rect.centerx, rect.centery, center=True)

    for key, label, value in (
        ("music", "배경음악", music_volume),
        ("effects", "효과음", effects_volume),
    ):
        rect = buttons[key]
        draw_text(f"{label} {round(value * 100)}%", SMALL_FONT, DARK, rect.x, rect.y - 25)
        pygame.draw.rect(screen, (225, 220, 210), rect, border_radius=8)
        fill = pygame.Rect(rect.x, rect.y, int(rect.width * value), rect.height)
        if fill.width:
            pygame.draw.rect(screen, BLUE if key == "music" else PINK, fill, border_radius=8)
        knob_x = rect.x + int(rect.width * value)
        pygame.draw.circle(screen, DARK, (knob_x, rect.centery), 9)
    draw_text("게임 진행이 일시정지되었습니다.", SMALL_FONT, GRAY, panel.centerx, 545, center=True)


def draw_boss_test_confirm_overlay():
    if not game.get("boss_test_confirm"):
        return
    shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    shade.fill((20, 20, 24, 165))
    screen.blit(shade, (0, 0))
    panel = pygame.Rect(WIDTH // 2 - 220, 235, 440, 210)
    rounded(panel, WHITE, 10, LINE, 2)
    draw_text("보스전으로 이동하시겠습니까?", BIG_FONT, DARK, panel.centerx, panel.y + 58, center=True)
    draw_text("개발용 테스트 기능입니다.", SMALL_FONT, GRAY, panel.centerx, panel.y + 94, center=True)
    controls = boss_test_controls()
    mouse = pygame.mouse.get_pos()
    for key, label in (("yes", "YES"), ("no", "NO")):
        rect = controls[key]
        color = GREEN if key == "yes" else CARD
        if rect.collidepoint(mouse):
            color = YELLOW if key == "yes" else (238, 244, 247)
        rounded(rect, color, 8, LINE, 2)
        draw_text(label, FONT, DARK, rect.centerx, rect.centery, center=True)


def draw_resignation_event_overlay():
    event = game["resignation_event"]
    if not event:
        return
    shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    shade.fill((30, 24, 22, 155))
    screen.blit(shade, (0, 0))
    panel = pygame.Rect(WIDTH // 2 - 260, 165, 520, 340)
    rounded(panel, WHITE, 8, LINE, 2)
    draw_text("교장 선생님과 가위바위보", TITLE_FONT, DARK, panel.centerx, 205, center=True)
    draw_text("서은주", SMALL_FONT, BROWN, panel.centerx - 120, 260, center=True)
    draw_text("교장 선생님", SMALL_FONT, BROWN, panel.centerx + 120, 260, center=True)
    player_label = event["player"] or "선택"
    draw_text(player_label, START_TITLE_FONT, ORANGE, panel.centerx - 120, 320, center=True)
    draw_text(event["principal"], START_TITLE_FONT, BLUE, panel.centerx + 120, 320, center=True)
    draw_text("VS", BIG_FONT, RED, panel.centerx, 320, center=True)

    if event["phase"] == "choose":
        mouse = pygame.mouse.get_pos()
        for rect, hand in resignation_choice_buttons():
            rounded(rect, YELLOW if rect.collidepoint(mouse) else CARD, 10, LINE, 2)
            draw_text(hand, FONT, DARK, rect.centerx, rect.centery, center=True)
        draw_text("낼 패를 선택하세요.", SMALL_FONT, DARK, panel.centerx, 470, center=True)
    else:
        result = "승리! 학교 탈출 성공" if event["success"] else "패배! 사표 수리 거절"
        color = GREEN if event["success"] else RED
        draw_text(result, BIG_FONT, color, panel.centerx, 420, center=True)
        draw_text("결과를 확인하는 중...", SMALL_FONT, DARK, panel.centerx, 465, center=True)


def draw_game():
    mouse = pygame.mouse.get_pos()
    draw_outer_background()
    draw_phone_frame()
    draw_room_background()
    if game["eating"]["active"]:
        draw_photo_character()
        draw_fade_overlay()
        return
    draw_top_hud()
    activity_active = game["lesson"]["active"] or game["office_work"]["active"]
    if game["room"] not in ("집", "학교", "아기방") and not activity_active:
        draw_photo_character()
    draw_room_controls(mouse)
    draw_lesson_animation()
    draw_office_work_animation()
    draw_message()
    draw_fade_overlay()
    draw_resignation_event_overlay()
    if game["settings_open"]:
        draw_settings_overlay()
    draw_boss_test_confirm_overlay()


def start_buttons():
    return {
        "start": pygame.Rect(WIDTH // 2 - 92, 510, 184, 54),
        "quit": pygame.Rect(WIDTH // 2 - 92, 574, 184, 48),
    }


def update_start_animation(now):
    if start_animation["last_switch"] == 0:
        start_animation["last_switch"] = now
        start_animation["bounce_start"] = now

    if now - start_animation["last_switch"] >= START_SWITCH_MS:
        start_animation["variant_index"] = (start_animation["variant_index"] + 1) % len(START_VARIANTS)
        start_animation["last_switch"] = now
        start_animation["bounce_start"] = now

    elapsed = now - start_animation["bounce_start"]
    if elapsed < START_BOUNCE_UP_MS:
        t = elapsed / START_BOUNCE_UP_MS
        eased = 1 - (1 - t) ** 3
        start_animation["offset_y"] = int(-START_BOUNCE_HEIGHT * eased)
    elif elapsed < START_BOUNCE_UP_MS + START_BOUNCE_DOWN_MS:
        t = (elapsed - START_BOUNCE_UP_MS) / START_BOUNCE_DOWN_MS
        eased = 1 - (1 - t) ** 3
        start_animation["offset_y"] = int(-START_BOUNCE_HEIGHT * (1 - eased))
    else:
        start_animation["offset_y"] = 0


def draw_start_screen():
    mouse = pygame.mouse.get_pos()
    buttons = start_buttons()

    screen.fill((255, 248, 232))
    pygame.draw.circle(screen, (255, 226, 167), (190, 130), 92)
    pygame.draw.circle(screen, (207, 237, 224), (728, 152), 118)
    pygame.draw.circle(screen, (255, 219, 229), (720, 470), 86)

    draw_text("서은주 키우기", START_TITLE_FONT, (67, 54, 48), WIDTH // 2, 100, center=True)
    draw_text("오늘도 귀엽게 돌봐주세요", FONT, BROWN, WIDTH // 2, 151, center=True)

    image_panel = pygame.Rect(WIDTH // 2 - 150, 185, 300, 292)
    rounded(image_panel.move(0, 8), (0, 0, 0, 42), 28)
    rounded(image_panel, (255, 255, 255), 28, (235, 194, 139), 3)

    variant = START_VARIANTS[start_animation["variant_index"]]
    pet = get_teacher_pet_photo(variant)
    if pet is None:
        rounded(pygame.Rect(WIDTH // 2 - 105, 215 + start_animation["offset_y"], 210, 240), CREAM, 22, LINE, 2)
        draw_text("사진 없음", FONT, RED, WIDTH // 2, 335 + start_animation["offset_y"], center=True)
    else:
        pet = pygame.transform.smoothscale(pet, (224, 280))
        pet_rect = pet.get_rect(center=(WIDTH // 2, 331 + start_animation["offset_y"]))
        screen.blit(pet, pet_rect)

    pygame.draw.ellipse(screen, (0, 0, 0, 38), (WIDTH // 2 - 94, 459, 188, 24))

    for key, label in (("start", "게임 시작"), ("quit", "게임 종료")):
        rect = buttons[key]
        if key == "start":
            base = (244, 151, 90)
            hover = (255, 170, 108)
            text_color = WHITE
        else:
            base = (255, 255, 255)
            hover = (255, 246, 234)
            text_color = DARK

        color = hover if rect.collidepoint(mouse) else base
        rounded(rect.move(0, 4), (0, 0, 0, 36), 18)
        rounded(rect, color, 18, (181, 130, 83), 2)
        draw_text(label, BIG_FONT, text_color, rect.centerx, rect.centery, center=True)


def handle_start_screen(event):
    if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
        return True

    buttons = start_buttons()
    if buttons["start"].collidepoint(event.pos):
        start_story()
    elif buttons["quit"].collidepoint(event.pos):
        return False
    return True


def story_skip_button():
    return pygame.Rect(WIDTH - 124, HEIGHT - 70, 86, 40)


def fade_value(elapsed, duration, fade_ms=1500):
    if elapsed < fade_ms:
        return int(255 * elapsed / fade_ms)
    if elapsed > duration - fade_ms:
        return int(255 * (duration - elapsed) / fade_ms)
    return 255


def draw_story_background(stage):
    top, mid, accent = stage["colors"]
    screen.fill(top)
    if stage["variant"] == "baby":
        rounded(pygame.Rect(0, 415, WIDTH, 235), mid, 0)
        rounded(pygame.Rect(95, 315, 710, 92), accent, 28)
        pygame.draw.circle(screen, (255, 247, 178), (710, 105), 46)
        for x in range(120, 780, 130):
            pygame.draw.circle(screen, (255, 255, 255), (x, 90 + (x % 3) * 28), 12)
    elif stage["variant"] == "kid":
        rounded(pygame.Rect(0, 430, WIDTH, 220), (120, 191, 119), 0)
        pygame.draw.circle(screen, (255, 214, 93), (120, 112), 46)
        rounded(pygame.Rect(560, 270, 230, 22), accent, 8)
        pygame.draw.line(screen, (133, 91, 54), (600, 292), (555, 430), 9)
        pygame.draw.line(screen, (133, 91, 54), (750, 292), (795, 430), 9)
    else:
        rounded(pygame.Rect(90, 86, 720, 390), mid, 16, (158, 174, 188), 3)
        rounded(pygame.Rect(170, 130, 560, 146), accent, 10)
        draw_text("CLASS", BIG_FONT, WHITE, WIDTH // 2, 182, center=True)
        for x in range(150, 760, 125):
            rounded(pygame.Rect(x, 384, 74, 52), (198, 160, 105), 8)

    draw_text(stage["title"], SMALL_FONT, (78, 67, 61), 64, 44)


def draw_story_scene(now):
    elapsed = elapsed_in_scene(now)
    if elapsed >= STORY_DURATION_MS:
        start_adult_intro()
        return

    stage_index = min(len(STORY_STAGES) - 1, elapsed // STORY_STAGE_DURATION_MS)
    play_story_audio(stage_index)
    stage = STORY_STAGES[stage_index]
    stage_elapsed = elapsed % STORY_STAGE_DURATION_MS
    if stage_index == 2 and stage_elapsed >= TEEN_AUDIO_DURATION_MS:
        stop_story_audio()
    alpha = fade_value(stage_elapsed, STORY_STAGE_DURATION_MS, 700)
    zoom = 1.0 + stage_elapsed / STORY_STAGE_DURATION_MS * 0.12

    draw_story_background(stage)

    pet = get_teacher_pet_photo(stage["variant"])
    if pet is not None:
        width = int(250 * zoom)
        height = int(312 * zoom)
        image = pygame.transform.smoothscale(pet, (width, height)).convert_alpha()
        image.set_alpha(alpha)
        rect = image.get_rect(center=(WIDTH // 2, 320))
        screen.blit(image, rect)

    text_index = 0 if stage_elapsed < STORY_STAGE_DURATION_MS // 2 else 1
    text_duration = STORY_STAGE_DURATION_MS // 2
    text_elapsed = stage_elapsed % text_duration
    text_alpha = fade_value(text_elapsed, text_duration, 450)
    text = stage["texts"][text_index]
    rounded(pygame.Rect(110, HEIGHT - 145, WIDTH - 220, 74), (255, 255, 255), 18, LINE, 2)
    draw_text_alpha(text, BIG_FONT, DARK, WIDTH // 2, HEIGHT - 108, text_alpha, center=True)

    rect = story_skip_button()
    mouse = pygame.mouse.get_pos()
    rounded(rect, (255, 255, 255) if rect.collidepoint(mouse) else (248, 239, 222), 15, (171, 137, 93), 2)
    draw_text("스킵", SMALL_FONT, DARK, rect.centerx, rect.centery, center=True)

    transition_alpha = 0
    if stage_elapsed < 700:
        transition_alpha = int(150 * (1 - stage_elapsed / 700))
    elif stage_elapsed > STORY_STAGE_DURATION_MS - 700:
        transition_alpha = int(150 * ((stage_elapsed - (STORY_STAGE_DURATION_MS - 700)) / 700))
    if transition_alpha:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, transition_alpha))
        screen.blit(overlay, (0, 0))


def draw_adult_intro(now):
    elapsed = elapsed_in_scene(now)
    if elapsed >= ADULT_INTRO_DURATION_MS:
        start_guide()
        return

    screen.fill((245, 241, 231))
    pygame.draw.circle(screen, (233, 205, 135), (WIDTH // 2, 280), 190)
    pygame.draw.circle(screen, (198, 224, 216), (180, 135), 70)
    pygame.draw.circle(screen, (221, 177, 192), (730, 492), 82)

    pet = get_teacher_pet_photo("adult")
    if pet is not None:
        image = pygame.transform.smoothscale(pet, (260, 324)).convert_alpha()
        image.set_alpha(fade_value(min(elapsed, 1600), 1600, 700))
        rect = image.get_rect(center=(WIDTH // 2, 306))
        screen.blit(image, rect)

    if elapsed < 1600:
        alpha = fade_value(elapsed, 1600, 500)
        draw_text_alpha("성인이 되었습니다.", START_TITLE_FONT, DARK, WIDTH // 2, 92, alpha, center=True)
    else:
        alpha = fade_value(elapsed - 1600, 1400, 350)
        draw_text_alpha("인생 시작", START_TITLE_FONT, ORANGE, WIDTH // 2, 92, alpha, center=True)


def guide_start_button():
    return pygame.Rect(WIDTH // 2 - 100, HEIGHT - 76, 200, 46)


def draw_guide_screen():
    screen.fill((245, 241, 231))
    draw_text("설명서", START_TITLE_FONT, DARK, WIDTH // 2, 60, center=True)
    panel = pygame.Rect(90, 112, WIDTH - 180, 430)
    rounded(panel, WHITE, 16, LINE, 2)
    lines = [
        "허기: 밥을 먹어야 유지됩니다. 커피, 빵, 스테이크로 회복할 수 있습니다.",
        "커피: 일시적으로 좋아지지만 많이 마시면 나중에 안 좋아집니다.",
        "에너지: 잠을 자거나 커피를 마시면 회복됩니다.",
        "정신건강: 게임, 휴식, 좋은 이벤트로 회복됩니다.",
        "위생: 씻기를 해야 유지됩니다.",
        "업무: 수업과 업무 처리를 통해 관리합니다.",
        "평판: 이벤트와 행동에 따라 오르내립니다. 0이 되면 위험합니다.",
    ]
    y = panel.y + 34
    for line in lines:
        for wrapped in wrap_text(line, FONT, panel.width - 70):
            draw_text(wrapped, FONT, DARK, panel.x + 35, y)
            y += 31
        y += 8
    button = guide_start_button()
    mouse = pygame.mouse.get_pos()
    rounded(button, GREEN if button.collidepoint(mouse) else CARD, 12, LINE, 2)
    draw_text("본 게임 시작", BIG_FONT, DARK, button.centerx, button.centery, center=True)


def draw_growth_scene(now):
    elapsed = elapsed_in_scene(now)
    if elapsed >= GROWTH_SCENE_DURATION_MS:
        start_game()
        return

    stage = game["life_stage"]
    first_line, second_line = GROWTH_SCENES[stage]
    screen.fill((16, 17, 24))

    image_alpha = max(0, min(255, int((elapsed - 650) / 700 * 255)))
    pet = get_teacher_pet_photo(stage)
    if pet is not None and image_alpha > 0:
        image = pygame.transform.smoothscale(pet, (250, 312)).convert_alpha()
        image.set_alpha(image_alpha)
        screen.blit(image, image.get_rect(center=(WIDTH // 2, 315)))

    if elapsed >= 1450:
        alpha = min(255, int((elapsed - 1450) / 550 * 255))
        draw_text_alpha(first_line, BIG_FONT, WHITE, WIDTH // 2, 95, alpha, center=True)
    if elapsed >= 2850:
        alpha = min(255, int((elapsed - 2850) / 550 * 255))
        draw_text_alpha(second_line, TITLE_FONT, YELLOW, WIDTH // 2, 535, alpha, center=True)

    if elapsed > GROWTH_SCENE_DURATION_MS - 650:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, int(255 * (elapsed - (GROWTH_SCENE_DURATION_MS - 650)) / 650)))
        screen.blit(overlay, (0, 0))


def ending_summary(reputation):
    if reputation >= 90:
        return "많은 사람들에게 존경받는 삶을 살았습니다."
    if reputation >= 70:
        return "주어진 자리에서 성실하게 살아갔습니다."
    if reputation >= 40:
        return "그녀의 삶에는 인정과 아쉬움이 함께 남았습니다."
    return "세상은 그녀의 노력을 충분히 기억하지 못했습니다."


def detailed_evaluation(stats):
    evaluations = []
    rules = {
        "hunger": (
            "가장 기본적인 끼니조차 자주 놓쳤습니다.",
            "바쁜 중에도 끼니를 챙기려 노력했습니다.",
            "건강한 식생활로 자신을 잘 돌보았습니다.",
        ),
        "energy": (
            "쉬어야 할 순간에도 자신을 몰아붙였습니다.",
            "피곤함 속에서도 삶의 균형을 찾으려 했습니다.",
            "충분히 쉬며 삶을 이어갈 힘을 지켰습니다.",
        ),
        "mental_health": (
            "마음의 상처를 오래 홀로 견뎌야 했습니다.",
            "기쁨과 슬픔을 받아들이며 살아갔습니다.",
            "힘든 순간에도 미소를 잃지 않았습니다.",
        ),
        "hygiene": (
            "자신을 돌보는 일에는 소홀했습니다.",
            "일상 속에서 자신을 돌보려 노력했습니다.",
            "언제나 자신을 깨끗하게 가꾸었습니다.",
        ),
        "work": (
            "책임을 감당하는 일이 점점 버거워졌습니다.",
            "맡은 일을 차근차근 처리했습니다.",
            "많은 책임을 끝까지 감당했습니다.",
        ),
    }
    for key, value in stats.items():
        low_text, normal_text, high_text = rules[key]
        if value < 40:
            evaluations.append(low_text)
        elif value >= 75:
            evaluations.append(high_text)
        else:
            evaluations.append(normal_text)
    return evaluations


def score_evaluation(key, value):
    texts = {
        "hunger": ("기본적인 식사 관리가 부족했습니다.", "끼니를 대체로 잘 챙겼습니다.", "자기 관리를 잘했습니다."),
        "energy": ("휴식이 크게 부족했습니다.", "조금 더 쉬었으면 좋았습니다.", "충분한 활력을 유지했습니다."),
        "mental_health": ("마음의 상처를 돌보지 못했습니다.", "힘든 감정을 견디며 살아갔습니다.", "행복한 삶을 살았습니다."),
        "hygiene": ("자신을 돌보는 부분이 부족했습니다.", "기본적인 위생을 유지했습니다.", "깔끔한 생활을 유지했습니다."),
        "work": ("맡은 책임을 다하기 어려웠습니다.", "주어진 업무를 수행했습니다.", "책임감 있게 일했습니다."),
        "reputation": ("주변의 신뢰를 잃었습니다.", "일정한 신뢰를 얻었습니다.", "많은 사람에게 인정받았습니다."),
    }
    low, middle, high = texts[key]
    if value < 40:
        return low
    if value >= 75:
        return high
    return middle


def overall_evaluation(stats, reputation):
    average = (sum(stats.values()) + reputation) / 6
    if average >= 80:
        return ["당신은 서은주의 삶을 세심하게 이끌었습니다.", "그녀는 많은 순간에 돌봄과 존중을 받았습니다."]
    if average >= 60:
        return ["당신은 서은주의 삶을 비교적 잘 이끌었습니다.", "하지만 몇몇 순간에는 그녀를 더 돌볼 수 있었습니다."]
    if average >= 40:
        return ["그녀의 삶에는 돌봄과 방치가 함께 남았습니다.", "당신의 선택은 정말 최선이었습니까?"]
    return ["그녀는 필요한 도움을 충분히 받지 못했습니다.", "당신의 선택이 이 삶을 만들었습니다. 후회는 없습니까?"]


def reputation_emotion(reputation):
    if reputation >= 80:
        return "review_happy", "행복한 삶이었습니다.", GREEN
    if reputation >= 55:
        return "review_neutral", "무난한 삶이었습니다.", DARK
    if reputation >= 35:
        return "review_sad", "많이 지친 삶이었습니다.", BROWN
    return "review_despair", "무너져가는 삶이었습니다.", RED


def ending_buttons():
    return {
        "restart": pygame.Rect(WIDTH // 2 - 145, HEIGHT - 58, 180, 42),
        "skip": pygame.Rect(WIDTH - 126, HEIGHT - 58, 90, 42),
    }


def life_review_duration():
    reached_index = LIFE_STAGE_ORDER.index(game["life_stage"])
    return (reached_index + 1) * ENDING_STAGE_MS


def skip_life_review():
    global scene_start_time
    now = pygame.time.get_ticks()
    scene_start_time = now - life_review_duration() - ENDING_EVALUATION_MIN_MS
    game["ending_controls_revealed"] = True


def draw_skip_button():
    button = ending_buttons()["skip"]
    mouse = pygame.mouse.get_pos()
    rounded(button, YELLOW if button.collidepoint(mouse) else CARD, 10, LINE, 2)
    draw_text("?ㅽ궢", SMALL_FONT, DARK, button.centerx, button.centery, center=True)


def death_evaluation(cause):
    return {
        "굶주림으로 사망": "바쁜 삶 속에서 가장 기본적인 것조차 챙기지 못했습니다.",
        "탈진으로 사망": "쉬어야 할 순간에도 멈추지 못했습니다.",
        "우울증으로 사망": "마음의 상처를 돌보지 못했습니다.",
        "위생 악화로 사망": "자신을 돌보는 일을 뒤로 미뤘습니다.",
        "업무 과부하로 사망": "책임감은 강했지만 결국 자신을 잃어버렸습니다.",
    }.get(cause, "그녀의 삶은 당신의 선택 위에서 이어졌습니다.")


def death_reason_label():
    if game["ending_type"] == "reputation_death":
        return "평판 붕괴"
    cause = game.get("death_cause", "")
    if "카페인" in cause:
        return "카페인 과다 복용"
    if "굶주림" in cause:
        return "굶주림"
    if "탈진" in cause:
        return "탈진"
    if "우울" in cause:
        return "우울증"
    if "위생" in cause:
        return "위생 악화"
    if "업무" in cause:
        return "업무 과부하"
    return cause


def old_age_evaluation():
    if game["nursery_care_count"] >= 3:
        lines = [
            "그녀는 마지막까지 가족과 함께했습니다.",
            "긴 삶을 살아오며 사랑과 기억을 다음 세대에 남겼습니다.",
            "당신은 그녀의 인생을 끝까지 책임졌습니다.",
        ]
    elif game["nursery_care_count"] > 0:
        lines = [
            "노년의 짧은 순간이나마 가족의 온기를 나누었습니다.",
            "그녀가 남긴 마음은 다음 세대의 기억 속에 이어질 것입니다.",
        ]
    else:
        lines = [
            "긴 삶의 끝에서 가족과 나눌 시간은 많지 않았습니다.",
            "그래도 그녀가 지나온 시간은 조용한 흔적으로 남았습니다.",
        ]
    if game["nursery_special_count"] > 0:
        lines.append("손주와 함께한 특별한 순간은 오래도록 따뜻한 기억이 되었습니다.")
    return lines


def draw_review_stage(stage, stage_elapsed):
    colors = {
        "baby": (248, 226, 229),
        "kid": (218, 239, 216),
        "teenager": (224, 235, 246),
        "adult": (245, 241, 231),
        "middleage": (221, 211, 198),
        "old age": (205, 209, 218),
    }
    screen.fill(colors[stage])
    pygame.draw.circle(screen, (255, 244, 207), (WIDTH // 2, 285), 190)
    pet = get_teacher_pet_photo(stage)
    if pet is not None:
        image = pygame.transform.smoothscale(pet, (250, 312)).convert_alpha()
        image.set_alpha(fade_value(stage_elapsed, ENDING_STAGE_MS, 500))
        screen.blit(image, image.get_rect(center=(WIDTH // 2, 310)))

    review_texts = {
        "baby": "작은 생명으로 세상에 태어났습니다.",
        "kid": "세상을 배우며 어린 시절을 지나왔습니다.",
        "teenager": "꿈과 고민 속에서 청소년기를 보냈습니다.",
        "adult": "성인이 되어 자신의 삶과 책임을 짊어졌습니다.",
        "middleage": "세월 속에서 수많은 선택의 결과를 마주했습니다.",
        "old age": "긴 시간을 지나 삶의 마지막 계절에 도달했습니다.",
    }
    review_texts.update({
        "baby": "\uccab \uc2dc\uc808\uc740 \uc9e7\uc740 \uae30\uc5b5\uc73c\ub85c \ub0a8\uc558\uc2b5\ub2c8\ub2e4.",
        "kid": "\uc5b4\ub9b0 \ub0a0\uc758 \uc6c3\uc74c\uacfc \uc2dc\uac04\uc774 \uc2a4\uccd0 \uc9c0\ub098\uac11\ub2c8\ub2e4.",
        "teenager": "\ud559\ucc3d \uc2dc\uc808\uc758 \uafc8\uacfc \uace0\ubbfc\uc774 \uae30\uc5b5\ub429\ub2c8\ub2e4.",
        "adult": "\uc131\uc778\uc774 \ub41c \ub4a4 \uc790\uc2e0\uc758 \uc77c\uacfc \ucc45\uc784\uc744 \ub9c8\uc8fc\ud588\uc2b5\ub2c8\ub2e4.",
        "middleage": "\uc2dc\uac04\uc774 \uc313\uc774\uba70 \uc120\ud0dd\uc758 \ubb34\uac8c\ub3c4 \ucee4\uc84c\uc2b5\ub2c8\ub2e4.",
        "old age": "\uae34 \uc5ec\uc815\uc758 \ub05d\uc5d0\uc11c \uc9c0\ub098\uc628 \ub0a0\ub4e4\uc744 \ub3cc\uc544\ubd05\ub2c8\ub2e4.",
    })
    draw_text(LIFE_STAGE_LABELS[stage], TITLE_FONT, DARK, WIDTH // 2, 55, center=True)
    rounded(pygame.Rect(100, HEIGHT - 145, WIDTH - 200, 74), WHITE, 18, LINE, 2)
    draw_text_alpha(
        review_texts[stage], BIG_FONT, DARK, WIDTH // 2, HEIGHT - 108,
        fade_value(stage_elapsed, ENDING_STAGE_MS, 500), center=True,
    )


def death_animation_state(elapsed):
    frame_start = 0
    for variant, duration in DEATH_ANIMATION_FRAMES:
        frame_end = frame_start + duration
        if elapsed < frame_end:
            return variant, elapsed - frame_start, duration
        frame_start = frame_end
    variant, duration = DEATH_ANIMATION_FRAMES[-1]
    return variant, duration, duration


def draw_death_transition(now):
    elapsed = elapsed_in_scene(now)
    if elapsed >= DEATH_ANIMATION_DURATION_MS:
        change_scene("life_review")
        return

    variant, frame_elapsed, frame_duration = death_animation_state(elapsed)
    bounce_window = min(360, frame_duration)
    if frame_elapsed < bounce_window:
        t = frame_elapsed / bounce_window
        jump = int(-34 * math.sin(math.pi * t))
        scale = 1.0 + 0.16 * math.sin(math.pi * t)
        shake = int(math.sin(frame_elapsed / 18) * (1 - t) * 10)
    else:
        jump = 0
        scale = 1.0
        shake = 0

    screen.fill((24, 24, 31))
    pygame.draw.circle(screen, (72, 65, 82), (WIDTH // 2 + shake, 305), 220)
    pygame.draw.ellipse(screen, (0, 0, 0, 70), (WIDTH // 2 - 120 + shake, 476, 240, 34))

    base = get_original_face_photo(variant)
    if base is None:
        base = get_teacher_pet_photo(variant)
    if base is not None:
        bounds = pygame.Rect(0, 0, int(250 * scale), int(312 * scale))
        bounds.center = (WIDTH // 2 + shake, 310 + jump)
        image, rect = contain_surface(base, bounds)
        screen.blit(image, rect)

    draw_text("...", START_TITLE_FONT, WHITE, WIDTH // 2 + shake, 86, center=True)


def draw_life_review(now):
    elapsed = elapsed_in_scene(now)
    reached_index = LIFE_STAGE_ORDER.index(game["life_stage"])
    reached_stages = LIFE_STAGE_ORDER[:reached_index + 1]
    review_duration = life_review_duration()

    if elapsed < review_duration:
        stage_index = min(len(reached_stages) - 1, elapsed // ENDING_STAGE_MS)
        stage_elapsed = elapsed % ENDING_STAGE_MS
        draw_review_stage(reached_stages[stage_index], stage_elapsed)
        draw_skip_button()
        return

    adult_elapsed = elapsed - review_duration
    if adult_elapsed >= ENDING_EVALUATION_MIN_MS:
        game["ending_controls_revealed"] = True
    screen.fill((242, 237, 229))

    reputation = game["final_reputation"]
    stats = game["final_stats"]
    is_clear = game["ending_type"] == "clear"
    is_reputation_death = game["ending_type"] == "reputation_death"
    title = "삶을 끝까지 완주했습니다." if is_clear else game["death_cause"]
    draw_text(title, TITLE_FONT, GREEN if is_clear else RED, WIDTH // 2, 34, center=True)
    if not is_clear:
        draw_text(f"사망 원인: {death_reason_label()}", TITLE_FONT, RED, WIDTH // 2, 78, center=True)

    emotion_variant, emotion_text, emotion_color = reputation_emotion(reputation)
    emotion_base = get_original_face_photo(emotion_variant)
    if emotion_base is not None:
        image_y = 106 if not is_clear else 74
        emotion_image, emotion_rect = contain_surface(emotion_base, pygame.Rect(WIDTH // 2 - 92, image_y, 184, 190 if not is_clear else 214))
        emotion_image = emotion_image.convert_alpha()
        emotion_image.set_alpha(min(255, int(adult_elapsed / 800 * 255)))
        screen.blit(emotion_image, emotion_rect)
    else:
        fallback = get_teacher_pet_photo(emotion_variant)
        if fallback is not None:
            image = pygame.transform.smoothscale(fallback, (172, 214)).convert_alpha()
            image.set_alpha(min(255, int(adult_elapsed / 800 * 255)))
            screen.blit(image, image.get_rect(center=(WIDTH // 2, 181)))
    draw_text(emotion_text, BIG_FONT, emotion_color, WIDTH // 2, 302, center=True)

    table = pygame.Rect(85, 330, WIDTH - 170, 205)
    rounded(table, WHITE, 12, LINE, 2)
    draw_text("최종 인생 평가", SMALL_FONT, DARK, table.centerx, table.y + 17, center=True)
    column_x = (table.x + 70, table.x + 190, table.x + 430)
    draw_text("항목", TINY_FONT, DARK, column_x[0], table.y + 41, center=True)
    draw_text("점수", TINY_FONT, DARK, column_x[1], table.y + 41, center=True)
    draw_text("평가", TINY_FONT, DARK, column_x[2], table.y + 41, center=True)
    pygame.draw.line(screen, LINE, (table.x + 18, table.y + 58), (table.right - 18, table.y + 58), 2)

    rows = [(key, STAT_INFO[key][0], stats[key]) for key in STAT_INFO]
    rows.append(("reputation", "평판", reputation))
    for index, (key, label, value) in enumerate(rows):
        y = table.y + 77 + index * 21
        draw_text(label, TINY_FONT, DARK, column_x[0], y, center=True)
        draw_text(str(value), TINY_FONT, PURPLE if key == "reputation" else DARK, column_x[1], y, center=True)
        draw_text(score_evaluation(key, value), TINY_FONT, BROWN, column_x[2], y, center=True)
        if index < len(rows) - 1:
            pygame.draw.line(screen, (236, 229, 216), (table.x + 18, y + 11), (table.right - 18, y + 11), 1)

    if is_reputation_death:
        summary = ["그녀가 무너지는 동안 당신은 무엇을 했습니까?", "당신은 지켜줄 수 있었습니다. 후회는 없습니까?"]
    elif is_clear and game["nursery_care_count"] > 0:
        summary = ["그녀는 마지막까지 가족과 함께했습니다.", "당신은 서은주의 긴 인생을 끝까지 책임졌습니다."]
    else:
        summary = overall_evaluation(stats, reputation)
    draw_text(summary[0], SMALL_FONT, RED if is_reputation_death else DARK, WIDTH // 2, 555, center=True)
    draw_text(summary[1], TINY_FONT, BROWN, WIDTH // 2, 578, center=True)

    buttons = ending_buttons()
    mouse = pygame.mouse.get_pos()
    if game["ending_controls_revealed"]:
        rounded(buttons["restart"], GREEN if buttons["restart"].collidepoint(mouse) else CARD, 10, LINE, 2)
        draw_text("다시 시작하기", FONT, DARK, buttons["restart"].centerx, buttons["restart"].centery, center=True)
    else:
        remaining = max(0, math.ceil((ENDING_EVALUATION_MIN_MS - adult_elapsed) / 1000))
        draw_text(f"평가 화면 유지 중... {remaining}초", SMALL_FONT, GRAY, WIDTH // 2 - 55, HEIGHT - 37, center=True)
    rounded(buttons["skip"], YELLOW if buttons["skip"].collidepoint(mouse) else CARD, 10, LINE, 2)
    draw_text("스킵", SMALL_FONT, DARK, buttons["skip"].centerx, buttons["skip"].centery, center=True)


def draw_resignation_ending(now):
    elapsed = elapsed_in_scene(now)
    if elapsed >= ENDING_EVALUATION_MIN_MS:
        game["ending_controls_revealed"] = True

    screen.fill((229, 241, 226))
    pygame.draw.circle(screen, (255, 218, 112), (WIDTH // 2, 190), 125)
    epilogue = game.get("resignation_epilogue")
    mood = game.get("resignation_epilogue_mood", "happy")
    if not epilogue:
        epilogue, mood = choose_resignation_epilogue()
        game["resignation_epilogue"] = epilogue
        game["resignation_epilogue_mood"] = mood
    pet = get_teacher_pet_photo(mood)
    if pet is not None:
        image = pygame.transform.smoothscale(pet, (230, 288)).convert_alpha()
        image.set_alpha(min(255, int(elapsed / 800 * 255)))
        screen.blit(image, image.get_rect(center=(WIDTH // 2, 260)))

    draw_text("학교 탈출 성공", START_TITLE_FONT, GREEN, WIDTH // 2, 72, center=True)
    draw_text("서은주는 마침내 사표를 제출하고 학교를 떠났습니다.", BIG_FONT, DARK, WIDTH // 2, 445, center=True)
    for index, line in enumerate(wrap_text(epilogue, FONT, WIDTH - 170)[:2]):
        draw_text(line, FONT, BROWN, WIDTH // 2, 486 + index * 28, center=True)
    draw_text(f"최종 평판 : {game['final_reputation']}", TITLE_FONT, PURPLE, WIDTH // 2, 555, center=True)

    buttons = ending_buttons()
    mouse = pygame.mouse.get_pos()
    if game["ending_controls_revealed"]:
        rounded(buttons["restart"], GREEN if buttons["restart"].collidepoint(mouse) else CARD, 10, LINE, 2)
        draw_text("다시 시작하기", FONT, DARK, buttons["restart"].centerx, buttons["restart"].centery, center=True)
    rounded(buttons["skip"], YELLOW if buttons["skip"].collidepoint(mouse) else CARD, 10, LINE, 2)
    draw_text("스킵", SMALL_FONT, DARK, buttons["skip"].centerx, buttons["skip"].centery, center=True)


def handle_ending_click(pos):
    buttons = ending_buttons()
    if buttons["skip"].collidepoint(pos):
        if current_scene == "life_review":
            skip_life_review()
        else:
            game["ending_controls_revealed"] = True
    elif game["ending_controls_revealed"] and buttons["restart"].collidepoint(pos):
        reset_to_start()


def handle_click(pos):
    if game.get("boss_test_confirm"):
        return
    if settings_button().collidepoint(pos) and not game["eating"]["active"]:
        open_settings(pygame.time.get_ticks())
        return

    if game["transition"]:
        return

    if game["resignation_event"]:
        if game["resignation_event"]["phase"] == "choose":
            for rect, hand in resignation_choice_buttons():
                if rect.collidepoint(pos):
                    choose_resignation_hand(hand)
                    break
        return

    if game["care_action"]["type"]:
        game["message"] = "행동이 끝날 때까지 잠시 기다려주세요."
        return

    if game["eating"]["active"]:
        game["message"] = "식사가 끝날 때까지 잠시 기다려주세요."
        return

    if game["office_work"]["active"]:
        if game["office_work"]["phase"] == "desktop" and grade_app_button().collidepoint(pos):
            open_grade_app()
        return

    if game["lesson"]["active"]:
        return

    if game["mini"]["active"] and game["room"] == "거실":
        click_mini(pos)
        return

    if game["room"] in ("집", "학교"):
        for rect, room in room_door_buttons():
            if rect.collidepoint(pos):
                start_location_transition(game["location"], room)
                return

    if commute_button().collidepoint(pos):
        commute()
        return

    if game["room"] not in ("집", "학교") and back_button().collidepoint(pos):
        hub = "집" if game["location"] == "home" else "학교"
        start_location_transition(game["location"], hub)
        return

    if game["room"] == "부엌":
        for rect, index, _food in food_buttons():
            if rect.collidepoint(pos):
                feed(index)
                return
    elif game["room"] == "화장실":
        if pygame.Rect(PHONE.right - 135, 236, 104, 48).collidepoint(pos):
            start_care_action("wash")
    elif game["room"] == "침실":
        if pygame.Rect(PHONE.right - 150, 236, 124, 48).collidepoint(pos):
            start_care_action("sleep")
    elif game["room"] == "아기방":
        if pygame.Rect(PHONE.right - 160, 236, 128, 48).collidepoint(pos):
            nursery_care()
    elif game["room"] == "교무실":
        if pygame.Rect(PHONE.right - 174, 270, 130, 46).collidepoint(pos):
            start_office_work()
    elif game["room"] == "반":
        if pygame.Rect(PHONE.right - 174, 345, 130, 46).collidepoint(pos):
            start_lesson()
    elif game["room"] == "교장실":
        if pygame.Rect(PHONE.right - 188, 270, 144, 48).collidepoint(pos):
            attempt_resignation()
    elif game["room"] == "거실":
        mini_rect = pygame.Rect(PHONE.centerx - 70, PHONE.bottom - 145, 140, 44)
        if mini_rect.collidepoint(pos):
            start_mini_game()
    elif game["room"] == "도박방":
        bet_buttons, choice_buttons = gamble_buttons()
        for rect, amount in bet_buttons:
            if rect.collidepoint(pos):
                if game["coins"] >= amount:
                    game["gamble_bet"] = amount
                else:
                    game["message"] = "코인이 부족합니다."
                return
        for rect, choice in choice_buttons:
            if rect.collidepoint(pos):
                play_gamble(choice)
                return


def handle_settings_click(pos, now):
    buttons = settings_controls()
    if buttons["resume"].collidepoint(pos):
        close_settings(now)
    elif buttons["restart"].collidepoint(pos):
        restart_game()
    elif buttons["sound"].collidepoint(pos):
        set_sound_enabled(not sound_enabled)
    elif buttons["music"].inflate(0, 20).collidepoint(pos):
        set_music_volume((pos[0] - buttons["music"].x) / buttons["music"].width)
    elif buttons["effects"].inflate(0, 20).collidepoint(pos):
        set_effects_volume((pos[0] - buttons["effects"].x) / buttons["effects"].width)


def handle_boss_test_confirm_click(pos):
    controls = boss_test_controls()
    if controls["yes"].collidepoint(pos):
        game["boss_test_confirm"] = False
        start_resignation_boss(test_mode=True)
    elif controls["no"].collidepoint(pos):
        game["boss_test_confirm"] = False


update_background_music("start")
running = True
while running:
    now = pygame.time.get_ticks()
    if current_scene == "start":
        update_start_animation(now)
    elif current_scene == "game":
        delta_ms = min(100, max(0, now - game["last_update"]))
        game["last_update"] = now
        if not game["settings_open"] and not game.get("boss_test_confirm"):
            update_game_clock(delta_ms)
            if current_scene == "game":
                update_location_transition(delta_ms)
                update_eating(delta_ms)
                update_coffee_penalty(delta_ms)
                update_care_action(delta_ms)
                update_resignation_event(delta_ms)
                update_lesson(delta_ms)
                update_office_work(delta_ms)
                decay(now)
                update_random_events(now)
                update_reputation_recovery(now)
                update_mini_game()
        if current_scene == "game" and game["game_over"] and not game["death_animation_done"]:
            if game["ending_type"] == "clear":
                change_scene("life_review")
            else:
                begin_death_transition()
    elif current_scene == "resignation_boss":
        delta_ms = min(100, max(0, now - game["last_update"]))
        game["last_update"] = now
        update_resignation_boss(delta_ms)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if current_scene == "game" and event.key == pygame.K_b:
                game["boss_test_confirm"] = True
            elif current_scene == "game" and event.key == pygame.K_y:
                skip_test_day()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if current_scene == "start":
                running = handle_start_screen(event)
            elif current_scene == "story":
                if story_skip_button().collidepoint(event.pos):
                    start_adult_intro()
            elif current_scene == "guide":
                if guide_start_button().collidepoint(event.pos):
                    start_game()
            elif current_scene == "game":
                if game.get("boss_test_confirm"):
                    handle_boss_test_confirm_click(event.pos)
                elif game["settings_open"]:
                    handle_settings_click(event.pos, now)
                else:
                    handle_click(event.pos)
            elif current_scene in ("life_review", "resignation_ending"):
                handle_ending_click(event.pos)
        elif event.type == pygame.MOUSEMOTION and event.buttons[0] and current_scene == "game" and game["settings_open"]:
            controls = settings_controls()
            if controls["music"].inflate(0, 20).collidepoint(event.pos):
                set_music_volume((event.pos[0] - controls["music"].x) / controls["music"].width)
            elif controls["effects"].inflate(0, 20).collidepoint(event.pos):
                set_effects_volume((event.pos[0] - controls["effects"].x) / controls["effects"].width)

    if current_scene == "start":
        draw_start_screen()
    elif current_scene == "story":
        draw_story_scene(now)
    elif current_scene == "adult_intro":
        draw_adult_intro(now)
    elif current_scene == "guide":
        draw_guide_screen()
    elif current_scene == "growth":
        draw_growth_scene(now)
    elif current_scene == "death_transition":
        draw_death_transition(now)
    elif current_scene == "life_review":
        draw_life_review(now)
    elif current_scene == "resignation_ending":
        draw_resignation_ending(now)
    elif current_scene == "resignation_boss":
        draw_resignation_boss()
    else:
        draw_game()

    draw_cheat_notice(now)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
