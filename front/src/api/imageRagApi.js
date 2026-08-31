export const searchImage = async (file) => {
    const formData = new FormData();

    formData.append("file", file);

    const response = await fetch(
        "/api/image-rag/search",
        {
            method: "POST",
            body: formData,
        }
    );

    if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
            errorData.detail || "이미지 검색에 실패했습니다."
        );
    }

    return response.json();
};


export const getImageUrl = (path) => {
    return path;
};