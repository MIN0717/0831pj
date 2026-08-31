import styled from "styled-components";

import { getImageUrl } from "../api/imageRagApi";


function SearchResult({
                          data,
                          loading,
                          error,
                      }) {
    return (
        <Card>
            <SectionTitle>
                <Number>02</Number>

                <h2>검색 결과</h2>
            </SectionTitle>


            {error && (
                <ErrorBox>
                    {error.message}
                </ErrorBox>
            )}


            {loading && (
                <Center>
                    <Spinner />

                    <h3>
                        이미지를 분석하고 있습니다.
                    </h3>

                    <p>
                        AI가 음식 종류를 판단하고 관련 이미지를 검색합니다.
                    </p>
                </Center>
            )}


            {!loading && !data && !error && (
                <Center>
                    <EmptyIcon>
                        AI
                    </EmptyIcon>

                    <h3>
                        아직 검색 결과가 없습니다.
                    </h3>

                    <p>
                        이미지를 업로드해주세요.
                    </p>
                </Center>
            )}


            {data && (
                <>
                    <FoodInfo>
                        <Label>
                            AI 분석 결과
                        </Label>

                        <h2>
                            {data.food_name}
                        </h2>

                        <p>
                            {data.description}
                        </p>
                    </FoodInfo>


                    <ResultHeader>
                        <h3>
                            관련 이미지
                        </h3>

                        <span>
              {data.images?.length || 0}개
            </span>
                    </ResultHeader>


                    <ImageGrid>
                        {data.images?.map(
                            (image, index) => (
                                <ImageCard key={image}>
                                    <img
                                        src={getImageUrl(image)}
                                        alt={`${data.food_name} ${index + 1}`}
                                    />

                                    <IndexBadge>
                                        {String(index + 1).padStart(2, "0")}
                                    </IndexBadge>
                                </ImageCard>
                            )
                        )}
                    </ImageGrid>
                </>
            )}
        </Card>
    );
}


export default SearchResult;


const Card = styled.section`
  min-height: 650px;

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


const Center = styled.div`
  min-height: 520px;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  text-align: center;

  color: #7e8794;

  h3 {
    margin: 20px 0 8px;

    color: #dfe3e9;
  }

  p {
    margin: 0;

    font-size: 14px;
  }
`;


const EmptyIcon = styled.div`
  width: 72px;
  height: 72px;

  display: flex;
  align-items: center;
  justify-content: center;

  border: 1px solid #293142;
  border-radius: 22px;

  color: #7180ff;

  font-weight: 800;
`;


const Spinner = styled.div`
  width: 46px;
  height: 46px;

  border: 4px solid #242a35;
  border-top-color: #7180ff;

  border-radius: 50%;

  animation: spin 0.8s linear infinite;

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
`;


const ErrorBox = styled.div`
  padding: 14px;

  border-radius: 12px;

  background: rgba(255, 80, 80, 0.08);

  color: #ff9c9c;
`;


const FoodInfo = styled.div`
  padding: 24px;

  border: 1px solid #28304a;
  border-radius: 18px;

  background: rgba(92, 108, 247, 0.08);

  h2 {
    margin: 0;

    font-size: 32px;
  }

  p {
    margin: 12px 0 0;

    color: #a8afba;
  }
`;


const Label = styled.p`
  margin: 0 0 10px !important;

  color: #7e8cff !important;

  font-size: 12px;
  font-weight: 800;
`;


const ResultHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;

  margin: 28px 0 14px;

  h3 {
    margin: 0;
  }

  span {
    color: #8d96a3;
  }
`;


const ImageGrid = styled.div`
  display: grid;

  grid-template-columns:
    repeat(3, minmax(0, 1fr));

  gap: 14px;
`;


const ImageCard = styled.div`
  position: relative;

  overflow: hidden;

  aspect-ratio: 1 / 1;

  border-radius: 15px;

  background: #0f1217;

  img {
    width: 100%;
    height: 100%;

    object-fit: cover;
  }
`;


const IndexBadge = styled.div`
  position: absolute;

  right: 9px;
  bottom: 9px;

  padding: 5px 8px;

  border-radius: 8px;

  background: rgba(0, 0, 0, 0.7);

  font-size: 11px;
`;