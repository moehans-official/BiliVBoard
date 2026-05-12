def load_bvids(filename='bvid.txt'):
    bvids = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and '#' in line:
                line = line.split('#')[0].strip()
            if line:
                bvids.append(line)
    return bvids


def truncate_score(score):
    """抹零功能：去掉小数点后的数字，直接取整"""
    return int(score)
