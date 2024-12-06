class TestUser:
    def setup_class(self):
        self.login_api = LoginApi()
        self.user_api = UserManageApi()
    
    def test_create_user(self):
        # 先登录
        self.login_api.login("admin", "password")
        
        # 创建用户
        user_info = {
            "name": "test_user",
            "email": "test@example.com"
        }
        response = self.user_api.create_user(user_info)
        assert response.status_code == 200 