import API from "@utils/api";
import { useState, useEffect } from "react";

export const useLoadingInterceptor = () => {
  const [isLoading, setIsLoading] = useState(false);
  useEffect(() => {
    const pendingInterceptor = API.interceptors.request.use((config) => {
      setIsLoading(true);
      return config;
    });
    const resolveInterceptor = API.interceptors.response.use(
      (response) => {
        setIsLoading(false);
        return response;
      },
      (error) => {
        setIsLoading(false);
        return error;
      }
    );
    return () => {
      API.interceptors.request.eject(pendingInterceptor);
      API.interceptors.response.eject(resolveInterceptor);
    };
  }, []);
  return isLoading;
};
