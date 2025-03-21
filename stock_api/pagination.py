from rest_framework.pagination import PageNumberPagination
from math import ceil


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 3

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)

        # Calcular el número total de páginas
        count = response.data["count"]
        page_size = self.page_size
        total_pages = ceil(count / page_size)

        # Agregar el número total de páginas a la respuesta
        response.data["total_pages"] = total_pages

        return response
