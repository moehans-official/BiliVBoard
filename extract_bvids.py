import json

with open('/workspace/songs.json') as f:
    songs = json.load(f)

bvids = [s['bvid'] for s in songs if s.get('bvid')]

with open('/workspace/DataCollector/bvid.txt', 'w') as f:
    for bvid in bvids:
        f.write(bvid + '\n')

print(f'Wrote {len(bvids)} BVIDs to bvid.txt')
