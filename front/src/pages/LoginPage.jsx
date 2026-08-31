import { useState } from "react";
import styled from "styled-components";


function LoginPage({
    onLogin,
    onGoSignup,
}) {
    const [email, setEmail] =
        useState("");

    const [password, setPassword] =
        useState("");

    const [error, setError] =
        useState("");

    const [loading, setLoading] =
        useState(false);


    const handleSubmit = async (event) => {
        event.preventDefault();

        setError("");
        setLoading(true);


        try {
            await onLogin({
                email,
                password,
            });

        } catch (err) {
            setError(
                err.message ||
                "로그인에 실패했습니다."
            );

        } finally {
            setLoading(false);
        }
    };


    return (
        <Page>

            <Card>

                <Eyebrow>
                    IMAGE RAG
                </Eyebrow>

                <Title>
                    로그인
                </Title>

                <Description>
                    이미지 검색 서비스를 이용하려면
                    로그인해주세요.
                </Description>


                <Form onSubmit={handleSubmit}>

                    <Field>

                        <Label>
                            이메일
                        </Label>

                        <Input
                            type="email"
                            value={email}
                            onChange={(event) =>
                                setEmail(
                                    event.target.value
                                )
                            }
                            placeholder="test@test.com"
                            required
                        />

                    </Field>


                    <Field>

                        <Label>
                            비밀번호
                        </Label>

                        <Input
                            type="password"
                            value={password}
                            onChange={(event) =>
                                setPassword(
                                    event.target.value
                                )
                            }
                            placeholder="비밀번호"
                            required
                        />

                    </Field>


                    {
                        error && (
                            <ErrorMessage>
                                {error}
                            </ErrorMessage>
                        )
                    }


                    <PrimaryButton
                        type="submit"
                        disabled={loading}
                    >
                        {
                            loading
                                ? "로그인 중..."
                                : "로그인"
                        }
                    </PrimaryButton>

                </Form>


                <Bottom>

                    <span>
                        계정이 없나요?
                    </span>

                    <TextButton
                        type="button"
                        onClick={onGoSignup}
                    >
                        회원가입
                    </TextButton>

                </Bottom>

            </Card>

        </Page>
    );
}


export default LoginPage;


const Page = styled.div`
  min-height: 100vh;

  display: flex;
  align-items: center;
  justify-content: center;

  padding: 24px;

  background: #0c0f14;

  color: #f4f6f8;
`;


const Card = styled.div`
  width: 100%;
  max-width: 420px;

  padding: 40px;

  border: 1px solid #252a33;
  border-radius: 18px;

  background: #13171e;
`;


const Eyebrow = styled.div`
  margin-bottom: 10px;

  color: #7e8cff;

  font-size: 13px;
  font-weight: 700;

  letter-spacing: 0.16em;
`;


const Title = styled.h1`
  margin: 0;

  font-size: 34px;
`;


const Description = styled.p`
  margin: 12px 0 30px;

  color: #9199a7;

  line-height: 1.6;
`;


const Form = styled.form`
  display: flex;
  flex-direction: column;

  gap: 20px;
`;


const Field = styled.div`
  display: flex;
  flex-direction: column;

  gap: 8px;
`;


const Label = styled.label`
  color: #c7ccd4;

  font-size: 14px;
  font-weight: 600;
`;


const Input = styled.input`
  padding: 14px 16px;

  border: 1px solid #303641;
  border-radius: 10px;

  background: #0d1117;

  color: white;

  font-size: 15px;

  outline: none;

  &:focus {
    border-color: #7e8cff;
  }
`;


const PrimaryButton = styled.button`
  height: 48px;

  border: none;
  border-radius: 10px;

  background: #7e8cff;

  color: white;

  font-size: 15px;
  font-weight: 700;

  cursor: pointer;

  &:disabled {
    opacity: 0.6;

    cursor: default;
  }
`;


const ErrorMessage = styled.div`
  padding: 12px;

  border-radius: 8px;

  background: rgba(255, 80, 80, 0.12);

  color: #ff8b8b;

  font-size: 14px;
`;


const Bottom = styled.div`
  margin-top: 24px;

  display: flex;
  justify-content: center;
  gap: 8px;

  color: #9199a7;

  font-size: 14px;
`;


const TextButton = styled.button`
  padding: 0;

  border: none;

  background: transparent;

  color: #7e8cff;

  font-weight: 700;

  cursor: pointer;
`;