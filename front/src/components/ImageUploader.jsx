import { useEffect, useState } from "react";
import styled from "styled-components";


function ImageUploader({
                           selectedFile,
                           onFileChange,
                           onSearch,
                           loading,
                       }) {
    const [previewUrl, setPreviewUrl] = useState(null);


    useEffect(() => {
        if (!selectedFile) {
            setPreviewUrl(null);
            return;
        }

        const url = URL.createObjectURL(selectedFile);

        setPreviewUrl(url);


        return () => {
            URL.revokeObjectURL(url);
        };
    }, [selectedFile]);


    const handleChange = (event) => {
        const file = event.target.files?.[0];

        if (!file) {
            return;
        }

        onFileChange(file);
    };


    return (
        <Card>
            <SectionTitle>
                <Number>01</Number>

                <h2>이미지 업로드</h2>
            </SectionTitle>


            <UploadArea>
                {previewUrl ? (
                    <Preview
                        src={previewUrl}
                        alt="업로드 이미지"
                    />
                ) : (
                    <Placeholder>
                        <UploadIcon>+</UploadIcon>

                        <strong>
                            이미지를 선택하세요
                        </strong>

                        <p>
                            JPG, JPEG, PNG, WEBP
                        </p>
                    </Placeholder>
                )}

                <input
                    type="file"
                    accept="image/*"
                    onChange={handleChange}
                    hidden
                />
            </UploadArea>


            {selectedFile && (
                <FileInfo>
                    <span>선택된 파일</span>

                    <strong>
                        {selectedFile.name}
                    </strong>
                </FileInfo>
            )}


            <SearchButton
                type="button"
                onClick={onSearch}
                disabled={!selectedFile || loading}
            >
                {loading
                    ? "AI 분석 중..."
                    : "유사 이미지 검색"
                }
            </SearchButton>
        </Card>
    );
}


export default ImageUploader;


const Card = styled.section`
  padding: 26px;

  border: 1px solid #252b35;
  border-radius: 22px;

  background: rgba(20, 24, 31, 0.94);
`;


const SectionTitle = styled.div`
  display: flex;
  align-items: center;

  gap: 12px;

  margin-bottom: 22px;

  h2 {
    margin: 0;

    font-size: 18px;
  }
`;


const Number = styled.span`
  display: flex;
  align-items: center;
  justify-content: center;

  width: 34px;
  height: 34px;

  border-radius: 10px;

  background: #202744;

  color: #8795ff;

  font-size: 13px;
  font-weight: 800;
`;


const UploadArea = styled.label`
  display: flex;
  align-items: center;
  justify-content: center;

  width: 100%;

  aspect-ratio: 1 / 0.82;

  overflow: hidden;

  border: 1px dashed #39404b;
  border-radius: 18px;

  background: #10141a;

  cursor: pointer;
`;


const Placeholder = styled.div`
  text-align: center;

  color: #89919f;

  strong {
    display: block;

    margin-top: 16px;

    color: #e8ebf0;
  }

  p {
    margin: 8px 0 0;

    font-size: 13px;
  }
`;


const UploadIcon = styled.div`
  width: 58px;
  height: 58px;

  margin: 0 auto;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 16px;

  background: #1e2540;

  color: #8795ff;

  font-size: 30px;
`;


const Preview = styled.img`
  width: 100%;
  height: 100%;

  object-fit: cover;
`;


const FileInfo = styled.div`
  margin-top: 14px;

  display: flex;
  flex-direction: column;

  gap: 5px;

  padding: 13px 15px;

  border-radius: 12px;

  background: #10141a;

  span {
    color: #737c89;

    font-size: 11px;
  }

  strong {
    overflow: hidden;

    font-size: 13px;

    text-overflow: ellipsis;
    white-space: nowrap;
  }
`;


const SearchButton = styled.button`
  width: 100%;

  margin-top: 16px;

  padding: 15px;

  border: 0;
  border-radius: 13px;

  background: #5d6cf7;

  color: white;

  font-weight: 700;

  cursor: pointer;

  &:disabled {
    opacity: 0.45;

    cursor: not-allowed;
  }
`;