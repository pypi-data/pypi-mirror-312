from flask import request, jsonify
from notion_database import NotionDatabase
from notion_database.const.query import Direction, Timestamp


class PageRoutes:
    def __init__(self):
        self.common_sort = {"direction": Direction.ascending, "timestamp": Timestamp.last_edited_time}

    def search(self):
        integrations_token = request.form.get('integrations_token')
        query = request.form.get('query', "")
        page_size = request.form.get('page_size', 100)
        start_cursor = request.form.get('start_cursor', None)
        # sort = request.form.get('sort')
        sort = self.common_sort

        result = NotionDatabase.search_pages(integrations_token=integrations_token, query=query, sort=sort,
                                             page_size=page_size, start_cursor=start_cursor)
        return jsonify(result)

    def retrieve(self):
        integrations_token = request.form.get('integrations_token')
        page_id = request.form.get('page_id')
        result = NotionDatabase.retrieve_page(integrations_token=integrations_token, page_id=page_id)
        return jsonify(result)
