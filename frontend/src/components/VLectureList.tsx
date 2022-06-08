import styled from "styled-components";
import Lecture from "@components/Lecture";

const FlexBox = styled.div`
  display: flexbox;
  flex-wrap: wrap;
  justify-content: space-between;
  margin-bottom: 2rem;
`;

interface VLectureListProps {
  lectures: Lecture[];
}

const VLectureList = (props: VLectureListProps): JSX.Element => {
  return (
    <FlexBox>
      {props.lectures.map((lecture, _idx) => (
        <Lecture key={`lecture_${lecture.id}`} {...lecture} />
      ))}
    </FlexBox>
  );
};

export default VLectureList;
