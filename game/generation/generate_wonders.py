from ..game.models import Wonder, Stage, Resources

def generate_wonders():
    colossus_of_rhodes = Wonder(
        "Colossus of Rhodes", "ore",
        stage1=Stage({"shield": 1, "victory_points": 3}, {"wood": 2}),
        stage2=Stage({"victory_points": 4}, {"clay": 3}),
        stage3=Stage({"shield": 1, "victory_points": 7}, {"ore": 4})
    )

    colossus_of_rhodes_night = Wonder(
        "Colossus of Rhodes Night", "ore",
        stage1=Stage({"victory_points": 3}, {"wood": 2}),
        stage2=Stage({"victory_points": 4, "shield": 1}, {"clay": 3}),
        stage3=Stage({"shield": 2, "victory_points": 7}, {"ore": 4})
    )

    lighthouse_of_alexandria = Wonder(
        "Lighthouse of Alexandria", "glass",
        stage1=Stage({"choices": ["wood", "ore", "clay", "stone"], "victory_points": 3}, {"stone": 2}),
        stage2=Stage({"victory_points": 4}, {"ore": 2}),
        stage3=Stage({"victory_points": 7, "choices": ["cloth", "papyrus", "glass"]}, {"glass": 3})
    )

    lighthouse_of_alexandria_night = Wonder(
        "Lighthouse of Alexandria Night", "glass",
        stage1=Stage({"choices": ["wood", "ore", "clay", "stone"], "victory_points": 3}, {"stone": 2}),
        stage2=Stage({"victory_points": 5, "choices": ["cloth", "papyrus", "glass"]}, {"ore": 2}),
        stage3=Stage({"victory_points": 7, "choices": ["cloth", "papyrus", "glass", "ore", "stone", "wood", "clay"]}, {"glass": 3})
    )

    temple_of_artemis_in_ephesus = Wonder(
        "Temple of Artemis in Ephesus", "papyrus",
        stage1=Stage({"victory_points": 3, "coins": 4}, {"stone": 2}),
        stage2=Stage({"victory_points": 5, "coins": 4}, {"wood": 2}),
        stage3=Stage({"victory_points": 7, "coins": 4}, {"papyrus": 3})
    )

    temple_of_artemis_in_ephesus_night = Wonder(
        "Temple of Artemis in Ephesus Night", "papyrus",
        stage1=Stage({"victory_points": 2, "coins": 9}, {"stone": 2}),
        stage2=Stage({"victory_points": 1, "coins": 4}, {"wood": 2}),
        stage3=Stage({"victory_points": 5, "coins": 4}, {"papyrus": 3})
    )

    hanging_gardens_of_babylon = Wonder(
        "Hanging Gardens of Babylon", "clay",
        stage1=Stage({"victory_points": 3}, {"clay": 2}),
        stage2=Stage({"victory_points": 7}, {"wood": 3}),
        stage3=Stage({"choices": ["compass", "gear", "tablet"]}, {"clay": 4})
    )

    hanging_gardens_of_babylon_night = Wonder(
        "Hanging Gardens of Babylon Night", "clay",
        stage1=Stage({"victory_points": 3, "choices": ["compass", "tablet", "gear"]}, {"clay": 2}),
        stage2=Stage({"victory_points": 4}, {"wood": 3}),
        stage3=Stage({"choices": ["compass", "gear", "tablet"], "victory_points": 7}, {"clay": 4})
    )

    statue_of_zeus_in_olympia = Wonder(
        "Statue of Zeus in Olympia", "wood",
        stage1=Stage({"victory_points": 3, "special": "one free build per age"}, {"wood": 2}),
        stage2=Stage({"victory_points": 5}, {"stone": 2}),
        stage3=Stage({"shield": 1, "victory_points": 7}, {"ore": 2})
    )

    statue_of_zeus_in_olympia_night = Wonder(
        "Statue of Zeus in Olympia Night", "wood",
        stage1=Stage({"victory_points": 3, "shield": 1}, {"wood": 2}),
        stage2=Stage({"victory_points": 5, "special": "one free build per age"}, {"stone": 2}),
        stage3=Stage({"shield": 1, "victory_points": 7}, {"ore": 2})
    )

    mausoleum_of_halicarnassus = Wonder(
        "Mausoleum of Halicarnassus", "cloth",
        stage1=Stage({"victory_points": 3}, {"clay": 2}),
        stage2=Stage({"victory_points": 5}, {"wood": 3}),
        stage3=Stage({"special": "build one discarded card for free"}, {"stone": 3})
    )

    mausoleum_of_halicarnassus_night = Wonder(
        "Mausoleum of Halicarnassus Night", "cloth",
        stage1=Stage({"special": "build one discarded card for free", "victory_points": 2}, {"clay": 2}),
        stage2=Stage({"special": "build one discarded card for free", "victory_points": 1}, {"wood": 2}),
        stage3=Stage({"special": "build one discarded card for free", "victory_points": 3}, {"stone": 3})
    )

    pyramids_of_giza = Wonder(
        "Pyramids of Giza", "stone",
        stage1=Stage({"victory_points": 3}, {"wood": 2}),
        stage2=Stage({"victory_points": 5}, {"stone": 3}),
        stage3=Stage({"victory_points": 7}, {"wood": 4}),
        stage4=Stage({"victory_points": 9}, {"stone": 5})
    )

    pyramids_of_giza_night = Wonder(
        "Pyramids of Giza Night", "stone",
        stage1=Stage({"victory_points": 3}, {"wood": 2}),
        stage2=Stage({"victory_points": 5}, {"stone": 3}),
        stage3=Stage({"victory_points": 5}, {"wood": 4}),
        stage4=Stage({"victory_points": 5}, {"stone": 5})
    )

    return [[colossus_of_rhodes,colossus_of_rhodes_night],
       	[lighthouse_of_alexandria, lighthouse_of_alexandria_night],
        [temple_of_artemis_in_ephesus, temple_of_artemis_in_ephesus_night],
        [hanging_gardens_of_babylon, hanging_gardens_of_babylon_night],
        [statue_of_zeus_in_olympia, statue_of_zeus_in_olympia_night],
        [mausoleum_of_halicarnassus, mausoleum_of_halicarnassus_night],
        [pyramids_of_giza, pyramids_of_giza_night]]
