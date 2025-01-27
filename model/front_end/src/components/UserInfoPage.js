// UserInfoPage.jsx
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getUserInfo, logout } from "../api/accounts";
import { getSocialLoginUrl } from "../api/accounts";

const UserInfoPage = () => {
  const [userInfo, setUserInfo] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showQRModal, setShowQRModal] = useState(false);
  const navigate = useNavigate();
  const [categoryNames] = useState({
      1: "main", 2: "technology", 3: "business", 
      4: "science", 5: "health", 6: "politics", 
      7: "art", 8: "sport"
  });

  const kakaoPageUrl = 'http://pf.kakao.com/_TxdIxbn';

  useEffect(() => {
      const fetchUserInfo = async () => {
          try {
              setLoading(true);
              const username = localStorage.getItem('username');
              
              if (!username) {
                  throw new Error('로그인이 필요합니다.');
              }

              const data = await getUserInfo(username);
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

  const handleEditInfo = () => {
      navigate('/edit-user-info');
  };

  const handleLogout = () => {
      logout();
      navigate('/');
  };

  const handleKakaoPageNavigation = () => {
      window.open(kakaoPageUrl, '_blank');
  };

  if (loading) return <div>로딩 중...</div>;
  if (error) return <div>{error}</div>;
  if (!userInfo) return <div>사용자 정보가 없습니다.</div>;

  return (
      <div className="common-container">
          <div className="auth-card">
              <h2 className="auth-title">사용자 정보</h2>
              <div className="kakao-button-group">
                  <button 
                      onClick={() => setShowQRModal(true)}
                      className="kakao-qr-button"
                  >
                      (카카오톡 챗봇 추가)PC용 QR 코드
                  </button>
                  <button 
                      onClick={handleKakaoPageNavigation}
                      className="kakao-link-button"
                  >
                      (카카오톡 챗봇 추가)스마트폰용 링크
                  </button>
              </div>
              <div className="user-info-section">
                  <div className="info-card">
                      <div className="info-label">사용자명</div>
                      <div className="info-value">{userInfo.username}</div>
                  </div>
                  <div className="info-card">
                      <div className="info-label">전화번호</div>
                      <div className="info-value">{userInfo.phone_number}</div>
                  </div>
                  <div className="info-card">
                      <div className="info-label">관심 카테고리</div>
                      <div className="info-value">
                          {Array.isArray(userInfo.categories) && userInfo.categories.length > 0
                              ? userInfo.categories.map(categoryId => categoryNames[categoryId] || '알 수 없는 카테고리').join(', ')
                              : '선택된 카테고리 없음'}
                      </div>
                  </div>
                  <div className="info-card">
                      <div className="info-label">메신저 플랫폼</div>
                      <div className="info-value">{userInfo.default_social_provider || '선택된 플랫폼 없음'}</div>
                  </div>
              </div>
              
              <div className="button-group">
                  <button onClick={handleChangePassword} className="btn btn-primary">
                      비밀번호 변경
                  </button>    
                  <button onClick={handleEditInfo} className="btn btn-secondary">
                      정보 수정
                  </button>
                  <button onClick={handleLogout} className="btn btn-secondary">
                      로그아웃
                  </button>
              </div>
          </div>

          {showQRModal && (
              <div className="modal-overlay">
                  <div className="modal-content">
                      <div className="modal-header">
                          <h3>친구 추가 QR 코드</h3>
                      </div>
                      <img 
                          src="/static/qr_code.png" 
                          alt="QR Code" 
                          className="modal-qr-image"
                      />
                      <button 
                          onClick={() => setShowQRModal(false)}
                          className="modal-close-button"
                      >
                          닫기
                      </button>
                  </div>
              </div>
          )}
      </div>
  );
};

export default UserInfoPage;
