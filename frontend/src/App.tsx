import { BrowserRouter, Route, Routes } from "react-router-dom";
import Navbar from "@components/Navbar";
import Home from "@pages/Home";
import { GlobalStyle } from "@styles/global";
import Grad from "@pages/Select";
import Result from "@pages/Result";

const MainRouter = (): JSX.Element => {
  return (
    <>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="grad" element={<Grad />} />
          <Route path="result" element={<Result />} />
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
