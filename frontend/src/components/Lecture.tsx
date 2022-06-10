import { useHeaders } from "@hooks/useHeaders";
import { useAppDispatch, useAppSelect } from "@hooks/useStore";
import { fetchLectures, fetchResult } from "@stores/resultSlice";
import React, { useCallback, useState } from "react";
import styled from "styled-components";

const ButtonWrapper = styled.div`
  /* position: relative; */
  box-sizing: content-box;
`;

const Button = styled.button<{ learn?: boolean }>`
  display: block;
  /* box-sizing: border-box; */
  position: relative;
  height: 80px;
  min-width: 240px;
  padding: 1rem;
  margin: 2rem 0;
  border-radius: 10px;
  border: ${(props) =>
    props.learn ? `1px inset rgba(102, 103, 171, 0.3)` : "none"};
  /* border: none; */
  background-color: transparent;
  background-color: ${(props) =>
    props.learn ? `rgba(102, 103, 171, 0.1)` : "transparent"};
  box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.05);
  :hover {
    box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.1);
  }
  transition: 0.2s;
  :hover {
    cursor: pointer;
  }
`;

const Label = styled.span`
  display: inline-block;
  font-weight: 200;
`;

const Credit = styled.span<{ learn: boolean }>`
  display: inline-block;
  position: absolute;
  top: 0.4rem;
  right: 0.4rem;
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
  background-color: ${(props) =>
    props.learn ? "rgba(102, 103, 171)" : "transparent"};
  color: ${(props) => (props.learn ? "white" : "transparent")}; ;
`;

const Name = styled.div`
  padding: 0.4rem 0 0 0;
  font-size: 1.5rem;
  font-weight: 700;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
`;

// interface ILecture extends Lecture {}

const Lecture = (lecture: Lecture): JSX.Element => {
  const { lecture_name, lecture_code, credit, id, learned } = lecture;
  const [learn, setLearn] = useState(learned);
  const { post, del } = useHeaders();
  const sid = useAppSelect((select) => select.user.studentId);
  const dispatch = useAppDispatch();
  const handleClick = () => {
    learn ? del(`/users/lectures/${id}`) : post(`/users/lectures/${id}`, {});
    setLearn(!learn);
    dispatch(fetchResult(sid));
    dispatch(fetchLectures(sid));
  };

  return (
    <ButtonWrapper>
      <Button onClick={handleClick} learn={learn}>
        <Label className="label">{lecture_code}</Label>
        <Credit className="label" learn={learn}>
          {credit}
        </Credit>
        <Name>{lecture_name}</Name>
      </Button>
    </ButtonWrapper>
  );
};

export const DLecture = (lecture: Omit<Lecture, "learned">): JSX.Element => {
  const { lecture_name, lecture_code, credit } = lecture;
  return (
    <ButtonWrapper>
      <Button>
        <Label className="label">{lecture_code}</Label>
        {credit && (
          <Credit className="label" learn={true}>
            {credit}
          </Credit>
        )}
        <Name>{lecture_name}</Name>
      </Button>
    </ButtonWrapper>
  );
};

// export default React.memo(
//   Lecture,
//   (prev, next) =>
//     prev.lecture_code === next.lecture_code &&
//     prev.learned === next.learned &&
//     prev.id === next.id
// );

export default React.memo(Lecture);
