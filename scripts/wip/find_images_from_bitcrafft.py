import os
import shutil

search_dir = 'assets/data/AssetRipper_export_20250722_191126'
destination_dir = 'assets/data/images'
filenames_to_find = [
    'AbyssalOyster.png',
    'Aloe.png',
    'AncientThorns.png',
    'ArmoredReefClam.png',
    'BaobabTreeAncient.png',
    'BaobabTreeYoung.png',
    'BasaltStalagmite.png',
    'BeechTreeMature.png',
    'BeechTreeSapling.png',
    'BeechTreeYoung.png',
    'BentoniteClay.png',
    'BirchTreeMature.png',
    'BirchTreeSapling.png',
    'BirchTreeYoung.png',
    'Bluebell.png',
    'Bullrushes.png',
    'Bush.png',
    'BushBlackberry.png',
    'BushStrawberry.png',
    'Citriformis.png',
    'CloudberryBush.png',
    'CrystalShellScallop.png',
    'CypressTreeAncient.png',
    'CypressTreeMature.png',
    'CypressTreeSapling.png',
    'CypressTreeYoung.png',
    'Daisy.png',
    'DeadTree.png',
    'DendroTreeMature.png',
    'DendroTreeSapling.png',
    'DendroTreeYoung.png',
    'DesertRose.png',
    'DioriteBoulder.png',
    'DioritePillar.png',
    'DioritePillarInterior.png',
    'ExquisiteHieroglyphs.png',
    'Ferns.png',
    'FineHieroglyphs.png',
    'Fireweed.png',
    'Flint.png',
    'Fossils.png',
    'FrenziedSchoolOfAbyssalSwordfish.png',
    'FrenziedSchoolOfAzureSharks.png',
    'FrenziedSchoolOfOceancrestMarlins.png',
    'FrenziedSchoolOfSeastormTuna.png',
    'FrenziedSchoolOfSerpentFish.png',
    'FrenziedSchoolOfWavecrestEel.png',
    'GardenFormation.png',
    'GardenFormationInterior.png',
    'GardenPillarA.png',
    'GardenPillarB.png',
    'GardenPillarC.png',
    'GardenPillarD.png',
    'GardenPillarInterior.png',
    'Bamboo.png',
    'Brambles.png',
    'ClayT1.png',
    'ClayT10.png',
    'ClayT2.png',
    'ClayT3.png',
    'ClayT4.png',
    'ClayT5.png',
    'ClayT6.png',
    'ClayT7.png',
    'ClayT8.png',
    'ClayT9.png',
    'ElephantEar.png',
    'HeartPowerSource.png',
    'Jute.png',
    'MushroomT1.png',
    'MushroomT10.png',
    'MushroomT2.png',
    'MushroomT3.png',
    'MushroomT4.png',
    'MushroomT5.png',
    'MushroomT6.png',
    'MushroomT7.png',
    'MushroomT8.png',
    'MushroomT9.png',
    'OreVeinT1.png',
    'OreVeinT10.png',
    'OreVeinT2.png',
    'OreVeinT3.png',
    'OreVeinT4.png',
    'OreVeinT5.png',
    'OreVeinT6.png',
    'OreVeinT7.png',
    'OreVeinT8.png',
    'OreVeinT9.png',
    'OutcropT10.png',
    'OutcropT2.png',
    'OutcropT3.png',
    'OutcropT4.png',
    'OutcropT5.png',
    'OutcropT6.png',
    'OutcropT7.png',
    'OutcropT8.png',
    'OutcropT9.png',
    'Palmetto.png',
    'Seaweed.png',
    'TravelersFruit.png',
    'GhostSucculent.png',
    'GhostThyme.png',
    'GiantGroundselPlant.png',
    'GoldenWitlow.png',
    'GraniteBoulder.png',
    'GrassyReeds.png',
    'Heather.png',
    'HoneyberryBush.png',
    'JuniperBerryBush.png',
    'KingOfTheAlps.png',
    'LargeBrambles.png',
    'LargeGardenBoulderA.png',
    'LargeGardenFormation.png',
    'LargeRockyGardenPillars.png',
    'LimestoneBoulder.png',
    'LimestoneOutcrop.png',
    'MapleTreeGnarled.png',
    'MapleTreeMature.png',
    'MapleTreeSapling.png',
    'MapleTreeYoung.png',
    'MarbleBoulder.png',
    'Marigold.png',
    'MistberryBush.png',
    'MorningGlory.png',
    'MudMound.png',
    'NeatHieroglyphs.png',
    'OakTreeAncient.png',
    'OakTreeMature.png',
    'OakTreeSapling.png',
    'OakTreeYoung.png',
    'OysterMushrooms.png',
    'PearlbackSnail.png',
    'PeerlessHieroglyphs.png',
    'PineTreeAncient.png',
    'PineTreeMature.png',
    'PineTreeSapling.png',
    'PineTreeYoung.png',
    'PineWeed.png',
    'PinkLilies.png',
    'PricklyPear.png',
    'RedArcticGrass.png',
    'ReindeerLichen.png',
    'RockyGardenBoulderA.png',
    'Rosemary.png',
    'RottenLog.png',
    'RottenStump.png',
    'RoughHieroglyphs.png',
    'SaltDeposit.png',
    'SandcoveredFossils.png',
    'SandstoneBoulder.png',
    'SchoolOfAbyssalSwordfish.png',
    'SchoolOfAzureSharks.png',
    'SchoolOfBreezyFinDarters.png',
    'SchoolOfCoralcrestDarter.png',
    'SchoolOfEmberfinShiners.png',
    'SchoolOfEmberscaleSturgeon.png',
    'SchoolOfHexfinPerch.png',
    'SchoolOfMossfinChub.png',
    'SchoolOfOceancrestMarlins.png',
    'SchoolOfSeastormTuna.png',
    'SchoolOfSerpentFish.png',
    'SchoolOfShrimpT1.png',
    'SchoolOfShrimpT2.png',
    'SchoolOfShrimpT3.png',
    'SchoolOfShrimpT4.png',
    'SchoolOfShrimpT5.png',
    'SchoolOfShrimpT6.png',
    'SchoolOfWavecrestEel.png',
    'SeasideClam.png',
    'ShaleBoulder.png',
    'SilkenHexmoths.png',
    'SimpleHieroglyphs.png',
    'SnowdropFlowers.png',
    'SpanishMoss.png',
    'SpruceTreeMature.png',
    'SpruceTreeSapling.png',
    'SpruceTreeYoung.png',
    'Sticks.png',
    'Thyme.png',
    'ToughShelledMussel.png',
    'WhiteLily.png',
    'WildDaisies.png',
    'WildDandelion.png',
    'Wildflowers.png',
    'WildGrains.png',
    'WildOnion.png',
    'WildPeppermint.png',
    'WillowTreeMature.png',
    'WillowTreeSapling.png',
    'WillowTreeYoung.png',
    'DepletedResource.png',
    'EnergySource.png',
    'FlaxLog.png',
    'GemEncrustedStalagmite.png',
    'KeyPillarEmpty.png',
    'LargeLavender.png',
    'LargeLimestoneRock1.png',
    'LargeLimestoneRock2.png',
    'LeverDoorContraptionState1.png',
    'LeverDoorContraptionState2.png',
    'MediumLavender.png',
    'PartiallyPoweredDoor.png',
    'PoweredDoor.png',
    'SchoolOfMuckfin.png',
    'UnpoweredDoor.png'
]

