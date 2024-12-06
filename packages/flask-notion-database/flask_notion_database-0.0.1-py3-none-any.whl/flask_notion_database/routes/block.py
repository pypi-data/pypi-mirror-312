from flask import request, jsonify
from notion_database import NotionDatabase


class BlockRoutes:
    def __init__(self):
        pass

    def retrieve(self):
        integrations_token = request.form.get('integrations_token')
        block_id = request.form.get('block_id')
        is_children = request.form.get('is_children', False)
        page_size = request.form.get('page_size', 100)
        start_cursor = request.form.get('start_cursor', None)
        result = NotionDatabase.retrieve_block(integrations_token=integrations_token, block_id=block_id,
                                               is_children=is_children, page_size=page_size, start_cursor=start_cursor)
        return jsonify(result)
