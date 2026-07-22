from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    """
    Token authentication that accepts both:
    Authorization: Token <key>
    Authorization: Bearer <key>
    """

    keyword = "Bearer"

    def authenticate(self, request):
        result = super().authenticate(request)
        if result is not None:
            return result

        original_keyword = self.keyword
        self.keyword = "Token"
        try:
            return super().authenticate(request)
        finally:
            self.keyword = original_keyword
