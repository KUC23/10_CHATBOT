// 소셜 로그인 버튼
// 소셜 로그인 버튼을 클릭하면 해당 소셜 로그인 페이지로 리다이렉트되는 컴포넌트입니다.

// src/components/SocialLoginButton.js


import React from "react";
import { useNavigate } from "react-router-dom";
import { getSocialLoginUrl } from "../api/accounts";

const SocialLoginButton = ({ provider }) => {
    const navigate = useNavigate();

    const handleSocialLogin = async () => {
        const isLoggedIn = localStorage.getItem('access');
        if (!isLoggedIn) {
            alert('로그인이 필요합니다');
            navigate('/login');
            return;
        }

        try {
            const authUrl = await getSocialLoginUrl(provider);
            if (authUrl) window.location.href = authUrl;
        } catch (error) {
            console.error("소셜 로그인 실패:", error);
            alert("소셜 로그인 연동에 실패했습니다.");
        }
    };

    return <button onClick={handleSocialLogin}>{provider} Login</button>;
};

export default SocialLoginButton;





const SocialLinkButton = ({ provider }) => {
    const handleLink = async () => {
        try {
            const authUrl = await getSocialLoginUrl(provider);
            window.location.href = authUrl;
        } catch (error) {
            alert("소셜 계정 연동 실패");
        }
    };

    return <button onClick={handleLink}>Connect with {provider}</button>;
};

export { SocialLoginButton, SocialLinkButton };