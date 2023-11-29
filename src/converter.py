import base64
import os
import shutil
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Converts the game to a Linux-compatible version.')

parser.add_argument('arg1', nargs='?', type=str, help='Path to the game directory, if not given it will default to the default Steam directory')
parser.add_argument('arg2', nargs='?', type=str, help='Path to the new game directory, if not given it will be created in the script\'s directory')

args = parser.parse_args()

# The string will be supplied by the generator
RUNNER_BINARY_STRING = ''
RUNNER_BINARY = base64.b64decode(RUNNER_BINARY_STRING)

# Steam folder name
DELTARUNE_NAME = 'DELTARUNEdemo'

# Path to the directory where the game is located
DELTARUNE_PATH = args.arg1 if args.arg1 else os.path.expanduser(f'~/.steam/steam/steamapps/common/{DELTARUNE_NAME}')

if (not os.path.isdir(DELTARUNE_PATH)):
    if (args.arg1):
        print(f'The game directory {args.arg1} was not found.')
    else:
        print('The game directory was not found. Please supply it as an argument.')
    subprocess.run(['python3', os.path.realpath(__file__), '-h'])
    exit()

# Path where the new game will be created
NEW_DELTARUNE_PATH = args.arg2 if args.arg2 else os.path.join(os.getcwd(), DELTARUNE_NAME)

# Subdirectories that need to be created
DELTARUNE_DIRECTORIES = [
    'mus',
    'lang'
]

