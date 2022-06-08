import { useHeaders } from "@hooks/useHeaders";
import { useAppDispatch, useAppSelect } from "@hooks/useStore";
import { fetchLectures, fetchResult } from "@stores/resultSlice";
import { setMajor } from "@stores/userSlice";
import { majors } from "@utils/majors";
import React from "react";
import styled from "styled-components";
import { SelectBox } from "./common";

const SelectMajorContainer = styled.div`
  padding-top: 10px;
`;

const SelectMajor = (): JSX.Element => {
  const { studentId: sid, major } = useAppSelect((select) => select.user);
  const { put, post } = useHeaders();

  const dispatch = useAppDispatch();
  const handleChange = async (event: React.ChangeEvent<HTMLSelectElement>) => {
    if (major) {
      put("/users/major", event.target.value);
    } else {
      post("/users", { student_id: sid, major: event.target.value });
    }
    dispatch(setMajor({ major: event.target.value }));
    dispatch(fetchLectures(sid));
    dispatch(fetchResult(sid));
  };

  return (
    <SelectMajorContainer>
      <span>{`${sid.slice(2, 4)}학번 `}</span>
      <SelectBox onChange={handleChange} defaultValue={major || "null"}>
        <option disabled={true} value="null">
          전공을 선택하세요
        </option>
        {Object.entries(majors).map((major) => {
          const [code, name] = major;
          return (
            <option key={code} value={code}>
              {name}
            </option>
          );
        })}
      </SelectBox>
    </SelectMajorContainer>
  );
};

export default SelectMajor;
