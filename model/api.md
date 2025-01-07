1. 로그인 요청 
endpoint: api/v1/accounts/login/
- request body
```json
{
  "username": "string",
  "password": "string"
}
```
username란에 핸드폰번호 입력으로도 로그인 가능
```json
{
  "username": "010xxxxxxxx",
  "password": "string"
}
```
- response(성공, 200 ok)
```json
{
  "refresh": "eyJhbGciOiJIUzUxMiIsInR...",
  "access": "eyJhbGciOiJIUzUxMiIsInR..."
}
```
- response(실패, 401 unauthorized)
```json
{"detail":"비밀번호 또는 사용자 이름이 잘못되었습니다."}
```

2. 회원가입 요청
endpoint: api/v1/accounts/signup/
- request body
```json
#필수요구정보
{
  "username": "newuser",
  "phone_number": "01012345678",
  "password": "password123",
  "password2": "password123", #비밀번호 확인
  "categories": [category pk] #관심사
}
```
- response(성공, 201 created)
```json
{
    "id": 12,
    "groups": [],
    "user_permissions": [],
    "categories": [
        1
    ],
    "last_login": null,
    "is_superuser": false,
    "username": "username",
    "is_staff": false,
    "date_joined": "2025-01-05T03:41:25.924654Z",
    "first_name": null,
    "last_name": null,
    "nickname": null,
    "birthday": null,
    "gender": null,
    "introduction": null,
    "email": null,
    "phone_number": "01011111111",
    "is_active": true
}
```

- response(실패, 400 bad reqeust) : 이미 존재하는 유저정보
```json
{
    "username": [
        "A user with that username already exists."
    ],
    "phone_number": [
        "user with this phone number already exists."
    ]
}
```

- response(실패, 400 bad reqeust) : 빈 칸 있음
```json
{
    "phone_number": [
        "This field may not be blank."
    ]
}
```

- response(실패, 400 bad reqeust) : password!=password2
```json
{
    "password": [
        "비밀번호가 일치하지 않습니다."
    ]
}
```

3. 로그아웃 요청
endpoint: api/v1/accounts/logout/

- request body
```json
{
  "refresh": "eyJhbGciOiJIUzUxMiIsInR..."
}
```
- response(성공, 200 Ok)
```json
{
    "message": "성공적으로 로그아웃되었습니다."
}
```
- response(실패, 401 Unauthorized)
```json
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired"
        }
    ]
}
```

4. 회원탈퇴 요청
endpoint: api/v1/accounts/delete/
- request body
```json
{
    "password": "password123"
}
```
- response(성공, 200 ok)
```json
{
    "message": "회원탈퇴가 완료되었습니다."
}
```
- response(실패, 401 Unauthorized) 토큰불일치
```json
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired"
        }
    ]
}
```

- response(실패, 400 bad request) 비밀번호 불일치
```json
{
    "password": [
        "비밀번호가 올바르지 않습니다."
    ]
}
```
5-1. 회원정보조회
endpoint: api/v1/accounts/<str:username>/
- request body
없음

- response(성공, 200 Ok)
```json
{
    "id": 2,
    "groups": [],
    "user_permissions": [],
    "categories": [],
    "last_login": null,
    "is_superuser": false,
    "username": "suho",
    "is_staff": false,
    "date_joined": "2025-01-03T04:28:37.667999Z",
    "first_name": "su",
    "last_name": "ho",
    "nickname": "사람",
    "birthday": "2000-01-01",
    "gender": null,
    "introduction": null,
    "email": "su@human.com",
    "phone_number": "01012345673",
    "is_active": true,
    "is_social_connected": false,
    "connected_social_providers": []
}
```
- response(실패, 404 Not found) 해당하는 유저 없음
```json
{
    "detail": "No User matches the given query."
}
```

- response(실패, 401 Unauthorized)
```json
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired"
        }
    ]
}
```
5-2. 회원정보수정
endpoint: api/v1/accounts/update/
- request body
```json
{
    "email": "em@.com",
    "first_name": "name",
    "last_name": "eman",
    "nickname": "nick",
    "birthday": "2000-01-01",
    "phone_number": "01012345678",
    "categories" : [category pk]
}
```
- response(성공, 200 ok)
```json
{
    "email": "em@.com",
    "first_name": "new_name",
    "last_name": "eman",
    "nickname": "new_nickname",
    "birthday": "2000-01-01",
    "phone_number": "01012345678",
    "categories" : [category pk]
}
```
- response(실패, 401 Unauthorized) 토큰불일치
```json
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired"
        }
    ]
}
```
- response(실패, 400 bad request) 정보입력 오류
```json
{
    "categories": [
        "Expected a list of items but got type \"str\"."
    ]
}
```

6. 비밀번호변경
endpoint: api/v1/accounts/password/change/
- request body
```json
{
    "old_password": "oldpassword123",
    "new_password": "newpassword123",
    "new_password2": "newpassword123"
}
```
- response(성공, 200 Ok)
```json
{
    "message": "비밀번호가 변경되었습니다."
}
```
- response(실패, 400 bad request)기존 비밀번호 불일치
```json
{
    "old_password": [
        "비밀번호가 올바르지 않습니다."
    ]
}
```

