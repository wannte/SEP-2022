import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  studentId: "20165046",
  major: null,
};

export const userSlice = createSlice({
  name: "id",
  initialState,
  reducers: {
    setId: (state, { payload }) => {
      state.studentId = payload.studentId;
    },
    setMajor: (state, { payload }) => {
      state.major = payload.major;
    },
  },
});

export const { setId, setMajor } = userSlice.actions;

export default userSlice.reducer;
