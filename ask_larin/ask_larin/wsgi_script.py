def application(environ, start_response):
    get_params = environ.get('QUERY_STRING', '')
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)
    post_params = request_body.decode('utf-8')

    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)

    response = [
        f"GET: {get_params}\nPOST: {post_params}\n".encode('utf-8'),
    ]
    return response