- response(실패, 400 bad request)신규 비밀번호 password!=password2
```json
{
    "new_password": [
        "비밀번호가 일치하지 않습니다."
    ]
}
```

- response(실패, 401 Unauthorized) 토큰불일치
```json
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired"
        }
    ]
}
```

7. 소셜로그인 중복확인: 소셜계정으로 로그인 시도 시 소셜계정의 이메일/전화번호가 기존에 가입된 유저의 이메일/전화번호와 같은지 확인
endpoint: api/v1/socials/check-user/
- request body
```json
{
    "email":"new.email.com",
    "phone_number":"01011113222"
}
```
- response(성공, 200 ok) 중복되는 이메일/전화번호가 없음
```json
{
    "status": "not_exists",
    "message": "새 계정을 생성할 수 있습니다."
}
```
- response(성공, 200ok) 중복되는 이메일/전화번호가 있음(여전히200ok) ->사용자가 계정을 연동할지 새로운 계정을 생성할지 선택택
```json
{
    "status": "exists",
    "message": "중복된 계정이 존재합니다.",
    "options": {
        "link_account": true,
        "create_new_account": true
    }
}
```

8. 소셜로그인 중복계정 처리: link=연동/create_new=새  계정 생성
endpoint: api/v1/socials/social-link-or-create/
- request body
```json
{
    "decision": "link", # or create_new
    "email": "em.email.com",
    "phone_number": "01012345678",
    "provider": "discord",
    "social_id": "idid"
}

```
- response(성공, 200 ok) decision=='link'
```json
{
    "status": "success",
    "message": "기존 계정에 소셜 계정이 연동되었습니다."
}
```
- response(성공, 200 ok) decision=='create_new'
```json
{
    "status": "success",
    "message": "새 계정이 생성되었습니다."
}
```

- response(실패, 400 bad request) 정보입력 오류
```json
{
    "status": "error",
    "message": "잘못된 요청입니다."
}
```

9. 소셜 회원가입 : **포스트맨에서 확인 불가**
(사유: Django는 CSRF 보호 메커니즘이 있는데, OAuth2 인증 흐름에서는 CSRF 토큰을 사용 불가 ->CSRF관련 오류 발생) -> **예상되는 API구조임**
- 카카오톡 회원가입 api/v1/socials/kakao/login/
- 디스코드 회원가입 api/v1/socials/discord/login/
- request body
```json
{
    "provider": "kakao",
    "access_token": "access_token"
}
```
- response(성공, 200 ok)
```json
{
    "message": "소셜 로그인이 성공적으로 완료되었습니다.",
    "data": {
        "refresh": "eyJhbGciOiJIUzUxMiIsInR...",
        "access": "eyJhbGciOiJIUzUxMiIsInR...",
        "user": {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "nickname": "nick"
        }
    }
}
```

10. 카카오/디스코드 계정 연동
endpoint: api/v1/socials/link-social-account/
- request body
```json
{
    "provider": "discord", #or 'kakao'
    "social_id": "string"
}
```
- response(성공, 200 Ok)
```json
{
    "message": "discord 계정이 성공적으로 연결되었습니다."
}
```
- response(실패, 400 Bad request) 
```json
{
    "message": "이미 연결된 소셜 계정입니다."
}
```


11. 연동한 카카오/디스코드 계정 확인
endpoint: api/v1/socials/linked-social-accounts/
- request body: 없음

- response(성공, 200 Ok) 연동된 계정 있음
```json
{
    "status": "success",
    "linked_accounts": [
        {
            "provider": "discord", # or "kakao"
            "social_id": "string"
        }
    ]
}
```
- response(성공, 200 Ok) 연동된 계정 없음
```json
{
    "is_social_connected": false,
    "connected_social_providers": []
}
```

12. 정보를 받을 소셜계정 선택
- request body
```json
{
    "provider": "discord" # or 'kakao'
}
```
- response(성공, 200 Ok)
```json
{
    "status": "success",
    "message": "discord 계정이 기본 소셜 계정으로 설정되었습니다."
}
```
- response(실패, 400 Bad reqeust)
```json
{
    "status": "error",
    "message": "연결되지 않은 소셜 계정입니다."
}
```
13. 카테고리 조회
- request body 없음
- response(성공, 200 Ok)
```json
[
    {
        "id": 1,
        "name": "Main"
    },
    {
        "id": 2,
        "name": "Technology"
    },
    {
        "id": 3,
        "name": "Business"
    },
    {
        "id": 4,
        "name": "Science"
    },
    {
        "id": 5,
        "name": "Health"
    },
    {
        "id": 6,
        "name": "Politics"
    },
    {
        "id": 7,
        "name": "Art"
    },
    {
        "id": 8,
        "name": "Sport"
    }
]
```
