import React from "react";
import { Route, Routes, Redirect } from 'react-router-dom';
import Home from "../components/Home";
import Error404 from '../components/Error/404';

const AppRouter = (props) => {

  console.log("================================== AppRouter ======================================");

  return (
    <React.Fragment>
      <Routes>
        <Route path="/" exact element={<Home />} />
        <Route component={Error404} />
      </Routes>
    </React.Fragment>
  );
}

export default AppRouter;