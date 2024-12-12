import requests
import pytest 
import os
def pytest_namespace():
    return {"james_token": None, "lars_token": None, "james_uid": None, "lars_uid": None}


@pytest.fixture
def james_token():
    assert pytest.james_token
    return pytest.james_token

@pytest.fixture
def lars_token():
    assert pytest.lars_token
    return pytest.lars_token

@pytest.fixture
def james_uid():
    assert pytest.james_uid
    return pytest.james_uid

@pytest.fixture 
def lars_uid():
    assert pytest.lars_uid
    return pytest.lars_uid

class TestLogin:

    def setup_class(self) -> None:
        self.base_url = "http://44.202.3.35:6000"

    def _send_request(self, request: requests.Request, authorization = None):
       s = requests.session()
       if authorization:
           auth_header = {"Authorization": "Bearer " + authorization}
           request.headers.update(auth_header)
        
       return s.send(request.prepare())
    
    def login(self, user_name, password):
        return self._send_request(requests.Request(url=self.base_url + "/login", 
                                                   json={"userName": user_name, 
                                                         "password": password}, 
                                                   method="POST")) 
    
    
    def get_accont(self, authorization):
        return self._send_request(requests.Request(url=self.base_url + "/account", method="GET"), authorization=authorization)
    
    def get_transactions(self, authorization, uid, limit):
        return self._send_request(requests.Request(url=self.base_url + "/transactions", 
                                                   params={"limit": limit, "userId": uid}, 
                                                   method="GET"), 
                                  authorization=authorization)


    def test_james_can_login(self):
        resp = self.login("James", "ILoveGuitars")
        assert resp.status_code == 200
        pytest.james_token = resp.json()["token"]
    

    def test_get_james_user_info(self, james_token):
        resp = self.get_accont(james_token)
        assert resp.status_code == 200 
        pytest.james_uid = resp.json()["userId"]

    def test_get_james_user_info_from_graphql(self, james_token, james_uid):
        query = """query {
            me {
                userId
            }
        }"""
        resp = self._send_request(requests.Request(
            url=self.base_url + "/graphql",
            method="POST",
            json={"query": query}
        ), authorization=james_token)

        assert resp.status_code == 200
        james_info = resp.json()["data"]["me"]
        assert james_info["userId"] == james_uid


    def test_get_james_transactions(self, james_token, james_uid):
        resp = self.get_transactions(james_token, james_uid, limit=5)
        assert resp.status_code == 200 
        assert len(resp.json()) == 5 
        resp = self.get_transactions(james_token, james_uid, limit=10)
        assert resp.status_code == 200 
        assert len(resp.json()) == 10 
    
    def test_lars_can_login(self):
        resp = self.login("Lars", "ILoveDrums")
        assert resp.status_code == 200
        pytest.lars_token = resp.json()["token"]

    
    def test_get_lars_user_info(self, lars_token):
        resp = self.get_accont(lars_token)
        assert resp.status_code == 200
        pytest.lars_uid = resp.json()["userId"]


    def test_get_lars_transactions(self, lars_token, lars_uid):
        resp = self.get_transactions(lars_token, lars_uid, limit=5)
        assert resp.status_code == 200
