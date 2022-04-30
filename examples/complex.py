import api2ch

api = api2ch.Api2ch()


def parse_post(url: str) -> str:
    valid, board, thread_id = api2ch.parse_url(url)
    if not valid:
        raise api2ch.Api2chError(404, 'Invalid URL')

    thread = api.thread(board, thread_id)
    post = thread.posts[0]
    text = ''

    text += f'{post.dt().isoformat()} | Пост №{post.post_id}: {post.url(thread.board)}:\n\n'
    text += f'{post.header}\n' if thread.enable_subject else ''
    text += f'{post.body_text}\n\n'

    if post.files:
        text += 'Файлы:\n'
        for f in post.files:
            text += f'— {f.original_name}, {f.size_string}: {f.url()}\n'

    return text


def pretty_print_post(url: str):
    try:
        text = parse_post(url)
    except api2ch.Api2chError as e:
        print('Request Error', e.code, e.reason)
    else:
        print(text)


if __name__ == '__main__':
    pretty_print_post('https://2ch.hk/cg/res/1323206.html')
