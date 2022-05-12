import React, { useState } from "react";
import styled from "styled-components";
type ILecture = Omit<Lecture, "learned">;

const Wrapper = styled.div<{ learned: boolean }>`
  height: 80px;
  min-width: 320px;
  padding: 1rem;
  margin: 2rem 0;
  border-radius: 10px;
  border: ${(props) => (props.learned ? `1px inset black` : "none")};
  background-color: transparent;
  box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.1);
  :hover {
    box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.4);
  }
`;

const Button = styled.button``;

const Label = styled.span`
  /* padding: 1rem 1rem 1rem 0; */
  font-weight: 200;
`;

const Name = styled.div`
  font-size: 1.5rem;
  font-weight: 700;
`;

const MLecture = (lecture: ILecture): JSX.Element => {
  const [learned, setLearned] = useState(false);
  const { lectureName, lectureCode, lectureCredit } = lecture;
  const handleClick = () => {
    setLearned(!learned);
  };
  return (
    <Wrapper onClick={handleClick} learned={learned}>
      <Label className="label">{lectureCode}</Label>
      <Label className="label">{lectureCredit}</Label>
      <Name>{lectureName}</Name>
    </Wrapper>
  );
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
const Lecture = (lecture: Lecture): JSX.Element => {
  return (
    <div>
      <></>
    </div>
  );
};

export default React.memo(MLecture);