# File that will be copied, converting to lower case because of case-insensitive filesystems
DELTARUNE_FILES = [
    'audiogroup1.dat',
    'AUDIO_INTRONOISE.ogg',
    'AUDIO_INTRONOISE_ch1.ogg',
    'data.win',
    'options.ini',
    'snd_bigcar_yelp.ogg',
    'snd_closet_fall.ogg',
    'snd_closet_fall_ch1.ogg',
    'snd_closet_impact.ogg',
    'snd_closet_impact_ch1.ogg',
    'snd_dtrans_drone.ogg',
    'snd_dtrans_flip.ogg',
    'snd_dtrans_heavypassing.ogg',
    'snd_dtrans_lw.ogg',
    'snd_dtrans_square.ogg',
    'snd_dtrans_twinkle.ogg',
    'snd_fountain_make.ogg',
    'snd_fountain_target.ogg',
    'snd_ghostappear.ogg',
    'snd_great_shine.ogg',
    'snd_great_shine_ch1.ogg',
    'snd_him_quick.ogg',
    'snd_hitcar.ogg',
    'snd_hitcar_little.ogg',
    'snd_icespell.ogg',
    'snd_paper_rumble.ogg',
    'snd_paper_rumble_ch1.ogg',
    'snd_paper_surf.ogg',
    'snd_paper_surf_ch1.ogg',
    'snd_power',
    'snd_revival.ogg',
    'snd_revival_ch1.ogg',
    'snd_rurus_appear.ogg',
    'snd_rurus_appear_ch1.ogg',
    'snd_smallcar_yelp.ogg',
    'snd_snowgrave.ogg',
    'snd_spell_pacify.ogg',
    'snd_usefountain.ogg',
    'snd_usefountain_ch1.ogg',
    'Steamworks.dll',
    'lang/lang_en_ch1.json',
    'lang/lang_ja.json',
    'lang/lang_ja_ch1.json',
    'mus/acid_tunnel.ogg',
    'mus/alarm_titlescreen.ogg',
    'mus/alley_ambience.ogg',
    'mus/april_2012.ogg',
    'mus/AUDIO_ANOTHERHIM.ogg',
    'mus/AUDIO_DARKNESS.ogg',
    'mus/AUDIO_DEFEAT.ogg',
    'mus/AUDIO_DRONE.ogg',
    'mus/AUDIO_STORY.ogg',
    'mus/basement.ogg',
    'mus/battle.ogg',
    'mus/berdly_audience.ogg',
    'mus/berdly_battle_heartbeat_true.ogg',
    'mus/berdly_chase.ogg',
    'mus/berdly_descend.ogg',
    'mus/berdly_flashback.ogg',
    'mus/berdly_theme.ogg',
    'mus/bird.ogg',
    'mus/boxing_boss.ogg',
    'mus/boxing_game.ogg',
    'mus/card_castle.ogg',
    'mus/castletown.ogg',
    'mus/castletown_empty.ogg',
    'mus/ch2_credits.ogg',
    'mus/charjoined.ogg',
    'mus/checkers.ogg',
    'mus/coolbeat.ogg',
    'mus/creepychase.ogg',
    'mus/creepydoor.ogg',
    'mus/creepylandscape.ogg',
    'mus/cyber.ogg',
    'mus/cybercity.ogg',
    'mus/cybercity_alt.ogg',
    'mus/cybercity_old.ogg',
    'mus/cyberhouse.ogg',
    'mus/cybershop_christmas.ogg',
    'mus/cyber_battle.ogg',
    'mus/cyber_battle_end.ogg',
    'mus/cyber_battle_prelude.ogg',
    'mus/cyber_shop.ogg',
    'mus/d.ogg',
    'mus/deep_noise.ogg',
    'mus/dogcheck.ogg',
    'mus/dontforget.ogg',
    'mus/elevator.ogg',
    'mus/fanfare.ogg',
    'mus/field_of_hopes.ogg',
    'mus/flashback_excerpt.ogg',
    'mus/forest.ogg',
    'mus/friendship.ogg',
    'mus/GALLERY.ogg',
    'mus/gameover_short.ogg',
    'mus/giant_queen_appears.ogg',
    'mus/gigaqueen_pre.ogg',
    'mus/hip_shop.ogg',
    'mus/home.ogg',
    'mus/honksong.ogg',
    'mus/joker.ogg',
    'mus/KEYGEN.ogg',
    'mus/kingboss.ogg',
    'mus/lancer.ogg',
    'mus/lancerfight.ogg',
    'mus/lancer_susie.ogg',
    'mus/legend.ogg',
    'mus/man.ogg',
    'mus/mansion.ogg',
    'mus/mansion_entrance.ogg',
    'mus/menu.ogg',
    'mus/muscle.ogg',
    'mus/music_guys.ogg',
    'mus/music_guys_intro.ogg',
    'mus/mus_birdnoise.ogg',
    'mus/mus_introcar.ogg',
    'mus/mus_school.ogg',
    'mus/napsta_alarm.ogg',
    'mus/noelle.ogg',
    'mus/noelle_ferriswheel.ogg',
    'mus/noelle_normal.ogg',
    'mus/noelle_school.ogg',
    'mus/ocean.ogg',
    'mus/prejoker.ogg',
    'mus/queen.ogg',
    'mus/queen_boss.ogg',
    'mus/queen_car_radio.ogg',
    'mus/queen_intro.ogg',
    'mus/quiet_autumn.ogg',
    'mus/rouxls_battle.ogg',
    'mus/ruruskaado.ogg',
    'mus/shinkansen.ogg',
    'mus/shop1.ogg',
    'mus/sink_noise.ogg',
    'mus/spamton_basement.ogg',
    'mus/spamton_battle.ogg',
    'mus/spamton_happy.ogg',
    'mus/spamton_house.ogg',
    'mus/spamton_laugh_noise.ogg',
    'mus/spamton_meeting.ogg',
    'mus/spamton_meeting_intro.ogg',
    'mus/spamton_neo_after.ogg',
    'mus/spamton_neo_meeting.ogg',
    'mus/spamton_neo_mix_ex_wip.ogg',
    'mus/static_placeholder.ogg',
    'mus/s_neo.ogg',
    'mus/s_neo_clip.ogg',
    'mus/tense.ogg',
    'mus/the_dark_truth.ogg',
    'mus/THE_HOLY.ogg',
    'mus/thrashmachine.ogg',
    'mus/thrash_rating.ogg',
    'mus/town.ogg',
    'mus/tv_noise.ogg',
    'mus/vs_susie.ogg',
    'mus/w.ogg',
    'mus/wind.ogg',
    'mus/wind_highplace.ogg'
]

assets_path = os.path.join(NEW_DELTARUNE_PATH, 'assets')

for directory in DELTARUNE_DIRECTORIES:
    os.makedirs(os.path.join(assets_path, directory), exist_ok=True)

for file in DELTARUNE_FILES:
    file_path = os.path.join(DELTARUNE_PATH, file)
    if (os.path.isfile(file_path)):
        shutil.copy(file_path, os.path.join(assets_path, file.lower()))

# Rename it so it works on Linux
os.rename(os.path.join(assets_path, 'data.win'), os.path.join(assets_path, 'game.unx'))

runner_path = os.path.join(NEW_DELTARUNE_PATH, "runner")

with open(runner_path, "wb") as f:
    f.write(RUNNER_BINARY)

# Give executable perms
subprocess.run(['chmod', '+rwx', runner_path])

# Download needed library
LIBRARY_LINK = ''
LIBRARY_FILE = ''
subprocess.run(['wget', LIBRARY_LINK])
subprocess.run(['sudo', 'dpkg', '-i', LIBRARY_FILE])
os.remove(os.path.join(os.getcwd(), LIBRARY_FILE))