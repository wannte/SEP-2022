import { DLecture } from "@components/Lecture";
import { useAppDispatch, useAppSelect } from "@hooks/useStore";
import { fetchLectures, fetchResult } from "@stores/resultSlice";
import { useEffect, useLayoutEffect } from "react";
import styled from "styled-components";

const locale = {
  spring: "봄",
  summer: "여름",
  fall: "가을",
  winter: "겨울",
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

const Complete = (): JSX.Element => {
  const lectures = useAppSelect((select) => select.result.lectures);
  const sid = useAppSelect((select) => select.user.studentId);
  const dispatch = useAppDispatch();

  useEffect(() => {
    dispatch(fetchLectures(sid));
  }, [dispatch, sid]);

  if (lectures?.ok === false) {
    return <Container>수강한 과목이 없습니다.</Container>;
  }
  return (
    <Container>
      {lectures &&
        Object.entries(lectures).map(([year, semester]) => {
          return (
            <Section>
              <Title>{year}</Title>
              {Object.entries(semester).map(([sms, lectures]) => {
                return (
                  <>
                    <SubTitle>{`${
                      locale[sms as keyof typeof locale]
                    }학기`}</SubTitle>
                    <Columns L={lectures} />
                  </>
                );
              })}
            </Section>
          );
        })}
    </Container>
  );
};

const Columns = ({ L }: { L: Lecture[] }): JSX.Element => {
  console.log(L);
  if (!L || L.length === 0)
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

export default Complete;
