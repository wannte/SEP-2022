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

export const fetchLectures = createAsyncThunk(
  "users/lectures/all",
  async (studentId: string, thunkAPI) => {
    const response = await API.get("users/lectures/all", {
      headers: { "student-id": studentId },
    });
    return response.data;
  }
);

interface ResultState {
  data: Result | null;
  lectures: LecturesAll | null;
  loading: "idle" | "pending" | "succeeded" | "failed";
}

const initialState: ResultState = {
  data: null,
  lectures: null,
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
    builder.addCase(fetchLectures.fulfilled, (state, { payload }) => {
      state.lectures = payload;
      state.loading = "succeeded";
    });
    builder.addCase(fetchLectures.pending, (state) => {
      state.loading = "pending";
    });
    builder.addCase(fetchLectures.rejected, (state) => {
      state.loading = "failed";
    });
  },
});

export default resultSlice.reducer;
