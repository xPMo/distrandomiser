#!/usr/bin/env python
import distance, random, sys, os, collections, glob

# Change to true if you want debug output (this will be a command line
# flag eventually)
debug = False

version = '0.1-alpha'

def debug_print(text):
    if debug:
        print(text)

# Get the directory passed
try:
    if not sys.argv[1] == "--version":
        leveldir = sys.argv[1] + '/'
    else:
        print(f'Distrandomiser Version {version}')
        exit()
except IndexError:
    # Use the current working directory
    leveldir = ''

# Level name shorthands, for convenience
bs = f'{leveldir}broken symmetry.bytes'
ls = f'{leveldir}lost society.bytes'
ns = f'{leveldir}negative space.bytes'
de = f'{leveldir}departure.bytes'
gz = f'{leveldir}ground zero.bytes'
af = f'{leveldir}aftermath.bytes'
fr = f'{leveldir}friction.bytes'
ma = f'{leveldir}the thing about machines.bytes'
co = f'{leveldir}corruption.bytes'
mo = f'{leveldir}monolith.bytes'
du = f'{leveldir}destination unknown.bytes'
cr = f'{leveldir}credits.bytes'

# Get the location of the Distance directory
if sys.platform == 'linux' or sys.platform == 'linux2':
    distdir = os.path.expanduser('~/.config/refract/Distance')
elif sys.platform == 'darwin':
    distdir = os.path.expanduser('~/Library/Application Support/Refract/Distance')
elif sys.platform == 'windows':
    distdir = os.path.expanduser('~/My Games/Distance')

# This requires some explanation. It seems the distance module doesn't have
# setters on the ability settings on the enable triggers, but you CAN
# alter the transform. So... here I have all the transforms for each
# level's ability box, and obtain every ability box in advance so I
# can alter the abilities enabled on each level.
#
# ...This is the most ridiculous hack I think I've ever written.
# Desperate times call for desperate measures, indeed... at least
# it works?
bs_abox_transform = ((691.8410034179688, 7.955999851226807, -2433.93310546875), (0, 0, 0, 1), (66.25, 66.25, 362.3999938964844))
ls_abox_transform = ((-685.8243408203125, 26.670000076293945, -389.71746826171875), (0.0, 0.5000000596046448, 0.0, -0.8660253882408142), (112.78399658203125, 112.78399658203125, 484.0814208984375))
de_abox_trasnform = ((-3988.756103515625, -29.958999633789062, -2159.41552734375), (0, 0, 0, 1), (200.0, 200.0, 638.0))
af_abox_transform = ((383.33331298828125, 164.0807647705078, -6622.5146484375), (0.3420201539993286, 0.9396926760673523, -1.719538545330579e-06, -9.84505049927975e-07), (199.99996948242188, 200.0, 529.7343139648438))
mo_abox_transform = ((-211.4759979248047, 116.73799896240234, -5069.0400390625), (0, 0, 0, 1), (268.1130065917969, 268.1130065917969, 268.1130065917969))

# Get the ability boxes
for lvl in [ls, de, af]:
    lvlbytes = distance.Level(lvl)
    for obj in lvlbytes.layers[0].objects:
        if obj.type == 'EnableAbilitiesBox':
            if obj.abilities['EnableJumping'] == 1:
                jump_abox = obj
            elif obj.abilities['EnableFlying'] == 1:
                wings_abox = obj
            elif obj.abilities['EnableJetRotating'] == 1:
                jets_abox = obj

aboxes = [jump_abox, wings_abox, jets_abox]


#available_levels = [bs, ls, ns, de, gz, af, fr, ma, co, mo, du, cr]
available_levels = [bs, ls, ns, de, gz, af, fr, ma, co, mo]
available_abilities = ['EnableJumping', 'EnableJetRotating',
                       'EnableFlying']

# This is used to keep track of the levels currently in the playlist
tracked_levels = []

# Same, but abilities
tracked_abilities = []

# Keep track of what abilities the player has
boost_enabled = True
jump_enabled = False
wings_enabled = False
jets_enabled = False

print(f'Distrandomiser Version {version}\n')

# 1 = Standard
# 1337 = No softlock checking, essentially a test mode
mode = 1337

if mode == 1:
    #requires_jets = [fr, ma, co]
    requires_jets = []
    requires_jump = [ns, fr, af, ma, mo, du]
    requires_boost = [de, gz, af]
    # These can be done with jets as well.
    requires_wings = [fr, ma, gz, du, mo, af]
elif mode == 1337:
    requires_jets = []
    requires_jump = []
    requires_boost = []
    requires_wings = []


