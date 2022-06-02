import API from "@utils/api";
import { useAppSelect } from "./useStore";

export const useHeaders = () => {
  const sid = useAppSelect((select) => select.user.studentId);
  const hs = { "student-id": sid };

  const fetch = async (url: string) => {
    const response = await API.get(url, { headers: hs });
    return response;
  };

  const post = async (url: string, payload: any) => {
    const response = await API.post(url, payload, { headers: hs });
    return response;
  };

  const put = async (url: string, payload: any) => {
    const response = await API.put(url, payload, { headers: hs });
    return response;
  };

  const del = async (url: string) => {
    const response = await API.delete(url, { headers: hs });
    return response;
  };

  return { fetch, post, put, del };
};
