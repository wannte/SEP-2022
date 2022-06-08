import { DLecture } from "@components/Lecture";
import { useAppDispatch, useAppSelect } from "@hooks/useStore";
import { fetchResult } from "@stores/resultSlice";
import { useEffect } from "react";
import styled from "styled-components";

const localeTitle = {
  basic: "기초 교양",
  major: "전공",
  research: "연구학점",
  free_select: "자유 선택",
  non_credit: "무학점 필수",
};

const localeSubTitle = {
  required_science: "기초 과학",
  required_language: "언어의 기초",
  liberal_arts: "인문 사회",
  freshman_semina: "신입생 세미나",
  required: "전공 필수",
  non_required: "전공 선택",
  research: "학사 논문 연구",
  basic: "기타 과학 선택",
  language_sw: "언어 선택/소프트웨어",
  pre_required: "선이수",
  other_pre_required: "기타 선이수",
  other_major: "타전공",
  other: "기타",
  art_music: "예능 실기",
  sport: "체육 실기",
  coloquium: "GIST 대학 콜로퀴움",
};

const FlexBox = styled.div`
  display: flexbox;
  flex-wrap: wrap;
  /* justify-content: space-between; */
  margin-bottom: 2rem;
`;

const Container = styled.div`
  margin: auto;
  max-width: 1200px;
  padding: 2rem 4rem;
`;

const Title = styled.div`
  font-weight: 500;
  font-size: 2rem;
  margin-bottom: 0.5rem;
`;

const SubTitle = styled.div`
  font-weight: 300;
  font-size: 1.5rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
`;

const Section = styled.div`
  border-bottom: 1px dotted rgba(0, 0, 0, 0.2);
  margin-bottom: 2rem;
`;

const Result = (): JSX.Element => {
  const result = useAppSelect((select) => select.result.data);
  const sid = useAppSelect((select) => select.user.studentId);
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(fetchResult(sid));
  }, []);

  return (
    <Container>
      {result ? (
        Object.entries(result).map(([key, title], idx) => {
          return (
            <Section key={`title_${idx}`}>
              <Title>{localeTitle[key as keyof typeof localeTitle]}</Title>
              {Object.entries(title).map(([elKey, elVal], idx) => {
                const lectures = elVal as Lectures;
                return (
                  <div key={`sub_${idx}`}>
                    <SubTitle>
                      <div>
                        {localeSubTitle[elKey as keyof typeof localeSubTitle]}
                      </div>
                      <div style={{ fontSize: "1rem", fontWeight: "700" }}>
                        {lectures.lectures.length
                          ? lectures.credit === 0
                            ? lectures.lectures.length + "학기 수강"
                            : lectures.credit.toString() + "학점 이수"
                          : ""}
                      </div>
                    </SubTitle>
                    <Columns L={lectures.lectures}></Columns>
                  </div>
                );
              })}
            </Section>
          );
        })
      ) : (
        <></>
      )}
    </Container>
  );
};

const Columns = ({ L }: { L: Lecture[] }): JSX.Element => {
  if (L.length === 0)
    return (
      <FlexBox>
        <div style={{ margin: "2rem 0" }}>수강한 강의가 없습니다.</div>
      </FlexBox>
    );
  return (
    <FlexBox>
      {L.map((lecture, idx) => {
        return (
          <div style={{ marginLeft: "1rem" }} key={`col_${idx}`}>
            <DLecture key={lecture.id} {...lecture}></DLecture>
          </div>
        );
      })}
    </FlexBox>
  );
};

export default Result;
