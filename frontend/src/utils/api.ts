import axios, { AxiosRequestConfig } from "axios";

const API_URL = "http://localhost:8000";
const config: AxiosRequestConfig = {
  baseURL: API_URL,
  validateStatus: (status: number) => status < 500,
  timeout: 10000,
  withCredentials: true,
};

const API = axios.create(config);

export default API;
