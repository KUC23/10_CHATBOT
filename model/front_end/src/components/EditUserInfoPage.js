import React, { useState, useEffect } from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { getUserInfo, updateUserInfo } from "../api/accounts";
import { useNavigate } from "react-router-dom";

const EditUserInfoPage = () => {
   const [userInfo, setUserInfo] = useState(null);
   const navigate = useNavigate();

   const [categoryNames] = useState({
       1: "main", 2: "technology", 3: "business", 
       4: "science", 5: "health", 6: "politics", 
       7: "art", 8: "sport"
   });

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

   const formik = useFormik({
       initialValues: {
           username: userInfo ? userInfo.username : "",
           phone_number: userInfo ? userInfo.phone_number : "",
           categories: userInfo ? userInfo.categories : "",
           default_social_provider: userInfo ? userInfo.default_social_provider : "",
       },
       enableReinitialize: true,
       validationSchema: Yup.object({
           username: Yup.string().required("Username is required"),
           phone_number: Yup.string().required("Phone number is required"),
           categories: Yup.string().required("Select a category"),
           default_social_provider: Yup.string().required("Select a platform"),
       }),
       onSubmit: async (values) => {
           try {
               const updateData = {
                   username: values.username,
                   phone_number: values.phone_number,
                   categories: [parseInt(values.categories, 10)],
                   default_social_provider: values.default_social_provider
               };

               console.log('수정 요청 데이터:', updateData);
               await updateUserInfo(updateData);
               alert("사용자 정보가 성공적으로 수정되었습니다.");
               navigate('/user-info');
           } catch (error) {
               console.error("사용자 정보 수정 실패:", error);
               const errorMessage = error.response?.data?.message || "사용자 정보 수정에 실패했습니다.";
               alert(errorMessage);
           }
       },
   });

   if (!userInfo) {
       return <div className="loading">Loading...</div>;
   }

   return (
       <div className="auth-container">
           <div className="auth-card">
               <h2 className="auth-title">정보 수정</h2>
               <form onSubmit={formik.handleSubmit} className="form-group">
                   <div className="input-container">
                       <input
                           className="input-field disabled"
                           name="username"
                           placeholder="사용자명"
                           value={formik.values.username}
                           onChange={formik.handleChange}
                           disabled
                       />
                   </div>

                   <div className="input-container">
                       <input
                           className="input-field"
                           name="phone_number"
                           placeholder="전화번호"
                           value={formik.values.phone_number}
                           onChange={formik.handleChange}
                       />
                       {formik.errors.phone_number && formik.touched.phone_number && (
                           <div className="error-text">{formik.errors.phone_number}</div>
                       )}
                   </div>

                   <div className="input-container">
                       <select
                           className="select-field"
                           name="categories"
                           value={formik.values.categories}
                           onChange={formik.handleChange}
                       >
                           <option value="">관심 카테고리 선택</option>
                           {Object.entries(categoryNames).map(([key, value]) => (
                               <option key={key} value={key}>{value}</option>
                           ))}
                       </select>
                       {formik.errors.categories && formik.touched.categories && (
                           <div className="error-text">{formik.errors.categories}</div>
                       )}
                   </div>

                   <div className="input-container">
                       <select
                           className="select-field"
                           name="default_social_provider"
                           value={formik.values.default_social_provider}
                           onChange={formik.handleChange}
                       >
                           <option value="">메신저 플랫폼 선택</option>
                           <option value="kakao">Kakao</option>
                       </select>
                       {formik.errors.default_social_provider && formik.touched.default_social_provider && (
                           <div className="error-text">{formik.errors.default_social_provider}</div>
                       )}
                   </div>

                   <button type="submit" className="btn btn-primary">
                       변경사항 저장
                   </button>
               </form>
           </div>
       </div>
   );
};

export default EditUserInfoPage;