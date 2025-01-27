// src/components/LoginPage.js


import React from "react";
import { useNavigate } from "react-router-dom";  // 라우터 이동을 위한 hook
import { useFormik } from "formik";      // 폼 상태 관리 라이브러리
import * as Yup from "yup";              // 폼 유효성 검사 라이브러리
import { login } from "../api/accounts";  // 로그인 API 함수
import SocialLoginButton from "./SocialLoginButton";  // 소셜 로그인 버튼 컴포넌트
import "../styles/App.css";             
import "../styles/Auth.css";  // 경로 수정

const LoginPage = () => {
    // useNavigate hook을 사용하여 페이지 이동 함수 생성
    const navigate = useNavigate();

    // Formik을 사용한 폼 상태 관리 설정
    const formik = useFormik({
        // 폼 필드의 초기값 설정
        initialValues: { 
            username: "", 
            password: "" 
        },
       // Yup을 사용한 폼 유효성 검사 스키마 정의
        validationSchema: Yup.object({
            username: Yup.string().required("Username is required"),
            password: Yup.string().required("Password is required"),
        }),

       // 폼 제출 시 실행될 함수
        onSubmit: async (values) => {
            try {

               // login API 호출하여 서버에 인증 요청
                const data = await login(values.username, values.password);
               // 로그인 성공 시 토큰을 localStorage에 저장
                localStorage.setItem("access", data.access);        // access token 저장
                localStorage.setItem("refresh", data.refresh);      // access token 저장
                localStorage.setItem("username", values.username); // username 저장 - UserInfoPage에서 필요

               // 로그인 성공 후 사용자 정보 페이지로 이동
                navigate("/user-info");
            } catch (error) {

               // 로그인 실패 시 alert로 에러 메시지 표시
                alert("Login failed!");
            }
        },
    });

   // 컴포넌트 UI 렌더링
    return (
        <div className="auth-container">
            <img src="/static/logo.png" alt="SmartScoop" className="logo" />
            <div className="auth-card">
                <h2 className="auth-title">Welcome to SmartScoop</h2>

                {/* 로그인 폼 */}
                <form onSubmit={formik.handleSubmit}>

                    {/* 사용자명 입력 필드 */}
                    <input
                        className="input-field"
                        name="username"
                        onChange={formik.handleChange} // 입력값 변경 시 Formik 상태 업데이트
                        value={formik.values.username}  // Formik에서 관리하는 값
                        placeholder="Username"
                    />
                    
                    {/* 비밀번호 입력 필드 */}
                    <input
                        className="input-field"
                        name="password"
                        type="password"
                        onChange={formik.handleChange}
                        value={formik.values.password}
                        placeholder="Password"
                    />

                    {/* 로그인 버튼 */}
                    <button type="submit" className="btn btn-primary">Login</button>

                    {/* 회원가입 페이지 이동 버튼 */}
                    <button 
                        type="button"
                        onClick={() => navigate("/signup")} 
                        className="btn btn-secondary"
                    >
                        Sign Up
                    </button>
                </form>
            </div>
        </div>
    );
};

// LoginPage 컴포넌트 내보내기
export default LoginPage;