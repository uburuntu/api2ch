from pathlib import Path

# In case of apocalypse - use any of `api_mirrors`
API_BASE = 'https://2ch.hk'

hostname_mirrors = (
    '2ch.hk',
    '2ch.pm',
    '2ch.re',
    '2ch.tf',
    '2ch.wf',
    '2ch.yt',
    '2-ch.so',
)

api_mirrors = tuple(f'https://{hostname}' for hostname in hostname_mirrors)

BOARDS = (
'b', 'po', 'vg', 'fag', 'news', 'sex', 'rf', 'hw', 'v', '2d', 'by', 'wrk', 'soc', 'ftb', 'pr', 'psy', 'kpop', 'dr', 'sp', 'mov', 'au',
'mobi', 'spc', 'fiz', 'hi', 'a', 'biz', 'em', 'ma', 'd', 'mus', 'pa', 'cg', 'gg', 'mu', 'fl', 'es', 'ga', 'fa', 'gsg', 'mg', 'un', 'fs',
'bi', 'me', 'tes', 'di', 'fet', 'm', 's', 'td', 'e', 'hry', 'p', 'c', 're', 'w', 'wm', 'fd', 'zog', 't', 'rm', 'ch', 'tv', 'fg', 'gd',
'alco', 'socionics', 'bg', 'hc', 'cc', 'mo', 'diy', 'r', 'vape', 'bo', 'mlp', 'mmo', 'wr', 'ho', 'asmr', 'math', 'hh', 'pvc', 'sf', 'vn',
'dom', 'h', 'trv', 'out', 'sw', 'law', 'qtr4', 'se', 'brg', 'o', 'int', 'ruvn', 'ew', 'ne', 'sn', 'tr', 'wh', 'de', 'izd', 'aa', 'old',
'kz', 'hv', 'wwe', 'whn', 'ph', 'ra', 'sci', 'wp', 'mc', 'ja', 'to', 'fur', 'web', 'br', 'gb', 'moba', 'abu', 'cul', 'media', 'guro',
'ussr', 'jsf', 'ukr', 'ya', 'r34', 'wow', 'gabe', 'cute', '8', 'mlpr', 'ro', 'who', 'srv', 'electrach', 'ing', 'got', 'crypt', 'lap', 'smo',
'hg', 'sad', 'fi', 'nvr', 'ind', 'ld', 'fem', 'vr', 'arg', 'char', 'pok', 'obr', 'catalog', 'api')

downloads_dir = Path('./downloads_2ch')
