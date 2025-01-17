// 회원 정보 수정 페이지
// 회원 정보를 수정할 수 있는 폼을 만들고, 수정된 정보를 서버에 보낼 수 있도록 합니다.

// src/components/EditUserInfoPage.js

import React, { useState, useEffect } from "react";
import { useFormik } from "formik";  // 폼 관리 라이브러리
import * as Yup from "yup";  // 유효성 검사 라이브러리
import { getUserInfo, updateUserInfo } from "../api/accounts";
import { useNavigate } from "react-router-dom";  // 페이지 이동을 위한 훅





const EditUserInfoPage = () => {
    const [userInfo, setUserInfo] = useState(null);  // 사용자 정보 상태
    const navigate = useNavigate();  // 페이지 이동을 위한 navigate 훅

    const [categoryNames, setCategoryNames] = useState({
        1: "main",
        2: "technology",
        3: "business",
        4: "science",
        5: "health",
        6: "politics",
        7: "art",
        8: "sport"
    });
    // 페이지 로드 시 기존 사용자 정보 가져오기

    useEffect(() => {
        const fetchUserInfo = async () => {
            try {
                const username = localStorage.getItem('username');
                if (!username) {
                    navigate('/');
                    return;
                }
                const data = await getUserInfo(username);
                setUserInfo(data); 
                console.log('받아온 사용자 정보:', data);
            } catch (error) {
                console.error("유저정보를 수정할 수 없습니다.", error);
                if (error.response?.status === 401) {
                    navigate('/');
            }
        }
    };
    fetchUserInfo();
}, [navigate]);

    // Formik을 사용한 폼 상태 및 유효성 관리
    const formik = useFormik({
        initialValues: {
            username: userInfo ? userInfo.username : "",
            phone_number: userInfo ? userInfo.phone_number : "",
            categories: userInfo ? userInfo.categories : "",
            default_social_provider : userInfo ? userInfo.default_social_provider  : "",
        },
        enableReinitialize: true,  // 처음에 가져온 정보로 초기화
        validationSchema: Yup.object({
            username: Yup.string().required("Username is required"),
            phone_number: Yup.string().required("Phone number is required"),
            categories: Yup.string().required("Select a category"),
            default_social_provider: Yup.string().required("Select a platform"),
        }),
        onSubmit: async (values) => {
            try {
                // 수정할 데이터 준비
                const updateData = {
                    username: values.username,
                    phone_number: values.phone_number,
                    categories: [parseInt(values.categories, 10)],  // 카테고리를 배열로 변환
                    default_social_provider: values.default_social_provider
                };
    
                console.log('수정 요청 데이터:', updateData);  // 전송할 데이터 확인
    
                // 사용자 정보 수정 API 호출
                await updateUserInfo(updateData);
                
                // 성공 메시지 표시
                alert("사용자 정보가 성공적으로 수정되었습니다.");
                
                // 사용자 정보 페이지로 리다이렉트
                navigate('/user-info');
                
            } catch (error) {
                // 에러 처리
                console.error("사용자 정보 수정 실패:", error);
                const errorMessage = error.response?.data?.message || "사용자 정보 수정에 실패했습니다.";
                alert(errorMessage);
            }
        },
    });



    if (!userInfo) {
        return <p>Loading...</p>;  // 사용자 정보 로딩 중
    }

    return (
        <form onSubmit={formik.handleSubmit}>
            <input
                name="username"
                placeholder="Username"
                value={formik.values.username}
                onChange={formik.handleChange}
                disabled  // input을 비활성화
                className="disabled-input"  // 스타일링을 위한 클래스 추가
            />
            <input
                name="phone_number"
                placeholder="Phone Number"
                value={formik.values.phone_number}
                onChange={formik.handleChange}
            />
            <select
                name="categories"
                value={formik.values.categories}
                onChange={formik.handleChange}
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
                value={formik.values.default_social_provider}
                onChange={formik.handleChange}
            >
                <option value="">Select Platform</option>
                <option value="kakao">Kakao</option>
                <option value="discord">Discord</option>
            </select>
            <button type="submit">Save Changes</button>
        </form>
    );
};

export default EditUserInfoPage;
























