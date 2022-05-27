/* eslint-disable react-hooks/exhaustive-deps */
import Lecture from "@components/Lecture";
import { useEffect, useState } from "react";
import styled from "styled-components";
import qs from "qs";
import { useHeaders } from "@hooks/useHeaders";
import { SelectBox } from "@components/common";
import Summary from "@components/Summary";
import { majors, Major } from "@utils/majors";
// const mockLectures: Array<Lecture> = [
//   {
//     lectureCode: "EC4219",
//     lectureName: "소프트웨어 공학",
//     lectureCredit: 3,
//     learned: false,
//   },
//   {
//     lectureCode: "EC4202",
//     lectureName: "이산수학",
//     lectureCredit: 3,
//     learned: true,
//   },
//   {
//     lectureCode: "EC3212",
//     lectureName: "운영체제",
//     lectureCredit: 3,
//     learned: false,
//   },
//   {
//     lectureCode: "EC3203",
//     lectureName: "컴퓨터 시스템 이론 및 실습",
//     lectureCredit: 4,
//     learned: false,
//   },
// ];

const FlexBox = styled.div`
  display: flexbox;
  flex-wrap: wrap;
  justify-content: space-between;
`;
const Container = styled.div`
  margin: auto;
  max-width: 1200px;
  padding: 2rem 4rem;
`;

const HeaderWrapper = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: end;
  flex-direction: row;
`;

const Title = styled.div`
  font-weight: 300;
  font-size: 2rem;
`;

const FormWrapper = styled.div``;

const years = Array(8)
  .fill(0)
  .map((_v, i) => i + 2015)
  .reverse();

interface Options {
  year: string;
  semester: string;
  major: Major;
}

const Grad = (): JSX.Element => {
  const [lectures, setLectures] = useState<Array<Lecture>>([]);
  const [options, setOptions] = useState<Options>({
    year: "2022",
    semester: "spring",
    major: "GS",
  });

  const { fetch } = useHeaders();

  const fetchLecture = async () => {
    const response = await fetch("/lectures?" + qs.stringify(options));
    setLectures(response.data);
  };

  const fetchMajor = async () => {};

  useEffect(() => {
    fetchLecture();
  }, [options]);

  return (
    <>
      <Container>
        <HeaderWrapper>
          <Title>
            {`${options.year}년 ${
              options.semester === "spring" ? "봄" : "가을"
            }학기 ${majors[options.major]}`}
          </Title>
          <FormWrapper>
            <SelectBox
              value={options.year}
              onChange={(e) => {
                setOptions({ ...options, year: e.target.value });
              }}
            >
              {years.map((year) => (
                <option key={year}>{year}</option>
              ))}
            </SelectBox>
            <SelectBox
              value={options.semester}
              onChange={(e) => {
                setOptions({ ...options, semester: e.target.value });
              }}
            >
              <option value="spring">봄학기</option>
              {parseInt(options.year) < 2022 && (
                <option value="fall">가을학기</option>
              )}
            </SelectBox>
            <SelectBox
              value={options.major}
              onChange={(e) => {
                setOptions({
                  ...options,
                  major: e.target.value as Major,
                });
              }}
            >
              {Object.entries(majors).map((major) => {
                const [code, name] = major;
                return (
                  <option key={code} value={code}>
                    {name}
                  </option>
                );
              })}
            </SelectBox>
          </FormWrapper>
        </HeaderWrapper>
        <FlexBox>
          {lectures.map((lecture, idx) => (
            <Lecture key={`lecture_${lecture.lecture_code}`} {...lecture} />
          ))}
        </FlexBox>
      </Container>
      <Summary />
    </>
  );
};

export default Grad;