seed = input('Seed (type nothing for random seed): ')

if seed == '':
    seed = None
    print('Generating randomiser game with random seed...')
else:
    print(f'Generating randomiser game with seed {seed}...')

random.seed(seed)

ability_order = []

while len(ability_order) < 3:
    if len(ability_order) == 0:
        selectint = random.randint(0,2)
    elif len(ability_order) == 1:
        selectint = random.randint(0,1)
    elif len(ability_order) == 2:
        selectint = 0

    ability_order.append(available_abilities[selectint])
    available_abilities.remove(available_abilities[selectint])

ability_trigger_count = 0

debug_print(ability_order)

#while len(tracked_levels) != 12:
while len(tracked_levels) != 10:
    level = available_levels[random.randint(0,len(available_levels) - 1)]

    if level not in tracked_levels:

        debug_print(level)
        if level in requires_jump and not jump_enabled:
            debug_print('needs jump!')
            continue
        if level in requires_wings:
            if not wings_enabled and not jets_enabled:
                debug_print('needs rotation!')
                continue

        lvlbytes = distance.Level(level)
        lvlbytes.settings.name = '???'
        lvlbytes.settings.modes = collections.OrderedDict([(5,0), (13,0), (1,0), (2,0), (8,0)])
        lvlbytes.settings.abilities = (0,
                                       int(not wings_enabled),
                                       int(not jump_enabled),
                                       int(not boost_enabled),
                                       int(not jets_enabled)
        )

        unwanted_objects = ['AdventureAbilitySettings', 'WingCorruptionZone',
                            'WingCorruptionZoneLarge', 'InfoDisplayBox',
                            'InfoAndIndicatorDisplayBox']
        objects = [obj for obj in lvlbytes.layers[0].objects if obj.type not in unwanted_objects]

        origabox = next((obj for obj in objects if obj.type == 'EnableAbilitiesBox'), None)
        if origabox != None:
            if len(tracked_abilities) < 3:
                ability = ability_order[len(tracked_abilities)]
                if ability == 'EnableJumping':
                    if level == de:
                        if not jets_enabled and not wings_enabled:
                            debug_print('level can\'t give jump; it needs flight')
                            continue
                        else:
                            abox = jump_abox
                    else:
                        abox = jump_abox
                elif ability == 'EnableFlying':
                    abox = wings_abox
                elif ability == 'EnableJetRotating':
                    abox = jets_abox
                tracked_abilities.append(ability)
            else:
                abox = aboxes[random.randint(0,2)]

            if abox == jump_abox:
                jump_enabled = True
                debug_print('jump on')
            elif abox == wings_abox:
                wings_enabled = True
                debug_print('wings on')
            elif abox == jets_abox:
                jets_enabled = True
                debug_print('jets on')

            abox.transform = origabox.transform
            # Set the IDs to stupid high numbers to prevent conflicts
            # Flimsy solution, but it works
            abox.container.id = 99996
            lastid = 99996
            for fragment in abox.fragments:
                lastid + 1
                fragment.container.id = lastid
            objects.remove(origabox)
            objects.append(abox)


        debug_print('added ' + level)
        tracked_levels.append(level)
        available_levels.remove(level)
        #print(tracked_levels)


        lvlbytes.layers[0].objects = objects

        # Write the modified data
        print(f'Writing randomiser{len(tracked_levels)}.bytes...')
        lvlbytes.write(f'{distdir}/Levels/MyLevels/randomiser{len(tracked_levels)}.bytes')

debug_print(tracked_levels)

playlisttext = '<GameObject Name="LevelPlaylist" GUID="0">\n' + \
                    '<Transform Version="0" GUID="0" />\n' + \
                    '<LevelPlaylist Version="0" GUID="0">\n' + \
                    '<PlaylistName>Randomiser</PlaylistName>\n' + \
                    f'<NumberOfLevelsInPlaylist>{len(tracked_levels)}</NumberOfLevelsInPlaylist>\n' + \
                    '<ModeAndLevelInfoVersion>0</ModeAndLevelInfoVersion>\n'

runs = 0
for level in tracked_levels:
    runs += 1
    playlisttext += '<GameMode>9</GameMode>\n' + \
                    '<LevelName>???</LevelName>\n' + \
                    f'<LevelPath>MyLevels/randomiser{runs}.bytes</LevelPath>'

playlisttext += '</LevelPlaylist>\n</GameObject>'

print(f'Writing randomiser.xml...')
with open(f'{distdir}/LevelPlaylists/randomiser.xml', 'w') as playlistfile:
    playlistfile.write(playlisttext)
