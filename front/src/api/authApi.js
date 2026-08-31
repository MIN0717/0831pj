export const signup = async ({
    email,
    password,
    nickname,
}) => {
    const response = await fetch(
        "/auth/signup",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                email,
                password,
                nickname,
            }),
        }
    );


    if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
            errorData.detail || "회원가입에 실패했습니다."
        );
    }


    return response.json();
};


export const login = async ({
    email,
    password,
}) => {
    const response = await fetch(
        "/auth/login",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                email,
                password,
            }),
        }
    );


    if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
            errorData.detail || "로그인에 실패했습니다."
        );
    }


    return response.json();
};


export const getMe = async (
    accessToken
) => {
    const response = await fetch(
        "/auth/me",
        {
            method: "GET",

            headers: {
                Authorization:
                    `Bearer ${accessToken}`,
            },
        }
    );


    if (!response.ok) {
        throw new Error(
            "인증에 실패했습니다."
        );
    }


    return response.json();
};


export const refreshTokens = async (
    refreshToken
) => {
    const response = await fetch(
        "/auth/refresh",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                refresh_token: refreshToken,
            }),
        }
    );


    if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
            errorData.detail ||
            "토큰 갱신에 실패했습니다."
        );
    }


    return response.json();
};


export const logout = async (
    refreshToken
) => {
    const response = await fetch(
        "/auth/logout",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                refresh_token: refreshToken,
            }),
        }
    );


    if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
            errorData.detail ||
            "로그아웃에 실패했습니다."
        );
    }


    return response.json();
};