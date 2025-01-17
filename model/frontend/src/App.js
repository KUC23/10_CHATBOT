// 라우팅 추가
// 회원 정보 페이지와 수정 페이지를 라우팅합니다.


// src/App.js

import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./components/LoginPage";
import SignupPage from "./components/SignupPage";
import UserInfoPage from "./components/UserInfoPage";
import EditUserInfoPage from "./components/EditUserInfoPage";
import ChangePasswordPage from "./components/ChangePasswordPage";  // 패스워드 변경 페이지

function App() {
    return (
        <Router>
            <Routes>
                <Route path="" element={<LoginPage />} />
                <Route path="/signup" element={<SignupPage />} />
                <Route path="/user-info" element={<UserInfoPage />} />
                <Route path="/edit-user-info" element={<EditUserInfoPage />} />
                <Route path="/change-password" element={<ChangePasswordPage />} />  {/* 패스워드 변경 페이지 */}
            </Routes>
        </Router>
    );
}

export default App;
