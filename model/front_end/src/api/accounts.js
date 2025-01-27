
// src/api/accounts.js

import axios from "axios";

const apiClient = axios.create({
    baseURL: "http://15.164.255.1:8000", // Django 서버 기본 URL
    headers: {
        'Content-Type': 'application/json',
    }
});


// Request Interceptor 추가
apiClient.interceptors.request.use(
    (config) => {
        // 회원가입과 로그인 요청에는 토큰을 추가하지 않음
        if (config.url.includes('/signup/') || config.url.includes('/login/')) {
            return config;
        }
        
        const token = localStorage.getItem('access');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);


export const getUserInfo = async (username) => {
    try {
        // 토큰 존재 여부 확인
        const token = localStorage.getItem('access');
        if (!token) {
            throw new Error('로그인이 필요합니다.');
        }
        console.log('Access Token:', token);  // 토큰 존재 여부 확인
        
        // API 요청 전 로그
        console.log('Requesting user info for:', username);
                
        const response = await apiClient.get(`/api/v1/accounts/profile/${username}/`,{
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        console.log('User info response:', response.data);  // 응답 데이터 확인
        
        return response.data;
    } catch (error) {
        console.error("사용자 정보 조회 실패", {
            status: error.response?.status,
            data: error.response?.data,
            headers: error.response?.headers

        });

        // 토큰 관련 에러 처리
        if (error.response?.status === 401) {
            localStorage.removeItem('access');  // 유효하지 않은 토큰 제거
            throw new Error('인증이 만료되었습니다. 다시 로그인해주세요.');
        }
        throw error;
    }
};

// 로그인 API 요청
export const login = async (username, password) => {
    try {
        const response = await apiClient.post("/api/v1/accounts/login/", {
            username,
            password,
        }, {
            headers: {
                'Content-Type': 'application/json',
            }
        });

        // 응답 확인을 위한 로그
        console.log('로그인 응답:', response.data);

        // 로그인 성공 시 토큰 확인
        if (response.data.access && response.data.refresh) {
            localStorage.setItem('access', response.data.access);
            localStorage.setItem('refresh', response.data.refresh);
            localStorage.setItem('username', username);  // username도 저장
        }

            return response.data;

    } catch (error) {
        // 자세한 에러 정보 로깅
        console.error("로그인 실패 상세 정보:", {
            status: error.response?.status,
            data: error.response?.data,
            message: error.message
        });
        throw error;  // 로그인 실패 시 에러 발생
    }
};


// 로그아웃기능 
export const logout = () => {
    // 로컬 스토리지에서 모든 인증 정보 삭제
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    localStorage.removeItem('username');
};



// 회원가입 API 요청
export const signup = async (formData) => {
    try {
        // 서버에 맞는 데이터 형식으로 변환
        const signupData = {
            username: formData.username,  // username 필드 추가
            password: formData.password,  // password1 필드 추가
            password2: formData.password2,  // password2 필드 추가
            phone_number: formData.phone_number, // phone_number 필드 추가
            // categories: [parseInt(formData.categories, 10)],  //  숫자로 변환하고 배열로 감싸기, 백엔드에서 데이터삭제?처리되서 받아지지 않음 삭제처리
            default_social_provider: formData.default_social_provider
        };

       // 디버깅을 위해 서버로 전송되는 데이터를 콘솔에 출력
        console.log('서버로 전송하는 데이터:', signupData);


       // apiClient를 사용하여 서버에 POST 요청 전송
       // '/api/v1/accounts/signup/' 엔드포인트로 가공된 데이터 전송
        const response = await apiClient.post("/api/v1/accounts/signup/", signupData);


        // 회원가입 성공 후 바로 로그인 시도
        const loginResponse = await login(formData.username, formData.password);

        // 로그인 성공 시 토큰과 username 저장
        localStorage.setItem('access', loginResponse.access);
        localStorage.setItem('refresh', loginResponse.refresh);
        localStorage.setItem('username', formData.username);


        // 디버깅을 위해 서버로부터 받은 응답을 콘솔에 출력
        console.log('서버 응답:', response.data);
        
        //  회원가입 성공 시 받은 데이터 반환
        return response.data;  // 회원가입 성공 시 받은 데이터 반환


    } catch (error) {
        // 에러 발생 시 상세 정보를 콘솔에 출력하여 디버깅 용이하게 함
       // status: HTTP 상태 코드
       // data: 서버에서 전송한 에러 데이터
       // message: 에러 메시지
        console.error("회원가입 실패 상세 정보:", {
            status: error.response?.status,
            data: error.response?.data,
            headers: error.response?.headers,
            message: error.message,
            fullError: error.response
        }
        ,"서버 에러 응답 데이터:", JSON.stringify(error.response?.data, null, 2
        )
    );

        // 에러 메시지를 좀 더 구체적으로 처리
        // 서버에서 반환한 에러 데이터가 있는 경우 처리
        if (error.response?.data) {
            const errorMessages = Object.entries(error.response.data)
                .map(([key, value]) => {
                    // 각 필드별 구체적인 에러 메시지 처리
                    if (key === 'phone_number' && value.includes('already exists')) {
                        return '이미 등록된 전화번호입니다. 다른 번호를 사용해주세요.';
                    } else if (key === 'categories') {
                        return '카테고리 형식이 올바르지 않습니다.';
                    } else if (key === 'username') {
                        return '사용자명이 이미 존재하거나 올바르지 않습니다.';
                    } else if (key === 'password') {
                        return '비밀번호 형식이 올바르지 않습니다.';
                    } else if (key === 'password2') {  // [추가] password2 에러 처리
                        return '비밀번호 확인을 입력해주세요.';
                    }
                    return `${key}: ${value}`;
                })
                .join('\n');
            
            throw new Error(errorMessages);
        }
        // 서버 응답이 없는 경우의 에러 처리        
        throw new Error('서버와의 통신 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
    }
};



// 사용자 정보 수정 함수 추가
export const updateUserInfo = async (values) => {
    try {
        const response = await apiClient.put("/api/v1/accounts/update/", values);
        console.log('사용자 정보 수정 응답:', response.data);  // 응답 확인을 위한 로그
        return response.data;
    } catch (error) {
        console.error("사용자 정보 수정 실패:", {
            status: error.response?.status,
            data: error.response?.data,
            message: error.message,
            fullError: error.response  // 전체 에러 정보 확인
        });
        throw error;
    }
};



// 비밀번호 변경 함수 추가
export const changePassword = async (passwordData) => {
    try {
        // 토큰 확인
        const token = localStorage.getItem('access');
        if (!token) {
            throw new Error('로그인이 필요합니다.');
        }

        const response = await apiClient.put("/api/v1/accounts/password/change/", passwordData, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        console.log('비밀번호 변경 응답:', response.data);
        return response.data;
    } catch (error) {
        console.error("비밀번호 변경 실패:", {
            status: error.response?.status,
            data: error.response?.data,
            message: error.message
        });
        
        // 401 에러 처리
        if (error.response?.status === 401) {
            throw new Error('인증이 만료되었습니다. 다시 로그인해주세요.');
        }
        
        throw error;
    }
};

// 소셜 로그인 함수 추가:
export const getSocialLoginUrl = async (provider) => {
    try {
        const response = await apiClient.post('/api/v1/socials/social-link-or-create/', {
            provider: provider,
            // 필요한 데이터 추가
        });
        return response.data.auth_url;
    } catch (error) {
        console.error("소셜 로그인 URL 획득 실패:", error);
        throw error;
    }
};



export const sendChatbotInvite = async (username) => {
    try {
        const response = await apiClient.post('/api/v1/socials/send-invite/', {
            username: username
        });
        return response.data;
    } catch (error) {
        console.error("챗봇 초대 전송 실패:", error);
        throw error;
    }
};









