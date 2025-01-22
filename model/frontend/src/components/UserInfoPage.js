// 사용자 정보 페이지
// 회원 정보를 표시하고, 수정 페이지로 이동하는 버튼과 패스워드 변경 버튼을 포함합니다.

// src/components/UserInfoPage.js

import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getUserInfo, logout } from "../api/accounts";

const UserInfoPage = () => {
    const [userInfo, setUserInfo] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();
    // 회원정보다 id 로 반환되는 것을 확인
    // 카테고리 이름을 저장할 상태 추가
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

    useEffect(() => {
        const fetchUserInfo = async () => {
            try {
                setLoading(true);
                // localStorage에서 현재 로그인한 사용자의 username 가져오기
                const username = localStorage.getItem('username');  // 로그인 시 저장했다고 가정
                
                if (!username) {
                    throw new Error('로그인이 필요합니다.');
                }

                const data = await getUserInfo(username);
                console.log("받아온 사용자 정보:", data);  // 데이터 구조 확인
                // messenger_platform 필드 specifically 확인
                console.log("메신저 플랫폼 필드:", data.default_social_provider);  // 구체적인 필드 확인
                setUserInfo(data);

            } catch (error) {
                console.error("상세 에러 정보:", error.response?.data);
                setError("사용자 정보를 불러오는데 실패했습니다.");
                if (error.response?.status === 401 || !localStorage.getItem('username')) {
                    navigate('');
                }
            } finally {
                setLoading(false);
            }
        };

        fetchUserInfo();
    }, [navigate]);

    const handleChangePassword = () => {
        navigate("/change-password");
    };


    // 정보 수정 페이지로 이동하는 함수 추가
    const handleEditInfo = () => {
        navigate('/edit-user-info');  // 정보 수정 페이지로 이동
    };


    // 카테고리 ID를 이름으로 변환하는 함수
    const getCategoryName = (categoryId) => {
        return categoryNames[categoryId] || '알 수 없는 카테고리';
    };



    if (loading) return <div>로딩 중...</div>;
    if (error) return <div>{error}</div>;
    if (!userInfo) return <div>사용자 정보가 없습니다.</div>;

    // 로그아웃 처리 함수 추가
    const handleLogout = () => {
        logout();  // 로그아웃 함수 호출
        navigate('/');  // 로그인 페이지로 이동
    };

    return (
        <div>
            <h2>사용자 정보</h2>
            <div>
                <p><strong>사용자명:</strong> {userInfo.username}</p>
                <p><strong>전화번호:</strong> {userInfo.phone_number}</p>
                {/* categories와 messenger_platform의 실제 데이터 구조 확인을 위한 로그 추가 */}
                {console.log('카테고리 정보:', userInfo.categories)}
                {console.log('메신저 플랫폼 정보:', userInfo.default_social_provider)}


                <p><strong>관심 카테고리:</strong> {
                    
                    // categories가 배열이고 값이 있는 경우에만 처리
                    Array.isArray(userInfo.categories) && userInfo.categories.length > 0
                        ? userInfo.categories.map(categoryId => getCategoryName(categoryId)).join(', ')
                        : '선택된 카테고리 없음'
                }</p>

                <p><strong>메신저 플랫폼:</strong> {
                    // messenger_platform이 있는 경우에만 표시
                   userInfo.default_social_provider || '선택된 플랫폼 없음'
                }</p>


                <div style={{ marginTop: '20px' }}>  {/* 버튼들을 위한 컨테이너 */}
                    <button 
                        onClick={handleChangePassword}
                        className="change-password-btn"
                    >
                        비밀번호 변경
                    </button>    
                    

                    {/* 정보 수정 버튼 추가 */}
                    <button 
                        onClick={handleEditInfo}
                        style={{ marginLeft: '10px' }}  // 버튼 간격 조정
                    >
                        정보 수정
                    </button>


                    {/* 로그아웃 버튼 추가 */}
                    <button 
                        onClick={handleLogout}
                        style={{ marginLeft: '10px' }}  // 버튼 간격 조정
                    >
                        로그아웃
                    </button>
                </div>
            </div>
        </div>
    );
};

export default UserInfoPage;