import { useHeaders } from "@hooks/useHeaders";
import { useAppDispatch, useAppSelect } from "@hooks/useStore";
import { setMajor } from "@stores/userSlice";
import API from "@utils/api";
import { majors } from "@utils/majors";
import React, { useEffect, useState } from "react";
import styled from "styled-components";
import { SelectBox } from "./common";

const SummaryBarBlock = styled.div`
  color: black;
  height: 120px;
  margin: 0 auto;
  position: sticky;
  bottom: 0px;
  background-color: rgba(255, 255, 255, 0.6);
  -webkit-backdrop-filter: blur(8px);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: space-between;
  border-top: 1px inset rgba(102, 103, 171, 0.4);
  z-index: 100;
`;

const SummaryBarWrapper = styled.div`
  position: relative;
  margin: 0 auto;
  max-width: 1200px;
  width: 100%;
  padding: 0 4em;
`;

const Summary = (): JSX.Element => {
  const [totalCredit, setTotalCredit] = useState(0);

  const { studentId: sid, major } = useAppSelect((select) => select.user);
  const { fetch, put } = useHeaders();

  const fetchTotalCredit = async () => {
    const response = await fetch("/users/credit/total");
    setTotalCredit(response.data);
  };

  fetchTotalCredit();

  const dispatch = useAppDispatch();
  const handleChange = async (event: React.ChangeEvent<HTMLSelectElement>) => {
    dispatch(setMajor({ major: event.target.value }));
    put("/users/major", { major: event.target.value });
  };

  return (
    <SummaryBarBlock>
      <SummaryBarWrapper>
        <div>
          <span>{`${sid.slice(2, 4)}학번 `}</span>
          {false ? (
            <span>{major}</span>
          ) : (
            <SelectBox onChange={handleChange}>
              <option disabled={true}>전공을 선택하세요</option>
              {Object.entries(majors).map((major) => {
                const [code, name] = major;
                return <option value={code}>{name}</option>;
              })}
            </SelectBox>
          )}
        </div>
        <div>{`총 ${totalCredit}학점 수강했습니다.`}</div>
      </SummaryBarWrapper>
    </SummaryBarBlock>
  );
};

export default Summary;
