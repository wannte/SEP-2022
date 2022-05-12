import { createSlice } from "@reduxjs/toolkit";

const MAJOR = {
  EECS: "EECS",
  PYHSICS: "PYHSICS",
};

const initialState = {
  studentId: "20165046",
  major: MAJOR.EECS,
};

export const userSlice = createSlice({
  name: "id",
  initialState,
  reducers: {
    setId: (state, { payload }) => {
      state.studentId = payload.studentId;
    },
  },
});

export const { setId } = userSlice.actions;

export default userSlice.reducer;