'''
os.makedirs(destination_dir, exist_ok=True)
for filename in filenames_to_find:
    file_found = False

    for root, dirs, files in os.walk(search_dir):
        if filename in files:
            src_path = os.path.join(root, filename)
            dest_path = os.path.join(destination_dir, filename)

            shutil.copy2(src_path, dest_path)
            print(f"Found and copied: {filename}")
            file_found = True
            break  # stop searching once found

    if not file_found:
        print(f"{filename} not found")
'''
os.makedirs(destination_dir, exist_ok=True)  # Make sure destination exists
found_any = False
for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.lower().endswith(".png"):
            src_path = os.path.join(root, file)
            dest_path = os.path.join(destination_dir, file)

            # If duplicate filenames exist, rename them to avoid overwrite
            if os.path.exists(dest_path):
                name, ext = os.path.splitext(file)
                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(destination_dir, f"{name}_{counter}{ext}")
                    counter += 1

            shutil.copy2(src_path, dest_path)
            print(f"Copied: {src_path} -> {dest_path}")
            found_any = True

print("\nFiles in destination folder:")
for file in os.listdir(destination_dir):
    file_path = os.path.join(destination_dir, file)
    if os.path.isfile(file_path):
        size_kb = os.path.getsize(file_path) / 1024
        print(f"{file} - {size_kb:.2f} KB")