#!/bin/env python3

import sys
import xml.etree.ElementTree as ET

if len(sys.argv) != 3:
  exit("Usage: " + sys.argv[0] + " rcj-soccer-sys-games-export.xml Output-Makefile")

root = ET.parse(sys.argv[1]).getroot()

games = []

for league in root.findall('leagues')[0]:
  for round in league.findall('leagueRound'):
    for match in round.findall('match'):
      game = {}
      game['name'] = match.attrib['name']
      game['team1'] = match.attrib['team1']
      game['team2'] = match.attrib['team2']
      games.append(game)

f = open(sys.argv[2], 'w')

f.write('all: ')
f.write(" ".join([game['name'] for game in games]))
#for game in games:
#  f.write(game['name'] + )

f.write('\n\n')

for game in games:
  f.write(game['name'] + ':\n')
  f.write('\tbash -c "TEAM_B=' + game['team2'] + ' TEAM_Y=' + game['team1'] + ' ./run-docker.sh"\n')
  f.write('\tbash -c "TEAM_B=' + game['team1'] + ' TEAM_Y=' + game['team2'] + ' ./run-docker.sh"\n')
