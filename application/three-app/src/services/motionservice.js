import axios from "axios";
const api_addr = "http://127.0.0.1:80/api";

const savemotion = (obj) => {
  return axios({
    method: "post",
    url: `${api_addr}/motion/save`,
    data: obj,
    withCredentials: true,
  });
};

const login = (obj) => {
  return axios({
    method: "post",
    url: `${api_addr}/auth/login`,
    data: {
      email: "test",
      password: "test",
    },
  });
};

export { savemotion };
export { login };
