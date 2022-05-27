import { useAppSelect } from "@hooks/useStore";
import axios from "axios";
import React, { useState } from "react";
import styled from "styled-components";

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
    box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.2);
  }
`;

const Button = styled.button``;

const Label = styled.span`
  /* padding: 1rem 1rem 1rem 0; */
  font-weight: 200;
`;

const Name = styled.div`
  padding: 0.4rem 0 0 0;
  font-size: 1.5rem;
  font-weight: 700;
`;

const Lecture = (lecture: Lecture): JSX.Element => {
  const sid = useAppSelect((select) => select.user.studentId);
  const { lecture_name, lecture_code, credit, id, learned } = lecture;
  const [learn, setLearn] = useState(learned);

  const handleClick = () => {
    if (learn) {
      axios.delete(`http://localhost:8000/users/lectures/${id}`, {
        headers: { "student-id": sid },
      });
    } else {
      axios.post(
        `http://localhost:8000/users/lectures/${id}`,
        {},
        {
          headers: { "student-id": sid },
        }
      );
    }
    setLearn(!learn);
  };
  return (
    <Wrapper onClick={handleClick} learned={learn}>
      <Label className="label">{lecture_code}</Label>
      <Label className="label">{credit}</Label>
      <Name>{lecture_name}</Name>
    </Wrapper>
  );
};

export default React.memo(Lecture);
