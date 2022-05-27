import styled from "styled-components";

export const FlexRow = styled.div`
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
`;

export const FlexColumn = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

export const SelectBox = styled.select`
  font-size: 1rem;
  margin-left: 1rem;
  border: none;
  background: transparent;
  min-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  border-radius: 2px;
  :hover {
    cursor: pointer;
  }
  option {
  }
`;
