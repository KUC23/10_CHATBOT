// 소셜 로그인 버튼
// 소셜 로그인 버튼을 클릭하면 해당 소셜 로그인 페이지로 리다이렉트되는 컴포넌트입니다.

// src/components/SocialLoginButton.js

import React from "react";

// 소셜 로그인 버튼 컴포넌트
const SocialLoginButton = ({ provider }) => {
    const handleSocialLogin = () => {
        // 소셜 로그인 처리 URL로 리다이렉트
        window.location.href = `/api/v1/socials/link-social-account/?provider=${provider}`;
    };

    return <button onClick={handleSocialLogin}>{provider} Login</button>;  // 버튼 클릭 시 소셜 로그인 호출
};

export default SocialLoginButton;
