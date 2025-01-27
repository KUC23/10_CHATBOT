import React from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { useNavigate } from "react-router-dom";
import { changePassword } from "../api/accounts";

const ChangePasswordPage = () => {
   const navigate = useNavigate();

   const formik = useFormik({
       initialValues: {
           old_password: "",
           new_password: "",
           confirm_password: "",
       },
       validationSchema: Yup.object({
           old_password: Yup.string().required("현재 비밀번호를 입력해주세요"),
           new_password: Yup.string().required("새 비밀번호를 입력해주세요"),
           confirm_password: Yup.string()
               .oneOf([Yup.ref("new_password")], "비밀번호가 일치하지 않습니다")
               .required("비밀번호 확인을 입력해주세요"),
       }),
       onSubmit: async (values) => {
           try {
               await changePassword({
                   old_password: values.old_password,
                   new_password: values.new_password,
                   new_password2: values.confirm_password
               });
               alert("비밀번호가 성공적으로 변경되었습니다.");
               navigate("/user-info");
           } catch (error) {
               const errorMessage = error.response?.data?.message || "비밀번호 변경에 실패했습니다.";
               alert(errorMessage);
           }
       },
   });

   return (
       <div className="auth-container">
           <div className="auth-card">
               <h2 className="auth-title">비밀번호 변경</h2>
               <form onSubmit={formik.handleSubmit} className="form-group">
                   <div className="input-changepwd-container">
                       <input
                           className="input-changepwd-field"
                           name="old_password"
                           type="password"
                           placeholder="현재 비밀번호"
                           value={formik.values.old_password}
                           onChange={formik.handleChange}
                       />
                       {formik.errors.old_password && formik.touched.old_password && (
                           <div className="error-text">{formik.errors.old_password}</div>
                       )}
                   </div>

                   <div className="input-changepwd-container">
                       <input
                           className="input-changepwd-field"
                           name="new_password"
                           type="password"
                           placeholder="새 비밀번호"
                           value={formik.values.new_password}
                           onChange={formik.handleChange}
                       />
                       {formik.errors.new_password && formik.touched.new_password && (
                           <div className="error-text">{formik.errors.new_password}</div>
                       )}
                   </div>

                   <div className="input-changepwd-container">
                       <input
                           className="input-changepwd-field"
                           name="confirm_password"
                           type="password"
                           placeholder="새 비밀번호 확인"
                           value={formik.values.confirm_password}
                           onChange={formik.handleChange}
                       />
                       {formik.errors.confirm_password && formik.touched.confirm_password && (
                           <div className="error-text">{formik.errors.confirm_password}</div>
                       )}
                   </div>

                   <button type="submit" className="btn btn-primary">
                       비밀번호 변경
                   </button>
               </form>
           </div>
       </div>
   );
};

export default ChangePasswordPage;