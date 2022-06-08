import styled from "styled-components";
import BackgroundImg from "@assets/graduation.jpg";
import { useState } from "react";
import { useAppDispatch } from "@hooks/useStore";
import { setId, setMajor } from "@stores/userSlice";
import { useNavigate } from "react-router-dom";
import API from "@utils/api";
import { fetchLectures, fetchResult } from "@stores/resultSlice";

const FlexColumn = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding: 15vh 0;
  height: 70vh;
`;

const Title = styled.h1`
  width: 600px;
  text-align: center;
  font-size: 66px;
  font-weight: 700;
  line-height: 1.4;
  color: rgb(0, 0, 0);
  word-break: keep-all;
  white-space: pre-wrap;
`;

const BackgroundMask = styled.div`
  width: 100%;
  height: calc(100vh - 50px);
  background: linear-gradient(
    to bottom,
    rgba(255, 255, 255, 1),
    rgba(255, 255, 255, 0.3),
    rgba(255, 255, 255, 0)
  );
  position: absolute;
  top: 50px;
  z-index: -1;
`;

const Background = styled.img`
  object-fit: cover;
  width: 100%;
  height: calc(100vh - 50px);
  position: absolute;
  top: 50px;
  z-index: -2;
`;

const Input = styled.input`
  background: rgba(255, 255, 255, 0.2);
  -webkit-backdrop-filter: blur(4px);
  backdrop-filter: blur(4px);
  box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.2);
  z-index: 2;
  text-align: center;
  border-radius: 1rem;
  border: none;
  width: 300px;
  height: 4rem;
  font-size: 1.5rem;
  transition: 0.2s;
  position: relative;
  :focus {
    outline: none;
    box-shadow: 0 0 1rem 0 rgba(0, 0, 0, 0.4);
  }
`;

const Home = (): JSX.Element => {
  const [input, setInput] = useState("");
  const idRegex = `^[0-9]{0,8}$`;

  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const handleChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const curr = event.target.value;
    if (curr.length <= 8 && curr.match(idRegex)) {
      setInput(curr);
    }
    if (curr.length === 8) {
      console.log("FULLFILLED");
      dispatch(setId({ studentId: curr }));
      const response = await API.get("/users/info", {
        headers: { "student-id": curr },
      });
      response?.data?.major
        ? dispatch(setMajor({ major: response.data.major }))
        : dispatch(setMajor({ major: null }));
      dispatch(fetchLectures(curr));
      dispatch(fetchResult(curr));
      navigate("/grad");
    }
  };

  return (
    <>
      <section>
        <BackgroundMask />
        <Background src={BackgroundImg} />
        <FlexColumn>
          <Title>복잡한 졸업요건 여기서 쉽고 간편하게</Title>
          <Input
            placeholder="학번 입력하고 시작"
            value={input}
            onChange={handleChange}
          />
        </FlexColumn>
      </section>
    </>
  );
};

export default Home;
