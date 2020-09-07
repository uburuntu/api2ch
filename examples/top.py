from api2ch import Api2ch

api = Api2ch()

boards = api.boards_by_types()
for board in boards.Art:
    threads = api.threads(board.id)
    top_thread = threads.sorted_by_views()[0]
    print(f'— /{threads.request.board} | {board.name} | Top thread: {top_thread.subject}, {top_thread.views} 👁‍🗨')
