/* eslint-disable react-hooks/exhaustive-deps */
import Lecture from "@components/Lecture";
import { useAppSelect } from "@hooks/useStore";
import axios from "axios";
import { useEffect, useState } from "react";
import styled from "styled-components";
import qs from "qs";

// const lectures: Array<Lecture> = [
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
const Wrapper = styled.div`
  margin: auto;
  max-width: 1200px;
  padding: 0 4rem;
`;

const majors = [
  "EB",
  "BS",
  "AP",
  "CT",
  "UC",
  "MM",
  "AI",
  "SS",
  "CH",
  "FE",
  "IR",
  "PP",
  "GS",
  "PS",
  "LH",
  "MD",
  "EC",
  "MC",
  "CM",
  "ET",
  "MA",
  "CC",
  "MB",
  "EV",
];

const years = Array(8)
  .fill(0)
  .map((v, i) => i + 2015)
  .reverse();

interface Options {
  year: string;
  semester: string;
  major: string;
}

const Grad = (): JSX.Element => {
  const [lectures, setLectures] = useState<Array<Lecture>>([]);
  const [options, setOptions] = useState<Options>({
    year: "2022",
    semester: "spring",
    major: "EC",
  });

  const id = useAppSelect((select) => select.user.studentId);

  const fetchLecture = async () => {
    const response = await axios.get(
      "http://localhost:8000/lectures?" + qs.stringify(options),
      { headers: { "student-id": id } }
    );
    setLectures(response.data);
  };

  useEffect(() => {
    fetchLecture();
  }, [options]);

  return (
    <Wrapper>
      <form>
        <select
          value={options.year}
          onChange={(e) => {
            setOptions({ ...options, year: e.target.value });
          }}
        >
          {years.map((year) => (
            <option key={year}>{year}</option>
          ))}
        </select>
        <select
          value={options.semester}
          onChange={(e) => {
            setOptions({ ...options, semester: e.target.value });
          }}
        >
          <option>spring</option>
          <option>fall</option>
        </select>
        <select
          value={options.major}
          onChange={(e) => {
            setOptions({ ...options, major: e.target.value });
          }}
        >
          {majors.map((major) => (
            <option key={major}>{major}</option>
          ))}
        </select>
      </form>
      <FlexBox>
        {lectures.map((lecture, idx) => (
          <Lecture key={`lecture_${idx}`} {...lecture} />
        ))}
      </FlexBox>
    </Wrapper>
  );
};

export default Grad;
