import { useEffect, useState } from "react";
import styled from "styled-components";

interface WrapperProps {
  isClosing: boolean;
  type: "success" | "warning";
}

const Wrapper = styled.div<WrapperProps>`
  color: ${(props) => (props.type === "warning" ? "D52425" : "000000")};
  -webkit-backdrop-filter: blur(8px);
  backdrop-filter: blur(8px);
  /* background-color: black; */
  border: 1px solid
    ${(props) => (props.type === "warning" ? "D52425" : "000000")};
  padding-bottom: 4px;
  position: relative;
  animation: 0.3s forwards
    ${(props) => (props.isClosing ? "fadeout" : "slideFromBottom")};
  @keyframes fadeout {
    from {
      opacity: 1;
    }
    to {
      opacity: 0;
    }
  }
  @keyframes slideFromBottom {
    from {
      opacity: 0;
      transform: translateY(100%);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;

const Message = styled.div`
  margin: 10px 20px;
`;

interface LineProps {
  duration: number;
  type: "success" | "warning";
}

const Line = styled.div<LineProps>`
  background-color: ${(props) =>
    props.type === "warning" ? "D52425" : "000000"};
  animation: ${(props) => props.duration}s linear timer;
  position: absolute;
  bottom: 0;
  width: 0%;
  height: 2px;
  border-radius: 1px;
  @keyframes timer {
    from {
      width: 100%;
    }
    to {
      width: 0%;
    }
  } ;
`;

const ToastItem = ({ message, type, duration }: Toast) => {
  const [isClosing, setIsClosing] = useState(false);

  useEffect(() => {
    const setExitTimeout = setTimeout(() => {
      setIsClosing(true);
      clearTimeout(setExitTimeout);
      // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    }, duration!);
    return () => clearTimeout(setExitTimeout);
  });

  return (
    <Wrapper type={type} isClosing={isClosing}>
      <Message color={type}>
        <div>{message}</div>
      </Message>
      {/* eslint-disable-next-line @typescript-eslint/no-non-null-assertion */}
      <Line type={type} duration={duration! / 1000} />
    </Wrapper>
  );
};

export default ToastItem;
