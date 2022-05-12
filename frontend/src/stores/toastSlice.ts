import { createSlice } from "@reduxjs/toolkit";

const initialState = Array<Toast>();

export const toastSlice = createSlice({
  name: "toast",
  initialState,
  reducers: {
    addToast: (state, { payload }) =>
      state.filter((toast) => toast.id !== payload.id).concat(payload),
    popToast: (state, { payload }) =>
      state.filter((toast) => toast.id !== payload.id),
  },
});

export const { addToast, popToast } = toastSlice.actions;

export default toastSlice.reducer;
