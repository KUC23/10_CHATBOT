1. 로그인 요청 (POST)
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
  "access": "eyJhbGciOiJIUzUxMiIsInR...",
  "redirect_url": "/"
}
```
- response(실패, 401 unauthorized)
```json
{"detail":"비밀번호 또는 사용자 이름이 잘못되었습니다."}
```

2. 회원가입 요청 (POST)
endpoint: api/v1/accounts/signup/
- request body
```json
#필수요구: username, phone_number, password, password2
{
  "username": "newuser",
  "phone_number": "01012345678",
  "password": "password123", #8글자 이상
  "password2": "password123", #비밀번호 확인
}
```
- response(200 Ok): 회원가입 후 로그인상태 유지
```json
{
    "message": "회원가입이 완료되었습니다.",
    "redirect_url": "/preferences/",
    "token": {
        "refresh": "eyJhbGc...",
        "access": "eyJhbGc..."
    }
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

3. 로그아웃 요청 (POST)
endpoint: api/v1/accounts/logout/
- headers
```json
{
    "Authorization": "Bearer <token>"
}
```
- request body
```json
{
  "refresh": "eyJhbGciOiJIUzUxMiIsInR..."
}
```
- response(성공, 200 Ok)
```json
{
    "message": "성공적으로 로그아웃되었습니다.",
    "redirect_url": "/login/"
}
```


4. 회원탈퇴 요청 (DELETE)
endpoint: api/v1/accounts/delete/
- headers
```json
{
    "Authorization": "Bearer <token>"
}
```
- request body
```json
{
    "password": "password123"
}
```
- response(성공, 200 ok)
```json
{
    "message": "회원탈퇴가 완료되었습니다.", 
    "redirect_url": "/"
}
```

```

- response(실패, 400 bad request) 비밀번호 불일치
```json
{
    "password": [
        "비밀번호가 올바르지 않습니다."
    ]
}
```
5-1. 회원정보조회 (GET)
endpoint: api/v1/accounts/<str:username>/
- headers
```json
{
    "Authorization": "Bearer <token>"
}
```
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
    "username": "user",
    "is_staff": false,
    "date_joined": "2025-01-03T04:28:37.667999Z",
    "first_name": "u",
    "last_name": "ser",
    "nickname": "사람",
    "birthday": "2000-01-01",
    "gender": null,
    "introduction": null,
    "email": "user@human.com",
    "phone_number": "01012345673",
    "is_active": true,
    "is_social_connected": "True",
    "connected_social_providers": ['kakao'],
    "defalut_social_providers": "kakao" # or discord
}
```
- response(실패, 403 Forbidden) 타인의 정보 조회불가
```json
{
    "error": "권한이 없습니다."
}
```

5-2. 회원정보수정 (PUT/PATCH)
endpoint: api/v1/accounts/update/
- headers
```json
{
    "Authorization": "Bearer <token>"
}
```
- request body
```json
{
    "id": 1,
    "categories": [
        4
    ],
    "username": "user",
    "first_name": null,
    "last_name": null,
    "nickname": null,
    "birthday": null,
    "email": null,
    "phone_number": "01011111111",
    "is_social_connected": "True",
    "connected_social_providers": ['kakao'],
    "default_social_provider": "kakao"
}
```
- response(200 Ok): 
```json
{
    "message": "수정 완료", 
    "redirect_url": "/profile/username/"
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

6. 비밀번호변경 (PUT)
endpoint: api/v1/accounts/password/change/
- headers
```json
{
    "Authorization": "Bearer <token>"
}
```
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
    "message": "비밀번호가 변경되었습니다.",
    "redirect_url": "/login/"
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


7. 소셜로그인 중복확인: 소셜계정으로 로그인 시도 시 소셜계정의 이메일/전화번호가 기존에 가입된 유저의 이메일/전화번호와 같은지 확인 (POST)
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
    "message": "새 계정을 생성할 수 있습니다.",
    "redirect_url": "/preferences/"
}
```
- response(성공, 200ok) 중복되는 이메일/전화번호가 있음(여전히200ok) ->사용자가 계정을 연동할지 새로운 계정을 생성할지 선택
```json
{
    "status": "exists",
    "message": "중복된 계정이 존재합니다.",
    "options": {
        "link_account": true,
        "create_new_account": true
    },
    "redirect_url": "/social-link-or-create/"
}
```
- response(성공, 200ok) 이미 연동된 계정
```json
{
    "status": "exists",
    "message": "이미 카카오/디스코드 계정이 연동된 상태입니다.",
    "redirect_url": "/preferences/"
}
```
- response(실패, 400 Bad request)
```json
{
    "status": "error",
    "message": "이메일 또는 휴대폰 번호를 입력해야 합니다.",
    "redirect_url": null
}
```

8. 소셜로그인 중복계정 처리: link=연동/create_new=새  계정 생성 (POST)
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
    "message": "기존 계정에 소셜 계정이 연동되었습니다.",
    "redirect_url": "/"
}
```
- response(성공, 200 ok) decision=='create_new'
```json
{
    "status": "success",
    "message": "새 계정이 생성되었습니다.",
    "redirect_url": "/preferences/"
}
```

- response(실패, 400 bad request) 정보입력 오류
```json
{
    "status": "error",
    "message": "잘못된 요청입니다.",
    "redirect_url": null
}
```
- response(실패, 400 bad request) 이미 연동된 계정
```json
{
    "status": "error",
    "message": "이미 연결된 소셜 계정입니다.",
    "redirect_url": null
}
```
- response(실패, 400 bad request) 계정 없음 
```json
{
    "status": "error",
    "message": "연동할 계정을 찾을 수 없습니다.",
    "redirect_url": null
}
```
- response(실패, 400 bad request) 정보 입력 오류
```json
{
    "status": "error",
    "message": "계정 생성 중 문제가 발생했습니다. 입력 정보를 확인해주세요.",
    "redirect_url": null
}
```


9. 소셜 회원가입 : **포스트맨에서 확인 불가** (POST)
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
            "email": "test@example.com"
        }
    }
}

현재 redirect 설정
- 첫 회원가입 시: preferences로 이동("redirect_url": "/preferences/")
- 이후 로그인 시: 메인화면으로 이동("redirect_url": "/")

```

