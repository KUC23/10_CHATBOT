import React from 'react';
import { useFormik } from "formik";
import * as Yup from "yup";
import { useNavigate } from 'react-router-dom';
import { signup } from "../api/accounts";

const SignupPage = () => {
  const navigate = useNavigate();

  const formik = useFormik({
      initialValues: {
          username: "",
          password: "",
          password2: "",
          phone_number: "",
          default_social_provider: "",
      },
      validationSchema: Yup.object({
          username: Yup.string()
              .required("Username is required"),
          password: Yup.string()
              .min(8, "비밀번호는 최소 8자 이상이어야 합니다")
              .matches(/[0-9]/, "숫자를 포함해야 합니다")
              .matches(/[!@#$%^&*]/, "특수문자(!@#$%^&*)를 포함해야 합니다")
              .required("Password is required"),
          password2: Yup.string()
              .oneOf([Yup.ref("password")], "비밀번호가 일치하지 않습니다")
              .required("비밀번호 확인을 입력해주세요"),
          phone_number: Yup.string()
              .required("Phone number를 입력해주세요"),
          default_social_provider: Yup.string()
              .required("매신저 플랫폼을 선택해주세요")
      }),
      onSubmit: async (values) => {
          try {
              const response = await signup(values);
              alert("회원가입이 완료되었습니다!");
              navigate('/user-info');
          } catch (error) {
              console.error('회원가입 실패:', error);
              alert(error.message || "회원가입 중 오류가 발생했습니다.");
          }
      },
  });

  // 비밀번호 검사 기믹
  const checks = {
      length: formik.values.password.length >= 8,
      number: /[0-9]/.test(formik.values.password),
      special: /[!@#$%^&*]/.test(formik.values.password)
  };

  return (
      <div className="auth-container">
          <img src="/static/logo.png" alt="SmartScoop" className="logo" />
          <div className="auth-card">
              <h2 className="auth-title">Create Account</h2>
              <form onSubmit={formik.handleSubmit}>
                  <input
                      className="input-field"
                      name="username"
                      placeholder="Username"
                      {...formik.getFieldProps('username')}
                  />
                  <div className="password-section">
                      <input
                          className="input-field"
                          name="password"
                          type="password"
                          placeholder="Password"
                          {...formik.getFieldProps('password')}
                      />
                      {/* 비밀번호 검시 기믹 */}
                      <div className="password-validation">
                            {Object.entries({
                                number: checks.number,
                                special: checks.special,
                                length: checks.length
                            }).map(([key, passed]) => (
                                <div
                                    key={key}
                                    className={`validation-item ${passed ? 'passed' : 'failed'}`}
                                >
                                    <span className="validation-icon">{passed ? '✓' : '✗'}</span>
                                    <span>
                                        {key === 'number' ? '영문(대,소문자 허용)숫자 포함' :
                                            key === 'special' ? '특수문자(!@#$%^&*) 포함' :
                                            '8자 이상'}
                                    </span>
                                </div>
                            ))}
                        </div>
                  </div>
                  <input
                      className="input-field"
                      name="password2"
                      type="password"
                      placeholder="Confirm Password"
                      {...formik.getFieldProps('password2')}
                  />
                  <input
                      className="input-field"
                      name="phone_number"
                      placeholder="Phone Number"
                      {...formik.getFieldProps('phone_number')}
                  />
                  <select
                      className="select-field"
                      name="default_social_provider"
                      {...formik.getFieldProps('default_social_provider')}
                  >
                      <option value="">Select Platform</option>
                      <option value="kakao">Kakao</option>
                  </select>
                  <button type="submit" className="btn btn-primary">Sign Up</button>
              </form>
          </div>
      </div>
  );
};

export default SignupPage;