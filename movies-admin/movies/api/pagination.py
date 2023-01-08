from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):

    def get_paginated_response(self, data):
        prevoius_page = (
            self.page.previous_page_number()
            if self.page.has_previous() else None
        )
        next_page = (
            self.page.next_page_number()
            if self.page.has_next() else None
        )
        print(prevoius_page)
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'prev': prevoius_page,
            'next': next_page,
            'results': data
        })
