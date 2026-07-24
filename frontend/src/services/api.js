import axios from "axios";

const api = axios.create({
  baseURL: "/server/AppSail/api", // Changed to Catalyst endpoint
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;