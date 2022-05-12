import Lecture from "@components/Lecture";
import styled from "styled-components";

const lectures: Array<Lecture> = [
  {
    lectureCode: "EC4219",
    lectureName: "소프트웨어 공학",
    lectureCredit: 3,
    learned: false,
  },
  {
    lectureCode: "EC4202",
    lectureName: "이산수학",
    lectureCredit: 3,
    learned: true,
  },
  {
    lectureCode: "EC3212",
    lectureName: "운영체제",
    lectureCredit: 3,
    learned: false,
  },
  {
    lectureCode: "EC3203",
    lectureName: "컴퓨터 시스템 이론 및 실습",
    lectureCredit: 4,
    learned: false,
  },
];

const FlexBox = styled.div`
  display: flexbox;
  flex-wrap: wrap;
  justify-content: space-between;
`;
const Wrapper = styled.div`
  margin: auto;
  max-width: 1200px;
  padding: 0 4rem;
`;

const majors = [
  "기초교육학부",
  "전기전자컴퓨터공학부",
  "신소재공학부",
  "기계공학부",
  "지구환경공학부",
];

const Grad = (): JSX.Element => {
  return (
    <Wrapper>
      <select>
        <option>2018</option>
        <option>2019</option>
        <option>2020</option>
        <option>2021</option>
        <option>2022</option>
      </select>
      <select>
        <option>Spring</option>
        <option>Fall</option>
      </select>
      <select>
        {majors.map((major) => (
          <option>{major}</option>
        ))}
      </select>
      <FlexBox>
        {lectures.map((lecture) => (
          <Lecture {...lecture} />
        ))}
      </FlexBox>
    </Wrapper>
  );
};

export default Grad;
