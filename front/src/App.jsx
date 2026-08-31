import {
    useEffect,
    useState,
} from "react";

import styled from "styled-components";

import ImageSearchPage
    from "./pages/ImageSearchPage";

import LoginPage
    from "./pages/LoginPage";

import SignupPage
    from "./pages/SignupPage";

import {
    getMe,
    login,
    logout,
    refreshTokens,
    signup,
} from "./api/authApi";


function App() {
    const [page, setPage] =
        useState("loading");

    const [user, setUser] =
        useState(null);


    useEffect(() => {
        initializeAuth();
    }, []);


    const initializeAuth = async () => {
        const accessToken =
            localStorage.getItem(
                "access_token"
            );

        const refreshToken =
            localStorage.getItem(
                "refresh_token"
            );


        if (!accessToken) {
            setPage("login");
            return;
        }


        try {

            const currentUser =
                await getMe(
                    accessToken
                );


            setUser(
                currentUser
            );

            setPage(
                "app"
            );


        } catch {

            if (!refreshToken) {

                clearTokens();

                setPage(
                    "login"
                );

                return;
            }


            try {

                const tokenData =
                    await refreshTokens(
                        refreshToken
                    );


                saveTokens(
                    tokenData
                );


                const currentUser =
                    await getMe(
                        tokenData.access_token
                    );


                setUser(
                    currentUser
                );

                setPage(
                    "app"
                );


            } catch {

                clearTokens();

                setUser(null);

                setPage(
                    "login"
                );
            }
        }
    };


    const saveTokens = (
        tokenData
    ) => {

        localStorage.setItem(
            "access_token",
            tokenData.access_token
        );

        localStorage.setItem(
            "refresh_token",
            tokenData.refresh_token
        );
    };


    const clearTokens = () => {

        localStorage.removeItem(
            "access_token"
        );

        localStorage.removeItem(
            "refresh_token"
        );
    };


    const handleLogin = async ({
        email,
        password,
    }) => {

        const tokenData =
            await login({
                email,
                password,
            });


        saveTokens(
            tokenData
        );


        const currentUser =
            await getMe(
                tokenData.access_token
            );


        setUser(
            currentUser
        );

        setPage(
            "app"
        );
    };


    const handleSignup = async ({
        email,
        password,
        nickname,
    }) => {

        await signup({
            email,
            password,
            nickname,
        });


        const tokenData =
            await login({
                email,
                password,
            });


        saveTokens(
            tokenData
        );


        const currentUser =
            await getMe(
                tokenData.access_token
            );


        setUser(
            currentUser
        );

        setPage(
            "app"
        );
    };


    const handleLogout = async () => {

        const refreshToken =
            localStorage.getItem(
                "refresh_token"
            );


        try {

            if (refreshToken) {
                await logout(
                    refreshToken
                );
            }

        } catch (error) {

            console.error(
                error
            );

        } finally {

            clearTokens();

            setUser(null);

            setPage(
                "login"
            );
        }
    };


    if (
        page === "loading"
    ) {
        return (
            <LoadingPage>
                로그인 상태 확인 중...
            </LoadingPage>
        );
    }


    if (
        page === "login"
    ) {
        return (
            <LoginPage
                onLogin={handleLogin}
                onGoSignup={() =>
                    setPage("signup")
                }
            />
        );
    }


    if (
        page === "signup"
    ) {
        return (
            <SignupPage
                onSignup={handleSignup}
                onGoLogin={() =>
                    setPage("login")
                }
            />
        );
    }


    return (
        <AppContainer>

            <UserBar>

                <UserInfo>

                    <strong>
                        {user?.nickname}
                    </strong>

                    <span>
                        {user?.email}
                    </span>

                </UserInfo>


                <LogoutButton
                    type="button"
                    onClick={handleLogout}
                >
                    로그아웃
                </LogoutButton>

            </UserBar>


            <ImageSearchPage />

        </AppContainer>
    );
}


export default App;


const AppContainer = styled.div`
  min-height: 100vh;

  background: #0c0f14;
`;


const LoadingPage = styled.div`
  min-height: 100vh;

  display: flex;
  align-items: center;
  justify-content: center;

  background: #0c0f14;

  color: white;

  font-size: 16px;
`;


const UserBar = styled.div`
  height: 64px;

  padding: 0 48px;

  display: flex;
  align-items: center;
  justify-content: space-between;

  border-bottom: 1px solid #232933;

  background: #10141a;

  color: white;

  @media (max-width: 700px) {
    padding: 0 20px;
  }
`;


const UserInfo = styled.div`
  display: flex;
  align-items: center;

  gap: 12px;

  span {
    color: #8d96a5;

    font-size: 14px;
  }
`;


const LogoutButton = styled.button`
  padding: 9px 16px;

  border: 1px solid #343b48;
  border-radius: 8px;

  background: transparent;

  color: #dce1e8;

  cursor: pointer;

  &:hover {
    background: #1a2029;
  }
`;