import { useState } from "react";
import styled from "styled-components";

import ImageUploader from "../components/ImageUploader";
import SearchResult from "../components/SearchResult";
import { useImageRagMutation } from "../query/useImageRagMutation";


function ImageSearchPage() {
    const [selectedFile, setSelectedFile] = useState(null);

    const imageMutation = useImageRagMutation();


    const handleFileChange = (file) => {
        setSelectedFile(file);

        imageMutation.reset();
    };


    const handleSearch = () => {
        if (!selectedFile) {
            return;
        }

        imageMutation.mutate(selectedFile);
    };


    return (
        <Page>
            <Header>
                <Eyebrow>
                    AI FOOD IMAGE SEARCH
                </Eyebrow>

                <h1>
                    음식 이미지 검색
                </h1>

                <p>
                    음식 사진을 업로드하면 AI가 음식을 분석하고
                    관련 이미지를 검색합니다.
                </p>
            </Header>


            <Content>
                <ImageUploader
                    selectedFile={selectedFile}
                    onFileChange={handleFileChange}
                    onSearch={handleSearch}
                    loading={imageMutation.isPending}
                />

                <SearchResult
                    data={imageMutation.data}
                    loading={imageMutation.isPending}
                    error={imageMutation.error}
                />
            </Content>
        </Page>
    );
}


export default ImageSearchPage;


const Page = styled.div`
  min-height: 100vh;

  padding: 48px;

  background: #0c0f14;

  color: #f4f6f8;
`;


const Header = styled.header`
  max-width: 1440px;

  margin: 0 auto 36px;

  h1 {
    margin: 0;

    font-size: 42px;
  }

  p {
    max-width: 620px;

    color: #9199a7;

    line-height: 1.7;
  }
`;


const Eyebrow = styled.div`
  margin-bottom: 12px;

  color: #7e8cff;

  font-size: 13px;
  font-weight: 700;

  letter-spacing: 0.18em;
`;


const Content = styled.main`
  max-width: 1440px;

  margin: 0 auto;

  display: grid;

  grid-template-columns:
    0.85fr 1.4fr;

  gap: 24px;

  @media (max-width: 900px) {
    grid-template-columns: 1fr;
  }
`;