/* eslint-disable react-hooks/exhaustive-deps */
import Lecture from "@components/Lecture";
import { useEffect, useState } from "react";
import styled from "styled-components";
import qs from "qs";
import { useHeaders } from "@hooks/useHeaders";
import { SelectBox } from "@components/common";
import Summary from "@components/Summary";
import { majors, Major } from "@utils/majors";
import { useAppSelect } from "@hooks/useStore";
import useDebounce from "@hooks/useDebounce";

const FlexBox = styled.div`
  min-height: calc(100vh - 130px - 6rem);
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

const NeedMajor = styled.div`
  line-height: calc(100vh - 130px - 5rem);
  text-align: center;
  height: calc(100vh - 130px - 6rem);
`;

const SearchBox = styled.div`
  position: fixed;
  bottom: 120px;
  right: calc(2rem - 300px);
  transition: 0.2s;
  :hover {
    right: -2rem;
  }
  input {
    background: rgba(255, 255, 255, 0.2);
    -webkit-backdrop-filter: blur(4px);
    backdrop-filter: blur(4px);
    box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.2);
    z-index: 100;
    text-align: center;
    border-radius: 1rem 0 0 1rem;
    padding-left: 1rem;
    padding-right: 4rem;
    border: none;
    width: 300px;
    height: 4rem;
    font-size: 1.5rem;
    transition: 0.2s;
    :focus {
      outline: none;
      box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.4);
    }
    transition: 0.2s;
  }
  button {
    color: black;
    position: relative;
    right: 3rem;
    top: calc(4rem - 50%);
    border: none;
    background: transparent;
    vertical-align: baseline;
    font-size: 1.5rem;
    border-radius: 8px;
    :hover {
      background-color: rgba(0, 0, 0, 0.1);
    }
  }
`;

const years = Array(8)
  .fill(0)
  .map((_v, i) => i + 2015)
  .reverse();

interface Options {
  year: string;
  semester: string;
  major: Major;
}

const Select = (): JSX.Element => {
  const [lectures, setLectures] = useState<Array<Lecture>>([]);
  const [filteredLectures, setFilteredLectures] = useState<Array<Lecture>>([]);
  const [learnedLectrues, setLearnedLectures] = useState<Array<Lecture>>([]);
  const [filter, setFilter] = useState("");
  const [options, setOptions] = useState<Options>({
    year: "2022",
    semester: "spring",
    major: "ALL",
  });
  const { major } = useAppSelect((select) => select.user);
  const result = useAppSelect((select) => select.result.data);
  const { fetch } = useHeaders();

  const fetchLecture = async () => {
    if (major) {
      const response = await fetch("/lectures?" + qs.stringify(options));
      setLectures(response.data);
      setFilteredLectures(filterLectures(response.data, filter));
    }
  };

  const filterLectures = (lectures: Lecture[], filter: string) => {
    return lectures.filter(
      (lecture) =>
        lecture.lecture_code.includes(filter) ||
        lecture.lecture_name.includes(filter)
    );
  };

  const debounceFilter = useDebounce({ value: filter, delay: 300 });
  useEffect(() => {
    if (debounceFilter) {
      setFilteredLectures(filterLectures(lectures, filter));
    } else {
      setFilteredLectures(lectures);
    }
  }, [debounceFilter]);

  useEffect(() => {
    fetchLecture();
    setFilter("");
  }, [options, major]);

  useEffect(() => {
    setLearnedLectures(lectures.filter((lecture) => lecture.learned));
  }, [result, lectures]);

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
        {major ? (
          <FlexBox>
            {filteredLectures.map((lecture, _idx) => (
              <Lecture key={`lecture_${lecture.id}`} {...lecture} />
            ))}
          </FlexBox>
        ) : (
          <NeedMajor>전공을 선택해주세요</NeedMajor>
        )}
      </Container>
      <SearchBox>
        <input
          placeholder="과목 검색"
          value={filter}
          onChange={(event) => {
            setFilter(event.target.value);
          }}
        />
        <button onClick={() => setFilter("")}>×</button>
      </SearchBox>
      {/* <Summary lLectures={learnedLectrues} /> */}
    </>
  );
};

export default Select;