10. 카카오/디스코드 계정 연동 (POST)
endpoint: api/v1/socials/link-social-account/
- headers
```json
{
    "Authorization": "Bearer <token>"
}
```
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
    "message": "discord 계정이 성공적으로 연결되었습니다.",
    "redirect_url": "/profile/username/"
}
```
- response(성공, 200 Ok)
```json
{
    "message": "이미 kakao/discord 계정이 연동되어 있습니다.",
    "redirect_url": "/profile/username/"
}
```


11. 연동한 카카오/디스코드 계정 확인 (GET)
endpoint: api/v1/socials/linked-social-accounts/
- headers
```json
{
    "Authorization": "Bearer <token>"
}
```
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

12. 정보를 받을 소셜계정 선택 (POST)
endpoint: api/v1/socials/default-social-accounts/
- headers
```json
{
    "Authorization": "Bearer <token>"
}
```
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
    "message": "discord 계정이 기본 소셜 계정으로 설정되었습니다.",
    "redirect_url": "/profile/username/"
}
```
- response(실패, 400 Bad reqeust)
```json
{
    "status": "error",
    "message": "discord 계정이 연결되지 않았습니다. 먼저 연동하세요.",
    "redirect_url": "/link-social-account/"
}
```
13. 카테고리 조회 (GET)
endpoints: api/v1/accounts/category/
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

14. 리프레쉬토큰 발급(POST)
endpoint: api/v1/accounts/token/refresh/
- request body
```json
{
    "refresh" : "eyJhbGc..."
    }
```

- response(성공, 200 Ok)
```json
{
    "access": "eyJhbGc...",
    "refresh": "eyJhbGc..."
}
```

15. preferences(POST) or dashboard
endpoint: api/v1/accounts/preferences/
- headers
```json
{
    "Authorization": "Bearer <token>"
}
```
- request body
```json
{
    "messenger_platform": "kakao", # or discord
    "categories": [category pk]
}
```
- response(성공, 200 Ok)
```json
{
    "message": "설정이 저장되었습니다.",
    "redirect_url": "/profile/username/"
}
```
- response(실패, 400 Bad reqeust)
```json
{
    "error": "유효하지 않은 카테고리 ID입니다.",
    "redirect_url": null
}
```


16. 관심사에 맞는 데이터를 DB에서 찾아서 전달(POST)
endpoints: api/v1/chatbots/news/

- headers
```json
{
    "Authorization": "Bearer <token>"
}
```
- request body
없음
- response(성공, 200 Ok)
```json
    "Technology": {
        "title": "title",
        "abstract": "abstract",
        "summary": {
            "english": "english summary",
            "korean": "한글 요약\n"
        },
        "vocab": {
            "단어1:": "뜻1",
            "단어2:": "뜻2",
            "단어3": "뜻3"
        },
        "url": "https://url",
        "category": "Technology"
    },
```
- response(성공, 200 Ok) 관심사가 여러 개일 경우 모두 반환
```json
{
    "articles": {
        "Technology": {
            "title": "title",
            "abstract": "abstract",
            "summary": {
                "english": "english summary",
                "korean": "한글 요약\n"
            },
            "vocab": {
                "단어1:": "뜻1",
                "단어2:": "뜻2",
                "단어3": "뜻3"
            },
            "url": "https://url",
            "category": "Technology"
        },
        "Science": {
            "title": "title",
            "abstract": "abstract",
            "summary": {
                "english": "english summary",
                "korean": "한글 요약\n"
            },
            "vocab": {
                "단어1:": "뜻1",
                "단어2:": "뜻2",
                "단어3": "뜻3"
            },
            "url": "https://url",
            "category": "Science"
        }
    }
}
```

- response(실패, 400 Bad request) 관심사 설정 안 됨
```json
{"error": "No categories set for this user"}
```
