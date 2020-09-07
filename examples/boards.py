from api2ch import Api2ch

api = Api2ch()

for board in ('tv', 'hw', 'fiz'):
    c = api.catalog(board)
    print(f'/{c.board} | {c.board_name}, "{c.board_info_outer}", bump limit: {c.bump_limit}')
