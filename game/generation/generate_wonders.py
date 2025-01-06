from ..game.models import Wonder, Stage, Resources

def generate_wonders():
    rhodes = Wonder(
        "Rhodos", "ore",
        stage1=Stage({"victory_points": 3}, {"wood": 2}),
        stage2=Stage({"shield": 2}, {"clay": 3}),
        stage3=Stage({"victory_points": 7}, {"ore": 4})
    )

    rhodes_night = Wonder(
        "Rhodo Night", "ore",
        stage1=Stage({"victory_points": 3, "shield":1, "coin":3}, {"stone": 3}),
        stage2=Stage({"victory_points": 4, "coin":4, "shield": 1}, {"ore": 4})
    )

    alexandria = Wonder(
        "Alexandria", "glass",
        stage1=Stage({"choices": [{"wood", "ore", "clay", "stone"}]}, {"clay": 2}),
        stage2=Stage({"choices": [{"glass":1, "papyrus":1, "cloth":1}]}, {"ore": 3}),
        stage3=Stage({"victory_points": 7}, {"wood": 4})
    )

    alexandria_night = Wonder(
        "Alexandria Night", "glass",
        stage1=Stage({"victory_points": 3}, {"stone": 2}),
        stage2=Stage({"choices": [{"wood":1, "ore":1, "clay":1, "stone":1}]}, {"stone": 2}),
        stage3=Stage({"victory_points": 7}, {"cloth": 1, "papyrus":1})
    )

    ephesus = Wonder(
        "Ephesus", "papyrus",
        stage1=Stage({"victory_points": 3}, {"clay": 2}),
        stage2=Stage({"coins": 9}, {"wood": 2}),
        stage3=Stage({"victory_points": 7}, {"ore":2, "glass": 1})
    )

    ephesus_night = Wonder(
        "Ephesus Night", "papyrus",
        stage1=Stage({"victory_points": 2, "coins":4}, {"stoe": 2}),
        stage2=Stage({"coins": 4, "victory_points":3}, {"wood": 2}),
        stage3=Stage({"victory_points": 4, "coins":4}, {"ore": 2, "cloth":1})
    )

    babylon = Wonder(
        "Babylon", "wood",
        stage1=Stage({"victory_points": 3}, {"clay": 2}),
        stage2=Stage({"choices": [{"gear": 1, "tablet": 1, "compass": 1}]}, {"ore":2, "cloth":1}),
        stage3=Stage({"victory_points":7}, {"wood": 4})
    )

    babylon_night = Wonder(
        "Babylon Night", "wood",
        stage1=Stage({"special":"play discarded"}, {"clay":2, "glass":1}),
        stage2=Stage({"choices": [{"gear": 1, "tablet": 1, "compass": 1}]}, {"clay":3, "glass":1})
    )

    olympia = Wonder(
        "Olympia", "clay",
        stage1=Stage({"victory_points": 3}, {"stone": 2}),
        stage2=Stage({"special":"first age card each color for free"}, {"wood": 2}),
        stage3=Stage({"victory_points": 7}, {"clay": 3})
    )

    olympia_night = Wonder(
        "Olympia Night", "clay",
        stage1=Stage({"victory_points": 2, "special": "construct the first age card in each age for free"}, {"ore": 2}),
        stage2=Stage({"victory_points": 3, "special": "construct the last age card in each age for free"}, {"clay": 3}),
        stage3=Stage({"victory_points": 5}, {"glass": 1, "papyrus":1, "cloth":1})
    )

    halicarnassus = Wonder(
        "Halicarnassus", "cloth",
        stage1=Stage({"victory_points": 3}, {"stone": 2}),
        stage2=Stage({"special": "at the end of the turn take a card from the discard pile and construct it for free"}, {"glass": 1, "papyrus":1}),
        stage3=Stage({"victory_points":7}, {"stone": 3})
    )

    halicarnassus_night = Wonder(
        "Halicarnassus Night", "cloth",
        stage1=Stage({"victory_points":2, "special": "at the end of the turn take a card from the discard pile and construct it for free"}, {"clay": 2}),
        stage2=Stage({"victory_points":1, "special": "at the end of the turn take a card from the discard pile and construct it for free"}, {"glass": 1, "papyrus":1}),
        stage3=Stage({"special": "at the end of the turn take a card from the discard pile and construct it for free"}, {"wood":3}),
    )

    gizah = Wonder(
        "Gizah", "stone",
        stage1=Stage({"victory_points": 3}, {"wood": 2}),
        stage2=Stage({"victory_points": 5}, {"clay": 2, "cloth":1}),
        stage3=Stage({"victory_points": 7}, {"stone": 4}),
    )

    gizah_night = Wonder(
        "Gizah Night", "stone",
        stage1=Stage({"victory_points": 3}, {"wood": 2}),
        stage2=Stage({"victory_points": 5}, {"stone": 3}),
        stage3=Stage({"victory_points": 5}, {"clay": 3}),
        stage4=Stage({"victory_points": 7}, {"stone": 4, "papyrus":1})
    )

    return [[rhodes,rhodes_night],
       	[alexandria, alexandria_night],
        [ephesus, ephesus_night],
        [babylon, babylon_night],
        [olympia, olympia_night],
        [halicarnassus, halicarnassus_night],
        [gizah, gizah_night]]
