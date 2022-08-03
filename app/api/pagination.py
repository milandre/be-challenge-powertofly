from flask_resty import CursorPaginationBase, meta


class CustomCursorPagination(CursorPaginationBase):
    """CustomCursorPagination

    CursorPaginationBase for each page with
    extra meta information
    """

    def get_page(self, query, view):
        field_orderings = self.get_field_orderings(view)

        cursor_in = self.get_request_cursor(view, field_orderings)

        page_query = query
        if cursor_in is not None:
            page_query = page_query.filter(self.get_filter(view, field_orderings, cursor_in))

        limit = self.get_limit()
        if limit is not None:
            page_query = page_query.limit(limit + 1)

        items = page_query.all()

        has_next_page = False
        if limit is not None and len(items) > limit:
            has_next_page = True
            items = items[:limit]

        if self.reversed:
            items.reverse()

        if has_next_page:
            next_cursor = self.make_cursor(items[-1], view, field_orderings)
            meta.update_response_meta({"next_cursor": next_cursor})

        meta.update_response_meta({"total": len(items), "has_next_page": has_next_page})

        return items
