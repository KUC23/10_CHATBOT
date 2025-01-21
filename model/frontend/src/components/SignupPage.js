// 회원가입 페이지
// 회원가입 폼과 유효성 검사, API 호출을 담당하는 컴포넌트입니다.

// src/components/SignupPage.js

import React, { useState, useEffect } from 'react';  // [변경] useState, useEffect 추
import { useFormik } from "formik";  // 폼 관리
import * as Yup from "yup";  // 유효성 검사
import { signup, getCategories } from "../api/accounts";  // 회원가입 API 호출 함수
import { useNavigate } from 'react-router-dom';

const SignupPage = () => {
    const navigate = useNavigate();  // useNavigate 훅 사용
    const [categories, setCategories] = useState([]);
    // Formik을 사용한 폼 상태 관리
    const formik = useFormik({
        initialValues: {
            username: "",
            password: "",
            password2: "",
            phone_number: "",
            categories: "",
            default_social_provider: "",
        },
        validationSchema: Yup.object({
            username: Yup.string().required("Username is required"),
            password: Yup.string().required("Password is required"),
            password2: Yup.string()
                .oneOf([Yup.ref("password")], "Passwords must match")
                .required("Confirm Password is required"),
            phone_number: Yup.string().required("Phone number is required"),
            categories: Yup.string().required("Select a category"),
            default_social_provider: Yup.string().required("Select a platform"),
        }),
        onSubmit: async (values) => {
            console.log('폼 제출 시작:', values); // 회원가입 실패시 문제파악을 위한 로그 제출 코드
            // 폼 데이터의 유효성 검사 상태 확인
            console.log('폼 에러:', formik.errors);  // formik의 유효성 검사가 제출을 막고 있는지 확인
            console.log('폼 터치 상태:', formik.touched);  // formik의 유효성 검사가 제출을 막고 있는지 확인
            try {
                console.log('API 호출 시도'); // 회원가입 실패시 문제파악을 위한 로그 제출 코드
                // 회원가입 API 호출
                const response = await signup(values);
                console.log('API 호출 성공:', response); // 회원가입 실패시 문제파악을 위한 로그 제출 코드
                alert("회원가입이 성공적으로 완료되었습니다!");

                // 회원가입 성공 후 UserInfoPage로 리다이렉트
                navigate('/user-info');  // 리다이렉트 코드

                // 성공 시 리다이렉트 또는 다른 처리
                // 회원가입 완료 후 사용자 정보 페이지로 이동
            } catch (error) {
                // 에러 메시지를 좀 더 사용자 친화적으로 표시
                const errorMessage = error.message
                    .split('\n')
                    .filter(msg => msg.trim())
                    .join('\n');
                alert(errorMessage);
            }
        },
    });



    return (
        <form onSubmit={formik.handleSubmit}>
            <input
                name="username"
                placeholder="Username"
                onChange={formik.handleChange}
                value={formik.values.username}
            />
            <input
                name="password"
                type="password"
                placeholder="Password"
                onChange={formik.handleChange}
                value={formik.values.password}
            />
            <input
                name="password2"
                type="password"
                placeholder="Confirm Password"
                onChange={formik.handleChange}
                value={formik.values.password2}
            />
            <input
                name="phone_number"
                placeholder="Phone Number"
                onChange={formik.handleChange}
                value={formik.values.phone_number}
            />
            <select
                name="categories"
                onChange={formik.handleChange}
                value={formik.values.categories}
            >
                <option value="">Select Interest</option>
                <option value="1">main</option>
                <option value="2">technology</option>
                <option value="3">business</option>
                <option value="4">science</option>
                <option value="5">health</option>
                <option value="6">politics</option>
                <option value="7">art</option>
                <option value="8">sport</option>
            </select>
            <select
                name="default_social_provider"
                onChange={formik.handleChange}
                value={formik.values.default_social_provider}
            >
                <option value="">Select Platform</option>
                <option value="kakao">Kakao</option>
                {/* <option value="discord">Discord</option> */}
            </select>
            <button type="submit">Sign Up</button>
        </form>
    );
};

export default SignupPage;
