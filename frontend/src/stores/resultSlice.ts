import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import API from "@utils/api";

export const fetchResult = createAsyncThunk(
  "users/graduation",
  async (studentId: string, thunkAPI) => {
    const response = await API.get("users/graduation", {
      headers: { "student-id": studentId },
    });
    return response.data;
  }
);

interface ResultState {
  data: Result | null;
  loading: "idle" | "pending" | "succeeded" | "failed";
}

const initialState: ResultState = {
  data: null,
  loading: "idle",
};

const resultSlice = createSlice({
  name: "result",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(fetchResult.fulfilled, (state, { payload }) => {
      state.data = payload;
      state.loading = "succeeded";
    });
    builder.addCase(fetchResult.pending, (state) => {
      state.loading = "pending";
    });
    builder.addCase(fetchResult.rejected, (state) => {
      state.loading = "failed";
    });
  },
});

export default resultSlice.reducer;
