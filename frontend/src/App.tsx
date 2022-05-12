import { BrowserRouter, Route, Routes } from "react-router-dom";
import Navbar from "@components/Navbar";
import Home from "@pages/Home";
import { GlobalStyle } from "@styles/global";
import Grad from "@pages/Grad";

const MainRouter = (): JSX.Element => {
  return (
    <>
      <Navbar />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="grad" element={<Grad />} />
        </Routes>
      </BrowserRouter>
    </>
  );
};

const App = (): JSX.Element => {
  return (
    <>
      <GlobalStyle />
      <MainRouter />
    </>
  );
};

export default App;
