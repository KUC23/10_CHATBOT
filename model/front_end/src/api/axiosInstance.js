// Axios 인스턴스 및 인터셉터 설정
// 우리는 인증이 필요한 API 요청을 보낼 때마다 access token을 자동으로 추가하기 위해 
// axios 인스턴스를 설정하고, 인터셉터를 사용하여 토큰을 자동으로 헤더에 추가하도록 합니다.

// src/api/axiosInstance.js

import axios from "axios";

// axios 인스턴스 생성
const axiosInstance = axios.create({
    baseURL: "http://yourapi.com",  // 기본 URL 설정
});

// 요청 인터셉터: 로그인 후 access token을 요청 헤더에 자동 추가
axiosInstance.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access");  // localStorage에서 access token 가져오기
        if (token) {
            config.headers["Authorization"] = `Bearer ${token}`;  // 헤더에 토큰 추가
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);  // 요청 실패 시 처리
    }
);

export default axiosInstance;
