import styled from "styled-components";
// import logo from "@assets/logo192.png";
import logo from "@assets/logo.svg";
import { useNavigate } from "react-router-dom";
import { memo } from "react";

const NavBarBlock = styled.div`
  color: black;
  height: 50px;
  margin: 0 auto;
  position: sticky;
  top: 0px;
  -webkit-backdrop-filter: blur(8px);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: space-between;
  border-bottom: 1px inset rgba(102, 103, 102, 0.4);
  z-index: 100;
`;

const NavWrapper = styled.div`
  position: relative;
  margin: 0 auto;
  max-width: 1200px;
  width: 100%;
  padding: 0 4em;
`;

const Logo = styled.img`
  position: absolute;
  top: 0;
  bottom: 0;
  margin: auto;
  height: 100%;
`;

const Menu = styled.div`
  display: flex;
  column-gap: 10px;
  align-items: center;
  justify-content: space-between;
  position: absolute;
  right: 4rem;
  top: 0;
  bottom: 0;
  margin: auto;
`;

const MenuButton = styled.button`
  height: 2rem;
  line-height: 2rem;
  font-weight: 300;
  font-size: 1rem;
  padding: 0 0.4rem;
  vertical-align: baseline;
  border-radius: 8px;
  transition: 0.2s;
  background: transparent;
  border: none;
  :hover {
    background-color: rgba(0, 0, 0, 0.1);
  }
`;

const Navbar = (): JSX.Element => {
  const navigate = useNavigate();
  return (
    <NavBarBlock>
      <NavWrapper>
        <a href="/">
          <Logo src={logo} alt="logo" />
        </a>
        <Menu>
          <MenuButton onClick={() => navigate("/grad")}>선택</MenuButton>
          <MenuButton onClick={() => navigate("/result")}>결과</MenuButton>
        </Menu>
      </NavWrapper>
    </NavBarBlock>
  );
};

export default memo(Navbar);
