class TestUserFlow:
    def setup_class(self):
        self.user_flow = UserFlow()
    
    @pytest.mark.parametrize("user_info", [
        {"name": "user1", "email": "user1@example.com"},
        {"name": "user2", "email": "user2@example.com"}
    ])
    def test_create_multiple_users(self, user_info):
        result = self.user_flow.create_user_flow(
            admin_user="admin",
            admin_pwd="password",
            new_user_info=user_info
        )
        assert result["status"] == "success" 